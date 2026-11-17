#!/usr/bin/env python3
"""Pantry moth (Indian meal moth) elimination planner: protocol, disposition, traps, timeline, watch."""
import argparse
from datetime import date, timedelta

FREEZE_DAYS = 4  # -18C, all stages; add margin for thick packs
CYCLE_DAYS = (28, 56)  # warm-kitchen generation time range

DISPOSITION = [
    # (keywords, action, note)
    (["flour", "rice", "oats", "oatmeal", "cereal", "granola", "paste", "noodle",
      "grain", "barley", "quinoa", "cornmeal", "bread crumbs", "breadcrumb"],
     "FREEZE then keep (if no visible webbing/larvae) else TOSS",
     "-18C/0F >= 4 days (a week for thick bags), then glass/metal gasket container"),
    (["nut", "almond", "walnut", "cashew", "peanut", "seed", "birdseed", "trail mix"],
     "FREEZE then keep (if clean) else TOSS",
     "nuts/seeds are TOP import vectors — freeze on arrival always"),
    (["dried fruit", "raisin", "date", "fig", "apricot", "prune"],
     "FREEZE then keep (if clean) else TOSS",
     "sticky-sweet = prime oviposition site; inspect seams"),
    (["pet food", "dog food", "cat food", "kibble", "hamster", "guinea", "rabbit"],
     "FREEZE full bag 4 days; transfer to sealed bin",
     "pet food + birdseed = #1 and #2 import vectors"),
    (["chocolate", "cocoa", "candy", "protein bar"],
     "TOSS if any webbing; else freeze 4 days",
     "chocolate is a classic hidden nursery"),
    (["spice", "tea", "herb", "coffee"],
     "INSPECT: toss any with clumping/webbing; freeze rest",
     "larvae hit red pepper, dried chili, chamomile first"),
    (["sugar", "salt", "baking soda", "baking powder"],
     "KEEP (inspect)",
     "not a food target; sieve if clumped from humidity only"),
    (["canned", "jar", "glass jar", "bottle", "vinegar", "oil", "honey", "syrup"],
     "KEEP — wipe exterior",
     "moths can't enter true seals; wipe jar rims/shelf contact"),
    (["unopened", "sealed box"],
     "SAME RULE as opened: freeze or toss",
     "larvae enter through folded carton seams — cardboard is not a barrier"),
    (["cardboard box", "paper bag", "plastic bag clip"],
     "TOSS packaging after transferring contents",
     "pupae hide in corrugation seams; never re-store in paper/plastic bags"),
]


def cmd_protocol(a):
    lvl = a.level
    print(f"INDIAN MEAL MOTH — {lvl.upper()} infestation protocol")
    print("=" * 46)
    stages = [
        ("DAY 0 — FIND & PULL (do this in one session)",
         ["Pull ALL dry goods from infested zone + adjacent cabinets",
          "Include: unopened boxes, spices, tea, chocolate, ALL pet food/birdseed",
          "Run `disposition` per item; sort into FREEZE / TOSS / KEEP piles",
          "Bag culls in sealed plastic; take OUT to bin immediately"]),
        ("DAY 0 — FREEZE KILL",
         ["Keepers → freezer at -18C/0F for >= 4 days (week for thick bags)",
          "No room? Oven-heat true oven-safe contents 60C/140F for 30 min",
          "After freeze: transfer to glass/metal with gasket lids"]),
        ("DAY 0 — DEEP CLEAN (after pull, same day)",
         ["Vacuum EVERY crack/seam/corner: shelf lips, pins, under-cabinet,",
          "  cabinet-top gap, ceiling corners within 1m, door hinges",
          "Wipe shelves + doors with vinegar or dish-soap water; dry fully",
          "Empty vacuum bag/canister OUTSIDE the house"]),
        ("DAY 1 — TRAPS",
         ["Pheromone traps: one per cabinet zone, eye level, away from drafts/",
          "  windows; never adjacent to each other",
          "Write the placement DATE on each trap with a marker"]),
        ("WEEK 1-6 — WATCH",
         ["Count catch weekly; log day-7 / day-14 / day-30 numbers",
          "Visible moths for ~2 weeks after day 0 = normal tail, not failure",
          "3 consecutive ZERO-catch weeks => declare clean (day ~30-45)"]),
    ]
    extra = {
        "mild": ["Repeat full pull of any cabinet where catch > 0 at day 14"],
        "moderate": ["Check rooms adjacent to kitchen (hallway closet dried flowers,",
                     "  pet food storage); re-run crack vacuum at day 7"],
        "severe": ["Repeat ENTIRE pull+clean at day 14 (missed sources likely)",
                   "Inspect under appliances and inside pantry ceiling voids",
                   "If still >5/week at day 30: licensed pest operator (IPM)"],
    }[lvl]
    for title, steps in stages:
        print(f"\n{title}")
        for s in steps:
            print(f"  - {s}")
    print("\nLEVEL-SPECIFIC:")
    for s in extra:
        print(f"  - {s}")
    print("\nGeneration time 4-8 wks: the protocol runs 6 weeks MINIMUM.")


def cmd_disposition(a):
    q = a.item.lower()
    hits = []
    for kws, action, note in DISPOSITION:
        if any(k in q for k in kws):
            hits.append((action, note))
    if not hits:
        print(f"'{a.item}': no specific rule — default:")
        print("  If dry and animal/plant origin: FREEZE 4d if clean, TOSS if webbing")
        print("  If truly sealed glass/metal/can: KEEP, wipe exterior")
        return
    print(f"'{a.item}':")
    for action, note in hits:
        print(f"  → {action}")
        print(f"    {note}")


def cmd_traps(a):
    n = a.cabinets
    print(f"Pheromone trap plan for {n} cabinet zone(s):")
    print(f"  Count: {max(1, n)} trap(s) — 1 per zone, NOT clustered")
    print()
    print("Placement:")
    print("  - Eye level or slightly above (moths fly up at dusk)")
    print("  - Inside or at mouth of each infested cabinet zone")
    print("  - >= 3 ft apart; never side-by-side (pheromone plumes collide)")
    print("  - Away from windows/doors/drafts that strip the plume")
    print("  - Away from food-prep surfaces (sticky inserts collect dust)")
    print()
    print("Reading them:")
    print("  - Catches MALES only => monitor, not control")
    print("  - Date each trap; count weekly")
    print("  - 0 for 3 consecutive weeks => clean")
    print("  - Replace inserts every 4-6 weeks or when dusty/full")
    print()
    print("Reality check: with all food removed+cleaned, expect catch to")
    print("collapse by day 14. Traps alone NEVER collapse a population.")


def _fmt(d):
    return d.isoformat()


def cmd_timeline(a):
    start = date.fromisoformat(a.start)
    lvl = a.level
    print(f"Timeline from {start} ({lvl}):")
    rows = [
        (0, "Pull + freeze/toss + deep clean + traps out"),
        (4, "Earliest keepers out of freezer (thick bags: day 7)"),
        (7, f"Trap check 1{'; repeat crack-vacuum' if lvl != 'mild' else ''}"),
        (14, "Trap check 2 — the verdict point"),
        (30, "Trap check 3; first possible 'clean' if 3 zero weeks"),
        (42, "Conservative clean date (full generation elapsed)"),
        (56, "Absolute latest: if catch > 0 today, find the missed source"),
    ]
    for off, what in rows:
        print(f"  {_fmt(start + timedelta(days=off))}  +{off:>3}d  {what}")
    print()
    print("Moth-free declaration needs: 3 consecutive zero-catch weeks.")
    print("Any catch after day 21 = a missed food source or new import —")
    print("re-pull the zone before it re-seeds.")


def cmd_watch(a):
    start = date.fromisoformat(a.start)
    print(f"Watch report from {start}:")
    print(f"  day 7  catch: {a.catch_day7}")
    print(f"  day 14 catch: {a.catch_day14}")
    print()
    if a.catch_day7 > 5:
        v = "PROTOCOL GAP — a food source survived day 0. Re-pull the whole"
        v += " zone + re-clean cracks. Do not wait for day 14."
    elif a.catch_day7 > 0:
        v = "ON TRACK (tail) — residual males from pre-pull eggs. Keep"
        v += " watching; verify no NEW webbing anywhere."
    else:
        v = "EXCELLENT — day-7 zero. Continue checks to day 30."
    print(f"  day 7 verdict: {v}")
    print()
    if a.catch_day14 > 1:
        v14 = "MISSED SOURCE — >1 at day 14 means active reproduction."
        v14 += " Full re-pull incl. adjacent rooms/pet food. Severe: re-clean."
    elif a.catch_day14 == 1:
        v14 = "CAUTION — single catch: inspect nearest cabinet seams daily"
        v14 += " for a week; escalate if any further catch."
    else:
        v14 = "PASS — collapse confirmed. Count 3 zero weeks from here."
    print(f"  day 14 verdict: {v14}")
    print()
    clean_earliest = start + timedelta(days=max(30, 14 + 21))
    print(f"  Earliest moth-free declaration: {clean_earliest} (3 zero weeks)")
    print(f"  Conservative (full generation): {start + timedelta(days=42)}")


def main():
    p = argparse.ArgumentParser(description="Pantry moth elimination planner.")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("protocol"); s.add_argument("--level", choices=["mild", "moderate", "severe"], required=True); s.set_defaults(f=cmd_protocol)
    s = sub.add_parser("disposition"); s.add_argument("--item", required=True); s.set_defaults(f=cmd_disposition)
    s = sub.add_parser("traps"); s.add_argument("--cabinets", type=int, default=1); s.set_defaults(f=cmd_traps)
    s = sub.add_parser("timeline"); s.add_argument("--start", required=True); s.add_argument("--level", choices=["mild", "moderate", "severe"], default="moderate"); s.set_defaults(f=cmd_timeline)
    s = sub.add_parser("watch"); s.add_argument("--start", required=True); s.add_argument("--catch-day7", type=int, default=0); s.add_argument("--catch-day14", type=int, default=0); s.set_defaults(f=cmd_watch)
    a = p.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
