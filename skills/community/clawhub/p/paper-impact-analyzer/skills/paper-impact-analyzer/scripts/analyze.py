#!/usr/bin/env python3
"""
Paper Impact Analyzer
Multi-source, fault-tolerant academic paper impact analysis.
Input: arXiv ID(s) → Output: Markdown impact report

Data sources (priority order):
  1. arXiv API (metadata, always available)
  2. GitHub API (stars/forks, most reliable)
  3. OpenAlex API (citations, free no key)
  4. Semantic Scholar API (citations + h-index, rate-limited)

Usage:
  python analyze.py 2603.04948
  python analyze.py 2603.04948 2602.15922 2603.05488
"""

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# SSL context for environments with certificate issues
# ---------------------------------------------------------------------------
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SourceStatus:
    name: str
    success: bool
    error: str = ""


@dataclass
class PaperImpact:
    arxiv_id: str
    title: str = ""
    authors: List[str] = field(default_factory=list)
    affiliations: List[str] = field(default_factory=list)
    published_date: str = ""
    abstract: str = ""
    venue: str = ""
    # GitHub
    github_url: str = ""
    github_stars: int = -1
    github_forks: int = -1
    github_issues: int = -1
    github_created: str = ""
    # Citations
    openalex_citations: int = -1
    s2_citations: int = -1
    s2_influential: int = -1
    # Author
    first_author_hindex: int = -1
    first_author_name: str = ""
    # Metadata
    sources: List[SourceStatus] = field(default_factory=list)
    age_days: int = 0
    rating: str = ""
    confidence: str = ""


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def http_get(url: str, timeout: int = 10, headers: Optional[Dict] = None) -> str:
    """Make GET request with timeout and SSL bypass. Returns response body."""
    hdrs = {"User-Agent": "PaperImpactAnalyzer/1.0"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    resp = urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX)
    return resp.read().decode("utf-8")


def http_get_json(url: str, timeout: int = 10, headers: Optional[Dict] = None) -> dict:
    """Make GET request and parse JSON."""
    return json.loads(http_get(url, timeout, headers))


# ---------------------------------------------------------------------------
# Layer 1: arXiv API
# ---------------------------------------------------------------------------

VENUE_PATTERNS = [
    r"(?:accepted|published|appeared|presented)\s+(?:at|in|as|by)\s+([A-Z][A-Za-z0-9\s\-&]+\d{4})",
    r"((?:ICLR|NeurIPS|ICML|AAAI|IJCAI|ACL|EMNLP|NAACL|CVPR|ICCV|ECCV|SIGIR|KDD|WWW|ICRA|IROS|CoRL)\s*\d{4})",
    r"(?:conference|journal)\s+paper\s+at\s+([A-Z][A-Za-z0-9\s]+\d{4})",
]


def fetch_arxiv(arxiv_id: str) -> Tuple[PaperImpact, SourceStatus]:
    """Fetch paper metadata from arXiv API."""
    paper = PaperImpact(arxiv_id=arxiv_id)
    status = SourceStatus(name="arXiv", success=False)
    try:
        url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        xml_text = http_get(url, timeout=15)
        root = ET.fromstring(xml_text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        entry = root.find("atom:entry", ns)
        if entry is None:
            status.error = "No entry found"
            return paper, status

        # Title
        title_el = entry.find("atom:title", ns)
        paper.title = " ".join(title_el.text.split()) if title_el is not None and title_el.text else ""

        # Authors
        for author_el in entry.findall("atom:author", ns):
            name_el = author_el.find("atom:name", ns)
            if name_el is not None and name_el.text:
                paper.authors.append(name_el.text.strip())
            aff_el = author_el.find("atom:affiliation", ns)  # arxiv doesn't always have this
            if aff_el is not None and aff_el.text:
                aff = aff_el.text.strip()
                if aff not in paper.affiliations:
                    paper.affiliations.append(aff)

        # Published date
        pub_el = entry.find("atom:published", ns)
        if pub_el is not None and pub_el.text:
            paper.published_date = pub_el.text[:10]
            try:
                pub_dt = datetime.strptime(paper.published_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                paper.age_days = (datetime.now(timezone.utc) - pub_dt).days
            except ValueError:
                pass

        # Abstract
        summary_el = entry.find("atom:summary", ns)
        paper.abstract = " ".join(summary_el.text.split()) if summary_el is not None and summary_el.text else ""

        # Comment field (often contains venue info like "Accepted at ICLR 2026")
        comment_el = entry.find("{http://arxiv.org/schemas/atom}comment")
        comment_text = ""
        if comment_el is not None and comment_el.text:
            comment_text = comment_el.text.strip()

        # Detect venue from comment, title, abstract (comment first - most reliable)
        text_to_search = f"{comment_text} {paper.title} {paper.abstract}"
        for pattern in VENUE_PATTERNS:
            m = re.search(pattern, text_to_search, re.IGNORECASE)
            if m:
                paper.venue = m.group(1).strip()
                break

        # Also check for "Published as a conference paper at" pattern (common in ICLR/NeurIPS)
        if not paper.venue:
            pub_match = re.search(
                r"[Pp]ublished\s+as\s+a\s+conference\s+paper\s+at\s+([A-Z][A-Za-z0-9\s]+\d{4})",
                text_to_search
            )
            if pub_match:
                paper.venue = pub_match.group(1).strip()

        # Extract GitHub URLs from abstract and comment
        for text_src in [paper.abstract, comment_text]:
            gh_match = re.search(r"github\.com/([\w\-]+/[\w\-\.]+)", text_src, re.IGNORECASE)
            if gh_match:
                paper.github_url = f"https://github.com/{gh_match.group(1)}"
                break

        status.success = True
    except Exception as e:
        status.error = str(e)[:100]
    return paper, status


# ---------------------------------------------------------------------------
# Layer 2: GitHub API
# ---------------------------------------------------------------------------

def fetch_github(paper: PaperImpact) -> SourceStatus:
    """Fetch GitHub repo metrics. Tries extracted URL first, then search."""
    status = SourceStatus(name="GitHub", success=False)

    repo_path = ""

    # Strategy 1: Use URL extracted from abstract
    if paper.github_url:
        m = re.search(r"github\.com/([\w\-]+/[\w\-\.]+)", paper.github_url)
        if m:
            repo_path = m.group(1).rstrip(".")

    # Strategy 2: Search GitHub by title keywords
    if not repo_path and paper.title:
        try:
            # Use meaningful words from title (skip common words)
            stop_words = {"the", "for", "and", "with", "from", "via", "are", "its",
                          "how", "can", "not", "but", "has", "was", "all", "any",
                          "new", "our", "more", "than", "into", "that", "this",
                          "based", "using", "towards", "beyond", "simple"}
            words = [w for w in paper.title.split()
                     if len(w) > 2 and w.isalpha() and w.lower() not in stop_words][:5]
            query = "+".join(words)
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&per_page=5"
            data = http_get_json(url, timeout=10)
            items = data.get("items", [])
            for top in items:
                top_name = (top.get("name", "") + " " + (top.get("description") or "")).lower()
                # Strict relevance: at least 3 title words or 60% must match
                matches = sum(1 for w in words if w.lower() in top_name)
                threshold = max(3, int(len(words) * 0.6))
                if matches >= threshold:
                    repo_path = top["full_name"]
                    paper.github_url = top["html_url"]
                    break
        except Exception:
            pass

    if not repo_path:
        status.error = "No GitHub repo found"
        return status

    # Fetch repo details
    try:
        url = f"https://api.github.com/repos/{repo_path}"
        data = http_get_json(url, timeout=10)
        paper.github_stars = data.get("stargazers_count", -1)
        paper.github_forks = data.get("forks_count", -1)
        paper.github_issues = data.get("open_issues_count", -1)
        created = data.get("created_at", "")
        paper.github_created = created[:10] if created else ""
        if not paper.github_url:
            paper.github_url = data.get("html_url", "")
        status.success = True
    except urllib.error.HTTPError as e:
        status.error = f"HTTP {e.code}"
    except Exception as e:
        status.error = str(e)[:100]
    return status


# ---------------------------------------------------------------------------
# Layer 3: OpenAlex API
# ---------------------------------------------------------------------------

def fetch_openalex(paper: PaperImpact) -> SourceStatus:
    """Fetch citation count from OpenAlex."""
    status = SourceStatus(name="OpenAlex", success=False)
    try:
        doi = f"10.48550/arXiv.{paper.arxiv_id}"
        url = f"https://api.openalex.org/works/doi:{doi}?select=id,cited_by_count,publication_date"
        data = http_get_json(url, timeout=10, headers={"User-Agent": "mailto:paper-impact@example.com"})
        paper.openalex_citations = data.get("cited_by_count", -1)
        status.success = True
    except urllib.error.HTTPError as e:
        status.error = f"HTTP {e.code}"
    except Exception as e:
        status.error = str(e)[:100]
    return status


# ---------------------------------------------------------------------------
# Layer 4: Semantic Scholar API
# ---------------------------------------------------------------------------

def fetch_semantic_scholar(paper: PaperImpact) -> SourceStatus:
    """Fetch citations and first author h-index from Semantic Scholar."""
    status = SourceStatus(name="Semantic Scholar", success=False)

    # Step 1: Paper citations
    try:
        time.sleep(1)  # Rate limit courtesy
        url = (
            f"https://api.semanticscholar.org/graph/v1/paper/ArXiv:{paper.arxiv_id}"
            f"?fields=citationCount,influentialCitationCount"
        )
        data = http_get_json(url, timeout=10)
        paper.s2_citations = data.get("citationCount", -1)
        paper.s2_influential = data.get("influentialCitationCount", -1)
        status.success = True
    except urllib.error.HTTPError as e:
        if e.code == 429:
            status.error = "Rate limited (429)"
            return status
        status.error = f"HTTP {e.code}"
        return status
    except Exception as e:
        status.error = str(e)[:100]
        return status

    # Step 2: First author h-index
    if paper.authors:
        try:
            time.sleep(1)
            author_name = paper.authors[0].replace(" ", "+")
            url = (
                f"https://api.semanticscholar.org/graph/v1/author/search"
                f"?query={author_name}&fields=name,hIndex,citationCount&limit=3"
            )
            data = http_get_json(url, timeout=10)
            authors = data.get("data", [])
            if authors:
                # Pick best match by h-index (usually the right person has higher h)
                best = max(authors, key=lambda a: a.get("hIndex") or 0)
                paper.first_author_hindex = best.get("hIndex", -1) or -1
                paper.first_author_name = best.get("name", "")
        except Exception:
            pass  # h-index is bonus data, don't fail over it

    return status


# ---------------------------------------------------------------------------
# Rating synthesis
# ---------------------------------------------------------------------------

def star_rating(score: int, max_score: int = 5) -> str:
    """Generate star rating string."""
    filled = min(score, max_score)
    return "+" * filled + "-" * (max_score - filled)


def synthesize(paper: PaperImpact) -> None:
    """Synthesize overall rating from available data."""
    scores = {}
    available = 0
    total_sources = 4

    # Count available sources
    for s in paper.sources:
        if s.success:
            available += 1

    # --- Venue ---
    venue_score = 0
    if paper.venue:
        venue_upper = paper.venue.upper()
        tier1 = ["ICLR", "NEURIPS", "ICML", "CVPR", "ICCV", "ACL", "EMNLP"]
        tier2 = ["AAAI", "IJCAI", "NAACL", "ECCV", "SIGIR", "KDD", "WWW", "ICRA", "CORL"]
        if any(v in venue_upper for v in tier1):
            venue_score = 5
        elif any(v in venue_upper for v in tier2):
            venue_score = 4
        else:
            venue_score = 3
    scores["venue"] = venue_score

    # --- GitHub ---
    gh_score = 0
    if paper.github_stars >= 0:
        if paper.github_stars >= 1000:
            gh_score = 5
        elif paper.github_stars >= 300:
            gh_score = 4
        elif paper.github_stars >= 50:
            gh_score = 3
        elif paper.github_stars >= 10:
            gh_score = 2
        else:
            gh_score = 1
    scores["github"] = gh_score

    # --- Citations ---
    best_citations = max(paper.openalex_citations, paper.s2_citations)
    cite_score = 0
    if best_citations >= 0:
        if paper.age_days < 90:
            # For very new papers, even a few citations are impressive
            if best_citations >= 20:
                cite_score = 5
            elif best_citations >= 5:
                cite_score = 4
            elif best_citations >= 1:
                cite_score = 3
            else:
                cite_score = 1  # Too new, not informative
        else:
            # For older papers
            if best_citations >= 100:
                cite_score = 5
            elif best_citations >= 30:
                cite_score = 4
            elif best_citations >= 10:
                cite_score = 3
            elif best_citations >= 3:
                cite_score = 2
            else:
                cite_score = 1
    scores["citations"] = cite_score

    # --- Author h-index ---
    author_score = 0
    if paper.first_author_hindex >= 0:
        if paper.first_author_hindex >= 50:
            author_score = 5
        elif paper.first_author_hindex >= 30:
            author_score = 4
        elif paper.first_author_hindex >= 15:
            author_score = 3
        elif paper.first_author_hindex >= 5:
            author_score = 2
        else:
            author_score = 1
    scores["author"] = author_score

    # --- Weighted synthesis (age-dependent) ---
    if paper.age_days < 90:
        # New papers: venue and github matter most
        weights = {"venue": 3.0, "github": 3.0, "citations": 0.5, "author": 2.0}
    elif paper.age_days < 365:
        # Medium-age papers: balanced
        weights = {"venue": 2.0, "github": 2.0, "citations": 2.5, "author": 1.5}
    else:
        # Mature papers: citations dominate
        weights = {"venue": 1.5, "github": 1.0, "citations": 3.5, "author": 1.0}

    # Only use dimensions with data
    total_weight = 0.0
    weighted_sum = 0.0
    for dim, score in scores.items():
        if score > 0:
            w = weights[dim]
            weighted_sum += score * w
            total_weight += w

    if total_weight > 0:
        avg = weighted_sum / total_weight
        if avg >= 4.2:
            paper.rating = "S"
        elif avg >= 3.5:
            paper.rating = "A"
        elif avg >= 2.5:
            paper.rating = "B"
        elif avg >= 1.5:
            paper.rating = "C"
        else:
            paper.rating = "D"
    else:
        paper.rating = "?"

    # Confidence
    if available >= 4:
        paper.confidence = "high"
    elif available >= 3:
        paper.confidence = "medium"
    elif available >= 2:
        paper.confidence = "low"
    else:
        paper.confidence = "very low"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def format_report(paper: PaperImpact) -> str:
    """Generate Markdown impact report."""
    lines = []
    lines.append(f"## Impact: {paper.title}")
    lines.append("")

    # Basic info
    age_str = ""
    if paper.age_days > 0:
        if paper.age_days < 30:
            age_str = f" ({paper.age_days} days ago)"
        elif paper.age_days < 365:
            age_str = f" (~{paper.age_days // 30} months ago)"
        else:
            age_str = f" (~{paper.age_days // 365} years ago)"

    lines.append(f"- **arXiv**: [{paper.arxiv_id}](https://arxiv.org/abs/{paper.arxiv_id})")
    lines.append(f"- **Published**: {paper.published_date}{age_str}")
    if paper.authors:
        authors_str = ", ".join(paper.authors[:5])
        if len(paper.authors) > 5:
            authors_str += f" (+{len(paper.authors) - 5} more)"
        lines.append(f"- **Authors**: {authors_str}")
    if paper.affiliations:
        lines.append(f"- **Affiliations**: {', '.join(paper.affiliations[:5])}")
    lines.append("")

    # Impact table
    lines.append("| Dimension | Data | Signal |")
    lines.append("|-----------|------|--------|")

    # Venue
    if paper.venue:
        venue_upper = paper.venue.upper()
        tier1 = ["ICLR", "NEURIPS", "ICML", "CVPR", "ICCV", "ACL", "EMNLP"]
        tier2 = ["AAAI", "IJCAI", "NAACL", "ECCV", "SIGIR", "KDD", "WWW", "ICRA", "CORL"]
        if any(v in venue_upper for v in tier1):
            sig = "+++++  (Tier-1)"
        elif any(v in venue_upper for v in tier2):
            sig = "++++- (Tier-2)"
        else:
            sig = "+++-- (Other)"
        lines.append(f"| Venue | **{paper.venue}** | {sig} |")
    else:
        lines.append("| Venue | Preprint / Unknown | — |")

    # GitHub
    if paper.github_stars >= 0:
        gh_str = f"[{paper.github_stars} stars / {paper.github_forks} forks]({paper.github_url})"
        if paper.github_stars >= 1000:
            sig = "+++++"
        elif paper.github_stars >= 300:
            sig = "++++-"
        elif paper.github_stars >= 50:
            sig = "+++--"
        elif paper.github_stars >= 10:
            sig = "++---"
        else:
            sig = "+----"
        lines.append(f"| GitHub | {gh_str} | {sig} |")
    elif paper.github_url:
        lines.append(f"| GitHub | [{paper.github_url}]({paper.github_url}) (fetch failed) | — |")
    else:
        lines.append("| GitHub | No repo found | — |")

    # Citations
    cite_parts = []
    if paper.openalex_citations >= 0:
        cite_parts.append(f"OpenAlex: {paper.openalex_citations}")
    if paper.s2_citations >= 0:
        cite_parts.append(f"S2: {paper.s2_citations}")
        if paper.s2_influential >= 0:
            cite_parts.append(f"influential: {paper.s2_influential}")
    if cite_parts:
        best = max(paper.openalex_citations, paper.s2_citations)
        if paper.age_days < 90 and best == 0:
            sig = "----- (too new)"
        elif best >= 100:
            sig = "+++++"
        elif best >= 30:
            sig = "++++-"
        elif best >= 10:
            sig = "+++--"
        elif best >= 3:
            sig = "++---"
        else:
            sig = "+----"
        lines.append(f"| Citations | {' / '.join(cite_parts)} | {sig} |")
    else:
        lines.append("| Citations | Data unavailable | — |")

    # Author h-index
    if paper.first_author_hindex >= 0:
        author_name = paper.first_author_name or paper.authors[0] if paper.authors else "?"
        if paper.first_author_hindex >= 50:
            sig = "+++++"
        elif paper.first_author_hindex >= 30:
            sig = "++++-"
        elif paper.first_author_hindex >= 15:
            sig = "+++--"
        elif paper.first_author_hindex >= 5:
            sig = "++---"
        else:
            sig = "+----"
        lines.append(f"| Author h-index | {author_name}: h={paper.first_author_hindex} | {sig} |")
    else:
        lines.append("| Author h-index | Data unavailable | — |")

    lines.append("")

    # Overall
    lines.append(f"**Rating**: {paper.rating}")
    lines.append(f"**Confidence**: {paper.confidence}")

    # Data completeness
    ok = sum(1 for s in paper.sources if s.success)
    total = len(paper.sources)
    lines.append(f"**Data completeness**: {ok}/{total} sources available")

    # Source details
    failed = [s for s in paper.sources if not s.success]
    if failed:
        fail_strs = [f"{s.name} ({s.error})" for s in failed]
        lines.append(f"**Failed sources**: {', '.join(fail_strs)}")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def analyze_paper(arxiv_id: str) -> str:
    """Analyze a single paper and return Markdown report."""
    # Clean input
    arxiv_id = arxiv_id.strip().replace("https://arxiv.org/abs/", "").replace("http://arxiv.org/abs/", "")

    # Layer 1: arXiv
    paper, arxiv_status = fetch_arxiv(arxiv_id)
    paper.sources.append(arxiv_status)

    if not arxiv_status.success:
        return f"## Error: Could not fetch arXiv metadata for {arxiv_id}\n\n{arxiv_status.error}\n"

    # Layer 2: GitHub
    gh_status = fetch_github(paper)
    paper.sources.append(gh_status)

    # Layer 3: OpenAlex
    oa_status = fetch_openalex(paper)
    paper.sources.append(oa_status)

    # Layer 4: Semantic Scholar
    s2_status = fetch_semantic_scholar(paper)
    paper.sources.append(s2_status)

    # Synthesize rating
    synthesize(paper)

    # Generate report
    return format_report(paper)


def analyze_paper_full(arxiv_id: str) -> Tuple[str, PaperImpact]:
    """Analyze a single paper and return both report and data object."""
    arxiv_id = arxiv_id.strip().replace("https://arxiv.org/abs/", "").replace("http://arxiv.org/abs/", "")
    paper, arxiv_status = fetch_arxiv(arxiv_id)
    paper.sources.append(arxiv_status)
    if not arxiv_status.success:
        return f"## Error: Could not fetch arXiv metadata for {arxiv_id}\n\n{arxiv_status.error}\n", paper
    gh_status = fetch_github(paper)
    paper.sources.append(gh_status)
    oa_status = fetch_openalex(paper)
    paper.sources.append(oa_status)
    s2_status = fetch_semantic_scholar(paper)
    paper.sources.append(s2_status)
    synthesize(paper)
    return format_report(paper), paper


def main():
    parser = argparse.ArgumentParser(description="Paper Impact Analyzer")
    parser.add_argument("arxiv_ids", nargs="+", help="arXiv paper IDs (e.g. 2603.04948)")
    args = parser.parse_args()

    results = []
    for arxiv_id in args.arxiv_ids:
        report, paper = analyze_paper_full(arxiv_id)
        results.append((report, paper))
        if len(args.arxiv_ids) > 1:
            time.sleep(1)

    # Print all reports
    output = "\n---\n\n".join(r[0] for r in results)
    print(output)

    # If multiple papers, print comparison table
    if len(args.arxiv_ids) > 1:
        print("\n---\n")
        print("## Comparison Summary\n")
        print("| Paper | Rating | GitHub | Citations | Venue |")
        print("|-------|--------|--------|-----------|-------|")
        for _, paper in results:
            short_title = paper.title[:40] + ("..." if len(paper.title) > 40 else "")
            gh = f"{paper.github_stars}" if paper.github_stars >= 0 else "—"
            best_cite = max(paper.openalex_citations, paper.s2_citations)
            cite = str(best_cite) if best_cite >= 0 else "—"
            venue = paper.venue if paper.venue else "Preprint"
            print(f"| {short_title} | **{paper.rating}** | {gh} | {cite} | {venue} |")
        print()


if __name__ == "__main__":
    main()
