# Heating Setback Optimizer

**"Turn the thermostat down at night — you'll save 10%." "No, the recovery
burns it all." Both folk claims are wrong, and which one is *more* wrong
depends on your house and heating system.** This tool computes the actual
degree-hour savings for YOUR building, subtracts recovery costs, applies
system-specific rules (heat-pump strips, radiant slabs), and prices the
season in dollars.

```
python3 scripts/setback.py --fuel-kwh 12000 --hdd 3200 --system furnace --depth 3 --hours 8
# Setback 3.0C x 8h/day: saves 591 kWh fuel (3.6% of heating) = $59.06/season

python3 scripts/setback.py --k 180 --system heat-pump --scan --price 0.25
# Scan: depth 2C -> $48 saved | depth 3C+ -> $0 (strips eat it)  ← the backfire
```

## The real-world problem
- Nearly every household argues about this. Generic advice ignores the two
  decisive variables: **heat-loss coefficient K** (derivable from last
  winter's fuel bill — the script does it) and **heating system**.
- The expensive trap: **deep setbacks on heat pumps with auxiliary resistive
  strips**. Night savings at COP 3 get repaid at morning recovery on COP-1
  strips — net zero or negative. HVAC forums are full of this; the scan mode
  shows exactly where the curve flattens to $0.
- Radiant-slab owners who copy furnace advice get a cold house all day (slab
  time constants are 6–12 h). The verdict engine caps them at 1 °C.
- Smart-thermostat marketing quotes "10–12% savings" — this tool computes
  your number instead of the brochure's.

## What it does
- Derives K from `--fuel-kwh --hdd` (bill-based, absorbs real infiltration)
- Degree-hour savings with thermal-mass realization factor (light/medium/heavy)
- Recovery penalty model for strip-equipped heat pumps; oversize factors per
  system; morning ramp minutes (full-mass vs air-feels-warm)
- `--scan` ranks setback depths 0–6 °C by net $ saving for your setup
- System handbook in references: furnace/boiler, heat pump (+cold-climate
  inverter nuance), radiant slab, electric baseboard (always pays)

## What's inside
- `SKILL.md` — triggers, steps, pitfalls, checklist
- `references/setback-physics.md` — the identity Q=K·ΔT, degree-hour math,
  mass/τ tables, per-system rules, deriving K from bills, honest reading of
  vendor claims
- `scripts/setback.py` — pure stdlib, `--json`, tested: furnace (1.2%/°C·8h
  band ✓), heat-pump backfire (deep setback → $0 ✓), scan ranking ✓

Heating-only (cooling has different latent-load physics — out of scope).
±20% decision-grade accuracy: right for choosing a schedule, not for
predicting an invoice.

MIT © Denis Voronin
