"""Metadata-only link, provenance, sensitivity, and progress validation."""

from __future__ import annotations

import posixpath
from pathlib import PurePosixPath
from typing import Any


def _indexes(records: list[dict[str, Any]]) -> dict[str, dict[Any, list[tuple[str, str]]]]:
    by_rel: dict[tuple[str, str], list[tuple[str, str]]] = {}
    by_no_suffix: dict[tuple[str, str], list[tuple[str, str]]] = {}
    by_stem: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for record in records:
        if record.get("kind") != "markdown":
            continue
        source_id = str(record["source_id"])
        relative = str(record["path"])
        key = (source_id, relative)
        by_rel.setdefault((source_id, relative.casefold()), []).append(key)
        no_suffix = str(PurePosixPath(relative).with_suffix(""))
        by_no_suffix.setdefault((source_id, no_suffix.casefold()), []).append(key)
        by_stem.setdefault((source_id, PurePosixPath(relative).stem.casefold()), []).append(key)
    return {"by_rel": by_rel, "by_no_suffix": by_no_suffix, "by_stem": by_stem}


def _resolve_link(
    record: dict[str, Any], link: dict[str, str], indexes: dict[str, dict[Any, list[tuple[str, str]]]]
) -> list[tuple[str, str]]:
    source_id = str(record["source_id"])
    source_path = PurePosixPath(str(record["path"]))
    raw = str(link["target"]).replace("\\", "/")
    candidates: list[tuple[str, str]] = []
    if link["kind"] == "markdown" or "/" in raw:
        normalized_target = posixpath.normpath(str(source_path.parent / raw))
        candidates.extend(indexes["by_rel"].get((source_id, normalized_target.casefold()), []))
        without_suffix = str(PurePosixPath(normalized_target).with_suffix(""))
        candidates.extend(indexes["by_no_suffix"].get((source_id, without_suffix.casefold()), []))
    if not candidates:
        target_path = PurePosixPath(raw)
        candidates.extend(indexes["by_stem"].get((source_id, target_path.stem.casefold()), []))
    unique = sorted(set(candidates))
    return unique


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    all_markdown_records = [record for record in records if record.get("kind") == "markdown"]
    # Detailed diagnostics are user-facing derived data. Never echo paths,
    # titles, tags, or link targets from records already classified sensitive.
    markdown_records = [record for record in all_markdown_records if not record.get("sensitive")]
    indexes = _indexes(markdown_records)
    broken_links: list[dict[str, str]] = []
    ambiguous_links: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []
    connected: set[tuple[str, str]] = set()

    for record in markdown_records:
        source_key = (str(record["source_id"]), str(record["path"]))
        for link in record.get("links", []):
            matches = _resolve_link(record, link, indexes)
            if not matches:
                broken_links.append(
                    {
                        "source_id": source_key[0],
                        "path": source_key[1],
                        "target": str(link["target"]),
                    }
                )
            elif len(matches) > 1:
                ambiguous_links.append(
                    {
                        "source_id": source_key[0],
                        "path": source_key[1],
                        "target": str(link["target"]),
                        "matches": [match[1] for match in matches],
                    }
                )
            else:
                target = matches[0]
                edges.append(
                    {
                        "source_id": source_key[0],
                        "from": source_key[1],
                        "to": target[1],
                    }
                )
                connected.add(source_key)
                connected.add(target)

    titles: dict[str, list[dict[str, str]]] = {}
    for record in markdown_records:
        title = str(record.get("title", "")).strip()
        if title:
            titles.setdefault(title.casefold(), []).append(
                {"source_id": str(record["source_id"]), "path": str(record["path"]), "title": title}
            )
    duplicate_titles = [values for values in titles.values() if len(values) > 1]
    orphan_notes = [
        {"source_id": str(record["source_id"]), "path": str(record["path"])}
        for record in markdown_records
        if (str(record["source_id"]), str(record["path"])) not in connected
    ]
    missing_sensitivity = [
        {"source_id": str(record["source_id"]), "path": str(record["path"])}
        for record in markdown_records
        if not record.get("sensitivity")
    ]
    missing_sensitivity_total = sum(1 for record in all_markdown_records if not record.get("sensitivity"))
    missing_authority = [
        {"source_id": str(record["source_id"]), "path": str(record["path"])}
        for record in markdown_records
        if not record.get("properties", {}).get("authority")
    ]
    invalid_progress = [
        {"source_id": str(record["source_id"]), "path": str(record["path"])}
        for record in markdown_records
        if str(record.get("properties", {}).get("type", "")).lower() == "project"
        and record.get("progress", {}).get("status") != "known"
    ]
    parse_skipped = [
        {"source_id": str(record["source_id"]), "path": str(record["path"])}
        for record in markdown_records
        if record.get("parse_skipped")
    ]
    result = {
        "summary": {
            "files_total": len(records),
            "markdown_total": len(all_markdown_records),
            "sensitive_total": sum(1 for record in records if record.get("sensitive")),
            "details_redacted_sensitive": len(all_markdown_records) - len(markdown_records),
            "missing_sensitivity_total": missing_sensitivity_total,
            "edges_total": len(edges),
            "issues_total": (
                len(broken_links)
                + len(ambiguous_links)
                + len(duplicate_titles)
                + missing_sensitivity_total
                + len(missing_authority)
                + len(invalid_progress)
                + len(parse_skipped)
            ),
        },
        "broken_links": broken_links,
        "ambiguous_links": ambiguous_links,
        "duplicate_titles": duplicate_titles,
        "orphan_notes": orphan_notes,
        "missing_sensitivity": missing_sensitivity,
        "missing_authority": missing_authority,
        "invalid_progress": invalid_progress,
        "parse_skipped": parse_skipped,
        "edges": edges,
        "non_destructive": True,
    }
    return result


def markdown_report(result: dict[str, Any]) -> str:
    summary = result["summary"]
    lines = [
        "# Knowledge Quality Report",
        "",
        "> This report is derived from local metadata and links. It does not delete, merge, rename, or rewrite source views.",
        "",
        f"- Files: {summary['files_total']}",
        f"- Markdown notes: {summary['markdown_total']}",
        f"- Sensitive or unknown-sensitivity records: {summary['sensitive_total']}",
        f"- Resolved link edges: {summary['edges_total']}",
        f"- Validation issues: {summary['issues_total']}",
        "",
    ]
    sections = (
        ("Broken links", result["broken_links"]),
        ("Ambiguous links", result["ambiguous_links"]),
        ("Duplicate titles", result["duplicate_titles"]),
        ("Orphan notes", result["orphan_notes"]),
        ("Missing sensitivity", result["missing_sensitivity"]),
        ("Missing authority", result["missing_authority"]),
        ("Unknown project progress", result["invalid_progress"]),
        ("Parse skipped", result["parse_skipped"]),
    )
    for title, items in sections:
        lines.extend([f"## {title}", ""])
        if not items:
            lines.append("- None")
        else:
            for item in items:
                lines.append(f"- `{str(item)[:500]}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
