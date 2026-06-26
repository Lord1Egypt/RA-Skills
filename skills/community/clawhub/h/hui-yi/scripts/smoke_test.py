#!/usr/bin/env python3
"""Lightweight smoke test for Hui-Yi cold memory.

Runs non-destructive checks:
- cold memory root exists
- validate.py --strict passes
- search.py returns a ranked/index hit for the query
- scheduler.py can produce JSON in preview mode for the configured schedule

Usage:
  python scripts/smoke_test.py [--memory-root PATH] [--query QUERY] [--schedule-id ID] [--config PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import resolve_memory_root  # noqa: E402


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


class SmokeFailure(Exception):
    """Raised when a smoke-test step fails."""


def run_step(name: str, cmd: list[str]) -> subprocess.CompletedProcess[str]:
    print(f"\n== {name} ==")
    print("$ " + " ".join(cmd))
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(
        cmd,
        cwd=SKILL_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    output = proc.stdout.strip()
    if output:
        print(output)
    if proc.returncode != 0:
        raise SmokeFailure(f"{name} failed with exit code {proc.returncode}")
    return proc


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a lightweight Hui-Yi smoke test")
    parser.add_argument("--memory-root", default=None, help="optional cold memory root")
    parser.add_argument("--query", default="hui-yi", help="query used for search/scheduler checks")
    parser.add_argument("--schedule-id", default="daily-evening-review", help="schedule id to preview")
    parser.add_argument("--config", default=None, help="optional scheduler config path; defaults to <memory-root>/schedule.json")
    args = parser.parse_args()

    memory_root = resolve_memory_root(args.memory_root)
    config_path = Path(args.config).resolve() if args.config else memory_root / "schedule.json"
    print("Hui-Yi smoke test")
    print(f"skill root: {SKILL_ROOT}")
    print(f"memory root: {memory_root}")
    print(f"schedule config: {config_path}")

    if not memory_root.exists():
        print(f"ERROR: memory root not found: {memory_root}")
        return 1

    py = sys.executable
    memory_args = ["--memory-root", str(memory_root)]

    try:
        run_step("validate strict", [py, "scripts/validate.py", *memory_args, "--strict"])

        search_proc = run_step("search", [py, "scripts/search.py", args.query, str(memory_root)])
        if "No matches" in search_proc.stdout or "ranked tags.json matches" not in search_proc.stdout:
            raise SmokeFailure("search completed but did not produce ranked tag matches")

        scheduler_proc = run_step(
            "scheduler preview",
            [
                py,
                "scripts/scheduler.py",
                *memory_args,
                "--config",
                str(config_path),
                "--schedule-id",
                args.schedule_id,
                "--preview",
                "--json",
                "--query",
                args.query,
            ],
        )
        try:
            payload = json.loads(scheduler_proc.stdout)
        except json.JSONDecodeError as exc:
            raise SmokeFailure(f"scheduler output is not valid JSON: {exc}") from exc
        if not payload.get("ok"):
            raise SmokeFailure("scheduler JSON returned ok=false")
        if args.schedule_id not in payload.get("schedulesMatched", []):
            raise SmokeFailure(f"scheduler did not match schedule id {args.schedule_id!r}")

    except SmokeFailure as exc:
        print(f"\nSMOKE TEST FAILED: {exc}")
        return 1

    print("\nSMOKE TEST PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
