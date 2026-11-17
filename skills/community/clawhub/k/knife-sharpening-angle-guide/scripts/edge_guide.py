#!/usr/bin/env python3
"""Knife sharpening guide: angle-per-class tables, grit ladders from defect
state, hand-holding pass-height math, burr-stage narration, steel decoder,
and stone-gap analysis. Pure stdlib; no network.

Examples:
  python3 edge_guide.py --knife german-chefs --condition very-dull
  python3 edge_guide.py --drawer
  python3 edge_guide.py --heights --blade-mm 45
  python3 edge_guide.py --stones-owned 1000 6000
  python3 edge_guide.py --steel vg10
"""
import argparse
import math

# knife class -> (angle_low, angle_high, default, asymmetry, notes)
KNIVES = {
    "gyuto":          (12, 15, 13, (50, 50), "Japanese double-bevel chef's; thin behind the edge"),
    "santoku":        (12, 15, 14, (70, 30), "often 70/30; check which face is flat"),
    "nakiri/uspasaki":(12, 15, 13, (50, 50), "vegetable push-cutter; keep it thin"),
    "petty/paring":   (15, 17, 15, (50, 50), "small control blade"),
    "german-chefs":   (17, 22, 20, (50, 50), "X50CrMoV15 class; toughness over finesse"),
    "western-santoku":(15, 20, 17, (50, 50), "hybrid; treat per steel hardness"),
    "boning-fillet":  (18, 22, 20, (50, 50), "flex needs a sturdier edge; 15 folds on bone"),
    "deba":           (20, 25, 22, (70, 30), "one-sided mostly; back stays FLAT"),
    "cleaver":        (25, 35, 28, (50, 50), "chopper; never thin this"),
    "pocket-edc":     (20, 25, 22, (50, 50), "edge stability beats razor factor"),
    "bread":          (15, 20, 17, (50, 50), "scallops only; see notes — rod technique, not stones"),
}

CONDITIONS = {
    # condition -> (start grit, ladder description)
    "chipped":     (300, "220-400 (flatten chips, reprofile) -> 800 -> 1000 -> 3000 -> finisher"),
    "very-dull":   (400, "400-800 (re-establish bevel) -> 1000 -> 3000 -> 6000 if polish desired"),
    "dull":        (800, "800 -> 1000 -> 3000; 6000 optional"),
    "refresh":     (1000, "1000 light passes -> 3000/6000 -> strop; often strop alone suffices"),
    "microbevel":  (3000, "3000-6000 micro-bevel pass per side -> strop"),
}

STEELS = {
    "x50crmov15": ("soft German stainless (~54-56 HRC)", "Sharpens fast, burrs big and floppy, dulls fast. Very forgiving; 1000/3000 finishes nicely."),
    "vg10": ("hard Japanese stainless (~60-61 HRC)", "Burrs small and brittle — LIGHT pressure or you snap micro-chips into the edge. Finish 3000-6000."),
    "sg2-r2": ("powdered stainless (~62-64 HRC)", "Slow on natural/aluminum-oxide stones; diamond or CBN plates for heavy work. Tiny stable burr."),
    "aogami-shirogami": ("carbon steel (~61-63 HRC)", "Fast on stones, takes screaming edges, rusts if you sneeze — wipe dry immediately."),
    "s35vn": ("premium powder stainless (~58-61 HRC)", "Abrasion resistant; diamond stones strongly preferred. Burr forms slowly; be patient."),
    "1095": ("simple carbon (~56-58 HRC)", "Easy everywhere; great learner steel. Oil or patina it."),
    "mystery": ("unknown/budget", "Assume soft stainless; if it won't hold any edge after proper sharpening, the knife isn't worth more stones."),
}

FINISH_GRITS = {
    1000: "working toothy edge — great for tomatoes, rope, general EDC",
    3000: "sharp kitchen sweet spot for most cooks",
    6000: "polished push-cut edge; delicate, wants a strop habit",
    8000: "mirror; razor territory, marginal for food release",
}

# what gap each grit band fills
GRIT_BANDS = [
    (220, 400, "repair/reprofile: chips, tip rebuild, setting new angle"),
    (400, 800, "very dull edges; first stone ever; flattening high spots"),
    (800, 1200, "main bevel workhorse: where the edge is actually formed"),
    (1200, 3000, "refinement; removing 1000-grit scratches"),
    (3000, 6000, "polish, push-cut sharpness, micro-bevel stage"),
    (6000, 10000, "cosmetic/pursuit; diminishing cut-performance returns"),
]


def knife_report(name):
    lo, hi, default, (front, back), notes = KNIVES[name]
    print(f"\n{'='*64}\n{name.upper()}  —  {notes}")
    print(f"{'='*64}")
    print(f"  Edge angle per side: {lo}-{hi}°, start at {default}°")
    if (front, back) == (50, 50):
        print(f"  Symmetric 50/50 bevel.")
    else:
        print(f"  FACTORY ASYMMETRY {front}/{back}: pass counts per side must match")
        print(f"  the ratio (e.g. 3 passes front : 2 passes back for 60/40).")
    return default


def ladder_for(condition, angle):
    start, desc = CONDITIONS[condition]
    print(f"\n  GRIT LADDER for condition '{condition}' (start {start}):")
    print(f"    {desc}")
    print(f"    Rule: never jump more than ~3x grit between steps; each stage")
    print(f"    exists to erase the previous stage's scratches.")
    return start


def heights_table(blade_mm):
    print(f"\n{'='*64}\nHAND-ANGLE HEIGHT TABLE (spine height above stone)")
    print(f"blade width {blade_mm} mm\n{'='*64}")
    print(f"  {'Angle':>6} | {'Height':>8} | reference")
    for ang in (12, 13, 15, 17, 20, 22, 25):
        h = blade_mm * math.sin(math.radians(ang))
        ref = ("matchstick" if h < 4 else "two stacked matchsticks" if h < 8
               else "thumb width" if h < 15 else "two thumbs")
        print(f"  {ang:>5}° | {h:>7.1f} mm | {ref}")
    print("\n  Marker trick: color the bevel with a Sharpie; two passes on the")
    print("  stone reveal EXACTLY where you're cutting — shoulder = too high,")
    print("  edge untouched = too low.")


def drawer_report():
    print("FULL DRAWER PLAN (one angle does NOT fit all)")
    print("=" * 64)
    print(f"  {'knife':18s} {'angle':>7s} {'asym':>6s}  notes")
    for name, (lo, hi, d, (f, b), _) in KNIVES.items():
        asym = f"{f}/{b}" if (f, b) != (50, 50) else "sym"
        print(f"  {name:18s} {lo}-{hi}°".ljust(28) + f"{asym:>6s}")
    print("\nSharpen order in one session: cheapest/softest steel first,")
    print("hardest/thinnest last (fresh stone surface for the finesse blade).")


def steel_report(key):
    name, behavior = STEELS[key]
    print(f"\n{key.upper()} — {name}")
    print(f"{'='*64}\n  {behavior}")


def stones_owned_report(owned):
    owned = sorted(set(owned))
    print(f"\nYOUR STONES: {owned}")
    print("=" * 64)
    gaps = []
    for lo, hi, purpose in GRIT_BANDS:
        covered = any(lo <= g <= hi for g in owned)
        if not covered:
            gaps.append((lo, hi, purpose))
    if gaps:
        print("  Coverage gaps:")
        for lo, hi, purpose in gaps:
            print(f"    {lo}-{hi}: {purpose}")
        # recommend the single most useful next stone
        coarse_gaps = [g for g in gaps if g[1] <= 800]
        fine_gaps = [g for g in gaps if g[0] >= 1200]
        if any(800 <= g <= 1200 for g in owned):
            # bevel-forming grit owned -> refine upward next
            if fine_gaps:
                print(f"\n  >> Best next stone: ~{fine_gaps[0][1]} grit ({fine_gaps[0][2]})")
            elif coarse_gaps:
                print(f"\n  >> Best next stone: ~{coarse_gaps[0][1]} grit ({coarse_gaps[0][2]})")
        else:
            print(f"\n  >> Buy first: a ~1000 grit stone. It is where edges are formed;")
            print(f"     everything else is refinement. (Gap purpose: {gaps[0][2]})")
    else:
        print("  Full coverage, no gaps.")
    print("\n  Finish-grit meaning:")
    for g, meaning in FINISH_GRITS.items():
        print(f"    {g}: {meaning}")


def burr_narration():
    print(f"\n{'='*64}\nTHE BURR PROTOCOL (the part everyone skips)")
    print(f"{'='*64}")
    steps = [
        ("Side A passes", "Sharpen side A at your angle, WEIGHT OF KNIFE ONLY, until you feel a burr along the ENTIRE opposite face."),
        ("Check the burr", "Stroke a thumb AWAY from the edge, perpendicular-ish, on side B's face. A burr = faint catch, like a folded foil edge. No catch = keep going."),
        ("Full length", "Burr must run heel to tip. The tip is where people stop early — finish the last 2 cm deliberately."),
        ("Side B mirror", "Same pass count and pressure on side B until a burr forms on A's face."),
        ("Shed the burr", "Alternating LIGHTEST passes (or edge-trailing strokes) until the burr falls off. A remaining wire edge = sharp today, dead tomorrow."),
        ("Strop", "10-20 edge-trailing passes on leather/cardboard (compound optional). This is what makes the edge LAST."),
        ("Test", "Phone-book paper slice, one smooth pull. Snagging = micro-burr or missed spot; tomato skin test for kitchen knives."),
    ]
    for i, (name, how) in enumerate(steps, 1):
        print(f"  {i}. {name}: {how}")


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "Knife sharpening guide").splitlines()[0])
    ap.add_argument("--knife", choices=KNIVES, help="per-knife angle + grit plan")
    ap.add_argument("--condition", choices=CONDITIONS, default="dull",
                    help="edge state (default 'dull')")
    ap.add_argument("--drawer", action="store_true", help="whole-drawer angle table")
    ap.add_argument("--heights", action="store_true", help="hand-angle height table")
    ap.add_argument("--blade-mm", type=float, default=45.0)
    ap.add_argument("--steel", choices=STEELS, help="steel sharpening expectations")
    ap.add_argument("--stones-owned", nargs="*", type=int, default=None,
                    help="your grits, e.g. 1000 6000")
    ap.add_argument("--burr", action="store_true", help="burr protocol narration")
    args = ap.parse_args()

    if not any([args.knife, args.drawer, args.heights, args.steel,
                args.stones_owned is not None, args.burr]):
        args.drawer = True
    if args.knife:
        knife_report(args.knife)
        ladder_for(args.condition, None)
    if args.drawer:
        drawer_report()
    if args.heights:
        heights_table(args.blade_mm)
    if args.steel:
        steel_report(args.steel)
    if args.stones_owned is not None:
        stones_owned_report(args.stones_owned)
    if args.burr:
        burr_narration()
    print()


if __name__ == "__main__":
    main()
