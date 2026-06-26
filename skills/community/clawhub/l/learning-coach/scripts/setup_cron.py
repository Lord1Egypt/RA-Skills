#!/usr/bin/env python3
"""Idempotent cron manager for learning-coach jobs."""

from __future__ import annotations
import argparse
import subprocess
from pathlib import Path

TAG = "# learning-coach"


def get_crontab() -> str:
    p = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if p.returncode != 0:
        return ""
    return p.stdout


def set_crontab(text: str) -> None:
    p = subprocess.run(["crontab", "-"], input=text, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "failed to set crontab")


def default_jobs(workspace: Path) -> list[str]:
    py = "python3"
    base = workspace / "skills" / "learning-coach" / "scripts"
    weekly = base / "weekly_report.py"
    return [
        f"30 7 * * * {py} {weekly} --mode daily-morning {TAG}",
        f"0 20 * * * {py} {weekly} --mode daily-evening {TAG}",
        f"0 10 * * 3,6 {py} {weekly} --mode curation-refresh {TAG}",
        f"0 7 * * 1 {py} {weekly} --mode weekly {TAG}",
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["apply", "remove", "show"])
    ap.add_argument("--workspace", default=str(Path.home() / ".openclaw" / "workspace"))
    args = ap.parse_args()

    current = get_crontab().splitlines()
    filtered = [ln for ln in current if TAG not in ln]

    if args.action == "show":
        jobs = [ln for ln in current if TAG in ln]
        print("\n".join(jobs) if jobs else "(no learning-coach jobs)")
        return 0

    if args.action == "remove":
        set_crontab("\n".join(filtered).strip() + "\n")
        print("Removed learning-coach cron jobs.")
        return 0

    jobs = default_jobs(Path(args.workspace))
    merged = filtered + jobs
    set_crontab("\n".join([x for x in merged if x.strip()]) + "\n")
    print("Applied learning-coach cron jobs:")
    for j in jobs:
        print("-", j)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
