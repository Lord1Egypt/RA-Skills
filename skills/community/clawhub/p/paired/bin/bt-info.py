#!/usr/bin/env python3
"""bt-info — Detailed information for one device, including GATT tree if connected.

bt-info AA:BB:CC:DD:EE:FF [--adapter hci0] [--json]
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import (get_device, list_gatt_tree, detect_profiles,
                    adapter_health)


def main() -> int:
    ap = argparse.ArgumentParser(description="Detailed BT device info")
    ap.add_argument("mac")
    ap.add_argument("--adapter", default="hci0")
    ap.add_argument("--json", action="store_true")
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

    d["profiles"] = detect_profiles(d.get("service_uuids", []))
    gatt: dict = {}
    if d.get("connected"):
        try:
            gatt = list_gatt_tree(args.mac, args.adapter)
        except Exception as e:
            gatt = {"error": str(e)}
    d["gatt"] = gatt

    if args.json:
        print(json.dumps(d, indent=2, default=str))
        return 0

    print(f"Device: {d['mac']}  ({d.get('name') or '(unnamed)'})")
    print(f"  Adapter:        {args.adapter}")
    print(f"  Address type:   {d['addr_type']}")
    print(f"  Manufacturer:   {d.get('manuf_name') or '?'}")
    print(f"  Paired:         {d.get('paired')}")
    print(f"  Trusted:        {d.get('trusted')}")
    print(f"  Connected:      {d.get('connected')}")
    if d.get("rssi") is not None:
        print(f"  RSSI:           {d['rssi']} dBm  (~{d.get('distance_m', '?')}m)")
    if d.get("icon"):
        print(f"  Icon:           {d['icon']}")
    if d.get("profiles"):
        print(f"  Profiles:       {', '.join(d['profiles'])}")
    if d.get("service_uuids"):
        print(f"  Service UUIDs:  {len(d['service_uuids'])} advertised")
        for u in d["service_uuids"][:8]:
            print(f"                  {u}")
        if len(d["service_uuids"]) > 8:
            print(f"                  ... and {len(d['service_uuids']) - 8} more")
    if isinstance(gatt, dict) and gatt and "error" not in gatt:
        print(f"\nGATT services ({len(gatt)}):")
        for svc_uuid, sv in gatt.items():
            print(f"  {svc_uuid}")
            for c_uuid, ch in sv["characteristics"].items():
                print(f"    char {c_uuid}  flags={','.join(ch['flags'])}")
    elif isinstance(gatt, dict) and "error" in gatt:
        print(f"\nGATT: not enumerated ({gatt['error']})")
    elif d.get("connected"):
        print("\nGATT: device connected but no services advertised")
    return 0


if __name__ == "__main__":
    sys.exit(main())
