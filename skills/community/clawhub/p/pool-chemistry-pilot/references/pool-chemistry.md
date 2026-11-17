# Pool Chemistry — Reference

## 1. The FC/CYA relationship (the core model)

Free chlorine in an outdoor stabilized pool exists mostly **bound to cyanuric acid**. Only the unbound fraction (HOCl, "active chlorine") sanitizes. As CYA rises, the bound fraction grows and active chlorine falls — roughly **hyperbolic**:

- CYA 0: active chlorine ~100% of FC
- CYA 20: FC is ~5% active
- CYA 30: ~3.5% active
- CYA 50: ~2% active
- CYA 90: ~1% active

Two practical consequences:

1. **Minimum FC scales with CYA.** The Trouble-Free-Pool consensus: maintain FC ≥ 7.5% of CYA (minimum 3 ppm, and never below 1 at any CYA). At CYA 40 keep FC ≥ 3; at CYA 80 keep FC ≥ 6. This is why the "I keep adding chlorine and it's still green" pool almost always has CYA 100+: the chlorine is present but chemically sleeping.
2. **"Chlorine lock" is a misnomer.** Chlorine is not locked; it is buffered. You can wake it up by raising FC to the slam level *for your CYA* — or, better, lowering CYA by dilution. Nothing you can buy "unlocks" it; the fix is water replacement or drainage.

### Slam (Shock Level And Maintain) table

| CYA (ppm) | Slam FC (ppm) |
|---|---|
| 0 | 10 |
| 10 | 10 |
| 20 | 10 |
| 30 | 12 |
| 40 | 16 |
| 50 | 20 |
| 60 | 24 |
| 70 | 28 |
| 80 | 31 |
| 90 | 35 |
| 100+ | drain/refill recommended (35+ unmanageable) |

Slam protocol: hold FC at slam level (test and re-dose as often as needed — typically every 2–4 h daytime, once at night), brush twice daily, pump/filter 24/7, clean filter when pressure rises 25%+. **You are done when**: FC holds overnight (loses <1 ppm dusk-to-dawn), CC < 0.5, and water is clear. Then let FC drift back to maintenance range.

## 2. pH, TA, and CO2 — why pH always rises

Pool water contains dissolved CO2 in equilibrium with air. Pool water is intentionally over-carbonated (that's TA — total alkalinity, mostly bicarbonate). CO2 outgasses → pH rises → that's the default drift of every outdoor pool: **pH up, TA slowly down**.

- Aeration (waterfalls, spa jets, kids splashing) accelerates outgassing → faster pH rise.
- Acid lowers both pH and (permanently) a bit of TA.
- Borates (30–50 ppm) buffer pH rise and reduce acid demand ~half.

**The classic error**: fighting perpetual pH rise with acid alone. Each acid addition cuts TA; eventually TA crashes and pH becomes unstable (bounces). The right strategy when pH perpetually runs high: lower TA to 60–70 (plaster) / 50–60 (vinyl, fiberglass), then let pH settle where it wants with minimal acid. Lower TA = less carbonation = slower outgassing = stabler pH.

TA target note: "TA 100–120" from bottle labels is pool-store canon; modern practice favors 60–80 for stable pH, offset by higher CH in plaster pools (the CSI balance matters more than any single number — see §5).

## 3. Chemical dosing math (what the script computes)

Pool-calculator constants, per **10,000 L of water** (divide/multiply for your volume):

| Goal | Chemical | Amount per 10,000 L per unit change |
|---|---|---|
| +1 ppm FC | liquid chlorine 12% | ~83 mL |
| +1 ppm FC | liquid chlorine 10% | ~100 mL |
| +1 ppm FC | dichlor (56% avail. Cl) | ~18 g |
| +1 ppm FC | cal-hypo 68% | ~15 g (adds 0.7 ppm CH) |
| +1 ppm FC | trichlor (90%) | ~11 g (adds 0.6 ppm CYA, lowers pH) |
| −0.1 pH unit (pH 7.6→7.5, TA-dependent) | muriatic acid 31.45% | ~60–100 mL (use TA-based table) |
| −1 ppm TA | muriatic acid 31.45% | ~125 mL |
| +1 ppm TA | baking soda | ~16.7 g |
| +1 ppm CH | calcium chloride 77% | ~12 g |
| +1 ppm CYA | pure cyanuric acid | ~8.3 g |
| +1 ppm salt | NaCl | ~10 g |
| +1 ppm borates | boric acid | ~11 g (plus ~15 g for the pH rise it buffers; see notes) |

Acid dosing is nonlinear in pH (buffer capacity peaks near pH 7.5 and depends strongly on TA). The script uses the standard piecewise table (TA 60/80/100/120 curves) rather than a single factor — read the pH-dose table in any pool calculator for the underlying curves. When precision matters, dose 80% of the calculated acid, circulate 30–60 min, re-test.

Cyanuric acid facts: dissolves slowly (put in a sock in the skimmer, pump 24/7; may take days); **the test only reads down to ~20–30 ppm reliably and overshoots above ~80** (dilute sample 1:1 with distilled, re-test, ×2). Each 1 ppm FC from dichlor adds ~0.9 ppm CYA; from trichlor ~0.6 ppm. This is the CYA ratchet: stabilized chlorine *is* the CYA source.

## 4. Sanitizer systems compared

- **Trichlor (pucks)** — cheap, convenient, acidic (pH ~3), CYA ratchet. Fine for high-use seasonal pools drainable each year; a slow disaster for year-round pools (CYA creep → 100+ → green pool → "chlorine lock" → pool store sells "phosphate remover").
- **Liquid chlorine / bleach** — no CYA side effect, pH-neutral-ish (slight rise), cheap in bulk. The default recommendation for most pools. Dose daily-to-every-other-day (it consumes itself at 2–4 ppm FC/day in sun; ~10%/day at CYA 30–50).
- **Saltwater generator (SWG)** — on-site electrolysis of salt to chlorine. Water feels nicer, no handling liquid chlorine; cell costs ~$500–900 every 3–7 seasons. SWG pools prefer CYA 60–80 (higher CYA = less FC consumption = less cell duty), TA 60–80, and slightly lower pH targets (cells tend to raise pH via H2 outgassing at the plates — aeration effect).
- **Bromine** — spas/hot tubs. Stable at high temps (chlorine isn't), reactivates from bromide by any oxidizer. Don't mix bromine and chlorine pools — switching is a drain.
- **Biguanide (Baquacil)** — non-chlorine; prone to slime and mold after a few seasons; conversion back to chlorine is miserable. Not recommended here.
- **Mineral systems** (copper/silver cartridges) — supplementary at best; copper stains blonde hair and plaster at higher levels, silver barely works without chlorine. Marketing-first chemistry.

## 5. CSI — the saturation balance (protects plaster, prevents scaling)

Calcium Saturation Index (Langelier-type): accounts for pH, temperature, CH, TA, CYA (carbonate fraction), and TDS. Target **−0.3 to +0.3**.

- CSI > +0.3: scaling (cloudy water, crust on heater elements, rough plaster)
- CSI < −0.3: water dissolves calcium — etching plaster, pitting heater copper, pinhole corrosion

The script computes CSI from your logs. Vinyl/fiberglass pools tolerate negative CSI (no plaster to etch) but avoid < −0.6 for metal-fittings sake. Never chase "perfect TA" while CSI is screaming — balance trumps individual targets.

## 6. Cloudy/green water triage

**Green** = algae (almost always). Test FC/CYA: ratio below maintenance → slam per the table. Phosphate removers don't kill algae (chlorine does); phosphates only reduce regrowth food. "Algaecides" (quats/polymers) are preventatives, not cures — slam is the cure.

**Cloudy** after slam/shock = dead algae/filter fines. Filter 24/7 (DE > cartridge > sand for fines), consider cellulose filter aid; clarifiers (cationic polymers) clump fines for the filter — mechanical fix, not chemical.

**Cloudy + high CH + high pH + CSI > +0.3** = calcium carbonate precipitation. Fix balance, don't floc.

**Metals**: iron/copper in fill water oxidized by high FC or high pH → green/rust stains and "green but no algae" water. Ascorbic acid lifts stains; sequestrant (HEDP) holds metals in solution. Raising FC to slam with metals present stains — check history/logs for metal episodes first (the script flags slam-before-metal-check if CH unusually low or pH logged very low historically... in practice: ask the owner).

## 7. Seasonal rhythm

- **Spring opening**: degrease/de-scale the waterline, clean filter media, test full panel, slam once water is 15°C+ (chlorine works poorly cold; below 10°C you can hold lower FC), balance TA first, then pH, then CH, then CYA, then start borates if used.
- **High summer**: FC consumption doubles (UV + bather load). SWG boost; liquid-chlorine pools dose evenings (sun degrades daytime doses).
- **Fall/winter**: bring pH to 7.2–7.4, CH to target (protects plaster through ice), algaecide (polyquat 60) at close, enzymes for non-chlorine oxidizables, lower water below skimmers in freeze climates.

## 8. Testing guidance

- **Test the same time daily** (FC falls through the day; consistent hour = comparable trend).
- K-2005/K-2006-style drop kits (FAS-DPD) beat test strips by an order of magnitude. Strips are go/no-go checks, not dosing instruments. The one exception: strips for pH/TA quick checks between drop tests.
- CYA above ~80: dilution protocol (1:1 distilled, re-test, double).
- **Salt**: only needed for SWG pools; calibrate the cell's reading against a drop/lambda test each season (cells drift).
- Keep a log (this script's `history`) — most "sudden" problems are visible as 3-week trends in hindsight.
