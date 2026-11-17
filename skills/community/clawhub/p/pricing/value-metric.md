# The Value Metric — What You Actually Charge For

The single decision every other pricing decision inherits. Change it later and you are re-contracting every customer, so it is worth an hour of arithmetic now.

**Before choosing or changing a metric**, read `price-book.md` (what is charged today and on which metric) and `## Offering` in `~/Clawic/data/pricing/memory.md`. **After the decision**, write it to `artifacts/decision-value-metric.md` with what was rejected and the condition that would revisit it, and add its `## Boxes` line in the same turn (`memory-template.md`).

## The Three Tests

A metric qualifies only if it passes all three. Two out of three is the shape of a metric that gets abandoned in eighteen months.

| Test | Question | Failure looks like |
|---|---|---|
| **Scales with value** | When they get twice the outcome, does the invoice move? | Flat fee on a product whose usage grows 10× (→ Signals in SKILL.md) |
| **Forecastable** | Can the buyer put a number in next year's budget before signing? | Unpredictable metered spend; procurement blocks the deal on the variance, not the price |
| **Countable without you** | Can they verify the invoice from something they already track? | "Compute units", "credits", "workflow events" — every dispute becomes a support ticket |

Fourth, softer test: the metric must be one the customer is happy to grow. A metric tied to something they want *less* of — errors caught, tickets raised, incidents handled — makes your success their failure, and they will engineer around it.

## Candidates by Model

`business_model` selects the row; the metric column is the default, not the only option.

| Model | Default metric | Switch when |
|---|---|---|
| B2B SaaS, collaboration | Editors (creators), viewers free | The product is used by one person per company → switch to a company-level metric (records, revenue processed, sites) |
| B2B SaaS, data or infrastructure | Metered unit tied to the workload (GB stored, requests, rows synced) | The buyer cannot forecast it → platform fee plus metered (`usage-based.md`) |
| Developer tools | Seats for the IDE-shaped part, usage for the run-time part | Almost always hybrid; a pure-seat dev tool caps out at team size |
| Vertical SaaS | The unit the customer's own business counts (properties, patients, vehicles, locations) | Never — this is the strongest metric class there is; it grows with them and needs no explanation |
| Payments / fintech | Percentage of the money moved, with a floor per transaction | Small-ticket volume makes the floor the real price (→ the processor-fee row of The Arithmetic) |
| Marketplace | Take rate on GMV | Frequency is low and basket is large → listing or subscription fee (`marketplace.md`) |
| Consumer subscription | Per account, with a household or device fence | Sharing is the growth channel rather than the leak |
| Services | Day, fixed scope, or outcome (`services.md`) | — |
| Physical goods | Per unit, with pack architecture (`retail.md`) | — |

## Hybrid Is the Common Answer

Pure-seat pricing detaches from value in products where value is not human hours. Pure usage pricing transfers all forecasting risk to the buyer, and procurement prices that risk into the deal. The hybrid resolves both:

- **Platform fee** — the predictable component the buyer budgets. Covers access, support, and the fences (SSO, audit, SLA).
- **Included allowance** — sized so a typical customer never sees an overage in a normal month. The allowance is the actual product decision: too small and every month is a negotiation, too large and the metered part never earns anything.
- **Metered component** — priced above the committed rate so committing is always the cheaper path (`usage-based.md`).

Rule of thumb for the split: if the metered part is under ~15% of a typical bill it is noise the buyer resents, and if it is over ~50% the "platform fee" is a minimum charge in disguise — name it that instead.

## Quantifying Value Before Naming a Number

Economic value to the customer = **reference price + differentiation value − negative differentiation**.

- **Reference price**: what they use today, including the fully loaded cost of the manual process. A spreadsheet plus half a person is a reference price of that person's loaded salary × the fraction of their time.
- **Differentiation value**: what your product does that the reference does not, in money. Time saved × loaded hourly cost; errors avoided × cost per error; revenue unlocked × margin; risk reduced × probability × impact.
- **Negative differentiation**: what they lose by switching — migration effort, retraining, a feature the incumbent has.

Then price at a fraction of the differentiation value, not at all of it. Capturing 100% leaves the buyer indifferent, and indifferent buyers do not champion a purchase internally. Practitioners typically quote a value-capture share in the 10-30% band for a tool the buyer must also implement; the exact fraction is a positioning choice, and the number you can defend in a room is worth more than the number a spreadsheet produced.

Worked shape: an incumbent costs 40k/year, your product saves 300 hours at 60/hour (18k) and avoids two 5k incidents (10k). Economic value = 40k + 28k = 68k. Price at 20-30% of the 28k differentiation above the reference, on top of displacing the 40k, and the case survives a CFO reading it.

## Migrating a Metric

The most expensive change in this skill. Sequence, in order:

1. Model the new metric against the last 12 months of actual usage per customer. Publish the distribution to yourself: how many pay more, how many pay less, and what the extremes are.
2. Cap the change. A migration where any customer's bill more than doubles produces a churn event, not a migration; a cap of `+X% in year one` costs less than the account.
3. New customers move first, and only on the new metric. Never sell both metrics to the same segment at the same time.
4. Existing customers move at renewal, with a side-by-side of old and new on their own numbers. Nobody accepts a metric change they cannot recompute themselves.
5. Record the cohort, the cap, and the expiry in `## Price History`, and each affected account's outcome as it lands (`memory-template.md`).

## Traps Specific to Metrics

| Trap | Why it fails | Do instead |
|---|---|---|
| Charging for something the buyer wants less of | Aligns your revenue against their success; they optimize you away | Price the outcome, or the capacity to produce it |
| A metric only your dashboard can measure | Every invoice is disputable and support carries the cost | Pick something in their system of record |
| Counting viewers as seats | Kills exactly the large accounts you want, because most users only read | Editors, or a company-level unit |
| Renaming the metric to "credits" | Hides the price from the buyer and from you; nobody can compare your quote to anything | Credits are acceptable only as a *bundle of named units* with the conversion published |
| Two metrics in one plan | The buyer cannot forecast the interaction and neither can you | One metric, plus an allowance and an overage on it |

**Write the outcome**: the chosen metric and the rejected candidates go to `artifacts/decision-value-metric.md`; the price built on it goes into `price-book.md`; any migration becomes a row in `## Price History` with its cohort and cap (`memory-template.md`).
