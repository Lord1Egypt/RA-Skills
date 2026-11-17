---
name: lawn-calendar-chemist
description: "Use when planning lawn care timing and products: soil-temperature windows for pre-emergent crabgrass control, N-P-K fertilizer math from bag guarantees, seeding vs pre-emergent conflicts, and a region-adjusted annual calendar. Prevents the two classic mistakes — applying too late and over-fertilizing."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [lawn-care, fertilizer, crabgrass, pre-emergent, soil-temperature, gardening]
---

# Lawn Calendar & Chemist

## Overview

Lawn care fails on **timing and dose**, not effort. Pre-emergent crabgrass control works
only before germination — which is driven by **soil temperature (4 consecutive days ≥55°F
at 2" depth)**, not by calendar dates or forsythia bloom. And fertilizer burn/waste comes
from ignoring what the bag guarantee actually contains per bag and per 1000 sq ft. This
skill converts your location, grass type, and soil-temp observations (or seasonal
estimates) into a **dated application calendar**, computes exact **product dose from bag
guarantees**, and catches the fatal conflicts (pre-emergent kills new seed; urea +
temperature >85°F burns cool-season grass).

## When to Use

- "When do I apply crabgrass preventer?" / "Is it too late for pre-emergent?"
- Building the whole-season plan: pre-emergent ×2, fertilizer rounds, seeding, aeration
- Deciding how much product to buy / spreader settings from N-P-K guarantees
- Overseeding timing vs pre-emergent conflict resolution
- "My lawn is yellow/burned" — fertilizer misapplication triage

**Don't use for:** irrigation design, soil-test interpretation beyond N-P-K basics (send
to extension service — the skill tells you when), or pesticide selection beyond pre/post
emergent herbicide classes.

## The Physics of Timing

- **Crabgrass germinates at soil 55°F (13°C) for 4+ consecutive days at 2-inch depth** —
  typically when soil hits 55°F for a week. Air temp is a poor proxy (soil lags air by
  ~1-2 weeks in spring). Apply pre-emergent when soil is **50-55°F and rising**, usually
  2-4 weeks before your last frost.
- **Soil temp estimation:** soil ≈ weekly mean air temp lagged ~10 days, minus 2-3°F.
  The script takes your 7-day mean air temp + date and estimates soil temp with a
  seasonal lag model — but a $10 soil thermometer beats any model.
- **Pre-emergent + seeding conflict:** most pre-emergents (dithiopyr, pendimethalin,
  prodiamine) inhibit ALL seedling roots for 3-4 months. Rules:
  - Spring pre-emergent → seed in fall (cool-season), not spring
  - Must seed spring? Use siduron (Tupersan, the only seed-safe pre-emergent) or skip
    pre-emergent and use post-emergent quinclorac later.
- **Second pre-emergent round** (~8-10 weeks after first) extends the window; prodiamine
  65 WG at 0.37 lb/1000 ft² gives ~4 months at 0.65 ai/1000 — the script computes this
  from label rate tables.
- **Fertilizer burn conditions:** urea-containing products above 85°F on cool-season
  (fescue/blue/rye) turf; always water-in 0.25-0.5" unless the label says otherwise.
- **Cool-season grass (fescue/KBG/rye):** feed fall-heavy (Sep-Nov = 2/3 of annual N);
  spring N causes topgrowth at root expense + disease. **Warm-season (bermuda/zoya/
  st augustine/centipede):** feed summer-heavy, NOTHING until green-up (soil 65°F+).

## Fertilizer Math (bag guarantees)

```
N-P-K 20-0-8 means: 20% N, 0% P₂O₅, 8% K₂O by weight
A 50-lb bag of 20-0-8 = 10 lb N, 4 lb K₂O
1 lb N / 1000 ft²  →  50-lb bag covers 10,000 ft² at that rate
cost per lb N = bag price / lb N in bag   (the honest comparison between products)
```
Slow-release fraction matters: >30% coated/urea-form N allows higher single doses
(1.25-1.5 lb N/1000) without burn; all-soluble stays ≤1 lb/1000 per application.

## Numbered Workflow

1. Collect: grass type (cool/warm), location or 7-day mean air temp + today's date,
   lawn size (measure: length × width minus house/beds — or pacing), goals (crabgrass?
   seed? just green?), bag guarantee of products on hand.
2. `scripts/lawn_plan.py soil-temp --air-mean 52 --date 2026-04-10` → estimated soil
   temp + pre-emergent window verdict (GO / WATCH / TOO LATE — with post-emergent route).
3. `scripts/lawn_plan.py calendar --grass cool --region transition` → dated annual plan
   (pre-emergent windows, N rounds in lb N/1000, seeding windows, aeration).
4. `scripts/lawn_plan.py fert --npk 20-0-8 --bag-lbs 50 --price 32 --area 6000 --n-rate 1.0`
   → lb/bag needed, coverage, cost per lb N, burn-risk flag by date/temperature.
5. Check conflicts: script refuses calendar entries that pair seeding with non-siduron
   pre-emergent, or high-N summer applications on cool-season grass.

## Pitfalls

1. **Applying pre-emergent by calendar date.** A warm February triggers germination 3
   weeks "early"; a cold spring pushes it late. Soil temp is the gate.
2. **Pre-emergent then seeding 6 weeks later.** Root inhibition kills the seeding; the
   label says 3-4 months. Seed in fall or use siduron.
3. **More N = more green (until it isn't).** >1 lb N/1000 soluble in one pass burns;
   spring-heavy N on cool-season lawns invites brown patch and shallow roots.
4. **Ignoring the slow-release fraction.** Cheap all-soluble bags limit dose and frequency.
5. **Watering-in failure:** pre-emergent MUST be activated with 0.5" water/irrigation
   within days or it degrades on the surface; fertilizer sits on leaves → burn.
6. **Weed-and-feed timing mismatch:** granular herbicide needs the weed leaf wet
   (morning dew) AND the fertilizer schedule may not align with the germination window.
7. **Not calibrating the spreader** — label rates assume it; a mis-set spreader doubles
   or halves everything. Calibrate: weigh what falls in 100 ft².

## Example

```
$ python3 scripts/lawn_plan.py soil-temp --air-mean 54 --date 2026-04-10 --region transition
Estimated 2" soil temp: ~52°F (lag model; verify with $10 thermometer)
Crabgrass gate: germination starts at 55°F × 4 days
VERDICT: WATCH/APPLY — in the 50-55°F pre-window; apply NOW so the barrier activates first.
 Too late already (soil 70°F)? → switch to post-emergent: quinclorac on 1-3-leaf crabgrass.

$ python3 scripts/lawn_plan.py fert --npk 20-0-8 --bag-lbs 50 --price 32 --area 6000 --n-rate 0.75
Bag: 10.0 lb N | need 4.5 lb N for 6000 ft² @ 0.75 → 22.5 lb product (0.45 bag)
Cost: $3.20 per lb N ($14.40 this application). Coverage check: bag covers 13,333 ft².
DATE FLAG: if applying after mid-May on cool-season grass, use ≤0.5 lb N/1000 + water in.

$ python3 scripts/lawn_plan.py calendar --grass cool --region transition
... Sep 01  fall N 1.0 lb/1000 (feed-height of fall)
... Sep 15  AERATE + overseed KBG/fescue @ soil 60-75°F falling (NO pre-emergent since spring)
... Oct 15  fall N 1.0 → root season; Nov 15 final N 0.75 ("winterizer" while still green)
... Feb 20* soil 50-55°F rising: pre-emergent #1 (prodiamine 0.37-0.65 lb ai/1000)
... Apr 25* pre-emergent #2 (8-10 wk after #1)  *dates shift with soil temp — use the gate
```

## Verification Checklist

- [ ] Grass type confirmed (cool vs warm season drives everything)
- [ ] Lawn area measured honestly (pacing × 0.9 for house/beds)
- [ ] Soil temp from thermometer or the lag model + region
- [ ] Pre-emergent window GO/WATCH/TOO-LATE verdict with activation watering
- [ ] N rates per application ≤1 lb/1000 soluble (≤1.5 slow-release), annual total by grass
- [ ] Seeding vs pre-emergent conflict resolved (fall seed / siduron)
- [ ] Spreader calibrated (100-ft² catch test)
