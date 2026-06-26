"""arXiv API search (sync)."""
import re
from typing import List, Tuple
from xml.etree import ElementTree

import httpx

from schemas import Paper

ARXIV_API = "https://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def _parse_entry(entry) -> Paper:
    title = (entry.findtext("atom:title", "", NS) or "").strip().replace("\n", " ")
    abstract = (entry.findtext("atom:summary", "", NS) or "").strip().replace("\n", " ")
    authors = [a.findtext("atom:name", "", NS) for a in entry.findall("atom:author", NS)]
    published = entry.findtext("atom:published", "", NS) or ""
    year = int(published[:4]) if len(published) >= 4 else None
    id_url = entry.findtext("atom:id", "", NS) or ""
    arxiv_id = id_url.split("/abs/")[-1] if "/abs/" in id_url else id_url
    # Strip version suffix (e.g., v1, v2) — S2 API doesn't accept versioned IDs
    arxiv_id = re.sub(r'v\d+$', '', arxiv_id)

    return Paper(
        id=f"ARXIV:{arxiv_id}",
        title=title,
        authors=authors,
        year=year,
        citation_count=0,
        abstract=abstract[:1000] if abstract else None,
        url=id_url,
    )


def search(query: str, limit: int = 20, offset: int = 0) -> Tuple[int, List[Paper]]:
    with httpx.Client(timeout=30) as client:
        resp = client.get(ARXIV_API, params={
            "search_query": f"all:{query}",
            "start": offset,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending",
        })
        resp.raise_for_status()

    root = ElementTree.fromstring(resp.text)
    total_str = root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults", "0")
    total = int(total_str) if total_str.isdigit() else 0
    papers = []
    for entry in root.findall("atom:entry", NS):
        try:
            papers.append(_parse_entry(entry))
        except Exception:
            pass
    return total, papers


def get_by_id(arxiv_id: str) -> Paper:
    """Fetch a single paper by arXiv ID (e.g. '2603.15727')."""
    # Strip ARXIV: prefix and version suffix
    raw_id = re.sub(r'^ARXIV:', '', arxiv_id)
    raw_id = re.sub(r'v\d+$', '', raw_id)

    with httpx.Client(timeout=30) as client:
        resp = client.get(ARXIV_API, params={"id_list": raw_id, "max_results": 1})
        resp.raise_for_status()

    root = ElementTree.fromstring(resp.text)
    entries = root.findall("atom:entry", NS)
    for entry in entries:
        # arXiv returns an entry even for invalid IDs, but with no title
        title = (entry.findtext("atom:title", "", NS) or "").strip()
        if title and title != "Error":
            return _parse_entry(entry)
    raise ValueError(f"arXiv paper not found: {arxiv_id}")
