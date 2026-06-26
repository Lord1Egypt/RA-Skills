#!/usr/bin/env python3
"""Audit or repair Feishu group session metadata for OpenClaw agents."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import backup_file, load_roles, write_json


def expected_fields(role: dict[str, Any], group_id: str) -> dict[str, Any]:
    return {
        "channel": "feishu",
        "chatType": "group",
        "displayName": f"feishu:g-{group_id}",
        "subject": group_id,
        "deliveryContext": {
            "channel": "feishu",
            "to": f"chat:{group_id}",
            "accountId": role["accountId"],
        },
        "lastChannel": "feishu",
        "lastTo": f"chat:{group_id}",
        "lastAccountId": role["accountId"],
    }


def apply_expected(session: dict[str, Any], expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        session[key] = value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roles", required=True, help="Path to roles.json")
    parser.add_argument("--group-id", required=True, help="Feishu group id like oc_xxx")
    parser.add_argument(
        "--state-dir",
        default="~/.openclaw",
        help="OpenClaw state dir (default: ~/.openclaw)",
    )
    parser.add_argument("--fix", action="store_true", help="Write fixes back to disk")
    parser.add_argument("--backup", action="store_true", help="Create .bak backups before writing")
    args = parser.parse_args(argv)

    _, roles = load_roles(Path(args.roles).expanduser().resolve())
    state_dir = Path(args.state_dir).expanduser().resolve()
    group_id = args.group_id
    had_issue = False

    print(f"Scanning group sessions for {group_id}")
    print()

    for role in roles:
        agent_id = role["agentId"]
        sessions_path = state_dir / "agents" / agent_id / "sessions" / "sessions.json"
        session_key = f"agent:{agent_id}:feishu:group:{group_id}"

        if not sessions_path.exists():
            had_issue = True
            print(f"[missing] {agent_id}: {sessions_path}")
            continue

        data = json.loads(sessions_path.read_text(encoding="utf-8"))
        session = data.get(session_key)
        if not isinstance(session, dict):
            had_issue = True
            print(f"[missing] {agent_id}: session key {session_key} not found")
            continue

        expected = expected_fields(role, group_id)
        mismatches: list[str] = []
        for key, expected_value in expected.items():
            if session.get(key) != expected_value:
                mismatches.append(key)

        if not mismatches:
            print(f"[ok] {agent_id}: session metadata is healthy")
            continue

        had_issue = True
        print(f"[issue] {agent_id}: mismatched fields -> {', '.join(mismatches)}")

        if args.fix:
            if args.backup:
                backup_file(sessions_path)
            apply_expected(session, expected)
            write_json(sessions_path, data)
            print(f"[fixed] {agent_id}: wrote repaired metadata")

    return 1 if had_issue else 0


if __name__ == "__main__":
    raise SystemExit(main())
