#!/usr/bin/env python3
"""Rebuild Hui-Yi index.md and tags.json from note files.

Now supports forgetting-aware metadata such as importance, state, review cadence,
last_seen, last_reviewed, and next_review.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path

from core.common import DEFAULT_HEARTBEAT_PATH, DEFAULT_MEMORY_ROOT, WORKSPACE_ROOT, load_json, memory_strength, save_json

SKIP = {"index.md", "retrieval-log.md", "_template.md"}
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INTERVAL_DAYS = 1  # Ebbinghaus: first review at +1 day while memory is still fresh
DEFAULT_IMPORTANCE = "medium"
DEFAULT_STATE = "cold"
VALID_IMPORTANCE = {"high", "medium", "low"}
VALID_STATE = {"hot", "warm", "cold", "dormant"}
VALID_CONFIDENCE = {"high", "medium", "low"}


def resolve_memory_root(arg: str | None) -> Path:
    if arg:
        candidate = Path(arg)
        return candidate if candidate.is_absolute() else (Path.cwd() / candidate).resolve()
    return DEFAULT_MEMORY_ROOT


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


def parse_section_lines(lines: list[str], heading: str) -> list[str]:
    out: list[str] = []
    capture = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line == heading:
            capture = True
            continue
        if capture and stripped_line.startswith("## "):
            break
        if capture:
            if stripped_line.startswith("- "):
                out.append(stripped_line[2:].strip())
            elif stripped_line:
                out.append(stripped_line)
    return out


def parse_single_value(lines: list[str], heading: str) -> str:
    values = parse_section_lines(lines, heading)
    return values[0] if values else ""


def parse_date_value(value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    for parser in (datetime.fromisoformat,):
        try:
            return parser(value).date().isoformat()
        except Exception:
            pass
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError:
        return None


def parse_int_after_colon(values: list[str], key: str, default: int = 0) -> int:
    prefix = f"{key}:"
    for value in values:
        if value.lower().startswith(prefix.lower()):
            raw = value.split(":", 1)[1].strip()
            try:
                return int(raw)
            except ValueError:
                return default
    return default


def normalize_enum(value: str, valid: set[str], default: str) -> str:
    value = value.strip().lower()
    return value if value in valid else default


def default_next_review(last_seen: str | None, interval_days: int) -> str:
    if not last_seen:
        # No review anchor available (brand-new note with no dates).
        # Schedule the first review tomorrow so the note enters the review queue
        # immediately — consistent with the Ebbinghaus +1d first-review principle.
        return (date.today() + timedelta(days=1)).isoformat()
    try:
        base = date.fromisoformat(last_seen)
    except ValueError:
        return (date.today() + timedelta(days=1)).isoformat()
    return (base + timedelta(days=max(interval_days, 1))).isoformat()


def relative_note_path(path: Path, memory_root: Path) -> Path:
    rel = path.relative_to(memory_root)
    return Path("memory") / "cold" / rel


def parse_session_signals(lines: list[str]) -> dict:
    values = parse_section_lines(lines, "## Session signals")
    current_session_hits = parse_int_after_colon(values, "current_session_hits", 0)
    recent_session_hits = parse_int_after_colon(values, "recent_session_hits", 0)
    cross_session_repeat_count = parse_int_after_colon(values, "cross_session_repeat_count", 0)
    consecutive_session_count = parse_int_after_colon(values, "consecutive_session_count", 0)
    last_activated = None
    for value in values:
        if value.lower().startswith("last_activated:"):
            raw = value.split(":", 1)[1].strip()
            last_activated = parse_date_value(raw)
            break
    return {
        "current_session_hits": current_session_hits,
        "recent_session_hits": recent_session_hits,
        "cross_session_repeat_count": cross_session_repeat_count,
        "consecutive_session_count": consecutive_session_count,
        "last_activated": last_activated,
    }


def parse_note(path: Path, memory_root: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), path.stem)
    summary_lines = parse_section_lines(lines, "## TL;DR")
    memory_type = parse_single_value(lines, "## Memory type") or "unknown"
    importance = normalize_enum(parse_single_value(lines, "## Importance") or DEFAULT_IMPORTANCE, VALID_IMPORTANCE, DEFAULT_IMPORTANCE)
    state = normalize_enum(parse_single_value(lines, "## Memory state") or DEFAULT_STATE, VALID_STATE, DEFAULT_STATE)
    semantic_context = " ".join(parse_section_lines(lines, "## Semantic context"))
    triggers = parse_section_lines(lines, "## Triggers")
    scenarios = parse_section_lines(lines, "## Use this when")
    confidence = normalize_enum(parse_single_value(lines, "## Confidence") or "medium", VALID_CONFIDENCE, "medium")
    last_verified = parse_date_value(parse_single_value(lines, "## Last verified") or "")
    tags = parse_section_lines(lines, "## Related tags")
    review_lines = parse_section_lines(lines, "## Review cadence")
    session_signals = parse_session_signals(lines)
    interval_days = parse_int_after_colon(review_lines, "interval_days", DEFAULT_INTERVAL_DAYS)
    review_count = parse_int_after_colon(review_lines, "review_count", 0)
    review_success = parse_int_after_colon(review_lines, "review_success", 0)
    review_fail = parse_int_after_colon(review_lines, "review_fail", 0)
    retrieval_count = parse_int_after_colon(review_lines, "retrieval_count", 0)
    reinforcement_count = parse_int_after_colon(review_lines, "reinforcement_count", 0)
    last_seen = parse_date_value(parse_single_value(lines, "## Last seen") or "") or last_verified
    last_reviewed = parse_date_value(parse_single_value(lines, "## Last reviewed") or "")
    next_review = parse_date_value(parse_single_value(lines, "## Next review") or "")
    if not next_review:
        anchor = last_reviewed or last_seen
        next_review = default_next_review(anchor, interval_days)

    rel_path = relative_note_path(path, memory_root).as_posix()
    summary = summary_lines[0] if summary_lines else title
    updated = last_verified or last_seen or date.today().isoformat()
    review = {
        "interval_days": interval_days,
        "review_count": review_count,
        "review_success": review_success,
        "review_fail": review_fail,
        "retrieval_count": retrieval_count,
        "reinforcement_count": reinforcement_count,
    }

    return {
        "title": title,
        "path": rel_path,
        "type": memory_type,
        "importance": importance,
        "state": state,
        "summary": summary,
        "semantic_context": semantic_context,
        "tags": tags,
        "triggers": triggers,
        "scenarios": scenarios,
        "confidence": confidence,
        "last_seen": last_seen,
        "last_reviewed": last_reviewed,
        "next_review": next_review,
        "review": review,
        "session_signals": session_signals,
        "strength": memory_strength({"review": review, "state": state}, DEFAULT_INTERVAL_DAYS),
        "last_verified": last_verified or "unknown",
        "updated": updated,
    }


def note_paths(memory_root: Path) -> list[Path]:
    paths = []
    for path in memory_root.rglob("*.md"):
        if path.name in SKIP:
            continue
        if path.parent == memory_root or path.parent.parent == memory_root:
            paths.append(path)
    return sorted(paths)


def backup_if_exists(path: Path) -> None:
    if path.exists():
        shutil.copy2(path, path.with_suffix(path.suffix + ".bak"))


def build_index(notes: list[dict]) -> str:
    lines = ["# Cold Memory Index", "", "## Entries", ""]
    notes_sorted = sorted(notes, key=lambda n: (n.get("updated") or "", n.get("importance") == "high"), reverse=True)
    for note in notes_sorted:
        lines.append(f"- `{Path(note['path']).name}` — {note['summary']}")
        lines.append(f"  - type: {note['type']}")
        lines.append(f"  - importance: {note['importance']}")
        lines.append(f"  - state: {note['state']}")
        lines.append(f"  - tags: {', '.join(note['tags']) if note['tags'] else 'none'}")
        lines.append(f"  - triggers: {', '.join(note['triggers']) if note['triggers'] else 'none'}")
        lines.append(f"  - read when: {'; '.join(note['scenarios']) if note['scenarios'] else 'n/a'}")
        lines.append(f"  - confidence: {note['confidence']}")
        lines.append(f"  - strength: {note.get('strength', 'weak')}")
        signals = note.get('session_signals', {}) if isinstance(note.get('session_signals'), dict) else {}
        lines.append(f"  - repetition: current={signals.get('current_session_hits', 0)}, recent={signals.get('recent_session_hits', 0)}, cross={signals.get('cross_session_repeat_count', 0)}")
        lines.append(f"  - updated: {note['updated']}")
        lines.append(f"  - next review: {note['next_review'] or 'none'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_tags(notes: list[dict]) -> str:
    payload = {
        "_meta": {
            "description": "Structured metadata for cold-memory retrieval",
            "version": 5,
            "updated": date.today().isoformat(),
        },
        "notes": notes,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def update_heartbeat_index_refresh(heartbeat_path: Path, notes: list[dict]) -> None:
    state = load_json(heartbeat_path)
    cold = ensure_cold_state(state)
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    today = date.today().isoformat()
    review_due_count = sum(1 for note in notes if note.get("next_review") and note["next_review"] <= today)
    state_counts = {"hot": 0, "warm": 0, "cold": 0, "dormant": 0}
    for note in notes:
        note_state = note.get("state")
        if note_state in state_counts:
            state_counts[note_state] += 1
    cold["lastIndexRefresh"] = now
    cold["lastReviewSweep"] = now
    cold["reviewDueCount"] = review_due_count
    cold["stateCounts"] = state_counts
    cold["lastSummary"] = f"Rebuilt cold-memory index and tags from {len(notes)} note(s); {review_due_count} review(s) due."
    save_json(heartbeat_path, state)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--heartbeat-path", default=None)
    args = parser.parse_args()

    memory_root = resolve_memory_root(args.memory_root)
    heartbeat_path = Path(args.heartbeat_path).resolve() if args.heartbeat_path else DEFAULT_HEARTBEAT_PATH
    index_path = memory_root / "index.md"
    tags_path = memory_root / "tags.json"

    if not memory_root.exists():
        print(f"memory root not found: {memory_root}")
        return 1

    notes = [parse_note(path, memory_root) for path in note_paths(memory_root)]
    backup_if_exists(index_path)
    backup_if_exists(tags_path)
    index_path.write_text(build_index(notes), encoding="utf-8")
    tags_path.write_text(build_tags(notes), encoding="utf-8")
    update_heartbeat_index_refresh(heartbeat_path, notes)
    print(f"Rebuilt index.md and tags.json from {len(notes)} note(s).")
    print(f"memory root: {memory_root}")
    print(f"heartbeat: {heartbeat_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
