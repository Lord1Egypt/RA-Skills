---
name: home-sale-proceeds-planner
description: "Use when selling a home and you need the real net-proceeds number: itemizes every deduction from the sale price (commissions, closing costs, mortgage payoff with per-diem interest, credits, transfer taxes by state), computes capital-gains exclusion eligibility (250k/500k + 2-of-5-year rule), prices pre-sale improvements that pay back, and compares rent-vs-sell honestly. Solves the 'I thought I'd clear 200k and got 140k' surprise."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [real-estate, home-sale, net-proceeds, capital-gains, closing-costs, moving]
---

# Home Sale Proceeds Planner

## Overview

Sellers fixate on the sale price and get blindsided by the settlement statement. Between accepted offer and wire transfer, 6–10% of the price evaporates: 5–6% realtor commissions (negotiable, and the 2024 NAR settlement changed the structure), title/escrow/attorney fees, transfer taxes (zero in some states, ~1%+ in others), mortgage payoff with per-diem interest to the funding date, property-tax prorations, repair credits, and the moving costs nobody counts. The number that matters — **the wire hitting your account** — is a calculation, and doing it at offer time changes decisions: what offer to accept, whether to credit vs repair, whether to rent it out a year instead.

On top of the proceeds math sits the tax layer: the **Section 121 exclusion** ($250k single / $500k married filing jointly of gain, tax-free) with its ownership+use 2-of-5-year test and the 2-year waiting period between exclusions, plus adjusted basis (purchase price + capital improvements + selling costs) — which is where sellers leave real money by forgetting improvements and overpaying tax. Recapture of depreciation (for the rental-period crowd) and the 3.8% NIIT surtax on high earners complete the trap set.

This skill produces: a full **net-proceeds estimate** (line-itemed, state-aware on transfer tax), a **capital-gains estimate** with exclusion application and improvement-basis capture, a **credit-vs-repair decision aid**, and a **rent-vs-sell first-pass comparison**.

## When to Use

- Listing soon or weighing an offer: what clears after everything?
- "Should I fix it up first?" — which pre-sale improvements return more than they cost (mostly they don't)
- Estimating taxes: exclusion eligibility, basis from improvements, depreciation recapture for past rentals
- Rent vs sell: honest first-pass numbers (cap rate from net operating income, not gross rent myths)
- Timing: the 2-year exclusion clock (ownership+use), mid-year occupancy, moving-deduction reality (mostly gone for employees post-2017)

**Don't use for:** 1031 exchanges (investment-property deferral — specialist territory; the skill flags when it applies), short sales/foreclosure tax traps (cancelled-debt income — CPA), or non-US tax systems (capital-gains rules here are US federal + state pointers).

## Net Proceeds Model (line items)

```
sale_price
− commission % (buyer + seller agent; negotiable, post-2024 decoupled)
− seller closing costs:
    title insurance + escrow/settlement fee     (region varies, 0.4–1.2%)
    attorney fee (attorney states)              ($500–1,500)
    transfer tax                                 (STATE TABLE: 0–2%+)
    recording/HOA estoppel/county misc           ($200–800)
− mortgage payoff(s) incl. per-diem interest     (payoff ≠ statement balance)
− liens: HELOC, tax, mechanic's, solar lease/PPA (VERIFY solar paper!)
− property tax proration                        (credit if prepaid)
− repair credits / buyer closing-cost credits    (from the offer)
− home warranty for buyer                        ($350–600, optional concession)
− courier/wire/recording misc                    ($100–300)
= NET PROCEEDS (before moving costs & taxes)
```

Then the tax layer on gain: `gain = net_sale_price − adjusted_basis`; `adjusted_basis = purchase_price + capital_improvements + selling_expenses (incl. commission)`; exclusion applied if 2-of-5 rules met.

### Transfer tax quick table (state level only — cities add more)

| State | Rate (per $100 / ~%) |
|---|---|
| AK, ID, IA, LA, MO, NM, ND, OR*, TX, UT, WY, MS | ~0 (none or trivial) |
| CA | $0.55/$500 ≈ 0.11% (many cities add) |
| CO | 0.01–0.02% |
| FL | $0.70/$100 = 0.7% (deeds) |
| GA | $1/$100 = 1% |
| IL (Chicago) | 0.75% + city 1.05–1.5% |
| MA | $2.28/$500 ≈ 0.46% + municipal |
| NY | $2/$500 ≈ 0.4% + NYC 1–1.425% + mansion tax |
| WA | 1.28% (excise, seller) |
| Others | 0.1–0.5% typical |

*OR: some counties. Always verify county+city stacking — this is the line item sellers most often miss.

## Capital-Gains Exclusion (Section 121) — the gate checks

1. **Ownership test:** owned the home ≥ 24 months of the last 60.
2. **Use test:** lived in it as primary residence ≥ 24 months of the last 60 (can be nonconsecutive).
3. **Not excluded another home** in the prior 2 years (once every 2 years).
4. Exclusion: $250k single / $500k MFJ of *gain* (not proceeds) tax-free.
5. **Partial exclusion** if moved for work/health/unforeseen (safe harbors): exclusion × (months of qualifying use / 24).
6. **Rental-period allocation** (nonqualified use after 2008): gain allocable to nonqualified use is NOT excluded — prorate; plus **depreciation recapture** (unrecaptured §1250, up to 25% rate) is never excluded.
7. Improvements count into basis ONLY if capital (asset lasting >1 yr: roof, kitchen, HVAC, addition) — not repainting/repairs. Keep receipts; the script takes an improvements list.

## Credit-vs-Repair Decision (offer negotiation)

- Buyer credit ≤ expected repair cost × (1 − your time/hassle discount) is usually better than doing the repair yourself pre-closing: you skip contractor risk and timeline risk.
- Lender caps: buyer credits are capped (typically 3–9% of price by loan type) — credits sometimes get shaved at underwriting; repairs by seller don't.
- Pre-sale cosmetic spend that reliably returns >1×: paint, flooring fixes, light plumbing/electrical fixes, deep clean + staging. Returns <1× usually: kitchen remodels, bath additions, HVAC "upgrades" for sale, pools.

## Common Pitfalls

1. **Confusing payoff with balance.** Payoff adds per-diem interest and can include escrow shortages; HELOCs must be frozen/zeroed — request official payoff letters, not app guesses.
2. **Forgetting the solar panel contract.** Leases/PPAs attach to the house; buyers can walk or demand payoff ($10–25k surprise). Locate the paper before listing.
3. **Missing transfer tax stacking** (state+county+city). Budget from the table, verify locally.
4. **Skipping improvements in basis.** The $40k kitchen and $15k roof in 2021 cut the taxable gain by $55k. Sellers without records overpay tax every day.
5. **Assuming the 2-of-5 test on technicality.** A 2019-2023 rental + 2024 move-back for 8 months usually FAILS the use test — partial exclusion only if work/health safe harbor applies.
6. **NIIT blindness.** Gain above the exclusion at high income (MAGI > $200k single/$250k MFJ) picks up 3.8% surtax on top of LTCG.
7. **Moving costs** aren't deductible for employees (post-TCJA through 2025); self-employed relocating for work partially are. Budget them as pure cash out.
8. **Rent-vs-sell on gross yield.** $2,800 rent on a $450k house is not "7.4% return" — vacancy, taxes, insurance, maintenance, management eat 35–45% of gross. The script computes NOI properly.

## Verification Checklist

- [ ] Every proceeds line item listed with a $ or explicit 0 — no silent omissions
- [ ] Payoff modeled with per-diem interest, payoff date noted
- [ ] Transfer tax flagged as state+local stacking, verified against the actual county
- [ ] Solar lease/PPA and HELOC existence explicitly asked
- [ ] Exclusion eligibility: both tests checked with dates; partial-proration shown if applicable
- [ ] Improvements list requested for basis (capital vs repair distinction applied)
- [ ] Depreciation recapture flagged for any rental history
- [ ] Rent-vs-sell (if asked) uses NOI/cap-rate, not gross yield

## One-Shot Recipe

```bash
# 720k offer on a home bought 380k with 90k improvements, 210k mortgage left
python3 scripts/proceeds.py estimate --price 720000 --payoff 210000 \
  --commission 5.5 --state GA --improvements 90000 --purchase 380000
# → line-itemed net proceeds + gain 235k → excluded (MFJ under 500k) → tax 0

# rent-vs-sell first pass
python3 scripts/proceeds.py rent-vs-sell --price 720000 --net-proceeds 480000 \
  --rent 2800 --taxes 4800 --insurance 1400 --maintenance-pct 1.5
```
