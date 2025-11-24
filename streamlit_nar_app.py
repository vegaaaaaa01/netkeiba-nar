import streamlit as st

from nar_scraper import (
    get_shutuba_by_date_nar,
    export_one_book_all_venues_pretty_to_bytes,
    normalize_ymd,
    NAR_JYO_CD,
)

st.set_page_config(page_title="NAR 出馬表生成", layout="wide")

st.title("地方競馬(NAR) 出馬表生成ツール")

# ▼ プルダウンで競馬場選択
venue_list = list(NAR_JYO_CD.keys())
default_venue = "高知" if "高知" in venue_list else venue_list[0]
place_name = st.selectbox("競馬場を選択してください", options=venue_list, index=venue_list.index(default_venue))

# ▼ 開催日入力
ymd_input = st.text_input("開催日 (YYYYMMDD または YYMMDD)", value="")

if st.button("出馬表を取得してExcelを生成"):
    try:
        ymd = normalize_ymd(ymd_input)
    except ValueError as e:
        st.error(str(e))
    else:
        with st.spinner("出馬表を取得中..."):
            df = get_shutuba_by_date_nar(ymd, place_name)
        if df.empty:
            st.warning("対象日のレースが見つかりませんでした。開催日・競馬場を確認してください。")
        else:
            st.success(f"{place_name} の出馬表を取得しました。行数: {len(df)}")
            excel_bytes = export_one_book_all_venues_pretty_to_bytes(df)
            filename = f"NAR_{place_name}_出馬表_{ymd}.xlsx"
            st.download_button(
                label="出馬表Excelをダウンロード",
                data=excel_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
