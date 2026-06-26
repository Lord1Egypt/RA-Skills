#!/usr/bin/env python3
"""bt-contacts — Browse contacts via PBAP from a paired phone.

Examples:
  bt-contacts AA:BB:CC:DD:EE:FF                  # list contacts (first 25 names)
  bt-contacts AA:BB:CC:DD:EE:FF --max 0           # all contacts
  bt-contacts AA:BB:CC:DD:EE:FF --pull            # pull entire phonebook to .vcf
  bt-contacts AA:BB:CC:DD:EE:FF --pull --save-to ./contacts.vcf
  bt-contacts AA:BB:CC:DD:EE:FF --repo sim        # SIM card contacts
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_obex_msg as obex_msg


def main() -> int:
    ap = argparse.ArgumentParser(description="PBAP — phone contacts")
    ap.add_argument("mac")
    ap.add_argument("--repo", default="internal",
                    choices=["internal", "sim"], help="Phone book to read")
    ap.add_argument("--max", type=int, default=25, help="Max contacts (0 = all)")
    ap.add_argument("--pull", action="store_true",
                    help="Pull entire phonebook as .vcf file")
    ap.add_argument("--save-to", help="Output .vcf path (with --pull)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.pull:
        try:
            r = obex_msg.pbap_pull_all_vcards(
                args.mac, repo=args.repo, save_to=args.save_to,
            )
        except Exception as e:
            sys.stderr.write(f"PBAP pull failed: {e}\n")
            return 1
        if args.json:
            print(json.dumps(r, indent=2))
        else:
            print(f"pulled {args.repo} phonebook -> {r['saved_to']}  status={r['status']}")
        return 0 if r["status"] == "complete" else 1

    try:
        contacts = obex_msg.pbap_list_contacts(args.mac, repo=args.repo,
                                                max_count=args.max)
    except Exception as e:
        sys.stderr.write(f"PBAP list failed: {e}\n")
        sys.stderr.write("(phone must have granted Phone Book Access for this host)\n")
        return 1
    if args.json:
        print(json.dumps(contacts, indent=2))
        return 0
    if not contacts:
        print("(empty)")
        return 0
    print(f"  {'HANDLE':<10}  Name")
    for c in contacts:
        print(f"  {c['handle']:<10}  {c['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
