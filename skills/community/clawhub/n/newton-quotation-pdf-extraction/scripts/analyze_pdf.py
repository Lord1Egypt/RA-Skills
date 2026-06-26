#!/usr/bin/env python3
"""
Analyze PDF structure and content.
Usage: python analyze_pdf.py <input.pdf>
"""

import argparse
import json
import sys
import pdfplumber


def analyze_pdf(pdf_path):
    """Analyze PDF structure and return metadata."""
    analysis = {
        "file_path": pdf_path,
        "pages": [],
        "total_pages": 0,
        "has_text": False,
        "has_tables": False
    }

    with pdfplumber.open(pdf_path) as pdf:
        analysis["total_pages"] = len(pdf.pages)

        for page_num, page in enumerate(pdf.pages, 1):
            page_info = {
                "page_number": page_num,
                "width": page.width,
                "height": page.height,
                "text_length": 0,
                "word_count": 0,
                "table_count": 0,
                "image_count": len(page.images),
                "char_count": 0
            }

            # Extract text info
            text = page.extract_text()
            if text:
                page_info["text_length"] = len(text)
                page_info["word_count"] = len(text.split())
                page_info["char_count"] = len(text.replace(" ", "").replace("\n", ""))
                analysis["has_text"] = True

            # Extract tables info
            tables = page.extract_tables()
            page_info["table_count"] = len(tables)
            if tables:
                analysis["has_tables"] = True
                page_info["tables"] = [
                    {"rows": len(table), "cols": len(table[0]) if table else 0}
                    for table in tables
                ]

            # Extract words with coordinates
            words = page.extract_words()
            page_info["extracted_words"] = len(words)

            analysis["pages"].append(page_info)

    return analysis


def print_analysis(analysis):
    """Print analysis in human-readable format."""
    print(f"PDF Analysis: {analysis['file_path']}")
    print("=" * 50)
    print(f"Total Pages: {analysis['total_pages']}")
    print(f"Contains Text: {'Yes' if analysis['has_text'] else 'No'}")
    print(f"Contains Tables: {'Yes' if analysis['has_tables'] else 'No'}")
    print()

    for page in analysis["pages"]:
        print(f"Page {page['page_number']}:")
        print(f"  Dimensions: {page['width']:.1f} x {page['height']:.1f} pts")
        print(f"  Text: {page['char_count']} chars, {page['word_count']} words")
        print(f"  Tables: {page['table_count']}")
        print(f"  Images: {page['image_count']}")
        print(f"  Extracted Words: {page['extracted_words']}")

        if "tables" in page:
            for i, table in enumerate(page["tables"], 1):
                print(f"    Table {i}: {table['rows']} rows x {table['cols']} cols")
        print()


def main():
    parser = argparse.ArgumentParser(description="Analyze PDF structure")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    try:
        analysis = analyze_pdf(args.input)

        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            print_analysis(analysis)

    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
