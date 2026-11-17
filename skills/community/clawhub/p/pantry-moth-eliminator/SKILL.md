---
name: pantry-moth-eliminator
description: Use when you see small moths in the kitchen, webbing in flour or rice, or larvae climbing walls/ceiling — Indian meal moth infestation. Generates a staged elimination protocol (find-pull-freeze-clean-trap) with exact timelines, an item-by-item disposition engine (freeze/toss/heat), pheromone-trap placement math, cabinet crack-cleaning procedure, and a re-infestation watch with expected moth-free dates.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [pantry-moths, indian-meal-moth, kitchen-pests, food-storage, pest-control, home-care]
---

# Pantry Moth Eliminator

## Overview

The Indian meal moth (*Plodia interpunctella*) is the moth most kitchens
eventually meet: it hitches in via birdseed, bulk grains, dried fruit, pet
food, or grocery packaging gaps. One fertilized female lays ~400 eggs; in a
warm kitchen the cycle (egg→larva→pupate→adult) runs **4–8 weeks**, so
"just throwing out the flour" fails — larvae are already pupating in the
ceiling corner, under shelf liners, and inside the seams of sealed-looking
boxes.

This skill generates a **staged protocol** calibrated to infestation level:

1. **Level triage** — mild (moths seen, no webbing) / moderate (webbing,
   larvae on walls) / severe (recurring catch, multiple cabinets).
2. **Disposition engine** — for every category of dry food: freeze-kill
   (−18°C/0°F for ≥4 days), heat-kill (140°F/60°C for 30 min oven), or
   toss — including the non-obvious calls (spices, tea, chocolate, pet
   food, unopened boxes with larvae-sized gaps).
3. **Timeline** — day 0 pull, freeze windows, deep-clean cracks (where
   pupae hide), day 7/14/30 trap checks with pass/fail thresholds.
4. **Trap math** — where pheromone traps go, how many, and how to read
   them (traps are monitors, not control).
5. **Re-infestation defense** — incoming-goods quarantine, storage
   hardening, and expected moth-free date math from biology.

## When to Use

- Moths fluttering in the kitchen or near dry goods
- Webbing / clumping / larvae in flour, rice, oats, nuts, cereal, pet food
- Larvae climbing walls or ceiling corners (they seek dark pupation cracks)
- After bringing in bulk grains, birdseed, or dried fruit and wanting to
  prevent an infestation

**Don't use for:** clothes moths (different species, different protocol —
look for holes in wool, cases not webbing), weevils in pasta (disposition
similar but no trapping), or commercial kitchens (call a licensed pest
operator).

## Quick Start

```bash
python3 scripts/moths.py protocol --level moderate
python3 scripts/moths.py disposition --item "brown rice, opened"
python3 scripts/moths.py disposition --item "spices"
python3 scripts/moths.py traps --cabinets 4
python3 scripts/moths.py timeline --start 2026-10-04 --level moderate
python3 scripts/moths.py watch --start 2026-10-04 --catch-day7 3 --catch-day14 0
```

Stdlib-only, no network.

## The Biology You're Fighting (why partial attempts fail)

| Stage | Duration (warm kitchen) | Where | Killable by |
|---|---|---|---|
| Egg | 2–14 days | on/near food surface | toss/freezing |
| Larva | 2–6 weeks (the webbing stage) | INSIDE food, then wandering | freeze/heat/toss |
| Pupa | 1–2 weeks | **cracks, seams, ceiling corners** — away from food | vacuum + wipe only |
| Adult | 1–2 weeks | flying; ♂ follows pheromone | traps MONITOR only |

Key facts the protocol encodes:
- **Larvae chew into packaging** that looks sealed: folded carton seams,
  plastic bags. Cardboard is not a barrier.
- **Pupae hide away from food** — cleaning only the pantry shelves misses
  the ceiling corner, under-cabinet lip, and shelf-support holes. This is
  the #1 reason infestations "come back" (they never left).
- **Freeze at −18°C/0°F for 4+ days** kills all stages (standard food-
  industry disinfestation). Home freezers vary — give it a week for
  thick bags.
- **Pheromone traps catch males only** — they confirm and date-stamp the
  infestation but will never eliminate it. Zero catch for 3 consecutive
  weeks = clean.
- Adults live ~2 weeks without mating success once traps + food removal
  collapse the population — the visible-moth tail after a proper day-0
  is normal, not failure.

## Workflow

1. **Triage**: `protocol --level mild|moderate|severe` prints the full
   staged plan (find → pull → freeze → clean → trap → watch).
2. **Pull everything dry** from the infested zone — including unopened
   boxes (larvae enter through seams). Run each through
   `disposition --item "..."` for freeze/toss/heat calls.
3. **Freeze-kill keepers** (−18°C, ≥4 days; a week for thick packages),
   then transfer to glass/metal with gasket lids. Moths cannot chew glass.
4. **Deep clean on the same day** — vacuum every crack, seam, and corner
   in and around the cabinets (include under-shelf lips, shelf pins,
   ceiling corners within ~1 m, and the cabinet top gap). Wipe with
   vinegar/dish soap; let dry. Empty the vacuum OUTSIDE.
5. **Traps**: `traps --cabinets N` — placement plan (one per cabinet zone,
   at eye level, away from windows/drafts, never stacked near each other).
6. **Watch**: `watch --start DATE --catch-day7 N --catch-day14 N` →
   verdict against thresholds (day7 >5 = protocol gap, day14 >1 = missed
   source, day14 =0 = on track, day30+ 3-weeks-zero = declared clean).
7. **Quarantine everything new**: freeze bulk goods for 4 days before
   shelving; inspect birdseed/pet food on arrival (top sources).

## Common Pitfalls

1. **Throwing out only the visibly infested bag.** Larvae have already
   migrated — pull the ENTIRE dry-goods zone, not the casualties.
2. **Trusting "sealed" boxes.** Cardboard seams and folded flaps are
   larva-doors. Unopened ≠ safe.
3. **Skipping the crack-cleaning.** Pupae sit in seams away from food;
   this is the actual comeback mechanism.
4. **Treating pheromone traps as the weapon.** They catch ~males only and
   saturate; they date-stamp progress, they don't collapse populations —
   food removal does.
5. **Cleaning before pulling.** Adults re-oviposit on the next night's
   goods. Pull → freeze/toss → clean, in that order, same day.
6. **Forgetting pet food and birdseed** — the two most common import
   vectors. Dry pet food must go through the same protocol.
7. **Sprays/aerosols in food cabinets** — unnecessary and contaminates
   food-contact surfaces; vacuum + soap is the whole job.
8. **Declaring victory at day 10.** The cycle is 4–8 weeks; only 3
   consecutive zero-catch weeks (day ~30–45) is a clean verdict.

## Verification Checklist

- [ ] Level triaged and full protocol printed before touching anything
- [ ] ALL dry goods pulled (incl. unopened, spices, tea, chocolate, pet food)
- [ ] Every keeper frozen −18°C ≥4 days (or heat-treated) before re-storage
- [ ] Keepers re-stored in glass/metal gasket containers
- [ ] Cracks/seams/corners vacuumed then wiped; vacuum emptied outside
- [ ] Traps placed per plan (count + eye level + spacing)
- [ ] Day 7 / 14 / 30 trap checks logged; verdict from thresholds
- [ ] New bulk goods quarantine habit installed (freeze-on-arrival)

## Safety Notes

- Freeze-treat, never microwave sealed bags; heat-treat only true oven-
  safe containers at 60°C/140°F for 30 min.
- Pheromone traps are non-toxic; keep out of reach of pets that might eat
  the sticky insert.
- If larvae appear in bedroom closets or wool items — that's clothes
  moths, a different protocol (see When NOT to use).
