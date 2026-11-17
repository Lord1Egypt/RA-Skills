#!/usr/bin/env python3
"""Hotel room protective sweep: bedbug inspection, hidden-camera hotspots,
valuables/exit audit, and evidence logging with escalation letters.

Pure stdlib. Data lives in a JSON log next to the script (or --data PATH).

Examples:
  python3 room_sweep.py --sweep
  python3 room_sweep.py --sweep --camera-focus
  python3 room_sweep.py --log --room 407 --property "Riverside Inn" \
      --finding "fecal smear clusters, mattress piping head end" --photos 3
  python3 room_sweep.py --letter --room 407 --property "Riverside Inn"
"""
import argparse
import json
import os
import sys
from datetime import datetime

BEDBUG_STEPS = [
    ("Luggage discipline", "Luggage in bathtub or on the rack. NOT on bed/floor/sofa until sweep done."),
    ("Strip head of bed", "Pull sheets toward foot; mattress pad stays as a tray for anything that falls."),
    ("Mattress seams + piping", "Fingertip along EVERY seam, both sides, corners doubled. Look: apple-seed adults (4-5mm), marker-dot fecal clusters, translucent eggs (1mm), amber casings."),
    ("Box spring", "Underside, corner guards, peel mesh if possible. #1 harbor in established rooms."),
    ("Headboard", "Remove if hinged. Screw holes, wall gap, tufts/seams on cloth boards."),
    ("Frame + legs + joints", "Joint crevices, caster mounts, anywhere wood meets wood."),
    ("Nightstands", "Top drawer first, drawer rails, behind and under. Wall art above bed, its backing."),
    ("Luggage rack", "Fold joints and webbing seams — your bags ride here."),
    ("Room perimeter", "Baseboard seams, carpet edge under bed, curtain hems, plugs/jacks near head of bed."),
]

CAMERA_STEPS = [
    ("Dark the room", "Lights off, blinds closed. Phone flashlight ready."),
    ("Line-of-sight doctrine", "Stand at bed, then in bathroom: what can SEE you? Only those objects matter."),
    ("Smoke detector", "Classic host. Lens glint sweep of its face; check for a second, fake one."),
    ("Clock radio / display", "Any pinhole dot facing the bed. Glint sweep the front face."),
    ("Chargers + plugs", "USB bricks and wall plugs at chest height facing bed/bath; glint sweep."),
    ("Vent grilles + detector discs", "Flashlight ACROSS the grille at an angle; look for reflections."),
    ("Decor with a view", "Pictures, shelves, air fresheners, power strips aimed at bed/bath."),
    ("Network (optional)", "If router is disclosed: unexpected always-on devices with heavy traffic get a physical look."),
]

HOTSPOT_SCORES = {
    "smoke-detector": 4, "clock-radio": 4, "usb-charger": 3, "wall-plug": 3,
    "vent-grille": 3, "motion-disc": 3, "power-strip": 2, "picture-frame": 2,
    "shelf-object": 2, "tv-box": 2, "mirror-edge": 1, "hair-dryer": 1,
}

VERDICTS = {
    "live": "LIVE BUGS/EGGS — established colony. Do not unpack. Demand a room on a DIFFERENT floor/wing (not adjacent), or leave.",
    "signs": "SIGNS ONLY (fecal/casings) — treat as infested until proven otherwise. Different room, not adjacent; bag and heat-treat clothes on return home.",
    "clean": "NO SIGNS — unpack; keep luggage on the rack, away from the bed, all stay.",
}


def load_log(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"entries": []}


def save_log(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def print_block(title, steps, focus=False):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)
    for i, (name, how) in enumerate(steps, 1):
        print(f"  {i:2d}. {name}")
        for line in how.split(". "):
            line = line.strip()
            if line:
                print(f"      {line}." if not line.endswith(".") else f"      {line}")
    if focus:
        print("\n  VERDICT KEY:")
        for k, v in VERDICTS.items():
            print(f"    - {k.upper()}: {v}")


def cmd_sweep(args):
    print("HOTEL ROOM SWEEP — first 15 minutes, before unpacking")
    print(f"Started: {datetime.now():%Y-%m-%d %H:%M}")
    print_block("PART 1 — BEDBUG SWEEP (in order, most-likely first)", BEDBUG_STEPS, focus=True)
    print_block("PART 2 — CAMERA CHECK (darkness + line-of-sight)", CAMERA_STEPS)
    print("\n" + "=" * 64)
    print("PART 3 — SECURITY / COMFORT / VALUABLES")
    print("=" * 64)
    checks = [
        ("Door", "Lock + deadbolt + chain work; peephole clear (cover if unshielded)."),
        ("Exits", "Count fire exits; walk the route once; in smoke you navigate by wall."),
        ("Safe", "Bolted down (not portable), lock cycles, laptop fits. Portable safe = on your body instead."),
        ("Valuables", "Passport/meds/spare cash: safe or body. NEVER drawers (staff-accessible)."),
        ("Phone", "Reaches front desk; note the internal dial prefix."),
        ("Window", "Locks; ground-floor note; AC actually cools."),
    ]
    for i, (name, how) in enumerate(checks, 1):
        print(f"  {i:2d}. {name}: {how}")
    print("\nIf ANYTHING is found:  python3 room_sweep.py --log --finding \"...\" "
          "--room N --property NAME --photos K")
    print("then:                   python3 room_sweep.py --letter --room N --property NAME")


def cmd_log(args):
    path = args.data
    data = load_log(path)
    entry = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "room": args.room or "?",
        "property": args.property or "?",
        "finding": args.finding,
        "photos": args.photos,
        "guest": args.guest or os.environ.get("USER", "guest"),
    }
    data["entries"].append(entry)
    save_log(path, data)
    print(f"Logged [{entry['ts']}] room {entry['room']} @ {entry['property']}:")
    print(f"  finding: {entry['finding']}")
    print(f"  photos:  {entry['photos']}")
    print(f"Saved to {path} ({len(data['entries'])} entries).")
    f = args.finding.lower()
    if any(w in f for w in ("bug", "egg", "live", "casing", "larva", "nymph")):
        print("\n" + VERDICTS["live"])
    elif any(w in f for w in ("fecal", "smear", "stain", "blood", "bite")):
        print("\n" + VERDICTS["signs"])
    if "camera" in f or "lens" in f or "device" in f:
        print("\nCAMERA: Do NOT disconnect. Photograph in place, call police non-emergency, then the property.")


def cmd_hotspots(args):
    print("CAMERA HOTSPOT RISK TABLE (where cameras are actually found)")
    print("-" * 64)
    for spot, score in sorted(HOTSPOT_SCORES.items(), key=lambda kv: -kv[1]):
        bar = "#" * score
        print(f"  {spot:16s} risk {score}/4  {bar}")
    print("\nRule: risk matters only WITH a bed/bath line-of-sight and power.")


def cmd_letter(args):
    data = load_log(args.data)
    mine = [e for e in data["entries"]
            if (not args.room or e["room"] == args.room)
            and (not args.property or e["property"] == args.property)]
    if not mine:
        sys.exit("No logged findings for that room/property — log first with --log.")
    today = datetime.now().strftime("%B %d, %Y")
    prop = args.property or mine[0]["property"]
    lines = [
        f"To: Management, {prop}",
        f"Date: {today}",
        "",
        "RE: Room condition — formal complaint and request for remedy",
        "",
        "On check-in I performed a standard room-condition inspection and documented the following:",
        "",
    ]
    for e in mine:
        lines.append(f"  [{e['ts']}] {e['finding']} ({e['photos']} timestamped photos taken)")
    lines += [
        "",
        "I request the following, in order:",
        "  1. Immediate transfer to a comparable room in a different part of the property (not adjacent to the affected room),",
        "     at no charge, including assistance moving belongings.",
        "  2. Full refund or comp of the affected night(s) at issue.",
        "  3. Written confirmation of the property's pest-control inspection date for the affected room, or",
        "     a police report reference number if the finding was a recording device.",
        "  4. Laundry/dry-cleaning credit for all clothing exposed in the affected room.",
        "",
        "This correspondence and my photographic evidence are retained. Please respond within 24 hours",
        "before I escalate to [booking platform] and [local health/licensing authority].",
        "",
        "Sincerely,",
        args.guest or "[guest name]",
    ]
    letter = "\n".join(lines)
    print(letter)
    if args.out:
        with open(args.out, "w") as f:
            f.write(letter + "\n")
        print(f"\n-- saved to {args.out}", file=sys.stderr)


LEGACY_FLAGS = {"--sweep": "sweep", "--log": "log", "--letter": "letter",
                "--hotspots": "hotspots"}


def main():
    # accept legacy style: room_sweep.py --sweep ... -> room_sweep.py sweep ...
    argv = sys.argv[1:]
    if argv and argv[0] in LEGACY_FLAGS:
        argv[0] = LEGACY_FLAGS[argv[0]]
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep_log.json"),
                    help="evidence log JSON path")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sweep", help="print the guided 15-minute sweep")
    s.add_argument("--camera-focus", action="store_true")
    sub.add_parser("hotspots", help="camera hotspot risk table")
    lg = sub.add_parser("log", help="log a finding")
    lg.add_argument("--finding", required=True)
    lg.add_argument("--room"), lg.add_argument("--property")
    lg.add_argument("--photos", type=int, default=0)
    lg.add_argument("--guest")
    lt = sub.add_parser("letter", help="draft escalation letter from log")
    lt.add_argument("--room"), lt.add_argument("--property")
    lt.add_argument("--guest")
    lt.add_argument("--out", help="also write letter to this file")
    args = ap.parse_args(argv)
    {"sweep": cmd_sweep, "hotspots": cmd_hotspots,
     "log": cmd_log, "letter": cmd_letter}[args.cmd](args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
