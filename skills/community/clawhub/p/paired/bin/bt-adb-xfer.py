#!/usr/bin/env python3
"""bt-adb-push / bt-adb-pull — file transfer that bypasses the broken OBEX path.

  bt-adb-push FILE [REMOTE]            # default: /sdcard/Download/<basename>
  bt-adb-pull REMOTE [LOCAL]           # default: ~/Downloads/bluetooth/<basename>
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_adb


def main() -> int:
    invoked = Path(sys.argv[0]).name
    op = "pull" if "pull" in invoked else "push"

    ap = argparse.ArgumentParser(description=f"ADB {op}")
    if op == "push":
        ap.add_argument("local")
        ap.add_argument("remote", nargs="?",
                        help="Default: /sdcard/Download/<basename>")
    else:
        ap.add_argument("remote")
        ap.add_argument("local", nargs="?",
                        help="Default: ~/Downloads/bluetooth/<basename>")
    ap.add_argument("--serial")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        if op == "push":
            local = Path(args.local).expanduser()
            remote = args.remote or f"/sdcard/Download/{local.name}"
            r = bt_adb.push(str(local), remote, serial=args.serial)
        else:
            remote = args.remote
            local = (args.local or
                     f"~/Downloads/bluetooth/{Path(remote).name}")
            r = bt_adb.pull(remote, local, serial=args.serial)
    except Exception as e:
        sys.stderr.write(f"{op} failed: {e}\n")
        return 1

    if args.json:
        print(json.dumps(r, indent=2))
    else:
        print(r["stdout"] or f"{op} OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
