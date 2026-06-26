#!/usr/bin/env python3
"""bt-list — Show known/paired/connected BT devices on a given adapter.

Examples:
  bt-list                    # all known devices on hci0
  bt-list --paired           # only paired
  bt-list --connected        # only currently connected
  bt-list --json             # JSON for scripting
  bt-list --adapter hci1     # use a different controller
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import (list_adapters, adapter_path, adapter_health,
                    DEVICE_IFACE, OM_IFACE, BLUEZ_SERVICE, get_bus,
                    _props_to_partial, _finalise, _device_path_to_mac,
                    detect_profiles)
import dbus


def _enumerate(adapter: str) -> list[dict]:
    apath = adapter_path(adapter)
    if apath is None:
        raise RuntimeError(f"adapter {adapter!r} not found")
    bus = get_bus()
    om = dbus.Interface(bus.get_object(BLUEZ_SERVICE, "/"), OM_IFACE)
    out = []
    for path, ifaces in om.GetManagedObjects().items():
        if not path.startswith(apath + "/") or DEVICE_IFACE not in ifaces:
            continue
        partial = _props_to_partial(ifaces[DEVICE_IFACE])
        mac = partial.get("mac") or _device_path_to_mac(path)
        if not mac:
            continue
        d = _finalise(mac, partial)
        d["profiles"] = detect_profiles(d.get("service_uuids", []))
        out.append(d)
    out.sort(key=lambda d: (
        not d.get("connected"),
        not d.get("paired"),
        -(d.get("rssi") or -127),
        d.get("name") or "",
    ))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="List BlueZ-known BT devices")
    ap.add_argument("--adapter", default="hci0")
    ap.add_argument("--paired", action="store_true")
    ap.add_argument("--connected", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    health = adapter_health(args.adapter)
    if not health["ok"]:
        sys.stderr.write(f"adapter {args.adapter} unhealthy: {health['reason']}\n")
        return 2

    devs = _enumerate(args.adapter)
    if args.paired:
        devs = [d for d in devs if d.get("paired")]
    if args.connected:
        devs = [d for d in devs if d.get("connected")]

    if args.json:
        print(json.dumps(devs, indent=2))
        return 0

    if not devs:
        print(f"No matching devices on {args.adapter}.")
        return 0

    print(f"  {'STATE':<10}  {'MAC':<17}  {'Manufacturer':<14}  {'Profiles':<24}  Name")
    print(f"  {'-'*10}  {'-'*17}  {'-'*14}  {'-'*24}  ----")
    for d in devs:
        st = []
        if d.get("connected"):
            st.append("CONN")
        if d.get("paired"):
            st.append("PAIR")
        if d.get("trusted"):
            st.append("TRUST")
        state = "/".join(st) or "-"
        profiles = ", ".join(d.get("profiles", []))[:24]
        print(f"  {state:<10}  {d['mac']:<17}  "
              f"{(d.get('manuf_name') or ''):<14}  "
              f"{profiles:<24}  "
              f"{d.get('name') or '(unnamed)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
