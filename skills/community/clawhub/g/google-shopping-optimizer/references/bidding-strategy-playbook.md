# Bidding Strategy Playbook

## Overview

Bidding is where Shopping campaign strategy meets execution. The right bid structure ensures top-performing products get maximum exposure while preventing low-performers from draining budget. This playbook covers campaign architecture, ROAS target setting, bid management by segment, and the transition between manual and automated bidding strategies.

## Campaign Architecture

### The Tiered Priority Model

The most effective Shopping campaign structure uses tiered campaigns to control which products receive the most investment:

**Tier 1 — Top Performers (High Priority)**
- Products: Top 15–25% by contribution margin and conversion rate
- Goal: Maximum impression share and revenue capture
- ROAS Target: Lower (more aggressive) — these products have proven economics
- Budget: 35–45% of total Shopping budget
- Monitoring: Daily spend pacing and ROAS checks

**Tier 2 — Core Catalog (Medium Priority)**
- Products: Middle 40–50% by performance
- Goal: Profitable growth with controlled spend
- ROAS Target: Moderate — balance growth with profitability
- Budget: 35–45% of total Shopping budget
- Monitoring: Weekly performance reviews

**Tier 3 — Long Tail / Testing (Low Priority)**
- Products: Bottom 25–35% by performance + new/unproven products
- Goal: Discovery and data collection at minimal cost
- ROAS Target: Higher (more conservative) or Maximize Clicks with a bid cap
- Budget: 10–20% of total Shopping budget
- Monitoring: Bi-weekly review, graduate performers to Tier 2

**Tier 4 — Brand Defense (Optional)**
- Products: All products, targeting brand queries only
- Goal: Protect branded search real estate from competitors
- ROAS Target: Aggressive — brand queries have the highest conversion rates
- Budget: 5–10% of total Shopping budget
- Monitoring: Weekly impression share on brand terms

### Product Group Segmentation

Within each campaign tier, segment products into groups for granular bid control:

| Segmentation Level | Method | When to Use |
|---|---|---|
| Category | google_product_category or product_type | Different categories have different margins and conversion rates |
| Brand | brand attribute | Own brands vs. third-party brands have different economics |
| Performance tier | custom_label (star/core/tail) | Historical performance differs within categories |
| Margin tier | custom_label (high/mid/low) | Different margin levels need different ROAS targets |
| Price range | item group by price brackets | High-AOV vs. low-AOV products convert differently |
| Seasonality | custom_label (in-season/off-season) | Seasonal products need bid adjustments by calendar period |

### Product Group Hierarchy Example

```
Campaign: Shopping — Top Performers
├── Ad Group: High-Margin Electronics
│   ├── Product Group: Brand A (ROAS target: 350%)
│   ├── Product Group: Brand B (ROAS target: 400%)
│   └── Everything else (ROAS target: 450%)
├── Ad Group: High-Margin Home
│   ├── Product Group: Furniture (ROAS target: 300%)
│   ├── Product Group: Décor (ROAS target: 400%)
│   └── Everything else (ROAS target: 450%)
└── Ad Group: High-Margin Apparel
    ├── Product Group: Women's (ROAS target: 350%)
    ├── Product Group: Men's (ROAS target: 400%)
    └── Everything else (ROAS target: 450%)
```

## ROAS Target Setting

### Calculating Breakeven ROAS

Every product (or product group) has a breakeven ROAS — the minimum return needed to cover variable costs:

```
Breakeven ROAS = 1 / Net Margin %

Example:
- Selling price: $50
- Variable costs (COGS + fees + shipping + returns): $35
- Net margin: ($50 - $35) / $50 = 30%
- Breakeven ROAS: 1 / 0.30 = 333%
```

Any ROAS above breakeven generates profit. Any ROAS below breakeven loses money on ad spend.

### Setting Target ROAS by Segment

| Segment | Margin | Breakeven ROAS | Target ROAS | Buffer | Rationale |
|---|---|---|---|---|---|
| High margin (>40%) | 40%+ | 250% | 300–350% | 20–40% | Aggressive — can afford more clicks to drive volume |
| Medium margin (25–40%) | 25–40% | 250–400% | 400–500% | 25–50% | Balanced — profitability with growth |
| Low margin (15–25%) | 15–25% | 400–667% | 600–800% | 30–50% | Conservative — every click must convert efficiently |
| Very low margin (<15%) | <15% | 667%+ | 800%+ | 50%+ | Highly selective — consider excluding from paid |

**Buffer formula**: Target ROAS = Breakeven ROAS × (1 + Buffer %)

The buffer accounts for: data variability, seasonal fluctuations, return rates not captured in ROAS calculation, and your desired profit per ad dollar.

### ROAS Target Adjustments

| Condition | Adjustment | Duration |
|---|---|---|
| Peak season (demand surge) | Lower ROAS target by 15–25% | During peak period |
| Off-season / trough | Raise ROAS target by 20–30% | During off-peak period |
| New product launch | Lower target by 30–50% to gather data | First 30–60 days |
| Product going end-of-life | Lower target to accelerate clearance | Until sold through |
| Competitor stockout | Lower target to capture incremental share | While opportunity lasts |
| Budget constrained | Raise target to focus on highest-efficiency clicks | Until budget freed up |

## Bid Adjustments

### Device Bid Adjustments

| Metric | Desktop | Mobile | Tablet |
|---|---|---|---|
| Conversion rate | [baseline] | Typically 30–60% lower | Typically 10–25% lower |
| AOV | [baseline] | Typically 5–15% lower | Similar to desktop |
| ROAS | [baseline] | Typically 30–50% lower | Typically 10–20% lower |

**Calculation**:
```
Device Bid Adjustment = (Device ROAS / Desktop ROAS - 1) × 100%

Example:
- Desktop ROAS: 500%
- Mobile ROAS: 300%
- Mobile adjustment: (300/500 - 1) × 100 = -40%
```

Apply adjustment in Google Ads at the campaign level. Review monthly as device performance shifts with seasons and product mix.

### Audience Bid Adjustments

| Audience | Typical ROAS Lift | Recommended Bid Increase |
|---|---|---|
| Cart abandoners (1–7 days) | 3–5× baseline | +100 to +200% |
| Cart abandoners (8–30 days) | 2–3× baseline | +50 to +100% |
| Past purchasers (repeat) | 2–4× baseline | +80 to +150% |
| Product page viewers (1–14 days) | 1.5–2.5× baseline | +30 to +80% |
| All site visitors (1–30 days) | 1.3–2× baseline | +20 to +50% |
| Customer match (email list) | 2–3× baseline | +50 to +100% |
| Similar audiences | 1.1–1.5× baseline | +10 to +30% |

**Setup requirements**:
1. Google Ads remarketing tag installed on all site pages
2. Audience lists created in Google Ads with sufficient membership (1,000+ for search/shopping)
3. Lists added to campaigns in "Observation" mode (not "Targeting" — you still want to reach new customers)
4. Customer match list uploaded if available (email list with 1,000+ matched entries)

### Time-of-Day / Day-of-Week Adjustments

Analyze conversion rate and ROAS by hour and day:
- If conversions peak 7–10pm, increase bids during those hours
- If weekends convert poorly, decrease bids Saturday–Sunday
- Use ad scheduling in Google Ads to implement up to 6 time segments per day
- Minimum 2–4 weeks of data at 50+ conversions per time segment before adjusting

### Geographic Bid Adjustments

| Signal | Action |
|---|---|
| States/regions with higher conversion rates | Increase bids +10 to +30% |
| States/regions with lower conversion rates | Decrease bids -10 to -30% |
| Areas outside delivery range | Exclude entirely |
| Areas with higher shipping costs | Decrease bids to offset margin impact |

## Smart Bidding vs. Manual Bidding

### When to Use Smart Bidding (Target ROAS / Maximize Conversion Value)

- Campaign has 15+ conversions in the past 30 days (Google's minimum for Smart Bidding to learn)
- You have enough budget to not be severely constrained (Smart Bidding needs room to optimize)
- Conversion tracking is accurate and complete (including conversion values)
- You're willing to accept short-term volatility during the learning period (2–4 weeks)

### When to Use Manual CPC / Enhanced CPC

- New campaigns with limited conversion data (<15 conversions/month)
- Very small catalogs where you can manage bids product-by-product
- Testing phase where you want direct control over spend
- Campaigns with highly variable product values where Smart Bidding struggles

### Smart Bidding Best Practices

1. **Don't change ROAS targets too frequently** — each change triggers a new learning period. Wait 2–3 weeks between adjustments.
2. **Make small adjustments** — change ROAS targets by no more than 15–20% at a time.
3. **Don't constrain budget excessively** — if the campaign is consistently limited by budget, Smart Bidding can't optimize effectively. Either increase budget or raise the ROAS target.
4. **Use portfolio bid strategies** — group similar campaigns under one bid strategy to give the algorithm more data to learn from.
5. **Monitor closely during learning** — performance may dip for 1–2 weeks after changes. Don't panic-adjust.

## Performance Max Considerations

### Asset Group Strategy

Performance Max campaigns replace standard Shopping for many advertisers. Key differences in bid management:

- No manual bid adjustments (device, audience, time) — the algorithm handles all adjustments
- ROAS target is the primary lever, along with audience signals
- Budget allocation across channels (Shopping, Display, YouTube, Search) is automated
- Use asset groups to segment products with different creative and audience strategies

### Audience Signals for Performance Max

| Signal Type | What to Provide | Impact |
|---|---|---|
| Customer match lists | Email/phone lists of past purchasers | Helps PMax find similar high-value users |
| Website visitor lists | Remarketing audiences from Google Ads | Warm audiences for re-engagement |
| Custom segments | Search terms your customers use | Targets users searching related terms |
| Interests & demographics | In-market audiences relevant to your products | Broadens reach to likely buyers |

### Monitoring Performance Max

Since PMax combines multiple channels, monitor:
- Overall campaign ROAS vs. target
- Shopping-specific metrics via the "Listings" tab (impressions, clicks, CTR)
- Asset group performance (which groups drive conversions)
- Search term insights (available in the Insights tab, though limited)
- New customer acquisition rate (if using the new customer goal)

## Budget Management

### Budget Allocation Framework

```
Total Shopping Budget Allocation:
├── Tier 1 (Top Performers): 35–45%
├── Tier 2 (Core Catalog): 35–45%
├── Tier 3 (Long Tail): 10–20%
└── Tier 4 (Brand Defense): 5–10%
```

### Budget Pacing Rules

| Signal | Action |
|---|---|
| Campaign hitting daily budget before 3pm | Increase budget or raise ROAS target to be more selective |
| Campaign underspending daily budget by >30% | Lower ROAS target to be more aggressive, or improve feed quality |
| ROAS above target but budget capped | Increase budget — you're leaving profitable clicks on the table |
| ROAS below target but not budget capped | Raise ROAS target, add negatives, or pause underperforming products |

### Seasonal Budget Adjustments

| Season | Budget Change | Rationale |
|---|---|---|
| Pre-peak (2–4 weeks before) | +20–30% | Build momentum and data before peak spending |
| Peak season | +40–100% | Capture demand surge with proven products |
| Post-peak | −30–50% | Reduce as demand drops; shift to clearance |
| Off-season | Return to baseline or −10–20% | Maintain visibility for evergreen products |

## Measurement and Optimization Cadence

### Daily Checks (5 minutes)

- Campaign spend pacing (on track for daily budget?)
- ROAS by campaign (any sudden drops?)
- Disapproval alerts from Merchant Center

### Weekly Review (30 minutes)

- Search Terms report: add negatives, identify opportunities
- Product-level performance: flag any new underperformers
- Impression share trends: improving or declining?
- Competitor activity: any new entrants or pricing changes?

### Monthly Deep Dive (2 hours)

- Full ROAS analysis by product group, device, audience, and geography
- Bid adjustment recalibration based on fresh data
- Title performance analysis: which titles drive highest CTR?
- Budget reallocation between tiers based on opportunity
- Custom label updates: reclassify products based on latest performance

### Quarterly Strategy Review (Half day)

- Campaign structure assessment: is the current architecture still optimal?
- ROAS target recalibration against updated margins
- Competitive landscape review: positioning changes needed?
- Feed quality audit: score vs. last quarter
- New feature adoption: any new Google Shopping features to leverage?
