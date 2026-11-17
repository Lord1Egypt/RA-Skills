# Hand-Me-Down Flow

**Every family with two kids runs a logistics system nobody wrote down.**
Bins of outgrown clothes, a crib in the garage, three winter coats in a
closet — and the younger kid outgrows half of it before anyone opens the
bin. Attics quietly destroy the rest.

## The Problem

- "2T" doesn't mean 2 years old — it fits a median 20–28-month-old.
  Families miss whole seasons because the label lied.
- Attic summer heat (50–65 °C) embrittles elastic, foam, and laminates
  in 1–3 seasons; basements mildew cotton above ~65% RH. "Stored for
  the next kid" often means "composted."
- Mystery bags between families: ungraded hand-me-downs get donated
  unopened because the receiving parent can't tell treasure from trash.
- Nobody knows when to pull what. The question "what do we have for the
  3-year-old this winter?" has an answer — it's just not written down.

## What This Skill Does

`scripts/handmedown.py` — a registry of stored items (size, season,
A–D condition grade, location) plus per-kid birthdays, and a **match
pass** that computes fit windows from size labels and tells you, per
kid: PULL NOW, IN THE NEXT 6 MONTHS, and which windows are closing.
Chain verdicts flag items with no future recipient (donate now), and
`manifest` prints a graded transfer list so hand-offs between families
actually get used.

```bash
python3 scripts/handmedown.py --data fam.json add-kid --name Mia --birthday 2021-04-10
python3 scripts/handmedown.py --data fam.json add --name "snowsuit" --category outerwear \
  --size 4T --season winter --condition B --location "closet bin 2"
python3 scripts/handmedown.py --data fam.json match
python3 scripts/handmedown.py --data fam.json manifest --to "cousin Emma"
```

## Who Needs This

- Families with 2+ kids rotating clothes/gear
- Cousin/friend hand-me-down circuits (both directions)
- Parents storing for a future baby — deciding what's worth keeping
- Anyone who's opened a bin of ruined clothes and wondered what happened

## Example

Mia (born Apr 2021) is 43 months old; Leo (Sep 2023) is 37 months. A
B-grade 4T winter coat (fits median 38–46 mo) matches Leo NOW — pull it
this season. The same coat for Mia is one season from outgrown; the
chain verdict shows her window closing. A 24M summer outfit matches
nobody and never will (Leo is already past it): PASS ALONG / DONATE —
with the reason printed.

## License

MIT — see LICENSE.
