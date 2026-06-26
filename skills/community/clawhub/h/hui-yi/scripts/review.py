#!/usr/bin/env python3
"""Review and resurface Hui-Yi cold memories.

Commands:
- due:      list notes whose next_review is due or overdue
- resurface: rank resurfacing candidates using repetition-first reinforcement
- feedback: log retrieval feedback and update note review metadata
- session:  interactive batch review of due or repeatedly-activated notes
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
from datetime import date
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.signal_apply import main as signal_apply_main
from core.common import (
    load_tags_payload,
    memory_strength,
    note_file_path,
    parse_date,
    parse_heading_value,
    repetition_signal,
    resolve_memory_root,
    save_json,
)
from core.feedback_core import DORMANT_INTERVAL_DAYS, write_note_feedback
from core.scoring import resurfacing_priority
from core.signal_detect import load_context_text
from core.signal_pipeline import apply_candidates


def load_tags(memory_root: Path) -> dict:
    return load_tags_payload(memory_root)


def save_tags(memory_root: Path, payload: dict) -> None:
    payload.setdefault("_meta", {})["updated"] = date.today().isoformat()
    save_json(memory_root / "tags.json", payload)


def cmd_due(args: argparse.Namespace) -> int:
    memory_root = resolve_memory_root(args.memory_root)
    payload = load_tags(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    today = date.today()
    due = []
    for note in notes:
        next_review = parse_date(note.get("next_review"))
        repeat_value = repetition_signal(note, today)
        if (next_review and next_review <= today) or repeat_value >= 0.35:
            score, meta = resurfacing_priority(note, today, None)
            due.append((score, meta, note))

    due.sort(key=lambda item: item[0], reverse=True)
    if not due:
        print("No notes due for review.")
        return 0

    print("Due notes:")
    for score, meta, note in due[: args.limit]:
        print(
            f"- priority={score:.3f} overdue={meta['overdue_days']}d repeat={meta.get('repetition_signal', 0.0):.3f} | {note.get('title')} | "
            f"importance={note.get('importance')} state={note.get('state')} "
            f"strength={meta.get('memory_strength')} next_review={note.get('next_review')}"
        )
    return 0


def cmd_resurface(args: argparse.Namespace) -> int:
    memory_root = resolve_memory_root(args.memory_root)
    payload = load_tags(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    today = date.today()
    query_text = load_context_text(args.query, args.context_file, args.stdin)
    candidates = []

    for note in notes:
        score, meta = resurfacing_priority(note, today, query_text)
        if query_text:
            if meta["relevance_value"] < args.min_relevance and meta.get("repetition_signal", 0.0) < 0.35:
                continue
            strong_fields = {"title", "summary", "tags", "triggers"}
            matched_fields = set(meta.get("matched_fields", []))
            if not (strong_fields & matched_fields) and meta.get("repetition_signal", 0.0) < 0.35:
                continue
        else:
            next_review = parse_date(note.get("next_review"))
            if (not next_review or next_review > today) and meta.get("repetition_signal", 0.0) < 0.35:
                continue
        if score >= args.min_priority:
            candidates.append((score, meta, note))

    candidates.sort(key=lambda item: item[0], reverse=True)
    if not candidates:
        print("No resurfacing candidates right now.")
        return 0

    print("Resurfacing candidates:")
    surfaced = candidates[: args.limit]
    if args.write_signals and args.session_key:
        signal_candidates = [
            {
                "title": note.get("title"),
                "path": note.get("path"),
                "relevance": meta.get("relevance_value", 0.0),
                "confidence": "high" if meta.get("relevance_value", 0.0) >= 0.60 else "medium",
                "matched_fields": meta.get("matched_fields", []),
                "overlap_terms": meta.get("overlap_terms", []),
                "raw_score": meta.get("raw_relevance", 0.0),
                "repetition_signal": meta.get("repetition_signal", 0.0),
            }
            for _, meta, note in surfaced
            if meta.get("relevance_value", 0.0) >= max(args.min_relevance, 0.30) or meta.get("repetition_signal", 0.0) >= 0.35
        ]
        apply_candidates(
            memory_root,
            signal_candidates,
            args.session_key,
            strength="weak",
            source="resurface_candidate",
            activated_at=today.isoformat(),
        )
        payload = load_tags(memory_root)
        notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
        by_path = {n.get("path"): n for n in notes}
        surfaced = [(score, meta, by_path.get(note.get("path"), note)) for score, meta, note in surfaced]

    for score, meta, note in surfaced:
        prompt = f"You previously touched on '{note.get('title')}'. Want me to pull that thread back in?"
        print(f"- priority={score:.3f} | {note.get('title')}")
        print(
            f"  repetition={meta.get('repetition_signal', 0.0):.3f} relevance={meta['relevance_value']:.3f} due_pressure={meta['due_pressure']:.3f} "
            f"overdue={meta['overdue_days']}d importance={note.get('importance')} "
            f"state={note.get('state')} strength={meta.get('memory_strength')}"
        )
        if query_text:
            overlap = ", ".join(meta.get("overlap_terms", [])) or "n/a"
            fields = ", ".join(meta.get("matched_fields", [])) or "n/a"
            print(f"  context_query={query_text[:200].replace(chr(10), ' ')}")
            print(f"  overlap_terms={overlap}")
            print(f"  matched_fields={fields}")
        print(f"  prompt: {prompt}")
        print(f"  path: {note.get('path')}")
    return 0


def apply_session_signal(
    memory_root: Path,
    note_name: str,
    session_key: str | None,
    today: date,
    *,
    strength: str,
    source: str,
) -> None:
    if not session_key:
        return

    original_argv = sys.argv
    try:
        sys.argv = [
            "signal_apply.py",
            note_name,
            "--memory-root",
            str(memory_root),
            "--session-key",
            session_key,
            "--strength",
            strength,
            "--source",
            source,
            "--activated-at",
            today.isoformat(),
        ]
        exit_code = signal_apply_main()
        if exit_code != 0:
            print(f"Warning: signal_apply reported error (exit code {exit_code}).")
    finally:
        sys.argv = original_argv


def apply_feedback_signal(memory_root: Path, note_name: str, useful: str, session_key: str | None, today: date) -> None:
    if useful != "yes" or not session_key:
        return
    apply_session_signal(
        memory_root,
        note_name,
        session_key,
        today,
        strength="strong",
        source="feedback_useful",
    )


def cmd_feedback(args: argparse.Namespace) -> int:
    memory_root = resolve_memory_root(args.memory_root)
    payload = load_tags(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    today = date.today()

    target = args.note.strip().lower()
    target_words = set(target.split())

    matched = None
    for note in notes:
        title_lower = (note.get("title") or "").strip().lower()
        path_lower = (note.get("path") or "").strip().lower()
        note_slug = Path(path_lower).stem
        if (
            title_lower == target
            or path_lower.endswith(target)
            or note_slug == target
            or (target_words and all(w in title_lower for w in target_words))
        ):
            matched = note
            break

    if not matched:
        print(f"Note not found: {args.note!r}")
        print("Tip: pass a slug (filename without .md), exact title, or keywords that all appear in the title.")
        return 1

    note_path = note_file_path(memory_root, matched)
    if not note_path.exists():
        print(f"Backing note file missing: {note_path}")
        return 1

    text = note_path.read_text(encoding="utf-8")
    state, interval_days, next_review = write_note_feedback(
        note_path,
        matched,
        text,
        args.useful,
        today,
        log_path=memory_root / "retrieval-log.md",
        query=args.query,
        action=args.action,
    )
    apply_feedback_signal(memory_root, matched.get("path") or matched.get("title") or args.note, args.useful, args.session_key, today)
    payload = load_tags(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    refreshed = next((n for n in notes if (n.get("path") == matched.get("path"))), matched)

    note_path = note_file_path(memory_root, refreshed)
    if note_path.exists():
        refreshed_text = note_path.read_text(encoding="utf-8")
        refreshed["strength"] = memory_strength(refreshed)
        refreshed["state"] = parse_heading_value(refreshed_text, "Memory state") or refreshed.get("state")
        refreshed["next_review"] = parse_heading_value(refreshed_text, "Next review") or refreshed.get("next_review")
        refreshed["last_reviewed"] = parse_heading_value(refreshed_text, "Last reviewed") or refreshed.get("last_reviewed")

    save_tags(memory_root, payload)

    matched = refreshed
    strength = matched.get("strength", memory_strength(matched))
    graduated = state == "dormant" and interval_days >= min(DORMANT_INTERVAL_DAYS.values())
    if graduated:
        print(
            f"🎓 Graduated: {matched.get('title')} — well-consolidated after "
            f"{matched.get('review', {}).get('review_count', '?')} reviews. "
            f"State → dormant, strength={strength}, next review in {interval_days} days."
        )
    else:
        print(
            f"Updated {matched.get('title')}: useful={args.useful}, "
            f"state={state}, strength={strength}, interval_days={interval_days}, next_review={next_review}"
        )
    return 0


def cmd_session(args: argparse.Namespace) -> int:
    memory_root = resolve_memory_root(args.memory_root)
    payload = load_tags(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    today = date.today()
    log_path = memory_root / "retrieval-log.md"

    due: list[tuple[float, dict, dict]] = []
    for note in notes:
        next_review = parse_date(note.get("next_review"))
        repeat_value = repetition_signal(note, today)
        if (next_review and next_review <= today) or repeat_value >= 0.35:
            score, meta = resurfacing_priority(note, today, None)
            due.append((score, meta, note))
    due.sort(key=lambda item: item[0], reverse=True)

    if not due:
        print("✓ Nothing due for review today.")
        return 0

    total = len(due)
    print(f"\n{'─' * 60}")
    print(f"  Review session — {total} note(s) due or repeatedly activated")
    print(f"  Commands:  y = useful   n = not useful   s = skip   q = quit")
    print(f"{'─' * 60}\n")

    reviewed = 0
    skipped = 0
    graduated_titles: list[str] = []

    for idx, (score, meta, note) in enumerate(due, 1):
        note_path = note_file_path(memory_root, note)
        if not note_path.exists():
            print(f"[{idx}/{total}] SKIP — file missing: {note.get('title')}\n")
            skipped += 1
            continue

        text = note_path.read_text(encoding="utf-8")
        tldr: list[str] = []
        in_section = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped == "## TL;DR":
                in_section = True
                continue
            if in_section:
                if stripped.startswith("## "):
                    break
                if stripped.startswith("- ") and stripped[2:].strip():
                    tldr.append(stripped[2:].strip())
                elif stripped and not stripped.startswith("-"):
                    tldr.append(stripped)

        overdue = meta.get("overdue_days", 0)
        print(f"[{idx}/{total}]  {note.get('title', 'untitled')}")
        print(f"         importance={note.get('importance','?')}  "
              f"state={note.get('state','?')}  strength={memory_strength(note)}  overdue={overdue}d  "
              f"repeat={meta.get('repetition_signal', 0.0):.3f}  priority={score:.3f}")
        for line in tldr[:4]:
            print(f"         → {line}")
        print()

        while True:
            try:
                raw = input("  Recall? [y/n/s/q] > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n\nSession interrupted (Ctrl+C).")
                _save_and_report(payload, memory_root, reviewed, skipped, total, graduated_titles)
                return 0

            if raw == "q":
                print()
                _save_and_report(payload, memory_root, reviewed, skipped, total, graduated_titles)
                return 0
            if raw == "s":
                skipped += 1
                print("  → Skipped.\n")
                break
            if raw in ("y", "n"):
                useful = "yes" if raw == "y" else "no"
                state, interval_days, next_review = write_note_feedback(
                    note_path, note, text, useful, today, log_path=log_path
                )
                save_tags(memory_root, payload)

                note["strength"] = memory_strength(note)
                graduated = state == "dormant" and interval_days >= min(DORMANT_INTERVAL_DAYS.values())
                strength = note.get("strength", memory_strength(note))
                if graduated:
                    graduated_titles.append(note.get("title", "?"))
                    print(f"  🎓 Graduated! → dormant, strength={strength}, next review +{interval_days}d\n")
                else:
                    arrow = "↑" if useful == "yes" else "↓"
                    print(f"  {arrow} {state} / {strength} | +{interval_days}d → next: {next_review}\n")
                reviewed += 1
                break
            else:
                print("  Enter y, n, s, or q.")

    _save_and_report(payload, memory_root, reviewed, skipped, total, graduated_titles)
    return 0


def _save_and_report(payload: dict, memory_root: Path, reviewed: int, skipped: int, total: int, graduated_titles: list[str]) -> None:
    save_tags(memory_root, payload)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    upcoming = [n.get("next_review") for n in notes if n.get("next_review")]
    today_str = date.today().isoformat()
    future = [d for d in upcoming if d > today_str]
    next_session = min(future) if future else "n/a"

    print(f"{'─' * 60}")
    print(f"  Done. Reviewed {reviewed} / {total}  (skipped {skipped})")
    if graduated_titles:
        print(f"  🎓 Graduated: {', '.join(graduated_titles)}")
    print(f"  Next earliest review: {next_session}")
    print(f"{'─' * 60}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    due = sub.add_parser("due")
    due.add_argument("--memory-root", default=None)
    due.add_argument("--limit", type=int, default=10)

    resurface = sub.add_parser("resurface")
    resurface.add_argument("--memory-root", default=None)
    resurface.add_argument("--limit", type=int, default=5)
    resurface.add_argument("--query", default=None, help="short query or topic summary")
    resurface.add_argument("--context-file", default=None, help="path to a text file containing richer context")
    resurface.add_argument("--stdin", action="store_true", help="read additional context from stdin")
    resurface.add_argument("--min-relevance", type=float, default=0.15)
    resurface.add_argument("--min-priority", type=float, default=0.20)
    resurface.add_argument("--session-key", default=None, help="stable session identifier for optional weak activation writeback")
    resurface.add_argument("--write-signals", action="store_true", help="write weak activation signals for high-confidence resurfacing hits")

    feedback = sub.add_parser("feedback")
    feedback.add_argument("note")
    feedback.add_argument("--useful", choices=["yes", "no"], required=True)
    feedback.add_argument("--query", default=None)
    feedback.add_argument("--action", default=None)
    feedback.add_argument("--session-key", default=None, help="stable session identifier for real-session signal accumulation")
    feedback.add_argument("--memory-root", default=None)

    session = sub.add_parser("session", help="Interactive batch review of all due or repeatedly activated notes")
    session.add_argument("--memory-root", default=None)

    args = parser.parse_args()
    if args.command == "due":
        return cmd_due(args)
    if args.command == "resurface":
        return cmd_resurface(args)
    if args.command == "session":
        return cmd_session(args)
    return cmd_feedback(args)


if __name__ == "__main__":
    raise SystemExit(main())
