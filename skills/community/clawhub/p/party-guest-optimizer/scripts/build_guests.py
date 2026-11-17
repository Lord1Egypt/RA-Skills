#!/usr/bin/env python3
"""Guest JSON builder — interactive prompts producing guest_optimizer.py input.

Tolerates blanks, validates ids. Run:
    python3 build_guests.py -o party.json
"""
import argparse
import json
import sys
from pathlib import Path


def q(prompt: str, cast=str, optional=False, choices=None):
    while True:
        try:
            raw = input(prompt).strip()
        except EOFError:
            return None
        if raw == "" and optional:
            return None
        if raw == "":
            continue
        if choices and raw not in choices:
            print("  choose one of: " + ", ".join(choices))
            continue
        try:
            return cast(raw)
        except ValueError:
            print(f"  enter a valid value")
            continue


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="party.json")
    args = ap.parse_args()
    print("Guest builder — blank line to skip an optional field.")
    guests, ids = [], []
    n = q("How many guests? ", int) or 0
    for i in range(n):
        print(f"\n--- guest {i+1}/{n} ---")
        gid = q("  id (short name): ") or f"guest{i+1}"
        while gid in ids:
            gid = q("  already used — another id: ") or gid + "2"
        ids.append(gid)
        talker_s = q("  talker 1(listener)-5(dominant) [3]: ", optional=True)
        talker = int(talker_s) if talker_s and talker_s.isdigit() else 3
        talker = min(5, max(1, talker))
        ints_raw = q("  interests (comma-sep): ", optional=True) or ""
        interests = [x.strip().lower() for x in ints_raw.split(",") if x.strip()]
        guests.append({"id": gid, "talker": talker, "interests": interests})
    edges = []
    print("\n--- relationships (blank 'from' to stop) ---")
    while True:
        a = q("  from: ", optional=True)
        if not a:
            break
        b = q("  with: ") or ""
        if b not in ids or a not in ids:
            print("  unknown id")
            continue
        etype = q("  type (close/know/tension/ex): ",
                  choices=["close", "know", "tension", "ex"])
        if etype:
            edges.append({"a": a, "b": b, "type": etype})
    keep = []
    print("\n--- keep-apart pairs (blank first to stop) ---")
    while True:
        a = q("  first: ", optional=True)
        if not a:
            break
        b = q("  second: ") or ""
        if a in ids and b in ids and a != b:
            keep.append([a, b])
    must = []
    print("\n--- must-invite ids (blank to stop) ---")
    while True:
        m = q("  id: ", optional=True)
        if not m:
            break
        if m in ids and m not in must:
            must.append(m)
    data = {"guests": guests, "edges": edges, "keep_apart": keep,
            "must_invite": must}
    Path(args.out).write_text(json.dumps(data, indent=2))
    print(f"\nwrote {args.out} — {len(guests)} guests, {len(edges)} edges, "
          f"{len(keep)} keep-apart, {len(must)} must")
    return 0


if __name__ == "__main__":
    sys.exit(main())
