#!/usr/bin/env python3
"""bt-gatt — Read / write GATT characteristics on a connected BLE device.

Examples:
  bt-gatt-read  AA:BB:CC:DD:EE:FF 00002a19-0000-1000-8000-00805f9b34fb   # battery level
  bt-gatt-write AA:BB:CC:DD:EE:FF 0000xxxx-... DEADBEEF                   # hex payload
  bt-gatt-tree  AA:BB:CC:DD:EE:FF                                         # show all services + chars
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt_lib import (gatt_read, gatt_write, list_gatt_tree, get_device,
                    adapter_health)


def hex_to_bytes(s: str) -> bytes:
    s = s.replace(" ", "").replace("0x", "").replace(":", "")
    if len(s) % 2:
        s = "0" + s
    return bytes.fromhex(s)


def main() -> int:
    invoked = Path(sys.argv[0]).name
    if "tree" in invoked:
        op = "tree"
    elif "write" in invoked:
        op = "write"
    else:
        op = "read"

    ap = argparse.ArgumentParser(description=f"GATT {op}")
    ap.add_argument("mac")
    if op != "tree":
        ap.add_argument("char_uuid")
    if op == "write":
        ap.add_argument("payload_hex", help="Hex string, e.g. 'DEADBEEF' or '01:02:03'")
        ap.add_argument("--no-response", action="store_true",
                        help="Write without response (faster, no ack)")
    ap.add_argument("--adapter", default="hci0")
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
    if not d.get("connected"):
        sys.stderr.write(f"error: {args.mac} is not connected. Run bt-connect first.\n")
        return 1

    if op == "tree":
        tree = list_gatt_tree(args.mac, args.adapter)
        if not tree:
            print("No GATT services discovered yet — wait a few seconds and retry.")
            return 1
        for svc_uuid, sv in tree.items():
            print(f"service {svc_uuid}")
            for c_uuid, ch in sv["characteristics"].items():
                print(f"  char {c_uuid}  flags={','.join(ch['flags'])}")
                for du, _dv in ch["descriptors"].items():
                    print(f"    desc {du}")
        return 0

    if op == "read":
        try:
            v = gatt_read(args.mac, args.char_uuid, args.adapter)
        except RuntimeError as e:
            sys.stderr.write(f"read failed: {e}\n")
            return 1
        try:
            text = v.decode("utf-8")
            ascii_repr = text if all(32 <= ord(c) < 127 for c in text) else None
        except UnicodeDecodeError:
            ascii_repr = None
        print(f"hex:   {v.hex()}")
        if ascii_repr:
            print(f"ascii: {ascii_repr!r}")
        print(f"bytes: {len(v)}")
        return 0

    if op == "write":
        payload = hex_to_bytes(args.payload_hex)
        try:
            gatt_write(args.mac, args.char_uuid, payload,
                       adapter=args.adapter,
                       with_response=not args.no_response)
        except RuntimeError as e:
            sys.stderr.write(f"write failed: {e}\n")
            return 1
        print(f"wrote {len(payload)} bytes ({'with' if not args.no_response else 'no'} response)")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
