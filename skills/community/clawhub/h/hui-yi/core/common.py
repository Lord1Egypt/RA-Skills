#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import hashlib
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent


def detect_workspace_root(script_dir: Path) -> Path:
    skill_root = script_dir.parent
    if (skill_root / "SKILL.md").exists() and (skill_root / "manifest.yaml").exists():
        if skill_root.parent.name == "skills":
            return skill_root.parent.parent
        if skill_root.name == "hui-yi" and skill_root.parent.name == "temp":
            workspace_candidate = skill_root.parent.parent
            if (workspace_candidate / "skills").exists() or (workspace_candidate / "openclaw.json").exists():
                return workspace_candidate
        return skill_root
    return script_dir.parents[2]


WORKSPACE_ROOT = detect_workspace_root(SCRIPT_DIR)
DEFAULT_MEMORY_ROOT = WORKSPACE_ROOT / "memory" / "cold"
DEFAULT_HEARTBEAT_PATH = WORKSPACE_ROOT / "memory" / "heartbeat-state.json"
SKIP_MARKDOWN = {"index.md", "retrieval-log.md", "_template.md"}
TEXT_FALLBACK_ENCODINGS = ["utf-8", "utf-8-sig", "gb18030", "cp936"]
DEFAULT_SESSION_SIGNALS = {
    "current_session_hits": 0,
    "recent_session_hits": 0,
    "cross_session_repeat_count": 0,
    "consecutive_session_count": 0,
    "last_activated": None,
}
DEFAULT_INTERVAL_DAYS = 1
REVIEW_LADDER = [1, 2, 4, 7, 15, 30, 60]
STRENGTH_RISK_FACTOR = {"weak": 1.08, "normal": 1.0, "strong": 0.78}


def resolve_path(value: str | Path, base: Path | None = None) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    base_dir = base or Path.cwd()
    return (base_dir / candidate).resolve()


def resolve_memory_root(arg: str | None, default: Path = DEFAULT_MEMORY_ROOT) -> Path:
    if arg:
        return resolve_path(arg)
    return default


def load_json(path: Path, default: dict | list | None = None):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {} if default is None else default


def save_json(path: Path, data: dict | list) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_text_fallback(path: Path) -> str:
    last_error: Exception | None = None
    for encoding in TEXT_FALLBACK_ENCODINGS:
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            last_error = exc
            continue
    if last_error:
        raise last_error
    return path.read_text(encoding="utf-8", errors="replace")


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    value = value.strip()
    if not value or value == "-":
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        pass
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_heading_value(text: str, heading: str) -> str | None:
    pattern = rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        return None
    block = match.group(1)
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- "):
            value = stripped[2:].strip()
            return value or None
        return stripped
    return None


def parse_review_metric(text: str, key: str, default: int = 0) -> int:
    match = re.search(r"^## Review cadence\s*$(.*?)^(?:## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return default
    block = match.group(1)
    metric = re.search(rf"^-\s*{re.escape(key)}\s*:\s*(\d+)\s*$", block, re.MULTILINE)
    return int(metric.group(1)) if metric else default


def parse_section_metric(text: str, heading: str, key: str, default: int = 0) -> int:
    match = re.search(rf"^## {re.escape(heading)}\s*$(.*?)^(?:## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return default
    block = match.group(1)
    metric = re.search(rf"^-\s*{re.escape(key)}\s*:\s*(\d+)\s*$", block, re.MULTILINE)
    return int(metric.group(1)) if metric else default


def parse_metric_block(text: str, heading: str, keys: list[str], defaults: dict[str, int] | None = None) -> dict[str, int]:
    defaults = defaults or {}
    return {key: parse_section_metric(text, heading, key, defaults.get(key, 0)) for key in keys}


def parse_section_value(text: str, heading: str, key: str) -> str | None:
    match = re.search(rf"^## {re.escape(heading)}\s*$(.*?)^(?:## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return None
    block = match.group(1)
    metric = re.search(rf"^-\s*{re.escape(key)}\s*:\s*(.+?)\s*$", block, re.MULTILINE)
    return metric.group(1).strip() if metric else None


def note_file_path(memory_root: Path, note: dict) -> Path:
    """Resolve a note path and enforce the memory_root sandbox.

    tags.json is metadata, not authority. Reject absolute paths and parent
    traversal so poisoned metadata cannot make Hui-Yi read/write outside
    memory/cold/.
    """
    raw = str(note.get("path", "") or "").replace("\\", "/").strip()
    if not raw:
        raise ValueError("note path is empty")
    candidate = Path(raw)
    if candidate.is_absolute():
        raise ValueError(f"absolute note paths are not allowed: {raw}")
    parts = candidate.parts
    if parts[:2] == ("memory", "cold"):
        candidate = Path(*parts[2:]) if len(parts) > 2 else Path("")
    if not candidate.parts or any(part in {"..", ""} for part in candidate.parts):
        raise ValueError(f"unsafe note path outside memory root: {raw}")
    root = memory_root.resolve()
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"note path escapes memory root: {raw}") from exc
    return resolved


def session_fingerprint(session_key: str) -> str:
    """Stable non-reversible session identifier for local dedupe metadata."""
    digest = hashlib.sha256(session_key.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:16]}"


def normalize_signal_history(history: object) -> list[str]:
    """Hash legacy raw session ids in signal_history entries.

    v1.2.8 switched new entries to sha256 fingerprints. This migration keeps
    dedupe semantics while scrubbing older raw session-key prefixes the next
    time a note receives a signal.
    """
    if not isinstance(history, list):
        return []
    normalized: list[str] = []
    for item in history:
        value = str(item)
        parts = value.split("|", 3)
        if parts and parts[0] and not parts[0].startswith("sha256:"):
            parts[0] = session_fingerprint(parts[0])
            value = "|".join(parts)
        normalized.append(value)
    return normalized


def load_tags_payload(memory_root: Path) -> dict:
    tags_path = memory_root / "tags.json"
    if not tags_path.exists():
        return {"_meta": {"version": 5}, "notes": []}
    data = load_json(tags_path, default={"_meta": {"version": 5}, "notes": []})
    return data if isinstance(data, dict) else {"_meta": {"version": 5}, "notes": []}


def normalized_session_signals(note: dict) -> dict:
    raw = note.get("session_signals") if isinstance(note.get("session_signals"), dict) else {}
    merged = dict(DEFAULT_SESSION_SIGNALS)
    merged.update({k: raw.get(k, v) for k, v in DEFAULT_SESSION_SIGNALS.items()})
    return merged


def parse_session_signals(text: str) -> dict:
    signals = dict(DEFAULT_SESSION_SIGNALS)
    signals["current_session_hits"] = parse_section_metric(text, "Session signals", "current_session_hits", 0)
    signals["recent_session_hits"] = parse_section_metric(text, "Session signals", "recent_session_hits", 0)
    signals["cross_session_repeat_count"] = parse_section_metric(text, "Session signals", "cross_session_repeat_count", 0)
    signals["consecutive_session_count"] = parse_section_metric(text, "Session signals", "consecutive_session_count", 0)
    signals["last_activated"] = parse_section_value(text, "Session signals", "last_activated")
    return signals


def repetition_signal(note: dict, today: date | None = None) -> float:
    today = today or date.today()
    signals = normalized_session_signals(note)
    current_hits = max(0, int(signals.get("current_session_hits", 0) or 0))
    recent_hits = max(0, int(signals.get("recent_session_hits", 0) or 0))
    cross_repeat = max(0, int(signals.get("cross_session_repeat_count", 0) or 0))
    consecutive = max(0, int(signals.get("consecutive_session_count", 0) or 0))
    last_activated = parse_date(signals.get("last_activated"))

    score = 0.0
    score += min(current_hits / 3.0, 1.0) * 0.40
    score += min(recent_hits / 5.0, 1.0) * 0.25
    score += min(cross_repeat / 4.0, 1.0) * 0.20
    score += min(consecutive / 3.0, 1.0) * 0.15

    if last_activated:
        age = max(0, (today - last_activated).days)
        if age <= 1:
            score += 0.10
        elif age <= 3:
            score += 0.05

    return max(0.0, min(score, 1.0))


def bump_session_signal(note: dict, today: date | None = None, source: str = "session_repeat") -> dict:
    today = today or date.today()
    signals = normalized_session_signals(note)
    signals["current_session_hits"] = max(0, int(signals.get("current_session_hits", 0) or 0)) + 1
    signals["recent_session_hits"] = max(0, int(signals.get("recent_session_hits", 0) or 0)) + 1
    if source in {"session_repeat", "cross_session_repeat"}:
        signals["cross_session_repeat_count"] = max(0, int(signals.get("cross_session_repeat_count", 0) or 0)) + 1
    last_activated = parse_date(signals.get("last_activated"))
    if last_activated and (today - last_activated) <= timedelta(days=2):
        signals["consecutive_session_count"] = max(1, int(signals.get("consecutive_session_count", 0) or 0)) + 1
    else:
        signals["consecutive_session_count"] = 1
    signals["last_activated"] = today.isoformat()
    note["session_signals"] = signals
    return signals


def replace_or_insert_section_metrics(text: str, heading: str, values: dict[str, object]) -> str:
    rendered = "\n".join(f"- {key}: {value}" for key, value in values.items())
    block = f"## {heading}\n{rendered}\n\n"
    pattern = re.compile(rf"(^## {re.escape(heading)}\s*$\n)(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    if not text.endswith("\n"):
        text += "\n"
    return text + "\n" + block


def extract_notes_list(payload: dict | list | object) -> list[dict]:
    if isinstance(payload, dict):
        notes = payload.get("notes", [])
        return notes if isinstance(notes, list) else []
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    return []


def memory_strength(note: dict, default_interval_days: int = DEFAULT_INTERVAL_DAYS) -> str:
    review = note.get("review") if isinstance(note.get("review"), dict) else {}
    interval_days = int(review.get("interval_days", default_interval_days) or default_interval_days)
    retrieval_count = int(review.get("retrieval_count", 0) or 0)
    reinforcement_count = int(review.get("reinforcement_count", 0) or 0)
    review_success = int(review.get("review_success", 0) or 0)
    state = str(note.get("state", "cold"))

    if (
        reinforcement_count >= 3
        or retrieval_count >= 5
        or (review_success >= 4 and interval_days >= 15)
        or (state == "hot" and review_success >= 3)
    ):
        return "strong"
    if reinforcement_count >= 1 or retrieval_count >= 2 or review_success >= 2:
        return "normal"
    return "weak"


def run_main_with_argv(main_func, argv: list[str]) -> int:
    original_argv = sys.argv
    try:
        sys.argv = argv
        return int(main_func())
    finally:
        sys.argv = original_argv
