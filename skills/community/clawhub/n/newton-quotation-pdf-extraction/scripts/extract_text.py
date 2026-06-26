#!/usr/bin/env python3
"""
Extract text from PDF file.
Usage: python extract_text.py <input.pdf> [--pages START END] [--output output.txt]
"""

import argparse
import sys
import pdfplumber


def extract_text(pdf_path, start_page=None, end_page=None):
    """Extract text from PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)

        start = (start_page or 1) - 1
        end = end_page or total_pages

        text_parts = []
        for i in range(start, min(end, total_pages)):
            page_text = pdf.pages[i].extract_text()
            if page_text:
                text_parts.append(f"--- Page {i + 1} ---\n{page_text}")

        return "\n\n".join(text_parts)


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("--pages", nargs=2, type=int, metavar=("START", "END"),
                        help="Page range to extract (1-indexed)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")

    args = parser.parse_args()

    try:
        start_page = args.pages[0] if args.pages else None
        end_page = args.pages[1] if args.pages else None

        text = extract_text(args.input, start_page, end_page)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Text extracted to: {args.output}", file=sys.stderr)
        else:
            print(text)

    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
