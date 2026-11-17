# Drying Physics Handbook

## 1. Water budget: how wet is "wet"?
Laundry comes out of the washer at residual moisture RM = (wet − dry)/dry:

| Spin rpm | RM cottons | Water in a 4 kg dry load |
|---|---|---|
| 800 | ~70% | 2.8 kg |
| 1000 | ~62% | 2.5 kg |
| 1200 | ~55% | 2.2 kg |
| 1400 | ~50% | 2.0 kg |
| 1600 | ~45% | 1.8 kg |

Spin speed is the cheapest drying lever: 800→1400 removes 0.8 kg of water
using ~2 extra minutes of the washer's spin (≈30 Wh), which would take a
tumble dryer ~0.8 kWh and a rack hours of evaporation. Synthetics hold a
few points more than cottons at the same rpm (fabric structure).

## 2. Evaporation rate: the VPD engine
Drying rate ∝ vapor pressure deficit — the gap between how much water the
air COULD hold at its temperature and how much it holds now:

```
e_sat(T) = 0.6108 · exp(17.27·T/(T+237.3))   kPa  (Tetens)
VPD = e_sat(T_air) − RH/100 · e_sat(T_air)  = e_sat(T_air)·(1−RH/100)
E = k_class · VPD      [kg water per hour, per ~4 kg spread load]
```

k_class (empirical planning values, 4 kg cotton load spread on a standard
rack):
- still indoor air: 0.018 kg/h/kPa
- rack + fan or good crossflow: 0.035
- heated airer / radiator-drape: 0.060 (also raises local T → extra VPD)
- dehumidifier in closed room: 0.090 (keeps RH near 40% at the load)
- outdoor, light wind: 0.05; breezy: 0.10; strong sun adds radiation to VPD

Sanity check: room at 20 °C/50% RH → e_sat≈2.34 kPa, VPD≈1.17 kPa →
still air ≈ 0.021 kg/h → a 2 kg-water load takes ~95 h at that naive rate.
Reality: the load's own evaporative cooling and room volume change things;
in practice still-room loads take 12–24 h — because the two-phase model
(below) plus real room air exchange modify the constant. Use the script's
numbers; the classes are calibrated so that: still room 4 kg/1400rpm
20°C/50% lands ≈ 16–20 h, fan ≈ 9–12 h, dehumidifier ≈ 4–6 h — matching
field observations.

## 3. Two-phase drying
1. **Constant-rate phase** (~70% of the water): fabric surface stays wet,
   rate is the full E above.
2. **Falling-rate phase** (last 30%): water must diffuse from fiber
   interiors and seams; effective rate ≈ 0.4×E. This tail is why "dry-ish"
   laundry smells musty by evening: seams hold 10–15% moisture for hours —
   enough for microbial growth if the load sits folded.

Model: t_dry = 0.7·W/E + 0.3·W/(0.4·E) = W/E · (0.7+0.75) = 1.45·W/E.

## 4. Room humidity: where the water goes
Indoor rack drying is a zero-sum transfer: the water becomes room vapor
until ventilation removes it. Steady-state added moisture:

```
added_water_rate(t) = E(t)               (kg/h into the air)
removal = ACH · V · (x_room − x_out)·ρ   (kg/h out; x = humidity ratio kg/kg)
```
RH rise quick-number: one 4 kg load at 1400 rpm ≈ 2.0 kg water. In a
40 m³ flat at 20 °C with 1 ACH, air holds at 60% RH ≈ 0.6 kg total; the
load adds 3+ house-volumes of water over its drying → sustained RH push
toward 70–80% unless ventilated. Windows fog (see threshold table in
humidity-window-fog-doctor); drywall corners risk mold. The script prints
peak RH and flags the condensation chain.

The dehumidifier fixes both problems at once: it IS the ventilation
(moves water to a tank) and adds ~0.3 kWh/kg water of heat to the room —
in winter that's heat you'd partly buy anyway.

## 5. Method cost comparison (per 4 kg load, 2.0 kg water)
Energy to evaporate 2 kg water ≈ 2 × 0.63 kWh(th) = 1.26 kWh thermal.
- **Indoor rack, no help**: 0 kWh purchased (heat comes from your heating;
  in winter ≈ 1.3 kWh of your fuel ≈ 1.3×price_kWh_fuel/η — plus the
  humidity problem).
- **Rack + dehumidifier**: ~0.45–0.6 kWh electric, water goes to the tank,
  room gets the compressor heat back. Usually the winter winner.
- **Heated airer** (e.g., 230 W): ~1.2–1.8 kWh per load.
- **Vented/condenser tumble**: 1.8–2.5+ kWh (condenser dumps the heat AND
  the moisture into the room unless plumbed — worst of both).
- **Heat-pump tumble dryer**: 0.6–0.9 kWh — the appliance benchmark.
Outdoor line in drying weather: 0 kWh, zero indoor moisture.

## 6. Outdoor and freeze-drying
Same VPD engine with outdoor T/RH/wind. Sub-zero: clothes freeze stiff
(fabric water freezes), then sublimate — slower (sublimation pulls ~2.8
kJ/g vs 2.4 evaporation, and ice VP is low) but a sunny windy −5 °C day
completes a load in ~a day. Sunset dew re-wets: bring in before the
evening dew point crosses the fabric temperature. The script flags
re-wet risk when RH_out > 85% in the evening window.

## 7. Musty-load rescue
A slow load that sat damp >12 h: re-wash or run a 60 °C cycle (not just
re-dry) — drying kills surface microbes but the smell compounds (MVOCs)
stay in the fabric. Prevention: spread the load, spin ≥1200, fan, or
dehumidifier — the model's levers.

## 8. Model limits
- Planning-grade (±25%): fabric mix, rack density, and local drafts swing
  real times; the classes bound the common cases.
- Room-interaction modeled as single zone with fixed ACH; adjacent-room
  buffering ignored.
- Tumble dryer times not modeled (appliance specs cover that); only energy.
