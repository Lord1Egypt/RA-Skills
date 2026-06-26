#!/usr/bin/env python
"""Analyze and summarize PDF content."""

import argparse
import pdfplumber


def analyze_pdf(path: str) -> dict:
    """Analyze PDF structure and content.
    
    Args:
        path: Path to PDF file
    
    Returns:
        Analysis results
    """
    result = {
        "path": path,
        "total_pages": 0,
        "total_chars": 0,
        "total_words": 0,
        "tables_count": 0,
        "page_stats": []
    }
    
    all_text = []
    
    with pdfplumber.open(path) as pdf:
        result["total_pages"] = len(pdf.pages)
        result["metadata"] = {
            "author": pdf.metadata.get("Author", ""),
            "title": pdf.metadata.get("Title", ""),
        }
        
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            tables = page.extract_tables()
            
            chars = len(text)
            words = len(text.split())
            
            result["total_chars"] += chars
            result["total_words"] += words
            result["tables_count"] += len(tables) if tables else 0
            
            result["page_stats"].append({
                "page": i + 1,
                "chars": chars,
                "words": words,
                "tables": len(tables) if tables else 0
            })
            
            all_text.append(text)
    
    # Generate summary
    result["summary"] = {
        "avg_words_per_page": result["total_words"] / max(result["total_pages"], 1),
        "text_density": "high" if result["total_words"] > 5000 else "medium" if result["total_words"] > 1000 else "low"
    }
    
    # First and last page previews
    result["preview"] = {
        "first_page": all_text[0][:500] + "..." if all_text and len(all_text[0]) > 500 else all_text[0] if all_text else "",
        "last_page": all_text[-1][:500] + "..." if all_text and len(all_text[-1]) > 500 else all_text[-1] if len(all_text) > 1 else ""
    }
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Analyze PDF content")
    parser.add_argument("path", help="Path to PDF file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    result = analyze_pdf(args.path)
    
    if args.json:
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n📄 PDF Analysis: {result['path']}")
        print("=" * 50)
        print(f"Total Pages: {result['total_pages']}")
        print(f"Total Words: {result['total_words']:,}")
        print(f"Total Characters: {result['total_chars']:,}")
        print(f"Tables Found: {result['tables_count']}")
        if result['metadata']['title']:
            print(f"Title: {result['metadata']['title']}")
        if result['metadata']['author']:
            print(f"Author: {result['metadata']['author']}")
        print(f"\nAvg Words/Page: {result['summary']['avg_words_per_page']:.0f}")
        print(f"Text Density: {result['summary']['text_density']}")
        print("\n--- Page Breakdown ---")
        for stat in result["page_stats"][:10]:  # Show first 10 pages
            print(f"  Page {stat['page']}: {stat['words']:,} words, {stat['tables']} tables")
        if len(result["page_stats"]) > 10:
            print(f"  ... and {len(result['page_stats']) - 10} more pages")
        
        print("\n--- Preview (First Page) ---")
        print(result["preview"]["first_page"])


if __name__ == "__main__":
    main()
