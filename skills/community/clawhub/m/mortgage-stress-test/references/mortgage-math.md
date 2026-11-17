# Mortgage Math — Full Reference

## 1. Monthly principal & interest
```
r = APR / 12          (monthly rate)
n = term_years * 12
M = P * r * (1+r)^n / ((1+r)^n - 1)
```
Sanity anchor: $405,000 at 6.5%/30yr → r=0.0054167, (1+r)^360 ≈ 6.992 → M ≈ $2,560.

## 2. The full monthly stack ("PITI + M + maint")
| Component | How to estimate | Typical range |
|---|---|---|
| Principal & interest | formula above | — |
| Property tax | tax_pct × price / 12 | 0.3–2.5%/yr by state/county (US) |
| Homeowner insurance | quote, or 0.25–0.5%/yr | $1,200–$4,000/yr median US |
| PMI | 0.5–1.5% × loan / 12 while LTV > 80% | 0.5% ≈ "good credit", 1.5% ≈ lower credit |
| HOA/condo fees | listing | $0–$800+/mo |
| Maintenance | 1%/yr of price (1.5–2% if pre-1980 or big lot) | often forgotten, always due |

PMI exit estimate: find the first year where (balance − appreciation-based home value
gap) gives 20% equity on the *original* value path, then stop charging. In practice,
request PMI cancellation in writing at 20% original-value equity (automatic at 78% LTV
of original schedule under the Homeowners Protection Act, US).

## 3. Affordability gates
- **Front-end DTI** = true housing cost / gross monthly income. Target ≤ 28%.
- **Back-end DTI** = (housing + all debt service) / gross income. Target ≤ 36%
  (conservative), 43% is typical lender max, 50% is FHA-ish ceiling — at those levels
  there is no room for saving or shocks. FAIL if > 36 unless other assets cover it.
- **50/30/20 sanity**: at the true monthly cost, does at least 20% of *net* income
  still go to savings/retirement? If not, the house is too big.

## 4. Rate shock (ARM / refinance / regret test)
Recompute the payment at +1% and +2%. On a $405k loan, +2% (6.5→8.5%) moves P&I from
~$2,560 to ~$3,123 (+$563/mo). Rule: if the +2% payment breaks back-end 36%, do not
take the ARM / consider the fixed.

## 5. Rent vs buy — honest break-even
Compare two wealth paths at horizon y (years):

**Buy path wealth(y):**
```
equity = home_value(y) − balance(y)          home_value(y) = price × (1+apprec)^y
exit_cost = 0.065 × home_value(y)            (6-7% round-trip selling)
paid = down + closing + Σ monthly_own(y)     (all months, incl. PMI until exit)
buy_wealth = equity − exit_cost − paid − opp_cost(down+closing @ invest_return, y)
```

**Rent path wealth(y):**
```
rent_paid = Σ rent(y)  (rent grows 3%/yr by default)
invested  = (down + closing) grown at invest_return
+ monthly difference (rent_month − buy_month) invested monthly at invest_return
rent_wealth = invested_portfolio − rent_paid
```
Break-even year = first y where buy_wealth − rent_wealth > 0.

Typical results at 3% appreciation / 6% investment return: break-even ≈ 3–6 years.
At 0% appreciation, often **never** within 30 years in high-tax markets — that is a
finding, not a bug.

## 6. Down payment dilemmas
- 20% down kills PMI but empties the emergency fund → model maintenance shock risk.
- Smaller down + invested difference can win if investment return > effective mortgage
  cost after tax deduction; but only with disciplined investing of the difference.
- Never model the mortgage interest deduction at full value: it only helps to the
  extent itemized deductions exceed the standard deduction.

## 7. Honest caveats
- Property tax reassessment on sale (e.g., California Prop 13 reset) can double taxes
  vs the seller's bill — look up the *assessed* rate, not the seller's payment.
- Escrow shortages in year 2 (tax/insurance re-estimate) raise the payment 5–10%.
- New-construction HOAs rise after developer handover.
- This is a planning instrument, not a loan offer; rates/fees come from the lender's
  official Loan Estimate (check the APR line, page 1, and Section A–C fees).
