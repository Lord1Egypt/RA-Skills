#!/usr/bin/env python
"""Extract text from PDF files using pdfplumber."""

import argparse
import json
import pdfplumber


def extract_pdf(path: str, page_num: int = None) -> dict:
    """Extract text from PDF.
    
    Args:
        path: Path to PDF file
        page_num: Optional specific page number (1-indexed)
    
    Returns:
        Dict with pages and extracted text
    """
    result = {"path": path, "pages": []}
    
    with pdfplumber.open(path) as pdf:
        result["total_pages"] = len(pdf.pages)
        result["metadata"] = {
            "author": pdf.metadata.get("Author", ""),
            "title": pdf.metadata.get("Title", ""),
            "subject": pdf.metadata.get("Subject", ""),
        }
        
        pages_to_process = [page_num - 1] if page_num else range(len(pdf.pages))
        
        for i in pages_to_process:
            if 0 <= i < len(pdf.pages):
                page = pdf.pages[i]
                text = page.extract_text() or ""
                tables = page.extract_tables()
                result["pages"].append({
                    "page": i + 1,
                    "text": text,
                    "tables": tables if tables else []
                })
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF")
    parser.add_argument("path", help="Path to PDF file")
    parser.add_argument("--page", type=int, help="Specific page number (1-indexed)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    result = extract_pdf(args.path, args.page)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"PDF: {result['path']}")
        print(f"Pages: {result['total_pages']}")
        if result['metadata']['title']:
            print(f"Title: {result['metadata']['title']}")
        print("-" * 50)
        for page in result["pages"]:
            print(f"\n--- Page {page['page']} ---\n")
            print(page["text"])
            if page["tables"]:
                print(f"\n[Found {len(page['tables'])} table(s)]")


if __name__ == "__main__":
    main()
