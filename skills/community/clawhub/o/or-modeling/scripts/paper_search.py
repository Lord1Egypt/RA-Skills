#!/usr/bin/env python3
"""
Paper Search Tool - Query academic papers from OpenAlex and Semantic Scholar APIs

Usage:
    python paper_search.py "taxi dispatch optimization" --max-results 5
    python paper_search.py "vehicle routing problem" --source openalex --max-results 10
    python paper_search.py "ride sharing matching" --source semantic_scholar --max-results 5

Features:
    - Retry logic with exponential backoff for rate limiting (429 errors)
    - Graceful degradation: if one API fails, continue with the other
    - Deduplication and citation-based ranking
"""

import argparse
import sys
import time
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required. Install with: pip install requests")
    sys.exit(1)


# API Endpoints
OPENALEX_API = "https://api.openalex.org/works"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"

# Retry configuration
MAX_RETRIES = 3
INITIAL_BACKOFF = 1  # seconds


def search_with_retry(api_url: str, params: dict, headers: dict,
                      source_name: str) -> Optional[dict]:
    """Execute API request with retry logic for rate limiting.

    Returns:
        JSON response data if successful, None if all retries fail.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(api_url, params=params, headers=headers, timeout=30)

            if response.status_code == 429:
                # Rate limited - exponential backoff
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                print(f"   ⚠️  Rate limited (429). Retrying in {backoff}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(backoff)
                continue

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                print(f"   ⚠️  {source_name} error: {e}. Retrying in {backoff}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(backoff)
            else:
                print(f"   ❌ {source_name} API failed after {MAX_RETRIES} attempts: {e}")
                return None

    return None


def search_openalex(query: str, max_results: int = 5) -> list[dict]:
    """Search papers via OpenAlex API"""
    params = {
        "search": query,
        "per-page": max_results,
    }

    headers = {"Accept": "application/json"}

    data = search_with_retry(OPENALEX_API, params, headers, "OpenAlex")
    if not data:
        return []

    results = []
    for work in data.get("results", []):
        # Reconstruct abstract from inverted index if available
        abstract = ""
        if work.get("abstract_inverted_index"):
            words = []
            inv_index = work["abstract_inverted_index"]
            for word, positions in inv_index.items():
                for pos in positions:
                    words.append((pos, word))
            words.sort(key=lambda x: x[0])
            abstract = " ".join(w[1] for w in words)

        authors = [a["author"]["display_name"] for a in work.get("authorships", [])[:3]]
        concepts = [c["display_name"] for c in work.get("concepts", [])[:5]]
        cited_by = work.get("cited_by_count", 0)

        doi = "N/A"
        if work.get("doi"):
            doi = work["doi"].replace("https://doi.org/", "")

        results.append({
            "title": work.get("title", "N/A") or work.get("display_name", "N/A"),
            "authors": authors,
            "year": work.get("publication_year", "N/A"),
            "abstract": abstract[:500] + "..." if len(abstract) > 500 else abstract,
            "citations": cited_by,
            "doi": doi,
            "concepts": concepts,
            "source": "OpenAlex"
        })

    return results


def search_semantic_scholar(query: str, max_results: int = 5) -> list[dict]:
    """Search papers via Semantic Scholar Graph API"""
    params = {
        "query": query,
        "limit": max_results,
        "sort": "relevance",
        "fields": "title,authors,year,abstract,citationCount,externalIds"
    }

    headers = {"Accept": "application/json"}

    data = search_with_retry(SEMANTIC_SCHOLAR_API, params, headers, "Semantic Scholar")
    if not data:
        return []

    results = []
    for paper in data.get("data", []):
        authors = [a["name"] for a in paper.get("authors", [])[:3]]
        external_ids = paper.get("externalIds", {})

        results.append({
            "title": paper.get("title", "N/A"),
            "authors": authors,
            "year": paper.get("year", "N/A"),
            "abstract": (paper.get("abstract", "") or "N/A")[:500],
            "citations": paper.get("citationCount", 0),
            "doi": external_ids.get("DOI", "N/A"),
            "arxiv_id": external_ids.get("ArXiv", "N/A"),
            "ss_id": paper.get("paperId", "N/A"),
            "source": "Semantic Scholar"
        })

    return results


def format_paper_result(paper: dict, index: int) -> str:
    """Format a single paper result for display"""
    lines = [
        f"\n{'='*60}",
        f"[{index}] {paper['title']}",
        f"{'='*60}",
        f"Authors: {', '.join(paper['authors']) if paper['authors'] else 'N/A'}",
        f"Year: {paper['year']}",
        f"Citations: {paper['citations']}",
        f"Source: {paper.get('source', 'N/A')}",
    ]

    if paper.get("doi") and paper["doi"] != "N/A":
        lines.append(f"DOI: {paper['doi']}")

    if paper.get("arxiv_id") and paper["arxiv_id"] != "N/A":
        lines.append(f"arXiv: {paper['arxiv_id']}")

    if paper.get("concepts"):
        lines.append(f"Concepts: {', '.join(paper['concepts'])}")

    if paper.get("abstract") and paper["abstract"] != "N/A":
        lines.append(f"\nAbstract: {paper['abstract']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search academic papers from OpenAlex and Semantic Scholar",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python paper_search.py "taxi dispatch optimization" --max-results 5
    python paper_search.py "vehicle routing" --source openalex
    python paper_search.py "ride sharing" --source semantic_scholar --max-results 10
        """
    )

    parser.add_argument("query", type=str, help="Search query string")
    parser.add_argument("--max-results", type=int, default=5,
                        help="Maximum number of results per API (default: 5)")
    parser.add_argument("--source", type=str,
                        choices=["openalex", "semantic_scholar", "both"],
                        default="both",
                        help="API source to use (default: both)")

    args = parser.parse_args()

    if not args.query.strip():
        print("Error: Query cannot be empty")
        sys.exit(1)

    print(f"\n🔍 Searching for: \"{args.query}\"")
    print(f"   Max results per source: {args.max_results}")

    all_results = []
    sources_searched = []

    if args.source in ["openalex", "both"]:
        print("\n📚 Searching OpenAlex...")
        openalex_results = search_openalex(args.query, args.max_results)
        all_results.extend(openalex_results)
        sources_searched.append("OpenAlex")
        print(f"   Found {len(openalex_results)} papers")

    if args.source in ["semantic_scholar", "both"]:
        print("\n📚 Searching Semantic Scholar...")
        ss_results = search_semantic_scholar(args.query, args.max_results)
        all_results.extend(ss_results)
        sources_searched.append("Semantic Scholar")
        print(f"   Found {len(ss_results)} papers")

    if not all_results:
        print("\n❌ No papers found from any source. Suggestions:")
        print("   - Try different keywords")
        print("   - Check your internet connection")
        print("   - Wait a moment and retry (rate limiting)")
        sys.exit(1)

    # Sort by citations (descending)
    all_results.sort(key=lambda x: x.get("citations", 0), reverse=True)

    # Deduplicate by title (case-insensitive)
    seen_titles = set()
    unique_results = []
    for r in all_results:
        title_lower = r["title"].lower()
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_results.append(r)

    print(f"\n\n{'#'*60}")
    print(f"# SEARCH RESULTS ({len(unique_results)} unique papers from {', '.join(sources_searched)})")
    print(f"{'#'*60}")

    for i, paper in enumerate(unique_results, 1):
        print(format_paper_result(paper, i))

    # Summary
    print(f"\n\n{'#'*60}")
    print("# RESEARCH INSIGHTS SUMMARY")
    print(f"{'#'*60}")

    # Extract common themes
    all_concepts = []
    for paper in unique_results:
        if paper.get("concepts"):
            all_concepts.extend(paper["concepts"])

    if all_concepts:
        from collections import Counter
        concept_counts = Counter(all_concepts)
        top_concepts = concept_counts.most_common(5)
        print("\n📊 Top research themes:")
        for concept, count in top_concepts:
            print(f"   • {concept} ({count} papers)")

    print("\n✅ Most cited papers (key references):")
    sorted_by_citations = sorted(unique_results, key=lambda x: x.get("citations", 0), reverse=True)
    for i, paper in enumerate(sorted_by_citations[:3], 1):
        title = paper['title'][:55] + "..." if len(paper['title']) > 55 else paper['title']
        print(f"   {i}. \"{title}\" - {paper['citations']} citations")

    # API status summary
    print("\n📡 API Status:")
    for source in sources_searched:
        count = len([r for r in unique_results if r.get("source") == source])
        print(f"   • {source}: {count} papers")

    print("\n" + "="*60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
