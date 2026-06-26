#!/usr/bin/env python3
"""bt-adapters — Show all BlueZ adapters on this host.

Used by Agent to know what BT hardware is available before any operation.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import list_adapters, adapter_health, detect_profiles


def main() -> int:
    ap = argparse.ArgumentParser(description="List all BlueZ adapters on this host")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    adapters = list_adapters()
    if args.json:
        for a in adapters:
            a["health"] = adapter_health(a["name"])
            a["profiles"] = detect_profiles(a["uuids"])
        print(json.dumps(adapters, indent=2))
        return 0

    if not adapters:
        print("No BlueZ adapters present.")
        return 1
    print(f"  {'NAME':<6}  {'BD ADDRESS':<17}  {'STATE':<6}  {'ALIAS':<20}  Profiles")
    print(f"  {'-'*6}  {'-'*17}  {'-'*6}  {'-'*20}  --------")
    for a in adapters:
        h = adapter_health(a["name"])
        state = "OK" if h["ok"] else "DEAD"
        profs = ", ".join(detect_profiles(a["uuids"]))[:40] or "-"
        print(f"  {a['name']:<6}  {a['address']:<17}  {state:<6}  {a['alias']:<20}  {profs}")
        if not h["ok"]:
            print(f"    └─ {h['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
