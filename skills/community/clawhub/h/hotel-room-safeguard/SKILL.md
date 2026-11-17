---
name: hotel-room-safeguard
description: Use when checking into a hotel, hostel, or rental room — runs the first-15-minute protective sweep (bedbug harborage inspection order, hidden-camera RF/lens/emission checks ranked by risk, safe-vs-dresser valuables protocol, exit-route count) and logs evidence with timestamps if something IS found, so a bad room is caught before you unpack, not after you wake up with bites.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [travel, hotels, bedbugs, hidden-cameras, privacy, safety, security]
---

# Hotel Room Safeguard

## Overview

Two risks dominate bad hotel rooms: bedbugs (one pregnant female hitchhikes
home in your luggage and costs $1,500–$5,000 in extermination) and hidden
cameras (increasingly found in rentals; smoke detectors, clocks, and phone
chargers are the classic hosts). Both are checked in under 15 minutes with
unaided eyes and a phone flashlight — IF you know the search order and the
signatures. `scripts/room_sweep.py` is a guided audit: it walks the
bedbug harborage sequence (mattress seams → box spring → headboard →
luggage rack), scores camera-risk hotspots, and produces a dated evidence
log with a demand/escalation letter if findings force a room change.

## When to Use

- Check-in at any hotel, hostel, vacation rental, or budget accommodation —
  especially high-turnover rooms in bedbug-prone regions.
- Waking up with bites: evidence protocol + what to demand from the property.
- Renting rooms/stays where hidden-camera concern is real (the lens-glint
  scan takes 4 minutes).
- Deciding where the passport and laptop actually go overnight.

**Don't use for:** mattress shopping (different inspection), or as a
substitute for police when you FIND a camera — this skill's job is
detection + evidence + escalation, and calling the front desk/police is
part of the escalation path.

## How It Works

### 1. Bedbug sweep (inspection order matters — most-likely spots first)

1. Strip the bed near the head; keep the mattress pad as a tray.
2. **Mattress seams and piping** — run a fingertip along every seam: live
   bugs (apple-seed, 4–5 mm), dark fecal smears (marker-dot clusters),
   translucent eggs, amber shell casings.
3. **Box spring underside and corner guards** — the #1 harbor in infested
   rooms; peel back the mesh.
4. **Headboard** — remove if hinged; check screw holes and the wall gap.
   Cloth headboards: seam + tuft check.
5. **Bed frame joints and legs**, nightstand drawers (top drawer especially),
   behind the nightstand, wall art above the bed, luggage rack folds.
6. Room edges: baseboard seams, carpet edge under the bed, curtain hems near
   the floor, any wall plug or phone jack near the head of the bed.

Verdict logic: live bug or eggs = LEAVE (larvae/eggs mean an established
colony); fecal smears alone = treat as infested until proven otherwise
(demand a different room, NOT adjacent — bugs travel along walls).

### 2. Hidden-camera check

Risk-ranked scan (phone only):

1. **Darkness lens scan** — lights off, blinds closed; sweep the phone
   flashlight at suspected devices: a pinhole lens returns a blue-white
   glint. Cover: smoke detector, clock radio lens dot, phone charger blocks,
   air-vent grilles, wall plugs at chest height facing the bed/bath, "motion
   detector" discs, power strips, decorative objects with a line-of-sight to
   the bed or shower.
2. **Heat/field check (cheap detectors)** — lens-finder tools and RF
   sweepers exist for $20–60, but treat them as supplementary: false
   positives from Wi-Fi gear; a wired camera is RF-silent.
3. **Network check** — count Wi-Fi devices on the room's network where the
   property discloses the router; unexpected always-on devices with
   high traffic merit a physical look at the devices above.
4. **Line-of-sight doctrine** — the question that cuts the search: WHAT CAN
   SEE THE BED AND THE BATH? Stand there, look around, and inspect every
   object with that view. Cameras need a view; the view defines the search.

### 3. Valuables protocol

- Room safe: check it's bolted, test the lock, don't store the laptop if the
  safe is a portable model (they walk out whole).
- Never in the luggage in open view: passports, medication, spare cash.
- Dresser-vs-safe rule: anything you can't afford to lose goes in the safe
  or on your body, never in drawers (staff-accessible, and drawers are the
  first place light-fingered help looks).

### 4. Exit and comfort audit

- Count doors/fire exits; note the route (in smoke you navigate by wall).
- Check door lock, deadbolt, chain, and peephole (cover an unshielded one).
- AC works, window locks, phone reaches the front desk.

### 5. Evidence mode (`--evidence`)

If you find something: photographs with timestamps, the sweep log entry,
the property's response — then the script drafts the escalation letter
(room change / refund / medical note for bites / police report reference
for cameras) citing what was documented and when.

## Using the Script

```
# guided first-15-minutes sweep (interactive-free, prints checklist + verdicts)
python3 scripts/room_sweep.py --sweep

# log a finding with evidence
python3 scripts/room_sweep.py --log --finding "fecal smears mattress seam" \
  --room "407" --property "Riverside Inn" --photos 3

# generate the escalation letter from logged findings
python3 scripts/room_sweep.py --letter --room "407" --property "Riverside Inn"
```

## Common Pitfalls

1. **Unpacking first, checking second.** Luggage on the bed or floor IS the
   bridge bedbugs use to get home with you. Luggage stays in the bathtub or
   on the luggage rack until the sweep is done — the rack is metal-legged
   specifically because bugs can't climb it easily.
2. **Checking only the mattress.** The box spring and headboard harbor more
   bugs than the mattress in established infestations.
3. **Demanding the adjacent room.** Adjacent rooms share walls and the same
   infestation; ask for a different floor or wing.
4. **Trusting RF sweepers alone.** Wired cameras don't transmit; Wi-Fi
   cameras hide among legitimate traffic. The lens-glint scan and
   line-of-sight doctrine catch what sweepers miss.
5. **Searching every object equally.** Cameras need power and a view.
   Objects with a bed/bath view that plug in get the close look.
6. **Treating bites as the first signal.** 30%+ of people don't react to
   bedbug bites — absence of bites is not absence of bugs. The seams are
   the truth.
7. **Handling a found camera.** Don't disconnect it. Photograph in place,
   call police (non-emergency), then the property. It's evidence.

## Verification Checklist

- [ ] Sweep done BEFORE luggage touched the bed/floor/sofa.
- [ ] Mattress seams, box spring, headboard, frame, nightstand checked.
- [ ] Lens-glint scan done in darkness on bed/bath line-of-sight objects.
- [ ] Door lock, deadbolt, peephole, exit route verified.
- [ ] Valuables in a bolted safe or on-body; nothing irreplaceable in drawers.
- [ ] Any finding photographed with timestamp + logged before escalation.
