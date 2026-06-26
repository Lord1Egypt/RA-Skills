#!/usr/bin/env python3
"""bt-trust — Mark / unmark a paired device as Trusted.

Trusted devices auto-authorise profile connects (a paired BT speaker can
auto-reconnect when it powers up, etc.).
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import set_trusted, get_device, adapter_health, remove_device


def main() -> int:
    invoked = Path(sys.argv[0]).name
    ap = argparse.ArgumentParser(description="Trust / untrust / forget a BT device")
    ap.add_argument("mac")
    ap.add_argument("--adapter", default="hci0")
    if "untrust" in invoked:
        op = "untrust"
    elif "forget" in invoked or "unpair" in invoked:
        op = "forget"
    else:
        op = "trust"
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

    if op == "trust":
        set_trusted(args.mac, True, args.adapter)
        print(f"{args.mac}: Trusted=true")
    elif op == "untrust":
        set_trusted(args.mac, False, args.adapter)
        print(f"{args.mac}: Trusted=false")
    elif op == "forget":
        try:
            remove_device(args.mac, args.adapter)
        except RuntimeError as e:
            sys.stderr.write(f"error: {e}\n")
            return 1
        print(f"{args.mac}: removed (unpaired + forgotten)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
