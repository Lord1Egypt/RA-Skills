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
from datetime import date, datetime, timedelta
from pathlib import Path

from core.common import DEFAULT_HEARTBEAT_PATH, DEFAULT_MEMORY_ROOT, WORKSPACE_ROOT, load_json, memory_strength, normalize_signal_history, session_fingerprint, save_json, resolve_path, resolve_memory_root as common_memory_root
from core.safe_fs import atomic_write_bytes, atomic_write_text, check_directory, iter_files, preflight_files, read_bytes, read_text, safe_exists

SKIP = {"index.md", "retrieval-log.md", "_template.md"}
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INTERVAL_DAYS = 1  # Ebbinghaus: first review at +1 day while memory is still fresh
DEFAULT_IMPORTANCE = "medium"
DEFAULT_STATE = "cold"
VALID_IMPORTANCE = {"high", "medium", "low"}
VALID_STATE = {"hot", "warm", "cold", "dormant"}
VALID_CONFIDENCE = {"high", "medium", "low"}


def resolve_memory_root(arg: str | None) -> Path:
    return common_memory_root(arg)


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
    lines = read_text(path).splitlines()
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
    summary = " ".join(value for value in summary_lines if value and value != "-") or title
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
    for path in iter_files(memory_root, "*.md"):
        if path.name.lower() in SKIP:
            continue
        paths.append(path)
    return sorted(paths)


def retain_runtime_metadata(notes: list[dict], previous: object) -> None:
    """Rebuild derived fields without erasing real activation/dedup evidence.

    Only exact unambiguous paths may retain index-only data. Note content still
    owns counters, summaries, dates and the review ladder. Explicit lifecycle
    metadata is retained so superseded facts or fixtures do not reappear merely
    because the index was rebuilt.
    """
    old_notes = previous.get("notes", []) if isinstance(previous, dict) else []
    by_path: dict[str, list[dict]] = {}
    for old in old_notes if isinstance(old_notes, list) else []:
        if isinstance(old, dict) and isinstance(old.get("path"), str):
            by_path.setdefault(old["path"], []).append(old)
    for note in notes:
        matches = by_path.get(note["path"], [])
        if len(matches) != 1:
            continue
        old = matches[0]
        if isinstance(old.get("last_session_key"), str) and old["last_session_key"]:
            key = old["last_session_key"]
            note["last_session_key"] = key if key.startswith("sha256:") else session_fingerprint(key)
        if isinstance(old.get("signal_history"), list):
            note["signal_history"] = normalize_signal_history(old["signal_history"])[-20:]
        aliases = old.get("aliases")
        if isinstance(aliases, list):
            note["aliases"] = list(dict.fromkeys(x.strip() for x in aliases if isinstance(x, str) and x.strip()))
        for field in ("active", "fixture", "is_fixture"):
            if isinstance(old.get(field), bool):
                note[field] = old[field]
        for field in ("status", "superseded_by"):
            if isinstance(old.get(field), str) and old[field].strip():
                note[field] = old[field].strip()


def backup_if_exists(path: Path) -> None:
    if safe_exists(path):
        atomic_write_bytes(path.with_suffix(path.suffix + ".bak"), read_bytes(path))


def preflight_rebuild(memory_root: Path, heartbeat_path: Path) -> None:
    check_directory(heartbeat_path.parent)
    preflight_files(
        memory_root / "index.md", memory_root / "index.md.bak",
        memory_root / "tags.json", memory_root / "tags.json.bak", heartbeat_path,
    )
    note_paths(memory_root)


def build_index(notes: list[dict]) -> str:
    lines = ["# Cold Memory Index", "", "## Entries", ""]
    notes_sorted = sorted(notes, key=lambda n: (n.get("updated") or "", n.get("importance") == "high"), reverse=True)
    for note in notes_sorted:
        lines.append(f"- `{note['path'].removeprefix('memory/cold/')}` — {note['summary']}")
        lines.append(f"  - type: {note['type']}")
        lines.append(f"  - importance: {note['importance']}")
        lines.append(f"  - state: {note['state']}")
        if note.get("fixture") is True or note.get("is_fixture") is True:
            lines.append("  - fixture: true (excluded from ordinary recall)")
        if note.get("status"):
            lines.append(f"  - status: {note['status']}")
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
    heartbeat_path = resolve_path(args.heartbeat_path) if args.heartbeat_path else memory_root.parent / "heartbeat-state.json"
    index_path = memory_root / "index.md"
    tags_path = memory_root / "tags.json"

    if not safe_exists(memory_root, kind="directory"):
        print(f"memory root not found: {memory_root}")
        return 1

    preflight_rebuild(memory_root, heartbeat_path)
    notes = [parse_note(path, memory_root) for path in note_paths(memory_root)]
    retain_runtime_metadata(notes, load_json(tags_path))
    backup_if_exists(index_path)
    backup_if_exists(tags_path)
    atomic_write_text(index_path, build_index(notes))
    atomic_write_text(tags_path, build_tags(notes))
    update_heartbeat_index_refresh(heartbeat_path, notes)
    print(f"Rebuilt index.md and tags.json from {len(notes)} note(s).")
    print(f"memory root: {memory_root}")
    print(f"heartbeat: {heartbeat_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
