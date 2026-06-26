from __future__ import annotations

import json
from pathlib import Path

from openclaw_sec.models import CATEGORY_ORDER, AuditReport, Finding, SEVERITY_ORDER


SCORE_DEDUCTIONS = {
    "critical": 25,
    "high": 12,
    "medium": 5,
    "low": 2,
    "info": 0,
}


def sort_findings(findings: list[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda item: (
            SEVERITY_ORDER.get(item.severity, 99),
            CATEGORY_ORDER.get(item.category, 99),
            item.id,
        ),
    )


def summarize_findings(findings: list[Finding]) -> dict[str, object]:
    counts = {severity: 0 for severity in SEVERITY_ORDER}
    score = 100
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
        score -= SCORE_DEDUCTIONS.get(finding.severity, 0)
    score = max(0, min(100, score))
    return {
        "score": score,
        "severity_counts": counts,
        "top_findings": [finding.to_dict() for finding in sort_findings(findings)[:5]],
        "finding_count": len(findings),
    }


def render_text(report: AuditReport) -> str:
    summary = report.summary
    counts = summary["severity_counts"]
    lines = [
        f"OpenClaw-Sec Audit {report.version}",
        f"Generated: {report.generated_at}",
        f"Overall score: {summary['score']}/100",
        "Severity counts:",
        f"  critical: {counts['critical']}",
        f"  high: {counts['high']}",
        f"  medium: {counts['medium']}",
        f"  low: {counts['low']}",
        f"  info: {counts['info']}",
        "",
        "Top 5 findings:",
    ]
    top_findings = summary["top_findings"]
    if not top_findings:
        lines.append("  none")
    else:
        for finding in top_findings:
            lines.append(f"  - [{finding['severity']}] {finding['id']} {finding['title']}")
    if report.notes:
        lines.extend(["", "Notes:"])
        for note in report.notes[:10]:
            lines.append(f"  - {note}")
    return "\n".join(lines)


def render_json(report: AuditReport) -> str:
    return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)


def render_markdown(report: AuditReport) -> str:
    summary = report.summary
    counts = summary["severity_counts"]
    lines = [
        "# OpenClaw-Sec Audit Report",
        "",
        "## Executive summary",
        f"- Generated at: {report.generated_at}",
        f"- Overall score: {summary['score']}/100",
        f"- Total findings: {summary['finding_count']}",
        "",
        "## Score & severity counts",
        f"- critical: {counts['critical']}",
        f"- high: {counts['high']}",
        f"- medium: {counts['medium']}",
        f"- low: {counts['low']}",
        f"- info: {counts['info']}",
        "",
        "## Findings by severity",
    ]
    grouped = {severity: [] for severity in SEVERITY_ORDER}
    for finding in sort_findings(report.findings):
        grouped[finding.severity].append(finding)
    for severity in ("critical", "high", "medium", "low", "info"):
        lines.append(f"### {severity}")
        if not grouped[severity]:
            lines.append("- none")
            continue
        for finding in grouped[severity]:
            lines.append(f"- `{finding.id}` {finding.title}")
    lines.extend(["", "## Detailed evidence"])
    for finding in sort_findings(report.findings):
        lines.append(f"### {finding.id} {finding.title}")
        lines.append(f"- Category: {finding.category}")
        lines.append(f"- Severity: {finding.severity}")
        lines.append(f"- Confidence: {finding.confidence}")
        lines.append(f"- Heuristic: {str(finding.heuristic).lower()}")
        lines.append(f"- Risk: {finding.risk}")
        if finding.masked_examples:
            lines.append(f"- Masked examples: {', '.join(finding.masked_examples[:8])}")
        lines.append("- Evidence:")
        for item in finding.evidence[:12]:
            lines.append(f"  - {item}")
        lines.append("")
    lines.extend(["## Fix recommendations"])
    for finding in sort_findings(report.findings):
        lines.append(f"- `{finding.id}` {finding.recommendation}")
    lines.extend(["", "## Immediate next steps"])
    for finding in sort_findings(report.findings)[:5]:
        lines.append(f"- Address `{finding.id}`: {finding.recommendation}")
    lines.extend(["", "## Limitations / unsupported checks"])
    if report.notes:
        for note in report.notes:
            lines.append(f"- {note}")
    else:
        lines.append("- none")
    return "\n".join(lines)


def write_reports(report: AuditReport, output_dir: Path, output_format: str) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    formats = {"text", "json", "md"} if output_format == "all" else {output_format}
    if "text" in formats:
        path = output_dir / "summary.txt"
        path.write_text(render_text(report) + "\n", encoding="utf-8")
        paths["text"] = str(path)
    if "json" in formats:
        path = output_dir / "report.json"
        path.write_text(render_json(report) + "\n", encoding="utf-8")
        paths["json"] = str(path)
    if "md" in formats:
        path = output_dir / "report.md"
        path.write_text(render_markdown(report) + "\n", encoding="utf-8")
        paths["md"] = str(path)
    return paths
