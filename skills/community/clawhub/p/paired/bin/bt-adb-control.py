#!/usr/bin/env python3
"""bt-adb-launch / bt-adb-type / bt-adb-media — phone control via ADB."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_adb


def main() -> int:
    invoked = Path(sys.argv[0]).name
    if "launch" in invoked:
        ap = argparse.ArgumentParser(description="Launch app via ADB")
        ap.add_argument("target",
                        help="Package (com.foo.bar) or component (com.foo/.Activity)")
        ap.add_argument("--serial")
        args = ap.parse_args()
        try:
            r = bt_adb.launch_app(args.target, serial=args.serial)
        except Exception as e:
            sys.stderr.write(f"launch failed: {e}\n")
            return 1
        print(r["stdout"] or "OK")
        return 0

    if "type" in invoked:
        ap = argparse.ArgumentParser(description="Type text into focused field")
        ap.add_argument("text")
        ap.add_argument("--serial")
        args = ap.parse_args()
        try:
            bt_adb.type_text(args.text, serial=args.serial)
        except Exception as e:
            sys.stderr.write(f"type failed: {e}\n")
            return 1
        print("OK")
        return 0

    if "media" in invoked:
        ap = argparse.ArgumentParser(description="Media transport via ADB")
        ap.add_argument("action", nargs="?", default="status",
                        choices=["play", "pause", "play-pause",
                                 "next", "previous", "stop", "status"])
        ap.add_argument("--serial")
        ap.add_argument("--json", action="store_true")
        args = ap.parse_args()
        try:
            if args.action == "status":
                r = bt_adb.media_status(serial=args.serial)
                if args.json:
                    print(json.dumps(r, indent=2))
                else:
                    if not r["sessions"]:
                        print("(no media sessions)")
                    for s in r["sessions"]:
                        print(f"  {s.get('package', '?'):<30}  "
                              f"state={s.get('state', '?'):<10}  "
                              f"{s.get('title', '')}")
                return 0
            r = bt_adb.media_dispatch(args.action, serial=args.serial)
            print(f"{args.action}: {r['stdout'] or 'OK'}")
        except Exception as e:
            sys.stderr.write(f"media failed: {e}\n")
            return 1
        return 0

    sys.stderr.write(f"unknown invocation: {invoked}\n")
    return 2


if __name__ == "__main__":
    sys.exit(main())
