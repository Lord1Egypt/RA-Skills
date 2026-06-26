"""Multi-source academic paper API — search, details, references, citations, recommendations.

Primary sources: arXiv, DBLP, Google Scholar
Fallback: Semantic Scholar (S2) API
Recommendations: S2 only (unique feature)

All public functions maintain the same interface as before for backward compatibility.
"""
import os
import sys
import time
import logging
from typing import List, Tuple, Optional

import httpx

from schemas import Paper

logger = logging.getLogger(__name__)

S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_RECOMMEND = "https://api.semanticscholar.org/recommendations/v1"
PAPER_FIELDS = "paperId,title,authors,year,citationCount,abstract,url,externalIds"
PAPER_FIELDS_BASIC = "paperId,title,authors,year,citationCount,abstract,url"
PAPER_FIELDS_WITH_REFS = f"{PAPER_FIELDS},references,citations"


# ── S2 internal helpers (kept as fallback) ───────────────


def _headers():
    h = {}
    key = os.environ.get("S2_API_KEY", "")
    if key:
        h["x-api-key"] = key
    return h


def _request(method, url, max_retries=3, **kwargs):
    kwargs.setdefault("headers", _headers())
    kwargs.setdefault("timeout", 30)
    with httpx.Client() as client:
        for attempt in range(max_retries):
            resp = client.request(method, url, **kwargs)
            if resp.status_code == 429:
                wait = 2 ** attempt + 1
                print(f"[S2] Rate limited, retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        resp = client.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp


def _parse_paper(data: dict) -> Paper:
    ext_ids = data.get("externalIds") or {}
    arxiv_id = ext_ids.get("ArXiv")
    doi = ext_ids.get("DOI")
    pdf_url = None
    if arxiv_id:
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    return Paper(
        id=data.get("paperId", ""),
        title=data.get("title", ""),
        authors=[a.get("name", "") for a in (data.get("authors") or [])],
        year=data.get("year"),
        citation_count=data.get("citationCount", 0),
        abstract=data.get("abstract"),
        url=data.get("url"),
        doi=doi,
        arxiv_id=arxiv_id,
        pdf_url=pdf_url,
    )


def _s2_search(query: str, limit: int = 20, offset: int = 0, max_retries: int = 3) -> Tuple[int, List[Paper]]:
    """Direct S2 search (internal)."""
    resp = _request("GET", f"{S2_BASE}/paper/search",
                     max_retries=max_retries,
                     params={"query": query, "limit": limit, "offset": offset, "fields": PAPER_FIELDS})
    data = resp.json()
    return data.get("total", 0), [_parse_paper(p) for p in (data.get("data") or [])]


def _s2_get_paper_detail(paper_id: str) -> Paper:
    """Get paper detail from S2 (internal)."""
    resp = _request("GET", f"{S2_BASE}/paper/{paper_id}", params={"fields": PAPER_FIELDS})
    return _parse_paper(resp.json())


def _s2_get_references(paper_id: str, limit: int = 100) -> List[Paper]:
    """Get references from S2 (internal)."""
    resp = _request("GET", f"{S2_BASE}/paper/{paper_id}/references",
                     params={"fields": PAPER_FIELDS_BASIC, "limit": limit})
    data = resp.json()
    return [_parse_paper(item["citedPaper"]) for item in (data.get("data") or [])
            if item.get("citedPaper", {}).get("paperId")]


def _s2_get_citations(paper_id: str, limit: int = 100) -> List[Paper]:
    """Get citations from S2 (internal)."""
    resp = _request("GET", f"{S2_BASE}/paper/{paper_id}/citations",
                     params={"fields": PAPER_FIELDS_BASIC, "limit": limit})
    data = resp.json()
    return [_parse_paper(item["citingPaper"]) for item in (data.get("data") or [])
            if item.get("citingPaper", {}).get("paperId")]


def _s2_search_recent(query: str, year_from: int = 2024, limit: int = 20) -> List[Paper]:
    """S2 recent search (internal)."""
    resp = _request("GET", f"{S2_BASE}/paper/search",
                     params={"query": query, "limit": limit, "fields": PAPER_FIELDS,
                             "year": f"{year_from}-", "sort": "citationCount:desc"})
    data = resp.json()
    return [_parse_paper(p) for p in (data.get("data") or [])]


# ── Deduplication helper ─────────────────────────────────


def _dedup_papers(all_papers: List[Paper], limit: int) -> List[Paper]:
    """Deduplicate papers by normalized title, sort by citation count."""
    seen = set()
    unique = []
    for p in all_papers:
        norm = p.title.lower().strip().rstrip(".")
        if norm and norm not in seen:
            seen.add(norm)
            unique.append(p)
    unique.sort(key=lambda p: p.citation_count or 0, reverse=True)
    return unique[:limit]


# ══════════════════════════════════════════════════════════
#  PUBLIC API — multi-source with S2 fallback
# ══════════════════════════════════════════════════════════


def search(query: str, limit: int = 20, offset: int = 0) -> Tuple[int, List[Paper]]:
    """Multi-source search: arXiv + DBLP + S2, deduplicated and sorted by citations."""
    from services import arxiv, dblp

    all_papers = []
    total = 0

    # 1. arXiv (prioritized)
    try:
        t, papers = arxiv.search(query, limit=limit)
        total += t
        all_papers.extend(papers)
    except Exception as e:
        print(f"[search] arXiv failed: {e}", file=sys.stderr)

    # 2. DBLP
    try:
        t, papers = dblp.search(query, limit=limit)
        total += t
        all_papers.extend(papers)
    except Exception as e:
        print(f"[search] DBLP failed: {e}", file=sys.stderr)

    # 3. S2 (provides citation counts + broader coverage)
    try:
        t, papers = _s2_search(query, limit=limit, offset=offset)
        total += t
        all_papers.extend(papers)
    except Exception as e:
        print(f"[search] S2 failed: {e}", file=sys.stderr)

    return total, _dedup_papers(all_papers, limit)


def get_paper(paper_id: str) -> dict:
    """Get paper detail with references and citations.

    - Detail: S2 → arXiv fallback
    - References: download PDF → parse reference list → fallback S2
    - Citations: Google Scholar → fallback S2
    """
    # Basic info: S2 first, arXiv fallback
    print(f"[get_paper] Fetching detail: {paper_id}", file=sys.stderr)
    paper = None
    try:
        paper = _s2_get_paper_detail(paper_id)
    except Exception as e:
        print(f"[get_paper] S2 detail failed: {e}", file=sys.stderr)

    if not paper:
        # Fallback: arXiv direct ID lookup or title search
        from services import arxiv as arxiv_svc
        if paper_id.startswith("ARXIV:"):
            try:
                paper = arxiv_svc.get_by_id(paper_id)
                print(f"[get_paper] Got detail from arXiv fallback (ID): {paper.title}", file=sys.stderr)
            except Exception as e2:
                print(f"[get_paper] arXiv fallback (ID) failed: {e2}", file=sys.stderr)

        if not paper:
            # Search arXiv by title
            try:
                from services.reference_resolver import _title_similarity
                _, arxiv_results = arxiv_svc.search(paper_id, limit=5)
                for ap in arxiv_results:
                    if _title_similarity(paper_id, ap.title) >= 0.6:
                        paper = ap
                        print(f"[get_paper] Got detail from arXiv fallback (search): {paper.title}", file=sys.stderr)
                        break
            except Exception as e3:
                print(f"[get_paper] arXiv search fallback failed: {e3}", file=sys.stderr)

    if not paper:
        raise ValueError(f"Could not fetch paper detail for {paper_id} (S2 and arXiv both failed)")

    # References: try PDF download + parsing first
    refs = _get_references_from_pdf(paper)
    if not refs:
        print(f"[get_paper] PDF refs unavailable, falling back to S2", file=sys.stderr)
        try:
            resp = _request("GET", f"{S2_BASE}/paper/{paper_id}",
                            params={"fields": PAPER_FIELDS_WITH_REFS})
            data = resp.json()
            refs = [_parse_paper(r) for r in (data.get("references") or []) if r.get("paperId")]
        except Exception as e:
            print(f"[get_paper] S2 refs failed: {e}", file=sys.stderr)
            refs = []

    # Citations: Google Scholar → S2 fallback
    cites = _get_citations_from_gs(paper.title)
    if not cites:
        print(f"[get_paper] GS citations unavailable, falling back to S2", file=sys.stderr)
        try:
            resp = _request("GET", f"{S2_BASE}/paper/{paper_id}",
                            params={"fields": PAPER_FIELDS_WITH_REFS})
            data = resp.json()
            cites = [_parse_paper(c) for c in (data.get("citations") or []) if c.get("paperId")]
        except Exception as e:
            print(f"[get_paper] S2 citations failed: {e}", file=sys.stderr)
            cites = []

    return {"paper": paper, "references": refs, "citations": cites}


def get_references(paper_id: str, limit: int = 100) -> List[Paper]:
    """Get paper references: download PDF → parse → fallback S2."""
    # Try PDF-based extraction (need paper object for PDF URL)
    paper = None
    try:
        paper = _s2_get_paper_detail(paper_id)
    except Exception as e:
        print(f"[refs] S2 detail failed: {e}", file=sys.stderr)

    if not paper and paper_id.startswith("ARXIV:"):
        # Build minimal Paper for PDF download
        raw_id = paper_id.replace("ARXIV:", "").split("v")[0]
        paper = Paper(id=paper_id, title="", authors=[], year=None, citation_count=0,
                      arxiv_id=raw_id, pdf_url=f"https://arxiv.org/pdf/{raw_id}.pdf")
        print(f"[refs] Using arXiv PDF URL directly: {paper.pdf_url}", file=sys.stderr)

    if paper:
        try:
            refs = _get_references_from_pdf(paper)
            if refs:
                print(f"[refs] Got {len(refs)} references from PDF", file=sys.stderr)
                return refs[:limit]
        except Exception as e:
            print(f"[refs] PDF-based extraction failed: {e}", file=sys.stderr)

    # Fallback: S2 API
    if not paper_id.startswith("pdf:"):
        print(f"[refs] Falling back to S2 API", file=sys.stderr)
        try:
            return _s2_get_references(paper_id, limit)
        except Exception as e:
            print(f"[refs] S2 refs also failed: {e}", file=sys.stderr)
    return []


def get_citations(paper_id: str, limit: int = 100, title: str = None) -> List[Paper]:
    """Get citing papers: Google Scholar → fallback S2."""
    # Get paper title for GS search
    search_title = title
    if not search_title:
        try:
            paper = _s2_get_paper_detail(paper_id)
            search_title = paper.title
        except Exception as e:
            print(f"[cites] S2 detail failed: {e}", file=sys.stderr)

    if not search_title and paper_id.startswith("ARXIV:"):
        # Try arXiv to get title
        from services import arxiv as arxiv_svc
        raw_id = paper_id.replace("ARXIV:", "").split("v")[0]
        try:
            _, results = arxiv_svc.search(raw_id, limit=5)
            for r in results:
                if r.arxiv_id and raw_id in (r.arxiv_id or ""):
                    search_title = r.title
                    break
        except Exception:
            pass

    # Try Google Scholar
    if search_title:
        try:
            cites = _get_citations_from_gs(search_title, limit=limit)
            if cites:
                print(f"[cites] Got {len(cites)} citations from Google Scholar", file=sys.stderr)
                return cites
        except Exception as e:
            print(f"[cites] GS failed: {e}", file=sys.stderr)

    # Fallback: S2 API
    if not paper_id.startswith("pdf:"):
        print(f"[cites] Falling back to S2 API", file=sys.stderr)
        try:
            return _s2_get_citations(paper_id, limit)
        except Exception as e:
            print(f"[cites] S2 citations also failed: {e}", file=sys.stderr)
    return []


def recommend(paper_ids: List[str], limit: int = 20) -> List[Paper]:
    """Paper recommendations via S2 Recommendations API (no change)."""
    resp = _request("POST", f"{S2_RECOMMEND}/papers/",
                     json={"positivePaperIds": paper_ids},
                     params={"fields": PAPER_FIELDS_BASIC, "limit": limit})
    data = resp.json()
    return [_parse_paper(p) for p in (data.get("recommendedPapers") or [])]


def search_recent(query: str, year_from: int = 2024, limit: int = 20) -> List[Paper]:
    """Multi-source search for recent papers, with GS citation count enrichment."""
    from services import arxiv, dblp

    all_papers = []

    # 1. arXiv (naturally has the latest preprints)
    try:
        _, papers = arxiv.search(query, limit=limit)
        for p in papers:
            if p.year and p.year >= year_from:
                all_papers.append(p)
    except Exception as e:
        print(f"[recent] arXiv failed: {e}", file=sys.stderr)

    # 2. DBLP
    try:
        _, papers = dblp.search(query, limit=limit)
        for p in papers:
            if p.year and p.year >= year_from:
                all_papers.append(p)
    except Exception as e:
        print(f"[recent] DBLP failed: {e}", file=sys.stderr)

    # 3. S2 (has year filter + citation sort)
    try:
        papers = _s2_search_recent(query, year_from, limit)
        all_papers.extend(papers)
    except Exception as e:
        print(f"[recent] S2 failed: {e}", file=sys.stderr)

    # Deduplicate
    result = _dedup_papers(all_papers, limit * 2)

    # Enrich citation counts via Google Scholar (for papers with count=0)
    try:
        from services.google_scholar import enrich_citation_counts
        result = enrich_citation_counts(result)
    except Exception as e:
        print(f"[recent] GS citation enrichment failed: {e}", file=sys.stderr)

    return result[:limit]


# ── Internal multi-source helpers ────────────────────────


def _get_references_from_pdf(paper: Paper) -> List[Paper]:
    """Try to download paper PDF and extract references."""
    try:
        from services.paper_downloader import download_pdf
        from services.pdf_parser import parse_pdf

        pdf_path = download_pdf(paper)
        if not pdf_path:
            return []

        print(f"[refs] Parsing PDF: {pdf_path}", file=sys.stderr)
        result = parse_pdf(pdf_path)
        resolved = result.get("resolved_papers", [])
        if resolved:
            papers = [Paper(**p) for p in resolved]
            print(f"[refs] Extracted {len(papers)} references from PDF", file=sys.stderr)
            return papers
    except Exception as e:
        print(f"[refs] PDF extraction failed: {e}", file=sys.stderr)
    return []


def _get_citations_from_gs(title: str, limit: int = 50) -> List[Paper]:
    """Try to get citations from Google Scholar."""
    try:
        from services.google_scholar import get_citations as gs_get_citations
        cites = gs_get_citations(title, limit=limit)
        if cites:
            print(f"[cites] Got {len(cites)} citations from GS", file=sys.stderr)
            return cites
    except Exception as e:
        print(f"[cites] GS citation lookup failed: {e}", file=sys.stderr)
    return []
