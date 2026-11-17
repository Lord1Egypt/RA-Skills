# Pet Poison Triage

Species-aware first-response toxicity triage for dogs and cats:
hazard scoring, dose math for the calculable toxins (chocolate,
xylitol), unknown-toxin protocols (grapes, lilies), plant risk lookup,
and the pet poison kit.

## The Real Problem

ASPCA Animal Poison Control handles 400,000+ cases/year; the typical
pet owner facing a poisoning at night has two failure modes: panic
(useless or harmful folk remedies — salt, milk, peroxide in cats) or
"he seems fine" (the deadly toxins all have lag: antifreeze's fake
recovery, rat poison's 3-5 day silence, lily kidney failure at 24h).
Outcomes hinge on minutes-to-correct-action and dose math vs vibes —
30 g of baking chocolate is a different universe from 30 g of milk
chocolate, and cats are not small dogs (lilies deadly/xylitol harmless
vs the exact reverse in dogs).

## What It Does

- **triage** — hazard class for the species + first-30-minutes
  protocol (never induce vomiting unless told; fur decontamination)
- **chocolate** — theobromine mg/kg across 7 product types vs
  symptom/mild/moderate/severe bands
- **xylitol** — 0.1 g/kg hypoglycemia and 0.5 g/kg AKI thresholds,
  piece-counting for gum, birch-sugar rename trap
- **grapes** — no-safe-dose protocol with monitoring windows
- **plants** — true lily vs peace lily vs lily-of-the-valley (three
  different emergencies), sago palm, more
- **kit** — poison kit checklist + emergency card template
- **references/** — full toxin grid with onset windows and lag traps,
  decontamination rules, hotline numbers, toxic-vs-safe plant lists

## Quick Start

```bash
python3 scripts/pet_poison_triage.py triage "sugar-free gum" --species dog
python3 scripts/pet_poison_triage.py chocolate --product dark --grams 100 --weight-kg 20
python3 scripts/pet_poison_triage.py xylitol --grams 3 --weight-kg 25 --pure
python3 scripts/pet_poison_triage.py triage lily --species cat
python3 scripts/pet_poison_triage.py kit
```

Stdlib only, offline. NOT a substitute for a vet or poison hotline —
it exists to make that call faster and better-informed.

## License

MIT © Denis Voronin
