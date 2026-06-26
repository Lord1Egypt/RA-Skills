#!/usr/bin/env python3
"""Extract readable text from a PDF, optionally preserving page boundaries.

Requirements:
  python -m pip install pymupdf

Usage:
  python tools/pdf/extract_pdf_text.py input.pdf
  python tools/pdf/extract_pdf_text.py input.pdf --output out.txt
  python tools/pdf/extract_pdf_text.py input.pdf --pages 1-3,5 --page-breaks
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import fitz  # PyMuPDF


def parse_pages(spec: str | None, page_count: int) -> list[int]:
    if not spec:
        return list(range(page_count))

    selected: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                start, end = end, start
            for p in range(start, end + 1):
                if 1 <= p <= page_count:
                    selected.add(p - 1)
        else:
            p = int(chunk)
            if 1 <= p <= page_count:
                selected.add(p - 1)
    return sorted(selected)


def extract_text(pdf_path: Path, pages: str | None = None, page_breaks: bool = False) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    doc = fitz.open(str(pdf_path))
    try:
        page_indexes = parse_pages(pages, doc.page_count)
        chunks: list[str] = []
        for idx in page_indexes:
            page = doc.load_page(idx)
            text = page.get_text("text").strip()
            if page_breaks:
                chunks.append(f"\n===== PAGE {idx + 1} =====\n")
            chunks.append(text)
        return "\n\n".join(c for c in chunks if c != "")
    finally:
        doc.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path, help="Input PDF path")
    ap.add_argument("--output", "-o", type=Path, help="Optional output text file path")
    ap.add_argument("--pages", help="Page selection, e.g. 1-3,5")
    ap.add_argument("--page-breaks", action="store_true", help="Insert visible page separators")
    args = ap.parse_args()

    text = extract_text(args.pdf, pages=args.pages, page_breaks=args.page_breaks)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"saved {args.output}")
    else:
        sys.stdout.write(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
