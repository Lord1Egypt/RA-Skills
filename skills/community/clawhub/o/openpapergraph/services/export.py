"""Export papers to BibTeX, CSV, Markdown, or JSON."""
import csv
import io
import json
from typing import List

from schemas import Paper


def _sort_by_year(papers: List[Paper], ascending: bool = False) -> List[Paper]:
    """Sort papers by year. None-year papers go last."""
    return sorted(papers, key=lambda p: (0 if p.year else 1, (p.year or 0) * (1 if ascending else -1), (p.title or "").lower()))


def to_bibtex(papers: List[Paper]) -> str:
    entries = []
    for p in _sort_by_year(papers):
        author_str = " and ".join(p.authors) if p.authors else "Unknown"
        key = p.id.replace("/", "_").replace(":", "_")[:30]
        entries.append(
            f"@article{{{key},\n"
            f"  title = {{{p.title}}},\n"
            f"  author = {{{author_str}}},\n"
            f"  year = {{{p.year or ''}}},\n"
            f"  url = {{{p.url or ''}}},\n"
            f"}}\n"
        )
    return "\n".join(entries)


def to_csv(papers: List[Paper]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["id", "title", "authors", "year", "citation_count", "source", "url", "doi", "arxiv_id", "abstract"])
    for p in _sort_by_year(papers):
        writer.writerow([
            p.id, p.title, "; ".join(p.authors), p.year or "", p.citation_count,
            p.source or "", p.url or "", p.doi or "", p.arxiv_id or "",
            (p.abstract or "")[:500],
        ])
    return buf.getvalue()


def to_markdown(papers: List[Paper]) -> str:
    """Export papers as a Markdown list sorted by year descending."""
    lines = [f"# Paper List ({len(papers)} papers)\n"]
    for i, p in enumerate(_sort_by_year(papers), 1):
        lines.append(f"## {i}. {p.title or 'Untitled'}\n")
        lines.append(f"- **Year:** {p.year or 'N/A'}")
        lines.append(f"- **Authors:** {', '.join(p.authors) if p.authors else 'Unknown'}")
        lines.append(f"- **Citations:** {p.citation_count}")
        if p.source:
            lines.append(f"- **Source:** {p.source}")
        if p.url:
            lines.append(f"- **URL:** {p.url}")
        if p.doi:
            lines.append(f"- **DOI:** {p.doi}")
        if p.arxiv_id:
            lines.append(f"- **arXiv:** {p.arxiv_id}")
        if p.abstract:
            lines.append(f"- **Abstract:** {p.abstract[:500]}{'…' if len(p.abstract) > 500 else ''}")
        lines.append(f"- **ID:** {p.id}")
        lines.append("")
    return "\n".join(lines)


def to_json(papers: List[Paper]) -> str:
    """Export papers as formatted JSON sorted by year descending."""
    sorted_papers = _sort_by_year(papers)
    return json.dumps([p.to_dict() for p in sorted_papers], indent=2, ensure_ascii=False)
