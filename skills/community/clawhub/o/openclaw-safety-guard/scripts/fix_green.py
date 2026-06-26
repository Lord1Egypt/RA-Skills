#!/usr/bin/env python3
"""
GREEN-tier auto-fixer: applies only 100% safe, non-business-logic changes.

Currently handles:
  - chmod 600 on Gateway plist (security hardening, fully reversible)

NOT handled here (turned out to be scanner false positives):
  - MEMORY.md "dead links": memory/YYYY is a documentation placeholder pattern,
    not a real broken path. memory/projects/api-v1.md actually exists.
    Root fix: scan_memory.py needs smarter path validation.
"""
import os
import stat
import json
from datetime import datetime
from utils import get_data_dir, get_watchdog_config


PLIST_PATH = os.path.expanduser("~/Library/LaunchAgents/ai.openclaw.gateway.plist")


def fix_plist_permissions() -> dict:
    """chmod 600 on Gateway plist. Returns result dict."""
    if not os.path.exists(PLIST_PATH):
        return {"id": "plist_chmod", "status": "skipped", "reason": "plist not found"}

    current_mode = stat.S_IMODE(os.stat(PLIST_PATH).st_mode)
    current_oct = oct(current_mode)

    if current_mode == 0o600:
        return {"id": "plist_chmod", "status": "already_ok", "mode": current_oct}

    print(f"  [plist_chmod] Before: {current_oct}")
    os.chmod(PLIST_PATH, 0o600)
    new_mode = stat.S_IMODE(os.stat(PLIST_PATH).st_mode)
    print(f"  [plist_chmod] After:  {oct(new_mode)}")

    return {
        "id": "plist_chmod",
        "status": "fixed",
        "before": current_oct,
        "after": oct(new_mode),
        "fixed_at": datetime.now().isoformat(),
    }


def main():
    print("Running GREEN auto-fixes (safe, non-business-logic only)...")
    results = []

    result = fix_plist_permissions()
    results.append(result)
    status = result["status"]
    if status == "fixed":
        print(f"  ✅ plist chmod: {result['before']} → {result['after']}")
    elif status == "already_ok":
        print(f"  ✓  plist chmod: already 600, no change needed")
    else:
        print(f"  ⚠️  plist chmod: {result.get('reason', 'skipped')}")

    # Persist results into the daily log if it exists
    data_dir = get_data_dir()
    green_log = os.path.join(data_dir, "latest_green_fixes.json")
    with open(green_log, "w", encoding="utf-8") as f:
        json.dump({
            "ran_at": datetime.now().isoformat(),
            "fixes": results,
        }, f, ensure_ascii=False, indent=2)

    fixed_count = sum(1 for r in results if r["status"] == "fixed")
    print(f"GREEN fixes done: {fixed_count} applied.")


if __name__ == "__main__":
    main()
