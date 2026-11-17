#!/usr/bin/env python3
"""pdf_extract_tables.py — 表格提取到 CSV / Excel（能力 #6）

用法：
  python3 pdf_extract_tables.py in.pdf --xlsx out.xlsx   # 多表多 sheet
  python3 pdf_extract_tables.py in.pdf --csv-dir ./csv   # 每表一个 CSV
  python3 pdf_extract_tables.py in.pdf --pages 1-10 --xlsx out.xlsx
"""
import argparse, os, sys

def extract(path, pages_spec):
    import pdfplumber
    tables = []
    with pdfplumber.open(path) as pdf:
        ids = range(len(pdf.pages))
        if pages_spec:
            a, b = (int(x) for x in pages_spec.split("-"))
            ids = range(a - 1, min(b, len(pdf.pages)))
        for pid in ids:
            for ti, tbl in enumerate(pdf.pages[pid].extract_tables()):
                if tbl and len(tbl) > 1:
                    tables.append({"page": pid + 1, "index": ti + 1, "rows": tbl})
    return tables

def main():
    ap = argparse.ArgumentParser(description="PDF 表格提取")
    ap.add_argument("pdf")
    ap.add_argument("--xlsx", help="输出 Excel（每表一 sheet）")
    ap.add_argument("--csv-dir", help="输出 CSV 目录")
    ap.add_argument("--pages", help='页范围 "1-10"')
    a = ap.parse_args()
    if not a.xlsx and not a.csv_dir:
        ap.error("需指定 --xlsx 或 --csv-dir")
    tables = extract(a.pdf, a.pages)
    if not tables:
        print("⚠️ 未检出表格。无框线表格请走坐标聚类管道；扫描件请先 OCR（见 capabilities-value.md #6）")
        sys.exit(2)
    import pandas as pd
    for t in tables:
        t["df"] = pd.DataFrame(t["rows"][1:], columns=[str(c or f"col{i}") for i, c in enumerate(t["rows"][0])])
    if a.xlsx:
        with pd.ExcelWriter(a.xlsx, engine="openpyxl") as w:
            for i, t in enumerate(tables, 1):
                t["df"].to_excel(w, sheet_name=f"p{t['page']}_表{t['index']}"[:31], index=False)
        print(f"✅ {len(tables)} 个表格 → {a.xlsx}")
    if a.csv_dir:
        os.makedirs(a.csv_dir, exist_ok=True)
        for t in tables:
            p = os.path.join(a.csv_dir, f"p{t['page']}_表{t['index']}.csv")
            t["df"].to_csv(p, index=False, encoding="utf-8-sig")
        print(f"✅ {len(tables)} 个表格 → {a.csv_dir}/")
    print("质检提示：请抽核 ≥10% 行数值与原文比对；合并单元格区域建议目检")

if __name__ == "__main__":
    main()
