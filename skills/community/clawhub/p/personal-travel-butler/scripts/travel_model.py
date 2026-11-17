#!/usr/bin/env python3
"""Shared local Markdown travel entry parsing and rendering helpers."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Iterable


ENTRY_DIRS = {
    "places": "place",
    "guides": "guide",
    "trips": "trip",
    "preferences": "preference",
}
TYPE_DIRS = {value: key for key, value in ENTRY_DIRS.items()}
VALID_TYPES = set(TYPE_DIRS)
VALID_STATUS = {"inbox", "active", "planned", "visited", "archived", "needs-review"}
PLACEHOLDER_PROFILE_ID = "preference-20260614-profile"


def today_iso() -> str:
    return date.today().isoformat()


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"", "null", "~"}:
        return None
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_frontmatter_text(text: str) -> tuple[dict[str, Any], str, list[str]]:
    if not text.startswith("---\n"):
        return {}, text, ["missing YAML frontmatter"]
    match = re.match(r"^---\n(.*?)\n---\n?(.*)", text, re.DOTALL)
    if not match:
        return {}, text, ["unterminated YAML frontmatter"]

    data: dict[str, Any] = {}
    errors: list[str] = []
    current_key: str | None = None
    current_item: dict[str, Any] | None = None

    for line_number, line in enumerate(match.group(1).splitlines(), start=2):
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            item_text = line[4:].strip()
            if ":" in item_text:
                key, value = item_text.split(":", 1)
                current_item = {key.strip(): parse_scalar(value)}
                data[current_key].append(current_item)
            else:
                current_item = None
                data[current_key].append(parse_scalar(item_text))
            continue
        if line.startswith("    ") and current_key and current_item is not None and ":" in line:
            key, value = line.strip().split(":", 1)
            current_item[key.strip()] = parse_scalar(value)
            continue
        if line.startswith("  ") and current_key and ":" in line:
            if data.get(current_key) == []:
                data[current_key] = {}
            if isinstance(data.get(current_key), dict):
                key, value = line.strip().split(":", 1)
                data[current_key][key.strip()] = parse_scalar(value)
            continue
        if line.startswith("  "):
            errors.append(f"line {line_number}: cannot parse nested frontmatter line")
            continue
        if ":" not in line:
            errors.append(f"line {line_number}: cannot parse frontmatter line")
            continue

        key, raw_value = line.split(":", 1)
        current_key = key.strip()
        current_item = None
        value = raw_value.strip()
        data[current_key] = [] if value == "" else parse_scalar(value)

    return data, match.group(2), errors


def parse_frontmatter_file(path: Path) -> tuple[dict[str, Any], str, list[str]]:
    return parse_frontmatter_text(path.read_text(encoding="utf-8"))


def normalize_city_name(value: Any) -> str | None:
    if value is None:
        return None
    city = str(value).strip().strip('"').strip("'")
    if not city or city.lower() in {"null", "none"}:
        return None
    city = re.sub(r"\s+", "", city)
    if city.endswith("市") and len(city) > 1:
        city = city[:-1]
    return city


def city_validation_errors(city: Any, context: str) -> list[str]:
    normalized = normalize_city_name(city)
    if not normalized:
        return []
    errors: list[str] = []
    if any(sep in normalized for sep in ("/", "\\", ",", "，", "、", "|")):
        errors.append(f"{context}: city should contain one city only, got `{city}`")
    if any(marker in normalized for marker in ("省", "区", "县", "镇", "街道", "路", "号")):
        errors.append(f"{context}: city should not include province, district, street, or address detail: `{city}`")
    if "海口文昌" in normalized:
        errors.append(f"{context}: city looks ambiguous; use `文昌` or `海口`, not `{city}`")
    return errors


def require_valid_city(city: Any) -> str | None:
    errors = city_validation_errors(city, "city")
    if errors:
        raise ValueError(errors[0].split(": ", 1)[1])
    return normalize_city_name(city)


def parse_coordinates(value: str | None) -> dict[str, float] | None:
    if not value:
        return None
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 2:
        raise ValueError("coordinates must use LAT,LNG")
    try:
        lat = float(parts[0])
        lng = float(parts[1])
    except ValueError as exc:
        raise ValueError("coordinates must be numeric LAT,LNG") from exc
    validate_coordinates({"lat": lat, "lng": lng}, "coordinates")
    return {"lat": lat, "lng": lng}


def validate_coordinates(value: Any, context: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict):
        return [f"{context}: coordinates must be null or a mapping with lat and lng"]
    errors: list[str] = []
    lat = value.get("lat")
    lng = value.get("lng")
    if not isinstance(lat, (int, float)) or not -90 <= float(lat) <= 90:
        errors.append(f"{context}: coordinates.lat must be between -90 and 90")
    if not isinstance(lng, (int, float)) or not -180 <= float(lng) <= 180:
        errors.append(f"{context}: coordinates.lng must be between -180 and 180")
    return errors


def clean_list(value: Any) -> list[Any]:
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    cleaned = []
    for item in values:
        if isinstance(item, str):
            item = item.strip()
        if item not in (None, "", "-"):
            cleaned.append(item)
    return cleaned


def dedupe_text_list(values: list[Any]) -> list[Any]:
    seen: set[str] = set()
    result: list[Any] = []
    for value in values:
        key = str(value).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def section(body: str, title: str) -> str:
    pattern = rf"^##\s+{re.escape(title)}\s*\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, body, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


def bullet_summary(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("- "):
            continue
        item = line[2:].strip()
        if item and item != "-":
            lines.append(item)
    return "\n".join(lines)


def sections_as_notes(body: str, names: list[str]) -> str:
    chunks = [section(body, name) for name in names]
    return "\n\n".join(chunk for chunk in chunks if chunk and chunk != "-")


def summary_from_body(record_type: str, body: str) -> str:
    if record_type == "place":
        return bullet_summary(section(body, "Snapshot"))
    if record_type == "guide":
        return section(body, "Summary")
    if record_type == "trip":
        return section(body, "Intent")
    if record_type == "preference":
        return section(body, "Preference")
    return ""


def notes_from_body(record_type: str, body: str) -> str:
    if record_type == "place":
        return section(body, "Notes")
    if record_type == "guide":
        return sections_as_notes(body, ["Extracted Items", "Useful For"])
    if record_type == "trip":
        return sections_as_notes(body, ["Constraints", "Draft Plan", "Candidates"])
    if record_type == "preference":
        return section(body, "Applies To")
    return ""


def evidence_from_body(body: str) -> list[str]:
    evidence = []
    for raw in section(body, "Evidence").splitlines():
        line = raw.strip()
        if line.startswith("- "):
            item = line[2:].strip()
            if item and item != "-":
                evidence.append(item)
    return evidence


def normalize_compact_record(row: dict[str, Any], make_id=None) -> dict[str, Any]:
    normalized = dict(row)
    if make_id and not normalized.get("id"):
        normalized["id"] = make_id(
            str(normalized.get("type") or "place"),
            str(normalized.get("name") or "Untitled"),
            normalized.get("city"),
        )
    normalized.setdefault("notion_page_id", None)
    normalized.setdefault("type", "place")
    normalized.setdefault("status", "active")
    normalized.setdefault("record_weight", "light")
    normalized.setdefault("name", "Untitled")
    normalized.setdefault("city", None)
    normalized.setdefault("tags", [])
    normalized.setdefault("priority", 3)
    normalized.setdefault("summary", "")
    normalized.setdefault("notes", "")
    normalized.setdefault("detail_file", None)
    normalized.setdefault("source", [])
    normalized.setdefault("evidence", [])
    normalized.setdefault("address", None)
    normalized.setdefault("province", None)
    normalized.setdefault("phone", None)
    normalized.setdefault("website", None)
    normalized.setdefault("updated_at", today_iso())
    normalized.setdefault("last_synced_at", None)

    normalized["city"] = normalize_city_name(normalized.get("city"))
    for field in ("tags", "source", "evidence"):
        normalized[field] = clean_list(normalized.get(field))
    normalized["tags"] = dedupe_text_list(normalized["tags"])
    try:
        normalized["priority"] = int(normalized["priority"])
    except (TypeError, ValueError):
        normalized["priority"] = 3
    return normalized


def markdown_record_from_file(path: Path, expected_type: str) -> dict[str, Any] | None:
    frontmatter, body, errors = parse_frontmatter_file(path)
    if errors:
        return None
    record_type = str(frontmatter.get("type") or expected_type)
    if record_type != expected_type:
        return None
    evidence = clean_list(frontmatter.get("evidence")) or evidence_from_body(body)
    record = {
        "id": frontmatter.get("id"),
        "type": record_type,
        "status": frontmatter.get("status") or "active",
        "record_weight": "standard",
        "name": frontmatter.get("name") or path.stem,
        "city": frontmatter.get("city"),
        "tags": clean_list(frontmatter.get("tags")),
        "priority": int(frontmatter.get("priority") or 3),
        "summary": summary_from_body(record_type, body),
        "notes": notes_from_body(record_type, body),
        "detail_file": None,
        "source": clean_list(frontmatter.get("source")),
        "evidence": evidence,
        "address": frontmatter.get("address"),
        "province": frontmatter.get("province"),
        "phone": frontmatter.get("phone"),
        "website": frontmatter.get("website"),
        "updated_at": frontmatter.get("updated_at") or frontmatter.get("last_verified"),
        "last_synced_at": None,
    }
    if not record["id"]:
        return None
    return normalize_compact_record(record)


def is_placeholder_record(record: dict[str, Any]) -> bool:
    if record.get("id") == PLACEHOLDER_PROFILE_ID:
        summary = str(record.get("summary") or "")
        return "Use this file for durable travel preferences" in summary and not clean_list(record.get("evidence")) and not clean_list(record.get("source"))
    return False


def markdown_records(db: Path, include_placeholders: bool = False) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for dirname, expected_type in ENTRY_DIRS.items():
        folder = db / dirname
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            record = markdown_record_from_file(path, expected_type)
            if record and (include_placeholders or not is_placeholder_record(record)):
                records.append(record)
    return records


def slugify(value: str | None) -> str:
    normalized = (value or "").strip().lower()
    normalized = re.sub(r"[\s_]+", "-", normalized)
    normalized = re.sub(r"[^a-z0-9\-\u4e00-\u9fff]+", "", normalized)
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return normalized or "untitled"


def entry_id(entry_type: str, name: str, city: str | None, day: str) -> str:
    digest = hashlib.sha1(f"{entry_type}|{name}|{city or ''}|{day}".encode("utf-8")).hexdigest()[:8]
    return f"{entry_type}-{day.replace('-', '')}-{digest}"


def yaml_scalar(value: Any) -> str:
    if value is None or value == "":
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(values: Iterable[Any]) -> str:
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if not cleaned:
        return "[]"
    return "[" + ", ".join(yaml_scalar(value) for value in cleaned) + "]"


def yaml_coordinates(value: dict[str, float] | None) -> str:
    if not value:
        return "null"
    return f"\n  lat: {value['lat']}\n  lng: {value['lng']}"


def source_label(source: Any) -> str:
    if isinstance(source, dict):
        return str(source.get("title") or source.get("source") or source.get("url") or json.dumps(source, ensure_ascii=False, sort_keys=True))
    return str(source)


def render_generated_index(kind: str, records: list[dict[str, Any]]) -> str:
    today = today_iso()
    title = {"cities": "Cities Index", "tags": "Tags Index", "sources": "Sources Index"}[kind]
    header = f"""---
id: index-{kind}
type: index
status: active
name: {title}
city: null
coordinates: null
tags: [index]
source: []
evidence: []
priority: 3
last_verified: null
created_at: 2026-06-14
updated_at: {today}
---

# {title}

This is a derived view. Regenerate from atomic entries when stale.
"""
    groups: dict[str, list[dict[str, Any]]] = {}
    if kind == "cities":
        for record in records:
            groups.setdefault(str(record.get("city") or "Unknown"), []).append(record)
        section_title = "Cities"
    elif kind == "tags":
        for record in records:
            for tag in record.get("tags") or []:
                groups.setdefault(str(tag), []).append(record)
        section_title = "Tags"
    else:
        for record in records:
            for source in record.get("source") or []:
                groups.setdefault(source_label(source), []).append(record)
        section_title = "Sources"

    lines = [header.rstrip(), "", f"## {section_title}", ""]
    if not groups:
        lines.append("- No entries yet.")
    for name in sorted(groups):
        lines.extend(["", f"### {name}"])
        for record in sorted(groups[name], key=lambda item: (item.get("city") or "", item.get("name") or "")):
            city = record.get("city") or "Unknown"
            lines.append(f"- {record.get('name')} ({record.get('type')}, P{record.get('priority')}, {city})")
    return "\n".join(lines).rstrip() + "\n"


def save_generated_indexes(db: Path, records: list[dict[str, Any]] | None = None) -> None:
    records = records or markdown_records(db)
    index_dir = db / "indexes"
    index_dir.mkdir(parents=True, exist_ok=True)
    for kind in ("cities", "tags", "sources"):
        (index_dir / f"{kind}.md").write_text(render_generated_index(kind, records), encoding="utf-8")


def record_matches_filters(record: dict[str, Any], city: str | None = None, tags: list[str] | None = None) -> bool:
    if city and normalize_city_name(record.get("city")) != normalize_city_name(city):
        return False
    wanted_tags = {tag for tag in (tags or []) if tag}
    if wanted_tags and not wanted_tags.intersection({str(tag) for tag in record.get("tags") or []}):
        return False
    return True


def filter_records(records: list[dict[str, Any]], city: str | None = None, tags: list[str] | None = None) -> list[dict[str, Any]]:
    return [record for record in records if record_matches_filters(record, city, tags)]
