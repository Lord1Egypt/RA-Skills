#!/usr/bin/env python3
"""bt-adb-sms — SMS read/send via ADB (works around Samsung MAP-send block).

  bt-adb-sms-list                       # last 20 inbox SMS
  bt-adb-sms-list --limit 50
  bt-adb-sms-list --sent                # sent folder
  bt-adb-sms-list --json
  bt-adb-sms-send 07911123456 "hi"      # opens SMS app pre-populated; user taps send
  bt-adb-sms-send 07911... "hi" --silent  # try service call (often denied on user devices)
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_adb


def main() -> int:
    invoked = Path(sys.argv[0]).name
    if "send" in invoked:
        ap = argparse.ArgumentParser(description="Send SMS via ADB")
        ap.add_argument("number")
        ap.add_argument("text")
        ap.add_argument("--silent", action="store_true",
                        help="Try service-call SMS send (often denied — needs default-SMS-app)")
        ap.add_argument("--serial")
        ap.add_argument("--json", action="store_true")
        args = ap.parse_args()
        try:
            if args.silent:
                r = bt_adb.sms_send_silent(args.number, args.text, serial=args.serial)
            else:
                r = bt_adb.sms_send(args.number, args.text, serial=args.serial)
        except Exception as e:
            sys.stderr.write(f"send failed: {e}\n")
            return 1
        if args.json:
            print(json.dumps(r, indent=2))
        else:
            print(f"method: {r['method']}")
            if r.get("note"):
                print(f"note:   {r['note']}")
            print("→ tap Send on the phone to deliver")
        return 0

    # list
    ap = argparse.ArgumentParser(description="List SMS via ADB")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--sent", action="store_true",
                    help="Sent folder instead of inbox")
    ap.add_argument("--serial")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        msgs = (bt_adb.sms_sent(limit=args.limit, serial=args.serial)
                if args.sent
                else bt_adb.sms_inbox(limit=args.limit, serial=args.serial))
    except Exception as e:
        sys.stderr.write(f"list failed: {e}\n")
        return 1

    if args.json:
        print(json.dumps(msgs, indent=2))
        return 0

    if not msgs:
        print("(empty)")
        return 0
    print(f"  {'WHEN':<19}  {'FROM':<22}  Body")
    print(f"  {'-'*19}  {'-'*22}  ----")
    for m in msgs:
        ts = m.get("timestamp") or "?"
        addr = (m.get("address") or "?")[:22]
        body = (m.get("body") or "").replace("\n", " ")[:80]
        print(f"  {ts:<19}  {addr:<22}  {body}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
