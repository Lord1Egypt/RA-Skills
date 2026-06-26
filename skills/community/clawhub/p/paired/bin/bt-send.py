#!/usr/bin/env python3
"""bt-send — OBEX Object Push: push a file to a paired BT device.

Examples:
  bt-send ~/Downloads/photo.jpg AA:BB:CC:DD:EE:FF
  bt-send report.pdf AA:BB:CC:DD:EE:FF --timeout 300

The destination device must be paired + Object Push capable. On phones,
you'll get a notification asking to accept the incoming file. The
device must accept it within --timeout seconds (default 120).
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_obex


def main() -> int:
    ap = argparse.ArgumentParser(description="OBEX Object Push to a paired device")
    ap.add_argument("file")
    ap.add_argument("mac")
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    fp = Path(args.file).expanduser().resolve()
    if not fp.exists():
        sys.stderr.write(f"error: {fp} does not exist\n")
        return 1

    print(f"Pushing {fp} ({fp.stat().st_size} bytes) to {args.mac}...")
    print("On the receiving device, accept the incoming file when prompted.")
    try:
        result = bt_obex.push_file(args.mac, str(fp), timeout=args.timeout)
    except Exception as e:
        sys.stderr.write(f"PUSH FAILED: {e}\n")
        return 1

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = result.get("transfer_status")
        if status == "complete":
            print(f"  COMPLETE — {result.get('size')} bytes sent")
            return 0
        else:
            print(f"  FINAL STATUS: {status}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
