"""DBLP API search (sync) — best for CS conference proceedings."""
from typing import List, Tuple, Optional

import httpx

from schemas import Paper

DBLP_API = "https://dblp.org/search/publ/api"

VENUE_KEYS = {
    "ICLR": "iclr", "NeurIPS": "neurips", "ICML": "icml",
    "ACL": "acl", "EMNLP": "emnlp", "NAACL": "naacl",
    "WebConf": "www", "KDD": "kdd",
}


def _parse_hit(hit: dict) -> Optional[Paper]:
    info = hit.get("info", {})
    title = info.get("title", "").rstrip(".")
    if not title:
        return None
    authors_data = info.get("authors", {}).get("author", [])
    if isinstance(authors_data, dict):
        authors_data = [authors_data]
    authors = [a.get("text", a) if isinstance(a, dict) else str(a) for a in authors_data]
    year_str = info.get("year", "")
    year = int(year_str) if str(year_str).isdigit() else None
    doi = info.get("doi", "")
    url = info.get("ee", "") or info.get("url", "")
    paper_id = f"DOI:{doi}" if doi else f"DBLP:{info.get('key', '')}"
    return Paper(id=paper_id, title=title, authors=authors, year=year,
                 url=url or (f"https://doi.org/{doi}" if doi else None))


def search(query: str, limit: int = 20, offset: int = 0, venue: Optional[str] = None) -> Tuple[int, List[Paper]]:
    search_query = query
    if venue:
        keyword = VENUE_KEYS.get(venue, venue.lower())
        search_query = f"{query} {keyword}"
    with httpx.Client(timeout=30) as client:
        resp = client.get(DBLP_API, params={"q": search_query, "format": "json", "h": limit, "f": offset})
        resp.raise_for_status()
    data = resp.json()
    result = data.get("result", {})
    total = int(result.get("hits", {}).get("@total", 0))
    hits = result.get("hits", {}).get("hit", [])
    papers = [p for h in hits if (p := _parse_hit(h))]
    return total, papers
