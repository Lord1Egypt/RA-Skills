"""Assemble graded findings + charts into a structured Markdown report.

Deterministic layout: a priority-count summary, findings ordered P0->P3 with
every field spelled out, then embedded chart PNGs. The LLM layer may re-word
prose around this, but the facts and structure originate here.
"""
from __future__ import annotations
from pathlib import Path
import plotly.graph_objects as go
from ib_common.charts.render import render
from .findings import Finding, Priority

_ORDER = {Priority.P0: 0, Priority.P1: 1, Priority.P2: 2, Priority.P3: 3}


def sort_findings(findings: list[Finding]) -> list[Finding]:
    """Stable sort by priority, P0 first."""
    return sorted(findings, key=lambda f: _ORDER[f.priority])


def _summary_line(findings: list[Finding]) -> str:
    """One-line count of findings per priority."""
    counts = {p: 0 for p in Priority}
    for f in findings:
        counts[f.priority] += 1
    parts = [f"{p.value}: {counts[p]}" for p in Priority]
    return "**Summary** — " + ", ".join(parts)


def to_markdown(findings: list[Finding], chart_paths: dict[str, str]) -> str:
    """Render findings + chart references to a structured Markdown string."""
    lines: list[str] = ["# Portfolio Diagnostic Report", "", _summary_line(findings), ""]
    for f in sort_findings(findings):
        lines += [
            f"## [{f.priority.value}] {f.dimension}",
            f"- **Finding:** {f.finding}",
            f"- **Evidence:** `{f.evidence}`",
            f"- **Impact:** {f.impact}",
            f"- **Suggestion:** {f.suggestion}",
            f"- **Trigger:** {f.trigger_condition}",
            f"- **Confidence:** {f.confidence:.0%}",
            f"- **Data limitations:** {f.data_limitations}",
            "",
        ]
    if chart_paths:
        lines.append("## Charts")
        for name, png in chart_paths.items():
            lines.append(f"![{name}]({png})")
        lines.append("")
    return "\n".join(lines)


def build_report(findings: list[Finding], figures: dict[str, go.Figure],
                 out_dir: str | Path) -> dict:
    """Render charts, write report.md, and return the produced paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    chart_products: dict[str, dict] = {}
    chart_paths: dict[str, str] = {}
    for name, fig in figures.items():
        products = render(fig, out, name)
        chart_products[name] = {k: str(v) for k, v in products.items()}
        chart_paths[name] = products["png"].name    # relative for embedding
    md = to_markdown(findings, chart_paths)
    report_path = out / "report.md"
    report_path.write_text(md, encoding="utf-8")
    return {"report": str(report_path), "charts": chart_products}
