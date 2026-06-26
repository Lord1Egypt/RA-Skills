#!/usr/bin/env python3
"""
PubMed Fetch - Batch retrieve articles by PMID

Fetch full article details from PubMed given a list of PMIDs.

Usage:
    python pubmed_fetch.py PMID1 PMID2 PMID3 ...
    python pubmed_fetch.py --file pmids.txt
    python pubmed_fetch.py 12345678 --format summary
"""

import os
import sys
import json
import argparse
from typing import List, Optional

# Import from pubmed_search
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pubmed_search import (
    fetch_articles, get_api_key, format_output
)


def read_pmids_from_file(filepath: str) -> List[str]:
    """Read PMIDs from file (one per line)."""
    pmids = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if line and line.isdigit():
                pmids.append(line)
    return pmids


def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed articles by PMID",
        epilog="""
Examples:
    %(prog)s 12345678 98765432
    %(prog)s --file pmids.txt --output results.json
    %(prog)s 12345678 --format summary
        """
    )
    
    parser.add_argument("pmids", nargs="*", help="PMIDs to fetch")
    parser.add_argument("--file", "-f", help="File containing PMIDs (one per line)")
    parser.add_argument("--format", choices=["json", "summary"], default="json")
    parser.add_argument("--output", "-o", help="Save to file")
    parser.add_argument("--api-key", help="NCBI API key")
    
    args = parser.parse_args()
    
    # Collect PMIDs
    pmids = args.pmids
    if args.file:
        pmids.extend(read_pmids_from_file(args.file))
    
    if not pmids:
        print("Error: No PMIDs provided", file=sys.stderr)
        sys.exit(1)
    
    # Validate PMIDs
    pmids = [p for p in pmids if p.isdigit()]
    
    if not pmids:
        print("Error: No valid PMIDs found", file=sys.stderr)
        sys.exit(1)
    
    api_key = get_api_key(args)
    
    print(f"Fetching {len(pmids)} articles...", file=sys.stderr)
    
    # Fetch
    articles = fetch_articles(pmids, api_key)
    
    # Format
    output = format_output(articles, len(articles), "PMID fetch", args.format)
    
    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()