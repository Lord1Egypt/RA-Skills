# Price Experiments

A price test is the only way to measure elasticity in your own market. It is also the experiment most often read wrong, because the effect lands after the report is written.

**Before designing a test**, read `## Experiments` in `~/Clawic/data/pricing/memory.md` (what has already been tested, including tests that were abandoned and why) and `price-book.md` for the current baseline. **After the test ends — including when it is stopped early —** write the row to `## Experiments` with split, read metric, result and decision, in the same turn (`memory-template.md`).

## Legitimate Splits

| Split | Use when | Caution |
|---|---|---|
| **New traffic / new customers only** | The default for a list-price test | Slowest; needs volume |
| **Geographic** | Prices already differ by market (`international.md`) | Markets differ in more than price; compare each geo to its own baseline |
| **Time-based (before/after)** | Low traffic makes concurrent splits impossible | Seasonality and any other change in the same period confound it; requires a long, stable baseline |
| **Cohort by signup date** | Testing a change to existing customers | This is a price change, not a test — the notice rules apply (`price-increase.md`) |
| **Plan or packaging variant** | Testing structure rather than the number | Two variables at once unless the prices are held equal |
| **Same page, same shopper, different price** | Never | The complaint, the screenshot, and in some contexts a disclosure obligation |

Whatever price was displayed gets honored, including when it was a mistake. The cost of honoring a wrong price once is far below the cost of the story about not honoring it.

## The Metric

- **Revenue per visitor** (or per trial start, or per lead) is the read. Conversion rate alone always favours the lower price and routinely favours the losing variant.
- **Add churn.** A cheaper price converts worse-fit customers who leave sooner; a test read before the second billing cycle systematically overstates the cheap variant.
- **Read at 90 days minimum** for a subscription: one full billing cycle, the refund window, and the first renewal decision. Ninety days is also long enough for a novelty effect to decay.
- Track **average selling price** and discount depth alongside, if a sales team is involved, and carry both into the `## Experiments` row: a list-price test that is absorbed entirely by deeper discounts has tested nothing.

## Sizing and Duration

- Power the test on the **conversion** metric first, because revenue per visitor is high-variance and needs far more traffic to reach significance. If the conversion signal is unreachable at your traffic, a formal test is not available and the honest alternative is a sequential change with a long baseline.
- Fix the duration and the sample **before** starting, and do not read it early to decide whether to continue. Repeatedly checking until something looks significant manufactures results.
- Run whole weeks. Weekday and weekend traffic differ in intent, and a test that ends mid-week is unbalanced.
- Very small differences are not worth testing: if the traffic can only resolve a 30% effect, testing 49 against 52 is theatre.

## Alternatives When You Cannot Test

Most companies cannot run a properly powered price test, and that is fine:

- **Sequential change with a long baseline**: change one thing, hold everything else, compare against a clean prior period of similar length. Weak, but honest if the confounds are named.
- **Willingness-to-pay research** (`research.md`) to bound the range, then commit.
- **Discount depth as a proxy**: if closing consistently requires 25% off, the market has already priced you.
- **New-market pricing**: a new geography or a new segment is a clean surface for a different price with no existing customers to explain it to.
- **Painted-door tests** for a plan that does not exist yet: measure intent to select, then tell everyone who clicked exactly what is happening. Deceiving people who reach a checkout is not a test, it is a complaint.

## Reading the Result

| Observation | Likely meaning | Next |
|---|---|---|
| Higher price, revenue per visitor up, churn flat at 90 days | Genuine underpricing | Adopt; then plan the existing-customer sequence (`price-increase.md`) |
| Higher price, conversion down, RPV flat | The market is at its indifference point on this metric | Change the package, not the number (`packaging.md`) |
| Lower price, conversion up, RPV down | Elastic on conversion but not on revenue | Do not adopt; the cut is buying volume with margin |
| Lower price, RPV up, churn up at 90 days | The cheap variant bought worse-fit customers | Re-read at 180 days before adopting anything |
| Early lift that disappears | Novelty, or a seasonal confound | Extend, or re-run in a different period |
| No difference at all | The price is not the constraint in this funnel | Test packaging, positioning, or the page (`pricing-page.md`) |

Write the decision, not just the numbers. "Adopted 19" and "rejected, RPV flat and churn up" are what a future session can use; a table of conversion rates is not.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Reading on conversion rate | The cheaper price always wins on conversion, and can still earn less | Revenue per visitor, plus churn |
| Peeking until significant | Manufactures a result from noise | Fix duration and sample before starting |
| Same-page A/B on identical shoppers | Trust damage that outlives the finding | Cohort, geo, or new-traffic splits |
| Testing price and packaging together | Neither result is attributable | One variable; hold prices equal when testing structure |
| Not honoring a displayed price | The screenshot is the outcome, not the data | Honor it, always |
| Never recording abandoned tests | The same test is re-proposed every year | `## Abandoned` with the reason it stopped |
| Testing at traffic that cannot resolve the effect | Produces confident noise | Sequential change with a long baseline, honestly labelled |

**Write the outcome**: every test — started, finished, or abandoned — to `## Experiments` with split, read metric, result and decision; the adopted price to `price-book.md` and a row in `## Price History`; the read dates to `## Due` so the 90-day read actually happens (`memory-template.md`).
