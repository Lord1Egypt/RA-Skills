#!/usr/bin/env python3
"""
Unified HS Code Query Tool for Philippines Tariff.
One-command solution to query HS codes for products exported to Philippines.
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add script directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from suggest_chapter import suggest_chapters


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Query HS codes for products exported to Philippines',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Query by product name
  python3 query_hs_code.py "hair dryer"
  
  # Query with specific chapter hint
  python3 query_hs_code.py "mobile phone" --chapter 85
  
  # Only suggest chapters (no download)
  python3 query_hs_code.py "laptop" --suggest-only
  
  # Use existing PDF file
  python3 query_hs_code.py "charger" --pdf ~/Downloads/Chapter_85.pdf
        '''
    )
    
    parser.add_argument('product', help='Product name or description')
    parser.add_argument('--chapter', type=str, help='Specific chapter number (e.g., 85)')
    parser.add_argument('--pdf', type=str, help='Path to existing PDF file')
    parser.add_argument('--output-dir', type=str, default='~/Desktop/ph-hs-downloads',
                       help='Directory to save downloaded PDFs')
    parser.add_argument('--suggest-only', action='store_true',
                       help='Only suggest chapters, do not download or search')
    parser.add_argument('--max-results', type=int, default=20,
                       help='Maximum search results (default: 20)')
    
    args = parser.parse_args()
    
    print_header(f"Philippines HS Code Query: {args.product}")
    
    # Step 1: Suggest chapters
    print("Step 1: Analyzing product category...")
    suggestion = suggest_chapters(args.product)
    
    print(f"\nProduct: {suggestion['product']}")
    if suggestion['matched_keywords']:
        print(f"Matched keywords: {', '.join(suggestion['matched_keywords'])}")
    
    if not suggestion['suggestions']:
        print("\n⚠️  Could not determine product category automatically.")
        print("Please check the product name or provide a specific chapter number.")
        sys.exit(1)
    
    print("\nSuggested chapters:")
    for i, s in enumerate(suggestion['suggestions'][:5], 1):
        print(f"  {i}. Chapter {s['chapter']}: {s['description']} (score: {s['score']})")
    
    if args.suggest_only:
        return
    
    # Determine which chapter to use
    if args.chapter:
        chapter = args.chapter.zfill(2)
        print(f"\nUsing specified chapter: {chapter}")
    else:
        chapter = suggestion['suggestions'][0]['chapter']
        print(f"\nUsing top suggestion: Chapter {chapter}")
    
    # Step 2: Get PDF
    pdf_path = args.pdf
    source_url = ""
    
    if not pdf_path:
        print(f"\nStep 2: Downloading Chapter {chapter} PDF...")
        
        output_dir = os.path.expanduser(args.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            from get_chapter_pdf import download_chapter
            result = download_chapter(chapter, output_dir)
            
            if result['success']:
                pdf_path = result['file_path']
                source_url = result['source_url']
                print(f"✓ PDF ready: {pdf_path}")
            else:
                print(f"\n✗ Download failed: {result.get('error', 'Unknown error')}")
                if result.get('source_url'):
                    print(f"\nPlease manually download from:")
                    print(f"  {result['source_url']}")
                    print(f"\nThen run again with:")
                    print(f"  python3 query_hs_code.py \"{args.product}\" --pdf ~/Downloads/Chapter_{chapter}.pdf")
                sys.exit(1)
        except ImportError as e:
            print(f"\n✗ Missing dependency: {e}")
            print("Install with: pip install playwright")
            print("Then: playwright install chromium")
            sys.exit(1)
    else:
        print(f"\nStep 2: Using existing PDF: {pdf_path}")
        # Try to infer chapter from filename
        chapter_match = re.search(r'Chapter[_\s]?(\d+)', os.path.basename(pdf_path))
        if chapter_match:
            chapter = chapter_match.group(1).zfill(2)
        source_url = f"https://drive.google.com/file/d/.../view"  # Placeholder
    
    # Step 3: Search HS code
    print(f"\nStep 3: Searching HS codes for \"{args.product}\"...")
    
    try:
        from search_hs_code import extract_hs_codes_from_pdf, format_results_as_markdown, suggest_best_match
        
        # Generate search keywords from product name
        keywords = args.product.split()
        # Add common variations
        if 'hair' in args.product.lower() and 'dryer' in args.product.lower():
            keywords.extend(['blower', 'drying'])
        elif 'phone' in args.product.lower() or 'mobile' in args.product.lower():
            keywords.extend(['telephone', 'smartphone', 'cellular'])
        
        results = extract_hs_codes_from_pdf(pdf_path, keywords, max_results=args.max_results)
        
        if not results:
            print("\n⚠️  No matching HS codes found.")
            print("Try different keywords or check another chapter.")
            sys.exit(1)
        
        print(format_results_as_markdown(results, source_url, args.product))
        
        # Show best match
        best = suggest_best_match(results, keywords)
        if best and best['hs_code']:
            print(f"\n{'='*60}")
            print(f"  ✓ RECOMMENDED HS CODE: {best['hs_code']}")
            print(f"  Description: {best['description'][:80]}...")
            print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"\n✗ Search error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import re  # Need this for the script
    main()
