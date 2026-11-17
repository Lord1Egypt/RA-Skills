#!/usr/bin/env python3
"""
Session Transcript Adapter — turn extraction for the Auto-Capture pipeline.

Reads the OpenClaw per-agent session store (SQLite) and emits {user, assistant}
turns for auto_capture.py.

WHY SQLITE, NOT *.jsonl:
  OpenClaw migrated session storage to SQLite. The legacy
  ~/.openclaw/agents/<agent>/sessions/*.jsonl files stopped being written
  (last real activity: 2026-09-04 on this host). Reading them would make a
  nightly cron run green while capturing nothing. The authoritative source is
  the per-agent store the CLI itself reads:
      ~/.openclaw/agents/<agent>/agent/openclaw-agent.sqlite
  Messages live in `session_transcript_fts` (text, session_id, role, timestamp)
  and raw events in `transcript_events` (event_json).

Design constraints (inherited from the toolkit):
  * Local-only: writes a JSONL buffer on disk; nothing leaves the machine.
  * Read-only, snapshot-first: opens a COPY of the live DB (WAL-aware) so the
    Gateway's writer is never contended and we never mutate session state.
  * Explicit scope: default = most recent session(s) within a window; never a
    blind full-history dump.
  * Privacy filter: toolResult/tool noise excluded; obvious secrets redacted
    before the turn hits the buffer file.

Usage:
    # Latest active session, last 6 hours
    python3 transcript_adapter.py --hours 6 --out /tmp/turns.jsonl

    # A specific session id, verbose
    python3 transcript_adapter.py --session-id <uuid> --verbose

    # Then:
    python3 auto_capture.py --file /tmp/turns.jsonl --apply --force --no-split
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ─── Config ───────────────────────────────────────────────────────────────────

AGENT = os.environ.get("OPENCLAW_AGENT", "main")
AGENT_DB = Path(os.environ.get(
    "OPENCLAW_AGENT_DB",
    str(Path.home() / ".openclaw" / "agents" / AGENT / "agent"
        / "openclaw-agent.sqlite"),
))

SKIP_MARKERS = {"HEARTBEAT_OK", "NO_REPLY", "[OpenClaw heartbeat poll]"}
MAX_MSG_CHARS = 2000
DEFAULT_OUT = "/tmp/session_turns.jsonl"

SECRET_PATTERNS = [
    re.compile(r"\b(sk-[A-Za-z0-9]{16,})\b"),
    re.compile(r"\b(ghp_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(tk_[a-f0-9]{20,})\b"),
    re.compile(r"\b(AKIA[0-9A-Z]{16})\b"),
    re.compile(r"(?i)\b(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*\S+"),
]


def redact(text: str) -> str:
    for pat in SECRET_PATTERNS:
        text = pat.sub("«redacted»", text)
    return text


# ─── Snapshot the live DB (WAL-aware) ─────────────────────────────────────────


def snapshot_db(db_path: Path) -> Path:
    """Copy the agent store to a temp file so we never touch the live DB.

    Uses SQLite's own backup API when possible (WAL-safe); falls back to a
    file copy including -wal/-shm sidecars.
    """
    if not db_path.exists():
        raise SystemExit(f"❌ agent store not found: {db_path}")

    tmp = Path(tempfile.mkdtemp(prefix="oc-transcript-")) / "snapshot.sqlite"
    try:
        src = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        dst = sqlite3.connect(str(tmp))
        src.backup(dst)
        dst.close()
        src.close()
        return tmp
    except sqlite3.Error:
        shutil.copy2(db_path, tmp)
        for side in ("-wal", "-shm"):
            s = Path(str(db_path) + side)
            if s.exists():
                shutil.copy2(s, str(tmp) + side)
        return tmp


# ─── Turn extraction ──────────────────────────────────────────────────────────


def _clean(text: str) -> str:
    text = (text or "").strip()
    if not text or text in SKIP_MARKERS:
        return ""
    return text[:MAX_MSG_CHARS]


def fetch_rows(conn: sqlite3.Connection, session_id: str | None,
               since_ms: int | None) -> list[tuple]:
    """Pull (role, text, timestamp) rows, oldest first."""
    q = ("SELECT role, text, timestamp FROM session_transcript_fts "
         "WHERE role IN ('user','assistant')")
    params: list = []
    if session_id:
        q += " AND session_id = ?"
        params.append(session_id)
    if since_ms is not None:
        q += " AND timestamp >= ?"
        params.append(since_ms)
    q += " ORDER BY timestamp ASC"
    try:
        return conn.execute(q, params).fetchall()
    except sqlite3.OperationalError as e:
        raise SystemExit(f"❌ cannot read session_transcript_fts: {e}")


def latest_session_id(conn: sqlite3.Connection, since_ms: int | None) -> str | None:
    q = ("SELECT session_id FROM session_transcript_fts "
         "WHERE role IN ('user','assistant')")
    params: list = []
    if since_ms is not None:
        q += " AND timestamp >= ?"
        params.append(since_ms)
    q += " ORDER BY timestamp DESC LIMIT 1"
    row = conn.execute(q, params).fetchone()
    return row[0] if row else None


def rows_to_turns(rows: list[tuple]) -> list[dict]:
    """Pair each user message with the following assistant reply."""
    turns: list[dict] = []
    pending_user: str | None = None
    for role, text, _ts in rows:
        text = _clean(text)
        if not text:
            continue
        if role == "user":
            if pending_user is not None:
                turns.append({"user": pending_user, "assistant": ""})
            pending_user = text
        elif role == "assistant" and pending_user is not None:
            turns.append({"user": pending_user, "assistant": text})
            pending_user = None
    if pending_user is not None:
        turns.append({"user": pending_user, "assistant": ""})
    return turns


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw session store -> {user, assistant} turns.")
    parser.add_argument("--session-id", help="specific session_id (default: latest)")
    parser.add_argument("--hours", type=float, default=6,
                        help="only turns newer than N hours (default 6; 0 = all)")
    parser.add_argument("--max-turns", type=int, default=200,
                        help="cap turns written (default 200)")
    parser.add_argument("--out", default=DEFAULT_OUT,
                        help=f"output JSONL buffer (default: {DEFAULT_OUT})")
    parser.add_argument("--db", default=str(AGENT_DB), help="agent store path")
    parser.add_argument("--no-redact", action="store_true",
                        help="disable secret redaction (not recommended)")
    parser.add_argument("--keep-snapshot", action="store_true",
                        help="keep the temp snapshot for inspection")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    snap = snapshot_db(Path(args.db))
    since_ms = None
    if args.hours and args.hours > 0:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
        since_ms = int(cutoff.timestamp() * 1000)

    conn = sqlite3.connect(str(snap))
    try:
        sid = args.session_id or latest_session_id(conn, since_ms)
        if not sid:
            print("⏭  no session messages in window.")
            return 0
        rows = fetch_rows(conn, sid, since_ms)
        turns = rows_to_turns(rows)
    finally:
        conn.close()
        if not args.keep_snapshot:
            shutil.rmtree(snap.parent, ignore_errors=True)

    if not turns:
        print("⏭  no turns extracted.")
        return 0

    if len(turns) > args.max_turns:
        turns = turns[-args.max_turns:]

    if not args.no_redact:
        for t in turns:
            t["user"] = redact(t["user"])
            t["assistant"] = redact(t["assistant"])

    out = Path(args.out)
    with open(out, "w", encoding="utf-8") as fh:
        for t in turns:
            fh.write(json.dumps(t, ensure_ascii=False) + "\n")

    if args.verbose:
        print(f"   session_id: {sid}")
        print(f"   window: {args.hours}h  rows: {len(rows)}  turns: {len(turns)}")
    print(f"✅ {len(turns)} turn(s) from session {sid[:8]}… -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
