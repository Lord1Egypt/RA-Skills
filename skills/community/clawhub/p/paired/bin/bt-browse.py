#!/usr/bin/env python3
"""bt-browse — OBEX FTP: list / pull files from a paired BT device's filesystem.

Examples:
  bt-browse AA:BB:CC:DD:EE:FF                      # list root folder
  bt-browse AA:BB:CC:DD:EE:FF /Music               # list a sub-folder
  bt-browse AA:BB:CC:DD:EE:FF --pull /Music/song.mp3
  bt-browse AA:BB:CC:DD:EE:FF --pull /Music/song.mp3 --save-to ./song.mp3

Requires the device to support OBEX FTP (UUID 0000-1106). Many phones
expose this only after granting filesystem access in pair settings.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_obex


def main() -> int:
    ap = argparse.ArgumentParser(description="OBEX FTP browse / pull")
    ap.add_argument("mac")
    ap.add_argument("path", nargs="?", default="/", help="Folder to list (default /)")
    ap.add_argument("--pull", help="Filename (relative to listed folder) to pull")
    ap.add_argument("--save-to", help="Local path to save pulled file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.pull:
        try:
            r = bt_obex.pull_file(args.mac, args.pull, save_to=args.save_to)
        except Exception as e:
            sys.stderr.write(f"PULL FAILED: {e}\n")
            return 1
        if args.json:
            print(json.dumps(r, indent=2))
        else:
            print(f"saved {args.pull} -> {r['saved_to']}  status={r['status']}")
        return 0 if r["status"] == "complete" else 1

    try:
        listing = bt_obex.list_folder(args.mac, args.path)
    except Exception as e:
        sys.stderr.write(f"BROWSE FAILED: {e}\n")
        return 1

    if args.json:
        print(json.dumps(listing, indent=2))
        return 0
    if not listing:
        print(f"(empty: {args.path})")
        return 0
    print(f"  {'TYPE':<8}  {'SIZE':>10}  Name")
    for e in listing:
        t = e.get("Type") or ("folder" if e.get("Folder") else "file")
        sz = e.get("Size", "")
        print(f"  {t:<8}  {sz:>10}  {e.get('Name', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
