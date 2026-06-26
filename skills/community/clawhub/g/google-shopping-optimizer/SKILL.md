---
name: Google Shopping Optimizer
description: Optimize Google Merchant Center product feeds, bidding strategies, and Shopping ad performance for ecommerce sellers.
---

# Google Shopping Optimizer

Analyze Google Merchant Center product data, diagnose feed quality issues, optimize bidding strategies, and generate actionable plans that increase impressions, clicks, and conversions while reducing wasted ad spend. This skill transforms raw Merchant Center diagnostics, Shopping campaign reports, and product feed exports into a structured optimization plan covering feed health, product data quality, competitive positioning, bidding efficiency, and campaign structure. It identifies the specific issues suppressing performance — disapprovals, missing attributes, poor titles, inefficient bids, wasted spend on non-converting queries — and produces prioritized fixes with projected impact estimates.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Feed health analysis | Every product audited against all required and recommended attributes with specific errors listed per product | Category-level attribute compliance checked with sample products reviewed | Only checking disapproval count without diagnosing root causes |
| Title optimization | Keyword-enriched titles following category-specific templates with search volume data informing priority | Titles reviewed for completeness and basic keyword inclusion | Generic title advice without category-specific guidance or keyword research |
| Bidding strategy | Segment-specific ROAS targets with bid adjustments by device, audience, and product group | Portfolio-level ROAS target with basic campaign structure | Single ROAS target across all products with no segmentation |
| Query analysis | Search term report mined for negatives, query-product match quality scored, and converting queries identified | Top wasted spend queries identified and negated | No search term analysis or only reviewing top-level campaign metrics |
| Product grouping | Multi-level product groups by performance tier, margin, and category with differentiated bids | Product groups by category or brand with some bid differentiation | All products in a single ad group with uniform bids |
| Competitive analysis | Benchmark pricing, impression share, and click share against category competitors with positioning recommendations | Impression share reviewed with general competitive observations | No competitive data analyzed |

## Solves

- Your Google Shopping products keep getting disapproved and you need a systematic audit of feed quality issues with specific fixes for each disapproval type
- Your Shopping ads get impressions but low click-through rates, and you need to optimize titles, images, and pricing to improve competitive positioning
- Your ROAS is below target and you need to restructure campaigns, adjust bids by product segment, and eliminate wasted spend on non-converting search queries
- You have hundreds of products and need to prioritize which feed improvements will have the largest impact on impressions and revenue
- Your Merchant Center diagnostics show warnings and errors but you need help interpreting them and building a prioritized fix plan
- You want to expand to new markets or add free listings and need a feed optimization strategy that maximizes visibility across both paid and organic Shopping surfaces
- Your Shopping campaigns are structured as a single campaign with one ad group and you need a segmented structure that allows differentiated bidding by performance tier

## Workflow

### Step 1 — Audit feed health and product data quality
Export the full product feed from Merchant Center or your feed management tool. For each product, verify all required attributes are present and correctly formatted: id, title, description, link, image_link, availability, price, brand, gtin/mpn, condition, and product_type. Check recommended attributes: additional_image_link, sale_price, google_product_category, custom_labels, shipping, and tax. Flag every disapproved or warned product with the specific error code and root cause. Categorize issues by type: policy violations, data quality errors (missing attributes, incorrect formatting), image issues, pricing mismatches between feed and landing page, and availability mismatches.

### Step 2 — Optimize product titles and descriptions
Analyze current titles against category-specific best practices. Effective Shopping titles front-load the most important attributes in order: brand + product type + key attributes (size, color, material, model). Research top-performing search queries in the category using Search Terms reports and keyword tools. Rewrite titles to include high-volume, relevant search terms while staying within the 150-character limit (first 70 characters are most critical as they display in ads). For descriptions, ensure the first 160 characters contain the primary value proposition and key specifications since this portion may display in free listings.

### Step 3 — Analyze search query performance and build negative lists
Pull the Search Terms report for the past 30–90 days. Identify wasted spend: queries with significant spend but zero conversions, queries with ROAS below the break-even threshold, and queries that are irrelevant to the products being shown. Build negative keyword lists at the campaign and ad group level. Identify high-performing converting queries and ensure the matching products have optimized titles and competitive pricing. Calculate the query-to-product match quality — are the right products showing for the right searches?

### Step 4 — Restructure campaigns and product groups
Evaluate the current campaign structure against best practices. Recommend a tiered structure: (1) High-priority campaign with higher bids for top-performing products (high margin, high conversion rate, strong ROAS). (2) Medium-priority campaign for products with moderate performance. (3) Catch-all campaign with lower bids for remaining products and new/untested items. Within each campaign, create product groups segmented by category, brand, or custom label to enable granular bid management. Set up custom labels in the feed to tag products by margin tier, performance tier, seasonality, and promotion status.

### Step 5 — Optimize bidding and ROAS targets
For Smart Shopping / Performance Max campaigns: set segment-specific ROAS targets based on product margin and conversion data — high-margin products can accept lower ROAS, low-margin products need higher ROAS to remain profitable. For manual CPC or Enhanced CPC: set bids based on the value-per-click calculation (average order value × conversion rate × target margin). Apply bid adjustments by device (mobile vs. desktop conversion rate differences), audience (remarketing lists, customer match), and time of day/day of week based on conversion pattern data. Calculate the breakeven CPC for each product group.

### Step 6 — Optimize for competitive positioning
Pull the Merchant Center competitive visibility report and the Auction Insights (if available through linked Google Ads). Identify products where you have low impression share despite competitive pricing — these likely have feed quality issues. Identify products where competitors consistently win on price — evaluate whether to compete on price, differentiate on other attributes, or reduce bids to maintain profitability. For products with strong reviews and ratings, ensure seller ratings and product ratings extensions are enabled to improve click-through rates.

### Step 7 — Build the optimization roadmap and monitoring plan
Prioritize all identified improvements by projected impact and implementation effort. Create a phased execution plan: Phase 1 (Week 1) — Fix all disapprovals and critical feed errors. Phase 2 (Weeks 2–3) — Implement title optimizations and negative keyword lists. Phase 3 (Weeks 3–4) — Restructure campaigns and adjust bids. Phase 4 (Ongoing) — Monitor performance, refine bids, and iterate on feed quality. Define KPIs and tracking cadence: daily (spend, ROAS), weekly (impression share, CTR, conversion rate, disapproval count), monthly (revenue, profit, feed score).

## Example 1: Home & Garden DTC Brand (120 SKUs, $45K/month Shopping Spend)

**Input data**: Google Merchant Center export with 120 active products, Shopping campaign reports for 90 days, Search Terms report, and competitive visibility data.

**Feed audit findings**:
- 18 products disapproved: 9 for price mismatches (feed price doesn't match landing page), 5 for missing GTIN, 4 for policy-violating images (text overlay >10% of image)
- 34 products with missing `google_product_category` — defaulting to algorithm classification (lower match quality)
- 67 products with titles under 40 characters — significantly under-optimized (competitor average: 85 characters)
- 0 products using `additional_image_link` — missing lifestyle images that improve CTR
- No custom labels configured — all products bid identically regardless of margin or performance

**Title optimization (sample)**:
| Before | After |
|---|---|
| "Cedar Planter Box" | "Cedar Raised Garden Planter Box - Outdoor Elevated Wood Bed 4x2ft" |
| "Solar Path Lights" | "Solar Pathway Lights Outdoor LED - Waterproof Garden Walkway 8-Pack" |
| "Patio Umbrella" | "9ft Patio Umbrella with Tilt & Crank - Outdoor Market Table Umbrella Navy" |

**Search query analysis (90 days)**:
- $4,200 spent on non-converting queries (9.3% of total spend) — 340+ queries with $5+ spend and zero conversions
- Top wasted query: "free garden plans" ($180 spend, 0 conversions) — informational intent, not purchase intent
- 45 high-converting queries not reflected in product titles — opportunity to improve relevance scores
- Brand terms converting at 8.2% vs. non-brand at 1.4% — brand campaign separation needed

**Campaign restructure**:
| Campaign | Products | ROAS Target | Daily Budget |
|---|---|---|---|
| Shopping — Top Performers | 25 SKUs (top 20% by profit) | 400% | $600 |
| Shopping — Core Catalog | 60 SKUs (middle tier) | 600% | $700 |
| Shopping — Long Tail | 35 SKUs (new + low volume) | 300% | $200 |

**Projected impact**: Fixing disapprovals restores $3,800/mo in lost revenue. Title optimization projects +15–25% CTR improvement. Negative keyword cleanup saves $4,200/mo in wasted spend. Campaign restructure projects +18% overall ROAS improvement. Combined 90-day projection: +$28,000 incremental revenue, ROAS improvement from 380% to 520%.

## Example 2: Apparel Brand on Multiple Channels (450 SKUs, $120K/month Shopping Spend)

**Input data**: Merchant Center feed with 450 products across 6 apparel categories, Performance Max campaign data for 60 days, supplemental feed for promotions, and Google Ads auction insights.

**Feed audit findings**:
- 42 products disapproved: 22 for variant mismatches (color/size in title doesn't match variant attributes), 12 for image policy violations (model images with non-white backgrounds rejected), 8 for GTIN issues
- 180 products missing `color` attribute — critical for apparel discovery and filtering
- 95 products missing `size` attribute — prevents showing in size-filtered searches
- `product_type` taxonomy inconsistent — 14 different naming conventions for the same category
- Sale prices not updating via supplemental feed — 60 products showing wrong price
- No `product_highlight` or `product_detail` attributes — missing structured specification data

**Bidding analysis**:
- Overall ROAS: 320% (target: 500%)
- Top 50 SKUs (11% of catalog): ROAS 780%, contributing 45% of revenue — under-invested
- Bottom 150 SKUs (33% of catalog): ROAS 85%, consuming 28% of budget — margin-destructive
- Mobile ROAS: 210% vs. Desktop: 480% — mobile bids not adjusted despite 2.3x conversion rate gap
- Returning customer ROAS: 620% vs. New customer: 280% — no audience bid adjustments applied

**Custom label strategy**:
| Label | Values | Purpose |
|---|---|---|
| custom_label_0 | margin_high / margin_mid / margin_low | Differentiate ROAS targets by profitability |
| custom_label_1 | perf_star / perf_core / perf_tail / perf_drain | Segment by historical performance |
| custom_label_2 | seasonal_spring / seasonal_summer / evergreen | Adjust bids for seasonal relevance |
| custom_label_3 | promo_active / promo_none | Boost bids during active promotions |
| custom_label_4 | new_launch / established | Different bidding strategy for new vs. proven products |

**Projected impact**: Fixing disapprovals restores $12,500/mo in lost revenue. Attribute completeness improvements project +20% impression share. Bidding restructure with performance tiering projects ROAS improvement from 320% to 485%. Eliminating spend on bottom-tier drains saves $33,600/mo in wasted budget. Combined 90-day projection: +$95,000 incremental revenue, blended ROAS improvement from 320% to 510%.

## Common Mistakes

1. **Ignoring feed quality and focusing only on bids**: No amount of bid optimization can fix a feed with missing attributes, disapproved products, and thin titles. Feed quality is the foundation — without it, products either don't show at all or show for the wrong queries. Always fix feed issues before touching bids.

2. **Writing titles for humans instead of algorithms**: Shopping ad titles serve double duty — they're the primary signal Google uses for query matching AND the text shoppers see. Front-load high-volume search keywords rather than writing creative marketing copy. "Cedar Raised Garden Planter Box - Outdoor Elevated Bed 4x2ft" outperforms "The Beautiful Cedar Box for Your Garden" because it matches more purchase-intent queries.

3. **Bidding uniformly across all products**: A single ROAS target treats a $100 product with 60% margins the same as a $15 product with 20% margins. Segment products by margin and performance to set appropriate targets — high-margin winners deserve more aggressive bids while low-margin, low-conversion products should be bid down or excluded.

4. **Never reviewing the Search Terms report**: The Search Terms report reveals exactly which queries trigger your ads and how they perform. Without regular review, you accumulate wasted spend on irrelevant queries (informational searches, competitor brand names you can't compete on, wrong product matches) that silently erode ROAS.

5. **Using only required attributes and skipping recommended ones**: Required attributes get your products listed; recommended attributes make them competitive. Products with complete attributes — additional images, sale prices, product highlights, shipping details — receive higher quality scores and better ad placement than bare-minimum listings.

6. **Not setting up custom labels**: Without custom labels, you can't segment product groups by business-relevant dimensions like margin tier or performance category. This forces uniform bidding and prevents the granular campaign structure that separates high-ROAS advertisers from average ones.

7. **Ignoring mobile performance differences**: Mobile and desktop Shopping campaigns often have dramatically different conversion rates and ROAS. If mobile converts at half the rate of desktop but you bid identically, you're overspending on mobile clicks. Apply device bid adjustments or create device-specific campaigns.

8. **Setting and forgetting Performance Max campaigns**: Performance Max automates many decisions but still requires active management — audience signals, asset groups, feed quality, and ROAS targets all need regular review. "Automated" doesn't mean "unmanaged."

## Resources

- [Output template](references/output-template.md) — Structured format for presenting Google Shopping optimization plans
- [Feed optimization guide](references/feed-optimization-guide.md) — Attribute-by-attribute best practices for product feed quality
- [Bidding strategy playbook](references/bidding-strategy-playbook.md) — ROAS targeting, campaign structuring, and bid management frameworks
- [Quality checklist](assets/quality-checklist.md) — Pre-delivery validation checklist
