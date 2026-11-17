# Pool Chemistry Pilot

**Skill:** `pool-chemistry-pilot` · v1.0.0 · MIT · ClawHub `@voronindenis5/pool-chemistry-pilot`

## The real-world problem

Ten million-plus US households and millions more worldwide own a pool or spa — and nearly every one of them is caught between two bad information sources: pool-store "free water tests" designed to sell chemicals, and forum elders preaching conflicting gospels. The result is a national pattern of over-chlorinated, over-stabilized, perpetually green pools: the most common root cause ("CYA creep" from stabilized chlorine pucks) is invisible to strip tests and lucrative to the stores that caused it.

The chemistry itself is settled science. The FC/CYA relationship, the pH/TA/CO₂ outgassing cycle, and the Langelier saturation index are textbook material — they're just not packaged for a pool owner holding a test kit at 6PM.

## What it does

An offline dosing calculator and diagnostician, pure stdlib Python, state in a local JSON:

- **`setup`** — pool volume from dimensions (the #1 dosing error source), surface, sanitizer type
- **`log`** — test results (FC, CC, pH, TA, CH, CYA, salt, temp); `latest` merges most-recent values
- **`status`** — per-parameter verdicts, the FC/CYA ratio check (min FC = 7.5% of CYA), and a proper Langelier CSI (scaling/corrosive flag)
- **`plan`** — ordered treatment sequence with exact grams/mL: pH first, then FC, CYA dilution math, TA, CH, salt — each with a "why" and re-test pauses
- **`slam`** — the Shock-Level-And-Maintain protocol: slam FC interpolated from your CYA (CYA 40 → 16 ppm, CYA 80 → 31), chlorine dose, daily loop checklist, done-criteria
- **`history`** — trend table; "sudden" problems are usually visible as 3-week trends

Chemistry-first and brand-free: sodium hypochlorite is sodium hypochlorite, whether sold as pool shock or laundry bleach.

## Who needs this

- **Residential pool/spa owners** tired of the $200 pool-store visit that "finds" phosphate problems
- **New pool buyers** staring at a Taylor K-2006 kit with no idea what TA means
- **Hot-tub owners** — the skill flags the trichlor-in-small-volume trap that CYA-rockets spas
- **Saltwater (SWG) pool owners** — different CYA/TA targets, cell-vs-demand boost logic
- **Anyone fighting recurring green water** — the slam protocol ends the shock-and-hope cycle

## Example

```bash
python3 scripts/pool_pilot.py setup --shape rect --length 9 --width 4.5 --avg-depth 1.3 --sanitizer swg
python3 scripts/pool_pilot.py log --fc 1.5 --ph 7.9 --ta 90 --cya 80 --salt 2800
python3 scripts/pool_pilot.py plan --cya-target 50
# 1. LOWER pH 7.9 -> 7.6   muriatic acid: 711 mL
# 2. RAISE FC 1.5 -> 6.0+  liquid chlorine 12%: 2.62 L
# 3. LOWER CYA 80 -> 50    replace 38% of pool water (19.7 m³)
# 4. RAISE SALT -> 3200    21 kg NaCl
```

## Safety

Residential guidance only — not public-pool regulatory compliance. Generic chemicals are hazardous: acid to water never the reverse, chlorine and acid never mixed, stored locked. Ingestion: US Poison Control 1-800-222-1222, EU 112.

## License

MIT © Denis Voronin
