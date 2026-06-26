"""Normalize raw evidence into a stable internal shape."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from intelligence_desk_brief.contracts import CreateBriefRequest


def _parse_timestamp(raw_value: Any) -> tuple[str | None, str]:
    if not isinstance(raw_value, str) or not raw_value.strip():
        return None, "Unknown recency"
    raw_text = raw_value.strip()
    normalized = raw_text.replace("Z", "+00:00")
    try:
        timestamp = datetime.fromisoformat(normalized)
    except ValueError:
        for fmt in ("%a %b %d %H:%M:%S %z %Y", "%b %d, %Y"):
            try:
                timestamp = datetime.strptime(raw_text, fmt)
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=timezone.utc)
                return timestamp.isoformat(), timestamp.date().isoformat()
            except ValueError:
                continue
        return raw_value, "Retrieved during current run"
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.isoformat(), timestamp.date().isoformat()


def _confidence_value(label: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(label, 1)


def _signal_value(label: str) -> int:
    return {"high": 3, "medium": 2, "low": 1}.get(label, 1)


def normalize_evidence(
    raw_items: list[dict[str, Any]],
    request: CreateBriefRequest,
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for item in raw_items:
        affected_names = item.get("affected_names", [])
        if isinstance(affected_names, str):
            affected_names = [affected_names]
        source_title = item.get("source_title") or item.get("title") or "Untitled source"
        url = item.get("url") or ""
        published_at, recency_note = _parse_timestamp(
            item.get("published_at") or item.get("timestamp") or item.get("date")
        )
        source_type = item.get("source_type") or item.get("category") or "unknown"
        retrieval_status = item.get("retrieval_status") or "success"
        confidence_level = item.get("confidence_level") or "low"
        signal_strength = item.get("signal_strength") or "low"
        item_type = item.get("item_type", "evidence")

        holdings_set = set(request.holdings)
        watchlist_set = set(request.watchlist)
        themes_lower = {theme.lower() for theme in request.themes}
        affected_set = {name.upper() for name in affected_names}
        text_for_match = " ".join(
            str(part)
            for part in [
                item.get("factor"),
                item.get("fact"),
                item.get("interpretation"),
                item.get("why_it_matters"),
                source_title,
            ]
            if part
        ).lower()

        direct_relevance = len({name.upper() for name in holdings_set} & affected_set)
        watchlist_relevance = len({name.upper() for name in watchlist_set} & affected_set)
        adjacent_relevance = sum(1 for theme in themes_lower if theme in text_for_match)
        low_quality = retrieval_status != "success" or item_type == "retrieval_notice"

        normalized.append(
            {
                "id": item["id"],
                "item_type": item_type,
                "category": item.get("category", "unknown"),
                "signal_strength": signal_strength,
                "signal_value": _signal_value(signal_strength),
                "factor": item.get("factor") or "Unmapped factor",
                "affected_names": list(affected_names),
                "fact": item.get("fact") or "No direct fact extracted.",
                "interpretation": item.get("interpretation") or "No interpretation available.",
                "change_label": item.get("change_label") or "unchanged",
                "why_it_matters": item.get("why_it_matters") or item.get("interpretation") or "Pending analysis.",
                "watchpoint": item.get("watchpoint") or "Re-check on next run.",
                "confidence_level": confidence_level,
                "confidence_value": _confidence_value(confidence_level),
                "provider": item.get("provider") or "fixture",
                "source_type": source_type,
                "published_at": published_at,
                "retrieval_status": retrieval_status,
                "direct_relevance": direct_relevance,
                "watchlist_relevance": watchlist_relevance,
                "adjacent_relevance": adjacent_relevance,
                "cross_name_impact": len(affected_names),
                "is_x_signal": source_type.startswith("x") or source_type == "x_signals",
                "low_quality": low_quality,
                "raw_reference": item.get("raw_reference", item),
                "source": {
                    "title": source_title,
                    "url": url,
                    "timestamp": published_at,
                    "recency_note": item.get("recency_note") or recency_note,
                    "type": source_type,
                    "provider": item.get("provider") or "fixture",
                },
            }
        )
    return normalized
