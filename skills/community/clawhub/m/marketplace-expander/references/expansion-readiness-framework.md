# Expansion Readiness Framework

This framework assesses whether your current operations can support a new marketplace launch without degrading performance on existing channels. Use it during Step 7 of the marketplace evaluation workflow, after you have identified your target marketplaces.

---

## Overview

Marketplace expansion fails most often not because the opportunity was bad, but because the seller's operations could not support the additional complexity. This framework evaluates readiness across six operational dimensions, each scored on a 1-5 maturity scale.

**Minimum readiness threshold**: A seller should score at least 3 in every dimension before launching on a new marketplace. Any dimension scoring 1-2 requires remediation before proceeding.

---

## Dimension 1: Inventory and Supply Chain Readiness

Assess whether your supply chain can handle the increased demand and complexity of multi-marketplace inventory management.

### Maturity Levels

| Score | Level | Description |
|---|---|---|
| 1 | Manual | Inventory tracked in spreadsheets. No safety stock calculations. Single supplier with no backup. Stockouts happen monthly. |
| 2 | Basic | Using basic inventory software. Safety stock exists but is not dynamically calculated. 1-2 suppliers. Stockouts happen quarterly. |
| 3 | Managed | Multi-channel inventory management tool in place (e.g., Linnworks, Cin7, Sellbrite). Safety stock calculated per SKU. 2-3 suppliers. Stockouts are rare. |
| 4 | Optimized | Real-time inventory sync across all channels. Demand forecasting with seasonal adjustments. Dual-source for critical SKUs. Working capital reserved for 60-day inventory coverage. |
| 5 | Advanced | AI-driven demand planning. Automated reorder points. Multi-origin fulfillment with regional inventory positioning. Less than 2% stockout rate annually. |

### Key Questions

- Can your inventory management system integrate with the new marketplace? What is the integration timeline?
- Do you have enough working capital to fund inventory for the new channel without depleting stock on existing channels?
- What is your current lead time from PO to warehouse receipt? Can your suppliers scale production by 20-50%?
- Will you need to hold inventory in a new geographic location? If so, who manages it?

### Red Flags

- No multi-channel inventory sync (risk: overselling, stockouts on primary channel)
- Single supplier with 60+ day lead time (risk: cannot respond to demand spikes)
- Less than 30 days of inventory coverage at current velocity (risk: stockout during demand spike from new channel launch)

---

## Dimension 2: Fulfillment and Logistics Readiness

Evaluate whether your fulfillment infrastructure can serve the new marketplace's buyers at the speed and cost they expect.

### Maturity Levels

| Score | Level | Description |
|---|---|---|
| 1 | Self-Fulfillment Only | Packing and shipping from home or office. No 3PL. Ship times of 5-10 days domestically. |
| 2 | Single 3PL | One fulfillment partner. Can handle one marketplace. No international shipping capability. |
| 3 | Multi-Channel 3PL | 3PL integrates with multiple marketplaces. 2-3 day domestic shipping. Basic international shipping (one region). |
| 4 | Regional Distribution | Multiple fulfillment nodes covering primary markets. Marketplace-native fulfillment (FBA, WFS, SFP) for key channels. Returns handled efficiently. |
| 5 | Global Network | Fulfillment centers in 3+ regions. Sub-48-hour delivery in primary markets. Cross-border fulfillment with duties pre-paid. Automated returns processing. |

### Key Questions

- Does the target marketplace offer its own fulfillment service? Is it mandatory or optional?
- What delivery speed do buyers on this marketplace expect? (Same-day, 2-day, 5-day, 10-day?)
- What is the cost per shipment to the target marketplace's primary geography?
- How will returns be handled? Does the marketplace require local return addresses?
- For cross-border: What are customs duties and import tax implications? Who is the importer of record?

### Red Flags

- Target marketplace expects 2-day delivery but your closest warehouse is 7+ days away
- No return address in the target country (many marketplaces require one)
- Cross-border shipping costs exceed 15% of product value

---

## Dimension 3: Team and Organizational Readiness

Assess whether your team has the skills and capacity to manage an additional marketplace.

### Maturity Levels

| Score | Level | Description |
|---|---|---|
| 1 | Founder-Only | Founders handle all marketplace operations. No dedicated ecommerce staff. |
| 2 | Small Team | 1-2 people managing all marketplaces. Generalists, no platform specialists. |
| 3 | Functional Team | Dedicated marketplace manager. Separate roles for advertising, content, and customer service. Can manage 2-3 marketplaces. |
| 4 | Scaled Team | Platform-specific specialists. Dedicated ad managers per marketplace. Customer service team with language capabilities. Manager-to-marketplace ratio of 1:2 or better. |
| 5 | Center of Excellence | Cross-functional marketplace team with playbooks and SOPs for each platform. Hiring pipeline for marketplace talent. Training programs for new platforms. |

### Key Questions

- How many hours per week does the team currently spend on marketplace operations? What is the remaining capacity?
- Does anyone on the team have experience with the target marketplace? If not, what is the learning curve?
- Does the team have language skills for the target market? (Customer service, listing optimization, ad management)
- Who will own the new marketplace? Is this an addition to someone's role or a dedicated hire?
- What is the plan if the expansion doubles customer service volume?

### Capacity Planning Formula

```
Hours needed per marketplace per week (estimate):
- Listing management and optimization: 5-10 hrs
- Advertising management: 5-15 hrs
- Customer service: 5-20 hrs (scales with volume)
- Inventory and fulfillment coordination: 3-5 hrs
- Reporting and analytics: 2-4 hrs
- Total: 20-54 hrs/week per marketplace
```

If total team capacity is already at 80%+ utilization, hire before launching.

### Red Flags

- Team is already working 50+ hour weeks
- No one on the team speaks the language of the target market
- The person assigned to the new marketplace is also responsible for your highest-revenue existing channel

---

## Dimension 4: Technology and Integration Readiness

Evaluate whether your tech stack can support the new marketplace with reasonable integration effort.

### Maturity Levels

| Score | Level | Description |
|---|---|---|
| 1 | No Integration | All marketplaces managed through native seller portals. Copy-paste listing creation. Manual order processing. |
| 2 | Basic Tools | Using a multi-channel listing tool (e.g., Listing Mirror, Sellbrite). Manual order import to shipping software. |
| 3 | Integrated Stack | ERP or OMS connects to marketplaces via API or middleware (ChannelAdvisor, Linnworks, Pipe17). Orders flow automatically. Basic analytics dashboard. |
| 4 | Automated | Full automation from listing to order to fulfillment to accounting. Price optimization tools. Automated advertising bid management. Real-time dashboards per marketplace. |
| 5 | Custom Platform | Proprietary or highly customized tech stack. API-first architecture. Can integrate a new marketplace in under 1 week. Machine learning for pricing and advertising. |

### Key Questions

- Does your current listing tool / ERP support the target marketplace?
- What data fields does the new marketplace require that your product catalog does not currently have?
- Can your accounting system handle multi-currency transactions and marketplace-specific fee reconciliation?
- What analytics and reporting do you need to monitor the new marketplace? Can your current dashboards accommodate it?

### Red Flags

- Your current multi-channel tool does not support the target marketplace and there is no integration timeline
- Product data is stored in spreadsheets rather than a structured PIM/catalog system
- No way to reconcile marketplace payouts against orders (leading to financial blind spots)

---

## Dimension 5: Financial Readiness

Confirm that the business has the financial resources and controls to fund and monitor a marketplace expansion.

### Maturity Levels

| Score | Level | Description |
|---|---|---|
| 1 | Cash-Tight | Operating with less than 30 days of cash runway. No credit line. Cannot fund additional inventory without revenue from existing channels. |
| 2 | Stable | 60-90 days cash runway. Small credit line available. Can fund a modest expansion ($10-25K). |
| 3 | Funded | 90-120 days cash runway. Credit or financing available for inventory. Expansion budget of $25-75K without impacting existing operations. |
| 4 | Well-Capitalized | 120+ days cash runway. Multiple financing options. Can fund $75-200K expansion. Per-channel P&L tracking in place. |
| 5 | Investor-Ready | Strong balance sheet. Dedicated expansion fund. Sophisticated financial modeling with scenario analysis. Real-time margin tracking per SKU per channel. |

### Working Capital Model

```
Working capital needed for expansion = 
  Initial inventory investment
+ 90-day advertising budget
+ Compliance and setup costs
+ First 90 days of fixed costs (software, headcount)
+ Contingency (15-20%)
- Expected revenue collections in first 90 days (discounted 50% for conservative modeling)
```

### Key Questions

- What is the total cash outlay before you receive your first marketplace payout?
- Can you absorb a scenario where the new marketplace generates zero revenue for 90 days?
- Do you have per-channel profitability tracking, or will the new marketplace's P&L be blended into overall financials?
- What is your cost of capital? (Opportunity cost of tying up cash in new marketplace inventory vs. investing in existing channels)

### Red Flags

- Expansion requires more than 30% of current cash reserves
- No per-channel P&L tracking (cannot tell if the new marketplace is profitable)
- Expansion is being funded by delaying payments to existing suppliers

---

## Dimension 6: Brand and Content Readiness

Assess whether your brand assets, product content, and creative capabilities are ready for a new marketplace.

### Maturity Levels

| Score | Level | Description |
|---|---|---|
| 1 | Minimal | Basic product photos (white background only). Short text descriptions. No A+ content or brand store. |
| 2 | Adequate | Professional product photography. Keyword-optimized titles and bullet points for one marketplace. |
| 3 | Multi-Channel Ready | Product content adapted for 2-3 marketplaces. A+ / enhanced content on primary channel. Lifestyle images available. |
| 4 | Localized | Content localized (not just translated) for multiple markets and languages. Video content available. Brand store / storefront on primary marketplaces. |
| 5 | Content Engine | In-house or agency content production pipeline. A/B testing of listings. UGC program. Influencer content library. Can produce marketplace-specific content (e.g., TikTok videos, Shopee live assets) on demand. |

### Key Questions

- Does the target marketplace require specific image formats, dimensions, or content types not currently in your asset library?
- Can existing product descriptions be localized for the target market, or do they need to be rewritten?
- Does the marketplace favor video content (TikTok Shop, Shopee Live)? Do you have video production capability?
- Is your brand registered on the target marketplace? If not, what is the registration timeline?

### Red Flags

- Product images do not meet the target marketplace's requirements (e.g., minimum resolution, white background rules, infographic restrictions)
- No capability to produce content in the target market's language
- Marketplace requires video content but seller has no video assets or production plan

---

## Readiness Scorecard

| Dimension | Score (1-5) | Critical Gaps | Remediation Plan | Timeline |
|---|---|---|---|---|
| Inventory & Supply Chain | | | | |
| Fulfillment & Logistics | | | | |
| Team & Organization | | | | |
| Technology & Integration | | | | |
| Financial Readiness | | | | |
| Brand & Content | | | | |
| **Average Score** | | | | |

### Interpreting Results

- **Average 4.0-5.0**: Ready to launch. Proceed with confidence.
- **Average 3.0-3.9**: Ready with caveats. Address any dimensions scoring below 3 before launching.
- **Average 2.0-2.9**: Not ready. Significant operational gaps that will likely cause the expansion to underperform or fail. Invest 2-3 months in readiness building before proceeding.
- **Average 1.0-1.9**: Premature. Focus on strengthening existing operations before considering expansion.

### Decision Rule

**Do not launch if any single dimension scores 1.** A score of 1 in any dimension represents a structural gap that will cause cascading failures regardless of how strong other dimensions are. For example, a financially strong seller (5) with zero fulfillment capability in the target market (1) will waste money on advertising that drives orders they cannot deliver.
