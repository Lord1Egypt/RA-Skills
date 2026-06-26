#!/usr/bin/env python3
"""bt-adb-notif — list active notifications on the phone.

  bt-adb-notif
  bt-adb-notif --json
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_adb


def main() -> int:
    ap = argparse.ArgumentParser(description="Active notifications via ADB")
    ap.add_argument("--serial")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        notifs = bt_adb.notifications(serial=args.serial)
    except Exception as e:
        sys.stderr.write(f"failed: {e}\n")
        return 1

    if args.json:
        print(json.dumps(notifs, indent=2))
        return 0

    if not notifs:
        print("(no notifications)")
        return 0
    print(f"  {'PKG':<30}  {'TITLE':<30}  TEXT")
    for n in notifs:
        pkg = (n.get("package") or "?")[-30:]
        title = (n.get("title") or "")[:30]
        text = (n.get("text") or "")[:60]
        print(f"  {pkg:<30}  {title:<30}  {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
