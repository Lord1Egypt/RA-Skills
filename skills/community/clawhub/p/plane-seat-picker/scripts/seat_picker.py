#!/usr/bin/env python3
"""Plane Seat Picker — decode seats, dodge traps, pick by flight type.

Stdlib only, offline.

Commands:
  decode   --seat 14C --aircraft a320            position + zone + warns
  aircraft --type 787                            family facts
  choose   --flight red-eye --party N --pref P   ranked strategy
  families --kids infant|toddler|older --adults N
  traps                                          master trap list
"""
import argparse
import sys

AIRCRAFT = {
    "a320": dict(name="A320/321 family (ceo)", layout="3-3", pitch='29-31"',
                 width='18"', facts=["over-wing exits rows ~11-15: row ahead doesn't recline",
                                    "rows 10-17 = engine noise band",
                                    "front rows 1-8 noticeably quieter"]),
    "a320neo": dict(name="A320neo/A321neo", layout="3-3", pitch='29-31"',
                    width='18"', facts=["much quieter than ceo — genuine comfort upgrade",
                                       "A321neo LR long-haul: pick front third"]),
    "737-800": dict(name="737-800", layout="3-3", pitch='29-31"',
                    width='17.2-17.3"', facts=["over-wing exits ~row 14-16: rows 13-14 no recline",
                                              "MAX8 variant quieter; side bins pinch tall heads"]),
    "a220": dict(name="A220-100/-300", layout="2-3", pitch='30-32"',
                 width='18.5-18.9"', facts=["NO bad seat except the 3-block middle",
                                           "couples: take the 2-side (A+C)",
                                           "windows large and low; ride smooth for size"]),
    "e195": dict(name="E175/E195", layout="2-2", pitch='29-31"',
                 width='18.25"', facts=["no middle seats at all",
                                       "row 1 often blank-window",
                                       "back rows bumpier on short fuselage"]),
    "787": dict(name="787-8/9/10", layout="3-3-3", pitch='30-32"',
                width='17.2-17.5"', facts=["narrow seats for cabin length — the top complaint",
                                          "electronic dimming: crew can lock windows dark (bring eyeshade)",
                                          "lower cabin altitude = less fatigue; hydrate"]),
    "a350": dict(name="A350", layout="3-3-3", pitch='31-32"',
                 width='~18"', facts=["very quiet forward of wing",
                                     "some rows have misaligned windows — check airline-specific reviews"]),
    "777": dict(name="777-300ER (3-4-3 dense)", layout="3-4-3", pitch='31-32"',
                width='17.2"', facts=["middle-of-4 (E/F area) = worst economy seat flying",
                                     "2-side pairs (A-C) are the hidden value",
                                     "prefer 2-5-2 or 3-3-3 subfleets if choice exists"]),
    "a380": dict(name="A380", layout="3-4-3 (main)", pitch='31-32"',
                 width='17.5-18"', facts=["UPPER deck (2-4-2) quieter and smaller = best economy experience",
                                         "main deck: boarding wave + more rumble"]),
}

# layout -> position map for letters (standard schemes)
LETTERS = {
    "3-3": {"A": "window (left)", "B": "middle (left)", "C": "aisle (left)",
            "D": "aisle (right)", "E": "middle (right)", "F": "window (right)"},
    "2-3": {"A": "window (2-side)", "C": "aisle (2-side)", "D": "aisle (3-block)",
            "E": "middle (3-block)", "F": "window (3-block)"},
    "2-2": {"A": "window (left)", "C": "aisle (left)", "D": "aisle (right)", "F": "window (right)"},
    "3-3-3": {"A": "window (left)", "B": "middle", "C": "aisle (left)", "D": "aisle (center)",
              "E": "middle (center)", "F": "middle (center)", "G": "aisle (right)",
              "H": "aisle", "J": "middle (right)", "K": "window (right)"},
    "3-4-3": {"A": "window (left)", "B": "middle", "C": "aisle (left)",
              "D": "aisle", "E": "middle (of 4)", "F": "middle (of 4)", "G": "aisle",
              "H": "aisle (right)", "J": "middle (right)", "K": "window (right)"},
    "2-4-2": {"A": "window", "C": "aisle", "D": "aisle", "E": "middle (of 4)",
              "F": "middle (of 4)", "G": "aisle", "H": "aisle", "K": "window"},
}

TRAPS = [
    ("row ahead of exit", "no recline — exit path must stay clear"),
    ("last 2 rows", "limited/no recline + lav/galley halo + meal choice gone"),
    ("lav-adjacent", "door slams + queue hover + light; aisle seat takes bumps all night"),
    ("bulkhead", "no floor storage at feet; armrest trays (fixed, narrower); bassinet zone = babies"),
    ("exit row", "no floor storage T/O+landing; colder at doors; armrest tray; able-bodied only, no lap infants"),
    ("missing window", "787/A350 some rows: blank or misaligned panel — maps rarely mark it"),
    ("over-wing noise band", "engine noise peak + all-wing view; matters >4h flights"),
    ("fake 'preferred' rows", "first econ rows sold as premium are just rows — sometimes bulkhead traps"),
]

STRATEGIES = {
    ("red-eye", 1, "sleep"): [
        "window, front third, >=2 rows from lavs (deplane fast, cart passes early)",
        "A/C: exit row only if you fit armrest trays + cold; otherwise skip",
        "eyeshade regardless (787 windows lock dark crew-side)",
    ],
    ("red-eye", 2, "sleep"): [
        "window+middle together same side, front third",
        "light flight (<80%)? window+aisle gamble — middle fills last",
        "avoid row-ahead-of-exit (no recline) and last 3 rows",
    ],
    ("day", 1, "quiet"): [
        "front third, non-bulkhead, away from galley doors",
        "A220/E195 aircraft = inherently quieter and no-middle or no-bad-seat",
        "over-wing rows only if you ALSO want smooth ride",
    ],
    ("day", 2, "quiet"): [
        "two windows across the aisle (mirror pair) — chat + stretch, no middle",
        "or same-side window+middle for the empty-middle lottery on light flights",
    ],
    ("short-hop", 1, "deplane-fast"): [
        "front third aisle; nothing else matters <2h",
    ],
    ("short-hop", 2, "deplane-fast"): [
        "front pair same side (C+D aisles across = fastest for both)",
    ],
    ("anxious", 1, "calm"): [
        "over-wing window (smoothest ride, horizon reference)",
        "aisle if claustrophobic beats turbulence fear — control wins",
    ],
    ("motion-sickness", 1, "stable"): [
        "over-wing window: center of lift = least motion; horizon visible",
    ],
    ("tall", 1, "legroom"): [
        "exit row or bulkhead genuinely worth paying at 190cm+",
        "avoid row-ahead-of-exit even if cheap — zero recline + knee jam",
    ],
}

FAMILY_NOTES = {
    "infant": [
        "bassinet = bulkhead mounted, limited (2-6/aircraft), reserve AT BOOKING by phone if needed",
        "weight caps ~11-14 kg; length caps apply",
        "lap infant: NO exit rows for the whole party; infant fare ~10% + taxes",
        "bulkhead neighbors chose that row knowingly — the baby-row stigma works FOR you",
        "car seat onboard: approved label + purchased seat + window position (egress rule)",
    ],
    "toddler": [
        "split across the aisle: adult+child window one side, adult opposite",
        "tag-team walks; no trapped stranger next to the toddler",
        "window = entertainment (view + tray table surface)",
        "under-13 must sit with parent on US carriers when booked together — free, claim it",
    ],
    "older": [
        "any window; group splits into 2+2 pairs beat full rows (equipment-change resilience)",
        "exit rows often 15+ only — check before promising a kid the legroom",
    ],
}


def cmd_decode(args):
    fam = args.aircraft.lower().strip()
    if fam not in AIRCRAFT:
        print("aircraft families: " + ", ".join(sorted(AIRCRAFT)))
        return 1
    a = AIRCRAFT[fam]
    seat = args.seat.upper().strip()
    row = "".join(ch for ch in seat if ch.isdigit())
    letter = "".join(ch for ch in seat if ch.isalpha())
    pos = LETTERS.get(a["layout"], {}).get(letter)
    print(f"SEAT {seat} — {a['name']} (econ {a['layout']}, pitch {a['pitch']}, width {a['width']})")
    if pos:
        print(f"  POSITION: {pos}")
    else:
        print(f"  POSITION: letter {letter} not standard for {a['layout']} — check the airline's map (letters drift)")
    try:
        r = int(row)
        if r >= 30:
            print("  ZONE: likely rear third — check last-2-rows trap + lav proximity")
        elif 10 <= r <= 17 and fam in {"a320", "737-800", "a320neo"}:
            print("  ZONE: over-wing band — engine noise; verify exit-row recline traps around it")
        elif r <= 8:
            print("  ZONE: front third — quieter, fast deplaning, early meal choice")
    except ValueError:
        pass
    for f in a["facts"][:2]:
        print(f"  NOTE: {f}")
    return 0


def cmd_aircraft(args):
    fam = args.type.lower().strip()
    if fam not in AIRCRAFT:
        print("aircraft families: " + ", ".join(sorted(AIRCRAFT)))
        return 1
    a = AIRCRAFT[fam]
    print(f"{a['name']}\n  layout {a['layout']} | pitch {a['pitch']} | width {a['width']}")
    for f in a["facts"]:
        print(f"  - {f}")
    return 0


def cmd_choose(args):
    flight = args.flight.lower()
    pref = (args.pref or "default").lower()
    key = (flight, args.party, pref)
    if key not in STRATEGIES:
        # fall back to any matching flight+party
        cands = [k for k in STRATEGIES if k[0] == flight and k[1] == args.party]
        if not cands:
            cands = [k for k in STRATEGIES if k[0] == flight]
        key = cands[0] if cands else None
    if not key:
        print(f"flight types: {sorted({k[0] for k in STRATEGIES})}")
        return 1
    print(f"STRATEGY — {key[0].upper()}, party {key[1]}, pref {key[2]}:\n")
    for i, s in enumerate(STRATEGIES[key], 1):
        print(f"  {i}. {s}")
    return 0


def cmd_families(args):
    kids = args.kids.lower()
    if kids not in FAMILY_NOTES:
        print("kid stages: " + ", ".join(sorted(FAMILY_NOTES)))
        return 1
    print(f"FLYING WITH {args.kids.upper()} ({args.adults} adults):\n")
    for i, n in enumerate(FAMILY_NOTES[kids], 1):
        print(f"  {i}. {n}")
    return 0


def cmd_traps(args):
    print("THE TRAP LIST:\n")
    for i, (name, why) in enumerate(TRAPS, 1):
        print(f"  {i}. {name.upper()} — {why}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("decode")
    d.add_argument("--seat", required=True)
    d.add_argument("--aircraft", required=True)
    d.set_defaults(func=cmd_decode)
    a = sub.add_parser("aircraft")
    a.add_argument("--type", required=True)
    a.set_defaults(func=cmd_aircraft)
    c = sub.add_parser("choose")
    c.add_argument("--flight", required=True)
    c.add_argument("--party", type=int, required=True)
    c.add_argument("--pref")
    c.set_defaults(func=cmd_choose)
    f = sub.add_parser("families")
    f.add_argument("--kids", required=True)
    f.add_argument("--adults", type=int, default=2)
    f.set_defaults(func=cmd_families)
    t = sub.add_parser("traps")
    t.set_defaults(func=cmd_traps)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
