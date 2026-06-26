#!/usr/bin/env python3
"""
PDF 文本与表格提取
用法：python pdf_extract.py --input file.pdf [--page 0] [--tables]
"""
import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("请安装: pip install pdfplumber")
    sys.exit(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="输入 PDF")
    p.add_argument("--page", type=int, default=None, help="指定页码，默认全部")
    p.add_argument("--tables", action="store_true", help="提取表格")
    args = p.parse_args()

    with pdfplumber.open(args.input) as pdf:
        pages = [args.page] if args.page is not None else range(len(pdf.pages))
        for i in pages:
            page = pdf.pages[i]
            if args.tables:
                tables = page.extract_tables()
                for j, t in enumerate(tables):
                    print(f"--- Page {i+1} Table {j+1} ---")
                    for row in t:
                        print(row)
            else:
                text = page.extract_text()
                if text:
                    print(f"--- Page {i+1} ---")
                    print(text)


if __name__ == "__main__":
    main()
