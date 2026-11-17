---
name: knife-sharpening-angle-guide
description: Use when sharpening kitchen, pocket, or workshop knives (whetstone, guided rod, or pull-through) — matches the correct edge angle to knife class (Japanese 12-15° vs German 20° vs cleaver 25°+), builds the grit-progression ladder from chip repair to polish, computes the physical sharpening-pass height to hold an angle by hand, and explains burr formation/checking so the edge actually gets sharp instead of just shiny.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [knives, sharpening, whetstone, edges, cooking, maintenance, workshop]
---

# Knife Sharpening Angle Guide

## Overview

Sharpening fails for exactly three reasons: wrong angle for the knife class
(a 12° edge on a German chef's knife folds on the first pumpkin), skipped
grits (trying to finish on a 300-grit stone makes a toothy scraper, not an
edge), and never raising a burr (polishing an edge that was never formed).
`scripts/edge_guide.py` holds the lookup tables: per-class target angles,
asymmetric ratios for Japanese blades, grit ladders chosen from your
starting defect, pass-height math ("hold the spine X mm above the stone at
this blade height"), and burr-stage checks per side. It also decodes steel
types into sharpening-feel expectations (soft German steel vs powdered
metallurgy) and pick-a-stone advice from whatever stones you own.

## When to Use

- Knife is dull, chipped, or "sharpened" repeatedly by a pull-through and
  now won't take an edge.
- First time with whetstones; you don't know what angle or grit to use.
- Mixed drawer: German chef's, Japanese gyuto/santoku, paring, bread,
  boning, pocket knives — one angle does not fit all.
- Deciding whether a knife is worth sharpening vs the steel is just bad.
- Restoring a thrift/flea-market find with chips and a heel swale.

**Don't use for:** serrated bread-knife sharpening (rod-and-ceramic per-
scallop technique — different process), scissors (bevel geometry differs),
or axe/machete geometry (much blunter, different domain).

## How It Works

1. **Angle by knife class.** Japanese double-bevel (gyuto, santoku):
    12–15° per side; German/Western chef's: 20° (17 for a thin laser);
    paring 15–17°; boning/fillet flexibility 18–22°; pocket/EDC 20–25°
    (edge stability over sharpness); heavy deba/cleaver 25°+ with a
    hammer-spine left blunt.
2. **Asymmetric ratios.** Many Japanese blades run 70/30 or 80/20 — the
    script tells you passes per side to maintain the factory asymmetry
    rather than accidentally centering it.
3. **Grit ladder from defect state.**
   - Chips or tip repair: 220–400 → 1000 → finisher.
   - Very dull / first stone session: 400–800 → 1000 → 3000–6000 (or 8000
     for polish lovers).
   - Refresh a working edge: 1000 → 3000/6000.
   - The rule the script enforces: never jump more than ~3× grit in one
     step; each stage must remove the previous stage's scratches.
4. **Hold-the-angle math.** Height of the spine above the stone for a
   target angle = blade width × sin(angle). For a 45 mm German knife at
   20°: raise ~15 mm. The script prints a per-knife height table at 15°
   and 20° so hand-sharpeners have a physical reference, plus the
   "matchstick/marker-trick" description.
5. **Burr discipline.** Sharpen one side until a consistent burr forms the
   FULL length (feel by stropping thumb AWAY from edge on the opposite
   face); then mirror passes on side two; then one-lightest-pass alternating
   to shed the burr; then strop. The script narrates the stage checks.
6. **Steel decoder.** Soft stainless (X50CrMoV15 etc.): sharpens fast,
   dulls fast, forgiving. Hard Japanese (VG-10, ~60 HRC): burrs are small
   and brittle — lighter pressure. Powdered steels (SG2/R2, S35VN): slow on
   stones, need diamond/CBN for the burr stage. The script prints
   expectations so you don't misread steel behavior as technique failure.
7. **Stropping + maintenance.** 1–2 µm compound on leather or bare
   cardboard; weekly stropping pushes stone sessions to months apart.
   The honing-rod doctrine: rods realign, stones remove — a rod cannot
   sharpen a dull knife, only postpone the stone.

## Using the Script

```
# angle + grit plan for a German chef's knife, currently very dull
python3 scripts/edge_guide.py --knife german-chefs --condition very-dull

# full drawer plan
python3 scripts/edge_guide.py --drawer

# pass-height table for hand-holding angles
python3 scripts/edge_guide.py --heights --blade-mm 45

# what stones you need if you own these
python3 scripts/edge_guide.py --stones-owned 1000 6000

# steel expectations
python3 scripts/edge_guide.py --steel vg10
```

## Common Pitfalls

1. **One angle for everything.** 15° on a boning knife folds on bone; 25°
   on a gyuto makes it a wedge. Class first, habit second.
2. **Chasing polish without a burr.** If no burr ever formed, no new edge
   geometry exists — the knife will look great and cut nothing. Burr first,
   always, full length.
3. **Skipping grits.** 400 → 8000 leaves 400-grit scratches under a shiny
   bevel: an edge that fails in a week. Max ~3× jumps.
4. **Pushing pressure.** Weight of the knife (plus fingers) only; pressing
   bends the edge away and produces a wire edge that snaps off dull.
5. **Pull-through sharpeners on good knives.** They rip carbide chunks out
   of hard steel and set a sloppy 20°+ micro-bevel. Fine for a $10 beater,
   destructive on VG-10+.
6. **Ignoring asymmetry.** Centering a 70/30 Japanese blade changes its
   steering and food-release behavior; count passes per side.
7. **Testing sharpness wrong.** Paper-slice test (phone-book paper, one
   smooth pull) and tomato-skin test, not the thumb-across-edge gamble.

## Verification Checklist

- [ ] Angle chosen from knife class table (or factory bevel matched).
- [ ] Grit ladder has no >3× jumps from your starting condition.
- [ ] Burr raised full-length on side one BEFORE switching sides.
- [ ] Alternating lightest passes shed the burr; no wire edge remains.
- [ ] Stropped; paper test slices cleanly without snagging.
- [ ] Asymmetric blades: pass counts per side preserved (70/30 etc.).
