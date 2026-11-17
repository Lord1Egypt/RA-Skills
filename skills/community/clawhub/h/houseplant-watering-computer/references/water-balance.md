# Water Balance Physics — Reference

## The model in one paragraph

A potted plant lives inside a reservoir: the water its substrate holds after
a watering, minus what drains away. It consumes that reservoir at a rate set
by its leaf area, the light driving photosynthesis, and the dryness of the
air (VPD). Watering = refilling the reservoir after it's drawn down to a
safe floor. Every "how often should I water" question is really "how big is
the reservoir and how fast does it drain" — both computable.

## Substrate water-holding capacity (WHC)

Water a saturated, drained substrate holds, per liter of substrate:

| Substrate | WHC (mL/L) | Usable fraction | Notes |
|---|---|---|---|
| Peat/coir potting mix | 450–550 | ~0.60 | The default; holds well, drains OK |
| Garden soil in pot | 600+ | ~0.45 | Compacts, hypoxic — never use |
| 50/50 peat+perlite | 380–430 | ~0.62 | Faster cycling, more air |
| Cactus/succulent mix | 250–320 | ~0.65 | Mineral, fast dry |
| Chunky aroid/bark | 180–250 | ~0.70 | Air-first, frequent watering |
| LECA (semi-hydro) | 300–400 | ~0.55 | Capillary-fed from reservoir |

"Usable fraction" accounts for water held below the plant's extraction
tension (unavailable at permanent wilting point) and the safety floor you
shouldn't dip below. Denser mixes hold more total water but make less of it
available while simultaneously restricting oxygen — the classic trap.

## Pot geometry

Nursery pots are tapered (truncated cones), not cylinders:

    V = π·h/3 · (R² + R·r + r²)

with R = top radius, r = bottom radius. A "24 cm" tapered pot 22 cm tall
holds ~6.5 L gross, ~5.5 L of substrate after root mass and rim space —
nearly 2× a same-diameter short pot. This is why "same plant, same size
pot" can halve or double the watering interval.

Substrate volume scales the reservoir linearly but plant demand scales
sub-linearly (leaf area grows slower than pot volume), so bigger pots dry
slower per liter — big pots are more forgiving, and easier to overwater.

## Plant demand classes

Baseline transpiration (mL/day per L substrate, at bright-indirect,
22 °C, 45% RH, growing season):

- Cactus 7, succulent 10, small foliage 22, medium foliage 38,
  large foliage 60, fern 55, flowering-in-bloom 65.

These are honest orders of magnitude, not precision instruments — they
anchor the interval so your finger test has a prior instead of a guess.

## Light multiplier

Light drives photosynthesis and stomatal opening:

| Light | Multiplier |
|---|---|
| Low (north window/deep room) | 0.55 |
| Medium indirect | 0.8 |
| Bright indirect (baseline) | 1.0 |
| Some direct (E/W window) | 1.35 |
| Full sun (S window/outdoors) | 1.8 |

## VPD — the honest environmental driver

Vapor pressure deficit (kPa) = how much more water the air could hold at
current temperature vs what it holds now (Tetens equation):

    es = 0.6108 · e^(17.27T / (T+237.3));  VPD = es · (1 − RH/100)

Transpiration tracks VPD almost linearly in the normal range. Same plant:
18 °C/70% → 0.62 kPa (×0.7 demand), 22 °C/45% → 1.45 kPa (×1.0),
26 °C/30% → 2.35 kPa (×1.35).

Winter heating creates the lethal combo: warm dry air (transpiration
continues) + cold wet root zone (uptake slows, roots suffocate). This, not
the calendar, is why winter watering shrinks.

## Season multiplier

Summer 1.15, spring 1.0, fall 0.85, winter 0.6 (photoperiod + growth rate,
on top of the VPD effect already counted from your actual temp/RH inputs).

## Dose: how MUCH to apply

Refill to saturation, which means applying ~20–25% of substrate volume
(some runs through, flushing salts — this is desirable every watering;
"water sparingly" accumulates salts in the root zone). 1.4 L for a 6.5 L
monstera pot, 150 mL for a small succulent pot.

## Why drainage holes don't fix overwatering

Holes act at saturation: excess leaves, and the pot returns to field
capacity. But if you re-water at field capacity every two days, the
substrate never enters the aerated zone and roots suffocate regardless of
holes. Frequency is the variable; holes are plumbing.

## Self-watering / wick engineering

- Wicks (cotton rope 6–10 mm) bridge substrate to an external reservoir;
  capillary delivery roughly self-regulates with demand.
- Rate depends on wick diameter, length, height differential (reservoir
  below pot rim reduces flow), and substrate wettability.
- Always burn-in test a week before a trip; wick systems fail by
  over-delivering to thirsty mixes, not under-delivering.
- Species gate: rot-prone plants (succulents, cacti, sansevieria,
  ZZ) shouldn't be wicked — they tolerate drought better than saturation.

## Moisture-sensing truth table

| Method | What it actually tells you |
|---|---|
| Finger 2–4 cm | The zone where most fine roots live — good default |
| Bamboo skewer to bottom | The full profile incl. perched water — best DIY |
| Pot weight (heft) | Integrated total moisture — fastest, needs calibration |
| Cheap resistance meter | Ballpark, drifts with salts — calibrate against finger |
| No monitoring at all | How most houseplants die |
