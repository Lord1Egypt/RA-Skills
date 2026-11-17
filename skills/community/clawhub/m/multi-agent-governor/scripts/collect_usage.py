#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from _common import load_manifest, parse_iso, save_json


TOKEN_KEYS = ["input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens"]


def session_started_at(rollout_path: Path) -> datetime | None:
    with rollout_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "session_meta" and event.get("timestamp"):
                return parse_iso(event["timestamp"])
    return None


def thread_usage(rollout_path: Path, start: datetime, end: datetime) -> dict[str, int]:
    totals = {key: 0 for key in TOKEN_KEYS}
    calls = 0
    with rollout_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            timestamp = event.get("timestamp")
            if not timestamp:
                continue
            current = parse_iso(timestamp)
            if not start <= current <= end:
                continue
            payload = event.get("payload", {})
            if event.get("type") != "event_msg" or payload.get("type") != "token_count":
                continue
            usage = payload.get("info", {}).get("last_token_usage")
            if not usage:
                continue
            calls += 1
            for key in TOKEN_KEYS:
                totals[key] += int(usage.get(key, 0) or 0)
    totals["calls"] = calls
    totals["fresh_tokens"] = totals["input_tokens"] - totals["cached_input_tokens"] + totals["output_tokens"]
    return totals


def main() -> None:
    parser = argparse.ArgumentParser(description="Optional Codex adapter for governed-run token usage.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--thread-id", action="append", default=[])
    parser.add_argument("--state-db", default=str(Path.home() / ".codex" / "state_5.sqlite"))
    parser.add_argument(
        "--include-thread-titles",
        action="store_true",
        help="Include local task titles in output. Titles are omitted by default for privacy.",
    )
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    manifest_path, manifest = load_manifest(args.manifest)
    start = parse_iso(manifest["created_at"])
    end = parse_iso(manifest["completed_at"]) if manifest.get("completed_at") else datetime.now(timezone.utc)
    thread_ids = list(args.thread_id)
    if manifest.get("main_thread_id"):
        thread_ids.append(manifest["main_thread_id"])
    thread_ids.extend(agent["thread_id"] for agent in manifest.get("agents", []) if agent.get("thread_id"))
    thread_ids = list(dict.fromkeys(thread_ids))
    agent_thread_ids = {
        agent["thread_id"] for agent in manifest.get("agents", []) if agent.get("thread_id")
    }

    connection = sqlite3.connect(Path(args.state_db).expanduser())
    per_thread = []
    totals = {key: 0 for key in TOKEN_KEYS + ["calls", "fresh_tokens"]}
    for thread_id in thread_ids:
        columns = "rollout_path, title" if args.include_thread_titles else "rollout_path"
        row = connection.execute(f"SELECT {columns} FROM threads WHERE id = ?", (thread_id,)).fetchone()
        if not row:
            per_thread.append({"thread_id": thread_id, "error": "thread not found"})
            continue
        rollout_path = Path(row[0])
        usage_start = start
        if thread_id in agent_thread_ids:
            child_start = session_started_at(rollout_path)
            if child_start:
                usage_start = max(start, child_start)
        usage = thread_usage(rollout_path, usage_start, end)
        entry = {
            "thread_id": thread_id,
            "usage_started_at": usage_start.isoformat(),
            **usage,
        }
        if args.include_thread_titles:
            entry["title"] = row[1]
        per_thread.append(entry)
        for key in totals:
            totals[key] += usage[key]

    duration = max(0.0, (end - start).total_seconds())
    metrics = {
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
        "duration_seconds": duration,
        "agent_count": len(manifest.get("agents", [])),
        "threads": per_thread,
        "totals": totals,
        "cached_input_ratio": (totals["cached_input_tokens"] / totals["input_tokens"]) if totals["input_tokens"] else 0.0,
    }
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    if args.write:
        manifest["metrics"] = metrics
        save_json(manifest_path, manifest)


if __name__ == "__main__":
    main()
