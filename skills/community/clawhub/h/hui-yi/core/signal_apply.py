#!/usr/bin/env python3
"""Apply real session activation signals to a Hui-Yi cold note."""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import (
    load_tags_payload,
    note_file_path,
    parse_session_signals,
    replace_or_insert_section_metrics,
    resolve_memory_root,
    save_json,
    session_fingerprint,
    normalize_signal_history,
)

CONSECUTIVE_SESSION_WINDOW_DAYS = 14


def slugify(text: str) -> str:
    value = re.sub(r"[^\w\-\u4e00-\u9fff]+", "-", text.strip().lower())
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "session"


def find_note(notes: list[dict], target: str) -> dict | None:
    lookup = target.strip().lower()
    target_words = set(lookup.split())
    for note in notes:
        title_lower = (note.get("title") or "").strip().lower()
        path_lower = (note.get("path") or "").strip().lower()
        note_slug = Path(path_lower).stem
        if (
            title_lower == lookup
            or path_lower.endswith(lookup)
            or note_slug == lookup
            or (target_words and all(w in title_lower for w in target_words))
        ):
            return note
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply a real-session activation event to a Hui-Yi note")
    parser.add_argument("note")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--session-key", required=True)
    parser.add_argument("--strength", choices=["weak", "medium", "strong"], default="medium")
    parser.add_argument("--activated-at", default=None, help="ISO date, defaults to today")
    parser.add_argument("--source", default="feedback_useful")
    args = parser.parse_args(argv)

    memory_root = resolve_memory_root(args.memory_root)
    payload = load_tags_payload(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    matched = find_note(notes, args.note)
    if not matched:
        print(f"Note not found: {args.note!r}", file=sys.stderr)
        return 1

    note_path = note_file_path(memory_root, matched)
    if not note_path.exists():
        print(f"Backing note file missing: {note_path}", file=sys.stderr)
        return 1

    activated_day_obj = date.fromisoformat(args.activated_at) if args.activated_at else date.today()
    activated_day = activated_day_obj.isoformat()
    text = note_path.read_text(encoding="utf-8")
    signals = parse_session_signals(text)

    session_hash = session_fingerprint(args.session_key)
    dedup_key = f"{session_hash}|{slugify(Path(note_path).stem)}|{activated_day}|{args.source}"
    raw_history = matched.get("signal_history") if isinstance(matched.get("signal_history"), list) else []
    history = normalize_signal_history(raw_history)
    if dedup_key in history:
        if history != raw_history:
            matched["signal_history"] = history[-20:]
            payload.setdefault("_meta", {})["updated"] = activated_day
            save_json(memory_root / "tags.json", payload)
        print(f"SKIP duplicate activation: {matched.get('title')} | {dedup_key}", file=sys.stderr)
        return 0

    last_session_key = matched.get("last_session_key")
    same_session = last_session_key == session_hash
    signals["current_session_hits"] = (int(signals.get("current_session_hits", 0) or 0) + 1) if same_session else 1
    strength_bump = {"weak": 1, "medium": 1, "strong": 2}[args.strength]
    signals["recent_session_hits"] = int(signals.get("recent_session_hits", 0) or 0) + strength_bump

    if not same_session:
        signals["cross_session_repeat_count"] = int(signals.get("cross_session_repeat_count", 0) or 0) + 1
        last_activated = signals.get("last_activated")
        within_window = False
        if last_session_key and last_activated:
            try:
                within_window = date.fromisoformat(str(last_activated)) >= activated_day_obj - timedelta(days=CONSECUTIVE_SESSION_WINDOW_DAYS)
            except ValueError:
                within_window = False
        if within_window:
            signals["consecutive_session_count"] = int(signals.get("consecutive_session_count", 0) or 0) + 1
        else:
            signals["consecutive_session_count"] = 1
    else:
        signals["consecutive_session_count"] = max(1, int(signals.get("consecutive_session_count", 0) or 0))

    signals["last_activated"] = activated_day

    new_text = replace_or_insert_section_metrics(
        text,
        "Session signals",
        {
            "current_session_hits": signals["current_session_hits"],
            "recent_session_hits": signals["recent_session_hits"],
            "cross_session_repeat_count": signals["cross_session_repeat_count"],
            "consecutive_session_count": signals["consecutive_session_count"],
            "last_activated": signals["last_activated"],
        },
    )
    note_path.write_text(new_text, encoding="utf-8")

    matched["session_signals"] = signals
    matched["last_seen"] = activated_day
    matched["last_session_key"] = session_hash
    history = (history + [dedup_key])[-20:]
    matched["signal_history"] = history
    payload.setdefault("_meta", {})["updated"] = activated_day
    save_json(memory_root / "tags.json", payload)

    print(
        f"Applied signal: {matched.get('title')} | session_hash={session_hash} | "
        f"strength={args.strength} | recent_hits={signals['recent_session_hits']} | "
        f"cross_session_repeat_count={signals['cross_session_repeat_count']}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
