#!/usr/bin/env python3
"""
Excel 提取与转换
用法：python excel_extract.py --input data.xlsx --output out.csv [--sheet 0]
"""
import argparse
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("请安装: pip install pandas openpyxl")
    sys.exit(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="输入 Excel")
    p.add_argument("--output", "-o", required=True, help="输出 CSV")
    p.add_argument("--sheet", default=0, help="Sheet 索引或名称，默认 0")
    p.add_argument("--limit", type=int, default=0, help="限制行数，0 表示不限制")
    args = p.parse_args()

    sheet = args.sheet
    if isinstance(sheet, str) and sheet.isdigit():
        sheet = int(sheet)

    df = pd.read_excel(args.input, sheet_name=sheet)
    if args.limit > 0:
        df = df.head(args.limit)
    df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"已导出 {len(df)} 行到 {args.output}")


if __name__ == "__main__":
    main()
