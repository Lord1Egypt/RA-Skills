---
name: mattress-spec-decoder
description: Use when shopping for a mattress or decoding one you already own — translates marketing specs into materials science (foam density lb/ft³, ILD, coil type/count/gauge), computes your firmness band from sleep position + BMI, scores durability and real lifespan, decodes warranty sag-thresholds and prorated traps, and compares two mattresses side by side for YOUR body instead of brand marketing.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [mattress, sleep, shopping, consumer, bedding, ergonomics, warranty]
---

# Mattress Spec Decoder

Mattress shopping is engineered confusion: every retailer gets a different
model name for the same bed (so you can't price-compare), and the spec sheet
is written in marketing ("UltraCool Gel Infinity Foam!") instead of the four
numbers that actually predict performance: **foam density**, **ILD**,
**coil type/count**, and **layer stack order**.

This skill decodes the specs, computes the firmness band your body actually
needs, and tells you how many years the mattress will really last.

## When to Use

- Shopping for a new mattress (online or store) and comparing options
- Decoding a spec sheet: "is 1.5 lb/ft³ foam good or garbage?"
- Choosing firmness for your sleep position and body weight
- Deciding between memory foam / latex / hybrid / innerspring
- Checking whether a warranty is real coverage or theater
- Diagnosing sagging: "is this covered or is this normal softening?"
- Two sleepers with different positions/weights: what works for both

**Don't use for:** medical sleep disorders (apnea — see a doctor), or
crib/toddler mattresses (different safety rules: firm, tight fit, waterproof).

## Core Numbers That Matter

| Spec | Junk | Good | Excellent | Why |
|---|---|---|---|---|
| Memory foam density | <3.0 lb/ft³ | 3.0–4.0 | >4.0 | Density = lifespan. Low-density foam impressions in 1–2 years |
| Base (poly) foam | <1.5 lb/ft³ | 1.5–1.8 | >1.8 | The support layer nobody advertises — where cheap beds cheat |
| Latex density | — | 4.3–5.3 | 5.9+ | Durable across the board; weight is the tradeoff |
| Coil count (queen) | <300 | 480–900 | >900 is marketing | Returns diminish past ~900; type matters more |
| Coil gauge | 15+ (soft) | 13.5–14.5 | zoned 12.5–15 | Lower gauge = firmer steel |
| ILD/IFD | — | 10–15 soft / 15–25 med / 25+ firm | — | Very rarely published; ask or infer |

## Quick Start

```bash
# Firmness band for a 78 kg / 175 cm side sleeper
python3 scripts/mattress_advisor.py recommend --position side --weight 78 --height 175

# Couple with different profiles — get the compromise band
python3 scripts/mattress_advisor.py couple --p1 side,62,168 --p2 stomach,95,182

# Decode a spec sheet
python3 scripts/mattress_advisor.py decode --type hybrid \
    --memory-density 3.0 --base-density 1.5 --coils 480 --coil-type pocketed

# Compare two mattresses for your profile
python3 scripts/mattress_advisor.py compare --profile side,78,175 \
    --a 'name="DreamCloud-ish",type=hybrid,memory_density=4.0,base_density=1.8,coils=850,coil_type=pocketed,price=1100' \
    --b 'name="Box-o-Foam",type=foam,memory_density=2.5,base_density=1.3,coils=0,price=500'

# Is the 10-year warranty worth anything?
python3 scripts/mattress_advisor.py warranty --years 10 --prorated --sag-threshold 1.5

# Sagging after 2 years — covered?
python3 scripts/mattress_advisor.py sag --measured 1.75 --threshold 1.5 --years-owned 2
```

Stdlib-only Python 3. Offline. No brand affiliations.

## Workflow

1. **Profile first.** `recommend` → your firmness band (1–10), target ILD,
   mattress-type candidates, and body-specific warnings (BMI ≥ 30 needs
   ≥1.8 lb/ft³ base foam or impressions form fast).
2. **Decode the spec sheet.** `decode` → durability verdict per layer +
   expected lifespan + which specs are marketing noise.
3. **Compare finalists.** `compare` → weighted score for YOUR profile
   (support-fit, durability, motion isolation, heat, edge) with the reasoning
   printed per criterion.
4. **Stress-test the warranty.** `warranty` → sag threshold, prorated
   schedule math, what voids coverage. `sag` → verdict for your measured dip.
5. **Shop outside the label.** Use `references/buying-playbook.md`: same-bed
   fingerprinting, floor-model math, delivery-day inspection.

## Firmness Logic (what the script computes)

Base firmness by position: side 4/10 (shoulder/hip pressure), back 6/10,
stomach 7.5/10 (hip sink → spinal extension), combo 6/10.
BMI shift: <19 → −1; 25–29.9 → +1; ≥30 → +2 and a hard requirement for
high-density support. Couples: take the max firmness of the two profiles and
solve pressure relief with a comfort layer (topper), not a softer core —
split-core or dual-firmness options if the gap > 1.5 points.

## Common Pitfalls

1. **Trusting "10-year warranty."** Most are prorated after year 1–5, require
   sag > 1.5" measured with a string and no load, and are voided by stains.
   `warranty` decodes this.
2. **Buying by brand name.** Model names are retailer-exclusive on purpose.
   Match specs (densities, coil count, layer stack) instead.
3. **Ignoring base foam density.** Everyone checks memory foam; cheap beds
   cheapen the SUPPORT layer below it. That's what sags.
4. **One mattress, two bodies.** Averages don't work: the heavier sleeper's
   correct firmness destroys the lighter one's spine. Solve in layers.
5. **Judging in 5 minutes in a store.** Memory foam needs 10+ minutes to
   imprint; take your time, or rely on a ≥100-night trial.
6. **Confusing thick = durable.** 14" of low-density foam is worse than 10"
   of high-density. Total height is a marketing number.
7. **Firmness ≠ support.** Support = spinal alignment; firmness = surface
   feel. Heavy people can sleep on soft IF the support layer is dense.

## Verification Checklist

- [ ] `recommend` run with real weight/height/position
- [ ] Spec sheet decoded with actual densities (call the manufacturer —
      they must tell you; refusal is a verdict in itself)
- [ ] `compare` shows reasoning per criterion, not just a score
- [ ] Warranty decoded before purchase
- [ ] Trial period ≥ 100 nights confirmed (30-night minimum to adjust)

## References

- `references/mattress-science.md` — density/ILD/coil deep dive, layer stack
  order effects, heat and off-gassing physics, lifespan tables
- `references/buying-playbook.md` — same-bed fingerprinting, negotiation,
  delivery inspection, topper-first rescue for an existing mattress
