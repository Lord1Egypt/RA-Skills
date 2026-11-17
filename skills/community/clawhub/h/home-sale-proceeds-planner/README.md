# Home Sale Proceeds Planner

**The problem.** Sellers fixate on the sale price and get blindsided by the settlement statement. Between accepted offer and wire transfer, 6–10% evaporates: commissions (5.5% on a $720k sale = $39,600), title/escrow, transfer taxes (1% in Georgia, ~2.4% stacked in Chicago), mortgage payoff with per-diem interest, prorations, credits. The number that matters — *the wire hitting your account* — is a calculation nobody does until escrow sends the CD. Then the tax layer: sellers without improvement records overpay capital-gains tax every day, and sellers with rental history get surprised by depreciation recapture that the $250k/$500k exclusion explicitly does not cover.

**What this does.**

- **`estimate`** — full line-itemed net proceeds (commissions, closing costs, state-aware transfer tax, payoff + per-diem interest, HELOC, credits, prorations), then the tax layer: adjusted basis including your capital improvements and selling costs, Section 121 exclusion applied with the 2-of-5-year ownership+use tests run from actual dates, depreciation recapture carved out, NIIT flagged
- **`exclusion`** — standalone eligibility check: ownership test, use test with the 5-year lookback window math, prior-sale-within-2-years bar, partial-exclusion safe-harbor pointer (the 2019–2023 rental + short move-back case that fails the use test at 22 months)
- **`rent-vs-sell`** — honest first pass: NOI after vacancy/maintenance/management/taxes/insurance (a $2,800/mo rental on $720k is a 3.1% cap rate, not "4.7% return"), compared against net proceeds at a safe yield

**Example.** $720k offer, bought $380k with a $90k kitchen, $210k mortgage, married, Georgia: net proceeds $458,204 (63.6% of price — the number to plan the next down payment around), gain $198,480, exclusion applies (103 months owned, use test passed), federal tax $0. Same sale with the improvements forgotten: gain $288k, still excluded — but a California single seller at $900k gain pays ~$51k+ in tax where $90k of receipts would have cut it.

## Quick start

```bash
python3 scripts/proceeds.py estimate --price 720000 --payoff 210000 --commission 5.5 \
  --state GA --purchase 380000 --improvements 90000 --married \
  --owned-from 2018-05-01 --moved-in 2018-05-01
python3 scripts/proceeds.py exclusion --sold-on 2026-11-01 --owned-from 2019-06-01 \
  --moved-in 2019-06-01 --moved-out 2023-09-01
python3 scripts/proceeds.py rent-vs-sell --price 720000 --net-proceeds 480000 \
  --rent 2800 --taxes 4800 --insurance 1400
```

## Files

- `SKILL.md` — net-proceeds model, exclusion gate checks, credit-vs-repair doctrine, pitfalls
- `references/seller-settlement-math.md` — closing-cost tables, basis mechanics, Section 121 edge cases, tax-rate stacking, payoff checklist, wire-fraud warning
- `scripts/proceeds.py` — estimator/exclusion-checker/rent-vs-sell (stdlib only)

## Not for

1031 exchanges, short-sale/foreclosure debt-forgiveness tax, non-US tax systems — flagged when applicable, needs a specialist.

## License

MIT © 2026 Denis Voronin
