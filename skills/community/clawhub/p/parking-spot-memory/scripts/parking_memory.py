#!/usr/bin/env python3
"""parking_memory.py - remember where you parked and find the car again.

Modes:
  park   - log a parking event (level, row, section, notes, photo ref)
  find   - retrieve the most recent (or named) parking spot + guidance
  expiry - parking-card / meter expiry watch (table of active sessions)
  list   - recent parking history

Storage: ./data/parking_log.json (plain JSON, human-editable).
Zero dependencies (Python 3.8+ stdlib).
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
LOG = os.path.join(DATA_DIR, "parking_log.json")

TIME_FMT = "%Y-%m-%d %H:%M"


def load_log():
    if not os.path.exists(LOG):
        return []
    with open(LOG) as f:
        return json.load(f)


def save_log(log):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOG, "w") as f:
        json.dump(log, f, indent=2)


def parse_when(s):
    return datetime.strptime(s, TIME_FMT)


def fmt(dt):
    return dt.strftime(TIME_FMT)


def elapsed_desc(from_dt):
    delta = datetime.now() - from_dt
    mins = int(delta.total_seconds() // 60)
    if mins < 60:
        return "%d min ago" % mins
    hrs = mins // 60
    return "%dh%02dm ago" % (hrs, mins % 60)


def cmd_park(args):
    log = load_log()
    entry = {
        "ts": fmt(datetime.now()),
        "location": args.location,
        "level": args.level,
        "row": args.row,
        "section": args.section,
        "plate": args.plate,
        "photo": args.photo,
        "notes": args.notes,
        "paid_until": args.paid_until,
        "tz": args.tz,
    }
    log.append(entry)
    save_log(log)
    print("Parked logged: %s" % fmt(datetime.now()))
    print("  location : %s" % (args.location or "(none)"))
    bits = []
    for k in ("level", "row", "section"):
        v = getattr(args, k)
        if v:
            bits.append("%s=%s" % (k, v))
    if bits:
        print("  position : %s" % ", ".join(bits))
    if args.paid_until:
        print("  paid until: %s" % args.paid_until)
    if args.photo:
        print("  photo    : %s" % args.photo)
    if args.notes:
        print("  notes    : %s" % args.notes)
    return 0


def _find_latest(log, location=None):
    for e in reversed(log):
        if location is None or location.lower() in e.get("location", "").lower():
            return e
    return None


def cmd_find(args):
    log = load_log()
    if not log:
        sys.exit("no parking log yet - run `park` when you leave the car")
    e = _find_latest(log, args.location)
    if not e:
        sys.exit("no parking entry matching %r" % args.location)
    print("Last parked: %s (%s)" % (e["ts"], elapsed_desc(parse_when(e["ts"]))))
    print("  location : %s" % (e.get("location") or "(none recorded)"))
    for k in ("level", "row", "section", "plate"):
        if e.get(k):
            print("  %-8s: %s" % (k, e[k]))
    if e.get("paid_until"):
        print("  paid until: %s" % e["paid_until"])
    if e.get("photo"):
        print("  photo    : %s (review aisle markers vs the photo)" % e["photo"])
    if e.get("notes"):
        print("  notes    : %s" % e["notes"])
    print()
    print("Finding tips:")
    if e.get("level"):
        print("  - Head to level %s first; elevator banks are usually near rows' start." % e["level"])
    if e.get("row"):
        print("  - Walk row %s checking plate/sticker landmarks." % e["row"])
    if e.get("paid_until"):
        print("  - Meter/card expires %s - check if you owe before leaving." % e["paid_until"])
    print("  - Key fob panic button range improves near metal ceilings (multi-storey).")
    return 0


def cmd_expiry(args):
    log = load_log()
    now = datetime.now()
    any_active = False
    for e in log[-30:]:
        if not e.get("paid_until"):
            continue
        try:
            until = parse_when(e["paid_until"])
        except ValueError:
            print("  (unparseable paid_until in entry %s)" % e["ts"])
            continue
        if until + timedelta(hours=args.grace) < now:
            continue
        any_active = True
        left = until - now
        mins = int(left.total_seconds() // 60)
        if mins < 0:
            print("EXPIRED %d min ago | %s | %s" % (-mins, e.get("location", "?"), e["ts"]))
        else:
            flag = "LOW" if mins < 30 else "ok "
            print("%s %4d min left | %s" % (flag, mins, e.get("location", "?")))
    if not any_active:
        print("No active/expiring paid sessions in the last 30 entries.")
    return 0


def cmd_list(args):
    log = load_log()
    if not log:
        sys.exit("no parking log yet")
    n = args.n
    print("Last %d parking events:" % min(n, len(log)))
    for e in log[-n:][::-1]:
        pos = " ".join("%s=%s" % (k, e[k]) for k in ("level", "row", "section") if e.get(k))
        print("  %s  %s  %s" % (e["ts"], (e.get("location") or "?")[:30], pos))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode", required=True)

    sp = sub.add_parser("park", help="log where you parked now")
    sp.add_argument("--location", default=None, help="e.g. 'Airport T2 garage'")
    sp.add_argument("--level", default=None)
    sp.add_argument("--row", default=None)
    sp.add_argument("--section", default=None)
    sp.add_argument("--plate", default=None)
    sp.add_argument("--photo", default=None, help="path/reference to a photo")
    sp.add_argument("--notes", default=None, help="landmarks, exits, anything")
    sp.add_argument("--paid-until", default=None, help="'YYYY-MM-DD HH:MM'")
    sp.add_argument("--tz", default=None)
    sp.set_defaults(func=cmd_park)

    sp = sub.add_parser("find", help="where did I park?")
    sp.add_argument("--location", default=None, help="filter by location substring")
    sp.set_defaults(func=cmd_find)

    sp = sub.add_parser("expiry", help="active paid-parking sessions")
    sp.add_argument("--grace", type=int, default=1,
                    help="hours of grace to still show expired (default 1)")
    sp.set_defaults(func=cmd_expiry)

    sp = sub.add_parser("list", help="recent parking history")
    sp.add_argument("-n", type=int, default=10)
    sp.set_defaults(func=cmd_list)

    args = p.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
