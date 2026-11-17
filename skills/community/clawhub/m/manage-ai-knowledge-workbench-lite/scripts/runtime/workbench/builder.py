"""Deterministic Markdown knowledge-layer generation."""

from __future__ import annotations

import html
from pathlib import Path
import tempfile
from typing import Any

from .config import normalized, now_iso


VISIBLE_SENSITIVITY = {"public", "internal"}


def _md(value: Any) -> str:
    escaped = html.escape(str(value), quote=False)
    return escaped.replace("|", "\\|").replace("\n", " ")[:500]


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
    ) as handle:
        handle.write(content)
        handle.flush()
        temp_path = Path(handle.name)
    temp_path.replace(path)


def visible_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        record
        for record in records
        if record.get("sensitivity") in VISIBLE_SENSITIVITY and not record.get("sensitive")
    ]


def _source_index(records: list[dict[str, Any]]) -> str:
    lines = [
        "# Source Index",
        "",
        "> Derived metadata only. Source bodies and absolute source paths are not embedded.",
        "",
        "| Source | Relative path | Type | Sensitivity | Updated fingerprint |",
        "|---|---|---|---|---|",
    ]
    for record in records:
        lines.append(
            "| {source} | {path} | {kind} | {sensitivity} | `{digest}` |".format(
                source=_md(record["source_id"]),
                path=_md(record["path"]),
                kind=_md(record["kind"]),
                sensitivity=_md(record.get("sensitivity", "unknown") or "unknown"),
                digest=str(record["sha256"])[:12],
            )
        )
    return "\n".join(lines) + "\n"


def _tag_index(records: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for record in records:
        for tag in record.get("tags", []):
            counts[str(tag)] = counts.get(str(tag), 0) + 1
    lines = ["# Tag Index", "", "| Tag | Records |", "|---|---:|"]
    if not counts:
        lines.append("| No tags | 0 |")
    else:
        for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold())):
            lines.append(f"| {_md(tag)} | {count} |")
    return "\n".join(lines) + "\n"


def _project_index(records: list[dict[str, Any]]) -> str:
    projects = [
        record
        for record in records
        if record.get("kind") == "markdown"
        and str(record.get("properties", {}).get("type", "")).lower() == "project"
    ]
    lines = [
        "# Project Index",
        "",
        "> Progress is shown only when an explicit percentage, basis, and milestone denominator are present.",
        "",
        "| Project | Source path | Progress | Confidence | Basis |",
        "|---|---|---:|---|---|",
    ]
    if not projects:
        lines.append("| No project records | - | unknown | low | No accepted denominator |")
    for record in projects:
        progress = record.get("progress") or {"status": "unknown"}
        if progress.get("status") == "known":
            value = f"{progress['value']:g}%"
            confidence = progress.get("confidence") or "unknown"
            basis = progress.get("basis") or ""
        else:
            value = "unknown"
            confidence = "low"
            basis = "No accepted denominator"
        lines.append(
            f"| {_md(record['title'])} | {_md(record['source_id'])}/{_md(record['path'])} | "
            f"{_md(value)} | {_md(confidence)} | {_md(basis)} |"
        )
    return "\n".join(lines) + "\n"


def build_knowledge_pages(
    *,
    config: dict[str, Any],
    records: list[dict[str, Any]],
    validation: dict[str, Any],
) -> list[Path]:
    knowledge = normalized(config["paths"]["knowledge"])
    visible = visible_records(records)
    summary = validation["summary"]
    pages = {
        knowledge / "00-入口.md": "\n".join(
            [
                "# AI Knowledge Workbench",
                "",
                "> This is a derived local knowledge layer. Original source files remain authoritative and read-only.",
                "",
                f"- Visible metadata records: {len(visible)}",
                f"- Total source records: {len(records)}",
                f"- Sensitive or unknown-sensitivity records excluded from views: {summary['sensitive_total']}",
                f"- Resolved relations: {summary['edges_total']}",
                f"- Validation issues: {summary['issues_total']}",
                f"- Privacy mode: {config['privacy_mode']}",
                "- Dashboard body embedded: false",
                "",
            ]
        ),
        knowledge / "10-索引" / "来源索引.md": _source_index(visible),
        knowledge / "20-主题" / "标签索引.md": _tag_index(visible),
        knowledge / "30-项目" / "项目索引.md": _project_index(visible),
        knowledge / "40-行动" / "行动索引.md": "# Action Index\n\n- No deterministic actions were inferred.\n",
        knowledge / "80-待审核" / "待审核.md": "\n".join(
            [
                "# Review Queue",
                "",
                f"- Broken links: {len(validation['broken_links'])}",
                f"- Ambiguous links: {len(validation['ambiguous_links'])}",
                f"- Duplicate title groups: {len(validation['duplicate_titles'])}",
                f"- Missing sensitivity: {len(validation['missing_sensitivity'])}",
                f"- Unknown project progress: {len(validation['invalid_progress'])}",
                "",
            ]
        ),
        knowledge / "99-系统" / "构建状态.md": "\n".join(
            [
                "# Build Status",
                "",
                f"- Generated at: {now_iso()}",
                f"- Source files: {len(records)}",
                f"- Visible records: {len(visible)}",
                f"- Content access: {config.get('content_access', 'unknown')}",
                f"- Model transport: {config.get('model_transport', 'none')}",
                "- Source files changed: false",
                "",
            ]
        ),
    }
    for path, content in pages.items():
        atomic_write_text(path, content)
    return sorted(pages)


def assert_no_html_body_embedding(value: str) -> str:
    """Reserved for P4; keep HTML escaping behavior independently testable."""

    return html.escape(value, quote=True)
