# Grill Tank Fuel Forecaster

Propane grill-tank fuel forecasting from a bathroom scale: weigh-ins
with tare subtraction, hours-to-reserve at your grill's real BTU draw,
session/annual consumption, party GO/NO-GO thresholds, and exchange vs
refill economics.

## The Real Problem

Propane 20 lb cylinders have no usable fuel gauge — the gauge on some
grills measures pressure, which stays flat-ish until the tank is
nearly gone. The only honest measurement is mass, and most people
never make it: they guess, run out mid-party (the classic 4th-of-July
failure), or over-correct and swap "half-full" tanks at the exchange
cage — surrendering their own propane to a company that charges ~$1.73
per delivered pound while the refill station down the street charges
~$0.95. For a 2-cooks-a-week household that habit is worth roughly
$470 a year.

Meanwhile the math everyone uses is wrong in both directions: the
"30 cookouts per tank" sticker assumes one burner and short cooks,
while the rating plate's "48,000 BTU" assumes every burner plus the
side burner blazing at once. Real consumption lives in between and is
computable — 21,600 BTU per pound, sum the burners you actually light,
apply a duty cycle, keep a 20% reserve floor.

This skill is for: anyone who cooks on a 20 lb tank and owns a bathroom
scale, hosts parties where a flameout is embarrassing, budgets the
season's propane, or keeps choosing the exchange cage because the math
to compare was never in front of them.

## What It Does

- **weigh** — scale reading → lb/g of fuel left (tare-subtracted),
  hours of burn to the 20% reserve floor at your lit BTU
- **session** — per-cook fuel with preheat + duty-cycle corrections →
  sessions per tank, weeks per tank, tanks/yr for your routine
- **plan** — hours × guests with grate batching and re-fire margin →
  minimum scale weight for GO, checked against your current reading
- **compare** — exchange vs refill: $/lb at local prices, sessions per
  tank, annual cost at your actual usage, to-fumes vs to-reserve
- **references/tank-math.md** — the full burn-rate table by grill
  class, the 453.6 g/lb vs 424 g/lb unit trap, consumption model, and
  the safety rails (clearance, soapy-water leak checks, storage)

## Quick Start

```bash
python3 scripts/tank_forecast.py weigh --tare-lb 17 --current-lb 15.2 --burner-btu 36000
python3 scripts/tank_forecast.py session --burner-btu 36000 --hours 2.5 --sessions-week 2
python3 scripts/tank_forecast.py plan --cook-hours 3 --guests 8 --current-lb 31.4
python3 scripts/tank_forecast.py compare --exchange-cost 26 --refill-cost 19
```

Stdlib only, offline, `--json` on every subcommand. Exit 0 on success,
2 on bad input. Not a substitute for your supplier's certified scale —
it's the planning layer between you and the flameout.

## License

MIT © Denis Voronin
