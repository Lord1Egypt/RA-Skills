#!/usr/bin/env python3
"""
Read PDF file and extract text content
Usage: pdf-read.py <file.pdf> [--json] [--pages 1,3,5]
"""
import sys
import argparse
import json
from pathlib import Path

def import_fitz():
    """Import fitz with helpful error message"""
    try:
        import fitz
        return fitz
    except ImportError:
        print("Error: PyMuPDF not installed.", file=sys.stderr)
        print("Install: pip install pymupdf", file=sys.stderr)
        sys.exit(1)

def read_pdf(file_path, pages=None):
    """Read PDF and extract text"""
    fitz = import_fitz()
    
    doc = fitz.open(file_path)
    content = {
        'file': str(file_path),
        'pages': [],
        'total_pages': len(doc),
        'metadata': {
            'title': doc.metadata.get('title', ''),
            'author': doc.metadata.get('author', ''),
            'subject': doc.metadata.get('subject', ''),
            'creator': doc.metadata.get('creator', ''),
        }
    }
    
    # Determine which pages to extract
    if pages:
        page_numbers = [p-1 for p in pages if 1 <= p <= len(doc)]  # Convert to 0-based
    else:
        page_numbers = range(len(doc))
    
    for page_num in page_numbers:
        page = doc[page_num]
        page_content = {
            'number': page_num + 1,
            'text': page.get_text()
        }
        content['pages'].append(page_content)
    
    doc.close()
    return content

def main():
    parser = argparse.ArgumentParser(
        description='Read PDF file and extract text content',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdf-read.py document.pdf
  pdf-read.py document.pdf --json
  pdf-read.py document.pdf --pages 1,3,5
        """
    )
    parser.add_argument('file', help='Input PDF file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--pages', help='Specific pages to extract (e.g., 1,3,5 or 1-5)')
    
    args = parser.parse_args()
    
    # Validate file
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    if not file_path.suffix.lower() == '.pdf':
        print(f"Error: Not a PDF file: {file_path}", file=sys.stderr)
        sys.exit(1)
    
    # Parse pages argument
    pages = None
    if args.pages:
        try:
            if '-' in args.pages:
                start, end = args.pages.split('-')
                pages = list(range(int(start), int(end) + 1))
            else:
                pages = [int(p) for p in args.pages.split(',')]
        except ValueError:
            print("Error: Invalid page format. Use: 1,3,5 or 1-5", file=sys.stderr)
            sys.exit(1)
    
    try:
        content = read_pdf(file_path, pages=pages)
        
        if args.json:
            print(json.dumps(content, indent=2, ensure_ascii=False))
        else:
            # Plain text output
            print(f"File: {content['file']}")
            print(f"Total pages: {content['total_pages']}")
            if content['metadata']['title']:
                print(f"Title: {content['metadata']['title']}")
            if content['metadata']['author']:
                print(f"Author: {content['metadata']['author']}")
            print("\n" + "="*60)
            
            for page in content['pages']:
                print(f"\n--- Page {page['number']} ---")
                print(page['text'])
                        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
