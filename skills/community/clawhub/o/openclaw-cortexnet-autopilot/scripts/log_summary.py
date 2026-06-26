#!/usr/bin/env python3
"""Summarize autopilot run logs for quick inspection."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not path.exists():
        return rows
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            rows.append(obj)
    return rows


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Summarize OpenClaw autopilot logs")
    p.add_argument("--log-dir", default="./logs", help="Log directory")
    p.add_argument("--tail-rounds", type=int, default=5, help="How many latest rounds to print in text mode")
    p.add_argument("--json", action="store_true", help="Output JSON summary")
    return p.parse_args()


def trim_message(value: Any, max_len: int = 120) -> str:
    text = str(value or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def build_recent_rounds(rows: List[Dict[str, Any]], tail: int) -> List[Dict[str, Any]]:
    count = max(0, int(tail))
    if count == 0:
        return []
    items = rows[-count:]
    return [
        {
            "round_id": item.get("round_id"),
            "status": item.get("status"),
            "tool_used": item.get("tool_used"),
            "commit_status": item.get("commit_status"),
            "message": trim_message(item.get("message")),
        }
        for item in items
    ]


def main() -> int:
    args = parse_args()
    log_dir = Path(args.log_dir).resolve()
    round_path = log_dir / "round_reports.jsonl"
    runner_path = log_dir / "openclaw_runner.log"
    pause_path = log_dir / "PAUSED_REASON.txt"

    rounds = load_jsonl(round_path)
    events = load_jsonl(runner_path)

    status_counter = Counter()
    tool_counter = Counter()
    commit_counter = Counter()
    for row in rounds:
        status_counter[str(row.get("status", "unknown"))] += 1
        tool_counter[str(row.get("tool_used", "none"))] += 1
        commit_counter[str(row.get("commit_status", "unknown"))] += 1

    gate_counter = Counter()
    cli_call_fail_reason_counter = Counter()
    cli_switch_reason_counter = Counter()
    cli_init_fail_reason_counter = Counter()
    timeout_reason_counter = Counter()
    for ev in events:
        if ev.get("event") == "audit.fail":
            gate = str(ev.get("gate", "none"))
            gate_counter[gate] += 1
        if ev.get("event") == "cli.call_failed":
            reason = str(ev.get("reason", "unknown"))
            cli_call_fail_reason_counter[reason] += 1
        if ev.get("event") == "cli.switch":
            reason = str(ev.get("reason", "unknown"))
            cli_switch_reason_counter[reason] += 1
        if ev.get("event") == "cli.init.failed":
            reason = str(ev.get("reason", "unknown"))
            cli_init_fail_reason_counter[reason] += 1
        if ev.get("event") == "cli.finish" and bool(ev.get("terminated", False)):
            reason = str(ev.get("reason", "unknown"))
            timeout_reason_counter[reason] += 1

    latest_round = rounds[-1] if rounds else {}
    latest_pause = pause_path.read_text(encoding="utf-8").strip() if pause_path.exists() else ""
    recent_rounds = build_recent_rounds(rounds, args.tail_rounds)

    summary = {
        "log_dir": str(log_dir),
        "rounds_total": len(rounds),
        "status_counts": dict(status_counter),
        "tool_counts": dict(tool_counter),
        "commit_status_counts": dict(commit_counter),
        "audit_fail_gate_counts": dict(gate_counter),
        "cli_call_failed_reason_counts": dict(cli_call_fail_reason_counter),
        "cli_switch_reason_counts": dict(cli_switch_reason_counter),
        "cli_init_fail_reason_counts": dict(cli_init_fail_reason_counter),
        "terminated_reason_counts": dict(timeout_reason_counter),
        "latest_round": latest_round,
        "recent_rounds": recent_rounds,
        "paused_reason_present": pause_path.exists(),
        "paused_reason": latest_pause,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print("OpenClaw Log Summary")
    print(f"- log_dir: {summary['log_dir']}")
    print(f"- rounds_total: {summary['rounds_total']}")
    print(f"- status_counts: {summary['status_counts']}")
    print(f"- tool_counts: {summary['tool_counts']}")
    print(f"- commit_status_counts: {summary['commit_status_counts']}")
    print(f"- audit_fail_gate_counts: {summary['audit_fail_gate_counts']}")
    print(f"- cli_call_failed_reason_counts: {summary['cli_call_failed_reason_counts']}")
    print(f"- cli_switch_reason_counts: {summary['cli_switch_reason_counts']}")
    print(f"- cli_init_fail_reason_counts: {summary['cli_init_fail_reason_counts']}")
    print(f"- terminated_reason_counts: {summary['terminated_reason_counts']}")
    if latest_round:
        print(
            "- latest_round: "
            f"status={latest_round.get('status')} "
            f"tool={latest_round.get('tool_used')} "
            f"commit={latest_round.get('commit_status')} "
            f"message={latest_round.get('message')}"
        )
    if recent_rounds:
        print(f"- recent_rounds(last={len(recent_rounds)}):")
        for item in recent_rounds:
            print(
                "  "
                f"#{item.get('round_id')} "
                f"status={item.get('status')} "
                f"tool={item.get('tool_used')} "
                f"commit={item.get('commit_status')} "
                f"msg={item.get('message')}"
            )
    if latest_pause:
        print("- paused_reason:")
        for line in latest_pause.splitlines():
            print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
