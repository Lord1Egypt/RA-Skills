"""Multi-source reference resolver — arXiv (primary), CrossRef, OpenAlex.

Given a list of RawReference objects extracted from a PDF, attempt to resolve
each one to a full Paper object by querying multiple academic databases.

Resolution priority (S2 removed to avoid rate limits):
  1. arXiv ID → arXiv direct lookup
  2. Title → arXiv search (primary, fast, no rate limit)
  3. Title → CrossRef API (free, no key)
  4. Title → OpenAlex API (free, no key)

Uses ThreadPoolExecutor for parallel resolution.
"""
import os
import re
import sys
import logging
from typing import List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx

from schemas import Paper, RawReference

logger = logging.getLogger(__name__)

CROSSREF_BASE = "https://api.crossref.org/works"
OPENALEX_BASE = "https://api.openalex.org/works"


def _title_similarity(a: str, b: str) -> float:
    """Simple Jaccard similarity on lowered word sets."""
    wa = set(re.sub(r'[^a-z0-9\s]', '', a.lower()).split())
    wb = set(re.sub(r'[^a-z0-9\s]', '', b.lower()).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def _resolve_single(ref: RawReference) -> Optional[Paper]:
    """Resolve a single reference. Thread-safe (no shared state)."""
    paper = None

    # 1. arXiv ID → direct lookup
    if ref.arxiv_id and not paper:
        paper = _resolve_via_arxiv_search(ref.arxiv_id, ref.year)

    # 2. Title → arXiv search (primary source, no rate limit)
    if ref.title and not paper:
        paper = _resolve_via_arxiv_search(ref.title, ref.year)

    # 3. Title → CrossRef (free, no key)
    if ref.title and not paper:
        paper = _resolve_via_crossref(ref.title, ref.authors, ref.year)

    # 4. Title → OpenAlex (free, no key)
    if ref.title and not paper:
        paper = _resolve_via_openalex(ref.title, ref.year)

    return paper


def resolve_references(
    refs: List[RawReference],
    max_refs: int = 60,
    verbose: bool = True,
    max_workers: int = 4,
) -> Tuple[List[Paper], List[dict]]:
    """Resolve a list of raw references to Paper objects (parallel).

    Returns:
        (resolved_papers, unresolved_entries)
    """
    refs_to_resolve = refs[:max_refs]
    total = len(refs_to_resolve)
    resolved = []
    unresolved = []

    # Progress callback
    try:
        from services.graph_server import set_progress
    except ImportError:
        def set_progress(*a, **kw): pass

    if verbose:
        print(f"  [resolver] Resolving {total} references with {max_workers} workers...", file=sys.stderr)

    # Map futures to their index for ordered output
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {}
        for i, ref in enumerate(refs_to_resolve):
            future = executor.submit(_resolve_single, ref)
            future_to_idx[future] = (i, ref)

        done_count = 0
        for future in as_completed(future_to_idx):
            idx, ref = future_to_idx[future]
            done_count += 1
            try:
                paper = future.result()
            except Exception as e:
                paper = None
                logger.debug(f"Resolution failed for ref {idx}: {e}")

            # Update progress: refs resolution is 10%-40% of overall expansion
            pct = 10 + int(30 * done_count / total)
            label = ref.title[:40] if ref.title else f"ref {done_count}"
            set_progress("refs", f"Resolving references: {done_count}/{total} ({label}...)", pct)

            if paper:
                resolved.append(paper)
                if verbose and done_count % 10 == 0:
                    print(f"  [resolver] Progress: {done_count}/{total} done, {len(resolved)} resolved", file=sys.stderr)
            else:
                unresolved.append({
                    "raw_text": ref.raw_text,
                    "title": ref.title,
                    "authors": ref.authors,
                    "year": ref.year,
                    "doi": ref.doi,
                    "arxiv_id": ref.arxiv_id,
                    "source": "pdf_extraction",
                })

    if verbose:
        print(f"  Resolved {len(resolved)}/{total} references "
              f"({len(resolved)/max(total,1)*100:.0f}%)", file=sys.stderr)

    return resolved, unresolved


# ── arXiv resolver (primary) ─────────────────────────────


def _resolve_via_arxiv_search(title: str, year: Optional[int] = None) -> Optional[Paper]:
    """Search arXiv by title with fuzzy matching. Returns Paper with ARXIV:ID."""
    try:
        from services.arxiv import search as arxiv_search
        # Clean query for better arXiv results
        clean = re.sub(r'[:\-,;/()]+', ' ', title).strip()
        clean = re.sub(r'\s+', ' ', clean)
        # Use shorter query if very long
        words = clean.split()
        if len(words) > 10:
            clean = ' '.join(words[:10])
        _, papers = arxiv_search(clean, limit=3)
        for p in papers:
            sim = _title_similarity(title, p.title)
            year_ok = (year is None or p.year is None or abs((p.year or 0) - year) <= 1)
            if sim >= 0.55 and year_ok:
                p.resolved = True
                p.source = "arxiv"
                return p
    except Exception as e:
        logger.debug(f"arXiv search failed for '{title[:30]}': {e}")
    return None


# ── CrossRef resolver ─────────────────────────────────────


def _resolve_via_crossref(title: str, authors: List[str] = None, year: Optional[int] = None) -> Optional[Paper]:
    """CrossRef bibliographic search (free, no API key needed)."""
    try:
        with httpx.Client(timeout=15) as client:
            params = {"query.bibliographic": title, "rows": 3}
            if authors:
                params["query.author"] = " ".join(authors[:2])
            headers = {"User-Agent": "OpenPaperGraph/0.5 (mailto:openpapergraph@users.noreply.github.com)"}
            resp = client.get(CROSSREF_BASE, params=params, headers=headers)
            if resp.status_code == 200:
                items = resp.json().get("message", {}).get("items", [])
                for item in items:
                    cr_title = " ".join(item.get("title", []))
                    sim = _title_similarity(title, cr_title)
                    cr_year = None
                    if item.get("published-print", {}).get("date-parts"):
                        cr_year = item["published-print"]["date-parts"][0][0]
                    elif item.get("published-online", {}).get("date-parts"):
                        cr_year = item["published-online"]["date-parts"][0][0]
                    year_ok = (year is None or cr_year is None or abs(cr_year - year) <= 1)
                    if sim >= 0.6 and year_ok:
                        cr_authors = []
                        for a in (item.get("author") or []):
                            name = f"{a.get('given', '')} {a.get('family', '')}".strip()
                            if name:
                                cr_authors.append(name)
                        return Paper(
                            id=f"crossref:{item.get('DOI', '')}",
                            title=cr_title,
                            authors=cr_authors,
                            year=cr_year,
                            citation_count=item.get("is-referenced-by-count", 0),
                            url=item.get("URL"),
                            resolved=True,
                            source="crossref",
                            doi=item.get("DOI"),
                        )
    except Exception as e:
        logger.debug(f"CrossRef failed for '{title[:30]}': {e}")
    return None


# ── OpenAlex resolver ─────────────────────────────────────


def _resolve_via_openalex(title: str, year: Optional[int] = None) -> Optional[Paper]:
    """OpenAlex search (free, no API key needed)."""
    try:
        with httpx.Client(timeout=15) as client:
            params = {"search": title, "per_page": 3}
            if year:
                params["filter"] = f"publication_year:{year}"
            headers = {"User-Agent": "OpenPaperGraph/0.5 (mailto:openpapergraph@users.noreply.github.com)"}
            resp = client.get(OPENALEX_BASE, params=params, headers=headers)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                for r in results:
                    oa_title = r.get("title", "")
                    sim = _title_similarity(title, oa_title)
                    oa_year = r.get("publication_year")
                    year_ok = (year is None or oa_year is None or abs(oa_year - year) <= 1)
                    if sim >= 0.6 and year_ok:
                        oa_authors = []
                        for a in (r.get("authorships") or []):
                            name = a.get("author", {}).get("display_name", "")
                            if name:
                                oa_authors.append(name)
                        doi = None
                        if r.get("doi"):
                            doi = r["doi"].replace("https://doi.org/", "")
                        oa_id = r.get("id", "").replace("https://openalex.org/", "")
                        return Paper(
                            id=f"openalex:{oa_id}",
                            title=oa_title,
                            authors=oa_authors,
                            year=oa_year,
                            citation_count=r.get("cited_by_count", 0),
                            url=r.get("doi") or r.get("id"),
                            resolved=True,
                            source="openalex",
                            doi=doi,
                        )
    except Exception as e:
        logger.debug(f"OpenAlex failed for '{title[:30]}': {e}")
    return None
