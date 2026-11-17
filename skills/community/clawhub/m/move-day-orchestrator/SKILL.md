---
name: move-day-orchestrator
description: "Use when someone is planning or executing a move (apartment/house change) and needs a structured timeline, packing plan, box labeling system, truck or van sizing, moving-day run-of-show, or the first-night survival box. Generates a phased countdown plan from moving date, room-by-room packing waves, box inventory with QR-free numeric labels, truck volume estimation, and a day-of command sheet — the difference between a managed move and a chaotic one."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [moving, relocation, moving-day, packing, boxes, truck, household-move, logistics]
---

# Move Day Orchestrator

## Overview

Moving is one of the most stressful life events people routinely undergo — up there with divorce and job loss in surveys — and almost none of the stress is inherent: it's coordination failure. Things get packed that are needed immediately; the truck is too small; the disassembled bed's bolts vanish; nobody booked the elevator; the mattress won't make the corner; the utilities overlap wrong; and the "where is the kettle" search consumes the first week.

This skill converts a move into a project with a critical path:

1. **Countdown timeline** — phased plan keyed to your actual moving date: what must be done at T−8 weeks, T−4, T−1 week, the day before, the day, and the first week after. Declutter before packing (moving is a paid-by-the-kilo inventory audit), bookings with lead times (movers, elevator reservation, parking permit), address-change chains, utilities overlap strategy.
2. **Packing waves** — rooms ranked by "days-until-needed": storage/guest room first, kitchen-daily and bedroom last. Never pack the First-Night Box by accident.
3. **Box inventory** — numeric labeling (ROOM-SEQ: KIT-01…KIT-12) with contents log per box; priority flags (open-first); the inventory is what makes insurance claims and "where's the X" searches trivial.
4. **Truck & crew sizing** — volume estimate from home size + household density signals, with the 10–15% packing-inefficiency factor; van vs. box truck vs. pro-movers decision matrix; ramp/liftgate needs; stairs vs. elevator time multipliers for the crew plan.
5. **Day-of run-of-show** — an hour-blocked command sheet: loader sequence (heavy furniture first, boxes stacked wall-to-wall), the protection sequence (floors, doorframes, mattress covers), the person responsible for keys/wallet/charger (never in a box), the final sweep checklist per room, and the handoff/meter-reading protocol.
6. **First-night survival** — the box that moves in the car, not the truck: kettle/charger/meds/toilet paper/screwdriver/bedding/change of clothes/shower stuff; plus the day-after priority list (beds first, then kitchen, then bathroom — everything else can wait a week).

## When to Use

- Planning a move: "we're moving on <date>, where do we start?"
- "How big a truck / how many movers do I need for a 2-bed apartment?"
- Building the packing order and box system for a DIY move
- Moving-day schedule / who-does-what run sheet
- First-night and first-week setup priorities
- Long-distance moves: the drive plan, the overnight-stop box, arrival-day triage
- Office/small-business moves use the same skeleton (inventory, waves, run-of-show)

**Don't use for:** international container moves with customs (add a customs broker; the packing waves still apply), commercial/industrial relocation with machinery rigging, or storage-unit-only logistics (no home change).

## How It Works — Numbered Workflow

1. **Register the move**: `move set --date 2026-11-14 --from "2-bed apt, 3rd floor, elevator" --to "house, ground"` — the script computes the phase you're in and the days remaining.
2. **Build the inventory estimate**: `estimate` — either from home-size presets (studio/1/2/3/4-bed with density normal/heavy) or itemized big items (`add-sofa`, `add-bed`…) for a bottom-up volume; outputs truck class (van/10'/15'/20'/26' / multi-trip), estimated boxes by size, blankets/wraps count, and crew-hours with stairs/elevator multipliers.
3. **Generate the timeline**: `plan` — the phased checklist with dates computed back from moving day, lead-time warnings (book movers 4–6 weeks out in season; elevator reservation; parking permit for the truck), and the utilities overlap (keep old internet alive through moving day; new one installed day after arrival — or the overlap gamble explained).
4. **Run the packing waves**: `waves` — rooms ordered by days-until-needed with per-room notes (what makes it into the first-night box from each room); `box` command logs each packed box: label, room, priority, contents keywords — the searchable inventory.
5. **Moving day**: `runshow` — the hour-blocked run-of-show from protect-the-floors to final sweep, with the never-in-the-truck list, loader sequence, meter photos, and key handoff.
6. **Arrival**: `arrival` — first-night box manifest, first-24h priority order (beds → essentials bathroom → kitchen basics → internet installer meet), and the first-week plan (box-priority queue using the inventory's open-first flags).
7. **Claims and closeout**: boxes damaged? The inventory log (contents + condition notes at pack time) is the evidence for mover-liability or insurance claims.

## Quick Start

```bash
python3 scripts/move_orchestrator.py set --date 2026-11-14 --from "2-bed apt 65m2, 3rd fl, elevator" --to "house ground fl"
python3 scripts/move_orchestrator.py estimate --home 2bed --density normal
#   or bottom-up:  add sofa 3seat, fridge, washer, bed 160, desk, 40 boxes...
python3 scripts/move_orchestrator.py plan
python3 scripts/move_orchestrator.py waves
python3 scripts/move_orchestrator.py box KIT-01 kitchen --priority open-first --contents "kettle, mugs, coffee, filters"
python3 scripts/move_orchestrator.py find kettle        # -> KIT-01 (car, not truck)
python3 scripts/move_orchestrator.py runshow --start 08:30 --crew 3
python3 scripts/move_orchestrator.py arrival
```

State: `move_state.json` beside the script. Pure stdlib; print outputs; nothing leaves the machine.

## Output Examples

**`estimate` (excerpt):**
```
ESTIMATE: 2-bed, normal density  ->  ~18 m3 loaded volume
  truck: 15' box truck (max ~20 m3; 10% headroom) or 2x van trips
  boxes: ~8 XL, ~25 L, ~20 M, ~15 S  +  8 quilted blankets, 1 sofa cover
  crew: 2 pros x 5h (elevator both ends) or 3 friends x 7h (stairs at destination)
  weight note: piano/ready-to-assemble furniture changes everything — itemize them
```

**`runshow` (excerpt, 08:30 start, crew of 3):**
```
08:30  PROTECT: floors+doorframes both ends, mattress covers on
08:45  LOAD (heaviest first): washer, fridge (defrosted Fri, towels in base), sofa DISASSEMBLED legs off
       boxes: heavy-small low+forward, light-large high+rear, wall-of-boxes strap rails
10:30  FRAGILE/VALUABLES in CAR not truck: docs, jewelry, electronics, plants, first-night box
...
17:00  FINAL SWEEP every room + attic/balcony/water meter/photos -> keys to landlord
```

## Common Pitfalls

1. **Packing by room instead of by need-date.** Everything in "storage/guest room" can be boxed at T−3 weeks; the kettle and the coffee cannot. Packing waves rank rooms by days-until-needed, not by convenience.
2. **No first-night box (or it's in the truck).** The 22:00 arrival with no bedding, toilet paper, charger, or kettle is the single most common moving-day failure. The box travels in the car; the runshow has a hard checkpoint for it.
3. **Wrong truck size.** Too small = a second trip through traffic at double time-cost; too large = cost + difficulty parking. Estimate bottom-up for big items, add 10–15% for packing air. The estimate command shows both m³ and truck-class options.
4. **Bolts and remotes in "a safe place".** Disassembly hardware goes in a zip bag TAPED to the item it belongs to (or one labeled hardware box that rides in the car). The single most-lost moving item category is fasteners.
5. **Ignoring building logistics.** Elevator reservation (both buildings), parking spot for the truck (permit/tow risk), certificate-of-insurance for some buildings, narrow-stair furniture physics (measure diagonal + worst corner; the reference has the math).
6. **Utilities overlap done wrong.** Old internet/electric off the day you move = packing in the dark and no phone hotspot for the crew coordination; new internet installed the day you arrive = waiting days for a slot. Overlap old through moving day; book new for day-after-arrival.
7. **Moving clutter you were going to discard anyway.** Every kilo costs money and every box costs time. Declutter/sell/donate BEFORE packing (the timeline's T−8…T−4 phase exists for this); moving boxes you'll unpack straight into a donation bag is paying to keep trash.
8. **No inventory = no claim.** Mover-liability is per-kg (released-value ~$0.60/kg) unless declared; without a contents log per box you can't prove what was in the crushed one. The `box` command's contents keywords + priority flags are your claim evidence.
9. **Labeling boxes by room only.** "Kitchen" × 12 boxes means opening all twelve to find the kettle. ROOM-SEQ labels + contents keywords + open-first flags make the first week searchable instead of archaeological.

## Verification Checklist

- [ ] `set --date` computes correct days-remaining and current phase
- [ ] `estimate --home 2bed` prints m³, truck class, box counts, crew-hours (sanity: studio ~8-10 m³, 4-bed ~35-45 m³)
- [ ] `plan` shows phases with computed dates and lead-time warnings
- [ ] `waves` orders rooms by need-date and includes first-night-box pulls per room
- [ ] `box` log + `find <item>` returns the right box
- [ ] `runshow --start --crew` prints hour blocks incl. car-not-truck checkpoint and final sweep
- [ ] `arrival` prints first-night manifest + first-24h priorities
- [ ] No network imports (grep requests/urllib/socket — empty)

## One-Shot Recipes

**"We got the keys, we move Nov 14" (T−6 weeks):**
```bash
python3 scripts/move_orchestrator.py set --date 2026-11-14 --from "2-bed apt" --to "house"
python3 scripts/move_orchestrator.py plan        # this week: book movers, declutter wave 1
python3 scripts/move_orchestrator.py estimate --home 2bed --density normal
```

**Packing Saturday (T−2 weeks):**
```bash
python3 scripts/move_orchestrator.py waves       # storage/guest/books today; kitchen-daily stays
python3 scripts/move_orchestrator.py box STO-01 storage --contents "camping gear, suitcases"
```

**Morning of the move:**
```bash
python3 scripts/move_orchestrator.py runshow --start 08:30 --crew 3 | lp   # tape to the door
```

**Arrival evening:**
```bash
python3 scripts/move_orchestrator.py find kettle        # KIT-01 -> open first
python3 scripts/move_orchestrator.py arrival
```

## License & Disclaimer

MIT © Denis Voronin. Estimates are planning heuristics from standard household-volume tables; actual mover quotes override. Heavy/rigging items (pianos, safes, marble) need professionals regardless of what the estimate says.
