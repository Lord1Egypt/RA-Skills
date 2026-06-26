---
name: Profit Margin Analyzer
description: Calculate true per-product profitability by mapping all cost layers — COGS, platform fees, payment processing, shipping, returns, and advertising — to reveal actual unit economics and identify margin leaks across an e-commerce catalog.
---

# Profit Margin Analyzer

Calculate true per-product profitability by mapping all cost layers — COGS, platform fees, payment processing, shipping, returns, and advertising — to reveal actual unit economics and identify margin leaks across an e-commerce catalog. This skill transforms raw cost data and platform fee schedules into a complete margin picture at the SKU level, exposing products that appear profitable on a gross margin basis but destroy value once all costs are loaded. It accounts for the full cost stack from landed cost through post-sale returns and produces actionable improvement scenarios with specific dollar-impact estimates.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Cost data completeness | All cost layers captured per SKU: COGS, fees, shipping, returns, ad spend with source documentation | Major cost categories covered but some estimated (e.g., overhead allocated by percentage) | Only COGS and selling price known — fees, shipping, returns lumped or missing |
| Fee mapping accuracy | Platform-specific fee schedules applied per product category, size tier, and fulfillment method | Blended average fee rates applied across the catalog | Single flat percentage assumed for all marketplace fees |
| Unit economics granularity | Per-SKU contribution margin calculated with all variable costs itemized | Category-level margin analysis with representative SKU sampling | Portfolio-level gross margin only — no product-level breakdown |
| Margin leak identification | Specific cost drivers quantified per product with root cause and dollar impact ranked | Top margin leaks identified at category level with directional impact | No systematic identification — just "margins are low" |
| Improvement modeling | Scenarios modeled with specific levers, realistic assumptions, and projected P&L impact | High-level estimates of improvement from 2-3 generic strategies | No improvement scenarios — report ends at diagnosis |
| Advertising cost integration | Ad spend allocated to SKU level using campaign/ASIN data with ACoS and TACoS calculated | Ad spend allocated at category or brand level with blended ACoS | Ad spend treated as a fixed overhead — not attributed to products |

## Solves

- You see healthy top-line revenue but cannot explain why net profit is thin, and you need a full cost waterfall from selling price to true profit per unit
- Your Amazon seller account shows positive margins in Seller Central but you suspect FBA fees, storage fees, and referral fees are eating more than you realize on certain ASINs
- You sell across multiple channels (Amazon, Shopify, wholesale) and need to understand which channel delivers the best margin per product after all channel-specific costs
- You want to rationalize your catalog by cutting or repricing products that are margin-negative once all costs are loaded, but you lack the analysis to identify which ones
- Your advertising spend has grown but you do not know which products generate profitable sales after ad costs versus which products lose money on every ad-driven sale
- You are negotiating with suppliers and need to know exactly how much COGS reduction per unit would impact your bottom line after all downstream costs are factored in
- Your return rate varies by product and you need to quantify the true cost of returns — not just the refund, but restocking, disposal, shipping, and the referral fee you already paid

## Workflow

### Step 1 — Gather cost data across all layers
Collect the complete cost stack for each product in the catalog. Required data: (1) COGS/landed cost per unit including manufacturing, tariffs, duties, and inbound freight. (2) Selling price by channel, net of any coupons or promotions. (3) Platform fee schedules — Amazon referral fee percentages by category, FBA fee tables by size/weight tier, monthly storage rates, payment processing rates for DTC channels. (4) Outbound shipping costs by method and destination zone. (5) Return rates and return processing costs per product. (6) Advertising spend at the SKU or campaign level. (7) Any other variable costs: prep/labeling fees, packaging, inserts, warranty claims. Source this from platform reports (Amazon Fee Preview, Shopify transaction exports), supplier invoices, 3PL rate cards, and ad platform exports.

### Step 2 — Map cost structure to each product
Build the cost waterfall for each SKU by applying the correct fee schedule and rate to that product's specific attributes. Amazon referral fees vary by category (8% for consumer electronics, 15% for most other categories, 17% for clothing). FBA fees depend on size tier and weight — a 1 lb standard-size item costs ~$3.22 while a 3 lb item costs ~$4.90. Do not use blended averages across the catalog; each product must carry its actual fees. For multi-channel products, build separate cost stacks per channel. Map advertising costs to the products they drove sales for, using campaign-level data where available or allocating by revenue share where not.

### Step 3 — Calculate unit economics for every SKU
For each product on each channel, calculate the full unit economics waterfall:

| Line Item | Calculation |
|---|---|
| Selling Price | Net price after coupons/promotions |
| − COGS (Landed) | Manufacturing + tariffs + inbound freight |
| = Gross Margin | |
| − Referral / Marketplace Fee | Category-specific percentage of selling price |
| − Fulfillment Fee | FBA fee or 3PL pick/pack/ship cost |
| − Payment Processing | ~2.9% + $0.30 for DTC; included in referral fee for Amazon |
| − Outbound Shipping | Carrier cost for DTC; included in FBA fee for Amazon |
| − Storage Cost | Monthly storage allocated per unit based on inventory turns |
| − Return Cost | Return rate × (return shipping + restocking + lost referral fee) |
| − Advertising Cost | Ad spend per unit sold (spend ÷ attributed units) |
| = Net Contribution Margin | True per-unit profit after all variable costs |

### Step 4 — Analyze margin distribution by product and category
Segment the catalog by margin performance. Classify each SKU into tiers: (1) Strong margin (>25% net contribution margin) — protect and grow. (2) Healthy margin (15-25%) — maintain and optimize. (3) Thin margin (5-15%) — investigate for improvement opportunities. (4) Breakeven (0-5%) — immediate action required. (5) Margin-negative (<0%) — reprice, restructure, or discontinue. Calculate the revenue-weighted margin for each category and channel. Identify the Pareto distribution: which 20% of SKUs generate 80% of total contribution dollars, and which SKUs consume margin from the winners.

### Step 5 — Identify margin leaks
Systematically examine each cost layer for leaks — costs that are disproportionately high relative to the product's price or category benchmarks. Common margin leaks: (1) Products in a high-referral-fee category that could qualify for a lower fee with category reclassification. (2) Products just above a FBA size/weight tier threshold — a small dimension or weight reduction drops them to a cheaper tier. (3) Products with return rates above 10% where return costs consume the contribution margin. (4) Products with ACoS above 30% where advertising costs exceed the margin they generate. (5) Products with slow inventory turns accumulating storage fees that erode margins over time. (6) Products where DTC shipping costs exceed what the customer pays in shipping fees. Rank margin leaks by total annual dollar impact.

### Step 6 — Model improvement scenarios
For each identified margin leak and for the portfolio overall, model specific improvement scenarios with projected impact. Examples: "Reducing COGS by 8% through supplier renegotiation on top-20 SKUs adds $42,000 in annual contribution." "Reducing packaging dimensions on 12 SKUs to qualify for the next lower FBA size tier saves $18,400/year in fulfillment fees." "Cutting ad spend on 8 SKUs with ACoS above 40% while maintaining organic rank saves $24,000 with an estimated 15% revenue decline on those SKUs." Each scenario should state the lever, the assumption, the projected margin improvement per unit and annually, and the risk or tradeoff involved.

### Step 7 — Produce the margin report
Compile the analysis into a structured report containing: executive summary with portfolio-level margin metrics, cost structure breakdown showing where each dollar of revenue goes, product-level margin table sorted by contribution margin, margin distribution analysis with tier classification, ranked margin leak list with dollar impact, improvement scenarios with projected ROI, constraint validation (are improvement assumptions realistic?), and next steps with specific actions, owners, and timelines. Include methodology notes explaining fee schedules used, allocation methods, and data limitations.

## Example 1: Amazon FBA Seller (80 SKUs)

**Input data**: Amazon Business Reports, FBA Fee Preview, advertising reports, and supplier invoices for an 80-SKU home and kitchen catalog doing $2.4M annually on Amazon.

**Cost structure analysis**:

| Cost Layer | % of Revenue | Annual $ | Notes |
|---|---|---|---|
| COGS (Landed) | 32.0% | $768,000 | Avg landed cost $9.60/unit |
| Amazon Referral Fee | 15.0% | $360,000 | Home & Kitchen category at 15% |
| FBA Fulfillment Fee | 12.8% | $307,200 | Mix of standard and oversize |
| FBA Storage Fee | 2.1% | $50,400 | Includes long-term storage surcharges |
| Advertising (PPC) | 8.5% | $204,000 | Blended ACoS of 22%, TACoS of 8.5% |
| Returns Processing | 3.2% | $76,800 | 8.4% average return rate |
| **Total Costs** | **73.6%** | **$1,766,400** | |
| **Net Contribution** | **26.4%** | **$633,600** | |

**Margin tier distribution**:

| Tier | SKU Count | Revenue Share | Contribution Share |
|---|---|---|---|
| Strong (>25%) | 18 SKUs | 34% | 52% |
| Healthy (15-25%) | 27 SKUs | 38% | 35% |
| Thin (5-15%) | 22 SKUs | 19% | 11% |
| Breakeven (0-5%) | 8 SKUs | 6% | 1% |
| Negative (<0%) | 5 SKUs | 3% | −1% |

**Top margin leaks identified**:
1. 11 SKUs just above the FBA large standard-size threshold — reducing box dimensions by 0.5" on 7 of them drops fulfillment fees by $1.40/unit, saving $38,200/year
2. 5 margin-negative SKUs collectively lose $18,500/year — 3 can be repriced upward (low price elasticity based on BSR stability), 2 should be discontinued
3. 14 SKUs with ACoS above 35% are spending $67,000/year in ads generating only $191,000 in revenue — reducing bids on the 6 worst performers saves $28,000 with estimated 8% revenue loss on those SKUs
4. 9 SKUs have return rates above 15%, costing $34,000/year in return processing — listing improvements (better images, sizing info) projected to reduce returns by 25%, saving $8,500/year

**Projected improvement**: Executing all four initiatives adds $93,200 in annual contribution margin, improving portfolio net margin from 26.4% to 30.3%.

## Example 2: DTC Shopify Brand (35 SKUs)

**Input data**: Shopify analytics, Stripe payment reports, ShipStation export, Google/Meta ad reports, and supplier invoices for a 35-SKU skincare brand doing $1.1M annually through its Shopify store.

**Cost structure analysis**:

| Cost Layer | % of Revenue | Annual $ | Notes |
|---|---|---|---|
| COGS (Landed) | 22.0% | $242,000 | Premium ingredients, avg $11.00/unit |
| Payment Processing | 2.9% | $31,900 | Stripe at 2.9% + $0.30/transaction |
| Shipping (Outbound) | 6.8% | $74,800 | Avg $3.40/order, free shipping offered over $50 |
| Packaging & Inserts | 1.8% | $19,800 | Branded boxes, tissue, samples |
| Returns & Exchanges | 2.4% | $26,400 | 5.2% return rate, free return shipping offered |
| Advertising (Meta + Google) | 18.5% | $203,500 | Blended ROAS of 5.4x |
| Shopify Subscription + Apps | 0.9% | $9,900 | Advanced plan + 8 paid apps |
| **Total Costs** | **55.3%** | **$608,300** | |
| **Net Contribution** | **44.7%** | **$491,700** | |

**Key findings**:
- Advertising is the largest cost layer after COGS at 18.5% of revenue, and it varies wildly by SKU: hero products acquire customers at 12% ACoS while long-tail SKUs run at 35%+ ACoS
- Free shipping on orders over $50 costs $74,800/year — orders between $50-$60 have an effective shipping margin of −8% because the shipping cost exceeds the margin increment from the upsell
- 6 SKUs with AOV under $25 are margin-negative after shipping and payment processing are loaded: the $3.40 shipping + $1.03 payment processing on a $22 product with 78% gross margin leaves only $13.66, which disappears once ad costs are applied
- Subscription orders (28% of revenue) have 22% higher net margin than one-time purchases because ad cost is zero on repeat orders

**Improvement scenarios**:
1. Raising the free shipping threshold from $50 to $65 increases average order value by an estimated 12% and reduces shipping cost per revenue dollar by 18%, adding $31,000/year
2. Bundling the 6 low-AOV SKUs into sets with minimum $40 price points eliminates negative-margin standalone orders, adding $14,000/year
3. Shifting 15% of Meta ad budget to email/SMS retention campaigns (lower CAC) improves blended ad efficiency from 18.5% to 15.8% of revenue, adding $29,700/year
4. Negotiating a volume shipping rate (current volume qualifies for commercial plus pricing) reduces per-package cost by $0.45, saving $9,900/year

**Projected improvement**: Combined initiatives add $84,600 in annual contribution, lifting net margin from 44.7% to 52.4%.

## Common Mistakes

1. **Using gross margin as a proxy for profitability**: Gross margin (revenue minus COGS) ignores 40-60% of actual costs in e-commerce. A product with 70% gross margin can be margin-negative once platform fees, fulfillment, shipping, returns, and advertising are loaded. Always calculate net contribution margin with all variable costs included.

2. **Applying blended fee rates across the catalog**: Using an average 13% referral fee rate when your catalog spans categories from 8% to 17% dramatically misrepresents margins. Amazon referral fees, FBA fees, and shipping costs all vary by product attributes — each SKU must carry its actual fee burden.

3. **Ignoring the true cost of returns**: Return cost is not just the refund amount. It includes the original referral fee (which Amazon does not refund in full), return shipping, restocking/inspection labor, potential disposal of unsellable units, and the lost opportunity cost. A 10% return rate on a product with $5 in return processing costs per unit is a 10% × $5 = $0.50/unit hidden cost.

4. **Treating advertising as a fixed overhead instead of a variable cost per product**: Allocating ad spend evenly across the catalog or treating it as a lump overhead hides the reality that some products are profitable after ad costs and others are not. Attribute ad spend to the SKUs or campaigns that generated the sales.

5. **Neglecting storage fees on slow-moving inventory**: A product with healthy per-unit margins can become unprofitable if it sits in FBA warehouses for 6+ months accumulating storage fees and long-term storage surcharges. Calculate annualized storage cost per unit based on actual inventory velocity, not just the monthly per-cubic-foot rate.

6. **Overlooking FBA size tier boundaries**: FBA fulfillment fees jump significantly at tier boundaries. A product that is 18.1 inches on its longest side pays oversize fees versus standard-size fees at 18.0 inches — a difference of $4-8 per unit. Always check whether products near tier boundaries can be repackaged to qualify for a cheaper tier.

7. **Not accounting for payment processing on DTC channels**: On Shopify or other DTC platforms, payment processing fees (2.9% + $0.30 per transaction) are a meaningful cost that compounds on low-AOV products. A $15 product loses 4.9% to payment processing alone ($0.30 fixed fee is 2% on its own). This is especially impactful on channels where you also pay shipping.

8. **Calculating margins on listed price instead of net realized price**: Coupons, promotions, Subscribe & Save discounts, and negotiated wholesale prices all reduce the effective selling price. Calculate margins on the actual revenue received per unit — not the listed price — to avoid overstating profitability.

## Resources

- [Output template](references/output-template.md) — Structured format for presenting profit margin analysis reports
- [Cost structure guide](references/cost-structure-guide.md) — Detailed breakdown of all cost layers with fee schedules, formulas, and allocation methods
- [Margin optimization playbook](references/margin-optimization-playbook.md) — Strategies and decision frameworks for improving margins across every cost layer
- [Quality checklist](assets/quality-checklist.md) — Pre-delivery validation checklist for margin analysis reports
