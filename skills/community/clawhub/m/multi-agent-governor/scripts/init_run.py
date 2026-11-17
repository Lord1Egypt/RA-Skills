#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

from _common import now_iso, path_record, save_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a bounded multi-agent run.")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--mode", choices=["fast", "balanced", "fast-deep", "deep"], default="balanced")
    parser.add_argument("--deadline-minutes", type=int, default=90)
    parser.add_argument("--main-thread-id")
    parser.add_argument("--root", default="/tmp/multi-agent-runs")
    parser.add_argument("--run-id")
    args = parser.parse_args()

    if args.deadline_minutes <= 0:
        parser.error("--deadline-minutes must be positive")
    run_id = args.run_id or f"{datetime.now(timezone.utc):%Y%m%d-%H%M%S}-{secrets.token_hex(3)}"
    if not re.fullmatch(r"[A-Za-z0-9._-]+", run_id):
        parser.error("--run-id may contain only letters, digits, dot, underscore, and hyphen")

    run_dir = Path(args.root).expanduser().resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=False)
    (run_dir / "capsules").mkdir()

    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "objective": args.objective,
        "mode": args.mode,
        "status": "planning",
        "created_at": now_iso(),
        "completed_at": None,
        "deadline_minutes": args.deadline_minutes,
        "main_thread_id": args.main_thread_id,
        "limits": {
            "wave1_agents": 3,
            "qa_agents": 2,
            "total_agents": 5,
            "max_concurrent": 4,
            "qa_rounds": 1,
            "capsule_bytes": 6144,
        },
        "sources": [path_record(source) for source in args.source],
        "lanes": [],
        "agents": [],
        "sessions": [],
        "build": {"sequence": 0, "id": None, "artifacts": [], "created_at": None},
        "metrics": {},
    }
    manifest_path = run_dir / "run-manifest.json"
    save_json(manifest_path, manifest)
    print(manifest_path)


if __name__ == "__main__":
    main()
