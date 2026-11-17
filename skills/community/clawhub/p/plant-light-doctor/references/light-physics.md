# The Light Physics Behind plant-light-doctor

This document explains the actual model used by `plant_light_analyzer.py`,
with worked examples and field measurement methods.

## 1. Why DLI?

Photosynthesis is driven by the number of photons in the 400-700 nm band
(PAR, photosynthetically active radiation) landing on leaf area per day.
That count is the **Daily Light Integral**:

```
DLI (mol·m⁻²·day⁻¹) = PPFD (µmol·m⁻²·s⁻¹) × 3600 × hours / 1,000,000
```

Rule-of-thumb conversions:
- Full summer sun at noon: ~2000 µmol/m²/s → outdoor summer DLI 40-60
- Bright windowsill in direct sun: 800-2000 µmol/m²/s
- "Bright indirect" spot: 100-400 µmol/m²/s
- Typical office: 20-80 µmol/m²/s (DLI < 1 — almost nothing edible survives)
- Shade-tolerant foliage floor: DLI 1.5-4

Commercial greenhouse literature (Ohio State CEA program, Purdue HO-** series)
is the source of the plant DLI ranges in `plant-dli-table.md`.

## 2. The model, step by step

### 2.1 Solar declination and day length

For day-of-year N:

```
δ = 23.44° × sin(360° × (284 + N) / 365)
```

Day length at latitude φ (degrees):

```
cos(H₀) = -tan(φ) × tan(δ)        (H₀ = half the daylight arc in degrees)
daylen = 2 × H₀ / 15              (hours)
```

The script evaluates the 15th of each month.

### 2.2 Clear-sky PPFD

Solar elevation α at solar noon:

```
α = 90° - |φ - δ|
```

Atmospheric attenuation is modeled per Bouguer-Lambert with air mass
AM ≈ 1 / sin(α). Direct normal PPFD under clear sky:

```
PPFD_direct ≈ P₀ × 0.7^(AM^0.678)   with P₀ ≈ 2550 µmol/m²/s
```

Diffuse sky PPFD ≈ 8-12% of direct, more at low sun. Global horizontal
PPFD = direct × sin(α) + diffuse.

### 2.3 Vertical window capture

A vertical surface catches direct beam best when sun azimuth opposes the
wall normal. Integrated over a day, in mid-latitudes:

- **Equator-facing wall (S in N-hemisphere):** near-max capture; sun is in the
  southern half of the sky all day. Winter advantage: low sun angle ≈ near
  perpendicular incidence → December capture can rival June.
- **E/W walls:** sun spends roughly half its arc on each side; capture ≈ 45-55%
  of equator-facing, concentrated in morning/afternoon.
- **Pole-facing wall (N in N-hemisphere):** direct sun only in summer at high
  sun (when sun rises NE/sets NW); otherwise diffuse only ≈ 10-15% of S total.

The script encodes monthly capture coefficients per orientation, interpolated
by |latitude|.

### 2.4 Correction factors (all multiplicative)

| Factor | Range | Notes |
|---|---|---|
| Floor penalty | 0.75-1.0 | Ground floor + opposite building loses sky view; light wells worst |
| Obstruction | 1 - blockage | Fraction of sun hours blocked by buildings/trees (user input) |
| Glass transmission | 0.65-0.90 | Single ~0.90, double ~0.85, low-E ~0.75, tinted ~0.65 |
| Overhang shading | 0.55-1.0 | Deep eaves/balconies kill high summer sun, keep low winter sun |
| Climate | 0.55-1.05 | `cloudy` (oceanic), `temperate`, `sunny` (continental/Mediterranean) |
| Distance into room | 0.3-1.0 | Light falls ~hyperbolically from the glass; analyze AT the plant |

### 2.5 Hemisphere flip

All orientation tables are written for the northern hemisphere; for negative
latitude the script swaps S↔N (and biases E↔W morning/afternoon, which is
cosmetic). Sydney north-facing = Hamburg south-facing in character, but with
reversed seasons — December DLI is the SUMMER minimum there. The worst-month
logic picks the true seasonal minimum automatically.

## 3. Worked example

Berlin (52.5°N), south window, 2nd floor, clear view, double glass, temperate.

December: daylen ≈ 7.7 h, noon elevation ≈ 14.2°. Clear-sky direct ≈
2550 × 0.7^(1/sin(14.2°))^0.678 ≈ 720 µmol/m²/s. S-wall December capture
coefficient is high (low sun) ≈ 0.55 of daily global → effective average PPFD
over 7.7 h ≈ 175 µmol/m²/s inside glass (×0.85) → DLI ≈ 175 × 3600 × 7.7 / 1e6
× 0.85 ≈ **4.1 mol** — enough for pothos and sansevieria, marginal for herbs.

June: daylen ≈ 16.8 h, noon elevation ≈ 61°. Direct ≈ 1800 µmol/m²/s; S-wall
capture lower (high sun) ≈ 0.35 → average ≈ 260 µmol/m²/s → DLI ≈ **13-15 mol**
— herbs and lettuce thrive for ~4 months.

Verdict for basil (needs 10-14): SURVIVES summer, STRUGGLES winter → the script
recommends a 15-20 W bar, 12 h/day, November-February.

## 4. Measuring instead of modeling

The model is ±30%. For precision, measure:

1. **Phone lux meter** (any free app) at the plant position at solar noon on a
   sunny day. Convert: PPFD ≈ lux / 54 (sun), lux / 35 (cool white LED),
   lux / 70 (warm white). Rough but far better than nothing.
2. **Paper test:** at plant position at noon, hold a book. Shadow with sharp
   edges = direct sun (>1000 µmol/m²/s); fuzzy but readable-print shadow =
   bright indirect (200-500); no shadow you can see = low light (<100).
3. **Log 3 days** if possible: DLI estimates from 5-6 samples across the day
   (9:00, 11:00, 13:00, 15:00, 17:00) beat a single noon reading.

## 5. Grow-light engineering

Given target DLI need and worst-month natural DLI:

```
gap = need - worst_month_DLI
required_PPFD = gap × 1e6 / (3600 × photoperiod_hours)
```

Example: herbs need 12, window gives 4 → gap 8 mol. At 14 h photoperiod:
8e6 / (3600 × 14) ≈ 159 µmol/m²/s → a typical 2 ft, 20 W full-spectrum bar
delivers ~200-300 µmol/m²/s at 25-30 cm. That fixture closes the gap.

Efficacy reference (µmol/J, "efficiency" of turning watts into photons):
- Cheap white LED strips: 1.2-1.6
- Quality quantum boards (Samsung LM301): 2.5-2.8
- Best horticulture LEDs (2024+): 3.0-3.7

Watts needed = PPFD × area / efficacy. For a 0.6 × 0.2 m shelf: 159 × 0.12 / 2.3
≈ 8 W of quality board, or ~20 W of cheap strip (they lose the difference as heat).

Photoperiod rules: most foliage plants 12-14 h; never run 24/0 (plants need
the dark phase for respiration + some need it to bloom); use a $10 mechanical
timer — photoperiod consistency matters more than intensity.

## 6. Limits and honesty

- No interior reflection modeling (white walls help, plants near mirrors help).
- Curtains, screens, dirty glass: assume another 10-30% loss if present.
- Heat: S windows in summer can cook plants regardless of light; DLI is not
  the only axis of care.
- The plant DLI ranges assume otherwise-good care (water, roots, humidity).
