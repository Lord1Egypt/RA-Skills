# Lawn Calendar & Chemist

Lawn care is a timing problem. Crabgrass pre-emergent works only before germination —
which keys off **soil temperature (55°F × 4 days at 2")**, not the calendar on the bag.
This toolkit estimates soil temp from your weather, calls the pre-emergent window
(GO / WATCH / TOO LATE with the post-emergent fallback), computes exact fertilizer dose
and honest cost-per-lb-N from any bag guarantee, and prints a region- and grass-adjusted
annual calendar that catches the fatal conflict: spring pre-emergent killing fall seed.

## The real-world problem

- US households spend ~$100B/yr on lawn & garden; the most common failure modes are
  applying crabgrass preventer **2 weeks too late** (it's a pre-emergent — after
  germination it's fertilizer for the weed) and burning turf with over-dosed nitrogen.
- Bag math confuses everyone: "20-0-8 on a 50-lb bag" — how much for 6,000 ft²?
  Which bag is actually cheaper per pound of N? One command answers it.
- Pre-emergent + overseeding in the same season kills the $200 of seed you just bought.
  The calendar flags the conflict automatically.

## What it does

`scripts/lawn_plan.py` — Python stdlib, no dependencies:

- **`soil-temp`** — 10/30-day lag model estimating 2-inch soil temp from 7-day mean air
  temp; verdict ladder HOLD → WATCH/APPLY → APPLY TODAY → TOO LATE (with quinclorac /
  dithiopyr post-emergent routing and the fall Poa-annua second window)
- **`fert`** — lb N/P₂O₅/K₂O per bag, product pounds needed, cost per lb N, coverage,
  burn-risk flags (slow-release fraction, summer N on cool-season, P on centipede)
- **`calendar`** — 7-region × cool/warm-season dated plan anchored to soil-temp gates:
  pre-emergent rounds, N rounds, aeration/overseeding windows, winterizer; conflict
  checks (spring pre-emergent vs fall seed, spring N on cool grass)

## Quick start

```bash
python3 scripts/lawn_plan.py soil-temp --air-mean 54 --region transition
python3 scripts/lawn_plan.py fert --npk 20-0-8 --bag-lbs 50 --price 32 --area 6000 --n-rate 0.75
python3 scripts/lawn_plan.py calendar --grass cool --region transition --preemergent-spring
```

## Reference

`references/timing-and-math.md` — pre-emergent chemistry table (prodiamine/dithiopyr/
pendimethalin/siduron/indaziflam with residual months), grass-type N budgets, spreader
calibration protocol, fertilizer-burn triage, herbicide class map, soil-test guidance.

## License

MIT © Denis Voronin
