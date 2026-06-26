#!/usr/bin/env python3
"""Split PDF — extract specific pages into a new file."""

import argparse
import sys
from pypdf import PdfReader, PdfWriter


def parse_page_ranges(spec: str, total: int) -> list[int]:
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


def main():
    parser = argparse.ArgumentParser(description="Split PDF by page ranges")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument("--pages", required=True, help="Pages to extract (e.g. 1,3,5-10)")
    args = parser.parse_args()

    reader = PdfReader(args.input)
    pages = parse_page_ranges(args.pages, len(reader.pages))

    writer = PdfWriter()
    for i in pages:
        writer.add_page(reader.pages[i])

    with open(args.output, "wb") as f:
        writer.write(f)

    print(f"Extracted pages {args.pages} → {args.output} ({len(pages)} pages)")


if __name__ == "__main__":
    main()
