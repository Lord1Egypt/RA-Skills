---
name: pool-chemistry-pilot
description: "Use when a pool/spa owner reports test results (chlorine, pH, CYA, salt, borates, temp) and asks what to add, or asks why water is cloudy/green/irritating, or wants a chemical dosing plan with exact amounts. Computes chemical-by-chemical dosing from your actual test numbers, warns on unsafe water (high CYA, low FC/CYA ratio, pH drift), models the chlorine/CYA relationship, and prints a treatment sequence — never a sales pitch."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [pool, spa, water-chemistry, chlorine, cya, ph, dosing, hot-tub, maintenance]
---

# Pool Chemistry Pilot

## Overview

Pool chemistry advice on the internet is an octopus of conflicts of interest: pool-store free water tests that always find something to sell, forum elders who worship one system and damn all others, and apps with subscriptions. Meanwhile the actual chemistry is well understood: **chlorine disinfects, CYA buffers it, pH controls everything, and 90% of "my pool is green" is a FC/CYA ratio problem, not a product problem.**

This skill is a dosing calculator and diagnostician that works from **your** test numbers:

1. **Dosage engine** — exact amounts (g of dichlor, mL of acid, weight of borax…) to move each parameter from measured to target, using your pool's real volume.
2. **FC/CYA relationship model** — the core physics the pool store won't explain: active chlorine falls as CYA rises; below a threshold, algae outcompete chlorine at full slam levels.
3. **Trouble lights** — high CYA (the "chlorine lock" myth decoded), CH crashing plaster vs vinyl, salt-cell FC production vs demand, metals staining vs algae. Every recommendation is chemistry-first: dilution or generic chemicals, never branded products (sodium hypochlorite = liquid chlorine = bleach, same molecule).
4. **Treatment sequencing** — the order matters (pH first when out of range, then chlorine, then clarifiers). Wrong order wastes chemicals; the pilot prints the order.

State is a plain JSON log; the skill never phones home.

## When to Use

- "My test reads FC 1, pH 7.8, CYA 90 — what do I add?"
- "Pool went green after rain — do I shock it?"
- "How much acid to go from pH 8.0 to 7.4 in 30,000 L?" (dosing math)
- "Eyes burn after swimming — is it chlorine?" (usually pH, and the skill shows why)
- Planning startup chemistry for a new/refill pool or spring opening
- Deciding drain-vs-no-drain for high CYA (dilution math)
- Saltwater pool: cell output vs demand, when to boost manually

**Don't use for:** commercial/public pool code compliance (health-department regulations differ; this is residential guidance), pool building/plumbing/hydraulics, or swallowing-the-chemicals emergencies → poison control (US 1-800-222-1222) / emergency services.

## How It Works — Numbered Workflow

1. **Set up the pool once**: volume in liters or gallons (the script computes volume from pool shape/dimensions if unknown — the #1 dosing error is wrong volume), surface type (plaster/vinyl/fiberglass), and sanitizer type (trichlor/dichlor, liquid/salt).
2. **Log test results** whenever you test: FC, CC, pH, TA, CH, CYA, salt, borates, temp.
3. **Run `status`** — parameter-by-parameter verdict with trouble lights and the FC/CYA ratio check.
4. **Run `plan`** — the dosing sequence: what to add, how much, in what order, with 30–60 min re-test circulation pauses between steps.
5. **Run `slam`** when fighting algae (see Slam Protocol in references) — it computes the slam FC level from CYA and tracks it daily.
6. **Run `history`** to see trends; persistent drift tells you if your TA is too low to hold pH or your fill water is alkali.

## Target Ranges (residential, Trouble-Free-Pool-informed)

| Parameter | Target | Plaster | Vinyl/Fiberglass |
|---|---|---|---|
| FC (with CYA 30–50) | 3–7 ppm | same | same |
| CC | < 0.5 ppm | same | same |
| pH | 7.2–7.8 (aim 7.4–7.6) | same | same |
| TA | 60–120 ppm | 70–90 | 50–70 (fiberglass) |
| CH | 200–400 ppm | 250–450 | 150–250 (essentially cosmetic) |
| CYA | 30–50 ppm | 30–50 | 10–30 (SWG pools lower) |
| Salt (SWG) | 3000–4000 ppm | same | same |
| Borates (optional) | 30–50 ppm | same | same |

**The FC/CYA rule:** maintain FC ≥ 7.5% of CYA (min 3 ppm). At CYA 40 → FC 3 minimum. At CYA 90 → FC 7 minimum and your chlorine is still weaker than tap-water chlorine. High CYA doesn't "lock" chlorine; it hides it in reserve — but the active fraction is what kills algae, and it's tiny. That's the physics pool stores monetize.

## Quick Start

```bash
python3 scripts/pool_pilot.py setup --liters 45000 --surface plaster --sanitizer swg
#   (or --gallons 12000; or --shape rect --length 9 --width 4.5 --avg-depth 1.3 --unit metric)

python3 scripts/pool_pilot.py log --fc 1.5 --cc 0.5 --ph 7.8 --ta 90 --ch 350 --cya 80 --temp 27
python3 scripts/pool_pilot.py status
python3 scripts/pool_pilot.py plan --ph-target 7.4            # full dosing sequence
python3 scripts/pool_pilot.py slam                            # algae kill protocol
python3 scripts/pool_pilot.py history                         # trend table
```

State: `pool_state.json` beside the script. Pure stdlib. No network.

## Chemistry cheat-sheet (what each chemical does)

| Goal | Chemical | Notes |
|---|---|---|
| Raise FC | Liquid chlorine / bleach (sodium hypochlorite) | ~10–12% available chlorine; raises pH slightly |
| Lower pH | Muriatic acid (31.45% HCl) or dry acid (sodium bisulfate) | acid lowers TA a little too |
| Raise pH | Aeration (no TA change); borax / soda ash (also raise TA) | see references for which to pick |
| Raise TA | Baking soda (sodium bicarbonate) | soda ash raises pH much more per unit TA |
| Raise CYA | Stabilizer (cyanuric acid); trichlor/dichlor add it as a side effect | each ppm FC from dichlor adds ~0.9 ppm CYA |
| Raise salt | Pool salt (pure NaCl) | follow cell manufacturer range |

Full table, TA/CH/CYA interactions, and the slam-level table: `references/pool-chemistry.md`.

## Common Pitfalls

1. **Wrong pool volume.** Every dose scales with volume; a 20% volume error is a 20% dosing error. `setup --shape` computes it from dimensions; when in doubt, do the salt-rise method (add known kg salt, measure ppm rise).
2. **Chasing pH with product instead of aeration.** pH constantly rises in outdoor pools from CO2 outgassing; the fix is lower TA, not endless acid-and-backwashing.
3. **Ignoring CC.** Combined chlorine is "used up" chlorine holding organics; persistent CC > 0.5 means under-chlorination or ammonia in the water. That's a slam, not a shock-and-hope.
4. **Trichlor in a hot tub / small vinyl pool.** Trichlor is acidic (pH ~3) and adds CYA relentlessly; in small volumes CYA rockets. Dichlor same problem, gentler. For spas: liquid chlorine or lithium hypochlorite, or bromine. CYA runaway is the #1 "why is my pool always green" root cause.
5. **Shocking by "1 lb per 10k gal" folklore.** Shock level is a function of CYA: CYA 30 → slam 12; CYA 70 → slam 28. One-size shocks under-dose at high CYA (looks like "chlorine demand" and sells more product).
6. **Adding chemicals simultaneously or in the wrong order.** pH must be in range before you judge chlorine efficacy; acid and chlorine 30 min apart, pump running. The `plan` command sequences automatically.
7. **Testing at the wrong time.** FC falls through the day (sun consumes CYA-buffered chlorine); test at the same hour daily or your trend is noise.
8. **Pool-store CYA tests over-reporting.** The turbidimetric CYA test reads high at high CYA (dilution error compounding); if the melamine test says >90, dilute the sample 1:1 with distilled water, re-test, double the reading.

## Verification Checklist

- [ ] `setup` wrote `pool_state.json` with volume/surface/sanitizer
- [ ] `log` of a full test panel then `status` prints a verdict per parameter + FC/CYA ratio
- [ ] `plan` prints grams/mL per chemical with a sequence and re-test pauses
- [ ] `slam` computes slam FC from CYA and prints the daily checklist
- [ ] `history` shows the logged trend
- [ ] No network imports (grep requests/urllib/socket — empty)

## One-Shot Recipes

**"Green pool after a storm":**
```bash
python3 scripts/pool_pilot.py log --fc 0 --cc 1.0 --ph 7.2 --cya 45
python3 scripts/pool_pilot.py slam     # → slam level 18 ppm, brush 2x/day, filter 24/7, re-test FC nightly, keep FC at slam until FC holds overnight + water clear
```

**"Eyes burn — too much chlorine?"**
```bash
python3 scripts/pool_pilot.py log --fc 3 --ph 8.2 --ta 130 --cya 40
python3 scripts/pool_pilot.py plan    # → pH 8.2 is the culprit; acid dose to 7.4, then aeration, then drop TA
```

**"CYA is 90 — drain?"**
```bash
python3 scripts/pool_pilot.py log --cya 90
python3 scripts/pool_pilot.py plan --cya-target 40   # → 55% dilution or drain to 40% and refill (dilution math printed)
```

## Safety

Chemicals are hazardous. Always add acid to water (never water to acid), wear eye protection, never mix chlorine with acid (chlorine gas), store locked away from children. Pool chemistry is safe when respected. If swallowed: US Poison Control 1-800-222-1222, EU 112.

## License & Disclaimer

MIT. Residential guidance from standard pool chemistry; not a substitute for public-pool regulatory compliance or professional service. Generic chemical names only — no brand affiliations.
