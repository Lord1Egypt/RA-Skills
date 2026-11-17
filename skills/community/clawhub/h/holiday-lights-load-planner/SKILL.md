---
name: holiday-lights-load-planner
description: Use when hanging holiday or party string lights (incandescent mini, LED, C9, rope, projector) — computes per-circuit amp/watt load against the 80% breaker rule, daisy-chain limit warnings before the middle-of-the-night trip, timer/photocell rating checks, extension-cord gauge vs run length, and outdoor GFCI/wet-location rules, turning a guesswork tangle into a load sheet your panel won't argue with.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [holidays, christmas-lights, electrical-load, circuit-capacity, safety, diy]
---

# Holiday Lights Load Planner

## Overview

Every December the same two failures: a breaker trips at 6 PM with 40 guests
arriving at 7, or an extension cord under a rug slowly cooks itself. Both are
arithmetic, not bad luck: a 15 A circuit at the 80% rule gives you 1,440 W of
honest headroom, and one 300-bulb incandescent mini string eats 100+ W. A
deck rail of twenty strings is a space heater wearing tinsel. `scripts/lights_load.py`
turns the pile of boxes into a per-circuit load sheet: amps, watts, 80% margin,
daisy-chain warnings based on how many strings the fused plug actually allows,
cord gauge vs run length, and outdoor GFCI verdicts — before anything is hung.

## When to Use

- Planning the annual outdoor display: rooflines, bushes, inflatables, projector.
- Indoor tree + windows + mantel on one crowded outlet strip.
- Breaker trips when lights go up, or plugs/walls warm near decorations.
- Buying lights: deciding LED vs incandescent from real energy + capacity math.
- Any party/event lighting plan (patio string lights, market lights, weddings).

**Don't use for:** permanent landscape lighting design (NEC low-voltage rules,
continuous-load derating differences) or generator/inverter sizing — those need
their own load models. This skill is seasonal/portable decorative loads.

## How It Works

1. **Circuit budget.** US residential: 15 A → 1,800 W nameplate, 1,440 W at
   the 80% continuous rule; 20 A → 2,400/1,920 W. The script takes breaker
   size and existing always-on load on that circuit (fridge? TV wall?), then
   shows remaining headroom.
2. **Per-type wattage table.** Incandescent minis ~0.4–0.5 W/bulb, C7/C9
   incandescent 5–7 W/bulb, LED everything 0.05–0.1 W/bulb, rope light
   ~5.5 W/m (incandescent) / ~2 W/m (LED), inflatables 50–150 W blowers,
   projectors 30–100 W. Enter what's in the boxes; the script sums it.
3. **String count.** Strings → amps → watts on the chosen circuit, with the
   80% verdict, remaining margin in watts and strings-of-type, and a trip
   risk verdict.
4. **Daisy-chain limit.** Incandescent mini strings: fuse-limited, typically
   max 3–5 strings end-to-end (read the box); LED: often 20+ but wall-wart
   ratings bind first. Script flags when your plan exceeds the box limit.
5. **Extension cords.** Gauge vs run length vs load: #16 ≤ 25 ft light duty,
   #14 ≤ 50 ft, #12 for 100 ft or any outdoor run; always rated-W compliant,
   never coiled under anything flammable, outdoor-rated (W) jacket only.
6. **Outdoor rules.** GFCI-protected outlet or GFCI cord adapter, wet-location
   rated (UL 2238/WW) lights, plugs kept off the ground in covers, timers
   rated for the full load (a 15 A photocell timer carrying 12 A is fine; a
   5 A one carrying 8 A is a melting part).
7. **Timer/photocell rating check.** Sum amps through the timer; flag if the
   timer's rated amps < load.
8. **Schedule math.** 6 h/night × rate → season cost, and the LED payback
   line: "swapping these 12 incandescent strings for LED saves X W = room
   for Y more strings, $Z/season."

## Using the Script

```
# full plan: 15A circuit, 100W existing, 12 incandescent mini strings (100-bulb),
# 3 LED strings, 1 inflatable, 80 ft #14 cord, outdoor, timer rated 15A
python3 scripts/lights_load.py --breaker 15 --existing-watts 100 \
  --strings incandescent-mini:100:12 led-mini:70:3 --inflatables 1 \
  --cord-gauge 14 --cord-length-ft 80 --outdoor --timer-amps 15

# just compare: what does going LED save on the roofline?
python3 scripts/lights_load.py --breaker 15 --strings incandescent-mini:100:24 --compare-led
```

Outputs: per-type watt/amp subtotals, circuit total vs 1,440 W budget, margin,
verdict (SAFE / TIGHT / OVERLOAD), daisy-chain warning if strings-per-run
exceeds box limit, cord verdict, GFCI verdict if outdoor, timer verdict, and
season cost with LED-payback math.

## Common Pitfalls

1. **Counting nameplate circuit watts (1,800) as the budget.** Continuous
   multi-hour holiday loads get the 80% rule: 1,440 W on 15 A. Planning to
   1,800 is planning to nuisance-trip.
2. **Assuming "all lights on one plug" is fine because it works.** It works
   until the circuit's other residents (fridge compressor kicking in at 20%
   margin) show up. Always reserve existing load.
3. **Daisy-chaining by feel.** The fused plug on incandescent strings is the
   limit — exceed it and the fuse blows mid-season (best case) or the thin
   cord between strings carries the whole run's current (worst case).
4. **Indoor cords outdoors.** Indoor cords crack in cold, absorb water at the
   plug. Outdoor-rated jacket and an elevated, covered plug connection only.
5. **Timer as afterthought.** A $10 mechanical timer rated 10 A carrying a
   1,400 W display is the hidden failure point. Rate the timer like a cord.
6. **Forgetting inflatables are motors.** Each blower is 50–150 W continuous
   and looks like nothing on the box. Six inflatables = half a mini-string
   roofline of constant draw.
7. **LED conversion math done on bulb counts.** Two hundred LED bulbs draw
   less than twenty incandescent ones. Compare watts, not bulbs.

## Verification Checklist

- [ ] Breaker amps and existing circuit load captured before string math.
- [ ] Every string type entered with bulb count and quantity.
- [ ] Verdict is SAFE/TIGHT with ≥ 10% margin; anything OVERLOAD re-planned.
- [ ] Daisy-chain count per run ≤ box limit (incandescent especially).
- [ ] Outdoor runs: GFCI source, wet-location lights, elevated plugs.
- [ ] Cord gauge ≥ requirement for run length and load; no coiled cords.
- [ ] Timer/photocell rated ≥ total amps passing through it.
- [ ] After hanging: 15-min warm check — plugs and cords cool to touch.
