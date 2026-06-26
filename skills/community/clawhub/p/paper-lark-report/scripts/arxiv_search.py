"""
arxiv_search.py - arXiv API client for paper fetching and query building.
"""
import json
import re
import ssl
import time
import urllib.error
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional

# ============================================================================
# CONSTANTS
# ============================================================================
SKILL_DIR = Path(__file__).parent.parent
ARXIV_ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_API = "https://export.arxiv.org/api/query"

# ============================================================================
# DATA CLASS
# ============================================================================
@dataclass
class Paper:
    title: str
    authors: List[str]
    venue: str
    year: int
    paper_id: str
    url: str
    abstract: str            # short abstract (from initial fetch)
    full_abstract: str = ""  # complete abstract (fetched separately)
    posted_date: Optional[str] = None
    relevance_score: int = 0

# ============================================================================
# QUERY BUILDER
# ============================================================================
_GENERIC_TERMS = {
    "towards", "toward", "systems", "system", "approach",
    "method", "methods", "model", "models", "paper", "work",
    "research", "study", "based", "using", "used", "new",
    "safe", "safety", "efficient", "efficiency", "effective",
    "real", "world", "constraint", "constraints", "problem",
    "提出", "研究", "实现", "方法", "系统",
}

_COMPOUND_TERMS = [
    "multi-agent", "multi agent", "single-agent", "single agent",
    "multiagent", "llm-based", "llm based",
    "harness-based", "runtime assurance", "trace-based",
    "role-aware", "context routing", "least-privilege",
    "tool access", "orchestration", "collaboration",
]


def build_arxiv_query(research_direction: str) -> str:
    """
    Convert free-text research_direction into a precise arXiv abs: query.
    Extracts compound terms as atomic units, filters generic/academic
    stopwords, deduplicates, caps at 8 terms.
    """
    text = research_direction.lower()
    text_spaced = re.sub(r"-", " ", text)

    # Capture compound terms that appear in the text
    compound_terms: List[str] = []
    for comp in _COMPOUND_TERMS:
        pattern = r"\b" + re.escape(comp) + r"\b"
        if re.search(pattern, text_spaced):
            compound_terms.append(comp.replace(" ", "-"))

    # Capture remaining significant single tokens
    captured_substrings = set()
    for comp in compound_terms:
        captured_substrings.update(comp.split("-"))

    tokens = re.findall(r"[a-z]+", text_spaced)
    seen = set()
    for tok in tokens:
        if tok in _GENERIC_TERMS or tok in captured_substrings or len(tok) < 5:
            continue
        if tok not in seen:
            seen.add(tok)
            compound_terms.append(tok)
            if len(compound_terms) >= 8:
                break

    # AND the single most core term + OR the remaining terms for recall
    # The LLM scorer does fine-grained filtering; this just ensures baseline relevance.
    if len(compound_terms) == 0:
        return "abs:agent"
    if len(compound_terms) == 1:
        return f"abs:{compound_terms[0]}"
    if len(compound_terms) == 2:
        return f"abs:{compound_terms[0]}"
    core = compound_terms[0]
    rest = " OR ".join(f"abs:{t}" for t in compound_terms[1:])
    return f"abs:{core} AND ({rest})"


# ============================================================================
# FETCH HELPERS
# ============================================================================
def _get_text(entry, tag: str) -> str:
    el = entry.find(f"{ARXIV_ATOM_NS}{tag}")
    return el.text.strip() if el is not None and el.text else ""


def _build_paper(entry) -> Optional[Paper]:
    paper_id = _get_text(entry, "id").split("/")[-1]
    if not paper_id:
        return None

    title = _get_text(entry, "title").replace("\n", " ")
    summary = _get_text(entry, "summary").replace("\n", " ")
    published = _get_text(entry, "published")[:10]

    authors = [
        a.find(f"{ARXIV_ATOM_NS}name").text
        for a in entry.findall(f"{ARXIV_ATOM_NS}author")
        if a.find(f"{ARXIV_ATOM_NS}name") is not None
    ]

    category = ""
    for cat in entry.findall(f"{ARXIV_ATOM_NS}category"):
        if cat.get("term"):
            category = cat.get("term")
            break

    return Paper(
        title=title,
        authors=authors,
        venue=f"arXiv {category}" if category else "arXiv",
        year=int(published[:4]) if published else datetime.now().year,
        paper_id=paper_id,
        url=f"https://arxiv.org/abs/{paper_id}",
        abstract=summary[:500],
        full_abstract=summary,
        posted_date=published,
        relevance_score=0,
    )


# ============================================================================
# PUBLIC API
# ============================================================================
def fetch_arxiv_papers(query: str, max_results: int = 50) -> List[Paper]:
    """
    Search arXiv by query string and return a list of Paper objects.
    Uses abs: field queries for abstract-level matching.
    Retries on 429/503 with exponential backoff.
    """
    url = (
        f"{ARXIV_API}?"
        f"search_query={urllib.parse.quote(query)}"
        f"&start=0&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )

    papers = []
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                raw = resp.read().decode("utf-8")

            root = ET.fromstring(raw)
            for entry in root:
                if entry.tag != f"{ARXIV_ATOM_NS}entry":
                    continue
                paper = _build_paper(entry)
                if paper:
                    papers.append(paper)

            print(f"  Fetched {len(papers)} papers for query: {query}")
            break  # success

        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 4:
                wait = (attempt + 1) * 30
                print(f"  HTTP {e.code}, retrying in {wait}s (attempt {attempt+1}/5)...")
                time.sleep(wait)
            else:
                print(f"  arXiv fetch failed: HTTP {e.code}")
                break
        except Exception as e:
            print(f"  arXiv fetch failed: {e}")
            break

    return papers


def fetch_arxiv_details(papers: List[Paper]) -> List[Paper]:
    """
    Batch-fetch full abstracts for a list of Paper objects.
    Updates full_abstract, authors, and posted_date in-place.
    Max 5 IDs per request; 3-second delay between batches.
    Retries on 429/503 with exponential backoff.
    """
    if not papers:
        return papers

    paper_map = {p.paper_id: p for p in papers}
    batch_size = 5

    print(f"Fetching full abstracts for {len(papers)} papers...")

    for i in range(0, len(papers), batch_size):
        batch = papers[i : i + batch_size]
        ids = "+".join(p.paper_id for p in batch)
        batch_num = i // batch_size + 1

        for attempt in range(5):
            try:
                url = f"{ARXIV_API}?id_list={ids}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                ctx = ssl.create_default_context()
                with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                    raw = resp.read().decode("utf-8")

                root = ET.fromstring(raw)
                for entry in root:
                    if entry.tag != f"{ARXIV_ATOM_NS}entry":
                        continue

                    pid_elem = entry.find(f"{ARXIV_ATOM_NS}id")
                    if pid_elem is None or not pid_elem.text:
                        continue

                    pid = pid_elem.text.split("/")[-1]
                    if pid not in paper_map:
                        continue

                    p = paper_map[pid]

                    summary_el = entry.find(f"{ARXIV_ATOM_NS}summary")
                    if summary_el is not None and summary_el.text:
                        p.full_abstract = summary_el.text.strip()

                    authors = [
                        a.find(f"{ARXIV_ATOM_NS}name").text
                        for a in entry.findall(f"{ARXIV_ATOM_NS}author")
                        if a.find(f"{ARXIV_ATOM_NS}name") is not None
                    ]
                    if authors:
                        p.authors = authors

                    pub_el = entry.find(f"{ARXIV_ATOM_NS}published")
                    if pub_el is not None and pub_el.text:
                        p.posted_date = pub_el.text[:10]

                print(f"  Batch {batch_num}: {len(batch)} papers done")
                break  # success

            except urllib.error.HTTPError as e:
                if e.code in (429, 503) and attempt < 4:
                    wait = (attempt + 1) * 15
                    print(f"  Batch {batch_num} HTTP {e.code}, retrying in {wait}s (attempt {attempt+1}/5)...")
                    time.sleep(wait)
                else:
                    print(f"  Batch {batch_num} failed: HTTP {e.code}")
                    break
            except Exception as e:
                print(f"  Batch {batch_num} failed: {e}")
                break

        time.sleep(5)  # arXiv requires >= 3 s between requests

    return list(paper_map.values())
