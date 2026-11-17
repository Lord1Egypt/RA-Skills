# Parking Memory Science & Garage Navigation — Reference

## Why parking spots are forgotten

Parking-spot encoding fails for identifiable cognitive reasons, not
because people are careless:

1. **Low-distinctiveness encoding.** "D-43" carries almost no
   pre-existing associations; the brain stores it in the weakest
   memory channel. Random alphanumeric codes with no semantic hook
   decay in minutes to hours.
2. **Divided attention at encoding.** You park while ending
   navigation, checking a boarding pass, managing kids or luggage.
   Attention splits; the code never gets consolidated.
3. **Context shift at retrieval.** Encoded on arrival (fresh,
   daytime, purposeful), retrieved on return (tired, night, jet-lagged
   after a week). Context-dependent memory works against you twice.
4. **Interference.** Every previous garage you've ever used looks
   like this one. Rows, pillars, and cream-colored ceilings are
   near-identical across the entire built environment of parking.

The countermeasures map one-to-one onto the failure modes:

| Failure | Countermeasure |
|---------|----------------|
| weak encoding | say the marker out loud (phonological loop) + photo |
| divided attention | the 10-second ritual BEFORE leaving the car |
| context shift | external storage (the log), not recall |
| interference | level + row + landmark, not "looks familiar" |

## The photo protocol

One photo, taken from the driver's seat or beside the car, should
contain **three anchors**:

1. **The marker** (pillar sign / meter number) — the exact code
2. **The car** (yours, in place) — defeats "found the marker, where's
   the car" and rental-lookalike confusion
3. **A fixed landmark** (elevator door, column with a stripe, exit
   sign) — survives even if the marker is misremembered

Frame beats resolution: a wide shot with all three beats a crisp
close-up of just the sign.

## Level-first search doctrine

When the record is incomplete, search in this order — it minimizes
expected search time:

1. **Level** — the biggest partition of the space (wrong level =
   total miss; walking one level = ~2-4 min)
2. **Elevator/stair bank** — structures are symmetric; the bank you
   entered is a strong anchor if noted
3. **Row/aisle** — walks cheaply once the level is right
4. **Visual scan** — hazard lights via key fob (range ~30-60 m line
   of sight; better near metal ceilings; worse with concrete floors
   absorbing RF)

Fob tips: hold it under your chin (head acts as a crude director),
or against the car you suspect — the receiver proximity matters.
Panic button (hold lock) triggers lights+sound for 30 s on most
models.

## Structure-specific traps

- **Airports:** levels repeat with color themes — note the color word
  with the level ("P3 blue"). Economy lots + shuttle stops: the STOP
  NUMBER is the real address; log it in notes.
- **Malls/stadiums:** exit-door name/number into the venue is the
  anchor you'll see on return (e.g., "Door 7, Marta's side"). Log
  the door, not the row, in notes.
- **Hospitals:** buildings connect at odd levels — garage level B2
  may open into hospital floor 1. Note the building you entered.
- **Street parking:** photograph the nearest cross-street sign AND
  the meter/zone plate; note time restrictions (street cleaning!)
  in `paid_until`/notes.
- **Underground/large structures:** GPS is unreliable — RF-based
  "find my car" features degrade exactly where you need them;
  external memory (this log) doesn't.

## Meter & session management

- Log `paid_until` at the moment of payment — apps show the exact
  expiry; receipts show purchased duration (add to start time).
- The `expiry` mode's LOW flag at <30 min is the "top-up decision"
  threshold for most city meters (walk-back time included).
- EXPIRED display is a triage signal: check the windshield for a
  ticket and the zone's max-stay rules before driving off (some
  violations are cited minutes after expiry; some zones are
  fine for hours).
- Multi-day garages with in/out privileges: note the ticket *number*
  in notes — losing the physical ticket is its own expensive ritual.

## Data notes

- The log (`scripts/data/parking_log.json`) is plain JSON — editable,
  greppable, syncable. Entries are append-only; no delete command by
  design (history is a feature: `find --location` searches it).
- Privacy: entries may contain plate numbers and locations. The file
  lives locally; exclude it from cloud sync if that's a concern.
- Retention: `list -n` reads the tail; prune old entries manually if
  the file grows annoying (years of use ≈ a few hundred entries —
  harmless).

## Integration patterns

- **Voice-first capture:** the log schema is trivial — any assistant
  can write the entry ("log parking level P3 row D"). The script is
  the canonical reader.
- **Photo organization:** keep parking photos in a dedicated album
  named by date; the `photo` field references the filename so the
  album is the index.
- **Calendar pairing:** for airport trips, the parking entry pairs
  with the return-flight calendar event — "where's my car" queries
  correlate with landing times.
