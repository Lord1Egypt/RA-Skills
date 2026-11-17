# Condensation Physics & Moisture Handbook

## 1. Surface temperature of a glazing
Heat flow through a window (1 m²) in steady state:
```
T_in --R_i--> [pane stack] --R_o--> T_out
R_i ≈ 0.13 m²K/W  (indoor film, still air)
R_o ≈ 0.04 m²K/W  (outdoor film, windy)
R_glazing = 1/U − R_i − R_o
```
Inner surface temperature:
```
T_s = T_in − (T_in − T_out) · R_i / (R_i + R_glazing + R_o)
```
Typical U (whole window W/m²K): single 5.0–5.9; double clear 2.8; double
low-e 1.4–1.8; triple low-e 0.8–1.1. Frame U runs higher than center-of-
glass for aluminum without thermal break — frames fog FIRST.

Numerical feel (T_in=21, T_out=−10):
- single (U=5.8): T_s ≈ 21 − 31·(0.13/0.1725) ≈ −2.3 °C (freezes)
- double clear (U=2.9): T_s ≈ 3.0 °C
- double low-e (U=1.6): T_s ≈ 8.3 °C
- triple (U=0.9): T_s ≈ 12.1 °C
That 14 °C spread between single and triple is the entire story of "some
windows fog and others don't".

### Curtain cavity effect
A closed curtain blocks room air from washing the pane; the trapped air
layer adds ~0.15 m²K/W on the ROOM side, shifting a chunk of the drop onto
the glass: T_s falls another 3–6 °C. Result: fog exactly behind curtains,
where frames stay wet longest. Fix: gap at top+bottom (chimney wash), or
open curtains on cold nights, or accept and squeegee daily.

### Bay/bow and corner windows
Geometry that reduces airflow (bay recess) + sometimes reduced frame
insulation → coldest glass in the house. Often threshold 5–10 RH points
below flat windows of the same glazing. Add a margin for them.

## 2. Dew point and threshold RH
Magnus (over water, ±0.35 °C to 0–60 °C):
```
γ = ln(RH/100) + 17.62·T/(243.12+T);   Tdp = 243.12·γ/(17.62−γ)
```
Inverse at surface temp T_s gives threshold RH* — the humidity at which dew
point equals pane temperature. House stays dry iff RH < RH*(coldest window)
with ~5 RH points margin for night dip (glass coldest 4–7 am).

Threshold curves by outdoor temp (T_in = 21 °C, center-of-glass, computed
by `scripts/windowfog.py` with the same resistance chain):

| T_out | single | double clear | double low-e | triple |
|---|---|---|---|---|
| 0 °C | 38% | 61% | 76% | 86% |
| −5 | 30% | 54% | 71% | 83% |
| −10 | 23% | 47% | 67% | 80% |
| −15 | 18% | 42% | 62% | 77% |
| −20 | 14% | 36% | 58% | 74% |

Pane surface temps at T_in 21 / T_out −10: single −0.8 °C, double 9.3 °C,
double low-e 14.6 °C, triple 17.4 °C. (Exact values from the script; the
table gives the shape: single glazing basically cannot carry "healthy"
winter humidity; triple can.)

## 3. Moisture sources (audit table)
| Source | Typical water emission |
|---|---|
| Shower (10 min) | 100–250 g |
| Cooking (family dinner, gas) | 300–1000 g |
| 2 people sleeping (respiration/perspiration) | 40–80 g/h ≈ 400–600 g/night |
| Drying laundry indoors (one load) | 1500–3000 g/day (!) |
| Houseplants (per 10 medium pots) | 200–500 g/day |
| Aquarium (per m² surface) | ~200–600 g/day |
| Unflued gas heater | ~1.6 kg water per kg gas — enormous and often the hidden culprit |
| New construction moisture (1st year) | 5–20 kg/day, decaying over months |

## 4. Removal: ventilation math
Air at 21 °C/50% RH holds ~9.2 g/m³ (saturation ~18.3 at 21 °C). Outdoor
air at −5 °C/80% holds ~2.9 g/m³. Heating it to 21 °C gives RH ≈ 16% —
each m³ of exchange absorbs ~6.3 g of water. A 10-minute cross-ventilation
of a 90 m³ apartment exchanges ~60% of air → removes ~350 g water. Winter
ventilation is a one-way pump toward dryness; the skill's fix ladder uses
this (short intense bursts > continuous trickle for source spikes).

## 5. Mold risk framing
- Liquid water on organic substrates (frame wood, drywall paper, seals)
  above ~0 °C: germination in 24–48 h at RH≈surface 100%; visible colonies
  in days–weeks. Corner-of-frame black speckling IS this.
- Below 0 °C pane: frost deposits (deposition), no liquid → low direct
  mold risk, but morning thaw refills the same corner nightly.
- Established area > 1 m² on drywall or inside wall cavity = professional
  remediation territory; occupant-level fixes stop at surfaces.

## 6. Fix ladder (cost order)
1. **Free — behavior**: kitchen/bathroom door closed + 10-min burst
   ventilation after source events; bedroom burst on waking; laundry OUT of
   the living space (biggest single lever, 1.5–3 kg/day); kill unflued gas
   heating.
2. **Free — air washing**: curtains gapped 2–3 cm top and bottom; don't
   push furniture against exterior walls under windows; keep interior
   doors open by day for circulation.
3. **Cheap — hardware**: trickle vents on the coldest windows; magnetic
   secondary pane / interior storm film (moves you one glazing class for
   ~1/20 the cost of replacement: film lifts single→~double threshold).
4. **Capital**: low-e double/triple replacement; warm-edge spacers;
   HRV/ERV for tight houses (recovers heat while continuously pumping
   moisture out — the systematic fix for modern-build bedrooms).

## 7. Comfort floor honesty
Below ~30–35% RH: dry eyes/throat, static, some asthma aggravation. If your
threshold RH (coldest window −5 margin) sits under that, the answer is NOT
"dry out further" — it's glazing-side (ladder rung 3–4). The script's
verdict says which side of the line you're on.
