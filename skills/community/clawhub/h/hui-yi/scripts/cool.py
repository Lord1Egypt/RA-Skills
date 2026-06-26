#!/usr/bin/env python3
"""Cold-memory cooling helper for Hui-Yi.

Extended with lightweight forgetting-aware cold-memory stats.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json
from datetime import date, datetime
from pathlib import Path

from core.common import WORKSPACE_ROOT, load_json, save_json, resolve_path

DEFAULT_MEMORY_ROOT = WORKSPACE_ROOT / "memory"
DEFAULT_COLD_ROOT = DEFAULT_MEMORY_ROOT / "cold"


def resolve_roots(arg: str | None) -> tuple[Path, Path]:
    """Accept either workspace memory/ or cold-memory memory/cold/ roots.

    Most Hui-Yi scripts use --memory-root for memory/cold/. This helper keeps
    cool.py compatible with that convention while preserving its daily-note scan
    behavior, which needs the parent memory/ directory.
    """
    if not arg:
        return DEFAULT_MEMORY_ROOT, DEFAULT_COLD_ROOT
    root = resolve_path(arg)
    if root.name == "cold" or (root / "tags.json").exists():
        return root.parent, root
    return root, root / "cold"


def load_state(path: Path) -> dict:
    data = load_json(path, default={})
    return data if isinstance(data, dict) else {}


def save_state(path: Path, state: dict) -> None:
    save_json(path, state)


def ensure_cold_state(state: dict) -> dict:
    cold = state.get("coldMemory")
    if not isinstance(cold, dict):
        cold = {}
        state["coldMemory"] = cold
    cold.setdefault("lastScan", None)
    cold.setdefault("lastArchive", None)
    cold.setdefault("lastIndexRefresh", None)
    cold.setdefault("lastSummary", "")
    cold.setdefault("totalCoolings", 0)
    cold.setdefault("totalNotesArchived", 0)
    cold.setdefault("totalNotesMerged", 0)
    cold.setdefault("lastReviewSweep", None)
    cold.setdefault("reviewDueCount", 0)
    cold.setdefault("stateCounts", {"hot": 0, "warm": 0, "cold": 0, "dormant": 0})
    return cold


def parse_iso_to_date(value: str | None) -> date | None:
    if not value:
        return None
    # Extract the date portion only (first 10 chars: YYYY-MM-DD).
    # datetime.fromisoformat() on Python < 3.11 cannot parse timezone-aware
    # timestamps such as "2026-04-08T10:30:00+08:00", causing a silent ValueError
    # that makes lastArchive appear as None and scan_notes return ALL notes every run.
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def scan_notes(memory_root: Path, last_archive_date: date | None) -> list[Path]:
    all_notes = sorted(memory_root.glob("????-??-??*.md"))
    if last_archive_date is None:
        return all_notes

    pending: list[Path] = []
    for path in all_notes:
        prefix = path.stem[:10]
        try:
            note_date = date.fromisoformat(prefix)
        except ValueError:
            pending.append(path)
            continue
        if note_date > last_archive_date:
            pending.append(path)
    return pending


def compute_cold_stats(cold_root: Path) -> tuple[dict, int]:
    tags_path = cold_root / "tags.json"
    counts = {"hot": 0, "warm": 0, "cold": 0, "dormant": 0}
    due = 0
    today = date.today().isoformat()

    if not tags_path.exists():
        return counts, due

    try:
        data = json.loads(tags_path.read_text(encoding="utf-8"))
        # Support both the current {"notes": [...]} format and the legacy bare-array format.
        if isinstance(data, dict):
            notes = data.get("notes", []) if isinstance(data.get("notes"), list) else []
        elif isinstance(data, list):
            notes = data
        else:
            notes = []
    except Exception:
        return counts, due

    if not isinstance(notes, list):
        return counts, due

    for note in notes:
        if not isinstance(note, dict):
            continue
        state = note.get("state")
        if state in counts:
            counts[state] += 1
        next_review = note.get("next_review")
        if isinstance(next_review, str) and next_review and next_review <= today:
            due += 1
    return counts, due


def cmd_scan(args: argparse.Namespace) -> int:
    memory_root, cold_root = resolve_roots(args.memory_root)
    heartbeat = memory_root / "heartbeat-state.json"
    state = load_state(heartbeat)
    cold = ensure_cold_state(state)
    last_archive_date = parse_iso_to_date(cold.get("lastArchive"))
    pending = scan_notes(memory_root, last_archive_date)
    state_counts, review_due_count = compute_cold_stats(cold_root)

    print("=== Cooling scan ===")
    print(f"Memory root: {memory_root}")
    print(f"Last scan: {cold.get('lastScan')}")
    print(f"Last archive: {cold.get('lastArchive')}")
    print(f"Review due count: {review_due_count}")
    print(f"State counts: {json.dumps(state_counts, ensure_ascii=False)}\n")

    if not pending:
        print("No new daily notes pending cooling.")
    else:
        print(f"{len(pending)} daily note(s) pending cooling:")
        for path in pending:
            print(f"- {path.name}")

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    cold["lastScan"] = now
    cold["lastReviewSweep"] = now
    cold["reviewDueCount"] = review_due_count
    cold["stateCounts"] = state_counts
    save_state(heartbeat, state)
    return 0


def cmd_done(args: argparse.Namespace) -> int:
    memory_root, cold_root = resolve_roots(args.memory_root)
    heartbeat = memory_root / "heartbeat-state.json"
    state = load_state(heartbeat)
    cold = ensure_cold_state(state)
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    state_counts, review_due_count = compute_cold_stats(cold_root)

    cold["lastArchive"] = now
    cold["lastSummary"] = (
        f"Reviewed {args.reviewed}, archived {args.archived}, merged {args.merged}, "
        f"review_due {review_due_count}."
    )
    cold["totalCoolings"] = int(cold.get("totalCoolings", 0)) + 1
    cold["totalNotesArchived"] = int(cold.get("totalNotesArchived", 0)) + args.archived
    cold["totalNotesMerged"] = int(cold.get("totalNotesMerged", 0)) + args.merged
    cold["lastReviewSweep"] = now
    cold["reviewDueCount"] = review_due_count
    cold["stateCounts"] = state_counts

    save_state(heartbeat, state)
    print(json.dumps(cold, ensure_ascii=False, indent=2))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    memory_root, cold_root = resolve_roots(args.memory_root)
    heartbeat = memory_root / "heartbeat-state.json"
    state = load_state(heartbeat)
    cold = ensure_cold_state(state)
    state_counts, review_due_count = compute_cold_stats(cold_root)
    cold["stateCounts"] = state_counts
    cold["reviewDueCount"] = review_due_count
    print(json.dumps(cold, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["scan", "done", "status"])
    parser.add_argument("reviewed", type=int, nargs="?", default=0)
    parser.add_argument("archived", type=int, nargs="?", default=0)
    parser.add_argument("merged", type=int, nargs="?", default=0)
    parser.add_argument("--memory-root", default=None)
    args = parser.parse_args()

    if args.command == "scan":
        return cmd_scan(args)
    if args.command == "done":
        return cmd_done(args)
    return cmd_status(args)


if __name__ == "__main__":
    raise SystemExit(main())
