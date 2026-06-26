"""Archive: partition, merge, distill, and purge low-value rows."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from .core import (
    make_id,
    merge_rows_by_identity,
    normalize_content,
    row_identity_key,
    upsert,
)
from .ingest import is_low_signal_line


def should_archive(item: Dict[str, Any], cold_threshold: float) -> bool:
    event_type = str(item.get("event_type") or "")
    kind = str(item.get("kind") or "")
    if event_type == "decision":
        return False

    priority = float(item.get("priority_score") or 0.0)
    if priority >= 1.0:
        return False

    temperature = float(item.get("temperature") or item.get("weight") or 0.0)
    if temperature <= cold_threshold:
        return True

    age_days = float(item.get("age_days") or 0.0)
    recent_refs = int(item.get("recent_refs") or 0)
    occurrences = int(item.get("occurrences") or 1)

    if kind == "fact" and priority <= 0.0 and recent_refs == 0 and age_days >= 7.0 and occurrences <= 1:
        return True
    if kind == "event" and event_type in {"artifact", "progress"} and priority <= 0.5 and recent_refs == 0 and age_days >= 10.0:
        return True

    return (priority <= 0.0) and (recent_refs == 0) and (age_days >= 14.0) and (occurrences <= 1)


def partition_archive_rows(rows: List[Dict[str, Any]], cold_threshold: float) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    active: List[Dict[str, Any]] = []
    archived: List[Dict[str, Any]] = []
    for r in rows:
        if should_archive(r, cold_threshold):
            archived.append(r)
        else:
            active.append(r)
    return active, archived


def merge_archive_rows(existing: List[Dict[str, Any]], incoming: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = merge_rows_by_identity(existing + incoming)
    by_key: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        key = row_identity_key(row)
        prev = by_key.get(key)
        if not prev:
            by_key[key] = row
            continue
        prev_temp = float(prev.get("temperature") or prev.get("weight") or 0.0)
        row_temp = float(row.get("temperature") or row.get("weight") or 0.0)
        prev_seen = str(prev.get("last_seen_at") or prev.get("updated_at") or "")
        row_seen = str(row.get("last_seen_at") or row.get("updated_at") or "")
        if (row_temp >= prev_temp) or (row_seen > prev_seen):
            by_key[key] = row
    return list(by_key.values())


def distill_archived_rows(rows: List[Dict[str, Any]], label: str, now_iso: str) -> Optional[Dict[str, Any]]:
    if not rows:
        return None

    ranked = sorted(
        rows,
        key=lambda r: (float(r.get("priority_score") or 0.0), float(r.get("temperature") or r.get("weight") or 0.0)),
        reverse=True,
    )

    fragments: List[str] = []
    for row in ranked:
        content = str(row.get("content") or "").strip()
        if not content or is_low_signal_line(content):
            continue
        compact = re.sub(r"\s+", " ", content)
        if len(compact) > 40:
            compact = compact[:40] + "…"
        fragments.append(compact)
        if len(fragments) >= 3:
            break

    if not fragments:
        return None

    content = f"归档回流[{label}]：" + "；".join(fragments)
    return {
        "id": make_id("summary", content),
        "kind": "summary",
        "content": content,
        "confidence": 0.85,
        "importance": 0.8,
        "weight": 0.9,
        "temperature": 0.9,
        "temperature_bucket": "hot",
        "created_at": now_iso,
        "updated_at": now_iso,
        "last_seen_at": now_iso,
        "source": "archive_distill",
        "tags": ["soil", "distill", label],
    }


def purge_low_value_facts(facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove facts that are clearly noise: too short, zero priority with no refs, or fragment-like."""
    import re as _re
    MIN_CONTENT_LEN = 12
    kept: List[Dict[str, Any]] = []
    for f in facts:
        content = str(f.get("content") or "").strip()
        priority = float(f.get("priority_score") or 0.0)
        refs = int(f.get("recent_refs") or 0)
        hits = int(f.get("usage_hits") or 0)
        importance = float(f.get("importance") or 0.0)

        if len(content) < MIN_CONTENT_LEN:
            continue
        if _re.match(r'^[\d]+\.\s', content) and len(content) < 25:
            continue
        if _re.match(r'^[✅❌⚠️🔴🟢🟡•\-\*]\s*\S{0,15}$', content):
            continue
        if _re.match(r'^\*\*\S+:\*\*$', content):
            continue
        if priority <= 0.0 and refs == 0 and hits == 0 and importance <= 0.5 and len(content) < 25:
            continue

        kept.append(f)
    return kept
