# Monetization — Turning Usage Into Revenue

The growth question about money is not "what should we charge" — that is `pricing-strategy`. It is **where the paywall sits, who crosses it, and what happens to the cohort after they do.** This file covers the conversion mechanics between a user who gets value and revenue that recurs.

**Contents:** [Free Model Selection](#free-model-selection) · [Where the Limit Goes](#where-the-limit-goes) · [Paywall Mechanics](#paywall-mechanics) · [Trial Design](#trial-design) · [Packaging for Expansion](#packaging-for-expansion) · [Price Changes Without Churn Spikes](#price-changes-without-churn-spikes) · [Discounting Discipline](#discounting-discipline) · [Involuntary Churn and Dunning](#involuntary-churn-and-dunning) · [Cancellation Flow](#cancellation-flow) · [Traps](#traps)

**Before changing anything monetary**, read `## Funnel` (paid-conversion rate and its definition) and `## Pricing` in `~/Clawic/data/growth/memory.md`, plus `artifacts/pricing-change-<yyyy-mm>.md` if `## Boxes` lists one. A price change is the highest-blast-radius growth action available and the least reversible.

## Free Model Selection

| Model | Converts | Costs | Choose when |
|---|---|---|---|
| Free trial, no card | Moderate; large top of funnel | Support and infra for tyre-kickers | Value is provable within the trial window |
| Free trial, card up front | Much higher trial→paid, far smaller top of funnel | Deters evaluation | High-intent, considered purchase; strong brand |
| Freemium | Lowest rate, largest base | Permanent cost per free user | Free users create value for paid ones — content, network, virality (`loops.md`) |
| Reverse trial | Best of both in practice | Complexity in entitlements | Users need to feel the premium capability to want it (`activation.md`) |
| Demo/sales-led | Highest ACV | Human cost per opportunity | ACV supports a human touch (`b2b.md`) |

The freemium test is one question: **does a free user make the product better for a paying one?** If not, freemium is a permanent cost centre with a marketing story, and a trial converts the same demand for less.

## Where the Limit Goes

The limit that separates free from paid should be the dimension that **grows with the value the user receives**, and it must be legible before the user hits it.

| Limit dimension | Good when | Fails when |
|---|---|---|
| Usage volume (projects, records, messages) | Usage tracks value closely | The heaviest users are the least willing to pay (hobbyists) |
| Seats / collaborators | Value is collaborative | It taxes the loop you depend on — charging for the invitee kills viral growth (`loops.md`) |
| Advanced capability | The capability is only needed by people with budget | The capability is what makes the product work at all |
| Time | Nothing else is measurable | It rushes evaluation |
| Support/SLA | Enterprise buyers pay for it | It is the only difference, which reads as a shakedown |

Two rules: **never gate the aha moment** (a user who has not felt value will not buy the right to feel it), and **never gate the loop** (charging for the mechanism that acquires users is buying revenue with growth).

## Paywall Mechanics

- **Trigger on the limit, in context**: the user is doing the thing, hits the wall, sees exactly what unlocks it. A pricing page visited voluntarily converts a fraction as well as a contextual wall.
- **Show the wall before it blocks**: warn at ~80% of the limit so the upgrade is a plan rather than an interruption at the worst moment.
- **State the value in their units** — "your 3 projects are safe, upgrade to keep adding" — not the plan's feature list.
- **Soft walls beat hard walls** where the product allows: read-only, watermark, delayed export. They preserve the loop and the data while creating the reason to pay.
- Instrument `paywall_viewed` with the trigger and limit that caused it (`instrumentation.md`). The distribution of triggers tells you which limit is actually doing the monetising, and it is rarely the one the team assumed.

## Trial Design

- **Length is set by time-to-value, not by convention.** If the median user reaches value in 2 days, a 30-day trial adds 28 days of forgetting. Common defaults (14 days, 30 days) are conventions, not findings.
- **Trial conversion is an activation problem.** The number that predicts it is whether the user reached the aha action in the first days, not what happened at the end (`activation.md`).
- **Extend on engagement, not on request as a reflex**: an extension for a user who has been active is a good bet; an extension for a user who never logged in delays the answer.
- **The last day matters**: a reminder before expiry that names what they will lose, plus a clean path to pay, recovers a meaningful share of engaged trials (`lifecycle.md`).
- Card-up-front changes every rate in the funnel; comparing conversion across that boundary is comparing two businesses.

## Packaging for Expansion

Expansion revenue is the cheapest revenue: no acquisition cost, and it compounds with retention (`saas-metrics` for NRR definitions).

- Pick **one value metric** that scales with the customer's success (seats, usage, revenue processed, contacts). Price rises as their value rises, which makes increases feel earned rather than extracted.
- Avoid a value metric the customer can game cheaply, or one that punishes the behaviour you want (charging per API call in a product whose loop is API integration).
- **Three tiers plus enterprise** is the workable default: an entry tier that is genuinely usable, a main tier where most land, a high tier that makes the main one look reasonable and catches the demanding minority.
- Design the **upgrade trigger** into the product: a usage meter, a limit notification, an admin view showing team growth. Expansion that requires a salesperson to notice does not happen at self-serve scale.
- Downgrade paths are part of packaging: a customer who can shrink instead of leaving is retained revenue (`retention.md`).

## Price Changes Without Churn Spikes

1. **Grandfather existing customers**, at least for a defined period, and say so plainly. The trust cost of surprising them exceeds the revenue.
2. **Test on new customers first.** Price is one of the few things you can change for new cohorts and measure cleanly; run it as a cohort comparison, not a live A/B on the same page, since visible price differences between users are both detectable and damaging.
3. **Measure the whole chain**: conversion rate × price, not price alone. A 20% increase that costs 15% of conversions is still a win; a 20% increase that costs 30% is not.
4. **Watch the cohort for two full billing cycles** before declaring victory — the churn effect of a price change arrives at renewal, not at checkout.
5. **Announce with a runway** for existing customers: notice period, what changed, what they gain, and an option to lock in for a term.

## Discounting Discipline

- Every discount is a permanent teaching event: the market learns to wait. Cohorts acquired on discount show lower LTV and higher price sensitivity at renewal.
- Prefer **term commitment** (annual for two months free) over rate reduction: it improves cash and retention rather than eroding price.
- Time-box and reason-code every discount, and hold the total discounted share of new revenue against a cap you decided in advance.
- Never discount to save a churning customer whose problem is value; you have then paid to keep an unhappy customer who will churn later and tell people the list price is fake.

## Involuntary Churn and Dunning

The most recoverable revenue in the business, and usually unowned.

- Failed payments are a meaningful slice of total churn in card-billed subscription businesses; most failures are recoverable because the cause is an expired or replaced card rather than a decision.
- **Pre-expiry notice** before the card expires beats every retry.
- **Retry schedule** spread over days rather than hours, avoiding repeated same-day attempts that some issuers treat as suspicious; combine with automatic card-updater services where the processor offers them.
- **In-product notification** for a failed payment reaches users who ignore email.
- Set a hard end: after the schedule, downgrade rather than delete, so the account can return with its data (`retention.md`, `lifecycle.md`).

## Cancellation Flow

- Ask **one** structured reason with a free-text field. The reason distribution is the most actionable churn data you will get (`retention.md`).
- Offer the alternative that matches the reason: pause for "not using it right now", downgrade for "too expensive", a specific fix for "missing feature".
- **Do not obstruct.** Hidden cancellation, phone-only cancellation, and confirm-shaming produce chargebacks, public complaints, and regulatory exposure in multiple jurisdictions. A clean cancellation preserves the win-back.
- Offer export of their data on the way out. It costs nothing and it is the difference between a churned user and a hostile one.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Gating the aha moment | Users cannot want what they have not felt | Free through first value; charge for depth or scale |
| Charging per seat in a viral product | Taxes the loop that acquires users | Charge on a dimension that is not the invitation (`loops.md`) |
| Pricing page as the paywall | Voluntary visits convert far worse than contextual walls | Trigger at the limit, in context |
| Trial length copied from a competitor | Their time-to-value is not yours | Set from your own median TTV |
| A/B testing price on the same page | Detectable, damaging, and legally fraught in some markets | Cohort test on new customers |
| Discount to hit the quarter | Trains waiting, lowers LTV in the measured cohort | Term commitment, or fix packaging |
| Ignoring failed payments | Recoverable revenue leaks silently as "churn" | Dunning with pre-expiry notice |
| Retention offers in a maze of a cancel flow | Chargebacks, complaints, regulatory risk | One reason, one matched offer, clean exit |

**After any monetization change**, write it back in the same turn: the paid-conversion rate with its definition and as-of date into `## Funnel`, the plan structure, value metric, limits and current prices with their currency into `## Pricing`, both in `~/Clawic/data/growth/memory.md`. A price or packaging change is an artifact from the first one: `~/Clawic/data/growth/artifacts/pricing-change-<yyyy-mm>.md` with the old and new structure, the rationale, who was grandfathered, the measured effect on conversion and churn, and what was rejected — plus its `## Boxes` line in the same turn (`memory-template.md`). Revenue commitments and subscription costs belong in the shared `~/Clawic/data/finances/`, never duplicated here.
