#!/usr/bin/env python3
"""Append one execution step to an hh.ru application packet."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

VALID_STATUSES = {"passed", "failed", "blocked"}
VALID_EFFECTS = {"inspected", "drafted", "submitted", "blocked", "skipped"}


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def recompute_summary(payload: dict) -> None:
    steps = payload.get("steps", [])
    issue_keys: list[str] = []
    effects: list[str] = []
    submitted = False
    failed = False
    blocked = False
    for step in steps:
        issue_keys.extend(step.get("issue_keys", []))
        effect = str(step.get("effect", "")).strip()
        if effect:
            effects.append(effect)
        if effect == "submitted":
            submitted = True
        if step.get("status") == "failed":
            failed = True
        if step.get("status") == "blocked":
            blocked = True

    payload["summary"] = {
        "status": "failed" if failed else "blocked" if blocked else "submitted" if submitted else "draft",
        "effects": dedupe(effects),
        "submitted": submitted,
        "issue_keys": dedupe(issue_keys),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Packet JSON to update.")
    parser.add_argument("--step-id", required=True, help="Stable step identifier.")
    parser.add_argument("--action", required=True, help="What was attempted.")
    parser.add_argument("--expected", required=True, help="Expected browser behavior.")
    parser.add_argument("--actual", required=True, help="Observed browser behavior.")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES), help="Step status.")
    parser.add_argument("--effect", required=True, choices=sorted(VALID_EFFECTS), help="Operational effect of the step.")
    parser.add_argument("--note", default="", help="Optional note.")
    parser.add_argument("--issue-key", action="append", default=[], help="Repeatable issue key.")
    parser.add_argument("--screenshot", default="", help="Relative path to screenshot artifact.")
    parser.add_argument("--snapshot-json", default="", help="Relative path to page snapshot artifact.")
    parser.add_argument("--console-log", default="", help="Relative path to console log.")
    parser.add_argument("--outcome-url", default="", help="Optional final URL after the step.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    payload = load_manifest(manifest_path)

    step_id = args.step_id.strip()
    existing_ids = {step.get("step_id") for step in payload.get("steps", [])}
    if step_id in existing_ids:
        raise SystemExit(f"Step '{step_id}' already exists in {manifest_path}")

    step = {
        "step_id": step_id,
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "action": args.action.strip(),
        "expected": args.expected.strip(),
        "actual": args.actual.strip(),
        "status": args.status,
        "effect": args.effect,
        "note": args.note.strip(),
        "issue_keys": dedupe(args.issue_key),
        "outcome_url": args.outcome_url.strip(),
        "artifacts": {
            "screenshot": args.screenshot.strip(),
            "snapshot_json": args.snapshot_json.strip(),
            "console_log": args.console_log.strip(),
        },
    }

    payload.setdefault("steps", []).append(step)
    recompute_summary(payload)
    save_manifest(manifest_path, payload)
    print(manifest_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
