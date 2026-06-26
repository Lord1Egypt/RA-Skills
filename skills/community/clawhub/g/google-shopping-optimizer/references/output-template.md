# Google Shopping Optimization Plan — Output Template

## Executive Summary

**Analysis period**: [Start date] — [End date]
**Products analyzed**: [N] SKUs across [N] categories
**Data sources**: Google Merchant Center, Google Ads Shopping campaigns, Search Terms report
**Current monthly Shopping spend**: $[amount]
**Current blended ROAS**: [X]%

### Performance Snapshot

| Metric | Current | Target | Gap |
|---|---|---|---|
| Active products (no errors) | [N] / [N total] ([%]) | 100% | [N] products to fix |
| Blended ROAS | [X]% | [X]% | [X] percentage points |
| Impression share | [X]% | [X]% | [X] percentage points |
| Click-through rate | [X]% | [X]% | [X] percentage points |
| Conversion rate | [X]% | [X]% | [X] percentage points |
| Monthly wasted spend | $[amount] | $[target] | $[savings opportunity] |
| Feed quality score | [X] / 100 | [X] / 100 | [X] points |

### Top 3 Findings

1. [Finding — e.g., "18 products disapproved due to price mismatches, representing $3,800/mo in lost revenue"]
2. [Finding — e.g., "$4,200/mo wasted on non-converting search queries that should be negated"]
3. [Finding — e.g., "Bottom 33% of SKUs consuming 28% of budget at 85% ROAS — margin-destructive"]

---

## Feed Health Audit

### Disapproval Summary

| Disapproval Type | Count | Revenue Impact (est.) | Fix Complexity | Priority |
|---|---|---|---|---|
| Price mismatch | [N] | $[amount]/mo | Low — sync feed with landing page | P0 |
| Missing GTIN/MPN | [N] | $[amount]/mo | Low — add identifiers to feed | P0 |
| Image policy violation | [N] | $[amount]/mo | Medium — reshoot or edit images | P1 |
| Policy violation (other) | [N] | $[amount]/mo | Varies | P1 |
| Availability mismatch | [N] | $[amount]/mo | Low — improve inventory sync | P0 |

### Attribute Completeness

| Attribute | Status | Products Missing | Impact | Recommendation |
|---|---|---|---|---|
| title (optimized) | [Complete/Partial] | [N] under-optimized | High — primary query matching signal | Rewrite using category templates |
| description | [Complete/Partial] | [N] missing or thin | Medium — supports free listings | Expand to 500+ characters with keywords |
| google_product_category | [Complete/Partial] | [N] missing | Medium — improves classification accuracy | Map all products to deepest category |
| additional_image_link | [Complete/Partial] | [N] missing | Medium — improves CTR | Add 2–3 lifestyle/detail images per product |
| product_highlight | [Complete/Partial] | [N] missing | Low-Medium — enhances free listings | Add 4–6 bullet points per product |
| sale_price | [Complete/Partial] | [N] not using | Medium — triggers sale badge | Add for all products with active promotions |
| custom_label_0–4 | [Complete/Partial] | [N] not configured | High — enables campaign segmentation | Configure per labeling strategy below |
| color / size / material | [Complete/Partial] | [N] missing | High (apparel) / Medium (other) | Add for all relevant products |
| shipping | [Complete/Partial] | [N] missing | Low-Medium — improves transparency | Configure account-level or product-level shipping |

---

## Title Optimization

### Category-Specific Title Templates

| Category | Template | Character Target |
|---|---|---|
| [Category 1] | Brand + Product Type + Key Feature + Size/Variant + Color | 80–120 chars |
| [Category 2] | Brand + Product Type + Material + Use Case + Pack Size | 80–120 chars |

### Title Rewrite Samples

| Product | Current Title | Optimized Title | Key Changes |
|---|---|---|---|
| [SKU] | [Current] | [Optimized] | [What was added/changed] |
| [SKU] | [Current] | [Optimized] | [What was added/changed] |
| [SKU] | [Current] | [Optimized] | [What was added/changed] |

*Include rewrites for top 10–20 products by revenue or for products with the most under-optimized titles.*

---

## Search Query Analysis

### Wasted Spend Summary

| Category | Queries | Spend (period) | Projected Annual Waste | Action |
|---|---|---|---|---|
| Irrelevant / informational | [N] | $[amount] | $[amount] | Add as negative keywords |
| Wrong product match | [N] | $[amount] | $[amount] | Add as negatives + improve titles |
| Competitor brand terms | [N] | $[amount] | $[amount] | Evaluate or negate |
| Low-intent / broad | [N] | $[amount] | $[amount] | Add as negatives |
| **Total wasted** | **[N]** | **$[amount]** | **$[amount]** | |

### Negative Keyword List

| Level | Negative Keywords | Rationale |
|---|---|---|
| Campaign-level | [keyword list] | Universally irrelevant across all products |
| Ad group: [Name] | [keyword list] | Irrelevant for this product segment |

### High-Value Converting Queries

| Query | Impressions | Clicks | Conversions | ROAS | Matched Product | Title Contains Query? |
|---|---|---|---|---|---|---|
| [query] | [N] | [N] | [N] | [X]% | [product] | [Y/N] |

*Top 20 converting queries. If title doesn't contain the query, flag as title optimization opportunity.*

---

## Campaign Structure Recommendation

### Current vs. Recommended Structure

**Current**: [Describe current structure — e.g., "1 Shopping campaign, 1 ad group, all products"]

**Recommended**:

| Campaign | Products | ROAS Target | Daily Budget | Bid Strategy |
|---|---|---|---|---|
| Shopping — Top Performers | [N] SKUs (criteria) | [X]% | $[amount] | [Maximize conversion value / Target ROAS] |
| Shopping — Core Catalog | [N] SKUs (criteria) | [X]% | $[amount] | [Target ROAS] |
| Shopping — Long Tail / Test | [N] SKUs (criteria) | [X]% | $[amount] | [Target ROAS / Maximize clicks] |
| Shopping — Brand Defense | [N] SKUs (brand queries) | [X]% | $[amount] | [Target ROAS] |

### Custom Label Configuration

| Label Slot | Values | Assignment Logic |
|---|---|---|
| custom_label_0 | [values] | [How products are assigned] |
| custom_label_1 | [values] | [How products are assigned] |
| custom_label_2 | [values] | [How products are assigned] |
| custom_label_3 | [values] | [How products are assigned] |
| custom_label_4 | [values] | [How products are assigned] |

---

## Bidding Optimization

### Product Group Bid Recommendations

| Product Group | Current Bid / ROAS Target | Recommended | Rationale |
|---|---|---|---|
| [Group] | [Current] | [Recommended] | [Why — e.g., "ROAS 780% well above target, increase investment"] |

### Device Bid Adjustments

| Device | Conversion Rate | ROAS | Recommended Adjustment |
|---|---|---|---|
| Desktop | [X]% | [X]% | Baseline (0%) |
| Mobile | [X]% | [X]% | [+/-X%] |
| Tablet | [X]% | [X]% | [+/-X%] |

### Audience Bid Adjustments

| Audience | Conversion Rate | ROAS | Recommended Adjustment |
|---|---|---|---|
| All visitors (remarketing) | [X]% | [X]% | [+X%] |
| Cart abandoners | [X]% | [X]% | [+X%] |
| Past purchasers | [X]% | [X]% | [+X%] |
| Customer match list | [X]% | [X]% | [+X%] |
| Similar audiences | [X]% | [X]% | [+/-X%] |

---

## Competitive Positioning

### Impression Share Analysis

| Category / Segment | Your Impression Share | Top Competitor | Gap | Primary Cause |
|---|---|---|---|---|
| [Segment] | [X]% | [X]% | [X] pts | [Bid / Budget / Feed quality] |

### Price Competitiveness

| Product Group | Your Avg. Price | Market Avg. Price | Position | Recommendation |
|---|---|---|---|---|
| [Group] | $[amount] | $[amount] | [Above/At/Below] | [Hold / Compete / Differentiate] |

---

## Optimization Roadmap

### Phase 1 — Critical Fixes (Week 1)

| Action | Products Affected | Expected Impact | Owner | Due Date |
|---|---|---|---|---|
| Fix price mismatches | [N] | +$[amount]/mo revenue | [Owner] | [Date] |
| Add missing GTINs | [N] | +[X]% impression share | [Owner] | [Date] |
| Fix image policy violations | [N] | +$[amount]/mo revenue | [Owner] | [Date] |

### Phase 2 — Feed Optimization (Weeks 2–3)

| Action | Products Affected | Expected Impact | Owner | Due Date |
|---|---|---|---|---|
| Rewrite titles (top 50 products) | 50 | +15–25% CTR | [Owner] | [Date] |
| Add missing attributes | [N] | +[X]% quality score | [Owner] | [Date] |
| Configure custom labels | All | Enables campaign segmentation | [Owner] | [Date] |
| Build negative keyword lists | N/A | −$[amount]/mo waste | [Owner] | [Date] |

### Phase 3 — Campaign Restructure (Weeks 3–4)

| Action | Products Affected | Expected Impact | Owner | Due Date |
|---|---|---|---|---|
| Create tiered campaign structure | All | +[X]% ROAS | [Owner] | [Date] |
| Set segment-specific ROAS targets | All | +[X]% ROAS | [Owner] | [Date] |
| Apply device bid adjustments | All | +[X]% ROAS | [Owner] | [Date] |
| Set up audience bid adjustments | All | +[X]% ROAS | [Owner] | [Date] |

### Phase 4 — Ongoing Optimization (Continuous)

| Cadence | Action |
|---|---|
| Daily | Monitor spend pacing and ROAS by campaign |
| Weekly | Review Search Terms report, add negatives, check disapprovals |
| Bi-weekly | Adjust bids by product group based on performance trends |
| Monthly | Full performance review, title refresh for seasonal terms, competitive analysis |
| Quarterly | Feed audit, campaign structure review, ROAS target recalibration |

---

## Projected Impact Summary

| Improvement | Monthly Revenue Impact | Monthly Spend Impact | ROAS Impact |
|---|---|---|---|
| Fix disapprovals | +$[amount] | $0 | +[X] pts |
| Title optimization | +$[amount] | $0 (organic CTR gain) | +[X] pts |
| Negative keyword cleanup | $0 | −$[amount] saved | +[X] pts |
| Campaign restructure + bidding | +$[amount] | [+/-$amount] | +[X] pts |
| **Combined projection** | **+$[amount]** | **[+/-$amount]** | **+[X] pts** |

---

## Methodology Notes

- **Feed audit**: All [N] products checked against Google Merchant Center product data specification (version [date])
- **Title analysis**: Titles evaluated against category-specific Shopping title best practices and Search Terms query data
- **Bidding analysis**: Based on [N] days of campaign data with statistical significance threshold of [N] conversions per segment
- **ROAS calculations**: Include all Shopping campaign costs; exclude brand search and other non-Shopping campaigns
- **Competitive data**: Sourced from Merchant Center competitive visibility report and/or Google Ads auction insights
- **Revenue projections**: Based on historical conversion rates applied to projected impression/click increases; actual results may vary

---

## Next Steps

1. [ ] Approve Phase 1 critical fixes and assign owners by [date]
2. [ ] Begin title rewrites for top 50 products by [date]
3. [ ] Configure custom labels in feed management tool by [date]
4. [ ] Build and apply negative keyword lists by [date]
5. [ ] Implement campaign restructure by [date]
6. [ ] Set up weekly performance monitoring dashboard
7. [ ] Schedule 30-day post-implementation review on [date]
