#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path


SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "grocery" / "sessions"
SESSIONS_FILE = SESSIONS_DIR / "sessions.json"
MAX_INPUT_TOKENS = 20_000
MAX_CACHE_READ = 40_000
MAX_JSONL_LINES = 120


def load_sessions() -> dict:
    if not SESSIONS_FILE.exists():
        return {}
    try:
        return json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def session_line_count(session_file: Path) -> int:
    try:
        with session_file.open("r", encoding="utf-8") as handle:
            return sum(1 for _ in handle)
    except FileNotFoundError:
        return 0


def should_prune(meta: dict) -> bool:
    input_tokens = int(meta.get("inputTokens") or 0)
    cache_read = int(meta.get("cacheRead") or 0)
    session_path = Path(str(meta.get("sessionFile") or ""))
    line_count = session_line_count(session_path) if session_path else 0
    return (
        input_tokens >= MAX_INPUT_TOKENS
        or cache_read >= MAX_CACHE_READ
        or line_count >= MAX_JSONL_LINES
    )


def archive_session_files(entries: dict) -> None:
    timestamp = int(time.time())
    archive_dir = SESSIONS_DIR / f"archive-auto-{timestamp}"
    archive_dir.mkdir(parents=True, exist_ok=True)

    for meta in entries.values():
        session_path = Path(str(meta.get("sessionFile") or ""))
        if session_path.exists():
            shutil.move(str(session_path), str(archive_dir / session_path.name))

    for backup in SESSIONS_DIR.glob("*.bak.*"):
        shutil.move(str(backup), str(archive_dir / backup.name))


def main() -> int:
    sessions = load_sessions()
    if not sessions:
        return 0

    prune_needed = any(should_prune(meta) for meta in sessions.values())
    if not prune_needed:
        return 0

    archive_session_files(sessions)
    SESSIONS_FILE.write_text("{}\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
