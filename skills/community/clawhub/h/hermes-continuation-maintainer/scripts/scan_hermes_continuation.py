#!/usr/bin/env python3
"""Scan Hermes logs/state for premature text-stop continuation stalls.

The source is intentionally ASCII-only. Chinese phrases are represented with
Unicode escapes so the script survives Windows/WSL console encoding differences.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timedelta
import json
import re
import sqlite3
from pathlib import Path
from typing import Any


TS_FORMAT = "%Y-%m-%d %H:%M:%S,%f"
TURN_RE = re.compile(
    r"(?P<ts>\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+).*?"
    r"conversation turn: session=(?P<session>\S+) .*? msg='(?P<msg>.*)'"
)
END_RE = re.compile(
    r"(?P<ts>\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+).*?Turn ended: "
    r"reason=text_response\(finish_reason=stop\).*?"
    r"api_calls=(?P<api>\d+)/(?P<api_max>\d+) .*?"
    r"tool_turns=(?P<tools>\d+) .*?"
    r"response_len=(?P<response_len>\d+) session=(?P<session>\S+)"
)


CONTINUE_WORDS = {
    "continue",
    "\u7ee7\u7eed",  # ji xu
    "\u7ee7\u7eed\u5427",  # ji xu ba
}

ASKS_USER_MARKERS = (
    "from you",
    "need your",
    "please provide",
    "please clarify",
    "clarify",
    "which file",
    "what should",
    "can you provide",
    "\u9700\u8981\u4f60",  # xu yao ni
    "\u8bf7\u63d0\u4f9b",  # qing ti gong
    "\u8bf7\u786e\u8ba4",  # qing que ren
)
FINAL_MARKERS = (
    "done",
    "completed",
    "finished",
    "implemented",
    "all tests passed",
    "\u5df2\u5b8c\u6210",  # yi wan cheng
    "\u53ef\u4ee5\u5b89\u5168",  # ke yi an quan
)
EXECUTION_USER_MARKERS = (
    "continue",
    "fix",
    "update",
    "implement",
    "run",
    "test",
    "read",
    "inspect",
    "check",
    "debug",
    "diagnose",
    "write",
    "verify",
    "patch",
    "\u7ee7\u7eed",
    "\u6267\u884c",
    "\u4fee",
    "\u66f4\u65b0",
    "\u8bfb",
    "\u770b",
    "\u67e5",
    "\u5b9e\u73b0",
    "\u5b8c\u6210",
    "\u8dd1",
    "\u6d4b\u8bd5",
    "\u9a8c\u8bc1",
    "\u89e3\u51b3",
    "\u5904\u7406",
    "\u5b9a\u4f4d",
    "\u6392\u67e5",
    "\u4efb\u52a1",
)
FUTURE_MARKERS = (
    "i will",
    "i'll",
    "i need to",
    "i still need",
    "next",
    "now ",
    "then ",
    "let me",
    "i should",
    "\u6211\u4f1a",
    "\u6211\u5c06",
    "\u6211\u9700\u8981",
    "\u6211\u5148",
    "\u6211\u518d",
    "\u73b0\u5728",
    "\u4e0b\u9762",
    "\u63a5\u4e0b\u6765",
    "\u4e0b\u4e00\u6b65",
    "\u968f\u540e",
    "\u7136\u540e",
    "\u5148",
    "\u518d",
)
ACTION_MARKERS = (
    "read",
    "inspect",
    "check",
    "run",
    "test",
    "execute",
    "update",
    "write",
    "patch",
    "fix",
    "implement",
    "verify",
    "add",
    "smoke",
    "compile",
    "\u8bfb\u53d6",
    "\u67e5\u770b",
    "\u786e\u8ba4",
    "\u8fd0\u884c",
    "\u6d4b\u8bd5",
    "\u6267\u884c",
    "\u66f4\u65b0",
    "\u5199",
    "\u6539",
    "\u4fee",
    "\u5b9e\u73b0",
    "\u9a8c\u8bc1",
    "\u6dfb\u52a0",
    "\u52a0\u8f7d",
    "\u5b9a\u4f4d",
    "\u63a8\u8fdb",
)
CONTINUATION_REGEXES = (
    re.compile(r"\bneed(?:s)? more\b"),
    re.compile(r"\bstill need\b"),
    re.compile(r"\bneed to (?:continue|inspect|check|read|run|test|update|fix|implement|verify)\b"),
    re.compile(r"\bmore (?:runtime|continuation|context|work|implementation|tests?|verification)\b"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="/root/.hermes/logs/agent.log")
    parser.add_argument("--db", default="/root/.hermes/state.db")
    parser.add_argument("--since-minutes", type=int, default=360)
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--format", choices=("json", "text"), default="json")
    parser.add_argument(
        "--ascii-output",
        action="store_true",
        help="Escape non-ASCII log snippets in output.",
    )
    return parser.parse_args()


def parse_ts(raw: str) -> datetime | None:
    try:
        return datetime.strptime(raw, TS_FORMAT)
    except ValueError:
        return None


def is_recent(raw_ts: str, cutoff: datetime | None) -> bool:
    if cutoff is None:
        return True
    ts = parse_ts(raw_ts)
    return ts is not None and ts >= cutoff


def classify(text: str, user_msg: str = "", has_tools: bool = True) -> str:
    stripped = (text or "").strip()
    lowered = stripped.lower()
    if not stripped:
        return "empty"

    asks_user = (
        any(marker in lowered or marker in stripped for marker in ASKS_USER_MARKERS)
        or "?" in stripped
        or "\uff1f" in stripped
    )
    if asks_user:
        return "asks_user"

    if len(stripped) > 600:
        return "final_or_summary"

    if any(marker in lowered or marker in stripped for marker in FINAL_MARKERS):
        return "final_or_summary"

    user = (user_msg or "").lower()
    execution_user = any(marker in user or marker in user_msg for marker in EXECUTION_USER_MARKERS)

    if any(regex.search(lowered) for regex in CONTINUATION_REGEXES):
        return "continuation_candidate" if execution_user or has_tools else "review"

    has_future = any(marker in lowered or marker in stripped for marker in FUTURE_MARKERS)
    has_action = any(marker in lowered or marker in stripped for marker in ACTION_MARKERS)
    if has_future and has_action and (execution_user or has_tools):
        return "continuation_candidate"

    chinese_continue_markers = (
        "\u8fd8\u9700\u8981",  # hai xu yao
        "\u7ee7\u7eed",  # ji xu
        "\u63a5\u4e0b\u6765",  # jie xia lai
        "\u4e0b\u4e00\u6b65",  # xia yi bu
        "\u8fd8\u8981",  # hai yao
    )
    if any(marker in stripped for marker in chinese_continue_markers):
        return "continuation_candidate" if execution_user or has_tools else "review"

    return "review"


def fetch_assistant_stops(db_path: str, sessions: set[str], limit: int) -> list[dict[str, Any]]:
    path = Path(db_path)
    if not path.exists() or not sessions:
        return []

    con = sqlite3.connect(path)
    try:
        out: list[dict[str, Any]] = []
        for session in sorted(sessions):
            rows = con.execute(
                """
                select id, session_id, length(content), finish_reason, content
                from messages
                where session_id=? and role='assistant' and finish_reason='stop'
                order by id desc limit ?
                """,
                (session, limit),
            ).fetchall()
            for mid, sid, size, finish_reason, content in rows:
                out.append(
                    {
                        "id": mid,
                        "session": sid,
                        "length": size,
                        "finish_reason": finish_reason,
                        "content": (content or "")[:700],
                    }
                )
        return out
    finally:
        con.close()


def scan(log_path: str, db_path: str, since_minutes: int, limit: int) -> dict[str, Any]:
    log = Path(log_path)
    if not log.exists():
        raise SystemExit(f"log not found: {log}")

    cutoff = datetime.now() - timedelta(minutes=since_minutes) if since_minutes > 0 else None
    turns: list[dict[str, Any]] = []
    ends: list[dict[str, Any]] = []

    for line in log.read_text(errors="ignore").splitlines():
        match = TURN_RE.search(line)
        if match and is_recent(match.group("ts"), cutoff):
            turns.append(match.groupdict())
            continue

        match = END_RE.search(line)
        if match and is_recent(match.group("ts"), cutoff):
            item = match.groupdict()
            item["api_calls"] = int(item.pop("api"))
            item["api_max"] = int(item.pop("api_max"))
            item["tool_turns"] = int(item.pop("tools"))
            item["response_len"] = int(item["response_len"])
            ends.append(item)

    recent_turns = turns[-limit:]
    recent_ends = ends[-limit:]
    continue_turns = [
        turn
        for turn in recent_turns
        if (turn.get("msg") or "").strip().lower() in CONTINUE_WORDS
    ]

    sessions = sorted({turn["session"] for turn in continue_turns} | {end["session"] for end in recent_ends})
    assistant_stops = fetch_assistant_stops(db_path, set(sessions), limit)

    latest_user_by_session = {}
    for turn in recent_turns:
        latest_user_by_session[turn["session"]] = turn.get("msg") or ""

    tool_turns_by_session = defaultdict(int)
    for end in recent_ends:
        tool_turns_by_session[end["session"]] = max(
            tool_turns_by_session[end["session"]],
            int(end.get("tool_turns") or 0),
        )

    classified = []
    for item in assistant_stops:
        user_msg = latest_user_by_session.get(item["session"], "")
        has_tools = tool_turns_by_session.get(item["session"], 0) > 0
        classification = classify(item["content"], user_msg=user_msg, has_tools=has_tools)
        if classification != "final_or_summary" or item["length"] <= 240:
            classified.append(
                {
                    **item,
                    "classification": classification,
                    "user_msg": user_msg,
                    "has_tools_in_recent_end": has_tools,
                }
            )

    return {
        "log": str(log),
        "db": db_path,
        "since_minutes": since_minutes,
        "recent_continue_turns": continue_turns[-20:],
        "recent_text_response_ends": recent_ends[-20:],
        "classified_assistant_stops": classified[:limit],
        "counts": {
            "recent_turns": len(recent_turns),
            "recent_continue_turns": len(continue_turns),
            "recent_text_response_ends": len(recent_ends),
            "continuation_candidates": sum(
                1 for item in classified if item["classification"] == "continuation_candidate"
            ),
            "asks_user": sum(1 for item in classified if item["classification"] == "asks_user"),
            "review": sum(1 for item in classified if item["classification"] == "review"),
        },
    }


def ascii_snippet(text: str) -> str:
    return text.encode("unicode_escape", errors="backslashreplace").decode("ascii")


def print_text(result: dict[str, Any], ascii_output: bool = False) -> None:
    counts = result["counts"]
    print("Hermes continuation scan")
    print(f"log={result['log']}")
    print(f"db={result['db']}")
    print(f"since_minutes={result['since_minutes']}")
    print(
        "counts: "
        f"continue_turns={counts['recent_continue_turns']} "
        f"text_stop_ends={counts['recent_text_response_ends']} "
        f"candidates={counts['continuation_candidates']} "
        f"asks_user={counts['asks_user']} "
        f"review={counts['review']}"
    )
    for item in result["classified_assistant_stops"][:10]:
        content = " ".join((item.get("content") or "").split())
        if ascii_output:
            content = ascii_snippet(content)
        print(
            f"- {item['classification']} session={item['session']} "
            f"id={item['id']} len={item['length']} text={content[:180]}"
        )


def main() -> None:
    args = parse_args()
    result = scan(args.log, args.db, args.since_minutes, args.limit)
    if args.format == "text":
        print_text(result, ascii_output=args.ascii_output)
    else:
        print(json.dumps(result, ensure_ascii=bool(args.ascii_output), indent=2))


if __name__ == "__main__":
    main()
