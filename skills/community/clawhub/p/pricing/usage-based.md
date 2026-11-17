# Usage-Based and Hybrid Pricing

Metered pricing aligns revenue with value and moves all forecasting risk onto the buyer. The design work is giving that risk back.

**Before designing or changing meters**, read `price-book.md` (the current metric, allowance and overage rate) and `## Cost Inputs` in `~/Clawic/data/pricing/memory.md` (what a unit actually costs to serve). **After the design lands**, update `price-book.md` and write the rationale to `artifacts/decision-metering.md` with its `## Boxes` line (`memory-template.md`).

## The Standard Shape

`platform fee + included allowance + overage rate`, with an optional committed tier that buys a better rate.

- **Platform fee**: the predictable part the buyer budgets. Covers access, support, and the fences that define the tier (`packaging.md`).
- **Allowance**: sized so a typical customer sees no overage in a normal month. This is the real product decision — too small and every month is a negotiation; too large and the meter never earns.
- **Overage rate**: priced **above** the committed rate, always. If overage is cheaper than committing, nobody commits and your revenue becomes unforecastable too.
- **Commit tiers**: buy a larger allowance in advance at a lower unit rate. A 20-40% spread between the overage rate and the deepest commit rate is enough to make committing obviously correct without making overage punitive.

## Designing the Unit

| Property | Requirement | Failure |
|---|---|---|
| Granularity | Coarse enough that a bill is legible: "1,000 records synced", not "compute-seconds" | Units nobody can picture become disputes |
| Verifiability | Countable in the customer's own system (SKILL.md Rule 1) | Every invoice becomes a support ticket |
| Cost correlation | Tracks your marginal cost closely enough that heavy users are not loss-making | A flat unit price across workloads with 10× cost variance |
| Stability | Does not change meaning when the product changes | Re-defining a unit mid-contract is a price change, whatever it is called |

Credits are acceptable only as a **bundle of named units with a published conversion**. A credit whose conversion moves is an undisclosed price change, and it is the pattern buyers have learned to distrust.

## Preventing the Surprise Bill

The bill nobody expected is the largest churn driver in metered pricing, and it is entirely preventable:

- **Soft cap by default**: usage above the allowance is served, then flagged. Hard caps that break production make you the outage.
- **Alerts at 80% and 100%** of the allowance, to the person who pays and the person who uses. One of them is usually unaware of the other.
- **In-product usage visibility** on the same page as the plan. If they have to ask, the bill will surprise them.
- **A spike guard**: any single day above roughly 3× the trailing daily average triggers a notification before it becomes an invoice. Bugs and runaway loops are the common cause, and eating one incident buys more goodwill than it costs.
- **A published rounding and proration rule**. Rounding up per call versus per day changes small bills by an order of magnitude, and undisclosed rounding is what turns a disagreement into a chargeback.

## Commitments and True-Ups

- **Annual commit with monthly draw-down** is the standard enterprise shape: the customer commits to a value, consumes against it, and unused balance is forfeited or partially rolled over.
- **Rollover policy is a real decision.** No rollover maximizes revenue and creates end-of-term anger; unlimited rollover means you never recognize the revenue. A common middle is rolling over a stated fraction into the next term only if they renew.
- **True-up cadence**: monthly for self-serve, quarterly or annually for enterprise. Longer cadence means a larger, angrier invoice.
- **Ramp deals** (a commit that grows across a multi-year term) are how a customer signs for capacity they do not yet use. Write the ramp schedule into the contract with dates, and put each step in `## Due` so the increase is not a surprise on your side either.

## Migrating from Seats to Usage

The migration in `value-metric.md` applies in full, plus three metered-specific steps:

1. **Shadow-bill for at least one full cycle.** Show every affected customer what they *would* have paid on the new meter, using their own data, before anything changes.
2. **Cap the first-period increase.** A bill that more than doubles is a churn event regardless of how correct the meter is.
3. **Keep the old plan sellable to nobody.** Existing customers may stay on it until their stated expiry; new customers only ever see the meter.

## When Not to Meter

- The buyer's procurement cannot approve variable spend. Common in public sector and in large enterprises with annual budget locks — the answer is a commit with overage, not a refusal.
- Your marginal cost is genuinely near zero and does not vary with the unit. Then metering is just a tax on usage that discourages the adoption you want.
- The unit is not countable by the customer. Fix the unit first (→ Designing the Unit).
- Usage is lumpy and seasonal. Meter on a trailing average or an annual commit, not on the peak month.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Overage priced below the commit rate | Committing becomes irrational; forecastability disappears for both sides | Overage above commit, spread of 20-40% |
| Hard caps that stop the product | You become the incident, and the incident is on the customer's status page | Soft cap, alert, spike guard |
| Credits with a moving conversion | An undisclosed price change; buyers stop trusting quotes entirely | Named units, published conversion, changes announced like any price change |
| Metering something that scales with your inefficiency | You get paid more when the product is worse | Meter the outcome, not the compute |
| No usage visibility in-product | Every bill is a discovery, and half are disputed | Usage on the plan page, alerts at 80/100% |
| Unlimited rollover | Revenue is never recognized and the commit means nothing | Bounded rollover, conditional on renewal |
| Launching a meter without shadow-billing | Nobody, including you, knows what customers will actually pay | One full cycle of shadow bills before the switch |

**Write the outcome**: the meter, allowance, overage and commit rates go into `price-book.md`; the design rationale and rejected units to `artifacts/decision-metering.md`; each ramp step and true-up date to `## Due`; any negotiated commit to `## Deals` (`memory-template.md`).
