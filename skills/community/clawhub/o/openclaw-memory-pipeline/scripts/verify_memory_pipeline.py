#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REQUIRED_PATHS = [
    "MEMORY.md",
    "memory",
    "memory/inbox.md",
    "memory/projects",
    "memory/system",
    "memory/groups",
]

EXPECTED_CRON_NAMES = [
    "context: compress chat history (hourly)",
    "daily-memory-diary",
    "weekly-memory-review",
]


def classify(path: Path) -> str:
    if path.is_dir():
        return "dir"
    if path.is_file():
        return "file"
    return "missing"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def check_paths(workspace: Path) -> tuple[list[str], list[str]]:
    ok: list[str] = []
    bad: list[str] = []
    for rel in REQUIRED_PATHS:
        target = workspace / rel
        kind = classify(target)
        if kind == "missing":
            bad.append(f"missing: {rel}")
        else:
            ok.append(f"{kind}: {rel}")
    return ok, bad


def check_inbox(workspace: Path) -> tuple[list[str], list[str]]:
    inbox = workspace / "memory" / "inbox.md"
    ok: list[str] = []
    bad: list[str] = []
    if not inbox.exists():
        bad.append("missing: memory/inbox.md")
        return ok, bad

    text = read_text(inbox)
    if "## pending" in text:
        ok.append("inbox contains '## pending'")
    else:
        bad.append("inbox missing '## pending' section")

    if text.strip().startswith("# inbox"):
        ok.append("inbox header looks correct")
    else:
        bad.append("inbox header does not start with '# inbox'")
    return ok, bad


def check_recent_outputs(workspace: Path) -> tuple[list[str], list[str]]:
    ok: list[str] = []
    warn: list[str] = []
    memory_dir = workspace / "memory"
    raw_files = sorted(memory_dir.glob("*-raw.md"))
    daily_files = sorted([p for p in memory_dir.glob("????-??-??.md") if p.is_file()])

    if raw_files:
        ok.append(f"raw archive files found: {len(raw_files)}")
    else:
        warn.append("no raw archive files found yet")

    if daily_files:
        ok.append(f"daily summary files found: {len(daily_files)}")
    else:
        warn.append("no daily summary files found yet")

    return ok, warn


def load_cron_jobs(timeout_seconds: int) -> tuple[list[dict], list[str], list[str]]:
    ok: list[str] = []
    warn: list[str] = []
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list", "--json"],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except FileNotFoundError:
        warn.append("openclaw CLI not found; skipping cron verification")
        return [], ok, warn
    except subprocess.TimeoutExpired:
        warn.append("openclaw cron list timed out; skipping cron verification")
        return [], ok, warn

    if result.returncode != 0:
        warn.append(f"openclaw cron list failed with exit code {result.returncode}")
        stderr = (result.stderr or "").strip()
        if stderr:
            warn.append(f"cron stderr: {stderr}")
        return [], ok, warn

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        warn.append("unable to parse JSON from 'openclaw cron list --json'")
        return [], ok, warn

    jobs = payload.get("jobs", []) if isinstance(payload, dict) else []
    ok.append(f"cron API reachable; jobs returned: {len(jobs)}")
    return jobs, ok, warn


def payload_text(job: dict) -> str:
    payload = job.get("payload") or {}
    parts: list[str] = []
    for key in ("message", "text"):
        value = payload.get(key)
        if isinstance(value, str):
            parts.append(value)
    return "\n".join(parts)


def workspace_fingerprints(workspace: Path, job_name: str) -> list[str]:
    base = str(workspace)
    memory = f"{base}/memory"
    if job_name == "context: compress chat history (hourly)":
        return [f"{memory}/inbox.md", f"{memory}/YYYY-MM-DD-raw.md"]
    if job_name == "daily-memory-diary":
        return [f"{memory}/YYYY-MM-DD.md"]
    if job_name == "weekly-memory-review":
        return [f"{base}/MEMORY.md", f"{memory}/YYYY-MM-DD.md"]
    return [base]


def check_cron_jobs(workspace: Path, timeout_seconds: int) -> tuple[list[str], list[str], list[str]]:
    ok: list[str] = []
    warn: list[str] = []
    bad: list[str] = []

    jobs, load_ok, load_warn = load_cron_jobs(timeout_seconds)
    ok.extend(load_ok)
    warn.extend(load_warn)

    if not jobs and load_warn:
        return ok, warn, bad

    indexed = {job.get("name"): job for job in jobs if isinstance(job, dict)}

    for expected in EXPECTED_CRON_NAMES:
        job = indexed.get(expected)
        if not job:
            bad.append(f"missing cron job: {expected}")
            continue

        enabled = bool(job.get("enabled"))
        state = job.get("state") or {}
        last_status = state.get("lastStatus") or state.get("lastRunStatus")
        next_run = state.get("nextRunAtMs")
        text = payload_text(job)
        fingerprints = workspace_fingerprints(workspace, expected)
        matched = [fp for fp in fingerprints if fp in text]

        if enabled:
            ok.append(f"cron present and enabled: {expected}")
        else:
            bad.append(f"cron present but disabled: {expected}")

        if matched:
            ok.append(f"cron payload matches workspace: {expected}")
        else:
            bad.append(f"cron payload does not reference this workspace: {expected}")

        if last_status == "ok":
            ok.append(f"cron last status ok: {expected}")
        elif last_status:
            warn.append(f"cron last status {last_status}: {expected}")
        else:
            warn.append(f"cron has no recorded run status yet: {expected}")

        if next_run:
            ok.append(f"cron has next run scheduled: {expected}")
        else:
            warn.append(f"cron missing next scheduled run: {expected}")

    return ok, warn, bad


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Markdown memory pipeline structure.")
    parser.add_argument("--workspace", default=".", help="Workspace root (default: current directory)")
    parser.add_argument("--skip-cron", action="store_true", help="Skip cron verification and only check files/directories")
    parser.add_argument("--cron-timeout-seconds", type=int, default=8, help="Timeout for 'openclaw cron list --json' (default: 8)")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    if not workspace.exists():
        print(f"workspace does not exist: {workspace}", file=sys.stderr)
        return 2

    path_ok, path_bad = check_paths(workspace)
    inbox_ok, inbox_bad = check_inbox(workspace)
    output_ok, output_warn = check_recent_outputs(workspace)
    if args.skip_cron:
        cron_ok, cron_warn, cron_bad = [], ["cron verification skipped by flag"], []
    else:
        cron_ok, cron_warn, cron_bad = check_cron_jobs(workspace, max(args.cron_timeout_seconds, 1))

    all_ok = path_ok + inbox_ok + output_ok + cron_ok
    all_warn = output_warn + cron_warn
    all_bad = path_bad + inbox_bad + cron_bad

    print(f"workspace: {workspace}\n")

    print("PASS:")
    if all_ok:
        for item in all_ok:
            print(f"  - {item}")
    else:
        print("  - none")

    print("\nWARN:")
    if all_warn:
        for item in all_warn:
            print(f"  - {item}")
    else:
        print("  - none")

    print("\nFAIL:")
    if all_bad:
        for item in all_bad:
            print(f"  - {item}")
    else:
        print("  - none")

    print("\nsummary:")
    print(f"  pass={len(all_ok)} warn={len(all_warn)} fail={len(all_bad)}")

    return 1 if all_bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
