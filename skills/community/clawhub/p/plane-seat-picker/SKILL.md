---
name: plane-seat-picker
description: "Use when booking a flight and staring at a seat map (is 37F good? what about exit row 21? we're a family of 4 with a toddler) — decodes seat numbers to position (window/middle/aisle, left/right) per aircraft family, flags the trap rows (non-reclining last rows, seats ahead of exits, lav/galley proximity, bulkhead trade-offs), matches strategy to flight type (red-eye window vs day-flight family split, couples window+aisle gambit), covers bassinet/bulkhead for infants and under-2 lap rules, and rates any seat across legroom/recline/quiet/storage dimensions."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [travel, flying, seats, airlines, aircraft, families, booking]
---

# Plane Seat Picker

**The seat map is a puzzle and the airline's legend won't tell you
that 24A doesn't recline.** This tool decodes seats to actual
position per aircraft family, flags the structural traps (rows
ahead of exits, last-row recline, lavatory bounce), and picks
strategy by flight type — because the right seat on a red-eye is
the wrong seat on a daytime flight with kids.

## Overview

1. **decode** — seat number + aircraft family → window/middle/
   aisle, side of plane, and known traps for that zone.
2. **aircraft** — family quick facts: typical pitch/width, cabin
   layout codes (3-3, 3-3-3), what changes comfort.
3. **choose** — flight type (red-eye/day/short-hop) + party size +
   preferences → ranked strategy with concrete seat patterns.
4. **families** — infant (bassinet/bulkhead, lap-child rules) vs
   toddler (split across aisle) vs older kids (any window);
   car-seat onboard rules of thumb.
5. **traps** — the master trap list with WHY for each.

Stdlib Python, offline. Aircraft data is by FAMILY (A320ceo/neo,
737-800/MAX8, A321neo, 737-900, A220, E195, 787, A350, 777, A380)
— airlines configure individually, so verdicts are zone-logic that
holds across configurations.

## When to Use

- Any seat selection at booking or check-in
- "Is exit row worth the $45?" — the trade-offs, honestly
- Flying with an infant/toddler and need bassinet math
- Couples/groups on a 3-3 or 3-3-3: which pairs maximize odds of an
  empty middle
- Red-eye strategy: sleep vs aisle access

**Don't use for:** specific airline subfleet seat maps (airline
config varies; use this for the logic + zone traps, the airline's
map for exact rows), premium cabin selection (different game).

## How It Works — Numbered Steps

1. Decode a specific seat:
   ```
   python3 scripts/seat_picker.py decode --seat 32F --aircraft a320
   python3 scripts/seat_picker.py decode --seat 21A --aircraft 737-800
   ```
2. Aircraft family facts:
   ```
   python3 scripts/seat_picker.py aircraft --type 787
   ```
3. Strategy for your flight:
   ```
   python3 scripts/seat_picker.py choose --flight red-eye --party 1 --pref window
   python3 scripts/seat_picker.py choose --flight day --party 2 --pref quiet
   ```
4. Flying with kids:
   ```
   python3 scripts/seat_picker.py families --kids toddler --adults 2
   python3 scripts/seat_picker.py families --kids infant --adults 2
   ```
5. The trap list (why that cheap seat is cheap):
   ```
   python3 scripts/seat_picker.py traps
   ```

## Aircraft Family Table (excerpt)

| Family | Econ layout | Pitch | Notes |
|---|---|---|---|
| A320/321 (ceo) | 3-3 | 29-31" | F=C window right; C/D aisle. Loud over-wing rows ~10-16 |
| A320neo/A321neo | 3-3 | 29-31" | Much quieter than ceo; A321neo LR long-haul: pick forward |
| 737-800 / MAX8 | 3-3 | 29-31" | A=F windows; over-wing escape limits recline ahead of exits |
| A220 (-100/-300) | 2-3 | 30-32" | 2-3 means EVERY seat is window-or-aisle; A-side pairs for couples |
| E195 / E175 | 2-2 | 29-31" | No middle seat at all; A=C windows |
| 787-8/9 | 3-3-3 | 30-32" | 17.2-17.5" width is tight; windows dim electronically (no shade) |
| A350 | 3-3-3 | 31-32" | 18" width, quieter; A/K windows, D/E/F/G middle block |
| 777-300ER | 3-4-3 many airlines | 31-32" | The D-G middle-of-middle is the worst economy seat flying; prefer 2-4-2 configs |
| A380 main deck | 3-4-3 | 31-32" | Upper deck quieter; main deck boarding wave hits first |

## The Trap List

1. **Row ahead of an exit row** — seats don't recline (must keep
   exit clear). Common on 737/A320 at over-wing exits.
2. **Last 2 rows** — limited/no recline, near lavs (door slam,
   queue hover, smell), galley light, meal service reaches you
   last (choice gone).
3. **Lav-adjacent** — one row of buffer minimum; the aisle seat
   beside a lav gets bumped all night.
4. **Bulkhead trade** — legroom yes, but: no under-seat storage at
   your feet (all overhead, boarding-race), armrest-mounted trays
   (fixed, narrower), often bassinet territory = babies.
5. **Exit row trade** — legroom yes, but: no floor storage during
   takeoff/landing, colder at doors, tray in armrest (wider gap,
   no lift-over), must be able-bodied (no lap infants, often no
   under-15s), seat ahead of you is the recline trap #1.
6. **Missing-window rows** — some rows on 787/A350 have a blank
   wall panel or misaligned window; row maps rarely mark it.
7. **Over-wing rows** — engine noise peaks + view is all wing; on
   short-hops irrelevant, on 6 h flights it matters.
8. **"Premium" row scams** — first 2-3 economy rows priced as
   "preferred" are just... rows, sometimes WORSE (bulkhead traps)
   — check what you're actually buying.

## Strategy by Flight Type

- **Red-eye solo:** window + front third (deplane fast at 6 AM,
   meal cart passes early) + away from lavs. Eye mask regardless.
- **Red-eye pair on 3-3:** window+middle SAME side (keep the pair
   intact) or the window+aisle gambit on a light flight.
- **Day flight pair:** window+aisle across… no — window+middle
   together; people take the empty middles LAST, so if flight is
   <80% you often get the middle free ("poor man's premium").
- **Family + toddler:** SPLIT across the aisle (adult+A, adult+child
   across) — toddler gets window entertainment, two adults tag-team,
   no trapped stranger.
- **Family + infant:** bassinet bulkhead (book early, limited) or
   any window pair; lap infant can't sit in exit rows — the whole
   party.
- **Big group:** split 2+2 pairs rather than a full row — full rows
   get broken up by equipment changes more often.
- **Anxious flyer:** over-wing = smoothest ride (near center of
   lift); aisle for control, not window.
- **Motion sickness:** over-wing, window for horizon reference.
- **Tall (190cm+):** exit row or bulkhead genuinely worth paying;
   standard pitch puts knees into the seatback mechanism.

## Common Pitfalls

1. **Paying for exit row without checking the row AHEAD.** You
   bought 21A; if 20 is the last row before exit... you ARE 21A.
   But buying 20A to save money = no recline for 4 h.
2. **Bulkhead with a lap infant assumption.** Bassinets are
   limited, weight-capped (~11-14 kg), must request in advance;
   showing up with a baby does not get you bulkhead.
3. **The 3-4-3 middle.** On dense 777s, D-G block middles (E/F on
   3-4-3) are picked last for a reason. Take a 2-side window.
4. **Back-of-bus for quiet on a wide-body.** Galley + lav cluster
   zones beat "engine noise" placement every time — the engines are
   far away on a 777; the lav door is 40 cm away.
5. **Trusting the airline map's "good seat" color.** Those colors
   sell inventory. The trap rows are usually colored fine.
6. **Ignoring equipment change risk.** Sub-fleet swaps (737-800 →
   MAX8, A320 → A321) silently move your carefully picked row;
   re-check at T-24 h check-in.

## Example

```
$ seat_picker.py decode --seat 14C --aircraft a320
SEAT 14C — A320 FAMILY (3-3)
  POSITION: aisle, LEFT side (A window | B middle | C aisle | D aisle | E middle | F window)
  ZONE: over-wing rows on A320 typically 10-16...
  WARN: engine noise band; exit rows often right behind (check
  14-vs-15 recline on YOUR airline's map)

$ seat_picker.py choose --flight red-eye --party 2 --pref sleep
RED-EYE, PARTY OF 2, PRIORITY: SLEEP
  1. window+middle together, same side, front third, ≥2 rows from lavs
  2. if flight likely light (<80%): window+aisle gamble (middle
     fills last)
  3. AVOID: exit rows (armrest trays are narrow, cold at doors),
     row ahead of exit (no recline), last 3 rows (lavs+service)
```

## Verification Checklist

- [ ] Aircraft family confirmed (booking page or Flightradar-type
      lookup); seat letters re-decoded for THAT family
- [ ] Trap list checked against chosen rows (recline, lavs, bulkhead)
- [ ] Flight-type strategy applied (red-eye ≠ day-flight logic)
- [ ] Party layout chosen (together vs split for kids)
- [ ] Re-verify at T-24 h — equipment changes move rows
