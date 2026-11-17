"""Safe dashboard data projection and static asset rendering."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
import re
from typing import Any

from .builder import atomic_write_text, visible_records
from .config import atomic_write_json, normalized, now_iso
from .dashboard_assets import APP_JS, INDEX_TEMPLATE, STYLES_CSS


def _updated_at(record: dict[str, Any]) -> str:
    nanoseconds = int(record.get("mtime_ns", 0))
    if nanoseconds <= 0:
        return "unknown"
    value = dt.datetime.fromtimestamp(nanoseconds / 1_000_000_000, tz=dt.timezone.utc)
    return value.replace(microsecond=0).isoformat()


def dashboard_data(
    *,
    config: dict[str, Any],
    records: list[dict[str, Any]],
    validation: dict[str, Any],
) -> dict[str, Any]:
    visible = visible_records(records)
    visible_keys = {(str(record["source_id"]), str(record["path"])) for record in visible}
    projected_records = [
        {
            "source_id": str(record["source_id"]),
            "path": str(record["path"]),
            "title": str(record.get("title", record["name"]))[:300],
            "kind": str(record["kind"]),
            "type": str(record.get("properties", {}).get("type", ""))[:80],
            "tags": [str(tag)[:100] for tag in record.get("tags", [])],
            "sensitivity": str(record.get("sensitivity", "unknown")),
            "updated_at": _updated_at(record),
        }
        for record in visible
    ]
    topic_counts: dict[str, int] = {}
    for record in projected_records:
        for tag in record["tags"]:
            topic_counts[tag] = topic_counts.get(tag, 0) + 1
    topics = [
        {"label": label, "count": count}
        for label, count in sorted(topic_counts.items(), key=lambda item: (-item[1], item[0].casefold()))
    ]
    projects = []
    for source, projected in zip(visible, projected_records):
        if str(source.get("properties", {}).get("type", "")).lower() != "project":
            continue
        progress = source.get("progress") or {
            "status": "unknown",
            "value": None,
            "basis": "",
            "confidence": "low",
        }
        projects.append(
            {
                "source_id": projected["source_id"],
                "path": projected["path"],
                "title": projected["title"],
                "progress": progress,
            }
        )
    relations = [
        {
            "source_id": str(edge["source_id"]),
            "from": str(edge["from"]),
            "to": str(edge["to"]),
        }
        for edge in validation["edges"]
        if (str(edge["source_id"]), str(edge["from"])) in visible_keys
        and (str(edge["source_id"]), str(edge["to"])) in visible_keys
    ]
    recent = sorted(projected_records, key=lambda record: record["updated_at"], reverse=True)[:12]
    return {
        "schema_version": 1,
        "generated_at": now_iso(),
        "summary": {
            "files_total": len(records),
            "visible_records": len(projected_records),
            "markdown_total": validation["summary"]["markdown_total"],
            "relations_total": len(relations),
            "issues_total": validation["summary"]["issues_total"],
            "excluded_sensitive": len(records) - len(visible),
        },
        "privacy": {
            "mode": config["privacy_mode"],
            "content_access": config.get("content_access", "unknown"),
            "model_transport": config.get("model_transport", "none"),
            "body_embedded": False,
            "absolute_source_paths_embedded": False,
        },
        "update": {
            "mode": config.get("update", {}).get("mode", "manual"),
            "poll_seconds": config.get("update", {}).get("poll_seconds", 10),
        },
        "records": projected_records,
        "projects": projects,
        "topics": topics,
        "recent_changes": recent,
        "relations": relations,
        "lint": validation["summary"],
        "boundaries": {
            "source_files_read_only": True,
            "derived_view": True,
            "remote_database": False,
            "write_api": False,
        },
    }


def render_dashboard(*, config: dict[str, Any], data: dict[str, Any]) -> list[Path]:
    dashboard = normalized(config["paths"]["dashboard"])
    assets = dashboard / "assets"
    data_path = dashboard / "data.json"
    index_path = dashboard / "index.html"
    css_path = assets / "styles.css"
    js_path = assets / "app.js"
    atomic_write_json(data_path, data)
    embedded = json.dumps(data, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")
    html = INDEX_TEMPLATE.replace("__EMBEDDED_DATA__", embedded)
    atomic_write_text(index_path, html)
    atomic_write_text(css_path, STYLES_CSS)
    atomic_write_text(js_path, APP_JS)
    return [index_path, data_path, css_path, js_path]


def validate_dashboard_files(config: dict[str, Any], files: list[Path]) -> dict[str, Any]:
    source_roots = [str(normalized(source["root"])) for source in config["sources"]]
    texts = {path.name: path.read_text(encoding="utf-8") for path in files}
    json.loads(texts["data.json"])
    combined = "\n".join(texts.values())
    remote_patterns = (
        r'''(?:src|href)=["']https?://''',
        r'''url\(\s*["']?https?://''',
        r'''@import\s+["']https?://''',
        r'''fetch\(\s*["']https?://''',
    )
    remote_markers = [pattern for pattern in remote_patterns if re.search(pattern, combined, re.IGNORECASE)]
    absolute_paths = [root for root in source_roots if root in combined]
    return {
        "files": [str(path) for path in files],
        "remote_markers": remote_markers,
        "absolute_source_paths": absolute_paths,
        "body_embedded": False,
        "passed": not remote_markers and not absolute_paths,
    }
