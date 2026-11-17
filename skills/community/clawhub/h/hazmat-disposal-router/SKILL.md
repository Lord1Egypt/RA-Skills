---
name: hazmat-disposal-router
description: "Use when you have household items you can't just trash (old paint, car batteries, lithium cells, motor oil, pesticides, needles, propane tanks, CFL/LED bulbs, electronics, expired meds) — item-by-item verdicts (trash / HHW facility / take-back / retailer drop-off / never-drain warnings) with WHY in one line, the never-do list (paint thinner down the drain, lithium in trash, needles in plastic bottles), multi-item garage-cleanout audit mode that groups everything into one facility trip, storage rules until drop-off (lithium terminals, oil containers, original labels), and US/EU/UK take-back channel finders."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [hazmat, disposal, recycling, home, safety, environment]
---

# Hazmat Disposal Router

**Don't guess. Don't drain. Route it.** Every garage and under-sink
cabinet holds 5-15 items that are illegal or dangerous to trash —
and most people guess. Wrong guesses start garbage trucks fires
(lithium), poison waterways (oil, paint), or endanger workers
(needles in plastic bottles).

## Overview
1. **dispose** — item → verdict: where it goes, WHY (one line),
   warnings. Covers 20+ item families: paints, solvents, batteries
   (lead-acid / lithium / alkaline), motor oil, coolant, pesticides,
   pool chems, propane, CFL/LED, e-waste, meds, needles, thermometers,
   smoke alarms, fire extinguishers, asbestos-suspect, gasoline.
2. **audit** — garage/basement cleanout: list everything, get one
   grouped manifest (which items to which channel) for a single trip.
3. **storage** — safe interim storage rules until drop-off day
   (lithium bagging, oil containers, no-mixing, original labels).
4. **channels** — where to take things: US (Earth911-style search
   terms + retailer take-back), EU (WEEE/municipal recycling yards),
   UK (council HWRC), plus meds take-back everywhere.
5. **never** — the never-do list, printed with reasons.

Pure stdlib, offline. Regulations vary by locality — verdicts are the
consensus safe default; verify local rules for your address.

## When to Use
- Cleaning out garage / basement / dead relative's house
- After a paint project, oil change, or battery swap
- "Can I throw this in the bin?" — any item you suspect
- Renovation debris with old chemicals/tubes
- Setting up a household's permanent disposal map

**Don't use for:** active spills, unknown mixed chemicals reacting,
asbestos already crumbling (airborne = professional abatement), or
commercial quantities (different law).

## How It Works — Numbered Steps
1. Check single items as they surface:
   ```
   python3 scripts/hazmat_router.py dispose --item "latex paint"
   python3 scripts/hazmat_router.py dispose --item "li-ion battery"
   python3 scripts/hazmat_router.py dispose --item "motor oil"
   ```
2. For a cleanout, audit everything at once:
   ```
   python3 scripts/hazmat_router.py audit --items "latex paint,oil paint,car battery,li-ion packs,CFL bulbs,old gasoline,weed killer"
   ```
   → grouped manifest: HHW-facility pile vs retailer drop-offs vs
   trash-safe pile + trip plan.
3. Store safely until the run:
   ```
   python3 scripts/hazmat_router.py storage
   ```
4. Find your local channels:
   ```
   python3 scripts/hazmat_router.py channels --region US
   python3 scripts/hazmat_router.py channels --region EU
   ```
5. Memorize one thing — the never list:
   ```
   python3 scripts/hazmat_router.py never
   ```

## The Verdict Table (excerpts)
| Item | Verdict | Why |
|---|---|---|
| Latex paint (dried solid) | trash | Inert once fully dry — air-dry or mix with cat litter |
| Oil paint / solvents | HHW facility | VOC + heavy metals; never drain/trash liquid |
| Car battery (lead-acid) | Retailer drop-off | Retailers must take core; ~$10 core credit |
| Li-ion packs / power tool / e-bike | HHW / battery bin | #1 cause of garbage truck fires; tape terminals |
| Alkaline (modern, US) | trash (or recycle) | No mercury since ~1996; EU: battery bin |
| Motor oil | Any auto parts store | 1 L oil contaminates ~1M L water; stores resell it |
| Gasoline (old) | HHW facility | Never pour in grass/drains; degrades but ignitable |
| Propane tank (BBQ) | Retailer exchange / HHW | Pressurized + explosive in compactors |
| CFL bulbs | HHW / retail bin | Mercury vapor — never break in trash |
| LED / incandescent | trash | No mercury; no special handling |
| Meds (expired) | Pharmacy take-back | Never flush (water supply); DEA take-back days US |
| Needles / lancets | Sharps program | Never loose or in plastic bottles (workers) |
| Smoke alarm (ionization) | Mail-back mfr program | Americium-241 — tiny but regulated |
| Fire extinguisher | HHW / fire dept | Pressurized; discharge completely first if allowed |
| Weed killer / pesticides | HHW facility | Herbicides persist; never dilute-down-drain |

## Common Pitfalls
1. **"Thinners and paints down the drain."** Drains lead somewhere:
   septic fields die, municipal plants can't strip solvents, and it's
   illegal nearly everywhere. Liquid solvent = HHW, always.
2. **Li-ion in the bin.** Damaged cells short in the compactor —
   garbage truck fires have doubled in many cities from batteries
   alone. Tape terminals, bag separately, battery channel.
3. **Mixing leftovers "to save space."** Pool chlorine + acids,
   ammonia + bleach, oxidizers + organics: mixing containers can
   react in transport/storage. Original containers, never combined.
4. **Needles in soda bottles.** Sanitation worker injuries; the
   program exists specifically because this fails. Sharps container
   or a labeled rigid container per local program.
5. **Wet latex paint in the trash.** Liquid paint leaks through
   trucks, paints streets. DRY it first (cat litter / paint hardener
   / air) — then it's trash.
6. **Breaking CFLs to "fit the bin."** Mercury vapor exposure to you;
   sealed plastic bag if broken, HHW if intact.
7. **Full propane tanks to trash/compactor.** Explosive in compactors.
   Exchange programs take old tanks; HHW takes odd sizes.
8. **Hoarding HHW "for later."** Containers corrode (old gas cans,
   acid bottles), fumes accumulate; plan a drop-off run within a
   month of cleanout.

## Example
```
$ hazmat_router.py dispose --item "car battery"
CAR BATTERY (lead-acid):
  VERDICT: retailer drop-off — any auto parts store; core credit
  (~$10 on new battery). Scrap yards pay by weight.
  WHY: 8+ kg lead + sulfuric acid; landfill = groundwater.
  WARN: keep upright, terminals not shorting (no tools across posts).

$ hazmat_router.py audit --items "latex paint,oil paint,car battery,li-ion packs,CFL bulbs,old gasoline"
CLEANOUT MANIFEST — 6 items, 2 channels:
  HHW FACILITY RUN: oil paint, CFL bulbs, old gasoline, li-ion packs*
  RETAILER DROP-OFF: car battery (auto parts store, ~$10 credit)
  TRASH (prepared): latex paint — dry with cat litter first
  *tape/bag lithium terminals before transport
  TRIP PLAN: battery to parts store today (credit), rest to HHW
  Saturday. Check facility hours — many are weekly-only.
```

## Verification Checklist
- [ ] Every questionable item checked against the verdict table
- [ ] Audit manifest built; channels grouped for minimum trips
- [ ] Interim storage rules applied (original labels, no mixing,
      lithium terminals taped, upright, ventilated area)
- [ ] Local facility located + hours confirmed before loading
- [ ] Never-list items verified absent from your trash bins
