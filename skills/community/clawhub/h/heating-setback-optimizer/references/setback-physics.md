# Setback Physics & System Handbook

## 1. The core identity
A heated building at indoor temperature T_in, outdoor T_out, loses heat at

```
Q_loss = K · (T_in − T_out)      [W]   K = overall heat-loss coeff [W/K]
```

Fuel burned over a period = ∫Q_loss dt / η (η = system efficiency or COP).
Setback lowers T_in for some hours → lowers the integral → saves fuel. That
is the entire mechanism. Everything else is corrections:

- **Recovery**: the climb back to setpoint must happen with the system's
  excess capacity; energy spent recovering ≈ mass reheating, and if the
  system uses a less-efficient stage (strips) for it, it's expensive.
- **Solar/internal gains**: they mask part of the loss at lower T_in —
  slightly reduces measured savings; second-order, ignored.
- **Infiltration wind effects**: K itself varies; use seasonal average.

## 2. Degree-hour math for a rectangular setback
For setback depth ΔT over t_s hours per day, heating season D days:

```
Saved_energy_ideal = K · ΔT · t_s · D / η      [Wh]
```
Example: K=220 W/K, ΔT=3 K, t_s=8 h, D=210 d, furnace η=0.9:
220·3·8·210/0.9 = 1.23 MJ... → 1,232,000 Wh? No: 220 W/K·3 K·8 h = 5,280
Wh/day; ×210 d = 1,109 kWh thermal /0.9 = 1,232 kWh fuel ≈ the right order
(~5–8% of a typical 15–20 MWh season). Field studies agree: **~1% per
°C·(8 h)** — the "1% per degree per 8 hours" rule.

## 3. Thermal mass and the recovery ramp
Effective heat capacity C_eff by construction class:
- Light (timber frame, hollow doors, air): ~3 kWh/K (≈10.8 MJ/K)
- Medium (drywall + furnishings + some masonry): ~6 kWh/K
- Heavy (slab-on-grade, stone, brick internal): ~12 kWh/K

House time constant τ = C_eff/K: light 220 W/K → τ≈13.6 h; heavy → τ≈55 h.
Consequences:
- Setback must last a large fraction of τ to realize the ideal savings
  (the mass keeps releasing heat, floating the air temp).
- Recovery ramp from ΔT below setpoint, with system excess capacity
  Q_x = Q_max − K·(T_in−T_out):
  `ramp ≈ C_eff·ΔT / Q_x` hours. Furnaces are 2–3× oversized → ramps are
  fast and cheap. Heat-pump compressors are sized near design load →
  morning recovery at, say, −8 °C outside has little excess capacity.

## 4. System handbook (what the verdict engine applies)

### Furnace / boiler (gas, oil)
- Oversized burners make recovery cheap. Setback freely, 2–6 °C, ≥3 h
  windows. Savings ≈ 0.8–1.2% per °C·8 h.
- Condensing boilers: recovery from deep setback briefly exits condensing
  band — minor penalty, still net positive.

### Heat pump with auxiliary resistive strips
- Compressor-only capacity falls with outdoor temp; a deep morning recovery
  triggers strips (COP≈1 vs compressor 2.5–3.5) and burns the savings.
- Practical rules: cap setback ≈ 1.5–2 °C on cold climates, OR thermostat
  with "smart/adaptive recovery" that starts early enough to recover at
  compressor speed only. Never use "EM heat" positions for recovery.
- Cold-climate (inverter, no strips or locked-out) systems: behave closer
  to furnace; 2–3 °C is fine.

### Radiant floor (hydronic slab)
- Slab τ is huge; deep/short setbacks don't reach the mass and recovery is
  painfully slow (6–12 h). Max setback ≈ 1 °C, or hold constant with
  outdoor-reset control. A classic "setback made my house cold all day".

### Electric baseboard (resistance)
- η=1 (COP 1); setback saves exactly the degree-hours, recovery can't be
  inefficient (already resistance) → setback always pays, any depth.

## 5. Prices & fuels (defaults in script; override with --price)
- Natural gas: ~35–40 MJ/m³; price ~$0.9–1.6/m³ → ~$0.03–0.05/MJ_th
- Oil: 38 MJ/L; ~$1.0–1.6/L
- Resistance electric: 3.6 MJ/kWh at ~$0.10–0.35/kWh
- Heat pump: divide thermal energy by seasonal COP (2.5–3.8)
The script takes energy in kWh_th and a $/kWh_fuel to stay unit-clean.

## 6. Deriving K from a fuel bill (more honest than design-day)
```
K ≈ (fuel_thermal_kWh × η) / (HDD_base18 × 24 h)      [W/K]
```
Example: 12,000 kWh gas × 0.9 / (3200 HDD·24) = 140 W/K. Use this K; it
absorbs real infiltration and occupant behavior.

## 7. Where savings claims come from (and their honesty)
EPA/ENERGY STAR smart thermostat claims of 8%/10–12% assume ~2 °C 8-h night
+ ~2 °C 8-h away setbacks on furnace homes vs constant hold. Your mileage:
heavy houses and mild climates sit lower; leaky light houses higher. The
script reports % of heating energy, not of the total utility bill — the
common sleight that inflates claims.

## 8. Cooling is NOT symmetric
Setback in cooling saves less than the same ΔT in heating (latent load:
humidity removal), and deep cool setbacks can cause coil-freeze/short-cycle
issues. Out of scope here — the model is heating-only.
