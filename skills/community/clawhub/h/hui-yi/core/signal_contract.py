#!/usr/bin/env python3
"""Shared contract helpers for Hui-Yi signal and hook integration."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from datetime import date

TRIGGER_DEFAULTS = {
    "skill_hit": {"min_relevance": 0.30, "min_confidence": "medium", "limit": 3},
    "heuristic_fallback": {"min_relevance": 0.55, "min_confidence": "high", "limit": 2},
    "manual_probe": {"min_relevance": 0.30, "min_confidence": "medium", "limit": 3},
}
CONFIDENCE_ORDER = {"low": 1, "medium": 2, "high": 3}


def build_session_key(channel: str, scope_type: str, scope_id: str, thread_id: str | None = None) -> str:
    tail = f"thread:{thread_id}" if thread_id else "main"
    return f"{channel}:{scope_type}:{scope_id}:{tail}"


def resolve_trigger_defaults(trigger_source: str) -> dict:
    return dict(TRIGGER_DEFAULTS.get(trigger_source, TRIGGER_DEFAULTS["manual_probe"]))


def candidate_payload(note: dict, relevance: float, meta: dict, today: date) -> dict:
    return {
        "title": note.get("title"),
        "path": note.get("path"),
        "relevance": relevance,
        "confidence": meta.get("confidence", "none"),
        "matched_fields": meta.get("matched_fields", []),
        "overlap_terms": meta.get("overlap_terms", []),
        "raw_score": meta.get("raw_score", 0.0),
        "evaluated_at": today.isoformat(),
    }
