#!/usr/bin/env python3
"""
session-recall: Lightweight session transcript search for OpenClaw agents.

Scans JSONL session transcripts and returns file paths + line numbers
so the calling agent can read relevant context itself.

Usage:
  session-recall list [--agent AGENT] [--start TIME] [--end TIME] [--limit N] [--offset N]
  session-recall search QUERY [--agent AGENT] [--start TIME] [--end TIME] [--limit N] [--offset N]
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

SESSIONS_BASE = Path.home() / ".openclaw" / "agents"


def parse_time(s: str) -> float:
    """Parse a time specification into a Unix timestamp.

    Supports:
      - Relative durations: 30m, 6h, 2d, 1w, 3mo (minutes/hours/days/weeks/months)
      - Absolute dates: 2026-03-01, 2026-03-01T14:00, 03-01
      - Absolute datetimes: "2026-03-01 14:00"
      - Keywords: today, yesterday
    """
    s = s.strip().lower()
    now = time.time()

    # Keywords
    if s == "today":
        t = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return t.timestamp()
    if s == "yesterday":
        t = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        return t.timestamp()

    # Relative duration: 30m, 6h, 2d, 1w, 3mo
    m = re.match(r"^(\d+)\s*(mo|[mhdw])$", s)
    if m:
        n, unit = int(m.group(1)), m.group(2)
        if unit == "m":
            return now - n * 60
        if unit == "h":
            return now - n * 3600
        if unit == "d":
            return now - n * 86400
        if unit == "w":
            return now - n * 7 * 86400
        if unit == "mo":
            return now - n * 30 * 86400

    # Absolute: YYYY-MM-DD or YYYY-MM-DDTHH:MM or YYYY-MM-DD HH:MM
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s, fmt).timestamp()
        except ValueError:
            continue

    # Short absolute: MM-DD (assume current year)
    m = re.match(r"^(\d{1,2})-(\d{1,2})$", s)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        try:
            t = datetime.now().replace(month=month, day=day, hour=0, minute=0, second=0, microsecond=0)
            return t.timestamp()
        except ValueError:
            pass

    raise ValueError(
        f"Cannot parse time: {s!r}. "
        "Use relative (30m, 6h, 2d, 1w, 3mo), "
        "absolute (2026-03-01, 03-01, 2026-03-01T14:00), "
        "or keywords (today, yesterday)."
    )


def discover_agents() -> list[str]:
    """List all agent directories that have a sessions/ subdirectory."""
    if not SESSIONS_BASE.is_dir():
        return []
    return sorted(
        d.name
        for d in SESSIONS_BASE.iterdir()
        if d.is_dir() and (d / "sessions").is_dir()
    )


def get_session_files(
    agent: str,
    start_ts: float | None = None,
    end_ts: float | None = None,
) -> list[Path]:
    """Get session JSONL files for an agent, sorted by mtime descending.

    Filters by file mtime:
      - start_ts: only files modified at or after this time
      - end_ts: only files modified at or before this time
    """
    sessions_dir = SESSIONS_BASE / agent / "sessions"
    if not sessions_dir.is_dir():
        return []
    files = sorted(
        sessions_dir.glob("*.jsonl"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if start_ts is not None:
        files = [f for f in files if f.stat().st_mtime >= start_ts]
    if end_ts is not None:
        files = [f for f in files if f.stat().st_mtime <= end_ts]
    return files


def extract_text_from_content(content) -> str:
    """Extract human-readable text from message content."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return " ".join(parts)
    return ""


def get_first_user_message(path: Path) -> tuple[str, int]:
    """Get the first user message text and its line number."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") != "message":
                    continue
                msg = rec.get("message", {})
                if msg.get("role") != "user":
                    continue
                text = extract_text_from_content(msg.get("content", ""))
                # Strip metadata envelope, get the actual user text
                lines = text.split("\n")
                for l in reversed(lines):
                    l = l.strip()
                    if l and not l.startswith("```") and not l.startswith("{") and not l.startswith('"'):
                        m = re.match(r"^\[.*?\]\s*\w+:\s*(.+)", l)
                        if m:
                            return m.group(1)[:120], lineno
                        if not l.startswith("Conversation info") and not l.startswith("Sender "):
                            return l[:120], lineno
                return text[:120], lineno
    except Exception:
        pass
    return "", 0


def count_turns(path: Path) -> tuple[int, str, str]:
    """Count user+assistant message turns. Return (count, first_ts, last_ts)."""
    count = 0
    first_ts = ""
    last_ts = ""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") != "message":
                    continue
                msg = rec.get("message", {})
                role = msg.get("role", "")
                if role in ("user", "assistant"):
                    count += 1
                    ts = rec.get("timestamp") or msg.get("timestamp")
                    if ts:
                        if isinstance(ts, (int, float)):
                            ts_str = datetime.fromtimestamp(
                                ts / 1000 if ts > 1e12 else ts, tz=timezone.utc
                            ).strftime("%m-%d %H:%M")
                        else:
                            ts_str = str(ts)[:16].replace("T", " ")
                        if not first_ts:
                            first_ts = ts_str
                        last_ts = ts_str
    except Exception:
        pass
    return count, first_ts, last_ts


def cmd_list(args):
    """List sessions with previews."""
    agents = [args.agent] if args.agent else discover_agents()
    start_ts = parse_time(args.start) if args.start else None
    end_ts = parse_time(args.end) if args.end else None
    limit = args.limit or 20
    offset = args.offset or 0
    results = []

    for agent in agents:
        files = get_session_files(agent, start_ts, end_ts)
        for f in files:
            turns, first_ts, last_ts = count_turns(f)
            if turns == 0:
                continue
            preview, _ = get_first_user_message(f)
            results.append({
                "agent": agent,
                "file": str(f),
                "turns": turns,
                "time_range": f"{first_ts} ~ {last_ts}" if first_ts else "unknown",
                "preview": preview,
                "mtime": f.stat().st_mtime,
            })

    # Sort by mtime descending
    results.sort(key=lambda r: r["mtime"], reverse=True)
    total = len(results)
    results = results[offset : offset + limit]

    if not results:
        print("No sessions found.")
        return

    if offset > 0 or total > offset + limit:
        print(f"Showing {offset + 1}-{offset + len(results)} of {total} sessions\n")

    for r in results:
        print(f"{r['file']}  [{r['time_range']}]  {r['turns']} turns  \"{r['preview']}\"")
        if len(agents) > 1:
            print(f"  agent: {r['agent']}")


def cmd_search(args):
    """Search session transcripts for a query string."""
    query = args.query.lower()
    agents = [args.agent] if args.agent else discover_agents()
    start_ts = parse_time(args.start) if args.start else None
    end_ts = parse_time(args.end) if args.end else None
    limit = args.limit or 30
    offset = args.offset or 0
    results = []

    for agent in agents:
        files = get_session_files(agent, start_ts, end_ts)
        for fpath in files:
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    for lineno, line in enumerate(f, 1):
                        if query not in line.lower():
                            continue
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            rec = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if rec.get("type") != "message":
                            continue
                        msg = rec.get("message", {})
                        role = msg.get("role", "")
                        if role not in ("user", "assistant"):
                            continue
                        text = extract_text_from_content(msg.get("content", ""))
                        text_lower = text.lower()
                        idx = text_lower.find(query)
                        if idx == -1:
                            continue
                        # Extract snippet around match
                        start = max(0, idx - 40)
                        end = min(len(text), idx + len(query) + 80)
                        snippet = text[start:end].replace("\n", " ").strip()
                        if start > 0:
                            snippet = "..." + snippet
                        if end < len(text):
                            snippet = snippet + "..."

                        ts = rec.get("timestamp") or msg.get("timestamp")
                        ts_str = ""
                        if ts:
                            if isinstance(ts, (int, float)):
                                ts_str = datetime.fromtimestamp(
                                    ts / 1000 if ts > 1e12 else ts, tz=timezone.utc
                                ).strftime("%m-%d %H:%M")
                            else:
                                ts_str = str(ts)[:16].replace("T", " ")

                        results.append({
                            "file": str(fpath),
                            "line": lineno,
                            "role": role,
                            "timestamp": ts_str,
                            "snippet": snippet,
                            "agent": agent,
                            "mtime": fpath.stat().st_mtime,
                        })
            except Exception:
                continue

    # Sort by file mtime desc, then line number
    results.sort(key=lambda r: (-r["mtime"], r["line"]))
    total = len(results)
    results = results[offset : offset + limit]

    if not results:
        print(f"No matches for \"{args.query}\".")
        return

    if offset > 0 or total > offset + limit:
        print(f"Showing {offset + 1}-{offset + len(results)} of {total} matches\n")

    for r in results:
        agent_prefix = f"[{r['agent']}] " if not args.agent else ""
        print(f"{r['file']}:{r['line']}  [{r['timestamp']}] {agent_prefix}{r['role']}: {r['snippet']}")


def cmd_agents(args):
    """List available agent IDs."""
    agents = discover_agents()
    if not agents:
        print("No agents found.")
        return
    print("Available agents:")
    for a in agents:
        sessions_dir = SESSIONS_BASE / a / "sessions"
        count = len(list(sessions_dir.glob("*.jsonl")))
        print(f"  {a}  ({count} session files)")


def main():
    parser = argparse.ArgumentParser(
        description="Search OpenClaw session transcripts",
        prog="session-recall",
    )
    sub = parser.add_subparsers(dest="command")

    # Shared time/pagination arguments
    def add_common_args(p):
        p.add_argument(
            "--agent",
            help="Agent ID to search. Run 'session-recall agents' to list available IDs. "
            "Omit to search all agents.",
        )
        p.add_argument(
            "--start",
            help="Start of time window (inclusive). Accepts relative durations (30m, 6h, 2d, 1w, 3mo), "
            "absolute dates (2026-03-01, 03-01), datetimes (2026-03-01T14:00), "
            "or keywords (today, yesterday).",
        )
        p.add_argument(
            "--end",
            help="End of time window (inclusive). Same formats as --start. "
            "Omit to include everything up to now.",
        )
        p.add_argument("--limit", type=int, help="Max results to return (default: 20 for list, 30 for search)")
        p.add_argument("--offset", type=int, help="Skip this many results for pagination (default: 0)")

    # list
    p_list = sub.add_parser("list", help="List sessions with previews")
    add_common_args(p_list)

    # search
    p_search = sub.add_parser("search", help="Search transcripts by keyword")
    p_search.add_argument("query", help="Search query (case-insensitive substring match)")
    add_common_args(p_search)

    # agents
    sub.add_parser("agents", help="List available agent IDs and their session counts")

    args = parser.parse_args()
    if args.command == "list":
        cmd_list(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "agents":
        cmd_agents(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
