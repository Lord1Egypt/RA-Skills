#!/usr/bin/env python3
"""Shared helpers for the personal travel Notion sync scripts."""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from travel_model import city_validation_errors, normalize_compact_record


DEFAULT_NOTION_VERSION = "2026-03-11"
NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_SYNC_DIR = "notion-sync"
FIXED_NOTION_FILES = (
    "_README.md",
    "_config.example.json",
    "_schema.md",
    "_records.jsonl",
    "_index.md",
    "_ledger.jsonl",
    "_conflicts.md",
    "_sync_log.jsonl",
)
RECORD_TYPES = {"place", "guide", "trip", "preference"}
RECORD_STATUS = {"inbox", "active", "planned", "visited", "archived", "needs-review"}
RECORD_WEIGHTS = {"light", "standard", "detailed"}
REQUIRED_RECORD_FIELDS = (
    "id",
    "type",
    "status",
    "record_weight",
    "name",
    "city",
    "tags",
    "priority",
    "summary",
    "notes",
    "detail_file",
    "source",
    "evidence",
    "updated_at",
)
REQUIRED_NOTION_PROPERTIES = {
    "Name": "title",
    "Travel ID": "rich_text",
    "Type": "select",
    "Status": "select",
    "Record Weight": "select",
    "City": "rich_text",
    "Tags": "multi_select",
    "Priority": "number",
    "Summary": "rich_text",
    "Detail File": "rich_text",
    "Updated At": "date",
}
OPTIONAL_NOTION_PROPERTIES = {
    "Notes": "rich_text",
    "Evidence": "rich_text",
    "Source": "rich_text",
    "Address": "rich_text",
    "Province": "rich_text",
    "Sync Hash": "rich_text",
    "Phone": "rich_text",
    "Website": "url",
}
OPTIONAL_PROPERTY_CREATE_SCHEMA = {
    "Notes": {"rich_text": {}},
    "Evidence": {"rich_text": {}},
    "Source": {"rich_text": {}},
    "Address": {"rich_text": {}},
    "Province": {"rich_text": {}},
    "Sync Hash": {"rich_text": {}},
    "Phone": {"rich_text": {}},
    "Website": {"url": {}},
}
MAX_NOTION_TAGS = 20

PROPERTY_CREATE_SCHEMA = {
    "Name": {"title": {}},
    "Travel ID": {"rich_text": {}},
    "Type": {"select": {"options": [{"name": item} for item in sorted(RECORD_TYPES)]}},
    "Status": {"select": {"options": [{"name": item} for item in sorted(RECORD_STATUS)]}},
    "Record Weight": {"select": {"options": [{"name": item} for item in ("light", "standard", "detailed")]}},
    "City": {"rich_text": {}},
    "Tags": {"multi_select": {}},
    "Priority": {"number": {"format": "number"}},
    "Summary": {"rich_text": {}},
    "Detail File": {"rich_text": {}},
    "Updated At": {"date": {}},
    **OPTIONAL_PROPERTY_CREATE_SCHEMA,
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def default_db_path() -> Path:
    return project_root() / "travel-db"


def load_local_env() -> None:
    """Load simple KEY=VALUE lines from the project .env without overriding real env vars."""
    env_path = project_root() / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def save_local_env_value(key: str, value: str) -> None:
    """Set one value in project .env without printing or touching other secrets."""
    env_path = project_root() / ".env"
    lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    updated = False
    new_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            existing_key, _ = stripped.split("=", 1)
            if existing_key.strip() == key:
                new_lines.append(f"{key}={value}")
                updated = True
                continue
        new_lines.append(line)
    if not updated:
        new_lines.append(f"{key}={value}")
    env_path.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8")
    os.environ[key] = value


def resolve_db(path: str | None) -> Path:
    return Path(path).expanduser().resolve() if path else default_db_path().resolve()


def notion_dir(db: Path) -> Path:
    return db / NOTION_SYNC_DIR


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_iso() -> str:
    return date.today().isoformat()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: line {line_number}: invalid JSON: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}: line {line_number}: expected a JSON object")
        rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def load_records(sync_dir: Path) -> list[dict[str, Any]]:
    return [normalize_record(row) for row in read_jsonl(sync_dir / "_records.jsonl")]


def save_records(sync_dir: Path, records: list[dict[str, Any]]) -> None:
    records = sorted((normalize_record(row) for row in records), key=lambda row: (row["city"] or "", row["type"], row["name"]))
    write_jsonl(sync_dir / "_records.jsonl", records)
    (sync_dir / "_index.md").write_text(render_index(records), encoding="utf-8")


def load_ledger(sync_dir: Path) -> dict[str, dict[str, Any]]:
    return {str(row.get("id")): row for row in read_jsonl(sync_dir / "_ledger.jsonl") if row.get("id")}


def save_ledger(sync_dir: Path, ledger: dict[str, dict[str, Any]]) -> None:
    rows = [ledger[key] for key in sorted(ledger)]
    write_jsonl(sync_dir / "_ledger.jsonl", rows)


def append_sync_log(sync_dir: Path, entry: dict[str, Any]) -> None:
    entry = {"timestamp": now_iso(), **entry}
    path = sync_dir / "_sync_log.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def normalize_record(row: dict[str, Any]) -> dict[str, Any]:
    return normalize_compact_record(row, make_id=make_record_id)


def validate_records(records: list[dict[str, Any]], sync_dir: Path) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        for field in REQUIRED_RECORD_FIELDS:
            if field not in record:
                errors.append(f"_records.jsonl line {index}: missing `{field}`")
        record_id = str(record.get("id") or "")
        if not record_id:
            errors.append(f"_records.jsonl line {index}: empty `id`")
        elif record_id in seen:
            errors.append(f"_records.jsonl line {index}: duplicate id `{record_id}`")
        seen.add(record_id)

        if record.get("type") not in RECORD_TYPES:
            errors.append(f"_records.jsonl line {index}: invalid type `{record.get('type')}`")
        if record.get("status") not in RECORD_STATUS:
            errors.append(f"_records.jsonl line {index}: invalid status `{record.get('status')}`")
        if record.get("record_weight") not in RECORD_WEIGHTS:
            errors.append(f"_records.jsonl line {index}: invalid record_weight `{record.get('record_weight')}`")
        if not isinstance(record.get("tags"), list):
            errors.append(f"_records.jsonl line {index}: `tags` must be a list")
        errors.extend(city_validation_errors(record.get("city"), f"_records.jsonl line {index}"))
        if not 1 <= int(record.get("priority") or 0) <= 5:
            errors.append(f"_records.jsonl line {index}: `priority` must be 1-5")
        detail_file = record.get("detail_file")
        if record.get("record_weight") == "detailed" and not detail_file:
            errors.append(f"_records.jsonl line {index}: detailed record missing `detail_file`")
        if detail_file:
            detail_path = sync_dir / str(detail_file)
            if "/" in str(detail_file) or "\\" in str(detail_file):
                errors.append(f"_records.jsonl line {index}: detail_file must stay in notion-sync folder")
            elif not detail_path.exists():
                errors.append(f"_records.jsonl line {index}: detail file `{detail_file}` does not exist")
    return errors


def slugify(value: str | None) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"[^a-z0-9-]+", "", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "record"


def make_record_id(record_type: str, name: str, city: str | None = None, day: str | None = None) -> str:
    day = day or today_iso()
    digest = hashlib.sha1(f"{record_type}|{name}|{city or ''}|{day}".encode("utf-8")).hexdigest()[:8]
    return f"{record_type}-{day.replace('-', '')}-{digest}"


def detail_filename(record: dict[str, Any]) -> str:
    day = str(record.get("updated_at") or today_iso()).replace("-", "")[:8]
    city = slugify(record.get("city"))
    name = slugify(record.get("name"))
    suffix = hashlib.sha1(str(record.get("id")).encode("utf-8")).hexdigest()[:6]
    return f"{record.get('type', 'record')}-{day}-{city}-{name}-{suffix}.md"


def should_be_detailed(record: dict[str, Any]) -> bool:
    notes = str(record.get("notes") or "")
    evidence = record.get("evidence") if isinstance(record.get("evidence"), list) else []
    if record.get("type") == "trip":
        return True
    if len(notes) > 800:
        return True
    if len(evidence) > 3:
        return True
    if any(str(item).lower().startswith(("asset:", "ocr:", "image:")) for item in evidence):
        return True
    return False


def content_hash(record: dict[str, Any], detail_text: str = "") -> str:
    cleaned = dict(normalize_record(record))
    for volatile in ("notion_page_id", "last_synced_at"):
        cleaned.pop(volatile, None)
    payload = {"record": cleaned, "detail_text": detail_text}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def content_hash_with_detail(sync_dir: Path, record: dict[str, Any]) -> str:
    detail_text = ""
    detail_file = record.get("detail_file")
    if detail_file and "/" not in str(detail_file) and "\\" not in str(detail_file):
        detail_path = sync_dir / str(detail_file)
        if detail_path.exists():
            detail_text = detail_path.read_text(encoding="utf-8")
    return content_hash(record, detail_text)


def render_index(records: list[dict[str, Any]]) -> str:
    if not records:
        return "# Notion Sync Index\n\nDerived from `_records.jsonl`.\n\n## By City\n\n- No records yet.\n\n## By Type\n\n- No records yet.\n\n## High Priority\n\n- No records yet.\n"

    def line(record: dict[str, Any]) -> str:
        title = str(record.get("name") or "Untitled")
        detail_file = record.get("detail_file")
        display = f"[{title}]({detail_file})" if detail_file else title
        city = record.get("city") or "Unknown"
        summary = " ".join(str(record.get("summary") or "").split())
        if len(summary) > 180:
            summary = summary[:177].rstrip() + "..."
        tail = f" - {summary}" if summary else ""
        return f"- {display} ({record.get('type')}, {record.get('record_weight')}, P{record.get('priority')}, {city}){tail}"

    sections = ["# Notion Sync Index", "", "Derived from `_records.jsonl`.", "", "## By City"]
    by_city: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_city.setdefault(str(record.get("city") or "Unknown"), []).append(record)
    for city in sorted(by_city):
        sections.extend(["", f"### {city}"])
        sections.extend(line(record) for record in sorted(by_city[city], key=lambda row: row.get("name") or ""))

    sections.extend(["", "## By Type"])
    by_type: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        by_type.setdefault(str(record.get("type") or "place"), []).append(record)
    for record_type in sorted(by_type):
        sections.extend(["", f"### {record_type}"])
        sections.extend(line(record) for record in sorted(by_type[record_type], key=lambda row: row.get("name") or ""))

    sections.extend(["", "## High Priority"])
    high_priority = [record for record in records if int(record.get("priority") or 0) >= 4]
    if high_priority:
        sections.extend(line(record) for record in sorted(high_priority, key=lambda row: (-(row.get("priority") or 0), row.get("name") or "")))
    else:
        sections.append("- No high priority records yet.")
    return "\n".join(sections).rstrip() + "\n"


def render_detail_markdown(record: dict[str, Any]) -> str:
    record = normalize_record(record)
    tags = ", ".join(str(tag) for tag in record["tags"])
    evidence = "\n".join(f"- {format_record_item(item)}" for item in record["evidence"]) or "-"
    source = "\n".join(f"- {format_record_item(item)}" for item in record["source"]) or "-"
    return f"""---
id: {record["id"]}
type: {record["type"]}
status: {record["status"]}
record_weight: detailed
name: "{record["name"]}"
city: "{record["city"] or ""}"
tags: [{tags}]
priority: {record["priority"]}
updated_at: {record["updated_at"]}
---

# {record["name"]}

## Summary

{record["summary"]}

## Notes

{record["notes"]}

## Evidence

{evidence}

## Source

{source}
"""


def append_conflict(sync_dir: Path, conflict: dict[str, Any]) -> None:
    path = sync_dir / "_conflicts.md"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# Notion Sync Conflicts\n"
    if "No unresolved conflicts." in existing:
        existing = existing.replace("No unresolved conflicts.\n", "")
    block = [
        "",
        f"## {conflict.get('id', 'unknown')} - {now_iso()}",
        "",
        f"- Reason: {conflict.get('reason', 'manual review required')}",
        f"- Local changed: {conflict.get('local_changed')}",
        f"- Notion changed: {conflict.get('notion_changed')}",
        f"- Notion page ID: {conflict.get('notion_page_id')}",
        "",
    ]
    path.write_text(existing.rstrip() + "\n" + "\n".join(block), encoding="utf-8")


def notion_env() -> tuple[str | None, str | None, str]:
    load_local_env()
    token = os.environ.get("NOTION_TOKEN")
    data_source_id = os.environ.get("NOTION_TRAVEL_DATA_SOURCE_ID")
    version = os.environ.get("NOTION_VERSION", DEFAULT_NOTION_VERSION)
    return token, data_source_id, version


def normalize_notion_id(value: str | None) -> str:
    if not value:
        return ""
    match = re.search(r"([0-9a-fA-F]{32})", value.replace("-", ""))
    if not match:
        return value.strip()
    raw = match.group(1).lower()
    return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"


def travel_entries_database_payload(parent_page_id: str, title: str = "Travel Entries") -> dict[str, Any]:
    return {
        "parent": {"type": "page_id", "page_id": normalize_notion_id(parent_page_id)},
        "title": [{"type": "text", "text": {"content": title}}],
        "initial_data_source": {
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": PROPERTY_CREATE_SCHEMA,
        },
    }


def notion_request(method: str, path: str, token: str, version: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(
        NOTION_BASE_URL + path,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": version,
            "Content-Type": "application/json",
        },
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            if exc.code in {429, 529} and attempt < 3:
                retry_after = exc.headers.get("Retry-After")
                time.sleep(float(retry_after or 1))
                continue
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Notion API {exc.code}: {details}") from exc
    raise RuntimeError("Notion API request failed after retries")


def check_notion_properties(properties: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for name, expected_type in REQUIRED_NOTION_PROPERTIES.items():
        actual = properties.get(name)
        if actual is None:
            errors.append(f"missing Notion property `{name}`")
            continue
        actual_type = actual.get("type")
        if actual_type != expected_type:
            errors.append(f"Notion property `{name}` should be `{expected_type}`, got `{actual_type}`")
    return errors


def rich_text_value(prop: dict[str, Any] | None) -> str:
    items = (prop or {}).get("rich_text") or []
    return "".join((item.get("plain_text") or "") for item in items)


def title_value(prop: dict[str, Any] | None) -> str:
    items = (prop or {}).get("title") or []
    return "".join((item.get("plain_text") or "") for item in items)


def url_value(prop: dict[str, Any] | None) -> str:
    return str((prop or {}).get("url") or "")


def json_or_lines_value(text: str) -> list[Any]:
    stripped = text.strip()
    if not stripped:
        return []
    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        return [line.strip("- ").strip() for line in stripped.splitlines() if line.strip("- ").strip()]
    return parsed if isinstance(parsed, list) else [parsed]


def format_record_item(item: Any) -> str:
    if isinstance(item, dict):
        parts = []
        for key in ("source", "title", "url", "date", "captured_at", "confidence", "note"):
            value = item.get(key)
            if value is not None and value != "":
                parts.append(f"{key}: {value}")
        if parts:
            return "; ".join(parts)
        return json.dumps(item, ensure_ascii=False, sort_keys=True)
    return str(item)


def json_text(value: Any) -> str:
    return json.dumps(value if value is not None else [], ensure_ascii=False, sort_keys=True)


def notion_record_from_page(page: dict[str, Any]) -> dict[str, Any]:
    props = page.get("properties", {})
    tags_prop = props.get("Tags", {}).get("multi_select") or []
    updated = props.get("Updated At", {}).get("date") or {}
    record = {
        "id": rich_text_value(props.get("Travel ID")) or make_record_id("place", title_value(props.get("Name")) or "Untitled"),
        "notion_page_id": page.get("id"),
        "type": (props.get("Type", {}).get("select") or {}).get("name") or "place",
        "status": (props.get("Status", {}).get("select") or {}).get("name") or "active",
        "record_weight": (props.get("Record Weight", {}).get("select") or {}).get("name") or "light",
        "name": title_value(props.get("Name")) or "Untitled",
        "city": rich_text_value(props.get("City")) or None,
        "tags": [tag.get("name") for tag in tags_prop if tag.get("name")],
        "priority": props.get("Priority", {}).get("number") or 3,
        "summary": rich_text_value(props.get("Summary")),
        "notes": rich_text_value(props.get("Notes")),
        "detail_file": rich_text_value(props.get("Detail File")) or None,
        "source": json_or_lines_value(rich_text_value(props.get("Source"))),
        "evidence": json_or_lines_value(rich_text_value(props.get("Evidence"))),
        "address": rich_text_value(props.get("Address")) or None,
        "province": rich_text_value(props.get("Province")) or None,
        "phone": rich_text_value(props.get("Phone")) or None,
        "website": url_value(props.get("Website")) or None,
        "updated_at": (updated.get("start") if isinstance(updated, dict) else None) or str(page.get("last_edited_time") or today_iso())[:10],
        "last_synced_at": None,
    }
    return normalize_record(record)


def short_text(value: Any, limit: int = 1900) -> str:
    text = "" if value is None else str(value)
    return text[:limit]


def notion_properties_for_record(record: dict[str, Any], available_properties: set[str] | None = None, sync_hash: str | None = None) -> dict[str, Any]:
    record = normalize_record(record)
    tags = [{"name": short_text(tag, 100)} for tag in record["tags"][:MAX_NOTION_TAGS]]
    properties = {
        "Name": {"title": [{"text": {"content": short_text(record["name"])}}]},
        "Travel ID": {"rich_text": [{"text": {"content": short_text(record["id"])}}]},
        "Type": {"select": {"name": record["type"]}},
        "Status": {"select": {"name": record["status"]}},
        "Record Weight": {"select": {"name": record["record_weight"]}},
        "City": {"rich_text": [{"text": {"content": short_text(record["city"] or "")}}]},
        "Tags": {"multi_select": tags},
        "Priority": {"number": record["priority"]},
        "Summary": {"rich_text": [{"text": {"content": short_text(record["summary"])}}]},
        "Detail File": {"rich_text": [{"text": {"content": short_text(record["detail_file"] or "")}}]},
        "Updated At": {"date": {"start": str(record["updated_at"])[:10]}},
    }
    optional_values = {
        "Notes": record.get("notes") or "",
        "Evidence": json_text(record.get("evidence") or []),
        "Source": json_text(record.get("source") or []),
        "Address": record.get("address") or "",
        "Province": record.get("province") or "",
        "Sync Hash": sync_hash or "",
        "Phone": record.get("phone") or "",
    }
    for name, value in optional_values.items():
        if available_properties is None or name in available_properties:
            properties[name] = {"rich_text": [{"text": {"content": short_text(value)}}]}
    if available_properties is None or "Website" in available_properties:
        website = record.get("website") or None
        properties["Website"] = {"url": short_text(website, 2000) if website else None}
    return properties


def notion_sync_hash_from_page(page: dict[str, Any]) -> str:
    return rich_text_value((page.get("properties") or {}).get("Sync Hash"))
