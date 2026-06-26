#!/usr/bin/env python3
"""Shared feedback and state-transition logic for Hui-Yi."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import re
from datetime import date, timedelta
from pathlib import Path

from core.common import DEFAULT_INTERVAL_DAYS, REVIEW_LADDER, memory_strength, parse_heading_value, parse_review_metric, read_text_fallback

GRADUATION_MIN_REVIEWS = 7
GRADUATION_MIN_SUCCESS_RATE = 0.8
GRADUATION_INTERVAL_DAYS = {"high": 180, "medium": 120, "low": 90}
DORMANT_INTERVAL_DAYS = {"high": 180, "medium": 270, "low": 365}
ADAPTIVE_GROWTH = {"high": 1.35, "medium": 1.5, "low": 1.7}


def replace_heading_bullet(text: str, heading: str, new_value: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}\s*$\n)(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(rf"\1- {new_value}\n\n", text, count=1)
    return text + f"\n## {heading}\n- {new_value}\n"


def replace_review_metric(text: str, key: str, new_value: int) -> str:
    block_pattern = re.compile(r"(^## Review cadence\s*$)(.*?)(^(?:## |\Z))", re.MULTILINE | re.DOTALL)
    match = block_pattern.search(text)
    if not match:
        insertion = (
            f"\n## Review cadence\n"
            f"- interval_days: {DEFAULT_INTERVAL_DAYS}\n"
            f"- review_count: 0\n"
            f"- review_success: 0\n"
            f"- review_fail: 0\n"
            f"- retrieval_count: 0\n"
            f"- reinforcement_count: 0\n"
        )
        text += insertion
        match = block_pattern.search(text)
        if not match:
            return text
    block = match.group(2)
    metric_pattern = re.compile(rf"(^-\s*{re.escape(key)}\s*:\s*)(\d+)(\s*$)", re.MULTILINE)
    if metric_pattern.search(block):
        block = metric_pattern.sub(rf"\g<1>{new_value}\g<3>", block, count=1)
    else:
        if not block.endswith("\n"):
            block += "\n"
        block += f"- {key}: {new_value}\n"
    return text[: match.start(2)] + block + text[match.end(2) :]


def append_retrieval_log(log_path: Path, row: str) -> None:
    header = "# Retrieval Log\n\n| Date | Query | Matched | Useful | Action |\n|---|---|---|---|---|\n"
    if not log_path.exists():
        log_path.write_text(header, encoding="utf-8")
    current = read_text_fallback(log_path)
    if not current.endswith("\n"):
        current += "\n"
    current += row + "\n"
    log_path.write_text(current, encoding="utf-8")


def next_success_interval(interval_days: int, importance: str) -> int:
    current = max(1, interval_days)
    for step in REVIEW_LADDER:
        if current < step:
            return step
    growth = ADAPTIVE_GROWTH.get(importance, ADAPTIVE_GROWTH["medium"])
    return max(REVIEW_LADDER[-1], int(__import__("math").ceil(current * growth)))


def relearning_interval(interval_days: int) -> int:
    return 1 if interval_days <= REVIEW_LADDER[4] else 2


def compute_next_state(text: str, note: dict, useful: str, today: date) -> tuple[str, int, int, int, int, int, int, str]:
    interval_days = parse_review_metric(text, "interval_days", DEFAULT_INTERVAL_DAYS)
    review_count = parse_review_metric(text, "review_count", 0) + 1
    review_success = parse_review_metric(text, "review_success", 0)
    review_fail = parse_review_metric(text, "review_fail", 0)
    retrieval_count = parse_review_metric(text, "retrieval_count", 0) + 1
    reinforcement_count = parse_review_metric(text, "reinforcement_count", 0)
    state = parse_heading_value(text, "Memory state") or note.get("state", "cold")
    importance = note.get("importance", "medium")

    if useful == "yes":
        review_success += 1
        reinforcement_count += 1
        interval_days = next_success_interval(interval_days, importance)
        if state in {"cold", "dormant"}:
            state = "warm"
        elif state == "warm" and (importance == "high" or reinforcement_count >= 3):
            state = "hot"
    else:
        review_fail += 1
        interval_days = relearning_interval(interval_days)
        if state == "hot":
            state = "warm"
        else:
            state = "cold"

    success_rate = review_success / max(review_count, 1)
    graduation_interval = GRADUATION_INTERVAL_DAYS.get(importance, GRADUATION_INTERVAL_DAYS["medium"])
    dormant_interval = DORMANT_INTERVAL_DAYS.get(importance, DORMANT_INTERVAL_DAYS["medium"])
    if (
        state != "dormant"
        and useful == "yes"
        and reinforcement_count >= 3
        and review_success >= GRADUATION_MIN_REVIEWS
        and success_rate >= GRADUATION_MIN_SUCCESS_RATE
        and interval_days >= graduation_interval
    ):
        state = "dormant"
        interval_days = dormant_interval

    next_review = (today + timedelta(days=interval_days)).isoformat()
    return state, interval_days, review_count, review_success, review_fail, retrieval_count, reinforcement_count, next_review


def write_note_feedback(
    note_path: Path,
    note: dict,
    text: str,
    useful: str,
    today: date,
    log_path: Path | None = None,
    query: str | None = None,
    action: str | None = None,
) -> tuple[str, int, str]:
    (
        state,
        interval_days,
        review_count,
        review_success,
        review_fail,
        retrieval_count,
        reinforcement_count,
        next_review,
    ) = compute_next_state(text, note, useful, today)
    today_str = today.isoformat()

    new_text = replace_review_metric(text, "interval_days", interval_days)
    new_text = replace_review_metric(new_text, "review_count", review_count)
    new_text = replace_review_metric(new_text, "review_success", review_success)
    new_text = replace_review_metric(new_text, "review_fail", review_fail)
    new_text = replace_review_metric(new_text, "retrieval_count", retrieval_count)
    new_text = replace_review_metric(new_text, "reinforcement_count", reinforcement_count)
    new_text = replace_heading_bullet(new_text, "Last reviewed", today_str)
    new_text = replace_heading_bullet(new_text, "Last seen", today_str)
    new_text = replace_heading_bullet(new_text, "Next review", next_review)
    new_text = replace_heading_bullet(new_text, "Memory state", state)
    note_path.write_text(new_text, encoding="utf-8")

    note["state"] = state
    note["last_reviewed"] = today_str
    note["last_seen"] = today_str
    note["next_review"] = next_review
    if not isinstance(note.get("review"), dict):
        note["review"] = {}
    note["review"]["interval_days"] = interval_days
    note["review"]["review_count"] = review_count
    note["review"]["review_success"] = review_success
    note["review"]["review_fail"] = review_fail
    note["review"]["retrieval_count"] = retrieval_count
    note["review"]["reinforcement_count"] = reinforcement_count
    note["strength"] = memory_strength(note)

    if log_path is not None:
        _q = query or note.get("title") or "session review"
        _a = action or ("reinforced note" if useful == "yes" else "weakened note")
        append_retrieval_log(
            log_path,
            f"| {today_str} | {_q} | {Path(note.get('path', '')).name} | {useful} | {_a} |",
        )

    return state, interval_days, next_review
