#!/usr/bin/env python3
"""Validate OpenClaw R&D task status transitions and closure gates."""

import argparse
import json
import sys
from typing import Dict, List, Tuple

MASTER_ALLOWED = {
    "待开始": {"进行中"},
    "进行中": {"已完成", "已阻塞"},
    "已阻塞": {"进行中"},
    "已完成": set(),
}

SUBTASK_ALLOWED = {
    "待开始": {"进行中"},
    "进行中": {"已完成", "待开始"},
    "已完成": set(),
}


def validate_transition(task_type: str, from_status: str, to_status: str) -> Tuple[bool, str]:
    allowed = MASTER_ALLOWED if task_type == "master" else SUBTASK_ALLOWED
    if from_status not in allowed:
        return False, f"unknown from_status: {from_status}"
    if to_status in allowed[from_status]:
        return True, "ok"
    return False, f"invalid transition for {task_type}: {from_status} -> {to_status}"


def validate_snapshot(data: Dict) -> List[str]:
    errs: List[str] = []

    required_keys = ["master", "coding", "review", "testing", "bug_subtasks", "ui_changed", "ui_evidence_present"]
    for key in required_keys:
        if key not in data:
            errs.append(f"missing key: {key}")

    if errs:
        return errs

    for k in ["coding", "review", "testing"]:
        if data[k] not in SUBTASK_ALLOWED:
            errs.append(f"invalid status for {k}: {data[k]}")

    if data["master"] not in MASTER_ALLOWED:
        errs.append(f"invalid status for master: {data['master']}")

    for idx, bug in enumerate(data["bug_subtasks"], start=1):
        if bug not in SUBTASK_ALLOWED:
            errs.append(f"invalid BUG subtask #{idx} status: {bug}")

    if data["ui_changed"] and not data["ui_evidence_present"]:
        errs.append("ui_changed=true but ui_evidence_present=false; merge must be blocked")

    closure_ready = (
        data["coding"] == "已完成"
        and data["review"] == "已完成"
        and data["testing"] == "已完成"
        and all(status == "已完成" for status in data["bug_subtasks"])
    )

    if data["master"] == "已完成" and not closure_ready:
        errs.append("master cannot be 已完成 before coding/review/testing/all BUG subtasks are 已完成")

    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OpenClaw task state machine rules")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_transition = subparsers.add_parser("transition", help="validate one state transition")
    p_transition.add_argument("--task-type", choices=["master", "subtask"], required=True)
    p_transition.add_argument("--from-status", required=True)
    p_transition.add_argument("--to-status", required=True)

    p_snapshot = subparsers.add_parser("snapshot", help="validate full task snapshot JSON")
    p_snapshot.add_argument("--file", required=True, help="Path to JSON file")

    args = parser.parse_args()

    if args.command == "transition":
        ok, msg = validate_transition(args.task_type, args.from_status, args.to_status)
        if ok:
            print("OK:", msg)
            return 0
        print("ERROR:", msg)
        return 1

    with open(args.file, "r", encoding="utf-8") as f:
        data = json.load(f)

    errors = validate_snapshot(data)
    if errors:
        print("ERROR: snapshot validation failed")
        for err in errors:
            print("-", err)
        return 1

    print("OK: snapshot validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
