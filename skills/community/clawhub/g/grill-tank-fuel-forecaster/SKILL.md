---
name: grill-tank-fuel-forecaster
description: Use when a propane grill cook is planned and tank level is unknown or suspect — bathroom-scale weigh-in with tare (TW stamp) subtraction giving lb and grams of fuel left and hours of burn to a 20% reserve floor at your grill's total lit BTU (21,600 BTU/lb math, 1 lb = 453.6 g, the 424 g/lb and 4.24 lb/gal trap), cook-session consumption with preheat and duty-cycle corrections, party planning with guest-count batching, re-fire margin and GO/NO-GO scale thresholds, and cage-exchange vs refill economics ($/lb with 15 lb exchange fills vs 20 lb refills, annual cost at real usage) plus the safety rails — 5-10 ft clearance, soapy-water leak checks, never store or check leaks indoors.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [propane, grill, bbq, tank, fuel, forecasting, btu, exchange-vs-refill, safety]
---

# Grill Tank Fuel Forecaster

It's Saturday, 18 guests arrive in three hours, and the tank gauge —
there is no tank gauge. Propane cylinders have no usable fuel meter;
the only honest reading is mass on a bathroom scale. Meanwhile the
marketing says "30 cookouts per tank," the exchange cage quietly hands
you 15 lb for a 20 lb price, and every grill fire season starts with a
tank too close to the siding. This skill turns a scale reading and a
rating plate into numbers you can cook to: hours left, sessions per
tank, the minimum scale weight for tonight's party, and whether
exchange or refill is burning ~$470/yr.

## When to Use

- "How much gas is left?" — weigh the tank, get lb/g remaining and
  hours of cook time to a 20% reserve floor at your actual lit BTU
- Pre-party GO/NO-GO: is THIS tank enough for 3 hours × 8 guests, with
  re-fire margin, or do you swap now?
- Estimating how long a tank lasts your routine (weeks per tank,
  tanks/yr) before the season starts
- Deciding exchange cage vs refill station: real $/lb, the 15 lb
  exchange-fill gotcha, and what swapping early costs you in
  surrendered fuel
- Buying/sizing a grill: translating "48,000 BTU" into lb/hr you'll
  actually feed it
- Setting up the safe operating baseline: clearance, leak checks,
  storage, recert dates

## The Method

```bash
# 1. Weigh-in: scale reading → fuel left and hours to the reserve floor
python3 scripts/tank_forecast.py weigh --tare-lb 17 --current-lb 15.2 \
    --burner-btu 36000
# → 15.2 − 17 is negative → net-input mode: 15.2 lb fuel? No — reading
#   <= tare is interpreted as already-tare-subtracted NET fuel.
#   For a tank ON the scale: --current-lb 32.0 → 15.0 lb left.

# 2. Your routine: how long does a tank last, how many per year
python3 scripts/tank_forecast.py session --burner-btu 36000 \
    --hours 2.5 --sessions-week 2
# Thermostated/grill-marker? add --duty 0.6 and --preheat-min 10.

# 3. Party plan: minimum scale weight before ignition, GO/NO-GO vs yours
python3 scripts/tank_forecast.py plan --cook-hours 3 --guests 8 \
    --current-lb 31.4
# 16 guests on an 8-serving grate → 2 batches → 2× cook time.

# 4. Exchange vs refill at YOUR prices and usage
python3 scripts/tank_forecast.py compare --exchange-cost 26 \
    --refill-cost 19 --hours 2.5 --sessions-week 2
```

Add `--json` to any command for machine-readable output.

## The Numbers That Drive Everything

| Constant | Value | Why it matters |
|---|---|---|
| BTU per lb propane | 21,600 | BTU rating plate → lb/hr clock |
| 1 lb in grams | 453.6 | 424 g is lb/gallon garbled, 7% off |
| Liquid propane density | 4.24 lb/gal | 20 lb fill ≈ 4.7 gal |
| Tare (TW), steel 20 lb | ~17 lb | reading − TW = fuel left |
| Full tank on the scale | ~37 lb | 15 lb exchange fills read ~32 lb |
| Reserve floor | 20% of fill | output falls off below it; never plan past it |

Burn rates at common configurations (all burners lit, full output):

| Grill | Total BTU | lb/hr | Full-tank hours (to reserve) |
|---|---|---|---|
| Portable/tabletop | 10,000 | 0.46 | 34.8 hr |
| 2-burner | 26,000 | 1.20 | 13.3 hr |
| **3-burner (default)** | **36,000** | **1.67** | **9.6 hr** |
| 4-burner | 44,000 | 2.04 | 7.8 hr |
| 6-burner + rear | 66,000 | 3.06 | 5.2 hr |

Full burn-rate table with side burners and per-cook costs:
`references/tank-math.md` §2.

## Common Pitfalls

1. **Believing the "30 cookouts per tank" sticker.** That's one burner,
   short cooks, no preheat. A 3-burner at 2.5 hr × 2/wk burns ~9 lb/wk
   — a tank every 2 weeks, not every season. Run `session` with your
   real numbers.
2. **Reading 424 g as grams-per-pound.** That's 4.24 lb/gal with the
   units mangled; a pound is 453.6 g. Scales that show grams need the
   right constant or you're off 7%.
3. **Trusting the exchange cage's "full."** Exchange tanks are filled
   to ~15 lb, not 20 — you pay ~$1.73/lb vs ~$0.95/lb refilled, and
   swapping early gifts them your remaining fuel. `compare` runs your
   actual prices.
4. **Assuming tare is 17 lb.** Aluminum cylinders run 13-14 lb; steel
   varies 16.6-18.0. Read the TW stamp on the collar — an assumed tare
   is a ±1 lb fuel error before you start.
5. **Planning to empty instead of to the reserve.** Output sags badly
   below ~20%, cold weather makes it worse, and a flameout mid-party
   is the failure mode. All hours here stop at the floor.
6. **Summing the rating plate's max BTU as your draw.** If two of four
   burners run at medium, you're at ~25% of plate. Sum what's lit,
   apply duty ~0.6 for medium — otherwise you'll carry backup tanks
   forever.
7. **Weighing with a hot or frosty tank.** Condensation adds ~0.1-0.3
   lb; a hot tank after a cook reads high from... nothing, actually,
   but the scale drifts. Weigh cold and dry, before cooking.
8. **Checking for leaks with a flame.** Soapy water only. The lighter
   "test" is how garages disappear — see safety below.

## Safety — Non-Negotiable

- **5-10 ft clearance, outdoors only.** ≥5 ft from siding/eaves/rails,
  never under an awning or in a garage with the door open.
- **Never store tanks indoors** — spare cylinders live outside, upright,
  away from entries. Propane pools at floor level and finds pilots.
- **Leak check = soapy water, never a flame.** Bubbles at the fitting
  mean shut the valve, reseat, retest. New hose or post-swap, every time.
- **Transport upright, valve closed**, never in a hot parked car.
- **Recert:** collar date + 12 years (then 5-year requal). Exchanges
  take anything; refillers check.

Full rules with incident patterns: `references/tank-math.md` §6.

## Verification Checklist

- [ ] TW stamp read off the collar (not assumed 17 lb)
- [ ] Scale reading taken cold/dry, tank off the grill
- [ ] Burner BTU = sum of burners actually lit (plate is max-everything)
- [ ] Duty cycle set (1.0 wide-open manual, 0.6-0.7 thermostated/medium)
- [ ] All hour figures are to the 20% reserve, not to empty
- [ ] Exchange fills modeled at 15 lb, refills at 20 lb
- [ ] Party plan includes margin + reserve, not just raw cook fuel
- [ ] Tank clearances, storage, and leak-check rules from §6 reviewed
      before the season starts

## References

- `references/tank-math.md` — BTU derivations, the full burn-rate
  table by grill class, weight-based fuel semantics (453.6 g/lb vs the
  424 trap), the cook-session consumption model, exchange vs refill
  economics with worked annual numbers, and the safety rails.
