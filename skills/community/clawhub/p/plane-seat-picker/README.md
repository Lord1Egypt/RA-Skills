# Plane Seat Picker

**The seat map is a puzzle and the airline's legend won't tell you
that 24A doesn't recline.**

Decodes any seat to its actual position per aircraft family (3-3,
2-3, 3-3-3, 3-4-3 — letters drift), flags the structural traps
(row-ahead-of-exit no-recline, last-row lav halo, bulkhead
trade-offs, missing-window rows), and picks strategy by flight
type: red-eye sleep math, family splits for toddlers, bassinet
rules for infants, the window+aisle empty-middle gamble, tall
flyer legroom worth paying for.

## What it does

- **decode** — seat + aircraft family → position, zone, warnings
- **aircraft** — family facts: layout, pitch, width, what actually
  changes comfort (A220 has no bad seat; 777 middle-of-4 is the
  worst in economy; A380 upper deck is the quiet secret)
- **choose** — flight type × party size × preference → ranked
  concrete seat patterns
- **families** — infant (bassinet/bulkhead/lap rules) vs toddler
  (split-across-aisle doctrine) vs older kids
- **traps** — the 8 master traps with WHY for each

## Quick start

```bash
python3 scripts/seat_picker.py decode --seat 14C --aircraft a320
python3 scripts/seat_picker.py choose --flight red-eye --party 2 --pref sleep
python3 scripts/seat_picker.py families --kids toddler --adults 2
python3 scripts/seat_picker.py traps
```

Stdlib-only Python 3, offline. 9 aircraft families with zone logic
that holds across airline configurations.

## License

MIT
