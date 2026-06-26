#!/usr/bin/env python3
"""bt-connect / bt-disconnect — Open or close an active link to a paired device.

Same script handles both via $0; symlink-aware.
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import device_op, get_device, adapter_health


def main() -> int:
    invoked = Path(sys.argv[0]).name
    op = "Disconnect" if "disconnect" in invoked else "Connect"
    ap = argparse.ArgumentParser(description=f"{op} a paired BT device")
    ap.add_argument("mac")
    ap.add_argument("--adapter", default="hci0")
    ap.add_argument("--timeout", type=float, default=30.0)
    args = ap.parse_args()

    health = adapter_health(args.adapter)
    if not health["ok"]:
        sys.stderr.write(f"adapter unhealthy: {health['reason']}\n")
        return 2

    try:
        d = get_device(args.mac, args.adapter)
    except RuntimeError as e:
        sys.stderr.write(f"error: {e}\n")
        return 1

    if op == "Connect" and d.get("connected"):
        print(f"{args.mac} already connected.")
        return 0
    if op == "Disconnect" and not d.get("connected"):
        print(f"{args.mac} already disconnected.")
        return 0

    print(f"{op}ing {args.mac} on {args.adapter}...")
    try:
        device_op(args.mac, op, adapter=args.adapter, timeout=args.timeout)
    except RuntimeError as e:
        sys.stderr.write(f"{op.upper()} FAILED: {e}\n")
        return 1
    d2 = get_device(args.mac, args.adapter)
    print(f"  state: connected={d2.get('connected')} paired={d2.get('paired')}")
    return 0 if (op == "Connect") == bool(d2.get("connected")) else 1


if __name__ == "__main__":
    sys.exit(main())
