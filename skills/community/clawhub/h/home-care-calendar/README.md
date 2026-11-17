# Home Care Calendar

**The maintenance schedule your house wishes somebody was keeping.**

Homes decay on schedules nobody memorizes. The HVAC filter chokes for 18
months until the compressor dies ($4,000). Gutters fill until the fascia rots
($2,500). The water heater sediment layer grows until efficiency tanks. Every
one is a $12–$50 task whose neglect becomes a four-figure repair — and the
difference is just *remembering*.

Home Care Calendar turns a 10-minute inventory into a whole-home maintenance
system:

- **Guided inventory** — walk through ~25 standard home systems (furnace,
  filters, water heater, gutters, detectors, sump, chimney, deck, trees…),
  record install dates and notes
- **Auto-generated calendar** — every item maps to interval tasks from real
  maintenance science (filter 1–3 mo, HVAC service yearly, heater flush
  yearly, chimney 2 yr, detectors at DST changes) with why/how/effort/DIY-vs-pro
- **Seasonal intelligence** — furnace service before heating season, gutters
  after leaf-drop (not equinox), tree pruning in late winter
- **Completion tracking** — `done` resets each interval clock; history stays
- **ICS export** — tasks land in Google/Apple/Outlook calendar as all-day
  events with instructions
- **Deferred-maintenance debt** — every overdue task carries an expected-value
  neglect cost; the report sums your total in dollars, and every `done`
  shrinks it

Pure stdlib Python; state in one local JSON file.

## Quick Start

```bash
# One-time: guided inventory (walks you through the standard systems)
python3 scripts/home_care.py inventory

# Or add items directly
python3 scripts/home_care.py add --kind furnace --installed 2019 --last-done 2025-11-15

# This month / next 90 days / full seasonal year
python3 scripts/home_care.py calendar
python3 scripts/home_care.py calendar --days 90
python3 scripts/home_care.py calendar --year

# After completing a task
python3 scripts/home_care.py done hvac-filter:1

# Export to your calendar app
python3 scripts/home_care.py ics home-care.ics

# How much deferred maintenance am I sitting on?
python3 scripts/home_care.py debt
```

## Example: `debt`

```
DEFERRED-MAINTENANCE DEBT: $2,737

  $1,799.33  Water heater sediment flush — 2699 days overdue
  $ 899.67  TPR valve test — 2699 days overdue
  $  36.50  Furnace visual check — 219 days overdue
  $   1.67  HVAC filter change — 2 days overdue

Every `done` shrinks this number. Start with the top item.
```

After `done water-heater:1` (a 30-minute DIY flush): **$2,737 → $936.**

## Who Needs This

- **New homeowners** — the first-year maintenance schedule nobody hands you at
  closing
- **Busy owners** — "when did we last service the furnace?" answered instantly
- **Landlords** — per-property registries; diligence records
- **Renters** — filters, detectors, drains, caulk + documentation for deposits

## The Interval Library

~25 systems, 35+ tasks with intervals consolidated from manufacturer
guidance, EPA/DOE/ACCA HVAC standards, NFPA fire-safety recommendations, and
insurance practice — documented in
[references/task-library.md](references/task-library.md).

## License

MIT — see [LICENSE](LICENSE).
