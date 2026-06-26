#!/usr/bin/env python3
"""bt-adb-battery — accurate battery state via dumpsys.

  bt-adb-battery
  bt-adb-battery --json
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_adb


def main() -> int:
    ap = argparse.ArgumentParser(description="Phone battery via ADB dumpsys")
    ap.add_argument("--serial")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        b = bt_adb.battery(serial=args.serial)
    except Exception as e:
        sys.stderr.write(f"battery failed: {e}\n")
        return 1

    if args.json:
        # Drop raw to keep output clean
        b.pop("raw", None)
        print(json.dumps(b, indent=2))
        return 0

    print(f"Level:        {b['level_pct']}%")
    print(f"Voltage:      {b['voltage_mv']} mV")
    print(f"Temperature:  {b['temperature_c']}°C")
    src = []
    if b["ac_powered"]: src.append("AC")
    if b["usb_powered"]: src.append("USB")
    if b["wireless_powered"]: src.append("wireless")
    print(f"Charging:     {' + '.join(src) if src else 'no (on battery)'}")
    print(f"Technology:   {b.get('technology', '?')}")
    print(f"Health:       {b.get('health', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
