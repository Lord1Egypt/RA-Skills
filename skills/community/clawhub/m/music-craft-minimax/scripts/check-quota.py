#!/usr/bin/env python3
"""MiniMax Token Plan quota check.

Usage:
    python3 scripts/check-quota.py            # formatted per-model report
    python3 scripts/check-quota.py --quiet    # one-line summary
    python3 scripts/check-quota.py --json     # raw JSON to stdout

Exit codes:
    0  quota fetched successfully (and headroom present if --budget passed)
    2  mmx binary missing or quota endpoint failed
    3  per-model headroom insufficient (when --budget N is passed)

Source of truth: references/quota-checking.md
Reference implementation: ~/youtube-studio/tools/mmx_recipe.py::mmx_quota_show

Verified against mmx CLI v1.0.16 (2026-07-30). The actual JSON shape is:
{
  "model_remains": [
    {
      "model_name": "general" | "video" | ...,
      "current_interval_usage_count": <int>,
      "current_interval_remaining_percent": <0-100>,
      "current_interval_status": <1|3>,      # 3 = healthy
      "current_weekly_usage_count": <int>,
      "current_weekly_remaining_percent": <0-100>,
      "current_weekly_status": <1|3>
    },
    ...
  ]
}
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from typing import Any


def _run_cli(timeout: int) -> dict[str, Any]:
    """Call mmx quota show --output json and return parsed JSON or an error dict."""
    mmx = shutil.which("mmx")
    if mmx is None:
        return {"error": "mmx binary not found on PATH"}
    try:
        proc = subprocess.run(
            [mmx, "quota", "show", "--output", "json"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"error": f"mmx quota show timed out after {timeout}s"}
    if proc.returncode != 0:
        return {
            "error": proc.stderr.strip() or "non-zero exit",
            "returncode": proc.returncode,
        }
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"raw": proc.stdout.strip()}


def _summary(data: dict[str, Any]) -> str:
    """One-line summary using the 'general' model bucket (the Plus quota)."""
    general = _find_general(data)
    if not general:
        return "5h: ?  weekly: ?  (no 'general' bucket found)"
    return (
        f"5h: {general.get('current_interval_usage_count', '?')} used "
        f"({general.get('current_interval_remaining_percent', '?')}% left, "
        f"status={general.get('current_interval_status', '?')})  "
        f"week: {general.get('current_weekly_usage_count', '?')} used "
        f"({general.get('current_weekly_remaining_percent', '?')}% left, "
        f"status={general.get('current_weekly_status', '?')})"
    )


def _find_general(data: dict[str, Any]) -> dict[str, Any] | None:
    """Find the 'general' model bucket — the Plus-level quota."""
    for entry in data.get("model_remains", []):
        if entry.get("model_name") == "general":
            return entry
    # Fallback: first entry
    entries = data.get("model_remains", [])
    return entries[0] if entries else None


def _per_model_lines(data: dict[str, Any]) -> list[str]:
    lines = []
    for entry in data.get("model_remains", []):
        name = entry.get("model_name", "?")
        used_5h = entry.get("current_interval_usage_count", "?")
        pct_5h = entry.get("current_interval_remaining_percent", "?")
        status_5h = entry.get("current_interval_status", "?")
        used_w = entry.get("current_weekly_usage_count", "?")
        pct_w = entry.get("current_weekly_remaining_percent", "?")
        status_w = entry.get("current_weekly_status", "?")
        lines.append(
            f"  {name:<20} 5h: {used_5h} used ({pct_5h}% left, status={status_5h})  "
            f"week: {used_w} used ({pct_w}% left, status={status_w})"
        )
    return lines


def _budget_check(
    data: dict[str, Any], budget: int, safety_margin: int = 10
) -> tuple[bool, str]:
    """Check if budget units fit in current 5h headroom (general bucket only).

    Gates on TWO conditions:
    1. `general.current_interval_status == 3` (healthy); bail otherwise.
    2. Headroom ≥ budget + safety_margin (using `remaining_percent × 4500`).

    Conservative: even when `general` shows 50% left, status != 3 means the
    API is throttling and we should abort (matches documented contract).
    """
    general = _find_general(data)
    if not general:
        return False, "no 'general' bucket found in quota response"
    status = general.get("current_interval_status")
    if status is not None and status != 3:
        return False, f"interval not healthy (status={status})"
    pct = general.get("current_interval_remaining_percent")
    if pct is None:
        return False, "no remaining percentage in 'general' bucket"
    # Rough estimate: 4500 is the documented Plus ceiling
    CEILING = 4500
    try:
        headroom = int(CEILING * float(pct) / 100)
    except (TypeError, ValueError):
        return False, f"could not parse remaining percentage: {pct!r}"
    if headroom < budget + safety_margin:
        return False, f"have={headroom}  need={budget}+{safety_margin}"
    return True, f"budget={budget}  remaining≈{headroom}  margin={headroom - budget}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="MiniMax Token Plan quota check")
    p.add_argument("--quiet", action="store_true", help="Print one-line summary only")
    p.add_argument(
        "--json", action="store_true", help="Print raw JSON to stdout (no formatting)"
    )
    p.add_argument(
        "--budget",
        type=int,
        help="Estimate a batch of N units; exit 3 if headroom is short",
    )
    p.add_argument("--timeout", type=int, default=30)
    args = p.parse_args(argv)

    data = _run_cli(timeout=args.timeout)
    if "error" in data or "raw" in data:
        print(json.dumps(data, indent=2), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(data, indent=2))
    elif args.quiet:
        print(_summary(data))
    else:
        print(_summary(data))
        print()
        print("Per model:")
        for line in _per_model_lines(data):
            print(line)

    # Gate: budget check (uses remaining percentage as the source of truth;
    # status field semantics vary between models and CLI versions).
    if args.budget is not None:
        ok, reason = _budget_check(data, args.budget)
        if ok:
            print(f"\nOK: {reason}")
        else:
            print(f"\nABORT: insufficient headroom  {reason}", file=sys.stderr)
            return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
