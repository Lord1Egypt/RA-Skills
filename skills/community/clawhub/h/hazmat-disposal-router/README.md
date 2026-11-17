# Hazmat Disposal Router

**Don't guess. Don't drain. Route it.** Every garage and under-sink
cabinet holds 5-15 items that are illegal or dangerous to trash — old
paint, car batteries, lithium packs, motor oil, pesticides, propane,
CFLs, meds, needles. Most people guess, and the wrong guesses start
garbage-truck fires (lithium), poison waterways (oil: 1 L ruins a
million liters), and injure sanitation workers (needles in soda
bottles).

This toolkit gives you:

- **Item verdicts** — 35+ item families → trash / HHW facility /
  retailer drop-off / pharmacy / sharps / professional, each with the
  WHY in one line and the warning that matters.
- **Cleanout audit mode** — list the whole garage haul at once, get a
  grouped manifest by channel + a minimum-trips plan.
- **Interim storage rules** — the safe limbo between cleanout and
  drop-off day (lithium taping, no-mixing, original labels).
- **Channel finders** — US / EU / UK: where each channel lives near
  you (Earth911, PaintCare, WEEE retailer law, HWRC, pharmacy
  take-back).
- **The never list** — 10 common mistakes, each with the reason it's
  a mistake.

## The real-world problem
HHW programs exist almost everywhere but participation is low because
routing knowledge is fragmented. The average household's cleanout
mixes 2-3 genuinely hazardous items into ordinary trash — and
collection agencies across the US/EU report battery-driven truck
fires as their fastest-growing hazard.

## Quick start
```bash
python3 scripts/hazmat_router.py dispose --item "li-ion battery"
python3 scripts/hazmat_router.py audit --items "latex paint,car battery,CFL bulbs,old gasoline,weed killer"
python3 scripts/hazmat_router.py channels --region EU
python3 scripts/hazmat_router.py never
```

Pure Python stdlib. Offline. Verdicts are the consensus safe default;
verify local rules with your municipality.

## License
MIT © Denis Voronin
