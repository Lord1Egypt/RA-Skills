#!/usr/bin/env python3
"""Record and inspect the real TeamCreate result for a resumable run."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from artifact_contract import native_team_bootstrap_identity, validate_team_bootstrap_identity


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z-]+)*)?$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,80}$")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bootstrap_path(run_dir: Path) -> Path:
    return run_dir / "team-bootstrap.json"


def record(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    if not run_dir.is_dir():
        raise ValueError("run_dir_not_found")
    if not RUN_ID_RE.fullmatch(args.run_id):
        raise ValueError("invalid_run_id")
    if not SEMVER_RE.fullmatch(args.team_version):
        raise ValueError("invalid_team_version")
    team_name = args.team_name.strip()
    if len(team_name) < 3 or team_name.casefold() in {"unknown", "none", "null"}:
        raise ValueError("team_name_missing")
    output = bootstrap_path(run_dir)
    if output.exists():
        raise ValueError("team_bootstrap_already_exists")
    payload = {
        **native_team_bootstrap_identity(args.team_version),
        "run_id": args.run_id,
        "client_scope": args.client_scope,
        "team_version": args.team_version,
        "host": "workbuddy",
        "status": "team_created",
        "team_name": team_name,
        "host_mode": args.host_mode,
        "created_at": now(),
    }
    if args.team_create_task_id:
        payload["team_create_task_id"] = args.team_create_task_id.strip()
    validate_team_bootstrap_identity(payload,args.team_version,args.run_id,args.client_scope)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "team_bootstrap_recorded", "output": output.name, "team_name": team_name}, ensure_ascii=False))
    return 0


def inspect(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).expanduser().resolve()
    output = bootstrap_path(run_dir)
    if not output.is_file():
        print(json.dumps({"status": "team_bootstrap_missing", "reason": "team_bootstrap_missing"}, ensure_ascii=False))
        return 2
    try:
        payload = read_json(output)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "team_bootstrap_invalid", "reason": type(exc).__name__}, ensure_ascii=False))
        return 2
    errors: list[str] = []
    try:
        validate_team_bootstrap_identity(payload,args.team_version,args.run_id,args.client_scope)
    except ValueError as exc:
        errors.append(str(exc))
    if payload.get("status") != "team_created":
        errors.append("status_invalid")
    if payload.get("run_id") != args.run_id:
        errors.append("run_id_mismatch")
    if payload.get("team_version") != args.team_version:
        errors.append("team_version_mismatch")
    if not str(payload.get("team_name", "")).strip():
        errors.append("team_name_missing")
    if errors:
        print(json.dumps({"status": "team_bootstrap_invalid", "reasons": errors}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "team_bootstrap_verified", "run_id": args.run_id, "team_name": payload["team_name"]}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="记录和检查真实 TeamCreate 建团结果")
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--run-dir", required=True)
    rec.add_argument("--run-id", required=True)
    rec.add_argument("--team-version", required=True)
    rec.add_argument("--client-scope", required=True)
    rec.add_argument("--team-name", required=True)
    rec.add_argument("--host-mode", choices=["interactive", "non_interactive", "unknown"], default="unknown")
    rec.add_argument("--team-create-task-id")
    chk = sub.add_parser("inspect")
    chk.add_argument("--run-dir", required=True)
    chk.add_argument("--run-id", required=True)
    chk.add_argument("--team-version", required=True)
    chk.add_argument("--client-scope", required=True)
    args = parser.parse_args()
    try:
        return record(args) if args.command == "record" else inspect(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "team_bootstrap_invalid", "reason": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
