---
name: parking-spot-memory
description: Use when parking anywhere you'll return to unfamiliar — airports, stadium garages, hospital lots, rental cities, massive mall structures — logs level/row/section/photo/paid-until at park time, answers "where did I park?" with elapsed time and level-first search guidance, watches meter/session expiry, and keeps a per-location history so the same garage never stumps you twice.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [parking, car, airport, garage, find-my-car, memory-aid, meter]
---

# Parking Spot Memory

Every driver knows the walk of shame: circling level 4 of an airport
garage at 1 AM, key fob raised, trying to remember whether it was
"blue row D" or "D row blue." The failure is structural — parking
spots are low-distinctiveness information encoded at a moment you're
distracted (navigation ending, luggage, kids), retrieved hours or
days later in a different mental state. The fix is a 10-second
capture ritual at park time. This skill is that ritual plus instant
retrieval with level-first search guidance and meter-expiry watch.

## When to Use

- Airport / train-station / cruise-terminal parking (the multi-day,
  huge-structure, jet-lagged worst case)
- Stadium, concert, festival, hospital, and mall garages — anywhere
  the structure repeats floor-to-floor
- Street parking in an unfamiliar city ("which side street was it?")
- Rental cars (worse: unfamiliar plate AND car)
- Any paid parking — the expiry watch prevents tickets

Don't use for: your own driveway (you know), valet (the ticket is
the memory — keep the ticket), or EV charging sessions (the car's
app knows).

## The 10-Second Park Ritual

Capture **before leaving the car** — once you walk away, the detail
half-life begins:

1. **Look at the nearest marker** — pillar/beam sign (level+row) or
   meter number. Say it out loud once (audio encoding helps).
2. **Photograph it** — one photo: the marker + your car in frame, or
   the space from where you stand. The photo is the backup brain.
3. **Log it**:
   ```bash
   python3 scripts/parking_memory.py park \
       --location "Airport T2 garage" --level P3 --row D \
       --section blue --photo IMG_4812.jpg \
       --paid-until "2026-10-19 17:16" \
       --notes "near elevator 2, next to pillar"
   ```
4. If paid: log the expiry time immediately (`--paid-until`), not
   "later" — later is when tickets happen.

## Retrieval (the 1 AM scenario)

```bash
python3 scripts/parking_memory.py find
```

Returns the full record with elapsed time, then **level-first
guidance**: levels are the biggest filter (a P3-vs-P4 mistake costs
10 minutes; a row mistake costs 1), so the output orders your search
— level → elevator bank → row → landmark photo check. If you logged
a photo reference, it reminds you to compare aisle markers against
it rather than trusting recall.

For a specific past trip: `find --location hospital` filters by
substring. `list -n 20` shows recent history (and reveals your
patterns — same garage, same good zone).

## Meter / Session Expiry Watch

```bash
python3 scripts/parking_memory.py expiry
```

Scans recent entries for active `paid_until` sessions: minutes left
with a LOW flag under 30, or EXPIRED with how long ago — the
difference between "top up now" and "check for a ticket / max stay
violation" before you return to the car.

## Common Pitfalls

1. **Logging after walking away.** The single biggest failure mode;
   detail recall collapses within minutes. The log entry takes 10
   seconds *in place*.
2. **Recording only the level.** "P3" alone in a 400-space structure
   is a 20-minute search. Level+row minimum; add section/color when
   the garage color-codes.
3. **Trusting memory of "I'll remember the number."** Parking
   markers are deliberately low-distinctive (D-34, D-43, D-3B...).
   That's why they're forgotten.
4. **Skipping the photo.** The photo survives everything — wrong
   level guess, bad notes, week-long trips. One frame, zero cost.
5. **Ignoring the exit side.** Note which exit/elevator you used
   (`--notes "near elevator 2"`); returning to the wrong elevator
   bank in a symmetrical garage recreates the lost-car experience
   even with the right row.
6. **Not logging paid-until at payment time.** Reconstructed expiry
   times are wrong exactly when fines are highest.

## Verification Checklist

- [ ] Logged at park time, not at destination
- [ ] Level + row minimum captured (photo strongly recommended)
- [ ] `paid_until` set at the moment of payment
- [ ] On return: `find` read BEFORE entering the structure
- [ ] Landmark/exit note included for large or symmetrical garages

## One-Shot Recipe: rental-car return week

```bash
# day 1, at the space:
python3 scripts/parking_memory.py park --location "MIA Economy Purple" \
    --row "R14" --photo rental_keyfob_0421.jpg --plate "8XYZ421" \
    --notes "shuttle stop 4, dented rear bumper left"
# every return day:
python3 scripts/parking_memory.py find
```
Rental plate in the log turns "which of these 40 white Corollas"
into a lookup.
