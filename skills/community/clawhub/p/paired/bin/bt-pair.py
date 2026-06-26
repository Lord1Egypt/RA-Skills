#!/usr/bin/env python3
"""bt-pair — Pair (and optionally connect+trust) a discovered device.

The bt-agent.service must already be running (or start it with `systemctl --user start bt-agent`).

Examples:
  bt-pair AA:BB:CC:DD:EE:FF                 # pair, do NOT connect
  bt-pair AA:BB:CC:DD:EE:FF --connect       # pair + trust + connect
  bt-pair AA:BB:CC:DD:EE:FF --pin           # interactive PIN mode (requires agent in pin mode)
  bt-pair --discoverable                    # put OUR adapter in pairable mode (180s) for the
                                            # phone to initiate; useful for "pair my phone"
"""
from __future__ import annotations
import argparse, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import (device_op, set_trusted, get_device, adapter_path,
                    adapter_health, ADAPTER_IFACE, PROPS_IFACE,
                    BLUEZ_SERVICE, get_bus, AdapterDownError)
import dbus


def make_pairable(adapter: str, seconds: int = 180) -> None:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        raise AdapterDownError(f"adapter {adapter!r} not found")
    aobj = bus.get_object(BLUEZ_SERVICE, apath)
    props = dbus.Interface(aobj, PROPS_IFACE)
    props.Set(ADAPTER_IFACE, "Pairable", dbus.Boolean(True))
    props.Set(ADAPTER_IFACE, "PairableTimeout", dbus.UInt32(seconds))
    props.Set(ADAPTER_IFACE, "Discoverable", dbus.Boolean(True))
    props.Set(ADAPTER_IFACE, "DiscoverableTimeout", dbus.UInt32(seconds))


def main() -> int:
    ap = argparse.ArgumentParser(description="Pair a Bluetooth device")
    ap.add_argument("mac", nargs="?", help="MAC of device to pair (omit with --discoverable)")
    ap.add_argument("--adapter", default="hci0")
    ap.add_argument("--connect", action="store_true",
                    help="After pairing, trust + connect")
    ap.add_argument("--no-trust", action="store_true",
                    help="Do not set Trusted=true after pairing")
    ap.add_argument("--discoverable", action="store_true",
                    help="Just make our adapter pairable+discoverable (180s) and exit")
    ap.add_argument("--seconds", type=int, default=180,
                    help="--discoverable timeout (default 180)")
    ap.add_argument("--timeout", type=float, default=30.0,
                    help="Pair timeout in seconds (default 30)")
    args = ap.parse_args()

    health = adapter_health(args.adapter)
    if not health["ok"]:
        sys.stderr.write(f"adapter unhealthy: {health['reason']}\n")
        return 2

    if args.discoverable:
        make_pairable(args.adapter, args.seconds)
        print(f"{args.adapter}: Pairable+Discoverable for {args.seconds}s. "
              f"BD address {health['address']}, name {health['alias']!r}.")
        print("Now go to your phone's Bluetooth settings and pick that name.")
        return 0

    if not args.mac:
        sys.stderr.write("error: MAC required (or use --discoverable)\n")
        return 2

    print(f"Pairing {args.mac} on {args.adapter}...")
    try:
        device_op(args.mac, "Pair", adapter=args.adapter, timeout=args.timeout)
    except RuntimeError as e:
        sys.stderr.write(f"PAIR FAILED: {e}\n")
        return 1

    # Verify
    info = get_device(args.mac, args.adapter)
    if not info.get("paired"):
        sys.stderr.write("Pair returned but device is not Paired in BlueZ — strange\n")
        return 1
    print(f"  PAIRED OK ({info.get('name') or args.mac})")

    if not args.no_trust:
        set_trusted(args.mac, True, adapter=args.adapter)
        print("  Trusted=true")

    if args.connect:
        print(f"  connecting...")
        try:
            device_op(args.mac, "Connect", adapter=args.adapter, timeout=args.timeout)
        except RuntimeError as e:
            sys.stderr.write(f"CONNECT FAILED: {e}\n")
            return 1
        info = get_device(args.mac, args.adapter)
        print(f"  CONNECTED ({'profiles negotiated' if info.get('connected') else 'connection state ambiguous'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
