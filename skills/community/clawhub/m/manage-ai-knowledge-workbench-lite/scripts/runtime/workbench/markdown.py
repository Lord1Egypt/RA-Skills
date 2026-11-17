"""Small, dependency-free Markdown metadata parser."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse


WIKILINK_RE = re.compile(r"!?\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
INLINE_TAG_RE = re.compile(r"(?<![\w/])#([\w\-\u4e00-\u9fff/]+)")
MILESTONE_RE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s+complete", re.IGNORECASE)
ALLOWED_SENSITIVITY = {"public", "internal", "confidential", "restricted", "private"}


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inside = value[1:-1].strip()
        if not inside:
            return []
        return [part.strip().strip("'\"") for part in inside.split(",") if part.strip()]
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value.strip("'\"")


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, Any], int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0
    properties: dict[str, Any] = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        if line.strip() == "---":
            return properties, index + 1
        if line and not line.startswith((" ", "\t")) and ":" in line:
            key, raw = line.split(":", 1)
            key = key.strip()
            raw = raw.strip()
            if raw:
                properties[key] = _parse_scalar(raw)
            else:
                values: list[str] = []
                cursor = index + 1
                while cursor < len(lines):
                    match = re.match(r"^\s+-\s+(.+?)\s*$", lines[cursor])
                    if not match:
                        break
                    values.append(match.group(1).strip("'\""))
                    cursor += 1
                properties[key] = values
                index = cursor - 1
        index += 1
    return properties, 0


def _as_tags(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [part.strip() for part in str(value).split(",") if part.strip()]


def _clean_link(raw: str, kind: str) -> str | None:
    value = raw.strip().strip("<>")
    if kind == "wikilink":
        value = value.split("|", 1)[0]
    value = value.split("#", 1)[0].strip()
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.scheme or value.startswith(("//", "mailto:")):
        return None
    return value.replace("\\", "/")[:500]


def _progress(properties: dict[str, Any]) -> dict[str, Any] | None:
    if str(properties.get("type", "")).lower() != "project":
        return None
    raw_value = properties.get("overall_progress_pct", properties.get("progress_pct"))
    basis = str(properties.get("overall_progress_basis", properties.get("progress_basis", ""))).strip()
    confidence = str(
        properties.get("overall_progress_confidence", properties.get("progress_confidence", ""))
    ).strip()
    milestone = str(properties.get("milestone_progress", "")).strip()
    match = MILESTONE_RE.match(milestone)
    denominator_ok = bool(match and int(match.group(2)) > 0 and int(match.group(1)) <= int(match.group(2)))
    numeric = isinstance(raw_value, (int, float)) and not isinstance(raw_value, bool)
    valid = bool(numeric and 0 <= float(raw_value) <= 100 and basis and denominator_ok)
    return {
        "value": float(raw_value) if valid else None,
        "status": "known" if valid else "unknown",
        "basis": basis if valid else "",
        "confidence": confidence if valid else "low",
        "milestone_progress": milestone if valid else "unknown",
    }


def parse_markdown(path: Path, content_access: str = "local-parse") -> dict[str, Any]:
    if content_access == "filesystem-metadata":
        return {
            "title": path.stem,
            "properties": {},
            "tags": [],
            "links": [],
            "progress": None,
        }

    # Windows PowerShell 5.1 commonly writes UTF-8 with a BOM. ``utf-8-sig``
    # accepts both BOM and non-BOM UTF-8 so frontmatter remains detectable.
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = text.splitlines()
    properties, body_start = parse_frontmatter(lines)
    parse_body = content_access == "local-parse"
    title = str(properties.get("title", "")).strip()
    if not title and parse_body:
        for line in lines[body_start:]:
            if line.startswith("# "):
                title = line[2:].strip()
                break
    title = title or path.stem
    tags = set(_as_tags(properties.get("tags")))
    links: list[dict[str, str]] = []
    if parse_body:
        body = "\n".join(lines[body_start:])
        tags.update(INLINE_TAG_RE.findall(body))
        for raw in WIKILINK_RE.findall(body):
            target = _clean_link(raw, "wikilink")
            if target:
                links.append({"kind": "wikilink", "target": target})
        for raw in MARKDOWN_LINK_RE.findall(body):
            target = _clean_link(raw, "markdown")
            if target:
                links.append({"kind": "markdown", "target": target})

    sensitivity = str(properties.get("sensitivity", "")).strip().lower()
    if sensitivity not in ALLOWED_SENSITIVITY:
        sensitivity = ""
    safe_properties = {
        key: properties.get(key)
        for key in (
            "type",
            "status",
            "authority",
            "canonical",
            "sensitivity",
            "source_updated",
            "reviewed_at",
        )
        if key in properties
    }
    safe_properties["sensitivity"] = sensitivity
    return {
        "title": title[:300],
        "properties": safe_properties,
        "tags": sorted(tag[:100] for tag in tags if tag),
        "links": links,
        "progress": _progress(properties),
    }
