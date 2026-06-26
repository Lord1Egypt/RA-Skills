#!/usr/bin/env python3
"""Search text inside a PDF and print matching snippets.

Requirements:
  python -m pip install pymupdf

Usage:
  python tools/pdf/search_pdf.py input.pdf "transformer"
  python tools/pdf/search_pdf.py input.pdf "error code" --ignore-case --context 80
  python tools/pdf/search_pdf.py input.pdf "foo|bar" --regex
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re

import fitz  # PyMuPDF


def make_pattern(query: str, regex: bool, ignore_case: bool) -> re.Pattern[str]:
    flags = re.IGNORECASE if ignore_case else 0
    source = query if regex else re.escape(query)
    return re.compile(source, flags)


def snippet(text: str, start: int, end: int, context: int) -> str:
    left = max(0, start - context)
    right = min(len(text), end + context)
    s = text[left:right].replace("\n", " ").strip()
    return re.sub(r"\s+", " ", s)


def search_pdf(pdf_path: Path, query: str, regex: bool = False, ignore_case: bool = False, context: int = 80) -> int:
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    pattern = make_pattern(query, regex=regex, ignore_case=ignore_case)
    matches = 0

    doc = fitz.open(str(pdf_path))
    try:
        for i in range(doc.page_count):
            page = doc.load_page(i)
            text = page.get_text("text")
            if not text.strip():
                continue
            for m in pattern.finditer(text):
                matches += 1
                print(f"page {i + 1}: {snippet(text, m.start(), m.end(), context)}")
    finally:
        doc.close()

    print(f"total_matches={matches}")
    return 0 if matches else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", type=Path, help="Input PDF path")
    ap.add_argument("query", help="Search string or regex")
    ap.add_argument("--regex", action="store_true", help="Treat query as regex")
    ap.add_argument("--ignore-case", action="store_true", help="Case-insensitive search")
    ap.add_argument("--context", type=int, default=80, help="Snippet chars around each match (default: 80)")
    args = ap.parse_args()

    return search_pdf(
        args.pdf,
        args.query,
        regex=args.regex,
        ignore_case=args.ignore_case,
        context=args.context,
    )


if __name__ == "__main__":
    raise SystemExit(main())
