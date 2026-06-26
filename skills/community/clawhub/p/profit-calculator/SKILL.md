---
name: Profit Calculator
version: 1.1.0
description: Calculate true per-unit profit margins across channels by factoring in COGS, platform fees, shipping costs, ad spend allocation, returns, and overhead to identify which products and channels actually make money.
author: LeroyCreates
tags: [ecommerce, profitability, unit-economics, margin-analysis, cogs, channel-profitability]
---

# Profit Calculator

Many ecommerce brands think they are profitable because revenue is growing, only to discover at year-end that certain SKUs or channels have been losing money on every order. Profit Calculator walks you through a full per-unit profit waterfall for each SKU on each channel so you can see exactly which products and channels deserve more budget and which should be repriced, rebundled, or killed.

## Use when

> The operator says "my TikTok Shop sales look great but the bank account isn't growing — can we figure out what's actually making money?"

> A Shopify seller asks "if I raise the price by $2, will that offset my new 3PL rate and higher Meta CPMs, or am I still underwater?"

> An Amazon FBA brand wants to compare a single SKU's contribution margin between FBA, FBM, and their own DTC store side by side before reallocating inventory.

> A founder is preparing a board update and needs a clean per-SKU contribution margin waterfall that rolls up to a blended gross margin with and without advertising.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|----------|--------|------------|------|
| COGS calculation | Landed cost including freight, duty, inspection, and packaging per unit | Factory cost plus estimated freight | Factory cost only, no landed adjustments |
| Platform fee mapping | Every fee line itemized per channel (commission, referral, payment processing, storage, subscription amortized) | Major fees captured, minor fees estimated as percentage | Single blended "platform fee" percentage across channels |
| Shipping cost model | Actual weight/zone-based rate per SKU per channel from 3PL rate card | Average shipping cost per order applied uniformly | Free shipping absorbed with no per-unit allocation |
| Ad spend allocation | Channel-specific ROAS or blended MER applied per SKU with clear attribution window | Blended MER applied uniformly across all SKUs | Ad spend not included in unit economics |
| Return cost modeling | Return rate per category with full loaded cost (reverse logistics + product loss + restocking labor) | Average return rate applied with estimated cost per return | Returns ignored or treated as top-line revenue reduction only |
| Overhead allocation | Fixed overhead allocated per unit using activity-based costing or revenue-weighted method | Overhead allocated as flat percentage of revenue | Overhead excluded from unit economics entirely |
| Contribution margin target | Channel-specific targets with minimum floor (e.g., 20% DTC, 12% Amazon, 8% TikTok) | Single blended target across all channels | No target defined, just reporting current margins |
| Price sensitivity analysis | Scenario modeling at multiple price points showing margin impact per channel | Single price change scenario modeled | No price sensitivity analysis included |
| SKU rationalization | Clear kill/reprice/rebundle recommendations with P&L impact quantified | Flagging negative-margin SKUs without action plan | No SKU-level recommendations |
| Reporting cadence | Monthly P&L waterfall with automated data pull and variance tracking | Quarterly manual calculation | One-time snapshot with no refresh plan |

## Solves

### Revenue-profit disconnect
The brand is growing 40% YoY but cash flow is flat. Revenue metrics mask that 30% of SKUs lose money after platform fees and returns. The waterfall exposes per-unit contribution margin so the operator knows exactly where the margin leak is.

### Channel margin blindness
DTC looks profitable at 60% gross margin, but after Meta ad spend at 4x ROAS, shipping, and returns, contribution margin is 12%. Meanwhile Amazon FBA at 35% gross margin nets 18% contribution because ad spend is lower and returns are handled by Amazon. Without per-channel unit economics, budget allocation is backwards.

### Hidden fee accumulation
Platform fees compound in ways that are not obvious. Amazon's referral fee + FBA fee + storage fee + payment processing can exceed 40% on low-ASP items. TikTok Shop's commission + shipping subsidy clawback + affiliate commission stack differently. Each channel's fee waterfall must be mapped individually.

### Return cost underestimation
Brands treat returns as a revenue reversal, but the true cost includes reverse logistics ($4–8 per unit), product loss (30–60% of returned apparel is unsellable at full price), restocking labor, and the original outbound shipping cost that was never recovered. A 25% return rate can eliminate all margin on a $30 product.

### Ad spend misattribution
Using blended MER across all SKUs treats a hero product driving 80% of ad-attributed revenue the same as a tail SKU with zero ad spend. Per-SKU or per-category ROAS allocation reveals which products can afford advertising and which cannot.

### Overhead allocation avoidance
Brands exclude warehouse rent, software subscriptions, and team salaries from unit economics because they are "fixed costs." But a product that shows 15% contribution margin before overhead and 2% after overhead is one supply chain disruption away from losing money.

### Price optimization paralysis
Without a margin model, price changes are gut decisions. The waterfall lets you simulate raising price by $3 on Amazon and see exactly how contribution margin changes after the referral fee percentage adjusts and estimated conversion rate shifts.

## Workflow

### Step 1 — Gather SKU-Level Cost Data

Collect the landed cost per unit for every SKU. Landed cost means the total cost to get one unit to your warehouse ready to sell. This includes factory cost, inbound freight (ocean/air), duty and tariffs, inspection fees, packaging materials, and any prep costs (labeling, poly-bagging).

**What to ask for:**
- Most recent purchase order with per-unit costs broken out
- Freight invoices for the most recent shipment (divide total by units shipped)
- Customs/duty documentation or estimated duty rate by HTS code
- Packaging cost per unit (branded box, poly bag, inserts, labels)
- Any prep or kitting costs (FBA prep service, bundle assembly)

**Common mistakes:**
- Using factory FOB price instead of true landed cost (can understate COGS by 15–25%)
- Forgetting to include duty, which on many consumer goods is 5–15% of declared value
- Not updating COGS when suppliers raise prices mid-year
- Ignoring packaging cost differences between channels (Amazon requires specific prep that DTC does not)

**Output:** A table with each SKU, its landed cost per unit, and a breakdown of what is included.

### Step 2 — Map Channel Fee Structures

For each sales channel, document every fee that applies to a transaction. This must be done per channel because fee structures vary dramatically.

**Amazon FBA fee components:**
- Referral fee (category-dependent, typically 8–15%)
- FBA fulfillment fee (size and weight tiered)
- Monthly storage fee (standard vs. Q4 peak rates)
- Long-term storage fee (if applicable, for inventory over 181 days)
- Payment processing (included in referral fee for Amazon)
- Subscription fee amortized per unit (Professional seller plan $39.99/month ÷ units sold)

**Shopify DTC fee components:**
- Shopify subscription amortized per unit
- Payment processing (Shopify Payments: 2.4–2.9% + $0.30)
- App fees amortized per unit (Klaviyo, reviews app, etc.)
- Theme or development costs amortized (optional, for accuracy)

**TikTok Shop fee components:**
- Platform commission (category-dependent, typically 5–8%)
- Payment processing fee (typically included in commission)
- Affiliate commission (if using affiliate program, typically 10–20% of sale price)
- Shipping subsidy participation (if enrolled, can be clawed back)
- Sample costs for affiliate seeding (amortized per attributed sale)

**Walmart Marketplace fee components:**
- Referral fee (category-dependent, typically 6–15%)
- WFS fulfillment fee (if using Walmart Fulfillment Services)
- Storage fees (if using WFS)
- Payment processing (included in referral fee)

**Output:** A fee schedule table for each channel showing every line item as both percentage and estimated dollar amount per unit at current ASP.

### Step 3 — Calculate Shipping and Fulfillment Costs

Determine the outbound shipping and fulfillment cost per unit per channel. This is the cost to get the product from your warehouse (or 3PL or FBA) to the customer.

**For FBA:** The FBA fulfillment fee from Step 2 covers this. No additional shipping cost calculation needed for FBA orders.

**For 3PL-fulfilled channels (DTC, TikTok Shop self-fulfilled, Walmart self-fulfilled):**
- Pick-and-pack fee per order from 3PL rate card
- Outbound shipping rate based on weight and zone mix
- Packaging materials cost (box, dunnage, tape, label)
- If multi-item orders are common, calculate per-unit cost as total fulfillment cost ÷ average units per order

**For self-fulfilled:**
- Labor cost per order (time to pick, pack, label ÷ hourly rate)
- Shipping carrier rate (use average zone and weight)
- Materials cost

**Key nuance:** Free shipping is not free. If you offer free shipping on DTC, the shipping cost still hits your margin. Capture the actual cost here.

**Output:** Per-unit shipping and fulfillment cost for each channel.

### Step 4 — Allocate Advertising Cost Per Unit

Decide how to attribute ad spend to unit economics. There are two approaches:

**Approach A — Blended MER (simpler):**
Total monthly ad spend across all channels ÷ total revenue = ad cost as % of revenue. Apply this percentage to each unit's revenue. This is simpler but treats all SKUs equally, which is rarely accurate.

**Approach B — Channel-specific ROAS (more accurate):**
For each channel, take the channel's ad spend ÷ channel's attributed revenue = channel ad cost percentage. Apply per channel. Within a channel, if you can break ROAS down by product category or hero SKU vs. tail, do so.

**What to document:**
- Which approach you are using and why
- Ad spend by channel for the most recent representative month
- Revenue by channel for the same period
- Any known ROAS differences by product category
- Attribution window used (1-day click, 7-day click, etc.)

**Common mistake:** Excluding ad spend from unit economics entirely. This makes contribution margins look artificially high and leads to bad pricing and channel allocation decisions.

**Output:** Ad cost per unit or ad cost as percentage of revenue, documented per channel.

### Step 5 — Model Returns and Refund Costs

Returns are one of the most underestimated margin killers. Model the full cost of a return per unit.

**Return cost components:**
- Reverse logistics (cost to ship the product back or cost of prepaid return label): typically $4–8 per unit
- Product disposition: what percentage of returns are resellable at full price vs. discounted vs. unsellable
  - Apparel: 30–50% full price resellable, 20–30% liquidation, 20–40% write-off
  - Electronics: 60–70% full price after refurbishment, 20–30% liquidation
  - Beauty/consumables: 90%+ write-off (cannot resell opened products)
- Restocking labor: time to inspect, repackage, relabel (typically $1–3 per unit)
- Original outbound shipping cost: already paid and not recoverable
- Refund processing: payment processor does not always refund the transaction fee

**Calculate per-unit return cost:**
(Return rate for category) × (reverse logistics + product loss cost + restocking labor + original shipping) = return cost per unit sold

**Example:** A $35 apparel item with 28% return rate, $6 reverse logistics, 40% product loss ($14), $2 restocking, $5 original shipping:
0.28 × ($6 + $14 + $2 + $5) = $7.56 return cost per unit sold

**Output:** Return cost per unit per channel, broken out by component.

### Step 6 — Allocate Fixed Overhead Per Unit

Fixed costs do not change with volume in the short term, but they must be covered by contribution margin over time. Decide how to allocate them.

**Fixed overhead categories:**
- Warehouse or office rent
- Full-time team salaries (non-variable)
- Software subscriptions (Shopify, ERP, analytics tools, email platform)
- Insurance
- Professional services (accounting, legal)
- Equipment depreciation

**Allocation methods:**

*Revenue-weighted:* Allocate total monthly overhead proportional to each SKU's share of total revenue. Simple but penalizes high-ASP items.

*Unit-weighted:* Allocate total monthly overhead equally per unit sold. Simple but ignores that some SKUs consume more resources.

*Activity-based:* Allocate based on actual resource consumption (e.g., SKUs requiring custom packaging get more warehouse labor allocation). Most accurate but most time-consuming.

**Recommendation:** Start with revenue-weighted allocation. It is good enough for most brands under $10M in revenue. Switch to activity-based once you have SKUs with dramatically different handling requirements.

**Output:** Overhead cost per unit per channel, with the allocation method documented.

### Step 7 — Build the Profit Waterfall and Make Decisions

Assemble all components into a per-unit profit waterfall for each SKU on each channel.

**Waterfall structure:**
1. Retail price (channel-specific)
2. − Platform fees = Net revenue after fees
3. − COGS (landed cost) = Gross profit
4. − Shipping and fulfillment = Gross profit after fulfillment
5. − Ad spend allocation = Contribution margin before returns
6. − Return costs = Contribution margin after returns
7. − Overhead allocation = Net contribution margin

**Decision framework based on net contribution margin:**

| Margin Range | Action |
|-------------|--------|
| > 20% | Scale — increase inventory depth, expand advertising, consider new channels |
| 10–20% | Maintain — healthy margin, optimize where possible but no urgent action |
| 5–10% | Optimize — look for cost reduction (negotiate COGS, reduce return rate, adjust price) |
| 0–5% | Reprice or restructure — raise price, cut ad spend, renegotiate fees, or rebundle |
| < 0% | Kill or dramatically restructure — exit channel, discontinue SKU, or complete repositioning |

**Additional analyses to include:**
- Sensitivity table: how does margin change if price moves ±$2, ±$5
- Break-even volume: how many units must sell to cover fixed costs at current margin
- Channel comparison: same SKU side-by-side across all channels
- Top 10 and bottom 10 SKUs by contribution margin
- Margin trend: compare current margins to 3 and 6 months ago

**Output:** Complete profit waterfall table per SKU per channel, decision flags, and recommended actions.

## Worked Examples

### Example 1 — DTC Skincare Brand, 15 SKUs, Shopify + Amazon FBA

**Context:** A skincare brand selling 15 SKUs through their Shopify DTC store and Amazon FBA. Monthly revenue is $180K ($120K DTC, $60K Amazon). The founder believes DTC is more profitable because gross margins are higher, but cash flow does not reflect this.

**Step 1 — COGS:** Landed cost ranges from $4.20 (30ml serum) to $11.80 (full skincare kit). The brand sources from South Korea with 6.5% duty on cosmetics. Average landed cost is $7.40 per unit including freight at $0.85/unit by ocean and duty at $0.48/unit.

**Step 2 — Fees:** DTC: Shopify Basic ($39/mo ÷ 4,000 units = $0.01) + Shopify Payments (2.9% + $0.30) = $1.17 average. Amazon: 8% referral ($2.40) + FBA fee ($3.86 average) + storage ($0.18/unit/month) = $6.44 average.

**Step 3 — Shipping:** DTC: 3PL pick-pack ($2.50) + USPS Priority ($6.20 average) + materials ($0.45) = $9.15. Amazon FBA: included in FBA fee above.

**Step 4 — Ad spend:** DTC runs Meta ads at 4.2x ROAS. $28,600/month ÷ $120K revenue = 23.8% of DTC revenue = $7.14 per unit at $30 ASP. Amazon runs Sponsored Products at 6.8x ROAS. $8,800/month ÷ $60K = 14.7% = $4.41 per unit at $30 ASP.

**Step 5 — Returns:** DTC return rate: 8% (skincare returns are low). Cost per return: $6 reverse logistics + $12 product loss (opened, unsellable) + $1 restocking = $19. Per-unit return cost: 0.08 × $19 = $1.52. Amazon return rate: 5%. Amazon handles returns, but charges per return. Per-unit return cost: 0.05 × $15 = $0.75.

**Step 6 — Overhead:** $22,000/month total overhead. Revenue-weighted: DTC gets $14,667 (66.7%), Amazon gets $7,333 (33.3%). Per unit: DTC $3.67/unit (4,000 units), Amazon $3.67/unit (2,000 units).

**Step 7 — Waterfall:**

| Line Item | DTC ($30 ASP) | Amazon ($30 ASP) |
|-----------|--------------|-----------------|
| Retail price | $30.00 | $30.00 |
| − Platform fees | −$1.17 | −$6.44 |
| = Net after fees | $28.83 | $23.56 |
| − COGS | −$7.40 | −$7.40 |
| = Gross profit | $21.43 | $16.16 |
| − Shipping/fulfillment | −$9.15 | $0.00 |
| = After fulfillment | $12.28 | $16.16 |
| − Ad spend | −$7.14 | −$4.41 |
| = Contribution pre-returns | $5.14 | $11.75 |
| − Returns | −$1.52 | −$0.75 |
| = Contribution post-returns | $3.62 | $11.00 |
| − Overhead | −$3.67 | −$3.67 |
| = Net contribution | −$0.05 | $7.33 |
| Net margin | −0.2% | 24.4% |

**Insight:** DTC is actually break-even to slightly unprofitable at the per-unit level despite higher gross margins. The combination of expensive 3PL shipping ($9.15 vs. $0 for FBA) and higher ad cost (23.8% vs. 14.7%) wipes out the fee advantage. Recommendations: negotiate 3PL rates, test higher DTC pricing ($33–35), reduce Meta ad spend on low-converting SKUs, and shift inventory allocation toward Amazon.

### Example 2 — Apparel Brand, 40 SKUs, DTC + TikTok Shop + Amazon

**Context:** An apparel brand doing $350K/month across Shopify DTC ($200K), TikTok Shop ($90K), and Amazon ($60K). High return rates are suspected of eroding margins but the founder has never quantified the impact.

**Step 1 — COGS:** Average landed cost $12.50 per unit. Includes $8.00 factory, $1.80 freight (air for replenishment), $1.00 duty (12.5% on apparel), $1.20 packaging, $0.50 quality inspection.

**Step 7 — Waterfall Summary (hero product: $45 hoodie):**

| Line Item | DTC | TikTok Shop | Amazon FBA |
|-----------|-----|-------------|------------|
| Retail price | $45.00 | $42.00 | $45.00 |
| − Platform fees | −$1.61 | −$5.88 | −$8.10 |
| − COGS | −$12.50 | −$12.50 | −$12.50 |
| − Shipping | −$8.40 | −$7.20 | $0.00 |
| − Ad spend (channel ROAS) | −$11.25 | −$6.30 | −$5.40 |
| − Returns (28% DTC, 18% TT, 22% AMZ) | −$7.56 | −$4.86 | −$5.94 |
| − Overhead | −$2.80 | −$2.80 | −$2.80 |
| = Net contribution | $0.88 | $2.46 | $10.26 |
| Net margin | 2.0% | 5.9% | 22.8% |

**Insight:** The $45 hoodie barely breaks even on DTC and TikTok Shop. Returns are the primary margin killer — at 28% return rate with $27 fully-loaded cost per return, DTC loses $7.56 per unit sold to returns alone. Recommendations: implement fit quiz to reduce returns by 5–8 points, raise DTC price to $49, audit TikTok affiliate commission structure, and prioritize Amazon inventory allocation for this SKU.

## Common Mistakes

1. **Using gross margin as the decision metric.** Gross margin (revenue minus COGS) ignores the majority of per-unit costs. A SKU can have 70% gross margin and negative contribution margin. Always use the full waterfall.

2. **Treating shipping as a single line item.** Outbound shipping on DTC is fundamentally different from FBA fulfillment fees. One is variable by zone and weight; the other is tiered by product size. Lumping them together misses optimization opportunities.

3. **Ignoring returns in unit economics.** Returns are not just a revenue reversal. They carry real costs — reverse logistics, product loss, restocking — that can add $5–20 per unit sold depending on category and return rate.

4. **Applying blended ad spend across all SKUs.** Hero products and tail SKUs have dramatically different relationships with advertising. A hero driving most of the ad-attributed revenue subsidizes tail SKUs that would show negative margin if ad spend were properly allocated.

5. **Forgetting platform-specific fees.** Amazon alone has 6+ distinct fee types. TikTok Shop has affiliate commissions that do not exist on other platforms. Every channel must be mapped individually.

6. **Using stale COGS data.** Suppliers raise prices, freight rates fluctuate, and duty rates change. COGS should be updated at minimum quarterly or with every new PO.

7. **Excluding overhead entirely.** Fixed costs feel disconnected from unit economics, but contribution margin must cover overhead. Showing the overhead line separately is better than ignoring it.

8. **Not modeling the return cost per unit sold.** The correct formula is: return rate × cost per return = cost per unit SOLD (not per unit returned). This amortizes return costs across all units, including those that are never returned.

9. **Confusing channel revenue with channel profit.** A channel doing $100K/month in revenue and 5% margin contributes $5K. A channel doing $40K/month at 25% margin contributes $10K. Budget and inventory allocation should follow contribution dollars, not revenue.

10. **Building the model once and never updating it.** Costs change constantly. A profit waterfall is only useful if it is recalculated monthly with fresh data. Build the model to be easily refreshable.

## Resources

- **Output template:** See `references/output-template.md` for the full profit waterfall template with all 7 sections.
- **Fee schedule reference:** See `references/fee-schedule-reference.md` for current platform fee structures across Amazon, Shopify, TikTok Shop, and Walmart.
- **Sensitivity analysis guide:** See `references/sensitivity-analysis-guide.md` for price and cost scenario modeling methodology.
- **Quality checklist:** See `assets/quality-checklist.md` for the 55-item quality checklist to validate your analysis before presenting.
