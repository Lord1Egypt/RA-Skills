---
name: hand-me-down-flow
description: Use when passing children's clothes/toys/gear between siblings, cousins, or friend families — builds a hand-me-down chain registry with per-item condition grading, auto-matches inventory to each recipient kid's age window (sizes run 6-12 months ahead), prints transfer manifests and thank-you list, and flags the storage mistakes (attic heat, basement damp) that silently destroy stored boxes.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [family, kids, hand-me-downs, clothing-sizes, storage, organization, sustainability]
---

# Hand-Me-Down Flow

## Overview

Families with multiple kids (or a cousin/friend circuit) run a silent
logistics system: bins of outgrown clothes in the closet, a coat the
oldest wore two winters ago, someone's crib in a garage. It fails in
three predictable ways — nobody remembers **what's in the bins**, items
surface **after** the younger kid has outgrown them, and half the stored
stuff turns out ruined (attic heat delaminates, basements mildew, moth
larvae eat wool).

`scripts/handmedown.py` is that system: a registry of stored items with
size, season, condition grade, and location; each recipient kid with
birthday; per-kid **age-window matching** (child clothing sizes are
labeled ahead of actual age — a 2T label fits a median 18–24-month-old)
that tells you *now*: what to pull for this winter, what the middle kid
will inherit in spring, what to give away because the chain has no
future recipient. Plus the storage rules that keep the bin contents
alive, and the transfer manifest so the receiving parent knows what
they're getting.

## When to Use

- Rotating clothes/gear between your own kids ("what do we have for
  winter for the 3-year-old?").
- Passing items to cousins/friends and getting useful things back.
- Preparing a storage plan before the next baby.
- Deciding what to sell/donate vs store (chain has no future recipient).
- After receiving a batch from someone: grading and merging it.

**Don't use for:** estate/inheritance distribution (see heirloom
skills), adult clothing swaps, or selling (see marketplace pricing
skills) — this is the kids'-gear circulation lane.

## How It Works

1. **Registry.** JSON store (`--data path`, default `handmedown.json`
   next to the script): items with name, category, size label, season,
  condition grade (A new/tags, B gentle wear, C visible wear, D play
   clothes only), storage location, and notes.
2. **People.** Each kid: name + birthday. Age is computed live; the
   matcher converts item size labels to fit windows (median-age based,
   adjustable with `--fit-shift-months` for big/small kids).
3. **Match pass.** For every stored item and every kid: does this item
   fit this kid now, within ±1 season? Output per kid: PULL NOW list,
   IN 6 MONTHS list, and items whose window is closing (use it or move
   it along).
4. **Chain verdicts.** For each item: if no current or future kid in
   the registry will ever fit it (kid ages only go up), verdict
   PASS ALONG / DONATE — with the reason (window closed for everyone).
5. **Transfer manifest.** When you hand a batch to another family:
   itemized list with sizes and condition grades, so the receiver knows
   B from D and can re-return what they won't use.
6. **Storage rules.** Attic (summer heat delaminates and crumbles
   elastic/plastic), basement (damp → mildew), garage (temperature
   swings + pests): each location class carries a risk note the script
   prints; clean, dry, room-temp closet with sealed bins is the ideal.

## Using the Script

```bash
# add kids
python3 scripts/handmedown.py --data my.json add-kid --name Mia --birthday 2021-04-10
python3 scripts/handmedown.py --data my.json add-kid --name Leo --birthday 2023-09-02

# log stored items
python3 scripts/handmedown.py --data my.json add --name "winter coat" --category clothes \
  --size 4T --season winter --condition B --location "closet bin 2"

# who gets what, right now and next 6 months
python3 scripts/handmedown.py --data my.json match

# prepare a batch for the cousin family
python3 scripts/handmedown.py --data my.json manifest --to Emma

# what should leave the house entirely
python3 scripts/handmedown.py --data my.json match --chain-only
```

Outputs: per-kid PULL NOW / IN 6 MONTHS tables with per-item condition
and location, closing-window warnings, chain verdicts (DONATE with
reasons), transfer manifest, storage-risk notes for flagged locations.

## Common Pitfalls

1. **Storing by size label alone.** Labels run ahead of age (2T ≈
   median 18–24 mo). The matcher uses fit windows, not labels.
2. **Attic storage.** Summer attic temps 50–65 °C destroy elastic,
   laminate, and plastic within a couple of seasons. Stored "for the
   next kid" in an attic = composting money.
3. **No condition language between families.** "Here's a bag of
   clothes" with no grades means the good stuff gets treated like the
   stained stuff. Manifest with A–D grades fixes it.
4. **Waiting for perfect.** A B-grade winter coat stored until it fits
   someone is worth more used one season sooner; windows close faster
   than you think (one season ≈ 2 size steps for toddlers).
5. **Storing D-grade.** Play-clothes-only condition in storage is
   dead inventory — donate immediately, keep storage for A/B.
6. **Forgetting the size gap.** If the gap between kids is 4+ years,
   most clothes won't survive storage that long (style, rubber rot,
   moths); the chain verdict should factor gap length per item.

## Verification Checklist

- [ ] Every kid's birthday in the registry (ages drive everything).
- [ ] Items logged at intake (the day the box is packed), not months later.
- [ ] Condition graded at intake with the A–D scale, not from memory.
- [ ] Match pass run at each season change (2×/year minimum).
- [ ] Closing-window items either used this season or passed along now.
- [ ] Storage location risk flags read; nothing A/B grade in
      attic/garage/basement unprotected.
- [ ] Transfer manifests given (not just bags) so grades travel with items.
