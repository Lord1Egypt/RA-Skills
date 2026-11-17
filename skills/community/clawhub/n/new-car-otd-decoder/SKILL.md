---
name: new-car-otd-decoder
description: "Use when reviewing a new-car purchase quote, lease deal, or 'out-the-door' price. Audits OTD line items (doc fees vs state caps, taxed rebates, dealer add-on padding), decodes lease money factor into real APR, and compares financing against a pre-approved loan."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [car-buying, otd, lease, money-factor, negotiation, auto]
---

# New-Car OTD Decoder — Out-The-Door Quote Forensics

## Overview

A new-car "out-the-door" price is a stack of legitimate charges, state-capped fees, and pure dealer
padding. Sales tax on rebates varies by state; documentation fees range from a $75 cap in some
states to uncapped $500+ elsewhere; add-ons like "VIN etching" ($1495 for a $0 product) ride the
final worksheet because buyers are exhausted by then. Leases hide the real interest rate behind a
"money factor" that almost nobody converts to APR.

This skill takes a quote (paste of line items, or structured input) and returns an itemized audit:
every line classified **FAIR / CAPPED-BY-LAW / PADDED / REFUSE**, total padding found, corrected
OTD, lease money-factor → APR decode, and financing comparison vs a pre-approved rate.

## When to Use

- User shares a new-car purchase worksheet, OTD quote, or "drive-off" lease numbers
- Comparing lease vs buy, or dealer financing vs bank pre-approval
- A deal includes mandatory add-ons ("pro pack", ceramic coating, paint protection)
- Verifying that a quoted monthly payment actually matches the stated price and APR
- Don't use for: used-car condition/mileage audits (that's inspection territory), trade-in valuation
  alone, or rideshare/rental topics

## Core Knowledge

### 1. Anatomy of an honest OTD

```
OTD = negotiated price (or capitalized cost on a lease)
    - rebates / incentives / trade credit
    + sales tax (on the CORRECT base — see §2)
    + title & registration (state schedule — fair, non-negotiable)
    + doc/documentary fee (state-capped in many states — see references)
    + ANY gov-mandated fees (tire fee, battery fee, emissions — small, legit)
    + NOTHING ELSE
```

Anything past that — "dealer services", "market adjustment", "pro pack", "surface protection",
"VIN etch", "nitrogen fill" — is padding. Fair value of every classic add-on is in
`references/addon-catalog.md`; nearly all are worth $0–$50, not the $295–$1995 charged.

### 2. Sales tax on rebates — state dependent

- **Most states tax price AFTER manufacturer rebates** (rebate reduces taxable base).
- **Tax-on-rebate states (rebate is taxable income to you):** TX, and several others — see the
  table in `references/state-rules.md`. In tax-on-rebate states a $3000 rebate saves you less than
  $3000 + tax math suggests; the worksheet must show tax computed on the pre-rebate price.
- Trade-in credit reduces taxable base in most states, but **NOT** in CA, DC, HI, MI, VA and a few
  others (tax paid on full price even with a trade).

### 3. Lease decode — money factor is a disguised APR

```
rent charge uses MF where APR ≈ MF × 2400
monthly = (cap_cost − residual) / term  +  (cap_cost + residual) × MF
```

Checks that catch real deals:
- Quote MF × 2400 and compare to stated/known APR. Dealer-marked-up MFs (buy-rate + 0.0002–0.0004)
  add $9–$18/month per $10k of cap cost — pure profit.
- Drive-off must be decomposed: 1st payment + cap reduction + acquisition fee + DMV. A big "down"
  on a lease (cap cost reduction) is uninsured cash — if the car is totaled, you don't get it back.
- Missing disclosures: residual $, MF, acquisition fee, disposition fee, mileage cap, per-mile
  overage rate. Any refusal to show the MF is a walk-away.

### 4. Financing sanity

Compute payment from principal/rate/term (amortized). If dealer payment > formula payment, the gap
is markup (rate bump) or a hidden fee. Dealer "buy rate" markup of 1–2% APR is standard practice
unless the lender caps it.

## Workflow

1. **Collect the quote** — every line item with $ amounts, state, and whether cash/finance/lease.
   Get the *itemized* worksheet, never just a monthly payment or "OTD: $41,995".
2. **Run the audit:**
   ```bash
   python3 scripts/otd_decoder.py --demo                 # see the shape
   python3 scripts/otd_decoder.py --quote quote.json     # real audit
   ```
   (build `quote.json` from `scripts/quote.example.json`.)
3. **Read the verdict table**: total padding, corrected OTD, per-line REFUSE list.
4. **Lease?** Feed MF/term/residual/cap — get effective APR + payment verification + the markup
   vs a 0.00040-bump estimate.
5. **Financing?** Feed price minus rebates, rate offers — get payment comparison and total interest.
6. **Counter** using the scripts in `references/negotiation-playbook.md`: email-only OTD requests,
   "out-the-door or nothing" language, the add-on refuse list wording.

## Verdicts the script returns

| Verdict | Meaning |
|---|---|
| FAIR | Market-real (e.g., a genuine discount off MSRP) |
| STATE-CAPPED | Legal fee at/below cap (verify against references) |
| OVER-CAP | Doc fee above your state cap — demand reduction to cap |
| PADDED | Real product, cartoon price — counter at fair value |
| REFUSE | $0-value item (VIN etch, nitrogen, surface protection) |

## Common Pitfalls

1. **Negotiating monthly payment instead of OTD.** Payment games hide term/rate/APR. Always
   negotiate the single OTD number; financing is a separate conversation.
2. **Forgetting tax-on-rebate states.** In TX-class states, a $3,000 rebate ≈ $3,000 minus your
   tax rate applied to that $3,000 back — rebates are less valuable than sticker math suggests.
3. **Cap-cost reduction on a lease.** Big drive-off cash is uninsured. Keep drive-off to first
   payment + fees; roll the rest into the cap cost.
4. **Trusting the "money factor is not negotiable" line.** MF is rate markup-able AND negotiable —
   especially with manufacturer subvented lease programs (check the subvention MF before markup).
5. **Add-ons framed as "already installed."** Anything pre-installed can be refused or charged at
   fair value; "we can't remove it" → "then I'm not paying for it" (see playbook).
6. **Doc fee "we can't change it."** True in cap states at the cap — but the discount can absorb it
   elsewhere. In uncapped states it's negotiable like any other line.

## Verification Checklist

- [ ] Every quote line classified with a verdict and a reason
- [ ] Corrected OTD computed (quote total − REFUSE − PADDED-overflow)
- [ ] Lease: MF × 2400 stated as effective APR, payment re-derived from formula, matches quote ±$2
- [ ] Financing: payment from amortization formula matches quoted payment ±$1
- [ ] State column checked: doc-fee cap, rebate taxation, trade-in taxation
- [ ] User leaves with: corrected OTD + refuse list + one counter-email draft

## One-Shot Recipe: "they quoted $2,495 of add-ons"

Quote shows: Surface protection $495, VIN etch $1,495, all-weather mats $495, nitrogen $210.
Audit → REFUSE surface protection (dealer's own cost ≈ a $15 bottle), REFUSE VIN etch (insurance
companies give the discount without it; etch kits cost ~$20), PADDED mats (counter $150–200 — real
product), REFUSE nitrogen (air is 78% N₂; zero measurable benefit for street cars).
Total corrected: −$2,390. Mats stay at $180: corrected OTD ≈ quote − $2,100.
