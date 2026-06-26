---
name: Influencer ROI
description: Calculate and compare return on investment across influencer partnerships by tracking full attribution from creator content to actual sales, factoring in product seeding costs, commissions, content licensing fees, and assisted conversions.
---

# Influencer ROI

Influencer marketing spend is notoriously hard to measure because attribution is fragmented across platforms, discount codes get shared beyond the intended creator, and brands rarely account for hidden costs like product seeding, shipping samples, and content licensing fees. This skill builds a comprehensive ROI model for each creator partnership, giving ecommerce operators a clear picture of which influencers actually drive profitable sales versus those who merely generate vanity metrics.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|----------|--------|------------|------|
| Attribution method | UTM + unique discount code | Discount code only | Platform self-reported |
| Cost tracking | All-in (seeding + shipping + commission + licensing) | Commission + fee only | Commission only |
| Comparison window | Normalized 30-day window | Full campaign duration | No normalization |
| ROAS benchmark | Category-specific target | Platform average | No benchmark |
| Assisted conversion credit | Partial credit via touch model | Last-click only | Ignored |
| Renewal decision | Data-driven ROI threshold | Gut feel + engagement | Follower count |

## Solves

1. **Hidden cost blindness** — Most brands track commission but miss seeding ($50–300/unit), shipping ($8–25), and licensing fees ($500–5,000) that can flip a "profitable" creator to negative margin.
2. **Attribution leakage** — Discount codes get shared on coupon sites; this skill flags suspicious attribution gaps between code usage and creator audience size.
3. **Vanity metric traps** — High views and likes don't equal sales; the skill surfaces CPA and ROAS so you can deprioritize high-engagement, low-conversion creators.
4. **Cross-platform comparison** — Normalizes metrics across TikTok, Instagram, YouTube, and Pinterest so you compare apples to apples.
5. **Renewal timing** — Gives you a ranked creator profitability table so budget allocation decisions before the next cycle are objective.
6. **Assisted conversion credit** — Captures the brand awareness lift from creators whose audience converts later via other channels.
7. **Budget forecasting** — Projects expected revenue from a proposed creator mix using historical per-creator ROAS.

## Workflow

### Step 1 — Gather Raw Campaign Data
Collect for each creator: platform, follower count, views/impressions, clicks, attributed orders, attributed revenue, and the time period. Pull from your ecommerce backend (Shopify, WooCommerce) filtered by UTM source or discount code, not from creator or platform self-reported numbers.

### Step 2 — Compile Full Cost Breakdown
For each creator record: product seeding cost (unit cost × quantity sent), shipping cost for samples, agreed commission amount or flat fee, any content licensing or usage rights fee, and agency/management fee if applicable. Sum these into Total Creator Cost (TCC).

### Step 3 — Adjust for Attribution Leakage
Check whether the discount code appears on coupon aggregator sites (RetailMeNot, Honey, etc.). If code usage significantly exceeds the creator's reach, flag the creator as "leaky" and apply a leakage discount factor (typically 15–40%) to their attributed revenue.

### Step 4 — Calculate Core Metrics Per Creator
- **Net Revenue** = Attributed Revenue × (1 − Leakage Factor)
- **Gross Profit** = Net Revenue × Gross Margin %
- **Net Profit** = Gross Profit − TCC
- **ROAS** = Net Revenue ÷ TCC
- **CPA** = TCC ÷ Attributed Orders
- **CPM** = (TCC ÷ Impressions) × 1,000

### Step 5 — Normalize to 30-Day Window
Campaigns run for different durations. Divide all volume metrics (orders, revenue, impressions) by campaign days, then multiply by 30 to create a normalized monthly view that makes cross-creator comparison fair.

### Step 6 — Apply Assisted Conversion Credit
Identify customers who saw creator content (UTM touch) but converted through another channel within 30 days. Apply a 20% assisted conversion revenue credit to each relevant creator (adjustable based on your attribution philosophy).

### Step 7 — Rank and Recommend
Sort creators by Net Profit (descending). Flag creators above your ROAS threshold as "Renew," those within 20% below as "Test Again," and those significantly below as "Pause." Generate a ranked profitability table and a budget allocation recommendation for the next cycle.

## Examples

### Example 1 — Micro-Influencer vs. Macro-Influencer Comparison

**Input:**
```
Creator A (Micro, 45K followers, TikTok):
- Views: 180,000 | Clicks: 2,100 | Orders: 89 | Revenue: $8,010
- Costs: $120 product + $18 shipping + $450 flat fee + $0 licensing = $588 TCC
- Campaign: 21 days | Discount code clean (no leakage detected)

Creator B (Macro, 890K followers, Instagram):
- Views: 1,200,000 | Clicks: 4,800 | Orders: 156 | Revenue: $14,040
- Costs: $360 product (3 units) + $45 shipping + $3,500 flat fee + $1,000 licensing = $4,905 TCC
- Campaign: 28 days | Discount code found on 2 coupon sites (25% leakage factor applied)
```

**Output:**
| Metric | Creator A | Creator B |
|--------|-----------|-----------|
| Adjusted Revenue | $8,010 | $10,530 |
| Gross Profit (60% margin) | $4,806 | $6,318 |
| Net Profit | **$4,218** | **$1,413** |
| ROAS | 13.6x | 2.1x |
| CPA | $6.61 | $31.44 |
| 30-day norm orders | 127 | 167 |
| Decision | ✅ Renew | ⚠️ Test Again |

**Insight:** Creator A delivers 6.5× more net profit per dollar spent despite 20× fewer followers. Creator B's high reach is negated by leakage, high licensing costs, and lower conversion rate.

---

### Example 2 — YouTube Long-Form Attribution with Assisted Conversions

**Input:**
```
Creator C (Mid-tier, 210K YouTube subscribers):
- Views: 95,000 | Clicks: 1,650 | Direct orders: 43 | Direct revenue: $6,450
- Costs: $280 product + $22 shipping + $800 flat fee + $500 licensing = $1,602 TCC
- Campaign: 45 days | Assisted conversions identified: 31 orders, $4,650 additional revenue
- Assisted credit rate: 20%
```

**Calculations:**
- Assisted Revenue Credit = $4,650 × 20% = $930
- Total Adjusted Revenue = $6,450 + $930 = $7,380
- Gross Profit = $7,380 × 62% = $4,576
- Net Profit = $4,576 − $1,602 = **$2,974**
- ROAS = $7,380 ÷ $1,602 = **4.6x**
- Without assisted credit: ROAS = 4.0x → same renewal decision, but more accurate budget justification

**Decision:** Renew. YouTube long-form drives strong late-funnel conversion. Increase budget for next cycle.

---

## Common Mistakes

1. **Using platform-reported revenue instead of backend-verified orders.** Platforms over-attribute. Always verify against your Shopify/WooCommerce order data filtered by UTM or discount code.

2. **Forgetting product seeding costs.** A beauty brand sending 5 full-size sets ($60 each) to a creator effectively spends $300 before any fee is paid. Missing this can make a negative-margin creator look profitable.

3. **Comparing campaigns of different lengths without normalization.** A 7-day flash campaign versus a 60-day evergreen post are not directly comparable without per-day normalization.

4. **Ignoring discount code leakage.** Codes shared on Honey or RetailMeNot can inflate a creator's attributed revenue by 2–5×. Check aggregator sites before finalizing ROI.

5. **Treating all ROAS the same across product margins.** A 4x ROAS on a 70% margin product is very different from 4x on a 30% margin product. Always calculate net profit, not just revenue ROAS.

6. **Overlooking agency markup.** If you use an influencer agency, their 15–25% management fee is a real cost that belongs in TCC.

7. **Conflating brand awareness with direct response.** Macro-influencers often drive awareness that converts through other channels later. Use a 30–60 day attribution window for assisted conversions.

8. **Renewing based on follower count growth.** A creator who doubled their following during your campaign but delivered negative ROI should not be renewed on audience size alone.

9. **Missing content licensing costs.** If you repurpose creator content for paid ads, you owe a licensing fee. Forgetting this until the invoice arrives distorts initial ROI calculations.

10. **Ignoring seasonal indexing.** Q4 ROAS for a gift product will always outperform Q1. Normalize performance against seasonal baselines before comparing cohorts.

## Resources

- [Output Template](references/output-template.md) — Structured ROI report template
- [Attribution Guide](references/attribution-guide.md) — UTM setup and leakage detection methodology
- [Creator Cost Tracker](references/creator-cost-tracker.md) — Full cost breakdown worksheet
- [Quality Checklist](assets/checklist.md) — Pre-publish accuracy checklist
