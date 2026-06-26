# E-Commerce Cost Structure Guide

## Overview

E-commerce profitability depends on understanding and accurately mapping every cost layer between the selling price and true profit. Most sellers track COGS and selling price but underestimate or misallocate the intermediate costs — platform fees, fulfillment, shipping, returns, and advertising — that collectively consume 30-50% of revenue. This guide details each cost layer with specific rates, formulas, and allocation methods.

## Layer 1: COGS and Landed Cost

### Components

| Cost Element | Description | Typical Range |
|---|---|---|
| Manufacturing / Purchase | Cost to produce or procure the unit | 20–45% of selling price |
| Tariffs / Duties | Import duties based on HTS classification | 0–25% of declared value |
| Inbound Freight (International) | Ocean/air freight from manufacturer to port | $0.10–$2.00/unit depending on size/weight |
| Customs Brokerage | Broker fees for clearing customs | $0.05–$0.30/unit (amortized across shipment) |
| Inbound Freight (Domestic) | Trucking from port to warehouse/FBA | $0.05–$0.50/unit |
| Quality Inspection | Third-party inspection at origin | $0.02–$0.15/unit (amortized) |

### Landed Cost Formula

```
Landed Cost = Purchase Price + Tariffs + International Freight + Customs Fees + Domestic Freight + Inspection
```

### Key Considerations
- Always calculate landed cost per unit by dividing total shipment costs across all units in the shipment
- Tariff rates change — verify current rates via the HTS schedule for your product classification
- Air freight vs. ocean freight: air costs 4-8x more but arrives in 5-7 days vs. 25-40 days. Use air freight cost for emergency replenishment calculations; ocean freight for baseline COGS
- For domestic products, landed cost = purchase price + inbound shipping to your warehouse or FBA

## Layer 2: Marketplace and Platform Fees

### Amazon Referral Fees (by Category)

| Category | Referral Fee % | Minimum Per-Item Fee |
|---|---|---|
| Amazon Device Accessories | 45% | $0.30 |
| Apparel & Accessories | 17% | $0.30 |
| Automotive | 12% | $0.30 |
| Baby Products | 8% (first $10), 15% (above $10) | $0.30 |
| Beauty & Personal Care | 8% (first $10), 15% (above $10) | $0.30 |
| Books | 15% | — |
| Consumer Electronics | 8% | $0.30 |
| Furniture | 15% (first $200), 10% (above $200) | $0.30 |
| Grocery & Gourmet | 8% (first $15), 15% (above $15) | — |
| Health & Household | 8% (first $10), 15% (above $10) | $0.30 |
| Home & Kitchen | 15% | $0.30 |
| Jewelry | 20% (first $250), 5% (above $250) | $0.30 |
| Lawn & Garden | 15% | $0.30 |
| Pet Supplies | 15% (first $10), 22% (above $10) | $0.30 |
| Shoes, Handbags & Sunglasses | 15% | $0.30 |
| Sports & Outdoors | 15% | $0.30 |
| Tools & Home Improvement | 15% | $0.30 |
| Toys & Games | 15% | $0.30 |
| Everything Else | 15% | $0.30 |

*Note: Fee schedules are updated by Amazon periodically. Always verify current rates at sellercentral.amazon.com/gp/help/G200336920.*

### Amazon FBA Fulfillment Fees (Standard Size)

| Size Tier | Weight Range | Fulfillment Fee |
|---|---|---|
| Small Standard | Up to 6 oz | $3.06 |
| Small Standard | 6–12 oz | $3.15 |
| Small Standard | 12 oz – 16 oz | $3.32 |
| Large Standard | Up to 6 oz | $3.45 |
| Large Standard | 6–12 oz | $3.67 |
| Large Standard | 12 oz – 1 lb | $4.07 |
| Large Standard | 1–1.5 lb | $4.41 |
| Large Standard | 1.x–2 lb | $4.68 |
| Large Standard | 2–2.5 lb | $4.90 |
| Large Standard | 2.5–3 lb | $5.16 |
| Large Standard | 3+ lb | $5.16 + $0.16/half-lb above 3 lb |

### Amazon FBA Fulfillment Fees (Oversize)

| Size Tier | Weight Range | Fulfillment Fee |
|---|---|---|
| Small Oversize | Up to 70 lb | $9.73 + $0.42/lb above first lb |
| Medium Oversize | Up to 150 lb | $19.05 + $0.42/lb above first lb |
| Large Oversize | Up to 150 lb | $89.98 + $0.83/lb above first 90 lb |
| Special Oversize | Over 150 lb | $158.49 + $0.83/lb above first 90 lb |

### FBA Size Tier Boundaries

| Tier | Max Length | Max Width | Max Height | Max Weight | Max Dimensional Weight |
|---|---|---|---|---|---|
| Small Standard | 15" | 12" | 0.75" | 16 oz | — |
| Large Standard | 18" | 14" | 8" | 20 lb | — |
| Small Oversize | 60" | 30" | — | 70 lb | — |
| Medium Oversize | 108" | — | — | 150 lb | — |

*Critical: Products near tier boundaries should be evaluated for packaging optimization. Crossing from Large Standard to Small Oversize adds $4-6 per unit in fulfillment fees.*

### Amazon Storage Fees

| Period | Standard Size (per cubic foot/month) | Oversize (per cubic foot/month) |
|---|---|---|
| January – September | $0.87 | $0.56 |
| October – December | $2.40 | $1.40 |

**Long-Term Storage Surcharge**: $6.90 per cubic foot or $0.15 per unit (whichever is greater) for inventory stored over 271 days. Assessed monthly on the 15th.

**Storage Cost per Unit Formula**:
```
Monthly Storage Cost/Unit = (Unit Volume in cubic feet) × (Monthly rate per cubic foot)
Annualized Storage Cost/Unit = Monthly Storage × 12 (adjust for Q4 rate)
Effective Storage/Unit = Annualized Storage Cost ÷ Inventory Turns per Year
```

### Shopify Fees

| Component | Basic Plan | Shopify Plan | Advanced Plan |
|---|---|---|---|
| Monthly Subscription | $39/month | $105/month | $399/month |
| Online Credit Card Rate | 2.9% + $0.30 | 2.7% + $0.30 | 2.5% + $0.30 |
| In-person Credit Card Rate | 2.6% + $0.10 | 2.5% + $0.10 | 2.4% + $0.10 |
| Third-Party Payment Provider Fee | 2.0% | 1.0% | 0.6% |
| Transaction Fee (Shopify Payments) | 0% | 0% | 0% |

### Other Marketplace Fees

| Platform | Commission / Fee | Notes |
|---|---|---|
| Walmart Marketplace | 6–20% (category-dependent) | No monthly subscription fee |
| eBay | 3–15% final value fee + $0.30/order | Varies by category; store subscription reduces rates |
| Etsy | 6.5% transaction fee + 3% + $0.25 payment processing | Plus $0.20 listing fee per item |
| Target Plus | 5–15% commission | Invitation-only marketplace |
| TikTok Shop | 5% + $0.30 payment processing | Introductory rates may apply |

## Layer 3: Payment Processing

### Fee Structures

| Provider | Rate | Fixed Fee | Notes |
|---|---|---|---|
| Stripe | 2.9% | $0.30 | Standard online rate |
| PayPal | 3.49% | $0.49 | Standard online rate |
| Shopify Payments | 2.5–2.9% | $0.30 | Depends on plan tier |
| Square (Online) | 2.9% | $0.30 | Standard rate |
| Amazon Pay | 2.9% | $0.30 | For off-Amazon checkout |

### Payment Processing Cost Formula

```
Payment Processing Cost = (Selling Price × Rate %) + Fixed Fee per Transaction
```

**Impact on Low-AOV Products**: The fixed fee component ($0.30) has a disproportionate impact on low-priced items:

| Selling Price | Processing Cost (2.9% + $0.30) | Effective Rate |
|---|---|---|
| $10.00 | $0.59 | 5.9% |
| $20.00 | $0.88 | 4.4% |
| $30.00 | $1.17 | 3.9% |
| $50.00 | $1.75 | 3.5% |
| $100.00 | $3.20 | 3.2% |

*Note: On Amazon, payment processing is bundled into the referral fee — there is no separate charge. On DTC channels, payment processing is always a separate cost.*

## Layer 4: Shipping Costs

### Outbound Shipping (DTC)

| Carrier / Service | Weight Range | Approximate Cost | Transit Time |
|---|---|---|---|
| USPS Ground Advantage | Up to 1 lb | $3.50–$5.50 | 2–5 days |
| USPS Ground Advantage | 1–5 lb | $5.50–$9.00 | 2–5 days |
| USPS Priority Mail | Up to 1 lb | $7.00–$9.00 | 1–3 days |
| UPS Ground | 1–5 lb | $8.00–$14.00 | 1–5 days |
| UPS Ground | 5–10 lb | $12.00–$20.00 | 1–5 days |
| FedEx Ground | 1–5 lb | $8.00–$15.00 | 1–5 days |

*Rates vary by origin/destination zone. Commercial/negotiated rates are typically 20-40% below retail rates.*

### Free Shipping Economics

| Scenario | Impact |
|---|---|
| Free shipping on all orders | Full shipping cost absorbed — reduces margin by 5-12% of revenue |
| Free shipping above threshold | Increases AOV but absorbs shipping on qualifying orders |
| Flat-rate shipping | Predictable customer cost; seller absorbs difference on expensive-to-ship items |
| Exact shipping pass-through | No shipping cost burden but reduces conversion rate 10-30% |

**Free Shipping Threshold Formula**:
```
Optimal Threshold = Average Order Value × 1.2 to 1.4
```
Set the threshold 20-40% above current AOV to encourage upsell while limiting the number of orders that qualify without incremental revenue.

### Inbound Shipping to FBA

| Method | Cost Range | Use When |
|---|---|---|
| Partnered carrier (SPD) | $0.20–$0.80/unit | Small shipments, standard replenishment |
| Partnered carrier (LTL) | $0.10–$0.40/unit | Pallet-quantity shipments |
| Own carrier arrangement | Varies | Large volumes with negotiated freight rates |

*Inbound shipping is a COGS component and should be included in landed cost, not tracked separately.*

## Layer 5: Returns Processing

### Cost Components of a Return

| Component | Typical Cost | Notes |
|---|---|---|
| Return shipping label | $3.00–$8.00 | If seller provides prepaid label |
| Restocking / inspection | $1.00–$3.00 | Labor to receive, inspect, repackage |
| Amazon return processing fee | $0–$5.00+ | Charged on apparel/shoes; varies by size/weight |
| Lost referral fee | Partial refund only | Amazon refunds referral fee minus 20% of applicable fee or $5.00 (whichever is less) |
| Disposal fee (if unsellable) | $0.97–$6.90/unit | FBA removal/disposal fee |
| Value loss on returned inventory | 0–100% of COGS | Depends on product condition and resellability |

### Return Cost Formula

```
Cost per Return = Return Shipping + Restocking + Platform Return Fee + Lost Referral Fee + (Disposal Rate × Disposal Cost) + (Damage Rate × Unit COGS)
Return Cost per Unit Sold = Cost per Return × Return Rate
```

### Return Rate Benchmarks

| Category | Typical Return Rate |
|---|---|
| Apparel & Shoes | 15–30% |
| Consumer Electronics | 10–15% |
| Home & Kitchen | 5–10% |
| Beauty & Personal Care | 3–7% |
| Grocery / Consumables | 1–3% |
| Books / Media | 2–5% |
| Toys & Games | 5–10% |
| Furniture (large) | 8–15% |

## Layer 6: Advertising Costs

### Key Advertising Metrics

| Metric | Formula | Healthy Range |
|---|---|---|
| ACoS (Advertising Cost of Sale) | Ad Spend ÷ Ad-Attributed Revenue × 100 | 15–25% (category dependent) |
| TACoS (Total ACoS) | Ad Spend ÷ Total Revenue × 100 | 5–12% |
| ROAS (Return on Ad Spend) | Ad-Attributed Revenue ÷ Ad Spend | 4x–7x |
| CPA (Cost per Acquisition) | Ad Spend ÷ New Customers Acquired | Varies widely |
| CAC (Customer Acquisition Cost) | Total Marketing Spend ÷ New Customers | Should be < first-order profit |

### Advertising Cost per Unit Sold

```
Ad Cost per Unit = Total Ad Spend on Product ÷ Total Units Sold of Product
```

For Amazon Sponsored Products, attribution is at the ASIN level. For Meta/Google campaigns driving DTC traffic, attribute by campaign or use blended allocation:

```
Blended Ad Cost per Unit = Total Channel Ad Spend ÷ Total Channel Units Sold
```

### ACoS Breakeven Calculation

```
Breakeven ACoS = Net Margin Before Advertising (%)
```

If a product has a 30% margin before ad costs, any ACoS above 30% means advertising is destroying margin on those units. Products should target ACoS well below breakeven to maintain healthy net contribution.

### Ad Spend Allocation Methods

| Method | Best For | Limitation |
|---|---|---|
| Direct ASIN attribution | Amazon PPC with ASIN-level reports | Misses halo effect on organic sales |
| Campaign-level allocation | Google/Meta campaigns targeting specific products | Multi-product campaigns require splitting |
| Revenue-weighted blended | General brand spend across catalog | Overstates cost on organic sellers, understates on ad-dependent SKUs |
| Incremental ROAS | Measuring true ad-driven sales | Requires A/B test or holdout data |

## Layer 7: Overhead Allocation

### Fixed Costs Typically Excluded from Unit Economics

These costs are real but should be tracked separately from per-unit variable cost analysis:

| Cost | Monthly Range (Typical Small-Mid Seller) | Allocation Method |
|---|---|---|
| Software / SaaS tools | $200–$2,000 | Fixed cost — do not allocate per unit |
| Photography / Content | $500–$3,000 | Amortize across product lifecycle |
| Employee / VA salaries | $2,000–$15,000 | Fixed cost — track as overhead |
| Warehousing rent (non-FBA) | $1,000–$10,000 | Allocate per unit via cubic footage |
| Insurance | $100–$500 | Fixed cost |
| Professional services (legal, accounting) | $200–$2,000 | Fixed cost |

### When to Include Overhead in Unit Economics

Include overhead in unit economics only when:
1. It is directly variable with volume (e.g., pick/pack labor paid per unit)
2. You are doing a full profitability analysis including fixed cost coverage
3. You need to calculate true breakeven volume

For contribution margin analysis (the primary use of this skill), exclude fixed overhead and focus on variable costs only. This produces a clean "contribution per unit" that shows how much each sale contributes to covering fixed costs and generating profit.

## Putting It All Together: Full Cost Stack Example

### Example: $29.99 Product Sold on Amazon FBA (Home & Kitchen, 1.2 lb)

| Line Item | Amount | % of Price | Source |
|---|---|---|---|
| Selling Price | $29.99 | 100.0% | — |
| COGS (Landed) | $7.50 | 25.0% | Supplier invoice + freight allocation |
| Amazon Referral Fee (15%) | $4.50 | 15.0% | Home & Kitchen category |
| FBA Fulfillment Fee | $4.41 | 14.7% | Large Standard, 1–1.5 lb tier |
| FBA Storage (annualized) | $0.38 | 1.3% | Based on 6 inventory turns/year |
| Return Processing | $0.72 | 2.4% | 6% return rate × $12 per return |
| Advertising (PPC) | $2.40 | 8.0% | ACoS of 20% on 40% ad-attributed sales |
| **Total Costs** | **$19.91** | **66.4%** | |
| **Net Contribution** | **$10.08** | **33.6%** | |

### Example: $45.00 Product Sold on Shopify DTC (Skincare, 0.5 lb)

| Line Item | Amount | % of Price | Source |
|---|---|---|---|
| Selling Price | $45.00 | 100.0% | — |
| COGS (Landed) | $9.00 | 20.0% | Supplier invoice |
| Payment Processing (2.9% + $0.30) | $1.61 | 3.6% | Shopify Payments |
| Outbound Shipping | $4.20 | 9.3% | USPS Ground, Zone 4 avg |
| Packaging & Insert | $0.85 | 1.9% | Branded box + tissue |
| Return Processing | $0.78 | 1.7% | 4% return rate × $19.50/return |
| Advertising (Meta) | $7.65 | 17.0% | Blended CAC across channel |
| Shopify Subscription (allocated) | $0.12 | 0.3% | $105/month ÷ 875 orders/month |
| **Total Costs** | **$24.21** | **53.8%** | |
| **Net Contribution** | **$20.79** | **46.2%** | |
