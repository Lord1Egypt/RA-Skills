# Physical Goods — Margin, Channel, and Markdowns

Physical products have a real marginal cost, a channel that takes a cut, and inventory that decays in value. All three change the arithmetic.

**Before setting a price**, read `## Cost Inputs` in `~/Clawic/data/pricing/memory.md` (landed cost, fees, freight — with their `As of` dates) and `price-book.md` for the current list and MAP. **After the decision**, update `price-book.md` and write any channel or markdown policy to `artifacts/`, with its `## Boxes` line (`memory-template.md`).

## Landed Cost First

Unit cost is not the invoice from the factory. Landed cost = goods + freight + duty and tariffs + insurance + inbound handling + inspection + the amortized cost of tooling and the failed first run.

- Compute per unit at the **actual order quantity**, not at the quantity on the quote sheet. Per-unit cost at 5,000 units is not the cost at 500.
- Include the return rate as a cost: at a 10% return rate with half the returns unsellable, effective unit cost rises by roughly 5%.
- Re-check landed cost whenever freight rates, duty, or exchange rates move; write the new number to `## Cost Inputs` with its date. A price built on last year's freight is a price built on nothing.

## Markup and Margin Are Not the Same Number

`margin% = (price − cost) / price` · `markup% = (price − cost) / cost` · `price = cost / (1 − target margin)`

- Keystone (double the cost) = 100% markup = **50% margin**. Confusing the two is the most common arithmetic error in this domain and it always errs toward underpricing.
- To hit a 60% margin on a 20 cost: `20 / 0.4` = 50, not 32.

## The Channel Stack

Each layer takes its cut of the price at that layer, and the retail price has to carry all of them.

| Channel | Typical structure | Consequence |
|---|---|---|
| Direct | You keep the full price, pay payment fees and fulfilment | Highest margin, you fund all acquisition |
| Own store on a hosted platform | Platform subscription + payment fees | Predictable; the acquisition cost is still yours |
| Online marketplace | A referral or transaction fee per sale, varying widely by category | Traffic included; margin and customer relationship are not |
| Wholesale to a retailer | You sell at roughly 50% of the retail price | Your cost must sit below ~25% of retail for the maths to work |
| Distributor into retail | Distributor and retailer both take a margin | Cost below ~15-20% of retail |

Work backwards from the shelf price the market accepts, not forwards from cost. If the required cost is unreachable, the channel is wrong or the product is.

Marketplace fee schedules change and vary by category — treat any figure you remember as needing verification before it goes in a model, and write the checked number into `## Cost Inputs` with the date.

## Price Architecture Across a Range

- **Good-better-best applies to products too**, and the anchor rule from `packaging.md` holds: the top item legitimizes the middle.
- **Price-pack architecture**: the same product in different sizes at deliberately non-proportional prices. The larger pack should look obviously better per unit and still carry a higher absolute margin.
- **Price points, not prices.** Physical retail clusters at psychological thresholds; a product priced just above one loses more volume than the extra margin returns.
- Keep the entry item genuinely good. An entry product that disappoints costs you the range, not just the sale.

## Promotions and Markdowns

- **Promotion depth trains the customer.** A brand discounted 30% every month has a 30%-lower real price and a list price nobody believes.
- Break-even on a promotion is the standard formula: at 50% margin, a 20% discount needs `0.2 / 0.3` = **67% more units** to be neutral. Most promotions do not clear it; they pull demand forward from customers who would have paid full price.
- **Markdown cadence for seasonal stock**: a planned ladder (for example, first markdown at week 6, deeper at week 10, clearance at week 14) beats reacting late. Holding inventory has a carrying cost, and the first markdown is almost always cheaper than the third.
- Sell-through rate against plan is the trigger, not the calendar alone: below plan by a set margin at the checkpoint, mark down.
- A "was" price used in a promotion has to be a price you genuinely charged, for a period, recently — the rules on prior-price claims are specific and enforced on presentation alone (`compliance.md`).

## MAP, MSRP, and Channel Conflict

- **MSRP** is a recommendation; **MAP** governs the price a reseller may *advertise*, not the price they may sell at.
- A unilaterally announced advertised-price policy is the usual lawful shape in jurisdictions where dictating a reseller's resale price is unlawful. Negotiating it as an agreement is where the exposure starts (SKILL.md, Legal Tripwires).
- Enforce MAP consistently or not at all: selective enforcement is both commercially useless and legally worse.
- **Channel conflict** is a pricing problem before it is a sales problem: selling direct below your own retailers' price destroys the channel that carries your volume. Differentiate by bundle, configuration, or exclusive variant instead of by price.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Cost-plus on factory cost | Ignores freight, duty, returns and fees; the margin evaporates on the first landed shipment | Landed cost, refreshed with its date |
| Confusing markup with margin | 100% markup feels like 100% margin and is 50% | `price = cost / (1 − margin)` |
| Pricing forward from cost into a retail channel | Arrives above what the shelf accepts, then gets discounted to survive | Work backwards from the shelf price |
| Permanent promotion | The list price stops meaning anything and the brand is repriced | Fixed windows, published end dates (`discounting.md`) |
| Late first markdown | Carrying cost plus a deeper clearance later | A planned ladder with sell-through triggers |
| Free shipping absorbed into margin | It is a discount that never appears in discount reporting | Price it into the product or set a threshold |
| Underpricing to win the first retailer | Wholesale terms are the reference for every retailer after them | Hold the wholesale price; give a first-order term instead |

**Write the outcome**: landed cost, fees and freight to `## Cost Inputs` with their dates; list, wholesale and MAP to `price-book.md`; the markdown ladder and MAP policy to `artifacts/`; each promotion window and markdown checkpoint to `## Due`; every price change to `## Price History` (`memory-template.md`).
