#!/usr/bin/env python3
"""Block a WorkBuddy lead turn until the expected Agent return files are valid."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--return-dir", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--expected", required=True, help="Comma-separated Agent IDs")
    parser.add_argument("--contract", choices=["member", "delivery_review"], default="member")
    parser.add_argument(
        "--return-file", action="append", default=[], metavar="AGENT_ID=RELATIVE_PATH",
        help="Override the default <agent_id>.return.json path; the resolved file must remain under return-dir",
    )
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--poll-seconds", type=float, default=2.0)
    parser.add_argument(
        "--invalid-grace-seconds", type=float, default=5.0,
        help="Fail once an existing invalid return stays byte-stable for this many seconds",
    )
    return parser.parse_args()


def read_return(path: Path, run_id: str, agent_id: str, contract: str, require_attempt_id: bool = False) -> tuple[bool, str, dict]:
    if not path.is_file():
        return False, "missing", {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return False, f"invalid_json:{type(exc).__name__}", {}
    if not isinstance(payload, dict):
        return False, "root_not_object", {}
    if payload.get("run_id") != run_id:
        return False, "run_id_mismatch", payload
    if payload.get("agent_id") != agent_id:
        return False, "agent_id_mismatch", payload
    if payload.get("return_status") != "completed":
        return False, f"status:{payload.get('return_status', 'missing')}", payload
    if not str(payload.get("returned_at") or "").strip():
        return False, "returned_at_missing", payload
    if not str(payload.get("contribution_summary") or "").strip():
        return False, "contribution_summary_missing", payload
    if contract == "member":
        if not re.fullmatch(r"[0-9a-f]{64}", str(payload.get("handoff_sha256") or "")):
            return False, "handoff_sha256_missing_or_invalid", payload
        attempt_id = str(payload.get("attempt_id") or "").strip()
        if require_attempt_id and not attempt_id:
            return False, "attempt_id_missing", payload
        if attempt_id and path.name != f"{attempt_id}.return.json":
            return False, "attempt_id_path_mismatch", payload
        if not payload.get("response"):
            return False, "response_missing", payload
    else:
        if payload.get("review_status") not in {"passed", "conditional_pass", "rejected"}:
            return False, "review_status_invalid", payload
        if not str(payload.get("review_attempt_id") or "").strip():
            return False, "review_attempt_id_missing", payload
        if not str(payload.get("report_revision") or "").strip():
            return False, "report_revision_missing", payload
        if not str(payload.get("reviewed_manifest_sha256") or "").strip():
            return False, "reviewed_manifest_sha256_missing", payload
        if not isinstance(payload.get("reviewed_artifacts"), list) or not payload.get("reviewed_artifacts"):
            return False, "reviewed_artifacts_missing", payload
    return True, "completed", payload


def parse_return_files(raw_items: list[str], return_dir: Path, expected: list[str]) -> tuple[dict[str, Path], set[str]]:
    mapping = {agent_id: return_dir / f"{agent_id}.return.json" for agent_id in expected}
    overridden: set[str] = set()
    for raw in raw_items:
        if "=" not in raw:
            raise ValueError("return_file_invalid")
        agent_id, relative = (part.strip() for part in raw.split("=", 1))
        if agent_id not in mapping or not relative:
            raise ValueError("return_file_invalid")
        candidate = (return_dir / relative).resolve()
        try:
            candidate.relative_to(return_dir)
        except ValueError as exc:
            raise ValueError("return_file_outside_return_dir") from exc
        mapping[agent_id] = candidate
        overridden.add(agent_id)
    return mapping, overridden


def main() -> int:
    args = parse_args()
    expected = [item.strip() for item in args.expected.split(",") if item.strip()]
    if not expected or len(expected) != len(set(expected)):
        print(json.dumps({"status": "invalid_arguments", "expected": expected}, ensure_ascii=False))
        return 3

    return_dir = Path(args.return_dir).expanduser().resolve()
    return_dir.mkdir(parents=True, exist_ok=True)
    try:
        return_files, overridden = parse_return_files(args.return_file, return_dir, expected)
    except ValueError as exc:
        print(json.dumps({"status": "invalid_arguments", "reason": str(exc)}, ensure_ascii=False))
        return 3
    deadline = time.monotonic() + max(1, args.timeout)
    last_state: dict[str, str] = {}
    invalid_seen: dict[str, tuple[tuple[str, int, int], float]] = {}

    while True:
        completed: list[str] = []
        states: dict[str, str] = {}
        for agent_id in expected:
            ok, state, _ = read_return(
                return_files[agent_id], args.run_id, agent_id, args.contract,
                require_attempt_id=agent_id in overridden and args.contract == "member",
            )
            states[agent_id] = state
            if ok:
                completed.append(agent_id)

        if len(completed) == len(expected):
            print(json.dumps({
                "status": "all_agent_returns_received",
                "run_id": args.run_id,
                "return_dir": str(return_dir),
                "expected": expected,
                "completed": completed,
                "verified_files": {agent_id: str(return_files[agent_id]) for agent_id in expected},
                "verified_at": datetime.now(timezone.utc).isoformat(),
            }, ensure_ascii=False))
            return 0

        stable_invalid: dict[str, str] = {}
        now = time.monotonic()
        for agent_id in expected:
            path = return_files[agent_id]
            state = states[agent_id]
            if state == "missing" or agent_id in completed or not path.is_file():
                invalid_seen.pop(agent_id, None)
                continue
            stat = path.stat()
            signature = (state, stat.st_size, stat.st_mtime_ns)
            previous = invalid_seen.get(agent_id)
            if previous is None or previous[0] != signature:
                invalid_seen[agent_id] = (signature, now)
            elif now - previous[1] >= max(0.0, args.invalid_grace_seconds):
                stable_invalid[agent_id] = state
        if stable_invalid:
            print(json.dumps({
                "status": "agent_return_invalid",
                "run_id": args.run_id,
                "invalid": stable_invalid,
                "completed": completed,
                "retry_policy": "new_attempt_required_do_not_overwrite",
            }, ensure_ascii=False))
            return 4

        if states != last_state:
            print(json.dumps({
                "status": "waiting_for_agent_returns",
                "run_id": args.run_id,
                "completed": completed,
                "pending": [agent_id for agent_id in expected if agent_id not in completed],
                "states": states,
            }, ensure_ascii=False), flush=True)
            last_state = states

        if now >= deadline:
            print(json.dumps({
                "status": "collaboration_wait_timeout",
                "run_id": args.run_id,
                "completed": completed,
                "pending": [agent_id for agent_id in expected if agent_id not in completed],
                "states": states,
            }, ensure_ascii=False))
            return 2
        time.sleep(max(0.2, args.poll_seconds))


if __name__ == "__main__":
    sys.exit(main())
