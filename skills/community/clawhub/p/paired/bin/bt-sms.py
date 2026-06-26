#!/usr/bin/env python3
"""bt-sms — Send / list SMS through a paired phone.

Examples:
  bt-sms-send 07911123456 "running 5 mins late"
  bt-sms-send 07911123456 "hi" --modem AA:BB:..        # specific phone
  bt-sms-send 07911123456 "hi" --via-map               # use MAP not ofono
  bt-sms-list                                          # ofono outgoing queue
  bt-sms-list --map AA:BB:CC:DD:EE:FF                  # MAP inbox (first 25)
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_telephony as bt
import bt_obex_msg as obex_msg


def main() -> int:
    invoked = Path(sys.argv[0]).name
    op = "list" if "list" in invoked else "send"

    ap = argparse.ArgumentParser(description=f"SMS {op}")
    if op == "send":
        ap.add_argument("number")
        ap.add_argument("text")
        ap.add_argument("--modem", help="Phone MAC (default: first ofono modem)")
        ap.add_argument("--via-map", action="store_true",
                        help="Use OBEX MAP instead of ofono (rarely needed)")
    else:
        ap.add_argument("--modem", help="Phone MAC for ofono outgoing list")
        ap.add_argument("--map", dest="map_mac",
                        help="Show MAP inbox/outbox for this paired phone MAC")
        ap.add_argument("--folder", default="telecom/msg/inbox",
                        help="MAP folder, default telecom/msg/inbox")
        ap.add_argument("--max", type=int, default=25)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if op == "send":
        if args.via_map:
            if not args.modem:
                sys.stderr.write("--via-map needs --modem MAC of paired phone\n")
                return 2
            try:
                r = obex_msg.map_send_message(args.modem, args.number, args.text)
            except Exception as e:
                sys.stderr.write(f"MAP send failed: {e}\n")
                return 1
            (print(json.dumps(r, indent=2)) if args.json
             else print(f"MAP push: {r['status']}"))
            return 0 if r["status"] == "complete" else 1

        # ofono path
        modems = bt.list_modems()
        if not modems:
            sys.stderr.write("No ofono modem. Pair a phone with HFP first.\n")
            return 2
        modem = bt.modem_for_mac(args.modem) if args.modem else modems[0]
        if modem is None:
            sys.stderr.write(f"no ofono modem matches MAC {args.modem}\n")
            return 1
        ifaces = modem.get("Interfaces", [])
        if "org.ofono.MessageManager" not in ifaces:
            sys.stderr.write(
                f"This phone does not expose SMS via Bluetooth.\n"
                f"Modem interfaces present: {', '.join(ifaces) or '(none)'}\n"
                f"\nMost modern Samsung/iOS phones disable HFP MessageManager\n"
                f"and require MAP (Message Access Profile) which they don't expose\n"
                f"to non-Samsung-Account paired devices. SMS-send via BT is not possible\n"
                f"on this phone with default settings.\n"
            )
            return 3
        try:
            mpath = bt.sms_send(modem["path"], args.number, args.text)
        except Exception as e:
            sys.stderr.write(f"sms_send failed: {e}\n")
            return 1
        if args.json:
            print(json.dumps({"message_path": mpath, "modem": modem["path"]}, indent=2))
        else:
            print(f"sent: {mpath}")
        return 0

    # list path
    if args.map_mac:
        try:
            msgs = obex_msg.map_list_messages(args.map_mac,
                                               folder=args.folder,
                                               max_count=args.max)
        except Exception as e:
            sys.stderr.write(f"MAP list failed: {e}\n")
            return 1
        if args.json:
            print(json.dumps(msgs, indent=2))
            return 0
        if not msgs:
            print(f"(empty: {args.folder})")
            return 0
        for m in msgs:
            sender = m.get("Sender") or m.get("SenderAddress") or "?"
            ts = m.get("Timestamp", "?")
            subj = m.get("Subject") or "(no subject)"
            mtype = m.get("Type", "")
            read = " [READ]" if m.get("Read") == "1" else "      "
            print(f"  {ts}{read}  {sender:<20.20}  {mtype:<8}  {subj}")
        return 0

    # ofono outgoing queue
    modems = bt.list_modems()
    if not modems:
        sys.stderr.write("No ofono modem.\n")
        return 2
    modem = bt.modem_for_mac(args.modem) if args.modem else modems[0]
    ifaces = modem.get("Interfaces", [])
    if "org.ofono.MessageManager" not in ifaces:
        if args.json:
            print(json.dumps({"error": "modem has no MessageManager interface", "interfaces": ifaces}, indent=2))
        else:
            print(f"Modem {modem['path']} does not expose MessageManager.")
            print(f"Interfaces: {', '.join(ifaces) or '(none)'}")
        return 3
    msgs = bt.sms_list_outgoing(modem["path"])
    if args.json:
        print(json.dumps(msgs, indent=2))
    else:
        if not msgs:
            print("no pending outgoing messages")
        for m in msgs:
            print(f"  {m['path']}  state={m.get('State', '?')}  "
                  f"to={m.get('Recipient', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
