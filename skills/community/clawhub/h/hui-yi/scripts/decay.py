#!/usr/bin/env python3
"""Light maintenance helper for Hui-Yi cold memories.

This script is intentionally **not** the primary reinforcement engine.
Its job is limited to:
- confidence maintenance when verification is stale
- keeping overdue notes due now (never pushing them further away)
- reporting weak maintenance signals for operator review

It must not override repetition-driven reinforcement with aggressive state demotion.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import re
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import (
    DEFAULT_MEMORY_ROOT,
    SKIP_MARKDOWN,
    normalized_session_signals,
    parse_date,
    parse_heading_value,
    parse_review_metric,
    repetition_signal,
    resolve_memory_root,
    run_main_with_argv,
)
from scripts.rebuild import main as rebuild_main

SKIP = SKIP_MARKDOWN
CONFIDENCE_ORDER = ["high", "medium", "low"]
DEFAULT_INTERVAL_DAYS = 1


def replace_heading_bullet(text: str, heading: str, new_value: str) -> str:
    pattern = re.compile(
        rf"(^## {re.escape(heading)}\s*$\n)(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(rf"\1- {new_value}\n\n", text, count=1)
    return text


def iter_notes(root: Path):
    for path in root.rglob("*.md"):
        if path.name in SKIP:
            continue
        yield path


def demote_confidence(confidence: str | None) -> str | None:
    if confidence not in CONFIDENCE_ORDER:
        return confidence
    idx = CONFIDENCE_ORDER.index(confidence)
    return CONFIDENCE_ORDER[min(idx + 1, len(CONFIDENCE_ORDER) - 1)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Light maintenance helper for Hui-Yi notes. Keeps overdue reviews due now and avoids time-driven state demotion."
    )
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Run rebuild.py automatically after maintenance to sync index.md and tags.json",
    )
    args = parser.parse_args()

    root = resolve_memory_root(args.memory_root)
    today = date.today()
    changes = []
    maintenance_flags = []

    for path in iter_notes(root):
        text = path.read_text(encoding="utf-8")
        confidence = parse_heading_value(text, "Confidence")
        state = parse_heading_value(text, "Memory state")
        last_verified = parse_date(parse_heading_value(text, "Last verified") or "")
        last_reviewed = parse_date(parse_heading_value(text, "Last reviewed") or "")
        last_seen = parse_date(parse_heading_value(text, "Last seen") or "")
        next_review = parse_date(parse_heading_value(text, "Next review") or "")
        interval_days = parse_review_metric(text, "interval_days", DEFAULT_INTERVAL_DAYS)
        review_count = parse_review_metric(text, "review_count", 0)
        review_anchor = last_reviewed or last_seen or last_verified
        review_age = (today - review_anchor).days if review_anchor else None
        verify_age = (today - last_verified).days if last_verified else None
        overdue_days = (today - next_review).days if next_review else None

        target_confidence = confidence
        target_next_review = next_review.isoformat() if next_review else None
        reasons = []

        parsed_signals = normalized_session_signals({})
        if "## Session signals" in text:
            session_block = text.replace("## Session signals", "## Review cadence")
            parsed_signals["current_session_hits"] = parse_review_metric(session_block, "current_session_hits", 0)
            parsed_signals["recent_session_hits"] = parse_review_metric(session_block, "recent_session_hits", 0)
            parsed_signals["cross_session_repeat_count"] = parse_review_metric(session_block, "cross_session_repeat_count", 0)
            parsed_signals["consecutive_session_count"] = parse_review_metric(session_block, "consecutive_session_count", 0)
            last_activated_match = re.search(r"^-\s*last_activated\s*:\s*(.+?)\s*$", text, re.MULTILINE)
            if last_activated_match:
                parsed_signals["last_activated"] = last_activated_match.group(1).strip()
        repeat_value = repetition_signal({"session_signals": parsed_signals}, today)

        if verify_age is not None:
            if verify_age > 180 and confidence == "medium":
                target_confidence = "low"
                reasons.append(f"verification stale {verify_age}d")
            elif verify_age > 120 and confidence == "high":
                target_confidence = "medium"
                reasons.append(f"verification old {verify_age}d")

        if overdue_days is not None and overdue_days > 0:
            target_next_review = today.isoformat()
            reasons.append("review overdue; keep due now")

        if review_age is not None and review_age > 180 and review_count <= 1 and repeat_value < 0.20:
            maintenance_flags.append((path, f"low reinforcement signal for {review_age}d; consider manual review"))

        if state == "dormant" and repeat_value >= 0.35:
            maintenance_flags.append((path, "dormant note is being reactivated; consider resurfacing or warming it manually"))

        if not reasons:
            continue

        changes.append((path, confidence, target_confidence, target_next_review, reasons))

        if not args.dry_run:
            new_text = text
            if target_confidence and target_confidence != confidence:
                new_text = replace_heading_bullet(new_text, "Confidence", target_confidence)
            if target_next_review:
                new_text = replace_heading_bullet(new_text, "Next review", target_next_review)
            path.write_text(new_text, encoding="utf-8")

    if not changes and not maintenance_flags:
        print(f"No maintenance needed. memory root: {root}")
        return 0

    for path, old_conf, new_conf, next_review, reasons in changes:
        print(
            f"UPDATE: {path} | confidence {old_conf} -> {new_conf} | next review {next_review or 'n/a'} | reasons: {', '.join(reasons)}"
        )
    for path, reason in maintenance_flags:
        print(f"FLAG: {path} — {reason}")

    if args.dry_run:
        print("Dry run only; no files modified.")
        return 0

    if args.rebuild:
        heartbeat_path = root.parent / "heartbeat-state.json"
        exit_code = run_main_with_argv(
            rebuild_main,
            [
                "rebuild.py",
                "--memory-root",
                str(root),
                "--heartbeat-path",
                str(heartbeat_path),
            ],
        )
        if exit_code == 0:
            print("\nRebuild completed successfully via direct function call.")
        else:
            print(f"\nWarning: rebuild reported error (exit code {exit_code}).")
    else:
        print("\nNote: tags.json and index.md are NOT yet updated.")
        print("Run 'python3 scripts/rebuild.py' to sync them, or rerun with --rebuild.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
