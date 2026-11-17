#!/usr/bin/env python3
"""move_orchestrator.py — plan a household move: timeline, packing waves, box inventory,
truck/crew estimation, moving-day run-of-show, arrival priorities.

Offline, stdlib-only. State: move_state.json beside the script (or --state).
Commands: set | estimate | add-item | plan | waves | box | find | runshow | arrival
Estimates are heuristics from standard household-volume tables; mover quotes override.
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_STATE = Path(__file__).resolve().parent / "move_state.json"

HOME_M3 = {  # home preset -> (light, normal, heavy)
    "studio": (6, 8, 11),
    "1bed": (9, 12, 16),
    "2bed": (14, 18, 23),
    "3bed": (20, 26, 32),
    "4bed": (28, 36, 45),
}
TRUCKS = [  # (name, usable m3)
    ("cargo van", 4), ("10' box truck", 7), ("15' box truck", 10),
    ("20' box truck", 15), ("26' box truck", 22),
]
# common items: name -> (m3 assembled, m3 disassembled-ish, note)
ITEMS = {
    "sofa2": (1.6, 1.3, "legs off"),
    "sofa3": (2.2, 1.7, "legs off; sectional 3-4.5"),
    "bed160": (1.8, 0.9, "disassembled; mattress 0.5-0.7 alone"),
    "bed90": (1.2, 0.6, ""),
    "fridge": (1.2, 1.2, "defrost 48h before; towels in base"),
    "washer": (0.5, 0.5, "drum bolt per manual"),
    "dryer": (0.5, 0.5, ""),
    "dishwasher": (0.4, 0.4, ""),
    "table4": (1.5, 0.9, "dining table + 4 chairs"),
    "desk": (1.0, 0.6, ""),
    "wardrobe": (2.0, 0.5, "flat-pack moves in panels"),
    "tv55": (0.3, 0.3, "blanket or box"),
    "bike": (0.6, 0.4, "front wheel off"),
    "bookshelf": (1.0, 0.4, ""),
}
BOX_KINDS = [("XL 120L", 0.12, 0.8), ("L 75L", 0.075, 1.0), ("M 40L", 0.04, 1.2), ("S 20L", 0.02, 1.5)]

WAVES = [
    ("T-3 wks: storage, guest room, garage/balcony, out-of-season clothes, books",
     ["STO", "GUE", "BOO"],
     "books in SMALL boxes; label ROOM-SEQ now"),
    ("T-2 wks: decor, art, collections, spare electronics, linen excess",
     ["DEC", "ART", "ELE"],
     "art framed/collared; TVs blanket-wrapped"),
    ("T-1 wk: kitchen-daily partial, most clothes, workshop, furniture disassembly",
     ["KIT", "CLO", "WOR"],
     "keep one box of daily dishes out; wardrobe boxes for hanging"),
    ("T-2 days: bedding(1 set out), bathroom(1 set out), last kitchen, cleaning supplies",
     ["BED", "BAT", "KIT", "UTL"],
     "first-night box assembled and SEALED; hardware bags taped to furniture"),
]

FIRST_NIGHT = {
    "bedroom": ["bedding set", "pillow", "phone charger", "change of clothes each"],
    "bathroom": ["toilet paper", "soap", "towel each", "toothbrush", "meds"],
    "kitchen": ["kettle", "mugs", "coffee/tea", "snacks", "cutlery x4", "plates x4",
                 "dish soap + sponge", "bin bags"],
    "utility": ["box cutter", "screwdriver", "allen keys", "masking tape", "marker",
                 "flashlight", "extension cord", "lightbulbs"],
    "kids": ["one comfort toy each"],
    "pets": ["food bowl", "leash", "litter"],
}

PHASES = [
    (56, "T-8wks", ["3 mover quotes (binding)", "elevator slots + truck parking/permits BOTH ends",
                    "declutter wave 1: sell/donate big stuff", "start move file: quotes, leases, meter numbers"]),
    (42, "T-6wks", ["book crew/truck in writing", "order packing materials (estimate +20%)",
                    "declutter wave 2", "address-change list draft"]),
    (28, "T-4wks", ["utilities: OLD stays on through moving day", "new: elec/water at arrival, internet day-after",
                    "insurance: declared value or rider for electronics"]),
    (14, "T-2wks", ["pack waves 1-2 (storage/guest/books/decor)", "fridge/freezer defrost plan (48h)",
                     "kids/pets care for the day", "pharmacy refills"]),
    (7, "T-1wk", ["pack wave 3", "confirm elevator + parking", "cash for tips",
                   "cleaners booked for old place (or plan)", "first-night box assembled"]),
    (2, "T-2days", ["disassemble what's possible; hardware bags TAPED to items",
                     "fridge off+dry, towels in, doors taped ajar", "runshow printed", "shower tonight"]),
    (1, "T-1day", ["stage disassembled items at door", "phone + powerbank charged",
                    "valuable/car manifest finalized"]),
    (0, "MOVING DAY", ["runshow: protect floors -> load heavy first -> car valuables",
                        "final sweep EVERY room", "meter photos", "keys handoff"]),
    (-1, "T+1day", ["beds first, then bathroom, then kitchen basics", "internet installer meet",
                     "address changes fire", "old place walkthrough photos"]),
    (-7, "T+1wk", ["box queue by open-first flags", "donation pickup", "mover damage claims filed"]),
]


def load(state):
    if Path(state).exists():
        return json.loads(Path(state).read_text())
    return {"move": None, "items": [], "boxes": []}


def save(st, state):
    Path(state).write_text(json.dumps(st, indent=2, ensure_ascii=False))


# ------------------------------------------------------------------ commands
def cmd_set(a, st, state):
    st["move"] = {"date": a.date, "from": a.src, "to": a.dst}
    save(st, state)
    d0 = date.fromisoformat(a.date)
    days = (d0 - date.today()).days
    print(f"move set: {a.date} ({days} days out) | {a.src} -> {a.dst}")
    if days < 14 and days >= 0:
        print("!! under 2 weeks: skip to phases T-2wks..T-1day in plan — do them in parallel, today")


def volume_m3(st):
    if st["items"]:
        return sum(i["m3"] for i in st["items"]) * 1.12  # packing air
    return None


def cmd_add_item(a, st, state):
    key = a.item.lower().replace(" ", "")
    if key not in ITEMS:
        print(f"unknown item '{a.item}'. known: {', '.join(ITEMS)}")
        return
    full, flat, note = ITEMS[key]
    m3 = flat if a.flat else full
    if a.qty and a.qty > 1:
        m3 = m3 * a.qty
    st["items"].append({"item": key, "m3": m3, "qty": a.qty or 1, "note": note})
    save(st, state)
    print(f"added {a.qty or 1}x {key} ({m3:.1f} m3) {('- ' + note) if note else ''}")


def cmd_estimate(a, st, state):
    if a.home:
        light, normal, heavy = HOME_M3[a.home]
        m3 = {"light": light, "normal": normal, "heavy": heavy}[a.density]
        basis = f"preset {a.home}/{a.density}"
    else:
        v = volume_m3(st)
        if v is None:
            sys.exit("give --home Xbed --density Y, or add items first with add-item")
        m3 = v
        basis = f"itemized {len(st['items'])} items +12% air"
    truck = next((t for t in TRUCKS if t[1] >= m3 * 1.1), ("MULTI-TRIP 26' x2", 44))
    print(f"ESTIMATE ({basis}): ~{m3:.0f} m3 loaded volume")
    print(f"  truck: {truck[0]} (usable ~{truck[1]} m3; keep 10% headroom)")
    if truck[0] == "MULTI-TRIP 26' x2":
        print("         or: full-service mover with 2 trucks, or purge volume first")
    nboxes = max(8, int(m3 * 1.4))
    kinds = []
    rem = nboxes
    for name, vol, share in BOX_KINDS:
        n = max(2, int(nboxes * share / 4.5))
        kinds.append(f"~{n} {name.split()[0]}")
    print(f"  boxes: ~{nboxes} total ({', '.join(kinds)}) + 8 quilted blankets + sofa cover")
    crew_h = m3 * 0.6
    stairs = 1.0
    if a.stairs:
        stairs = 1.5 + 0.1 * max(a.stairs - 2, 0)
    elev = 1.15 if a.elevator else 1.0
    load_h = crew_h * stairs * elev
    print(f"  crew: 2 pros x {load_h / 2:.0f} h load"
          + (f" (stairs x{stairs:.1f}" + (", elevator x1.15)" if a.elevator else ")")))
    print(f"  friends: 3x x {load_h / 1.5:.0f} h at half pro speed")
    print("  note: piano/safe/marble = rigging pros regardless of this estimate")


def cmd_plan(a, st, state):
    if not st.get("move"):
        sys.exit("run set --date first")
    d0 = date.fromisoformat(st["move"]["date"])
    print(f"MOVE PLAN — {st['move']['date']} | {st['move']['from']} -> {st['move']['to']}")
    print(f"today is T{-(d0 - date.today()).days:+d} ({(d0 - date.today()).days} days to go)\n")
    for days_before, label, tasks in PHASES:
        phase_date = d0 - timedelta(days=days_before) if days_before >= 0 else d0 + timedelta(days=-days_before)
        mark = "[PAST]" if date.today() >= phase_date else "[    ]"
        print(f"{mark} {phase_date}  {label}")
        for t in tasks:
            print(f"      - {t}")
    print("\nlead-time warnings: movers 4-6 wks in season | elevator slots 2 wks |")
    print("internet install slots 2-3 wks | school records transfer 4 wks")


def cmd_waves(a, st, state):
    print("PACKING WAVES (by days-until-needed, not by room convenience):\n")
    for i, (label, rooms, note) in enumerate(WAVES, 1):
        print(f"wave {i}: {label}")
        print(f"   prefixes: {', '.join(rooms)} | {note}\n")
    print("FIRST-NIGHT BOX (travels in the CAR, sealed, list taped on):")
    for room, things in FIRST_NIGHT.items():
        print(f"  {room}: {', '.join(things)}")


def cmd_box(a, st, state):
    b = {"label": a.label, "room": a.room, "priority": a.priority or "normal",
         "contents": a.contents or "", "packed": date.today().isoformat()}
    st["boxes"].append(b)
    save(st, state)
    print(f"box {a.label} [{a.room}] priority={a.priority or 'normal'} :: {a.contents or '(no contents logged)'}")


def cmd_find(a, st, state):
    q = a.term.lower()
    hits = []
    for b in st["boxes"]:
        hay = (b["contents"] + " " + b["label"] + " " + b["room"]).lower()
        if q in hay:
            hits.append(b)
    if not hits:
        print(f"'{a.term}': not in any logged box — check unlogged boxes or the car manifest")
        return
    for b in hits:
        where = "CAR (first-night)" if b["priority"] == "open-first" else "truck"
        print(f"  {b['label']} [{b['room']}] ({where}): {b['contents']}")


def cmd_runshow(a, st, state):
    start = datetime.strptime(a.start, "%H:%M")
    crew = a.crew
    t = start

    def at(mins):
        return (start + timedelta(minutes=mins)).strftime("%H:%M")

    print(f"MOVING-DAY RUN-OF-SHOW — start {a.start}, crew {crew}")
    print("=" * 56)
    steps = [
        (0, "PROTECT: floors + doorframes BOTH ends, banisters, mattress covers on"),
        (15, "STAGE: disassembled items + hardware bags (taped to items) at the door"),
        (30, "LOAD heavy first: washer, fridge (dry, towels in base), sofa (legs off)"),
        (90, "LOAD furniture walls: wardrobes/desk/table strapped; mattresses vertical-ish"),
        (150, "LOAD boxes: heavy-small low+forward, light-large high+rear; strap a wall every layer"),
        (210, "CAR MANIFEST (never truck): docs, jewelry, cash, meds, laptops/chargers,"),
        (211, "   plants, candles(melt), flammables(movers refuse), perishables, FIRST-NIGHT BOX"),
        (240, "DRIVE (fuel checked, phone mounted, playlist chosen)"),
        (300, "UNLOAD reverse: boxes to labeled rooms by prefix, furniture placed first"),
        (420, "REASSEMBLY: beds first (you sleep tonight), then table/desk"),
        (480, "METERS + photos both ends; keys handoff; final sweep checklist per room:"),
        (481, "   closets, wardrobe tops, under beds, balcony/attic/cellar, appliances, mail slot"),
    ]
    for mins, text in steps:
        if mins in (211, 481):
            print(f"        {text}")
        else:
            print(f"{at(mins)}  {text}")
    print()
    print("fatigue window 16:00-18:00: no two-person carries after it if avoidable")
    print("tips: ~5% or $20-40/mover, cash, at the end; water out from the start")


def cmd_arrival(a, st, state):
    print("ARRIVAL — first 24 hours priority order:")
    print("  1. utilities confirmed ON (heat/hot water) — before dark")
    print("  2. beds assembled + made (everything else can wait)")
    print("  3. bathroom essentials + kitchen basics (open-first boxes)")
    print("  4. internet installer meet (slot booked for day-after)")
    print("  5. walk-through photos of NEW place condition (deposit protection)")
    print("  6. fridge plugged, upright 4h before loading (compressor oil)")
    print("\nFIRST-NIGHT BOX manifest (was in the car):")
    for room, things in FIRST_NIGHT.items():
        print(f"  {room}: {', '.join(things)}")
    print("\nFIRST WEEK: box queue by open-first flags; donation pickup for the")
    print("'why did we move this' pile; mover damage claims NOW while evidence fresh.")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", default=str(DEFAULT_STATE))
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("set")
    s.add_argument("--date", required=True, help="YYYY-MM-DD moving day")
    s.add_argument("--from", dest="src", required=True)
    s.add_argument("--to", dest="dst", required=True)

    e = sub.add_parser("estimate")
    e.add_argument("--home", choices=list(HOME_M3))
    e.add_argument("--density", choices=["light", "normal", "heavy"], default="normal")
    e.add_argument("--stairs", type=int, help="flights without elevator")
    e.add_argument("--elevator", action="store_true")

    ai = sub.add_parser("add-item")
    ai.add_argument("item")
    ai.add_argument("--qty", type=int)
    ai.add_argument("--flat", action="store_true", help="disassembled volume")

    sub.add_parser("plan")
    sub.add_parser("waves")

    b = sub.add_parser("box")
    b.add_argument("label", help="e.g. KIT-01")
    b.add_argument("room")
    b.add_argument("--priority", choices=["open-first", "fragile", "heavy", "normal"])
    b.add_argument("--contents")

    f = sub.add_parser("find")
    f.add_argument("term")

    r = sub.add_parser("runshow")
    r.add_argument("--start", default="08:30")
    r.add_argument("--crew", type=int, default=2)

    sub.add_parser("arrival")

    a = p.parse_args()
    st = load(a.state)
    {"set": cmd_set, "estimate": cmd_estimate, "add-item": cmd_add_item,
     "plan": cmd_plan, "waves": cmd_waves, "box": cmd_box, "find": cmd_find,
     "runshow": cmd_runshow, "arrival": cmd_arrival}[a.cmd](a, st, a.state)


if __name__ == "__main__":
    main()
