# Tank Math — 20 lb Propane Cylinders

Everything here comes from three constants and one bathroom scale. When
this file and your propane supplier disagree, the supplier wins — they
have the scale and the gauge.

## 1. The BTU Arithmetic

One pound of propane releases **≈ 21,600 BTU** when burned. That single
number converts a grill's rating plate into a fuel clock:

```
burn rate (lb/hr) = total lit BTU / 21,600
hours of burn      = lb of propane / burn rate
```

- 36,000 BTU (a classic 3-burner with all lit) → 36,000 / 21,600 =
  **1.67 lb/hr** → a full 20 lb tank is ~12 hr of wide-open burn.
- 60,000 BTU (4-burner + side burner, all on) → **2.78 lb/hr** → the
  same tank lasts ~7.2 hr.
- 12,000 BTU (one burner on a 2-burner, modest grill) → **0.56 lb/hr**
  → ~36 hr. The knob math matters more than the tank.

Two traps when reading the rating plate:

1. **The plate lists MAX total** — every burner plus side burner plus
   rear infrared, all at full. A "48,000 BTU" 4-burner is 4 × 12,000;
   if you cook on two burners at medium you are drawing roughly
   24,000 × 0.6 ≈ 14,400 BTU. Sum what you actually light.
2. **Knob position is not linear.** Medium is not 50% of max — typical
   burner valves run ~55-65% of max at the medium detent. If you cook
   at medium, multiply the lit BTU by ~0.6 (the `--duty` flag).

## 2. Burn-Rate Table by Grill Class

Approximate total output of the burners people actually light:

| Grill class | Total BTU (typical) | Burn rate | Full 20 lb tank* | 2.5 hr cook uses |
|---|---|---|---|---|
| Portable/tabletop (1 burner) | 8,000-12,000 | 0.37-0.56 lb/hr | 36-54 hr | 0.9-1.4 lb |
| 2-burner, one side lit | ~12,000 | 0.56 lb/hr | 36 hr | 1.4 lb |
| 2-burner both lit | 24,000-30,000 | 1.11-1.39 lb/hr | 14-18 hr | 2.8-3.5 lb |
| **3-burner all lit (default)** | **36,000** | **1.67 lb/hr** | **12 hr** | **4.2 lb** |
| 4-burner all lit | 40,000-48,000 | 1.85-2.22 lb/hr | 9-11 hr | 4.6-5.6 lb |
| 6-burner + rear, everything on | 60,000-72,000 | 2.78-3.33 lb/hr | 6-7.2 hr | 7.0-8.3 lb |
| Dedicated side burner | 10,000-12,000 | +0.46-0.56 lb/hr | — | +1.2-1.4 lb |

\* to empty; the planning number is to the 20% reserve (see §4).

Reading the table: a "typical" 2.5-hr mixed cook on a 3-burner costs
~4.2 lb — roughly a fifth of a tank. Most people's intuition (and the
"30 cookouts per tank" marketing) assumes 1-burner usage.

## 3. Weight-Based Remaining Fuel — the 424 g/lb Trap

Propane tanks have no usable fuel gauge; the only honest measurement is
mass. Put the tank on a bathroom/kitchen scale (±0.2 lb is fine):

```
fuel (lb) = scale reading − tare (TW stamped on collar)
```

- **Tare ("TW")** is the empty cylinder weight: ~17 lb for steel 20 lb
  tanks (16.6-18.0 range), ~13-14 lb for the newer aluminum ones. Read
  YOUR collar, don't assume 17.
- **Units:** 1 lb = **453.6 g**. The number **424** that floats around
  forums is *pounds per gallon garbled into grams* — liquid propane
  weighs **4.24 lb per US gallon** (0.51 kg/L at 60 °F). If a chart
  tells you a pound of propane is 424 g, it is off by 7%; the correct
  chain is: 20 lb fill ≈ 4.7 gal ≈ 9,070 g ≈ 432,000 BTU.
- Scale reading of a full tank: 17 + 20 = **37 lb** (±1 lb for fill
  variance). "Empty" at the reserve floor reads ~21 lb. A 15 lb
  exchange tank reads ~32 lb full — weigh after an exchange before
  believing it's "full".
- Bathroom scales drift: weigh yourself holding the tank and subtract,
  or better, zero the scale with a board on it. ±0.5 lb error is ±15
  minutes of cook time at 36,000 BTU — not a crisis, know your scale.

## 4. The Cook-Session Consumption Model

A cook is not `hours × max BTU`. Three corrections:

```
session fuel = (preheat_min/60 + cook_hr × duty) × burn_rate
```

- **Preheat:** 10-15 min at full output = 0.17-0.25 hr of max burn
  (~0.4 lb on a 3-burner). Trivial per cook, 8 lb/yr at 2 cooks/week —
  not trivial.
- **Duty cycle:** manual grills with lid-down cooking cycle burners on
  thermostatic control or your hand: use `--duty 0.6-0.7`. Manual
  grills left on full: `--duty 1.0`. Searing everything hot-and-fast
  is the 1.0 case; low-and-slow ribs at 250 °F is ~0.4-0.5.
- **The 20% reserve floor:** never plan past 16 lb of a 20 lb fill.
  Pressure drops as the tank empties (output falls off a cliff below
  ~20% at high draw), cold weather makes it worse, and a flameout
  mid-roast with guests standing there is the exact failure this skill
  exists to prevent. All `hours remaining` figures here are to the
  reserve, not to fumes.

Sanity anchor: 2 cooks/week × 2.5 hr × 1.67 lb/hr + preheats ≈
**9.2 lb/week ≈ 2 tanks/month** on a 3-burner run wide open — or one
tank per ~2 months at realistic medium-knob duty.

## 5. Exchange vs Refill Economics

| | Cage exchange (big-box, ~$26) | Refill (hardware store, ~$19) |
|---|---|---|
| Propane you get | **15 lb** (industry standard for exchanges) | **20 lb** by weight |
| $/lb propane | ~$1.73 | ~$0.95 |
| Your leftover fuel | **surrendered** — swap at 3 lb left, you gift them 3 lb | stays in your tank |
| Tank age/recert (12-yr stamp, 5-yr requal) | their problem — they take old tanks | your problem |
| Availability | 24/7 in parking lots | store hours |
| Line/wait | none | 5-10 min |

Break-even is instant: refill is ~45% cheaper per pound **and** you
keep your leftover propane. Exchange only wins when (a) the tank is
dead/out of recertification and you want to hand the problem to someone
else, or (b) it's Sunday night and the refill counter is closed.

Annual math at 9.2 lb/week (~480 lb/yr, 3-burner, 2.5 hr × 2/wk):
refill ≈ 26 fills × $19 ≈ **$494**/yr vs exchange ≈ 37 swaps × $26 ≈
**$962**/yr — the habit is worth ~$470/yr. Run `compare` with your own
local prices; exchange prices range $18-35 by region.

Note the trap in both directions: swapping early wastes your remaining
fuel to the exchange company; running to actual fumes risks a mid-cook
flameout. Swap/refill at the 20% floor — that's what the reserve is
for.

## 6. Safety — the Non-Negotiables

These aren't disclaimers, they're the failure modes that burn houses
down. Every one is a real incident pattern:

- **5-10 ft clearance, always outdoors.** Grill at least **5 ft (1.5 m)
  from the house** — siding, eaves, and railings included — and never
  under an awning or in a garage, even "with the door open." 10 ft from
  anything overhanging. Carbon monoxide + grease fires + structure
  = the classic grill-fire loss.
- **Never store or swap tanks indoors.** Spare cylinders live outside,
  away from the house entry, upright, on a firm surface. Not in the
  garage, not in the basement, not in the shed with the mower gas.
  Propane is heavier than air; a leaking tank indoors pools at floor
  level and finds the water heater's pilot light.
- **Leak check: soapy water, never a flame.** New hookup, new hose, or
  after any tank swap: spray connections with dish-soap-and-water (or
  leak detector fluid). **Bubbles = leak** — shut the valve, reseat the
  fitting, retest. A lighter is not a diagnostic; that's how eyebrows
  and garages are lost.
- **Transport upright, valve closed, windows open.** A tank lying down
  in a hot trunk vents liquid propane through the relief valve. Secure
  it upright; never leave it in a parked hot car.
- **OPD valves (post-1998 US)** — the triangular handwheel — shut flow
  at 80% fill. If your tank has the old round valve it can't be legally
  refilled; exchange it and modernize.
- **Recertification:** the manufacture date is stamped on the collar;
  certification is good **12 years**, then 5 years per requalification.
  Refillers check; exchanges take anything.
- **If you smell gas at the grill:** close the tank valve, extinguish
  everything, soapy-water every connection, fix before re-lighting. A
  hose that's been on the grill 5+ years is the usual suspect — they
  crack; replacements are $15 and 10 minutes.
- **Frost on the tank** during a long high-draw cook is normal physics
  (vaporization chilling the liquid); frost WITH sputtering burners
  means you're drawing faster than the tank can vaporize — usually an
  overfilled or very cold tank, sometimes a sign you're near empty.
