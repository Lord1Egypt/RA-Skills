---
name: property-tax-appeal-kit
description: Use when the annual assessment notice jumps, property taxes feel wrong, or before filing a tax appeal — equalization math (is your assessment ratio out of line vs the municipality's?), factual-error audit of the property record card (wrong square footage/baths is the cheapest win in appeals), comparable-sales evidence grading, dated appeal-window timeline from the notice date, and the hearing script with the three legal argument classes ranked by win rate.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [property-tax, appeal, assessment, home-ownership, taxes, real-estate]
---

# Property Tax Appeal Kit

## Overview
Most homeowners overpay property taxes not because their rate is wrong but because their **assessment** is wrong — and fewer than 5% ever appeal, which is exactly why assessors' mass-appraisal models drift: nobody checks them. Assessment errors are systematic: models never visited your house, don't know the basement floods or the highway got built behind it, and carry forward stale property-record-card data (the finished-basement the previous owner reported, the "2.5 baths" that are 1.5). A successful appeal needs three things most owners lack: the **equalization math** (whether you're assessed out of line — the only thing boards rule on), **evidence in the right form** (graded comparable sales, not "my taxes are too high"), and the **dated window** (typically 25–45 days from the assessment notice; miss it, wait a year).

This kit computes all three: equalization ratio vs the town's average (the uniformity argument), a record-card error audit (factual errors are near-automatic wins and don't even need comps), comparable grading and price-per-sqft analysis, savings math at your millage rate, and the hearing script with argument classes ranked: **1) factual error, 2) unequal assessment, 3) market value**.

## When to Use
- Assessment notice arrived and the value jumped more than the neighborhood did
- Considering "we'll appeal your taxes for 50% of savings" firms (this kit replaces them — their evidence is the same comps)
- Bought a house recently below its assessment (purchase price is evidence in most states)
- Property record card shows square footage, baths, or features that aren't real
- Permanent defect emerged (foundation, flood plain remap, adjoining construction) the model doesn't know

**Don't use for:** tax-bill hardship programs (senior/disabled exemptions and deferrals — different application, county office), rental income-property appeals in rent-controlled jurisdictions (income approach rules differ), or fighting the millage *rate* (that's a political/budget process, not an appeal — appeals contest your *value* only).

## Quick Start
```bash
# Equalization: are YOU out of line? (town avg ratio 0.92, yours 1.15)
python3 scripts/ptax.py equalize --assessed 420000 --market-est 365000 \
    --town-avg-ratio 0.92 --millage 24.5

# Record-card audit: the card says 2100 sqft / 2.5 bath; reality disagrees
python3 scripts/ptax.py card --card-sqft 2100 --actual-sqft 1950 \
    --card-baths 2.5 --actual-baths 1.5 --assessed 420000 --market-est 365000

# Comp evidence grading: 5 nearby sales
python3 scripts/ptax.py comps --assessed 420000 --subject-sqft 1950 \
    --sales "385000,2400" "322000,1900" "359000,2150" "341000,2000" "299000,1650"

# Dated timeline from your notice (30-day window, informal first)
python3 scripts/ptax.py timeline --notice 2027-01-15 --window 30 --informal yes
```

## The Three Argument Classes (ranked)
1. **Factual error** (highest win rate, cheapest): the record card is wrong — square footage, bath count, lot size, "finished" basement that isn't, garage that's a carport, deck long gone. Get the card from the assessor (public record, often online), walk the house with a tape measure, photograph every discrepancy. Value impact is mechanical (sqft × neighborhood $/sqft). No comps needed; no market argument to lose.
2. **Unequal assessment** (uniformity): your assessment ÷ your market estimate is out of line with the town's average ratio (or with comparable properties' ratios). Boards respond to this because equalization is their legal duty. Evidence: 3–5 assessed ratios of similar homes (public rolls) + your case. Script computes your ratio and the gap.
3. **Market value**: graded comparable sales — same town, ≤0.5–1 mi, sold within 6–12 months, similar style/age/size (within ±20–25% sqft), arms-length (not foreclosure/family sale). Adjust or drop outliers; median $/sqft beats average. Weakest class alone but strengthens 1–2.

## Verdict Bands (equalize output)
| Your ratio vs town avg | Verdict |
|---|---|
| > 1.10× avg | STRONG UNEQUALITY — appeal-ready; savings quantified |
| 1.03–1.10× avg | WORTH FILING — pair with record-card audit |
| 0.97–1.03× avg | IN LINE — only appeal on factual errors |
| < 0.97× avg | UNDERASSESSED — do NOT appeal (you invite a raise) |

## Common Pitfalls
1. **Arguing "taxes are too high."** Boards can't cut the rate; the only question is your value. Emotional testimony loses.
2. **Missing the window** — 25–45 days from the notice date (varies by jurisdiction; some run from publication). The `timeline` command dates every step; calendar it the day the notice arrives.
3. **Using listing prices as evidence** — boards want **sold** prices (closed, arms-length). Listings are asking, not proof.
4. **Comps from a different town/school district** — instantly discounted; tax rates and markets differ.
5. **Ignoring the record card** — a 150 sqft error is a mechanical win that costs one tape measure and one form.
6. **Appealing during a hot market when the ratio shows you underassessed** — a hearing can end with your assessment *raised*. Check equalization first; the script warns.
7. **Paying a contingency firm 30–50% of savings** for comps you can pull from the same public rolls this kit uses.
8. **Recent purchase above assessment** — in most states the sale can reset the basis; check state rules before accidentally documenting yourself upward.

## Verification Checklist
- [ ] Notice date logged; filing deadline computed and calendared (window from notice/publication per your jurisdiction)
- [ ] Property record card pulled and audited line-by-line vs measured reality (sqft, baths, lot, features)
- [ ] Equalization ratio computed vs town average — verdict checked against bands
- [ ] 3–5 graded sold comps (≤1 mi, 6–12 mo, ±25% size, arms-length) with median $/sqft
- [ ] Savings computed at your actual millage; filing effort priced against it
- [ ] Evidence packet: card copy + photos + comp table + ratio math (boards love numbers they can check)
- [ ] Hearing script rehearsed: lead with facts, end with the requested value (not "something lower")
- [ ] Next-year re-check calendared (assessment drift returns; make it an annual 30-minute audit)

## Example Session
```
$ python3 scripts/ptax.py equalize --assessed 420000 --market-est 365000 \
    --town-avg-ratio 0.92 --millage 24.5
EQUALIZATION CHECK
  your assessment:  $420,000   your market estimate: $365,000
  your ratio:       1.151  vs town average 0.920
  you are assessed 25.1% ABOVE the typical town ratio
  implied fair assessment: $365,000 x 0.92 = $335,800
  tax now:    $420,000 x 24.5 mills / 1000 = $10,290/yr
  tax at fair: $335,800 x 24.5 / 1000  = $8,227/yr
  SAVINGS IF WON: ~$2,063/yr (multi-year until reassessment cycle)
VERDICT: STRONG UNEQUALITY — appeal-ready. File with uniformity
  argument + record-card audit; request $335,800 (a number with
  math behind it), not "lower."

$ python3 scripts/ptax.py card --card-sqft 2100 --actual-sqft 1950 \
    --card-baths 2.5 --actual-baths 1.5 --assessed 420000 --market-est 365000
RECORD-CARD AUDIT
  [ERROR] square footage: card 2100 vs measured 1950 (-150 sqft, -7.1%)
  [ERROR] bathrooms: card 2.5 vs actual 1.5 (a half-bath counted full)
  value impact at town $/sqft ($187/sqft est): ~$28,000 + bath adj ~$5,000
  this is a FACTUAL-ERROR appeal — strongest class, no comps required.
  packet: card copy, photos, sketch with measurements, this math.
```
