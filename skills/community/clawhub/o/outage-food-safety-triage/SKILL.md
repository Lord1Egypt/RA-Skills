---
name: outage-food-safety-triage
description: Use when the power went out and you need to know what's still safe to eat — FDA/USDA-grounded triage of fridge/freezer contents after an outage. 4-hour fridge / 24-48h freezer rules, the 40°F danger-zone math, item-by-item keep-vs-toss engine (the non-obvious calls: condiments vs leftovers vs deli meat), refreezing rules, and a printable door-sign checklist for next time.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [food-safety, power-outage, fridge, freezer, refrigerator, emergency-prep, food-waste]
---

# Outage Food Safety Triage

## Overview

Power just came back. The fridge has been dark for 9 hours, the freezer
for 9 hours too. Standing in front of it, everyone faces the same costly
dilemma: toss everything (~$300 of food) or gamble (and risk the
food-poisoning cluster that ERs see after every hurricane). The official
rules are simple but almost nobody knows their specifics — and the
*category-level* calls are where the money and the safety live.

This skill is a triage instrument built on FDA/USDA guidance:

1. **Duration verdicts** — fridge held ≤4 h at ≤40°F (fine), 4–8 h in the
   danger zone (partial cull), freezer: 24 h half-full / 48 h full (still
   safe if intact crystals).
2. **Item-by-item disposition** — the keep/toss table people guess wrong:
   open mayonnaise survives, deli meat and leftovers do not; hard cheese
   survives, shredded does not; butter yes, soft cheese no.
3. **The 40°F / 4°C danger-zone math** — why "but it still felt cold" is
   not evidence, and what a thermometer check actually validates.
4. **Refreezing rules** — when thawed-then-refrozen is safe and when it's
   a silent hazard.
5. **Door-sign protocol** — the prepared-household trick that makes the
   next outage a 2-minute decision.

## When to Use

- Power outage just ended (or ongoing) and food sat in a closed fridge/
  freezer without power
- Fridge accidentally unplugged / door left open overnight / thermostat
  failure discovered late
- After a storm, rolling blackout, or freezer failure discovered on
  return from vacation
- Planning: printing the door sign + thermometer placement before storm
  season

**Don't use for:** flood-contaminated food (different protocol — assume
total loss of contact-flooded items), long multi-week outages with generator
fuel questions, or commercial food service (health-code rules apply).

## Quick Start

```bash
python3 scripts/triage.py verdict --hours 9 --fridge-temp unknown
python3 scripts/triage.py verdict --hours 5 --fridge-temp 41
python3 scripts/triage.py item --name "deli turkey, opened"
python3 scripts/triage.py item --name "open mayonnaise"
python3 scripts/triage.py refreeze --state "thawed, still cold, crystals"
python3 scripts/triage.py doorsign --out door-sign.md
```

Stdlib-only, no network.

## The Rules Being Applied

| Fact | Number | Consequence |
|---|---|---|
| Fridge safe window (closed, unpowered) | **4 hours** at ≤40°F/4°C | After that, perishables enter the danger zone |
| Danger zone | 40–140°F (4–60°C) | Bacteria double every 20 min in this band |
| Freezer, half full, closed | **24 hours** | Food safe if still ≤40°F / has ice crystals |
| Freezer, full, closed | **48 hours** | Full freezers hold mass-cold far longer |
| Never taste-test | — | Appearance and smell detect NOTHING about toxin presence |
| Refreeze rule | thawed but ≤40°F and crystals intact | Safe; quality drops, safety holds |
| Frozen-thawed-frozen fish/meat >40°F | toss | Toxins survive re-freezing; cold doesn't undo them |

**Why "felt cold" is not evidence:** fridge interiors stratify — the door
shelves hit 50°F in 2 hours while the back-bottom stays cold for 6. Only a
thermometer reading (appliance thermometer kept IN the fridge) counts as
data; everything else is inference from duration.

## Workflow

1. **Establish duration**: hours without power (or hours fridge discovered
   warm). If unsure, use the longest plausible estimate — never the
   shortest.
2. `verdict --hours H --fridge-temp T` → zone verdict for fridge and
   freezer sections (fridge-temp can be a number in °F or `unknown`).
3. **Walk the fridge with the item engine**: `item --name "..."` for each
   borderline thing. The output cites the category rule, not vibes.
4. **Freezer check**: still-frozen hard? ice crystals present? → refreeze
   path via `refreeze --state`. Thawed and >40°F → the toss list.
5. **Bag culled items immediately** — out of the house, not "later", so
   nobody salvages from the bin.
6. **Print the door sign** (`doorsign`) — thermometer placement + the
   4h/24h/48h numbers + the top-10 toss-first items. Tape it inside the
   door; the next outage becomes a 2-minute call.

## Common Pitfalls

1. **Tasting or smelling to check.** Listeria, Staph aureus and B. cereus
   toxins are invisible and odorless at dangerous doses. Tasting is the
   #1 outage food-poisoning mechanism.
2. **Averaging the duration.** "Power was out maybe 5, maybe 10 hours" →
   use 10. The math must be worst-case, not hopeful.
3. **Trusting door-shelf items.** Door shelves are the warmest zone;
  condiments survive there, milk does not — even within a "passing" 4-hour
   verdict, treat door-zone perishables as 1 hour worse.
4. **Refreezing fully thawed meat "because it's still cold."** Cold is
   necessary, not sufficient: if it spent >2h above 40°F, toxins may
   already be present and survive the refreeze.
5. **Forgetting the freezer's borrowed cold.** A full freezer is a cold
   battery. Half-empty freezers lose 24h of runway — which is why the
   doorsign says to keep jugs of water frozen in the gaps.
6. **Cooking as rescue.** Cooking kills bacteria; it does NOT destroy
   preformed toxins (Staph, B. cereus). Cook-to-save only applies to
   items already on the safe side of the line.
7. **Re-powering and "watching" the fridge.** After triage, discard first,
   sanitize spills, then restock — a leaky thawed-chicken package
   contaminates the survivors.

## Verification Checklist

- [ ] Duration estimated worst-case (longest plausible hours)
- [ ] Fridge verdict computed with thermometer reading if available
- [ ] Every borderline item run through the item engine, not eyeballed
- [ ] Freezer decided by ice-crystal state + temp, not by "mostly frozen"
- [ ] Refreeze decisions follow the 40°F+crystals rule
- [ ] Culls bagged and out of the house; spills sanitized before restock
- [ ] Door sign printed and taped inside the fridge for next time

## Safety Disclaimer

When in doubt, throw it out — food poisoning costs more than groceries.
This skill encodes FDA/USDA consumer guidance for planning; it cannot see
your actual food. High-risk households (pregnant, elderly, immunocompromised,
infants) should apply stricter cutoffs: any perishable with ≥2h of
uncertainty goes.
