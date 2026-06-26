#!/usr/bin/env python3
"""
Simple PDF text extractor that outputs plain text from PDF files.
Preserves natural reading order using PyPDF2.
"""
import argparse
import sys
import os
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    Returns the full text as a string.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Extract plain text from PDF files."
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output text file (default: stdout)")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: File '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)

    text = extract_text_from_pdf(args.input)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f"Error writing to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Text extracted to '{args.output}'", file=sys.stdout)
    else:
        print(text)


if __name__ == "__main__":
    main()
