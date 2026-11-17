# Big Purchases — Can You Afford It, and What Does It Really Cost

**Before answering**, read `## Money Shape` and `## Goals` in `~/Clawic/data/money/memory.md`, and check `~/Clawic/data/money/decisions/<year>.md` — this exact purchase may already have been decided against, and re-deciding it from scratch is how a rejected purchase eventually gets made.

## The Affordability Test

A purchase is affordable when all four hold. Three out of four is a deferral, not a purchase.

1. **The buffer survives it.** Paying for it leaves `emergency_fund_months` intact (`emergency-fund.md`).
2. **The running cost fits.** `(finance payment + running cost) ÷ net monthly income` is inside what the budget carries at the stress case, not the good month.
3. **It does not displace a funded ladder step.** Name what it takes money from (Rule 8) — if the answer is "the savings rate", say the new savings rate out loud.
4. **The replacement is already funded.** A car, a boiler or a laptop bought without a sinking fund for the next one is a purchase made twice (`budget.md`).

The price is the deposit on the running cost. That is the sentence that changes decisions.

## Total Cost of Ownership

`TCO = purchase price − resale value at exit + running costs over the holding period + finance cost`

Per year: `TCO ÷ years held`. Run it before comparing options, because it routinely reverses the ranking that the sticker prices suggest.

| Purchase | The costs people leave out |
|---|---|
| Car | Insurance, fuel or charging, tax, servicing, tyres, parking, depreciation — usually the largest single item and the one never counted |
| Home renovation | Contingency (15-20% is a working minimum on a fixed-price quote, more on an old building), permits, temporary accommodation, the finish nobody budgeted, the disruption to income |
| Wedding | The guest-count multiplier: most line items scale per head, so a guest-list decision is the budget decision |
| Boat, second home, horse, pool | Fixed annual costs that continue whether used or not; usage rarely matches the projection made at purchase |
| Education | Fees plus foregone income plus the years of contributions not made; against the earnings differential, honestly estimated |
| Laptop, phone, appliance | Resale value at exit — a device with a strong second-hand market can have a lower TCO at twice the price |
| Pet | Lifetime veterinary costs and end-of-life care, which arrive as unbudgeted four-figure events |

## Cars, Specifically

The largest discretionary purchase most households repeat.

- **Depreciation is the cost.** New cars lose the steepest part of their value in the first two to three years, which is why buying at two to three years old and holding transfers that loss to someone else. The counter-case is a warranty, a known history and, for some electric models, finance or tax incentives that only apply new — price those explicitly rather than assuming either side.
- **Buy, finance or lease** — compare on TCO per year, never on monthly payment. Leasing is renting: predictable, no residual risk, no asset at the end, and expensive if you keep cars a long time. Buying outright is cheapest per year for a long holder. Finance sits in between and is priced by the rate.
- Balloon-payment structures (PCP and equivalents) are quoted as a low monthly payment with a large optional final payment. The monthly figure is not the cost; the cost is total payments + balloon − resale value. Ask for the total amount payable, which most jurisdictions require to be disclosed.
- The car is an entity in its own right: if the user has the `car` skill, the vehicle, its registration and its service history live in that skill's shared `~/Clawic/data/vehicles/` box and this skill never writes there. Keep only the money side — the loan in `finances/accounts.md`, the running costs in the budget — and name the car by model and plate.

## Finance Offers, Priced Honestly

- **0% finance is not free if there is a cash discount.** The forgone discount is the interest. Effective rate ≈ discount % ÷ (years of the term ÷ 2) as a first approximation; ask for the cash price before mentioning finance.
- Where the cash price is identical, 0% finance is genuinely free money in an inflationary period, and taking it while the cash earns interest is correct. Both cases exist; the question is only ever "what is the cash price".
- Interest-free periods that revert: know the revert rate and the date, and set the clearing schedule as balance ÷ months before signing (`debt.md`).
- Add-ons sold at the point of sale — paint protection, gap insurance, extended warranty, payment protection — are priced for the moment of commitment. Decide on them a week later, separately, or not at all (`insurance.md`).
- Finance for a depreciating asset over a term longer than its useful life guarantees negative equity in the middle. Match the term to the life.

## The Behavioural Controls

These are cheap, they work, and they are the reason this file exists at all:

- **Cooling-off**: 72 hours for anything above a threshold the user sets, a week above a larger one. Almost nothing legitimate expires in that window, and something that does is a sales tactic (`scams.md`).
- **Price the recurring commitment as its annual total.** "40 a month" is 480 a year and 2,400 over five.
- **Sleep on the upgrade, not just the purchase.** The decision to buy is usually sound; the trim level, the extra room and the larger model are where the money goes.
- **Sunk cost has no vote.** Money already spent on the current item, or on deposits and research for the new one, does not belong in the decision. The only question is what happens from here.
- **The comparison is not against the best version, it is against not buying.** Retail framing always compares options within a purchase; the missing option is the status quo, and it costs nothing.
- **One large purchase at a time.** Two overlapping commitments is how a well-run budget becomes a debt problem inside a year.

## When A Big Purchase Is The Right Answer

The bias in this file is toward deferral, so state the other side plainly. A purchase is right when it removes a recurring cost or a risk: a repair that stops an escalating failure, a tool that replaces a rented one, a car that ends a commute the household is paying for in another currency, an appliance whose running cost is materially lower, professional treatment deferred long enough to get expensive, or equipment that raises income (`income.md`). Price those as an investment with a payback period: `payback months = cost ÷ monthly saving`. Under 24 months, it is usually a straightforward yes.

**Write it down.** The decision, the amount, the alternative rejected and what would change it goes as a row in `~/Clawic/data/money/decisions/<year>.md`; the TCO working, if it took real analysis, is an artifact at `~/Clawic/data/money/artifacts/decision-<kebab>.md` with its `## Boxes` line in the same turn. Any finance taken becomes a row in `~/Clawic/data/finances/accounts.md` with its rate and term, and its replacement sinking fund goes to `~/Clawic/data/finances/budget.md`. The vehicle itself is not money data and is not written here: where the `car` skill is installed the entity lives in its `~/Clawic/data/vehicles/` box, and this skill only names the car. Format in `memory-template.md`.
