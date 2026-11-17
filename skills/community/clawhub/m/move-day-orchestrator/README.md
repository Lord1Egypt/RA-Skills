# Move Day Orchestrator

**Skill:** `move-day-orchestrator` · v1.0.0 · MIT · ClawHub `@voronindenis5/move-day-orchestrator`

## The real-world problem

Moving ranks among the most stressful life events in survey after survey — and almost none of the pain is inherent. It's coordination failure: the truck is one size too small, the first-night box is somewhere in 40 identical boxes, the bed's bolts vanished into "a safe place", nobody reserved the elevator, the kettle can't be found for a week, and the whole day dissolves at 4PM when the crew gets tired and nobody has a list.

A move is a project with a critical path — it just never gets treated as one. This skill treats it as one.

## What it does

Pure-stdlib Python, state in a local JSON:

- **`set --date`** — registers the move, computes days remaining, flags the under-2-weeks crunch
- **`estimate`** — truck class from volume presets (studio→4-bed × light/normal/heavy density) or bottom-up itemized big items (+12% packing air); box counts by size, blankets, and crew-hours with stairs (×1.5–2) and elevator (×1.15) multipliers
- **`plan`** — the countdown: T−8wks (mover quotes, permits, declutter) → T−4 (utilities overlap strategy) → T−2 (packing waves, fridge defrost) → T−1day → moving day → T+1wk, with lead-time warnings (movers 4–6 wks in season, internet slots 2–3 wks)
- **`waves`** — packing ranked by days-until-needed, not room convenience; storage first, kettle never; includes the per-room first-night-box pulls
- **`box` / `find`** — box inventory: ROOM-SEQ labels (KIT-01), contents keywords, open-first/fragile flags; `find kettle` beats opening 12 "Kitchen" boxes
- **`runshow`** — the hour-blocked day-of command sheet: protect floors → load heavy-first → the car-manifest checkpoint (docs/meds/laptop/plants/first-night box NEVER in the truck) → final sweep → meter photos → keys
- **`arrival`** — first-24h priorities (utilities on, beds, bathroom, kitchen basics, fridge upright 4h) and the first-week box queue

## Who needs this

- **Anyone moving home** — ~10% of households move in a given year (US ~26M moves/yr; tens of millions more worldwide)
- **DIY + friends movers** — the run-of-show prevents the 4PM fog; the estimate prevents the second-trip-through-traffic disaster
- **First-time movers** who don't know elevator reservations and parking permits exist until the truck gets a ticket
- **Families** — kids/pets off-site plan, comfort toys in the car, beds-first arrival so everyone sleeps
- **The invisible coordinator** of any shared move — a printed run sheet ends the "what's left?" loop

## Example

```bash
python3 scripts/move_orchestrator.py set --date 2026-11-14 --from "2-bed apt 65m2, 3rd fl" --to "house"
python3 scripts/move_orchestrator.py estimate --home 2bed --density normal --stairs 3
# ESTIMATE: ~18 m3 | truck: 26' box truck (usable ~22 m3, keep 10% headroom)
#   crew: 2 pros x 9h load (stairs x1.6) | boxes ~25 + 8 blankets
python3 scripts/move_orchestrator.py runshow --start 08:30 --crew 3 | lp   # tape to the door
python3 scripts/move_orchestrator.py find kettle   # -> KIT-01 (open-first, in the CAR)
```

## License

MIT © Denis Voronin. Estimates are planning heuristics; mover quotes override. Pianos/safes/marble = rigging professionals, always.
