# Lawn Care Science — Reference

## Crabgrass germination biology

- **Gate:** 4 consecutive days with 2-inch soil temp ≥55°F (13°C). Full germination flush
  at 60-70°F soil. Light can start it earlier at thin/bare spots (soil surface warmer).
- **Soil temp estimation model (used by the script):**
  `soil_T ≈ 0.7 × (mean air T over last 10 days) + 0.3 × (mean air T over days 11-30) − 1.5°F`
  Sunny bare soil runs +5°F over turf-covered soil; mulched beds −3°F. A real thermometer
  at 9-11 AM beats any model — recommend it once, use the model as the tracker.
- **Pre-emergent chemistry table:**

| Active | Typical rate (ai/1000 ft²) | Window | Notes |
|---|---|---|---|
| prodiamine 65WG | 0.37-0.65 oz | 3-5 mo residual | the long pre-season standard |
| dithiopyr 40WSB | 0.25-0.5 oz | early post up to 1-tiller | only one with early POST activity |
| pendimethalin 60DG | 1.0-1.5 oz | 3-4 mo | yellow stain, cheap |
| siduron (Tupersan) | label | seed-safe | ONLY one safe over new seed |
| indaziflam | low oz | 6 mo | pros; very long residual — no seeding that year |

- **Activation:** 0.5" water within ~2-3 days or UV degrades surface granules.
- **Round 2** at 8-10 weeks (prodiamine split: 0.37 + 0.37) holds the wall into summer.

## Grass types and calendars

**Cool-season (tall fescue, KBG, perennial rye):** growth peaks 60-75°F; summer dormancy.
- N schedule: Sep 1.0, Oct 1.0, Nov 0.75 (winterizer while green) = 2/3 of annual;
  spring only 0.5 (May) if at all. Annual total 2-3 lb N/1000 (fescue low end, KBG high).
- Seeding: late Aug-mid Sep (soil 60-75°F falling, weed pressure falling). Spring seeding
  = crabgrass food unless siduron.
- Aeration: fall (core), spring only if soil is compacted and pre-emergent plans allow
  (aeration after pre-emergent breaks the barrier).

**Warm-season (bermuda, zoysia, St. Augustine, centipede):** green-up at soil 65°F.
- NOTHING before green-up. N May-Aug 0.5-1.0/mo (bermuda), zoysia/centipede 1/4 of that.
- Pre-emergent: soil 50-55°F in spring (same gate) + again early fall for winter weeds
  (annual bluegrass/Poa: soil 70°F FALLING, ~when nights hit 60s).
- Centipede hates phosphorus + high N; "centipede decline" is usually over-fertilization.

**Transition zone:** both types stressed; tall fescue is the default survivor. Expect the
spring gate mid-Feb (Atlanta/Dallas) to mid-April (Kansas/Mid-Atlantic).

## Fertilizer math details

```
bag N lb = bag_lbs × N% ; e.g. 50 lb × 0.20 = 10 lb N
product lb needed = area/1000 × n_rate ÷ N%
cost per lb N = price ÷ bag N lb          ← the only fair price comparison
PPF (P) and potash (K) same arithmetic with P₂O₅%/K₂O%
```
- 1 lb N/1000 ft² is the standard "round" for soluble; 0.5 for summer-stressed cool turf.
- Slow-release (coated urea, methylene urea, natural organics) fraction on the label:
  ≥30-40% SR allows 1.25-1.5 lb N/1000 in one pass and longer intervals.
- Iron (Fe) greening without growth: 0.1-0.2 oz Fe/1000 as chelate or ferrous sulfate —
  the "no-mow-growth green" trick; safe in summer.
- pH first: at pH <6.0 or >7.2 nutrient uptake collapses regardless of N — lime/sulfur
  per soil test, not guesswork.

## Spreader calibration (10 minutes, saves 30% product)

1. Weigh out exactly 5 lb of product into the spreader.
2. Spread over a measured 500 ft² (e.g. 10×50 ft) at your intended setting, walking your
   normal pace.
3. Weigh what's left. Applied lb/1000 = (5 − leftover) × 2.
4. Adjust setting until applied = intended lb/1000. Write the setting on the bag.

## Burn triage (yellow stripes / brown patches after feeding)

- **Stripes = overlap burn** (double-dosed lines): water deeply 0.5" daily for a week;
  recovery 2-3 weeks if crown alive.
- **Uniform scorch + dose >1.5 lb N/1000 soluble:** flood-irrigate 1" immediately, then
  0.5" daily ×3 days. Do NOT fertilize again for 4 weeks.
- **Granules sitting on leaves in heat:** sweep/blow off before watering in.
- **Dog spots (urea + salts, ring shape):** flush 1" water; seed dead centers in fall.

## Herbicide classes quick map

- Pre-emergent: prodiamine/dithiopyr/pendimethalin/siduron/indaziflam (table above)
- Post-emergent crabgrass: quinclorac (1-3 tiller), fenoxaprop (maturing), mesotrione
  (younger, cooler), topramezone — tank-mix rotation delays resistance
- Broadleaf (dandelion/clover/oxalis): 2,4-D + dicamba + MCPP/MCPA 3-ways; clover needs
  the dicamba component; apply fall > spring (into the root = translocation)
- NEVER aerate/verticut right after pre-emergent (breaks the chemical barrier)
- Grass killers near fescue: fenoxaprop/fluazifop will kill cool turf too — mesotrione
  (Tenacity) is the selective exception, primes new seedings
- Temperature windows: broadleaf sprays 50-85°F, actively growing weeds, no rain 6-24 h

## Annual N budgets by grass (lb N/1000/yr)

| Grass | Annual | Pattern |
|---|---|---|
| Tall fescue | 2-3 | fall-weighted |
| Kentucky bluegrass | 3-4 | fall-weighted, higher summer disease watch |
| Perennial rye | 2-3 | fall-weighted |
| Bermuda | 3-5 + | summer monthly |
| Zoysia | 1-2 | summer, light |
| St. Augustine | 2-3 | summer |
| Centipede | 0.5-1 | minimal; P-sensitive |

## Soil tests

Extension-service test ($10-20) every 2-3 years: pH, P, K, Ca, Mg, CEC, organic matter.
The skill's math assumes pH 6.0-7.0 and adequate P/K — if the test says otherwise, fix
that FIRST (lime takes 6-12 months to work).
