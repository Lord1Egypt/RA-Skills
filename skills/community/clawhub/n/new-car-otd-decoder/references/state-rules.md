# State Rules — Doc-Fee Caps, Rebate Taxation, Trade-In Taxation

> Always verify current numbers with the state DMV/revenue site — caps and tax rules change.
> This table is the decision map: WHICH questions to ask, with typical 2020s-era values.

## Documentation ("doc") fee caps (typical)

| Regime | States (examples) | Typical cap |
|---|---|---|
| Hard caps ~$75–$100 | CA ($85), ND, NH, MN, SC (~$60 cap-ish by practice), AR | $60–$100 |
| Mid caps $150–$300 | FL (~$300 sliding), WA, OR (~$150 region), CO, NE, KS, IA, MO, OK, WV | $150–$300 |
| Higher / uncapped | NY ($175 by law incl. some), TX (uncapped, market ~$225–$350), GA ($~ documentation unlimited, title fees fixed), PA, NJ, MI, OH (market ~$250–$450), IL | $250–$500+ |
| No doc fee allowed | MD (banned — title charges only) | $0 |

**Action:** classify the doc fee line as STATE-CAPPED if ≤ cap (then it is what it is — absorb it
in the negotiated price), OVER-CAP if above (demand reduction to cap; it's regulated).

## Sales tax on manufacturer rebates

| Rule | States (examples) | Meaning |
|---|---|---|
| Rebate NOT taxed (tax on net) | Most states: e.g., NY, IL, PA, OH, GA, NC, FL, AZ, CO, MA, VA, WA, NJ … | Tax base = price − rebates. Rebate saves full amount + its tax |
| Rebate TAXED (tax on gross) | **TX**, **NM**, **OK (partial regimes)**, and a few others | Tax base = price BEFORE rebate. A $3,000 rebate in a 6.25%+local (≈8.25%) TX deal is worth ≈ $3,000 − $0 (you save 3k but still pay ~$248 tax on it) |

Verify the worksheet's tax line: `tax_base` should equal price-minus-rebates in net-tax states,
price-before-rebates in gross states.

## Trade-in taxation (does trade value reduce the tax base?)

| Rule | States (examples) | Meaning |
|---|---|---|
| Trade credit reduces tax | Most states | Selling privately LOSES the tax benefit; trading is tax-advantaged |
| **No** trade credit | **CA, DC, HI, MI, VA** (and a few city regimes) | Trade-in value does NOT reduce sales tax; sell privately with no tax penalty (check VA local add-ons) |

## Legit non-negotiable government fees (typical ranges)

- Title: $5–$150 · Registration: $30–$400 (vehicle-value- or weight-based) · Plate transfer: $5–$30
- Tire/battery disposal: $1–$15 · Emissions (where applicable): $15–$40 · EV registration
  surcharge: $50–$250/yr in many states (real — factor into EV math)

## Lease-specific state items

- Tax on lease payment vs. tax on full price up front varies (e.g., IL historically taxed the full
  cap cost at signing; TX taxes full selling price on leases; most states tax the payment stream).
- One-pay leases can dodge per-payment taxes in some states — flag but verify.

## Negotiation quick math the states enable

1. Net-rebate state + trade-credit state: OTD = (price − rebates − trade) × tax% + fees. Push
   rebates AND trade into the base reduction.
2. Gross-rebate state: consider taking the rebate as cash-down alternative vs. a dealer "loyalty
   discount" — a $3,000 discount beats a $3,000 rebate in tax terms by rebate×tax%.
3. No-trade-credit state: get the trade priced honestly, then sell privately at +8–15% with zero
   tax downside.
