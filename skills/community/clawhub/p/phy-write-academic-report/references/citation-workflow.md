# Citation Verification Workflow

Reference guide for verifying, retrieving, and managing academic citations.
Adapted from ml-paper-writing's citation workflow, extended for thesis writing.

---

## 1. Why Citation Verification Matters

Large language models hallucinate citations at an alarming rate:

- **~40% error rate** in LLM-generated references — wrong author, wrong year, wrong venue, or entirely fabricated
- A single fake citation in a thesis can trigger an academic integrity investigation
- Reviewers and examiners routinely spot-check references; a fabricated entry destroys credibility
- Retracted or misattributed citations can invalidate the claims they support

**Rule: Every citation must be verified against at least two independent sources before inclusion.**

---

## 2. Citation APIs Overview

| API | Coverage | Rate Limit (free) | Best For | Base URL |
|-----|----------|--------------------|----------|----------|
| **Semantic Scholar** | 200M+ papers, CS-heavy | 100 req/5min (no key), 1 req/sec (key) | CS/AI papers, citation graphs | `api.semanticscholar.org/graph/v1` |
| **CrossRef** | 150M+ DOIs, all fields | 50 req/sec (polite pool with email) | DOI resolution, metadata verification | `api.crossref.org/works` |
| **arXiv** | 2.4M+ preprints | 1 req/3sec | Preprints, ML/AI/physics | `export.arxiv.org/api/query` |
| **OpenAlex** | 250M+ works, open access | 100K req/day, 10 req/sec | Broad coverage, institution data | `api.openalex.org/works` |

**Recommended strategy**: Search Semantic Scholar first (best CS coverage), verify via CrossRef (authoritative DOI metadata), fall back to arXiv for preprints.

---

## 3. Verified Citation Workflow

### Step 1: Search

Query Semantic Scholar (or CrossRef) with title, author, and year. Accept only results with high title similarity (>0.85 fuzzy match).

### Step 2: Verify with 2+ Sources

Cross-check the returned metadata against a second API. Confirm:
- Title matches exactly (modulo capitalization)
- Author list matches (at least first author + last author)
- Year matches
- Venue / journal matches

If any field conflicts between sources, flag for manual review.

### Step 3: Retrieve BibTeX via DOI

Once verified, use the DOI to fetch canonical BibTeX from CrossRef or doi.org:
```
GET https://doi.org/{DOI}
Accept: application/x-bibtex
```

This returns publisher-authoritative BibTeX — always prefer this over hand-crafted entries.

### Step 4: Validate Claims

Re-read the specific claim in your text that cites this paper. Confirm the cited paper actually supports that claim. Common errors:
- Citing a survey when you mean the original work
- Citing the wrong year of a multi-version paper (e.g., arXiv v1 vs published)
- Attributing a claim to Paper A when Paper A merely cites Paper B for it

### Step 5: Add to .bib

Insert the verified BibTeX entry into your `.bib` file using a consistent key format (see Section 7). Compile LaTeX to confirm the citation resolves.

---

## 4. Python Implementation

```python
"""
citation_manager.py — Verify and retrieve academic citations.

Usage:
    manager = CitationManager(email="you@university.edu")
    result = manager.cite("Attention Is All You Need", authors=["Vaswani"], year=2017)
    print(result["bibtex"])
"""

import re
import time
import json
import urllib.request
import urllib.parse
import urllib.error
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Optional


@dataclass
class CitationResult:
    """Verified citation metadata."""
    title: str
    authors: list[str]
    year: int
    venue: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    bibtex: Optional[str] = None
    key: str = ""
    verified: bool = False
    sources: list[str] = field(default_factory=list)


class CitationManager:
    """Search, verify, and retrieve academic citations from multiple APIs."""

    SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1"
    CROSSREF_BASE = "https://api.crossref.org/works"
    ARXIV_BASE = "http://export.arxiv.org/api/query"

    def __init__(self, email: Optional[str] = None, s2_api_key: Optional[str] = None):
        """
        Args:
            email: Contact email for CrossRef polite pool (recommended).
            s2_api_key: Semantic Scholar API key for higher rate limits.
        """
        self.email = email
        self.s2_api_key = s2_api_key
        self._last_request_time: dict[str, float] = {}

    # ------------------------------------------------------------------
    # Rate limiting
    # ------------------------------------------------------------------

    def _rate_limit(self, api: str, min_interval: float) -> None:
        """Enforce minimum interval between requests to the same API."""
        now = time.time()
        last = self._last_request_time.get(api, 0.0)
        wait = min_interval - (now - last)
        if wait > 0:
            time.sleep(wait)
        self._last_request_time[api] = time.time()

    def _get_json(self, url: str, headers: Optional[dict] = None) -> Optional[dict]:
        """Fetch JSON from a URL with error handling."""
        req = urllib.request.Request(url)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
            return None

    def _get_text(self, url: str, headers: Optional[dict] = None) -> Optional[str]:
        """Fetch plain text from a URL with error handling."""
        req = urllib.request.Request(url)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError):
            return None

    @staticmethod
    def _title_similarity(a: str, b: str) -> float:
        """Normalized title similarity (0-1)."""
        a_clean = re.sub(r"[^a-z0-9 ]", "", a.lower().strip())
        b_clean = re.sub(r"[^a-z0-9 ]", "", b.lower().strip())
        return SequenceMatcher(None, a_clean, b_clean).ratio()

    @staticmethod
    def _make_key(authors: list[str], year: int, title: str) -> str:
        """Generate citation key: firstauthor_year_firstword."""
        first_author = authors[0].split()[-1].lower() if authors else "unknown"
        first_author = re.sub(r"[^a-z]", "", first_author)
        first_word = re.sub(r"[^a-z]", "", title.split()[0].lower()) if title else "untitled"
        return f"{first_author}_{year}_{first_word}"

    # ------------------------------------------------------------------
    # Search APIs
    # ------------------------------------------------------------------

    def search_semantic_scholar(
        self, title: str, limit: int = 5
    ) -> list[dict]:
        """Search Semantic Scholar by title."""
        self._rate_limit("s2", 1.1)
        encoded = urllib.parse.quote(title)
        url = (
            f"{self.SEMANTIC_SCHOLAR_BASE}/paper/search"
            f"?query={encoded}&limit={limit}"
            f"&fields=title,authors,year,venue,externalIds"
        )
        headers = {}
        if self.s2_api_key:
            headers["x-api-key"] = self.s2_api_key
        data = self._get_json(url, headers=headers)
        if data and "data" in data:
            return data["data"]
        return []

    def search_crossref(
        self, title: str, limit: int = 5
    ) -> list[dict]:
        """Search CrossRef by title."""
        self._rate_limit("crossref", 0.1)
        encoded = urllib.parse.quote(title)
        url = f"{self.CROSSREF_BASE}?query.bibliographic={encoded}&rows={limit}"
        if self.email:
            url += f"&mailto={self.email}"
        data = self._get_json(url)
        if data and "message" in data and "items" in data["message"]:
            return data["message"]["items"]
        return []

    # ------------------------------------------------------------------
    # Verify
    # ------------------------------------------------------------------

    def verify(
        self,
        title: str,
        authors: Optional[list[str]] = None,
        year: Optional[int] = None,
        threshold: float = 0.85,
    ) -> Optional[CitationResult]:
        """
        Verify a citation against Semantic Scholar + CrossRef.

        Returns CitationResult if verified (title similarity >= threshold
        in at least 2 sources), else None.
        """
        result = CitationResult(title=title, authors=authors or [], year=year or 0, venue="")
        sources_matched = 0

        # --- Semantic Scholar ---
        s2_results = self.search_semantic_scholar(title)
        s2_match = None
        for item in s2_results:
            sim = self._title_similarity(title, item.get("title", ""))
            if sim >= threshold:
                s2_match = item
                break

        if s2_match:
            sources_matched += 1
            result.sources.append("semantic_scholar")
            result.title = s2_match.get("title", title)
            result.year = s2_match.get("year", result.year) or result.year
            result.venue = s2_match.get("venue", "")
            result.authors = [
                a.get("name", "") for a in s2_match.get("authors", [])
            ] or result.authors
            ext_ids = s2_match.get("externalIds", {}) or {}
            result.doi = ext_ids.get("DOI")
            result.arxiv_id = ext_ids.get("ArXiv")

        # --- CrossRef ---
        cr_results = self.search_crossref(title)
        cr_match = None
        for item in cr_results:
            cr_titles = item.get("title", [])
            cr_title_str = cr_titles[0] if cr_titles else ""
            sim = self._title_similarity(title, cr_title_str)
            if sim >= threshold:
                cr_match = item
                break

        if cr_match:
            sources_matched += 1
            result.sources.append("crossref")
            if not result.doi:
                result.doi = cr_match.get("DOI")
            if not result.venue:
                result.venue = (cr_match.get("container-title") or [""])[0]
            cr_year = None
            date_parts = (cr_match.get("published") or {}).get("date-parts", [[]])
            if date_parts and date_parts[0]:
                cr_year = date_parts[0][0]
            if cr_year and not result.year:
                result.year = cr_year

        # --- Verification decision ---
        if sources_matched >= 2:
            result.verified = True
        elif sources_matched == 1:
            # Accept single source only if DOI exists
            result.verified = result.doi is not None

        if result.verified:
            result.key = self._make_key(result.authors, result.year, result.title)
        return result if result.verified else None

    # ------------------------------------------------------------------
    # BibTeX retrieval
    # ------------------------------------------------------------------

    def get_bibtex(self, doi: Optional[str] = None, arxiv_id: Optional[str] = None) -> Optional[str]:
        """
        Retrieve canonical BibTeX via DOI (preferred) or arXiv ID.

        DOI resolution returns publisher-authoritative BibTeX.
        """
        if doi:
            self._rate_limit("doi", 0.5)
            url = f"https://doi.org/{doi}"
            bib = self._get_text(url, headers={"Accept": "application/x-bibtex"})
            if bib and "@" in bib:
                return bib.strip()

        if arxiv_id:
            self._rate_limit("arxiv", 3.0)
            clean_id = arxiv_id.replace("arXiv:", "")
            # Use Semantic Scholar to get a DOI for the arXiv paper
            url = f"{self.SEMANTIC_SCHOLAR_BASE}/paper/ArXiv:{clean_id}?fields=externalIds"
            headers = {}
            if self.s2_api_key:
                headers["x-api-key"] = self.s2_api_key
            data = self._get_json(url, headers=headers)
            if data:
                found_doi = (data.get("externalIds") or {}).get("DOI")
                if found_doi:
                    return self.get_bibtex(doi=found_doi)
            # Fallback: construct minimal arXiv BibTeX
            return (
                f"@misc{{{clean_id},\n"
                f"  title = {{See arXiv:{clean_id}}},\n"
                f"  note = {{arXiv:{clean_id}}},\n"
                f"  year = {{}}\n"
                f"}}"
            )
        return None

    # ------------------------------------------------------------------
    # High-level cite()
    # ------------------------------------------------------------------

    def cite(
        self,
        title: str,
        authors: Optional[list[str]] = None,
        year: Optional[int] = None,
    ) -> Optional[CitationResult]:
        """
        Full pipeline: search, verify, retrieve BibTeX, return result.

        Returns CitationResult with .bibtex populated, or None if
        verification fails.
        """
        result = self.verify(title, authors=authors, year=year)
        if result is None:
            return None

        bib = self.get_bibtex(doi=result.doi, arxiv_id=result.arxiv_id)
        if bib:
            # Replace the auto-generated key with our consistent format
            result.bibtex = re.sub(
                r"@(\w+)\{[^,]*,",
                rf"@\1{{{result.key},",
                bib,
                count=1,
            )
        return result


# ======================================================================
# 5. Quick Functions
# ======================================================================

def quick_cite(
    title: str,
    authors: Optional[list[str]] = None,
    year: Optional[int] = None,
    email: Optional[str] = None,
) -> Optional[str]:
    """
    One-liner citation: returns BibTeX string or None.

    Usage:
        bib = quick_cite("Attention Is All You Need", ["Vaswani"], 2017)
        if bib:
            print(bib)
    """
    manager = CitationManager(email=email)
    result = manager.cite(title, authors=authors, year=year)
    return result.bibtex if result else None


def batch_cite(
    citations: list[dict],
    email: Optional[str] = None,
    delay: float = 1.5,
) -> list[CitationResult]:
    """
    Verify and retrieve BibTeX for multiple citations.

    Args:
        citations: List of dicts with keys: title, authors (optional), year (optional).
        email: Contact email for CrossRef polite pool.
        delay: Seconds between citation lookups (respect rate limits).

    Returns:
        List of CitationResult objects (only verified ones).

    Usage:
        refs = [
            {"title": "Attention Is All You Need", "authors": ["Vaswani"], "year": 2017},
            {"title": "BERT: Pre-training of Deep Bidirectional Transformers"},
        ]
        results = batch_cite(refs, email="me@uni.edu")
        for r in results:
            print(r.key, r.verified)
    """
    manager = CitationManager(email=email)
    verified: list[CitationResult] = []
    for i, ref in enumerate(citations):
        result = manager.cite(
            title=ref["title"],
            authors=ref.get("authors"),
            year=ref.get("year"),
        )
        if result:
            verified.append(result)
        if i < len(citations) - 1:
            time.sleep(delay)
    return verified
```

---

## 6. BibTeX Management

### BibTeX vs BibLaTeX

| Feature | BibTeX | BibLaTeX |
|---------|--------|----------|
| Backend | `bibtex` | `biber` |
| Entry types | Limited (13) | Extended (20+) |
| Unicode | Poor | Full support |
| URL/DOI fields | Unofficial | Native |
| Customization | Difficult | Flexible |
| **Recommendation** | Legacy projects | New projects, theses |

### LaTeX Setup (BibLaTeX)

```latex
% In preamble
\usepackage[
    backend=biber,
    style=numeric,           % or: authoryear, ieee, apa
    sorting=nyt,             % name-year-title
    maxbibnames=99,          % show all authors in bibliography
    maxcitenames=2,          % truncate in-text citations
    doi=true,
    url=true,
    isbn=false,
]{biblatex}
\addbibresource{references.bib}

% In document body
\printbibliography[title={References}]
```

### LaTeX Setup (Traditional BibTeX)

```latex
% In preamble — nothing special needed

% At the end of document body
\bibliographystyle{plainnat}   % or: ieeetr, acm, apalike
\bibliography{references}      % references.bib (no extension)
```

### Citation Commands

| Command | Output (numeric) | Output (authoryear) | Package |
|---------|-------------------|---------------------|---------|
| `\cite{key}` | [1] | Author (Year) | Both |
| `\citep{key}` | [1] | (Author, Year) | natbib / biblatex |
| `\citet{key}` | Author [1] | Author (Year) | natbib / biblatex |
| `\parencite{key}` | [1] | (Author, Year) | biblatex only |
| `\textcite{key}` | Author [1] | Author (Year) | biblatex only |
| `\cite[p.~5]{key}` | [1, p. 5] | Author (Year, p. 5) | Both |
| `\cite{k1,k2}` | [1, 2] | Author1; Author2 | Both |

### Build Commands

```bash
# BibLaTeX (biber)
pdflatex main && biber main && pdflatex main && pdflatex main

# Traditional BibTeX
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

---

## 7. Consistent Citation Keys

**Format: `firstauthor_year_firstword`**

Rules:
- First author's **last name**, lowercased, ASCII only
- Publication **year**
- **First significant word** of title, lowercased

Examples:

| Paper | Key |
|-------|-----|
| Vaswani et al. (2017) "Attention Is All You Need" | `vaswani_2017_attention` |
| Devlin et al. (2019) "BERT: Pre-training of..." | `devlin_2019_bert` |
| He et al. (2016) "Deep Residual Learning..." | `he_2016_deep` |
| Brown et al. (2020) "Language Models are Few-Shot..." | `brown_2020_language` |

When collisions occur, append a distinguishing letter: `smith_2023_learning`, `smith_2023_learningb`.

---

## 8. Common Citation Formats

### Conference Paper

```bibtex
@inproceedings{vaswani_2017_attention,
  title     = {Attention Is All You Need},
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and
               Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N. and
               Kaiser, {\L}ukasz and Polosukhin, Illia},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  volume    = {30},
  year      = {2017},
  doi       = {10.5555/3295222.3295349},
}
```

### Journal Article

```bibtex
@article{lecun_2015_deep,
  title   = {Deep Learning},
  author  = {LeCun, Yann and Bengio, Yoshua and Hinton, Geoffrey},
  journal = {Nature},
  volume  = {521},
  number  = {7553},
  pages   = {436--444},
  year    = {2015},
  doi     = {10.1038/nature14539},
}
```

### arXiv Preprint

```bibtex
@misc{touvron_2023_llama,
  title         = {LLaMA: Open and Efficient Foundation Language Models},
  author        = {Touvron, Hugo and Lavril, Thibaut and Izacard, Gautier and
                   Martinet, Xavier and Lachaux, Marie-Anne and others},
  year          = {2023},
  eprint        = {2302.13971},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CL},
}
```

### PhD Thesis

```bibtex
@phdthesis{mikolov_2012_statistical,
  title  = {Statistical Language Models Based on Neural Networks},
  author = {Mikolov, Tom{\'a}{\v{s}}},
  school = {Brno University of Technology},
  year   = {2012},
  type   = {{PhD} Dissertation},
}
```

### Master's Thesis

```bibtex
@mastersthesis{doe_2024_exploring,
  title  = {Exploring Graph-Based Navigation for Web Agents},
  author = {Doe, Jane},
  school = {Stanford University},
  year   = {2024},
  type   = {{MSc} Thesis},
  note   = {Department of Computer Science},
}
```

---

## 9. Thesis-Specific Citation Notes

### Reference Count

Theses typically require significantly more references than conference papers:

| Document Type | Typical References |
|---------------|-------------------|
| Workshop paper | 10-20 |
| Conference paper | 25-40 |
| Journal paper | 30-60 |
| **Master's thesis** | **40-80** |
| **PhD thesis** | **80-200+** |

A thin bibliography signals insufficient literature review. Aim for the upper end of the range.

### University Style Mandates

Many universities mandate a specific citation style. **Check your department's thesis guidelines before writing a single citation.** Common mandated styles:

| Style | Typical Fields | Notes |
|-------|----------------|-------|
| IEEE | Engineering, CS | Numeric, compact |
| APA 7th | Social sciences, HCI | Author-year, strict formatting |
| Harvard | Business, humanities | Author-year, varies by institution |
| Chicago | History, arts | Footnotes or author-date |
| Vancouver | Medicine, biology | Numeric, sequential |

If your university provides a `.bst` file or BibLaTeX style, use it exactly as provided. Do not modify it.

### Self-Citation Rules

- Check with your supervisor about citing your own published work
- Some institutions require a declaration if you reuse content from your own papers
- When self-citing, use the same `author_year_firstword` key format
- Never inflate your bibliography with unnecessary self-citations

### Non-Paper Sources

Theses benefit from citing a broader range of sources than conference papers:

| Source Type | BibTeX Entry | When to Cite |
|-------------|--------------|--------------|
| Technical reports | `@techreport` | Implementation details, benchmarks |
| Standards (ISO, W3C) | `@misc` or `@standard` | Protocol/format specifications |
| Software documentation | `@manual` | Framework/library APIs |
| Software releases | `@software` (BibLaTeX) or `@misc` | Specific tool versions |
| Datasets | `@misc` with `howpublished` | Evaluation data sources |
| Blog posts / whitepapers | `@misc` with `url` + `note` | Industry context (use sparingly) |

---

## 10. Troubleshooting

### Citation Not Found

| Symptom | Cause | Fix |
|---------|-------|-----|
| Zero results from all APIs | Title is wrong or paper does not exist | Verify the paper exists via Google Scholar manually |
| Semantic Scholar returns results but CrossRef does not | Paper is a preprint without DOI | Accept single-source verification if arXiv ID exists |
| Title matches but year differs | Preprint year vs published year | Use the **published** year, not the arXiv submission year |
| Multiple versions of same paper | arXiv v1, v2, ... vs conference version | Cite the **published** (peer-reviewed) version when available |

### BibTeX Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Citation undefined` in LaTeX | Key mismatch or missing `biber`/`bibtex` run | Check key spelling; run full build chain |
| Special characters broken (`{\"u}`, `{\ss}`) | Encoding issue | Use BibLaTeX + biber (full Unicode support) |
| Author names formatted wrong | Inconsistent `First Last` vs `Last, First` | Always use `Last, First` format in `.bib` |
| DOI link broken in PDF | Missing `hyperref` or `doi` package | Add `\usepackage{hyperref}` before biblatex |
| `I found no \bibstyle command` | Missing `\bibliographystyle{}` | Add it before `\bibliography{}` for BibTeX |
| Duplicate bibliography entries | Same paper with different keys | Search `.bib` for duplicates; standardize keys |

### Rate Limit Errors

| API | Error | Fix |
|-----|-------|-----|
| Semantic Scholar | HTTP 429 | Wait 5 minutes; use API key for higher limits |
| CrossRef | HTTP 429 | Add `mailto` parameter for polite pool (50 req/sec) |
| doi.org | Slow / timeout | Retry after 2 seconds; these are free resolvers |

### Verification Failures

If `verify()` returns `None` but you are confident the paper exists:

1. Try searching with a shorter version of the title (first 6-8 words)
2. Search by DOI directly if you have one: `https://api.crossref.org/works/{DOI}`
3. Search by arXiv ID: `https://api.semanticscholar.org/graph/v1/paper/ArXiv:{ID}`
4. As a last resort, manually construct the BibTeX entry from the paper's own metadata page and add a `% MANUAL` comment for future auditing

```python
# Example: manual fallback search by DOI
manager = CitationManager(email="you@university.edu")
bib = manager.get_bibtex(doi="10.1038/nature14539")
print(bib)
```
