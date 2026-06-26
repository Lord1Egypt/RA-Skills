#!/usr/bin/env python3
"""
memory-oracle: checkpoint.py
Pre-compaction emergency save. Called by OpenClaw's memoryFlush hook.
Dumps all hot-tier context (SESSION-STATE.md, recent conversation) to SQLite.

Usage:
  checkpoint.py                          # Auto-detect session state
  checkpoint.py --text "emergency text"  # Save specific text
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
from init_db import load_settings, content_hash, generate_id, utcnow

SETTINGS = load_settings()


def get_db():
    import sqlite3
    db_path = os.path.expanduser(SETTINGS["paths"]["db"])
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")
    return conn


def checkpoint_session_state():
    """Read SESSION-STATE.md and save its contents."""
    ws = os.path.expanduser(SETTINGS["paths"]["workspace"])
    session_state_path = os.path.join(ws, "SESSION-STATE.md")

    if not os.path.exists(session_state_path):
        return None

    with open(session_state_path, "r", encoding="utf-8") as f:
        return f.read()


def save_checkpoint(conn, text: str) -> int:
    """Parse text and store facts with checkpoint source tag."""
    now = utcnow().isoformat()
    saved = 0

    # Split into meaningful chunks
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if len(line) < 10 or line.startswith("#"):
            continue
        # Remove markdown markers
        clean = line.lstrip("-*• ").strip()
        if len(clean) < 10:
            continue

        chash = content_hash(clean)

        # Skip if already exists
        existing = conn.execute(
            "SELECT id FROM facts WHERE content_hash=? AND status='active'",
            (chash,),
        ).fetchone()
        if existing:
            # Bump score on existing fact — it survived to checkpoint, it's important
            conn.execute(
                "UPDATE facts SET score = MIN(score * 1.2, ?), updated_at=? WHERE id=?",
                (SETTINGS["scoring"]["max_score"], now, existing[0]),
            )
            continue

        fid = generate_id("chk")
        conn.execute(
            """INSERT INTO facts (id, type, content, content_hash, base_importance,
               score, status, source, confidence, created_at, updated_at)
               VALUES (?, 'insight', ?, ?, 1.5, 1.5, 'active', 'checkpoint', 0.7, ?, ?)""",
            (fid, clean, chash, now, now),
        )
        saved += 1

    conn.commit()
    return saved


def main():
    parser = argparse.ArgumentParser(description="Memory Oracle — Checkpoint")
    parser.add_argument("--text", type=str, default=None, help="Text to checkpoint")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    conn = get_db()
    if conn is None:
        print("WARNING: Database not available, checkpoint skipped.", file=sys.stderr)
        sys.exit(0)  # Exit 0 — don't block compaction

    text = args.text
    if not text:
        text = checkpoint_session_state()

    if not text:
        result = {"saved": 0, "note": "nothing to checkpoint"}
    else:
        saved = save_checkpoint(conn, text)
        result = {"saved": saved, "source": "arg" if args.text else "SESSION-STATE.md"}

    conn.close()

    if args.json:
        print(json.dumps(result))
    else:
        print(f"Checkpoint: {result['saved']} facts saved")


if __name__ == "__main__":
    main()
