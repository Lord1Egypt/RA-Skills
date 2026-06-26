#!/usr/bin/env python3
"""bt-battery — Read a paired phone's battery + signal via BlueZ Battery1
or via ofono Handsfree HF Indicators.

Examples:
  bt-battery MAC
  bt-battery MAC --json
  bt-battery --all                  # every connected device with battery
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import dbus
from bt_lib import (BLUEZ_SERVICE, OM_IFACE, PROPS_IFACE, get_bus,
                    adapter_path, _mac_to_device_path, _device_path_to_mac,
                    list_adapters)

BATTERY_IFACE = "org.bluez.Battery1"


def _dbus_to_py(v):
    if isinstance(v, dbus.Dictionary):
        return {str(k): _dbus_to_py(x) for k, x in v.items()}
    if isinstance(v, (dbus.Array, list, tuple)):
        return [_dbus_to_py(x) for x in v]
    if isinstance(v, (dbus.String, dbus.ObjectPath)):
        return str(v)
    if isinstance(v, dbus.Boolean):
        return bool(v)
    if isinstance(v, (dbus.Int16, dbus.Int32, dbus.Int64,
                       dbus.UInt16, dbus.UInt32, dbus.UInt64,
                       dbus.Byte)):
        return int(v)
    return v


def battery_for(mac: str, adapter: str = "hci0") -> dict | None:
    bus = get_bus()
    apath = adapter_path(adapter)
    if apath is None:
        return None
    dpath = _mac_to_device_path(apath, mac)
    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    for path, ifaces in om.GetManagedObjects().items():
        if path != dpath:
            continue
        if BATTERY_IFACE in ifaces:
            return {
                "mac": mac.upper(),
                "percentage": _dbus_to_py(ifaces[BATTERY_IFACE].get("Percentage")),
                "source": _dbus_to_py(ifaces[BATTERY_IFACE].get("Source")),
            }
    return None


def all_batteries() -> list[dict]:
    bus = get_bus()
    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    out = []
    for path, ifaces in om.GetManagedObjects().items():
        if BATTERY_IFACE not in ifaces:
            continue
        mac = _device_path_to_mac(path)
        out.append({
            "mac": mac,
            "path": str(path),
            "percentage": _dbus_to_py(ifaces[BATTERY_IFACE].get("Percentage")),
            "source": _dbus_to_py(ifaces[BATTERY_IFACE].get("Source")),
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Battery level of paired BT devices")
    ap.add_argument("mac", nargs="?")
    ap.add_argument("--all", action="store_true",
                    help="Every device with battery info")
    ap.add_argument("--adapter", default="hci0")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.all:
        bs = all_batteries()
        if args.json:
            print(json.dumps(bs, indent=2))
        elif not bs:
            print("No connected devices report battery.")
        else:
            for b in bs:
                src = b.get("source") or "?"
                print(f"  {b['mac']}  {b.get('percentage', '?')}%  ({src})")
        return 0

    if not args.mac:
        sys.stderr.write("MAC required (or use --all)\n")
        return 2

    b = battery_for(args.mac, args.adapter)
    if args.json:
        print(json.dumps(b, indent=2))
        return 0
    if b is None:
        print(f"No battery data for {args.mac}.")
        print("  Hint: phone must be connected and have advertised the Battery service")
        print("  (Some phones only do this via HFP HF Indicators after a call connects)")
        return 1
    print(f"{b['mac']}  {b['percentage']}%  source={b['source']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
