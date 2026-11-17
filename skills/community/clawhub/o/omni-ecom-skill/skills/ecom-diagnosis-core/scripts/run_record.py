#!/usr/bin/env python3
"""2.0 compatibility entry for the authoritative SQLite run journal.

This command no longer maintains a second mutable run.json/events.jsonl ledger.
Initialization creates run-journal.sqlite through host_runtime. ``show`` emits a
derived read-only snapshot; all runtime mutations must use host_runtime.py.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PACKAGE_ROOT / "scripts"))

from artifact_contract import native_run_record_identity, validate_run_record_identity
from host_runtime import Runtime


def emit(value: dict) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def init_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    run_dir = root / args.run_id
    if run_dir.exists():
        raise ValueError("run_directory_exists")
    staging = Path(tempfile.mkdtemp(prefix=f".{args.run_id}.initializing-", dir=root))
    try:
        for name in ("inputs", "outputs", "evidence", "approvals", "artifacts"):
            (staging / name).mkdir()
        runtime = Runtime(staging, args.run_id, args.client_scope)
        try:
            runtime.init(args.package_version, args.task_type)
        finally:
            runtime.close()
        staging.replace(run_dir)
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise
    emit({"status": "PASS", "run_dir": str(run_dir), "run_id": args.run_id,
          "authority": "run-journal.sqlite"})
    return 0


def show(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    runtime = Runtime(run_dir, args.run_id, args.client_scope, read_only=True)
    try:
        identity = runtime.identity()
        status = runtime.status()
        payload = dict(**native_run_record_identity(identity["team_version"]),
                       run_id=identity["run_id"], client_scope=identity["client_scope"],
                       team_version=identity["team_version"], task_type=identity["task_type"],
                       runtime_status=status)
        validate_run_record_identity(payload, identity["team_version"], args.run_id, args.client_scope)
        emit(payload)
        return 0
    finally:
        runtime.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="初始化或查看 omni-ecom 2.0 权威运行账本")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--root", required=True)
    init.add_argument("--run-id", required=True)
    init.add_argument("--client-scope", required=True)
    init.add_argument("--package-version", required=True)
    init.add_argument("--task-type", required=True)
    for name in ("show", "event", "status"):
        item = sub.add_parser(name)
        item.add_argument("--run-dir", required=True)
        item.add_argument("--run-id", required=True)
        item.add_argument("--client-scope", required=True)
        if name == "event":
            for key in ("type", "stage", "actor", "status"):
                item.add_argument(f"--{key}")
            item.add_argument("--details")
        elif name == "status":
            item.add_argument("--status")
    args = parser.parse_args()
    try:
        if args.command == "init":
            return init_run(args)
        if args.command == "show":
            return show(args)
        raise ValueError("legacy_run_record_mutation_disabled_use_host_runtime")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        emit({"status": "FAIL", "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
