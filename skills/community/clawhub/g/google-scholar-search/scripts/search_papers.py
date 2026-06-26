#!/usr/bin/env python3
"""
Academic Paper Search using Semantic Scholar API
Free and open access to academic papers
"""

import sys
import json
import urllib.request
import urllib.parse
import time
from typing import List, Dict, Optional

BASE_URL = "https://api.semanticscholar.org/graph/v1"
HEADERS = {
    'User-Agent': 'OpenClaw-GoogleScholarSearch/1.0'
}

def make_request(url: str, retries: int = 3) -> Optional[Dict]:
    """Make HTTP request with retry logic."""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limit
                wait_time = (attempt + 1) * 2
                print(f"Rate limit hit. Waiting {wait_time} seconds...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"Error (attempt {attempt + 1}): {str(e)}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(1)
    return None

def search_papers(
    query: str,
    limit: int = 10,
    fields: str = "paperId,title,abstract,authors,year,citationCount,url,openAccessPdf,venue",
    year: Optional[str] = None,
    min_citation_count: Optional[int] = None,
    publication_type: Optional[str] = None  # "JournalArticle", "Conference", "Book"
) -> List[Dict]:
    """
    Search for academic papers using Semantic Scholar API.

    Args:
        query: Search query string
        limit: Number of results to return (max 100)
        fields: Comma-separated list of fields to return
        year: Filter by year (e.g., "2023" or "2020-2023")
        min_citation_count: Minimum citation count filter
        publication_type: Type of publication

    Returns:
        List of paper dictionaries
    """
    # Build request URL
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": fields
    }

    if year:
        params["year"] = year
    if min_citation_count:
        params["minCitationCount"] = min_citation_count
    if publication_type:
        params["publicationTypes"] = publication_type

    url = f"{BASE_URL}/paper/search?{urllib.parse.urlencode(params)}"

    data = make_request(url)
    if data:
        return data.get('data', [])
    return []

def get_paper_details(paper_id: str, fields: str = "paperId,title,abstract,authors,year,citationCount,references,citations,url,openAccessPdf") -> Optional[Dict]:
    """
    Get detailed information about a specific paper.

    Args:
        paper_id: Semantic Scholar paper ID
        fields: Comma-separated list of fields to return

    Returns:
        Paper dictionary or None if not found
    """
    url = f"{BASE_URL}/paper/{paper_id}?fields={urllib.parse.quote(fields)}"
    return make_request(url)

def format_paper(paper: Dict) -> str:
    """Format a paper for display."""
    title = paper.get('title', 'No title')
    authors = ', '.join([a.get('name', '') for a in paper.get('authors', [])[:5]])
    if len(paper.get('authors', [])) > 5:
        authors += ' et al.'
    year = paper.get('year', 'N/A')
    venue = paper.get('venue', 'Unknown venue')
    citations = paper.get('citationCount', 0)
    abstract = paper.get('abstract', 'No abstract available')
    url = paper.get('url', '')

    output = f"""
Title: {title}
Authors: {authors}
Year: {year}
Venue: {venue}
Citations: {citations}

Abstract:
{abstract}

URL: {url}
---
"""
    return output

def format_papers_json(papers: List[Dict]) -> str:
    """Format papers as JSON for machine processing."""
    return json.dumps(papers, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print("Usage: search_papers.py <query> [--limit N] [--year YYYY-YYYY] [--min-citations N] [--json] [--details paper-id]")
        print("\nExamples:")
        print("  search_papers.py 'machine learning transformers'")
        print("  search_papers.py 'deep learning' --limit 5 --year 2020-2023")
        print("  search_papers.py 'quantum computing' --min-citations 10")
        print("  search_papers.py 'artificial intelligence' --details <paper-id>")
        sys.exit(1)

    # Parse arguments
    query = sys.argv[1]
    limit = 10
    year = None
    min_citations = None
    output_json = False
    paper_id = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--year' and i + 1 < len(sys.argv):
            year = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--min-citations' and i + 1 < len(sys.argv):
            min_citations = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--json':
            output_json = True
            i += 1
        elif sys.argv[i] == '--details' and i + 1 < len(sys.argv):
            paper_id = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    # Get paper details if paper_id is provided
    if paper_id:
        paper = get_paper_details(paper_id)
        if paper:
            if output_json:
                print(format_papers_json([paper]))
            else:
                print(format_paper(paper))
        else:
            print(f"Paper not found: {paper_id}", file=sys.stderr)
        return

    # Search for papers
    papers = search_papers(
        query=query,
        limit=limit,
        year=year,
        min_citation_count=min_citations
    )

    if not papers:
        print(f"No papers found for query: {query}", file=sys.stderr)
        sys.exit(1)

    # Output results
    if output_json:
        print(format_papers_json(papers))
    else:
        print(f"Found {len(papers)} papers:\n")
        for paper in papers:
            print(format_paper(paper))

if __name__ == "__main__":
    main()
