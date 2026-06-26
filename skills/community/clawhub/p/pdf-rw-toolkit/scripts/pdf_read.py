#!/usr/bin/env python3
"""Extract text, tables, and metadata from PDF files."""

import argparse
import json
import sys
import csv
import io

import pdfplumber
from pypdf import PdfReader


def parse_page_ranges(spec: str, total: int) -> list[int]:
    """Parse page spec like '1,3,5-10' into 0-indexed list."""
    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = max(1, int(start))
            end = min(total, int(end))
            pages.update(range(start - 1, end))
        else:
            idx = int(part) - 1
            if 0 <= idx < total:
                pages.add(idx)
    return sorted(pages)


def show_info(path: str):
    reader = PdfReader(path)
    meta = reader.metadata
    info = {
        "file": path,
        "pages": len(reader.pages),
        "title": getattr(meta, "title", None),
        "author": getattr(meta, "author", None),
        "subject": getattr(meta, "subject", None),
        "creator": getattr(meta, "creator", None),
        "producer": getattr(meta, "producer", None),
        "encrypted": reader.is_encrypted,
    }
    print(json.dumps({k: v for k, v in info.items() if v is not None}, indent=2))


def extract_text(path: str, pages: list[int] | None = None):
    with pdfplumber.open(path) as pdf:
        target = pages if pages else range(len(pdf.pages))
        for i in target:
            if i >= len(pdf.pages):
                continue
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                print(f"--- Page {i + 1} ---")
                print(text)
                print()


def extract_tables(path: str, pages: list[int] | None = None, fmt: str = "csv"):
    with pdfplumber.open(path) as pdf:
        target = pages if pages else range(len(pdf.pages))
        table_num = 0
        all_tables = []
        for i in target:
            if i >= len(pdf.pages):
                continue
            page = pdf.pages[i]
            tables = page.extract_tables()
            for table in tables:
                table_num += 1
                if fmt == "json":
                    # Use first row as headers if possible
                    if len(table) > 1:
                        headers = [str(h) if h else f"col_{j}" for j, h in enumerate(table[0])]
                        rows = [dict(zip(headers, row)) for row in table[1:]]
                    else:
                        rows = table
                    all_tables.append({"page": i + 1, "table": table_num, "data": rows})
                else:
                    print(f"--- Page {i + 1}, Table {table_num} ---")
                    writer = csv.writer(sys.stdout)
                    for row in table:
                        writer.writerow(row)
                    print()
        if fmt == "json":
            print(json.dumps(all_tables, indent=2, ensure_ascii=False))
        if table_num == 0:
            print("No tables found.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Extract text/tables/info from PDF")
    parser.add_argument("file", help="Path to PDF file")
    parser.add_argument("--pages", help="Page range (e.g. 1,3,5-10)")
    parser.add_argument("--tables", action="store_true", help="Extract tables instead of text")
    parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Table output format")
    parser.add_argument("--info", action="store_true", help="Show PDF metadata")
    args = parser.parse_args()

    if args.info:
        show_info(args.file)
        return

    total = len(PdfReader(args.file).pages)
    pages = parse_page_ranges(args.pages, total) if args.pages else None

    if args.tables:
        extract_tables(args.file, pages, args.format)
    else:
        extract_text(args.file, pages)


if __name__ == "__main__":
    main()
