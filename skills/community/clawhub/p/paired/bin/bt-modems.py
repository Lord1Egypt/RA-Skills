#!/usr/bin/env python3
"""bt-modems — List ofono modems (1 per HFP-connected phone).

Examples:
  bt-modems              # one-line summary per modem
  bt-modems --json
  bt-modems --watch      # follow modem-add/remove events
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_telephony as bt


def main() -> int:
    ap = argparse.ArgumentParser(description="List ofono modems")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--full", action="store_true",
                    help="Per-modem full state (calls, network, signal)")
    args = ap.parse_args()

    try:
        modems = bt.list_modems()
    except Exception as e:
        sys.stderr.write(f"error: {e}\n")
        sys.stderr.write("(if 'Access denied': /etc/dbus-1/system.d/ofono-${USER}.conf may be missing)\n")
        return 2

    if args.full:
        modems = [bt.modem_state(m["path"]) for m in modems]

    if args.json:
        print(json.dumps(modems, indent=2, default=str))
        return 0

    if not modems:
        print("No ofono modems present. Pair a phone with HFP profile first.")
        print("Steps: bt-pair <phone-mac> --connect; phone needs HFP-AG profile.")
        return 0

    for m in modems:
        path = m["path"]
        powered = m.get("Powered", False)
        online = m.get("Online", False)
        name = m.get("Name", "")
        print(f"{path}")
        print(f"  Name:     {name}")
        print(f"  Powered:  {powered}   Online: {online}")
        ifaces = m.get("Interfaces", [])
        if ifaces:
            print(f"  Interfaces: {', '.join(ifaces)}")
        if "calls" in m:
            print(f"  Calls:    {len(m['calls'])} active")
            for c in m["calls"]:
                print(f"    - {c.get('LineIdentification', '?')} state={c.get('State', '?')}")
        if "network" in m and m["network"]:
            n = m["network"]
            print(f"  Network:  {n.get('Name', '?')} status={n.get('Status', '?')} "
                  f"strength={n.get('Strength', '?')}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
