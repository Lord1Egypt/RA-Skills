# Housing — Rent, Buy, Borrow, Move

**Before answering**, read `## Goals`, `## Money Shape` and `## Debt Plan` in `~/Clawic/data/money/memory.md`, plus `artifacts/decision-rent-vs-buy.md` if `## Boxes` lists it. This decision gets re-argued every time prices move; the written analysis exists so the argument starts from the numbers already agreed.

Housing is the largest line in most budgets and the largest leveraged position most households will ever take. Everything here is a money question; the property-as-investment case is `real-estate-investing`.

## Rent Versus Buy Is A Horizon Question

Owner-occupied housing is consumption bought with leverage. The honest advantages are forced saving, security of tenure, control of the space, and housing costs that stop tracking market rents. None of those appear in a return calculation, and all of them are real.

The number that decides it is the **round-trip transaction cost** against the **expected stay**.

Round trip = buying costs (transfer tax or duty, notary and registration, legal, survey, mortgage arrangement) + selling costs (agent commission, legal, any early-repayment charge). In many markets the pair totals 8-12% of the price; in a few it is under 5%; verify for `country` before quoting, because the whole answer turns on this figure.

Break-even years ≈ round-trip cost ÷ (annual cost of renting − annual cost of owning), where owning costs are mortgage interest (not principal — that is saving), property tax, buildings insurance, service charges, and maintenance. **A commonly used planning figure for maintenance is around 1% of property value a year**; verify it against the actual building, because an old house or a block with a major-works liability runs far above it.

Rule of thumb that falls out of the arithmetic: below roughly five years of expected stay, renting usually wins on money in a normal-cost market; above seven, buying usually does. Between them the answer is decided by whether the household wants tenure security more than flexibility.

What is **not** an argument: "rent is dead money". Interest, transaction costs, maintenance, insurance and property tax are equally dead — the only part of a mortgage payment that builds anything is the principal, and in the early years of an annuity mortgage that is the small part.

## What The Lender Will Lend, And What You Should Borrow

| Test | Lender's convention | What it means for you |
|---|---|---|
| Housing costs ÷ gross income | ≤28% | A ceiling on what can be borrowed, not a target |
| Total debt service ÷ gross income | ≤36%, sometimes up to 43% | A household at the ceiling has no room for a rate rise or an income drop |
| Loan to value | Pricing tiers, commonly stepping at 90%, 80%, 75%, 60% | Crossing a tier downwards can cut the rate materially — sometimes worth more than the extra deposit costs elsewhere |
| Affordability stress test | Assessed at a rate above the offered one | The stress rate is the honest budget input, not the teaser rate |

Budget from **net** income, not gross, and include the costs a lender does not count: commuting from the new location, utilities at the new size, service charge, maintenance sinking fund, furnishing, and the moving costs themselves. The `budget.md` fragility test applies with force here: if fixed + sinking exceeds ~60% of net income after the purchase, the household has bought a house with no capacity to absorb a shock.

## The Deposit

- Bigger deposits buy a lower rate at each LTV tier and a smaller loan; the marginal value is highest just above a tier boundary.
- **The deposit does not come from the emergency fund.** Completing a purchase with an empty buffer means the first boiler failure goes on a card at 22%.
- Money needed for a deposit inside two years is not investable money (`investing.md`, Rule 5). A market fall the quarter before completion is a cancelled purchase.
- Budget the costs *around* the deposit separately: duty or transfer tax, legal, survey, moving, immediate repairs, furnishing. They routinely total several percent more and are the reason a purchase completes with zero cash.
- First-time buyer schemes, guarantees and shared-ownership structures exist in many markets and each carries a specific catch — staircasing costs, a resale restriction, a subsidy repayable on sale. Establish `country` and read what the exit looks like before the entry.

## The Mortgage Itself

- **Fixed versus variable is a risk decision, not a forecast.** Fix when the budget cannot absorb the stress-tested payment; float when it can and the fixed premium is large. Never pick based on a prediction of rates.
- Fixing longer buys certainty and costs the early-repayment charge flexibility. Match the fix length to how long you will certainly stay, because breaking a fix to move can cost a large penalty.
- **The term is the strongest lever on total interest.** Extending it lowers the payment and raises the total repaid substantially; that trade is legitimate when it buys survivability, and expensive when it buys a bigger house.
- Overpayment: check the annual penalty-free allowance, and note that most lenders reduce the term rather than the payment by default. Reducing the term saves more interest; reducing the payment buys flexibility. Pick deliberately, and write the choice into `## Debt Plan` in `~/Clawic/data/money/memory.md`.
- **Prepay or invest** — the frontier is in SKILL.md's Where Experts Disagree. Prepayment is a guaranteed after-tax return equal to the rate; it is also illiquid, so it competes with ladder steps 5-7 and never with the buffer.
- Remortgage timing: start shopping three to six months before the fix ends, because rolling onto a lender's standard variable rate is usually the single most expensive month-to-month mistake available in the domain. Put the fix-end date in `## Due` the day the mortgage completes.
- Payment protection, mortgage life cover and similar products sold at the point of sale are insurance decisions and get priced like insurance, not accepted as a formality (`insurance.md`).

## Owning It

- Maintenance is a **sinking fund**, not an emergency (`budget.md`). A roof, a boiler and a bathroom all have known lifespans and known replacement costs; divide by the remaining months.
- Leasehold, condominium or community structures carry service charges and major-works levies that can arrive as five-figure demands with little notice. Read the reserve fund position before buying, and hold a sinking line after.
- Improvements are consumption unless they are proven to add more than they cost; most do not, and the ones that do are usually correcting a defect rather than adding a feature.
- Keep every improvement receipt: in several jurisdictions capital improvements raise the cost base and reduce tax on an eventual sale (`taxes.md`). The papers are the user's; the running cost-base total and where those papers live go in `~/Clawic/data/money/artifacts/tax-prep.md`.
- **Negative equity is only a realised problem if you must sell or must remortgage.** The plan for it is not to be forced into either: buffer intact, payments affordable at the stress rate, and no reliance on a sale date.

## Moving, Downsizing, and Renting Out

- Moving costs are a round trip every time, so serial moving is expensive in a way that monthly budgeting hides. Count the round-trip percentage against the years actually stayed.
- **Downsizing releases less than expected**: transaction costs both ways, plus the fact that smaller properties in desirable areas often carry a high price per square metre. Compute the net release before treating it as retirement funding (`retirement.md`).
- Renting out a former home converts a main residence into an investment property, which changes the tax treatment, the insurance, the mortgage terms and the legal obligations. All four need checking before the first tenant, and the underwriting side is `real-estate-investing`.
- Buying with a partner or a friend: the ownership split, what happens if one wants out, and what happens if one stops paying must be documented at purchase, in the deed structure or an agreement. Cohabiting partners are frequently not protected by default in the way married couples are (`household.md`).

**Write it down.** A rent-versus-buy or remortgage analysis — the round-trip percentage used, the break-even years, the expected stay, the decision and what would flip it — is an artifact at `~/Clawic/data/money/artifacts/decision-<kebab>.md`, with a row in `~/Clawic/data/money/decisions/<year>.md` and its `## Boxes` line, all in the same turn. The mortgage is an account: rate, balance, fix-end date and term go to `~/Clawic/data/finances/accounts.md`, and the deliberate not-prepaying decision goes to `## Debt Plan`. The fix-end date, the annual overpayment allowance reset and any major-works cycle go to `## Due`. Format in `memory-template.md`.
