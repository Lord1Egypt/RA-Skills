"""Google Scholar client — citations, citation counts, and search.

Uses the `scholarly` library for structured access to Google Scholar.
Falls back gracefully if scholarly is not installed or Google blocks requests.

Install: pip install scholarly
"""
import sys
import time
import logging
from typing import List, Optional

from schemas import Paper

logger = logging.getLogger(__name__)

# Rate limiting
_LAST_REQUEST_TIME = 0
_MIN_INTERVAL = 2.0  # seconds between requests


def _rate_limit():
    """Enforce minimum interval between Google Scholar requests."""
    global _LAST_REQUEST_TIME
    now = time.time()
    elapsed = now - _LAST_REQUEST_TIME
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _LAST_REQUEST_TIME = time.time()


def _scholarly():
    """Lazy import scholarly with availability check.

    Returns the scholarly.scholarly object which has search_pubs, citedby, etc.
    """
    try:
        from scholarly import scholarly as _mod
        return _mod
    except ImportError:
        return None


def _parse_scholar_paper(pub: dict) -> Paper:
    """Convert a scholarly publication dict to a Paper object."""
    bib = pub.get("bib", {})
    title = bib.get("title", "")
    authors = bib.get("author", [])
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(" and ")]
    year = None
    year_str = bib.get("pub_year", "")
    if str(year_str).isdigit():
        year = int(year_str)

    citation_count = pub.get("num_citations", 0)
    url = pub.get("pub_url") or pub.get("eprint_url") or ""

    # Generate a stable ID
    scholar_id = pub.get("author_pub_id") or pub.get("cites_id", [""])[0] or ""
    paper_id = f"GS:{scholar_id}" if scholar_id else f"GS:{title[:50]}"

    return Paper(
        id=paper_id,
        title=title,
        authors=authors if isinstance(authors, list) else [authors],
        year=year,
        citation_count=citation_count,
        url=url,
        source="google_scholar",
    )


def search(query: str, limit: int = 10) -> List[Paper]:
    """Search Google Scholar for papers matching query."""
    scholarly = _scholarly()
    if not scholarly:
        logger.debug("scholarly not installed, skipping Google Scholar search")
        return []

    papers = []
    try:
        _rate_limit()
        print(f"[GS] Searching: {query[:50]}...", file=sys.stderr)
        search_query = scholarly.search_pubs(query)
        for i, pub in enumerate(search_query):
            if i >= limit:
                break
            papers.append(_parse_scholar_paper(pub))
            if i < limit - 1:
                _rate_limit()
    except Exception as e:
        print(f"[GS] Search failed: {e}", file=sys.stderr)

    return papers


def get_citations(title: str, limit: int = 50) -> List[Paper]:
    """Get papers that cite a given paper (by title).

    Searches Google Scholar for the paper, then retrieves its citing papers.
    """
    scholarly = _scholarly()
    if not scholarly:
        logger.debug("scholarly not installed, skipping GS citations")
        return []

    try:
        _rate_limit()
        print(f"[GS] Finding citations for: {title[:50]}...", file=sys.stderr)

        # Find the paper first
        search_query = scholarly.search_pubs(title)
        pub = next(search_query, None)
        if not pub:
            print(f"[GS] Paper not found: {title[:50]}", file=sys.stderr)
            return []

        # Get citing papers
        _rate_limit()
        cites = []
        try:
            citedby = scholarly.citedby(pub)
            for i, citing_pub in enumerate(citedby):
                if i >= limit:
                    break
                cites.append(_parse_scholar_paper(citing_pub))
                if i < limit - 1:
                    _rate_limit()
        except Exception as e:
            print(f"[GS] citedby iteration failed: {e}", file=sys.stderr)

        print(f"[GS] Found {len(cites)} citing papers", file=sys.stderr)
        return cites

    except Exception as e:
        print(f"[GS] get_citations failed: {e}", file=sys.stderr)
        return []


def get_citation_count(title: str) -> Optional[int]:
    """Get the citation count for a paper by title."""
    scholarly = _scholarly()
    if not scholarly:
        return None

    try:
        _rate_limit()
        search_query = scholarly.search_pubs(title)
        pub = next(search_query, None)
        if pub:
            return pub.get("num_citations", 0)
    except Exception as e:
        logger.debug(f"GS citation count failed for '{title[:30]}': {e}")

    return None


def enrich_citation_counts(papers: List[Paper]) -> List[Paper]:
    """Batch-enrich citation counts for papers via Google Scholar.

    Only enriches papers that have citation_count == 0 (no existing count).
    Skips if scholarly is not available. Returns papers list (modified in place).
    """
    scholarly = _scholarly()
    if not scholarly:
        return papers

    enriched = 0
    for paper in papers:
        if paper.citation_count and paper.citation_count > 0:
            continue  # Already has citation count
        try:
            count = get_citation_count(paper.title)
            if count is not None and count > 0:
                paper.citation_count = count
                enriched += 1
        except Exception:
            continue
        # Stop after enriching a few to avoid rate limits
        if enriched >= 10:
            break

    if enriched > 0:
        print(f"[GS] Enriched citation counts for {enriched} papers", file=sys.stderr)

    return papers
