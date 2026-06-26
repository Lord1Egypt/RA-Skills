#!/usr/bin/env python3
"""
OpenMem - compress.py
Import and inspect OpenClaw session files for memory compression.

This script handles the mechanical part: reading JSONL session files and
extracting conversation text. The actual summarization/compression is done
by the AI agent using mem.py to store the results.

Usage:
  compress.py pending [--sessions-dir PATH]    List sessions not yet compressed
  compress.py read SESSION_ID [--sessions-dir PATH]
                                               Print session messages as text
  compress.py mark-done SESSION_ID [--db PATH] Mark session as compressed
  compress.py history [--db PATH]              Show compression history
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

DEFAULT_SESSIONS_DIR = Path(
    os.environ.get(
        "OPENMEM_SESSIONS_DIR",
        "~/.openclaw/agents/main/sessions"
    )
).expanduser()

DEFAULT_DB = Path(
    os.environ.get("OPENMEM_DB", "~/.openclaw/workspace/memory/openmem.db")
).expanduser()


# ---------------------------------------------------------------------------
# Session reading
# ---------------------------------------------------------------------------

def read_session_messages(session_file: Path) -> list[dict]:
    """Extract role+content messages from an OpenClaw JSONL session file."""
    messages = []
    try:
        with open(session_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if obj.get("type") != "message":
                    continue

                msg = obj.get("message", {})
                role = msg.get("role")
                if role not in ("user", "assistant"):
                    continue

                # Content can be a string or list of content blocks
                content = msg.get("content", "")
                if isinstance(content, list):
                    parts = []
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            parts.append(block.get("text", ""))
                    content = "\n".join(parts)

                content = content.strip()
                if not content:
                    continue

                # Strip internal sender metadata injected by OpenClaw
                content = _strip_sender_metadata(content)
                if not content:
                    continue

                messages.append({
                    "role": role,
                    "content": content,
                    "timestamp": obj.get("timestamp"),
                })
    except (OSError, PermissionError) as e:
        print(f"ERROR: cannot read {session_file}: {e}", file=sys.stderr)

    return messages


def _strip_sender_metadata(text: str) -> str:
    """Remove the sender metadata block OpenClaw prepends to user messages."""
    # Pattern: ```json\n{...}\n```\n\n[timestamp] actual message
    import re
    text = re.sub(
        r"^Sender \(untrusted metadata\):\s*```json\s*\{.*?\}\s*```\s*\n",
        "",
        text,
        flags=re.DOTALL
    )
    # Strip leading timestamp like "[Wed 2026-04-08 21:59 CDT] "
    text = re.sub(r"^\[[^\]]+\]\s*", "", text)
    return text.strip()


def list_session_files(sessions_dir: Path) -> list[Path]:
    """List all main session JSONL files (excludes checkpoints)."""
    if not sessions_dir.exists():
        return []
    files = []
    for p in sessions_dir.glob("*.jsonl"):
        # Skip checkpoint files (contain .checkpoint. in name)
        if ".checkpoint." not in p.name:
            files.append(p)
    return sorted(files, key=lambda p: p.stat().st_mtime)


def session_id_from_path(path: Path) -> str:
    return path.stem  # filename without .jsonl


# ---------------------------------------------------------------------------
# Compression tracking (stored in openmem DB)
# ---------------------------------------------------------------------------

def open_tracking_db(db_path: Path):
    """Open the openmem DB just for compression tracking."""
    import sqlite3
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(db_path))
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS compressed_sessions (
            session_id   TEXT PRIMARY KEY,
            session_file TEXT NOT NULL,
            compressed_at INTEGER NOT NULL,
            memory_count  INTEGER NOT NULL DEFAULT 0
        )
    """)
    db.commit()
    return db


def get_compressed_ids(db) -> set:
    rows = db.execute("SELECT session_id FROM compressed_sessions").fetchall()
    return {r["session_id"] for r in rows}


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_pending(args):
    sessions_dir = args.sessions_dir or DEFAULT_SESSIONS_DIR
    db = open_tracking_db(args.db)
    done = get_compressed_ids(db)

    files = list_session_files(sessions_dir)
    pending = [f for f in files if session_id_from_path(f) not in done]

    if not pending:
        print("All sessions have been compressed.")
        return

    print(f"Pending sessions ({len(pending)}):\n")
    for f in pending:
        sid = session_id_from_path(f)
        mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(f.stat().st_mtime))
        size_kb = f.stat().st_size // 1024
        # Count messages (parse each line to avoid false string matches)
        msg_count = 0
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    try:
                        if json.loads(line).get("type") == "message":
                            msg_count += 1
                    except json.JSONDecodeError:
                        pass
        except OSError:
            pass
        print(f"  {sid}")
        print(f"    modified: {mtime}  size: {size_kb}KB  messages: ~{msg_count}")
        print()

    print(f"To read a session:")
    print(f"  compress.py read <session-id>")
    print(f"\nAfter compressing, mark it done:")
    print(f"  compress.py mark-done <session-id>")


def cmd_read(args):
    sessions_dir = args.sessions_dir or DEFAULT_SESSIONS_DIR

    # Accept full UUID or prefix
    session_id = args.session_id
    session_file = sessions_dir / f"{session_id}.jsonl"

    if not session_file.exists():
        # Try prefix match
        matches = list(sessions_dir.glob(f"{session_id}*.jsonl"))
        matches = [m for m in matches if ".checkpoint." not in m.name]
        if len(matches) == 1:
            session_file = matches[0]
            session_id = session_id_from_path(session_file)
        elif len(matches) > 1:
            print(f"ERROR: ambiguous prefix '{session_id}', matches:", file=sys.stderr)
            for m in matches:
                print(f"  {m.name}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"ERROR: session '{session_id}' not found in {sessions_dir}", file=sys.stderr)
            sys.exit(1)

    messages = read_session_messages(session_file)
    if not messages:
        print("(no messages found)")
        return

    if args.json:
        for m in messages:
            print(json.dumps(m))
        return

    print(f"Session: {session_id}")
    print(f"Messages: {len(messages)}\n")
    print("=" * 60)

    for m in messages:
        ts = ""
        if m.get("timestamp"):
            try:
                import datetime
                ts = datetime.datetime.fromisoformat(
                    m["timestamp"].replace("Z", "+00:00")
                ).strftime(" [%Y-%m-%d %H:%M]")
            except Exception:
                pass
        role_label = "USER" if m["role"] == "user" else "AGENT"
        print(f"\n{role_label}{ts}:")
        print(m["content"])

    print("\n" + "=" * 60)
    print("\nCompress this session by reading the above and running:")
    print(f"  mem.py add \"<summary>\" --category insight --source session:{session_id}")
    print(f"  compress.py mark-done {session_id}")


def cmd_mark_done(args):
    db = open_tracking_db(args.db)
    now = int(time.time())
    db.execute(
        """INSERT OR REPLACE INTO compressed_sessions
           (session_id, session_file, compressed_at, memory_count)
           VALUES (?, ?, ?, ?)""",
        (args.session_id, str(args.session_id) + ".jsonl", now, args.memory_count or 0)
    )
    db.commit()
    print(f"OK: marked session {args.session_id} as compressed")


def cmd_history(args):
    db = open_tracking_db(args.db)
    rows = db.execute(
        "SELECT * FROM compressed_sessions ORDER BY compressed_at DESC"
    ).fetchall()

    if not rows:
        print("No sessions compressed yet.")
        return

    if args.json:
        for r in rows:
            print(json.dumps(dict(r)))
        return

    print(f"{'Session ID':<40} {'Compressed At':<20} {'Memories'}")
    print("-" * 70)
    for r in rows:
        ts = time.strftime("%Y-%m-%d %H:%M", time.localtime(r["compressed_at"]))
        print(f"{r['session_id']:<40} {ts:<20} {r['memory_count']}")


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="compress.py", description="OpenMem session compression helper")
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    p.add_argument("--json", action="store_true")

    sub = p.add_subparsers(dest="command", required=True)

    pending = sub.add_parser("pending", help="List sessions not yet compressed")
    pending.add_argument("--sessions-dir", type=Path, dest="sessions_dir")

    read = sub.add_parser("read", help="Print session messages")
    read.add_argument("session_id")
    read.add_argument("--sessions-dir", type=Path, dest="sessions_dir")

    done = sub.add_parser("mark-done", help="Mark a session as compressed")
    done.add_argument("session_id")
    done.add_argument("--memory-count", type=int, default=0, dest="memory_count")

    sub.add_parser("history", help="Show compression history")

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "pending": cmd_pending,
        "read": cmd_read,
        "mark-done": cmd_mark_done,
        "history": cmd_history,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
