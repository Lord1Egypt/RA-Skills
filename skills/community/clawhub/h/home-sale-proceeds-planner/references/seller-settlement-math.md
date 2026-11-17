# Home Sale Proceeds — Engineering Reference

## 1. Where the money goes (national midpoints, 2026 shape)

| Line | Typical | Notes |
|---|---|---|
| Buyer-agent commission | 2–3% | post-2024 NAR settlement: negotiated, written agreements, NOT "standard" anymore |
| Listing commission | 2–3% | flat-fee and discount models now common |
| Title insurance (owner policy) | 0.4–0.8% | paid by seller in some regions, buyer in others |
| Settlement/escrow fee | $500–1,500 | |
| Attorney (attorney states: NY, MA, SC, GA, DE...) | $750–1,500 | |
| Transfer tax | 0–2%+ | see SKILL table; county/city stack (Chicago: 0.75+1.05+0.25 potential) |
| Recording/misc | $100–400 | |
| Mortgage payoff + per-diem | balance + interest to funding | payoff letters valid ~10–30 days |
| Property-tax proration | region-timed | seller credit if prepaid; debit if arrears (most) |
| HOA estoppel/resale cert | $100–500 | FL/CO/TX communities |
| Survey (if required) | $400–800 | often reuse existing |
| Home warranty concession | $350–650 | |
| Courier/wire fees | $50–150 | |

**All-in seller cost:** ~7–9% incl. commissions, ~1.5–3% without.

## 2. Basis mechanics (the audit-proof version)

```
adjusted_basis = purchase_price
               + capital_improvements        (roof, HVAC, remodel, addition, fencing, driveway)
               + major systems upon purchase (if capitalized, not repaired)
               + selling_expenses            (commissions, title, transfer tax, attorney, staging)
gain           = sale_price − adjusted_basis
```

- Improvements must be **capital**: betterment, restoration, adaptation, or >1-year life. Repairs (paint, leaks, caulking) are NOT added — unless done as part of a renovation project that is itself capital.
- Safe-harbor records: receipts + before/after photos + permit copies. Without records, IRS permits "reasonable reconstruction" — but the burden shifts to you.
- Energy credits (25C/25D) claimed earlier reduce the improvement basis by the credit amount.

## 3. Section 121 in practice

- Tests run on the **sale date** (closing), not listing.
- Ownership and use can overlap and be nonconsecutive (24 total months within 60).
- Married filing jointly: either spouse meets ownership + BOTH meet use (or each qualifies on different homes only via complicated rules — see Pub 523 for the "one home each" trap).
- Gain allocation order: exclusion applies to qualifying gain FIRST; depreciation recapture is carved out and taxed (≤25% federal) regardless.
- Nonqualified use (rental after 2008, before re-occupancy): gain prorated:
  `nonqual_fraction = nonqual_days / total_ownership_days` → that slice of gain is taxable (no exclusion), the rest can be excluded.
- Safe harbors for partial exclusion (work ≥50 mi, health, unforeseen — death, divorce, disaster, multiple birth): `exclusion × (qualifying months / 24)` — with 12 months of qualifying use you get half.
- Repeated use: one exclusion per 2-year rolling window.
- House → rental conversion: up to 3 years of rental AFTER last primary use doesn't create nonqualified use (the "convert and keep the exclusion" window) — but depreciation still recaptures.

## 4. Tax rates on excess gain (2026 shape)

| Layer | Rate |
|---|---|
| Depreciation recapture (unrecaptured §1250) | up to 25% |
| LTCG (most sellers with excess gain) | 15% (20% at high income) |
| NIIT surtax | +3.8% if MAGI > $200k/$250k |
| State | 0% (TX/FL/WA...) to ~13% (CA, taxes as income) |

Excess gain often stacks: e.g., MFJ with $650k gain → $500k excluded → $150k at 15% + possible NIIT + state.

## 5. Credit-vs-repair math

- Post-inspection credits shift execution risk to the buyer's contractor — sellers accept ~5–10% discount for that (i.e., a $10k credit vs an $11k repair).
- Credits count toward buyer closing-cost caps by loan type (FHA/VA/Conventional differ; VA caps are strict) — oversized credits get trimmed at underwriting; keep a repair fallback.
- Pre-sale ROI (resale value per $1 spent, typical): interior paint $1.2–1.5; flooring repair $1.1–1.3; staging $1.1–1.5 (on vacancy); kitchen refresh (paint/hardware) $1.0–1.2; full kitchen remodel $0.5–0.7; bath remodel $0.55–0.7; roof replacement $0.6–0.8 (but faster sale); pool negative.
- Get a pre-listing inspection ($350–600): converts post-inspection renegotiation leverage into priced-in listing strategy. The buyer's inspector WILL find the roof issue; better you disclosed it first.

## 6. Payoff requests — checklist

1. Request written payoff from every servicer (1st, 2nd/HELOC) — include per-diem rate and "good through" date.
2. HELOC: request freeze; any balance at closing is paid from proceeds — verify no trailing draws.
3. Solar lease/PPA/loan: UCC filing must release; lease transfer needs buyer credit approval — start 30+ days early; loan balances ($10–25k) come out of proceeds if required.
4. Property-tax proration: which side of the installment date? County schedule decides credit vs debit.
5. Escrow refund (taxes/insurance held by servicer) arrives 2–4 weeks AFTER closing — not in the wire, but it's yours; don't forget it in the plan.

## 7. Rent-vs-sell honest layer

- NOI formula (script): gross − vacancy − maintenance (1–2%/yr of value) − management (7–10% unless self-managing: then price your time) − taxes − insurance − HOA.
- Cap rate < 4% = appreciation bet. 4–6% = thin. 6%+ = real estate is doing work (rare in 2026-price markets with current rates).
- Compare to: net proceeds × after-tax safe yield (T-bills/CDs ~4%ish, or index-dividend ~3.5%). Add appreciation − selling-cost drag − tenant-risk premium before concluding.
- One-number sanity: if (rent × 12 × 0.55) / price < mortgage-rate-free alternative yield, selling usually wins the income lane.

## 8. Wire fraud warning (a real 2026 problem)

Closing-day wire instructions emailed "updated" = fraud attempt standard. Call the title company at a KNOWN number to verify instructions before sending; wire only to verified accounts. Sellers receiving proceeds: same discipline in reverse.
