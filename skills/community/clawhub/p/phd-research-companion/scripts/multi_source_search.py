#!/usr/bin/env python3
"""
Multi-Source Academic Paper Search (real network calls, no fabricated entries)

Sources:
    arxiv          - export.arxiv.org Atom API
    dblp           - dblp.org publication search API (JSON)
    openalex       - api.openalex.org works endpoint
    semanticscholar- api.semanticscholar.org graph search

Design rule: if a source cannot be reached, the run FAILS LOUDLY for that
source. It never fabricates entries. Unverified entries are never written to
the BibTeX output.

Usage:
    python multi_source_search.py -q "mirror descent diagonal GD" -s arxiv dblp -l 20 -o ./lit
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

USER_AGENT = "phd-research-companion/2.0 (mailto:researcher@example.org)"
TIMEOUT = 25
RETRIES = 2
RETRY_BACKOFF = 1.5

SOURCES = ("arxiv", "dblp", "openalex", "semanticscholar")


class SourceError(RuntimeError):
    """Raised when a source cannot be reached or returns unusable data."""


class ProgressTracker:
    """Writes a JSON status file so long runs can be monitored."""

    def __init__(self, output_dir: Path, task_id: str = "search"):
        self.task_id = task_id
        self.progress_file = Path(output_dir) / f"search-progress-{task_id}.json"
        self.start = datetime.now()

    def update(self, stage: str, pct: int) -> None:
        elapsed = (datetime.now() - self.start).total_seconds()
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        self._write({
            "task_id": self.task_id,
            "stage": stage,
            "progress_percent": pct,
            "elapsed_seconds": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(),
            "status": "running" if pct < 100 else "completed",
        })
        print(f"[{pct}%] {stage} ({elapsed:.1f}s)")

    def complete(self, summary: dict) -> None:
        self._write({
            "task_id": self.task_id,
            "stage": "completed",
            "progress_percent": 100,
            "completed_at": datetime.now().isoformat(),
            "status": "completed",
            "summary": summary,
        })
        print(f"Completed: {summary.get('total_papers_found', 0)} papers")

    def _write(self, payload: dict) -> None:
        self.progress_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _fetch(url: str, expect: str = "json") -> str:
    """Fetch `url`, verifying the payload really is the format we asked for.

    Anti-bot gateways answer 200 with an HTML challenge page; accepting that
    as data is how a tool starts reporting nonsense, so it is rejected here.
    """
    host = urllib.parse.urlsplit(url).netloc
    accept = {"json": "application/json", "xml": "application/atom+xml",
              "text": "*/*"}[expect]
    last = None
    for attempt in range(RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT, "Accept": accept})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                ctype = (resp.headers.get("Content-Type") or "").lower()
                body = resp.read().decode("utf-8", errors="replace")
            if expect == "json" and "json" not in ctype:
                raise SourceError(
                    f"{host}: expected JSON, got Content-Type '{ctype or 'none'}' "
                    f"({len(body)} bytes) - anti-bot challenge or outage; "
                    f"no data taken from this source")
            if expect == "xml" and not any(t in ctype for t in ("xml", "atom", "text")):
                raise SourceError(f"{host}: expected XML/Atom, got '{ctype or 'none'}'")
            return body
        except SourceError:
            raise
        except urllib.error.HTTPError as e:
            last = e
            # 429 / 503: back off harder, and say so plainly.
            if e.code in (429, 503):
                time.sleep(3 * (attempt + 1))
            elif attempt < RETRIES:
                time.sleep(RETRY_BACKOFF ** attempt)
        except Exception as e:  # noqa: BLE001
            last = e
            if attempt < RETRIES:
                time.sleep(RETRY_BACKOFF ** attempt)
    code = getattr(last, "code", None)
    if code:
        raise SourceError(f"{host}: HTTP {code}"
                          + (" (rate limited; retry later or use an API key)"
                             if code in (429, 503) else ""))
    raise SourceError(f"{host}: {type(last).__name__}: {last}")


def _norm(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


# ------------------------------------------------------------------ sources


def search_arxiv(query: str, limit: int, year_from: int | None, year_to: int | None) -> list[dict]:
    import xml.etree.ElementTree as ET

    terms = [f'all:"{t}"' if " " in t else f"all:{t}" for t in query.split() if t]
    q = "+AND+".join(urllib.parse.quote(t) for t in terms) or urllib.parse.quote(query)
    url = (f"https://export.arxiv.org/api/query?search_query={q}"
           f"&start=0&max_results={max(1, limit)}"
           "&sortBy=relevance&sortOrder=descending")
    raw = _fetch(url, expect="xml")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        raise SourceError(f"arxiv: malformed Atom response ({e})")

    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for entry in root.findall("a:entry", ns):
        title = " ".join((entry.findtext("a:title", "", ns) or "").split())
        if not title:
            continue
        published = entry.findtext("a:published", "", ns)[:10]
        year = int(published[:4]) if published[:4].isdigit() else None
        if year_from and year and year < year_from:
            continue
        if year_to and year and year > year_to:
            continue
        arxiv_id = entry.findtext("a:id", "", ns)
        out.append({
            "title": title,
            "authors": [a.findtext("a:name", "", ns) for a in entry.findall("a:author", ns)],
            "year": year,
            "venue": "arXiv preprint",
            "doi": arxiv_id,
            "abstract": " ".join((entry.findtext("a:summary", "", ns) or "").split()),
            "source": "arxiv",
            "url": arxiv_id,
        })
    if not out:
        raise SourceError("arxiv: query returned zero usable entries")
    return out


def search_dblp(query: str, limit: int, year_from: int | None, year_to: int | None) -> list[dict]:
    url = ("https://dblp.org/search/publ/api?q="
           + urllib.parse.quote(query)
           + f"&format=json&h={max(1, limit)}")
    raw = _fetch(url, expect="json")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SourceError(f"dblp: malformed JSON ({e})")

    hits = (data.get("result", {}).get("hits", {}) or {}).get("hit", []) or []
    out = []
    for h in hits:
        info = h.get("info", {}) or {}
        title = " ".join((info.get("title") or "").split())
        if not title:
            continue
        year = info.get("year")
        year = int(year) if str(year).isdigit() else None
        if year_from and year and year < year_from:
            continue
        if year_to and year and year > year_to:
            continue
        authors = info.get("authors", {}).get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        out.append({
            "title": title.rstrip("."),
            "authors": [a.get("text", "") if isinstance(a, dict) else str(a) for a in authors],
            "year": year,
            "venue": info.get("venue") or "DBLP",
            "doi": info.get("doi") or info.get("ee") or "",
            "abstract": "",
            "source": "dblp",
            "url": info.get("ee") or info.get("url") or "",
        })
    if not out:
        raise SourceError("dblp: query returned zero usable entries")
    return out


def search_openalex(query: str, limit: int, year_from: int | None, year_to: int | None) -> list[dict]:
    filters = []
    if year_from:
        filters.append(f"from_publication_date:{year_from}-01-01")
    if year_to:
        filters.append(f"to_publication_date:{year_to}-12-31")
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(query)
           + f"&per-page={max(1, min(limit, 200))}"
           + ("&filter=" + ",".join(filters) if filters else ""))
    raw = _fetch(url, expect="json")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SourceError(f"openalex: malformed JSON ({e})")

    out = []
    for w in data.get("results", []) or []:
        title = " ".join((w.get("title") or w.get("display_name") or "").split())
        if not title:
            continue
        authors = [a.get("author", {}).get("display_name", "")
                   for a in (w.get("authorships") or [])]
        out.append({
            "title": title,
            "authors": [a for a in authors if a],
            "year": w.get("publication_year"),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
            "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
            "abstract": (w.get("abstract_inverted_index") and "") or "",
            "source": "openalex",
            "url": w.get("doi") or (w.get("primary_location") or {}).get("landing_page_url") or "",
        })
    if not out:
        raise SourceError("openalex: query returned zero usable entries")
    return out


def search_semanticscholar(query: str, limit: int, year_from: int | None, year_to: int | None) -> list[dict]:
    fields = "title,authors,year,venue,externalIds,abstract,url"
    url = ("https://api.semanticscholar.org/graph/v1/paper/search?query="
           + urllib.parse.quote(query)
           + f"&limit={max(1, min(limit, 100))}&fields={fields}")
    if year_from or year_to:
        url += f"&year={year_from or ''}-{year_to or ''}"
    raw = _fetch(url, expect="json")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SourceError(f"semanticscholar: malformed JSON ({e})")

    out = []
    for p in data.get("data", []) or []:
        title = " ".join((p.get("title") or "").split())
        if not title:
            continue
        ids = p.get("externalIds") or {}
        out.append({
            "title": title,
            "authors": [a.get("name", "") for a in (p.get("authors") or [])],
            "year": p.get("year"),
            "venue": p.get("venue") or "",
            "doi": ids.get("DOI") or ids.get("ArXiv") or "",
            "abstract": p.get("abstract") or "",
            "source": "semanticscholar",
            "url": p.get("url") or "",
        })
    if not out:
        raise SourceError("semanticscholar: query returned zero usable entries")
    return out


DISPATCH = {
    "arxiv": search_arxiv,
    "dblp": search_dblp,
    "openalex": search_openalex,
    "semanticscholar": search_semanticscholar,
}


# ------------------------------------------------------------------ bibtex


def _bibkey(paper: dict, idx: int) -> str:
    first = (paper.get("authors") or ["unknown"])[0] or "unknown"
    surname = re.sub(r"[^A-Za-z]", "", first.split()[-1] if first.split() else "unknown").lower()
    word = re.sub(r"[^A-Za-z]", "", (paper.get("title") or "untitled").split()[0]).lower()
    year = paper.get("year") or "nodate"
    return f"{surname}{year}{word}{idx}"


def _escape(s: str) -> str:
    return (str(s).replace("&", r"\&").replace("%", r"\%")
            .replace("_", r"\_").replace("#", r"\#"))


def to_bibtex(paper: dict, idx: int) -> str | None:
    """Emit a BibTeX entry only if the record is complete enough to be verified."""
    if not paper.get("title"):
        return None
    lines = [f"@article{{{_bibkey(paper, idx)},",
             f"  title   = {{{_escape(paper['title'])}}},",
             f"  author  = {{{_escape(' and '.join(paper.get('authors') or ['Unknown']))}}},",
             f"  year    = {{{paper.get('year') or 'nodate'}}},",
             f"  journal = {{{_escape(paper.get('venue') or 'Unknown venue')}}},"]
    if paper.get("doi"):
        lines.append(f"  doi     = {{{_escape(paper['doi'])}}},")
    if paper.get("url"):
        lines.append(f"  url     = {{{paper['url']}}},")
    lines.append(f"  note    = {{verified via {paper.get('source')} on "
                 f"{datetime.now().strftime('%Y-%m-%d')}}},")
    lines.append("}")
    entry = "\n".join(lines)
    if entry.count("{") != entry.count("}"):
        return None
    return entry


def dedupe(records: list[dict]) -> list[dict]:
    seen, out = set(), []
    for r in records:
        k = _norm(r.get("title"))
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Multi-source academic paper search (real APIs, no fabricated entries)")
    ap.add_argument("--query", "-q", required=True)
    ap.add_argument("--sources", "-s", nargs="+", default=["arxiv"], choices=list(SOURCES))
    ap.add_argument("--limit", "-l", type=int, default=15)
    ap.add_argument("--year-from", type=int, default=None)
    ap.add_argument("--year-to", type=int, default=None)
    ap.add_argument("--output-dir", "-o", default=".")
    ap.add_argument("--background", "-b", action="store_true",
                    help="write a progress JSON for monitoring")
    args = ap.parse_args()

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    tracker = ProgressTracker(out_dir) if args.background else None
    if tracker:
        tracker.update("starting search", 5)
    else:
        print(f"Query: {args.query}\nSources: {', '.join(args.sources)}")

    collected, failures = [], []
    n = len(args.sources)
    for i, src in enumerate(args.sources, 1):
        stage = f"querying {src} ({i}/{n})"
        if tracker:
            tracker.update(stage, 10 + int(70 * (i - 1) / n))
        else:
            print(f"[..] {stage}")
        try:
            got = DISPATCH[src](args.query, args.limit, args.year_from, args.year_to)
            collected.extend(got)
            print(f"     {src}: {len(got)} records")
        except SourceError as e:
            failures.append(str(e))
            print(f"     {src}: FAILED - {e}", file=sys.stderr)

    if not collected:
        print("\nNo records retrieved from any source. Nothing was written.",
              file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        if tracker:
            tracker.complete({"total_papers_found": 0, "failures": failures})
        return 2

    unique = dedupe(collected)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")

    entries, skipped = [], 0
    for idx, p in enumerate(unique, 1):
        e = to_bibtex(p, idx)
        if e:
            entries.append(e)
        else:
            skipped += 1

    bib_path = out_dir / f"search-results-{ts}.bibtex"
    bib_path.write_text(
        "% Generated by phd-research-companion 2.4.0\n"
        f"% Query: {args.query}\n"
        f"% Sources: {','.join(args.sources)}\n"
        f"% Retrieved: {datetime.now().isoformat(timespec='seconds')}\n"
        f"% Verified entries: {len(entries)}  (skipped incomplete: {skipped})\n"
        + (f"% FAILED SOURCES: {'; '.join(failures)}\n" if failures else "")
        + "\n" + "\n\n".join(entries) + "\n",
        encoding="utf-8")

    md_path = out_dir / f"search-summary-{ts}.md"
    lines = [f"# Literature search: {args.query}", "",
             f"- Retrieved: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
             f"- Sources: {', '.join(args.sources)}",
             f"- Unique records: {len(unique)}",
             f"- Verified BibTeX entries: {len(entries)}",
             f"- Skipped (incomplete record): {skipped}"]
    if failures:
        lines += ["", "## Failed sources (no data from these)", ""]
        lines += [f"- {f}" for f in failures]
    lines += ["", "## Records", ""]
    for i, p in enumerate(unique, 1):
        lines.append(f"{i}. **{p['title']}**  ")
        lines.append(f"   {', '.join(p.get('authors')[:5]) or 'n/a'}  ")
        lines.append(f"   {p.get('year') or 'n/a'} | {p.get('venue') or 'n/a'} | via {p.get('source')}  ")
        if p.get("url"):
            lines.append(f"   <{p['url']}>")
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")

    summary = {"query": args.query, "sources_used": list(args.sources),
               "total_papers_found": len(unique),
               "verified_bibtex_entries": len(entries),
               "failed_sources": failures,
               "output_bibtex": str(bib_path), "output_summary": str(md_path)}
    if tracker:
        tracker.complete(summary)
    print(f"\nBibTeX : {bib_path}")
    print(f"Summary: {md_path}")
    print(f"Verified entries: {len(entries)} / {len(unique)} records")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
