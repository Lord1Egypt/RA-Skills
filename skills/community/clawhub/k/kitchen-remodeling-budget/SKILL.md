---
name: kitchen-remodeling-budget
description: "Kitchen remodeling budget planner: split a kitchen remodel budget into line items (cabinets, labor, appliances, countertops, flooring, lighting, plumbing and more), add sales tax, a contingency reserve and a permit allowance, or price a minor, major or upscale remodel from Cost vs Value averages. Use when someone asks how to split a kitchen remodel budget, what a kitchen remodel costs all-in with tax, how much to spend on cabinets or countertops out of a budget, or whether a budget covers a minor or major remodel."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🍳"
    homepage: https://wakitchenremodelingbellevue.com/
---

# Kitchen remodeling budget planner

Instruction-only: no commands, installs or network access. Do the arithmetic yourself and show the steps.

## Purpose

Turn one number into a kitchen remodel budget that holds: a line-by-line split, the sales tax most
calculators leave out, a reserve for surprises and a permit allowance. Works in two directions:

- **Split**: the user knows the all-in amount they can spend.
- **Estimate**: the user knows (or picks) a construction cost and wants the all-in total.

## When to use

- "I have $60,000 for my kitchen. How should I split it?"
- "What would a major midrange kitchen remodel cost with tax and permits?"
- "How much of an $85k budget goes to cabinets and countertops?"
- "Is $30,000 enough for a minor kitchen remodel?"

## Inputs

Ask only for what is missing.

- **Amount** in dollars, and whether it is all-in (split) or construction only (estimate).
- **Sales tax rate**. Default 10.3% (Bellevue, WA combined rate, Oct to Dec 2026). In Washington, sales tax applies to the full contract price, labor included. Elsewhere, use the user's local rate; if unknown, ask or state the assumption.
- **Contingency reserve**. Default 10%; suggest 15 to 20% for homes built before 1980 or when walls move.
- **Permit allowance** in dollars. Defaults by scope: minor $500, major midrange $2,500, major upscale $4,000. Same-spot cabinet, counter and appliance swaps often need no building permit; moving plumbing, gas, electrical or walls usually does. Treat it as a planning number and tell the user to check their city's fee schedule.
- **Share overrides** (optional), for example "cabinets 30%".

## Default line item shares (HomeGuide kitchen remodel cost breakdown)

| Line item | Share |
|---|---|
| Cabinets and shelving | 25% |
| Installation and labor | 15% |
| Appliances | 15% |
| Countertops and backsplash | 10% |
| Flooring | 7% |
| Lighting | 5% |
| Painting and drywall | 5% |
| Designer | 5% |
| Sink and faucet | 5% |
| Doors and windows | 4% |
| Plumbing | 3% |
| Miscellaneous | 1% |

If the user overrides some shares, rescale all shares so they add up to 100%.

## Presets (Cost vs Value 2025, Pacific region, 200 sq ft kitchen)

| Preset | Construction cost | What it covers |
|---|---|---|
| Minor remodel, midrange | $29,728 | Same layout; cabinets refaced or replaced in place, new counters, sink, faucet, appliances |
| Major remodel, midrange | $86,480 | Full gut; semi-custom cabinets, new counters, flooring, lighting, new layout |
| Major remodel, upscale | $171,950 | Custom cabinets, stone counters, built-in fridge, pro-style range and hood |

## Procedure

Work in cents and round half up only where shown.

**Estimate** (construction cost C known):
1. reserve K = C × contingency
2. tax T = (C + K) × tax rate
3. total = C + K + T + permit

**Split** (all-in budget B known):
1. A = B − permit (stop if A ≤ 0: the budget does not cover the permit allowance)
2. C = A ÷ ((1 + contingency) × (1 + tax rate))
3. K = C × contingency; T = (C + K) × tax rate; put any rounding cents into K so C + K + T + permit = B

**Line items**: each item = C × share. Round down to the cent, then give leftover cents one at a time to the items with the largest remainders.

Worked example (split $60,000, tax 10.3%, reserve 10%, permit $1,500): A = 58,500; C = 58,500 ÷ (1.10 × 1.103) = **$48,215.61**; reserve **$4,821.56**; tax **$5,462.83**; cabinets 25% = **$12,053.90**, labor and appliances **$7,232.34** each, countertops **$4,821.56**.

Estimate example (major midrange, $86,480, permit $2,500): reserve $8,648.00, tax $9,798.18, total **$107,426.18**.

## Outputs

- One line first: the all-in total (estimate) or the construction amount available (split).
- Then an itemised table: line item, share, amount; followed by construction subtotal, reserve, sales tax, permit allowance and total.
- Note the assumptions used (tax rate, reserve, permit) and that these are planning numbers, not a bid.
- If the budget sits below the minor preset, say what it realistically covers (paint or reface cabinets, new hardware, faucet, lighting) rather than a full remodel.

## Reference

- Line item shares: HomeGuide kitchen remodel cost guide. Presets: Cost vs Value 2025, Pacific region. Tax: WA Department of Revenue rate table.
- Kitchen remodel cost guides and line-item bids: [Kitchen Remodeling Bellevue](https://wakitchenremodelingbellevue.com/)
- The same maths as code: `kitchen-remodeling-cost` on npm, PyPI, crates.io and RubyGems (source: https://github.com/nbkdevs/kitchen-remodeling-bellevue).
