#!/usr/bin/env python3
"""bt-adb-screenshot — capture phone screen to a local PNG.

  bt-adb-screenshot
  bt-adb-screenshot --to /tmp/phone.png
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_adb


def main() -> int:
    ap = argparse.ArgumentParser(description="Phone screenshot via ADB")
    ap.add_argument("--to", default="~/Downloads/bluetooth/phone-screen.png")
    ap.add_argument("--serial")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        r = bt_adb.screenshot(local_path=args.to, serial=args.serial)
    except Exception as e:
        sys.stderr.write(f"screenshot failed: {e}\n")
        return 1

    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(f"saved: {r['saved_to']}  ({r['size_bytes']} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
