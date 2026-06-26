#!/usr/bin/env python3
"""Shared scoring logic for Hui-Yi review, resurfacing, and scheduling."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import math
from datetime import date, timedelta

from core.common import DEFAULT_INTERVAL_DAYS, STRENGTH_RISK_FACTOR, memory_strength, parse_date, repetition_signal
from core.signal_detect import detect_match

IMPORTANCE_WEIGHT = {"high": 3.0, "medium": 2.0, "low": 1.0}


def forgetting_risk(note: dict, today: date) -> tuple[float, int]:
    next_review = parse_date(note.get("next_review"))
    review = note.get("review") if isinstance(note.get("review"), dict) else {}
    interval_days = max(1, int(review.get("interval_days", DEFAULT_INTERVAL_DAYS) or DEFAULT_INTERVAL_DAYS))
    strength = memory_strength(note)
    anchor = (
        parse_date(note.get("last_reviewed"))
        or parse_date(note.get("last_seen"))
        or parse_date(note.get("last_verified"))
    )
    if next_review and anchor is None:
        anchor = next_review - timedelta(days=interval_days)
    if anchor is None:
        return 0.0, 0

    elapsed_days = max(0, (today - anchor).days)
    progress = elapsed_days / max(interval_days, 1)
    risk = 1.0 - math.exp(-1.2 * progress)

    overdue = 0
    if next_review:
        overdue = (today - next_review).days
        if overdue > 0:
            overdue_ratio = min(2.0, overdue / max(interval_days, 1))
            risk = min(1.0, risk + 0.15 + 0.15 * overdue_ratio)

    risk *= STRENGTH_RISK_FACTOR.get(strength, 1.0)
    return max(0.05, min(risk, 1.0)), overdue


def due_pressure(note: dict, today: date) -> tuple[float, int]:
    risk_value, overdue = forgetting_risk(note, today)
    next_review = parse_date(note.get("next_review"))
    review = note.get("review") if isinstance(note.get("review"), dict) else {}
    interval_days = max(1, int(review.get("interval_days", DEFAULT_INTERVAL_DAYS) or DEFAULT_INTERVAL_DAYS))
    if not next_review:
        return risk_value, overdue
    days_until = (next_review - today).days
    if days_until <= 0:
        overdue_ratio = min(1.0, abs(days_until) / max(interval_days, 1))
        return min(1.0, 0.65 + 0.35 * overdue_ratio), overdue
    pre_due_window = max(1, interval_days // 2)
    if days_until <= pre_due_window:
        edge = 1.0 - (days_until / max(pre_due_window, 1))
        return max(risk_value, 0.25 + 0.45 * edge), overdue
    return min(risk_value, 0.20), overdue


def resurfacing_priority(note: dict, today: date, query: str | None) -> tuple[float, dict]:
    importance_value = IMPORTANCE_WEIGHT.get(note.get("importance", "medium"), 2.0) / 3.0
    due_value, overdue = due_pressure(note, today)
    if query:
        relevance_value, meta = detect_match(note, query)
        raw_relevance = meta.get("raw_score", 0.0)
    else:
        relevance_value, meta = 0.0, {"matched_fields": [], "overlap_terms": [], "raw_score": 0.0, "confidence": "none"}
        raw_relevance = 0.0
    repeat_value = repetition_signal(note, today)
    strength = memory_strength(note)
    strength_value = {"weak": 1.0, "normal": 0.75, "strong": 0.55}.get(strength, 0.75)

    score = (
        0.40 * repeat_value
        + 0.25 * relevance_value
        + 0.15 * due_value
        + 0.10 * importance_value
        + 0.10 * strength_value
    )
    meta.update(
        {
            "overdue_days": overdue,
            "raw_relevance": raw_relevance,
            "relevance_value": relevance_value,
            "due_pressure": due_value,
            "forgetting_risk": due_value,
            "importance_value": importance_value,
            "repetition_signal": repeat_value,
            "memory_strength": strength,
            "strength_value": strength_value,
        }
    )
    return score, meta
