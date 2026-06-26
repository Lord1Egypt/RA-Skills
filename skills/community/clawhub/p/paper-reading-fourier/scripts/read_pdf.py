#!/usr/bin/env python3
"""Extract text and basic structure from a PDF file.

Usage:
    python read_pdf.py <pdf_path> [--pages <start-end>] [--output <output_path>]

Uses pdfplumber for text extraction. Outputs markdown-formatted text to stdout
or to a specified output file.
"""

import argparse
import sys


def extract_pdf(pdf_path: str, pages: str = None) -> str:
    try:
        import pdfplumber
    except ImportError:
        print("Error: pdfplumber is not installed. Run: pip install pdfplumber", file=sys.stderr)
        sys.exit(1)

    page_range = None
    if pages:
        try:
            if "-" in pages:
                start, end = pages.split("-", 1)
                page_range = (int(start) - 1, int(end))  # 0-indexed
            else:
                p = int(pages) - 1
                page_range = (p, p + 1)
        except ValueError:
            print(f"Error: Invalid page range format: {pages}", file=sys.stderr)
            sys.exit(1)

    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        start_idx, end_idx = page_range if page_range else (0, total)
        end_idx = min(end_idx, total)

        for i in range(start_idx, end_idx):
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                lines.append(f"\n--- Page {i + 1} ---\n")
                lines.append(text)

            # Extract tables if any
            tables = page.extract_tables()
            for t_idx, table in enumerate(tables):
                lines.append(f"\n[Table {t_idx + 1} on Page {i + 1}]\n")
                for row in table:
                    lines.append("| " + " | ".join(str(c or "") for c in row) + " |")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF file")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--pages", "-p", default=None, help="Page range, e.g. '1-5' or '3'")
    parser.add_argument("--output", "-o", default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    result = extract_pdf(args.pdf_path, args.pages)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Extracted text saved to: {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
