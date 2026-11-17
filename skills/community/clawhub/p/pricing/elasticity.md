# Elasticity and Margin Maths

The arithmetic that turns a pricing opinion into a decision. Every formula here is derivable; run it before the recommendation.

**Before any margin claim**, read `## Cost Inputs` in `~/Clawic/data/pricing/memory.md` and check the `As of` date — a floor computed from a stale unit cost is not a floor. **After establishing a cost, a fee, or a measured elasticity**, write it to `## Cost Inputs` with its date and source (`memory-template.md`).

## Contribution Margin, Not Gross Margin

Everything below uses **contribution margin**: price minus the costs that actually vary with one more unit sold. For software that is infrastructure, payment fees, third-party per-seat costs, and support load — not salaries, not the office, not the CEO.

`m = (price − variable cost) / price`

Using a company-wide gross margin here inflates `m` and makes every discount look survivable. Using a fully loaded margin deflates it and makes every price look impossible. The unit that varies is the unit that counts.

## The Two Break-Evens

For a price rise of `x` (fraction) at contribution margin `m`:

`maximum tolerable volume loss = x / (m + x)`

For a price cut of `d`:

`required volume gain = d / (m − d)`

| m | +10% price tolerates a loss of | −10% price needs a gain of |
|---|---|---|
| 0.40 | 20.0% | 33.3% |
| 0.60 | 14.3% | 20.0% |
| 0.70 | 12.5% | 16.7% |
| 0.80 | 11.1% | 14.3% |
| 0.90 | 10.0% | 12.5% |

Two things this table settles permanently:

- **High-margin businesses have enormous room to raise and almost none to cut.** At 90% margin, a 10% cut needs 12.5% more units — for a software product, that is a growth-rate change, not a promotion.
- A cut of `d` is impossible once `d ≥ m`: the denominator goes to zero or negative, meaning no volume makes it back. Discounting past the contribution margin is buying customers with cash.

## Elasticity, Honestly

`E = %ΔQ / %ΔP`, always negative for normal goods. Elastic is `|E| > 1` (revenue falls when you raise); inelastic is `|E| < 1` (revenue rises).

- **You cannot know E from a spreadsheet.** It is measured — from a test (`testing.md`), from a past change with a recorded outcome (`## Price History`), or from a competitor's move you observed.
- The break-even loss from the table above **is** the elasticity threshold in disguise: +10% tolerating 12.5% loss means the move wins whenever `|E| < 1.25`.
- Elasticity is not one number for a business. It differs by segment, by tenure, by channel, and between acquisition and renewal — existing customers with data and workflows inside the product are systematically less elastic than a first-time visitor.
- Substitutes and switching cost dominate. If migrating out takes a week of somebody's time, that week is part of your price.

## The Profit Leverage of Price

Take a business with revenue 100, variable cost 30, fixed cost 55, profit 15. Move each lever by 1%:

| Lever | Profit change | Why |
|---|---|---|
| Price +1% (volume held) | +1.0 → +6.7% profit | The whole 1% falls to the bottom line |
| Volume +1% | +0.7 → +4.7% profit | Only the contribution margin of the extra unit lands |
| Variable cost −1% | +0.3 → +2.0% profit | Applies to 30 of revenue |
| Fixed cost −1% | +0.55 → +3.7% profit | Applies to 55 |

Price is the highest-leverage lever in almost every business, and the ratio grows with margin. This is why a quarter spent on pricing beats a quarter spent on a cost programme in most software companies — and why an accidental 20% discount policy is a bigger hole than any line item.

## Pricing Against a Competitor

`your price ≈ their price + differentiation value − their switching-cost advantage`

- **Never match a competitor's number.** Their price encodes their cost base, funding, segment, and channel. A venture-funded incumbent pricing below cost is running a strategy you cannot copy without their balance sheet.
- Answer "X charges less" with the differentiation arithmetic (`value-metric.md`): what your product does that theirs does not, in money, on their numbers.
- If the honest answer is that there is no differentiation value, the problem is positioning, not price, and cutting will only speed up the discovery.
- If they cut, do not follow reflexively. Model your own break-even first: matching a 15% cut at 70% margin needs 27.3% more volume, and a price war between two products with the same cost base ends with both at the floor.

## Segmented Elasticity — Where the Money Is

The same product sold at one price to two segments leaves money on both sides. Legitimate ways to charge different segments differently, in rough order of durability:

1. **Fences in the product** — a capability one segment must have (`packaging.md`). Most durable, because the buyer self-selects.
2. **Value metric** — bigger customers consume more of the metric and pay more automatically (`value-metric.md`).
3. **Channel and geography** — country bands, distributor pricing (`international.md`, `retail.md`).
4. **Commitment** — term length, prepay, volume commitment (`discounting.md`).
5. **Time** — early access, launch pricing with a stated end date.

Individual-level pricing from automated profiling is a different category with disclosure duties attached (SKILL.md, Legal Tripwires).

## When a Number Cannot Be Computed

Missing inputs are common. Do not stall, and do not invent:

- No variable cost known → use the target from `target_gross_margin_pct` as the assumed `m`, and say so in the same sentence as the result.
- No elasticity known → state the break-even volume change and frame the decision as "this move needs the loss to stay under X%", which is a testable claim.
- No competitor data → state the reference price the buyer is actually comparing against, even when it is a manual process.

Every one of those assumptions gets written into `## Cost Inputs` with its date, so the next session inherits the assumption instead of re-inventing a different one.

**Write the outcome**: unit costs, fee rates and assumed margins go to `## Cost Inputs` with their `As of` date; any measured elasticity goes to the `## Price History` or `## Experiments` row it came from (`memory-template.md`).
