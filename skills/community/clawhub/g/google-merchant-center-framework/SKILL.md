---
name: google-merchant-center-framework
description: |
  Google Merchant Center analysis and optimization framework. Use when the user asks about Shopping feed health, product disapprovals, title optimization, price competitiveness, Shopping campaign readiness, or any GMC diagnostic task.
metadata:
  version: "1.0"
  categories: "ecommerce, google-shopping, feed-management"
---

# Google Merchant Center Framework

Diagnose feed health, optimize product listings, resolve disapprovals, analyze price competitiveness, and assess Shopping campaign readiness. A decision-framework for agents working with Google Merchant Center accounts of any size.

## How This Skill Works

**Step 1:** Collect context from the user's message — merchant category, product count, known issues, goals (fix disapprovals, improve performance, launch Shopping ads, etc.).

**Step 2:** Ask one follow-up with all remaining questions using multiple-choice format. Key questions:
- a) Account size: (1) <500 SKUs, (2) 500-10K, (3) 10K-100K, (4) 100K+
- b) Primary goal: (1) Fix disapprovals, (2) Improve feed quality, (3) Boost Shopping performance, (4) Launch new campaign, (5) General audit
- c) Feed method: (1) Direct API, (2) Scheduled fetch (XML/CSV), (3) Shopify/WooCommerce plugin, (4) Supplemental feeds, (5) Not sure
- d) Current disapproval rate: (1) <2%, (2) 2-10%, (3) 10-25%, (4) >25%, (5) Unknown

Allow shorthand answers (e.g., "1a 2c 3b 4e").

**Step 3:** Analyze using the frameworks below. Prioritize by impact: disapprovals first (products not showing), then data quality (products showing poorly), then performance (products showing but underperforming).

**Step 4:** Deliver structured output with specific fixes, benchmarks, and priority order.

## Integration Note

This skill works best when paired with a Google Merchant Center MCP for live data access. Without live data, the agent applies frameworks to data the user provides (exports, screenshots, descriptions of issues). With live data, the agent can pull product statuses, diagnostics, and price insights directly.

---

## 1. Feed Health Analysis

### Health Score Framework

Calculate a feed health score from these weighted components:

| Component | Weight | How to Score |
|-----------|--------|-------------|
| Approval rate | 30% | 100% approved = 100 pts. Deduct 2 pts per % disapproved |
| Required attribute completeness | 25% | % of products with all required attrs filled |
| Recommended attribute completeness | 15% | % of products with 8+ of 12 recommended attrs |
| Data freshness | 15% | Updated <24h = 100, 24-48h = 70, 48-72h = 40, >72h = 0 |
| Image quality | 15% | % of products with compliant images (no watermarks, no placeholders, >100x100px) |

**Score interpretation:**
- 90-100: Excellent. Focus on performance optimization.
- 75-89: Good. Fix remaining disapprovals and fill attribute gaps.
- 50-74: Needs work. Systematic issues present. Prioritize disapprovals, then required attributes.
- <50: Critical. Feed is substantially broken. Triage disapprovals by volume.

### Required vs Recommended Attributes

**Always required (all products):**
- `id`, `title`, `description`, `link`, `image_link`, `availability`, `price`

**Required for most categories:**
- `brand` (required except for movies, books, musical recordings)
- `gtin` (required for all products with a manufacturer-assigned GTIN)
- `condition` (required if used or refurbished)

**Conditionally required:**
- `color`, `size`, `gender`, `age_group` — required for Apparel & Accessories
- `item_group_id` — required for product variants
- `shipping` — required if not set at account level
- `tax` — required in the US if not set at account level

**High-impact recommended attributes:**
- `additional_image_link` (up to 10 images; products with 3+ images get ~15% higher CTR)
- `product_type` (your own categorization; helps with campaign structure)
- `sale_price` + `sale_price_effective_date` (triggers sale badge in Shopping)
- `custom_label_0` through `custom_label_4` (essential for campaign segmentation)
- `product_highlight` (up to 10 bullet points; shown in free listings)
- `product_detail` (section_name + attribute_name + attribute_value tuples)

### Diagnostic Priority Order

1. **Account-level suspensions** — nothing shows until resolved
2. **Item-level disapprovals** — products removed from serving
3. **Item-level warnings** — products serve but with reduced visibility
4. **Missing required attributes** — will become disapprovals
5. **Missing recommended attributes** — reduces competitiveness
6. **Data quality issues** — poor titles, descriptions, categorization

---

## 2. Product Optimization

### Title Optimization

Titles are the single highest-impact attribute for Shopping performance. Google uses titles for query matching more heavily than descriptions.

**Structure formula by category:**

| Category | Title Formula | Example |
|----------|--------------|---------|
| Apparel | Brand + Gender + Product Type + Attributes (Color, Size, Material) | "Nike Women's Air Max 270 Running Shoes - Black/White, Size 8" |
| Electronics | Brand + Product Line + Model + Key Specs | "Samsung Galaxy S24 Ultra 256GB Titanium Black Unlocked" |
| Home & Garden | Brand + Product Type + Material + Key Dimensions + Color | "KitchenAid Classic 4.5-Quart Tilt-Head Stand Mixer Onyx Black" |
| Beauty | Brand + Product Line + Product Type + Size/Count + Variant | "CeraVe Moisturizing Cream Face and Body 19oz Fragrance-Free" |
| Grocery | Brand + Product Name + Flavor/Variant + Size/Count + Pack | "KIND Bars Dark Chocolate Nuts & Sea Salt 12-Count Box" |

**Title rules:**
- Max 150 characters; first 70 characters are most critical (truncation in mobile)
- Front-load the most important keywords in the first 70 characters
- Never use ALL CAPS or promotional text ("Free Shipping", "Best Price")
- Include color, size, material when relevant — these are matching signals
- Use the actual brand name, not abbreviations
- Separate attributes with hyphens or commas, not pipes

**Title quality scoring:**

| Signal | Points |
|--------|--------|
| Brand name present and correct | +20 |
| Product type keyword included | +20 |
| Key differentiating attribute (color/size/material) | +15 each, max +30 |
| Within 70-character sweet spot | +15 |
| No promotional language | +15 |
| **Total possible** | **100** |

### Description Optimization

- 1,000-5,000 characters optimal (minimum 500)
- First 150-200 characters most critical (may be shown in free listings)
- Include keywords naturally — Google does use descriptions for matching, but less than titles
- Include specifications, materials, dimensions, use cases
- No HTML tags (stripped by Google), no promotional language, no links

### Image Requirements

| Requirement | Standard | Notes |
|-------------|----------|-------|
| Minimum resolution | 100x100px (250x250 for apparel) | 800x800+ recommended for zoom |
| Max file size | 16MB | |
| Format | JPEG, PNG, GIF, BMP, TIFF, WebP | |
| Background | White or transparent preferred | Non-white OK but clean background required |
| Watermarks | Not allowed | Automatic disapproval |
| Text overlay | Not allowed on main image | OK on additional images |
| Promotional overlay | Not allowed | "Sale", "Free shipping" overlays = disapproval |
| Product visibility | Product must fill 75-90% of frame | No tiny product in large frame |

**Image optimization checklist:**
- Main image: product only, white background, high resolution
- 3+ additional images (lifestyle, different angles, scale/size reference)
- Apparel: show product on a person or flat-lay (not hanger)
- Consistent image style across product line

### GTIN/MPN Completeness

- **GTIN is critical.** Products with valid GTINs get ~20% more impressions than those without.
- Google cross-references GTINs against the GS1 database. Invalid GTINs cause disapprovals.
- If a product genuinely has no GTIN (custom, handmade, vintage, parts), set `identifier_exists` to `no`.
- Never fabricate GTINs. Never reuse GTINs across different products.
- MPN is required when GTIN is not available and the product has a manufacturer part number.

---

## 3. Price Competitiveness

### Interpreting Price Benchmarks

Google provides price benchmarks in the Price Competitiveness report. Key metrics:

| Metric | What It Means | Action Threshold |
|--------|---------------|-----------------|
| `benchmark_price` | Median price of the same product from other merchants | If your price >15% above: expect significantly lower CTR |
| `price_difference_percentage` | Your price vs benchmark | >10% above: review pricing. >20% above: likely suppressed |
| `country_code` | Market the benchmark applies to | Compare only within same market |

### Competitive Visibility Score Framework

| Position | Your Price vs Benchmark | Expected Impact |
|----------|------------------------|----------------|
| Strong | >10% below benchmark | High impressions, high CTR. Verify margin is acceptable. |
| Competitive | Within +/-10% of benchmark | Normal serving. Optimize other signals. |
| Weak | 10-20% above benchmark | Reduced impressions. Consider sale_price or promotions. |
| Uncompetitive | >20% above benchmark | Severely reduced serving. Re-evaluate pricing or exclude from Shopping. |

### Price Strategy Decisions

**When price is too high vs benchmark:**
1. Can you lower the price? Do it.
2. Can you add a promotion or sale_price? Triggers sale badge, improves CTR even if final price is still above benchmark.
3. Can you differentiate on value (bundle, warranty, fast shipping)? Add to title and description.
4. Is the product a loss leader for competitors? Consider excluding from Shopping.
5. Use `custom_label` to segment high-priced items into separate campaigns with different ROAS targets.

**Price-Landing Page Match** — #1 cause of avoidable disapprovals:
- Price shown on page must match `price` attribute exactly (including currency)
- `sale_price` must match the visible sale price on the landing page
- If microdata/structured data on the page differs from the feed, the feed value may be overridden or flagged

---

## 4. Performance Analysis

### Shopping Performance Benchmarks by Category

| Category | Median CTR | Good CTR | Median CPC (Shopping Ads) | Median Conv. Rate |
|----------|-----------|----------|--------------------------|------------------|
| Apparel & Accessories | 1.2% | >2.0% | $0.40-0.70 | 1.5-2.5% |
| Electronics | 0.8% | >1.5% | $0.50-1.00 | 1.0-2.0% |
| Home & Garden | 1.0% | >1.8% | $0.35-0.65 | 1.5-3.0% |
| Health & Beauty | 1.5% | >2.5% | $0.30-0.55 | 2.0-3.5% |
| Grocery & Food | 1.8% | >3.0% | $0.20-0.40 | 2.5-4.0% |
| Toys & Games | 1.3% | >2.2% | $0.25-0.50 | 2.0-3.5% |
| Sports & Outdoors | 1.0% | >1.7% | $0.35-0.65 | 1.5-2.5% |
| Auto Parts | 0.7% | >1.2% | $0.40-0.80 | 1.0-2.0% |

### Performance Diagnostic Tree

**Low impressions:**
1. Check disapprovals — products not serving at all?
2. Check price competitiveness — priced out of auctions?
3. Check title relevance — titles match search queries?
4. Check bid/budget (paid) — budget exhausting before end of day?
5. Check product ratings — competitors with ratings outranking you?

**Low CTR (impressions OK):**
1. Image quality — compelling vs generic?
2. Title quality — informative vs vague?
3. Price position — higher than competitors in same carousel?
4. Sale badge — competitors showing sales, you are not?
5. Shipping speed/cost — competitors showing "Free delivery" and you are not?

**Low conversion rate (clicks OK):**
1. Landing page match — does the page show what the listing promised?
2. Landing page speed — >3 seconds load time loses ~50% of mobile users
3. Price on landing page — any surprise fees or shipping costs?
4. Mobile experience — is the landing page mobile-optimized?
5. Availability — "Add to cart" immediately visible?

### Key Metrics to Track Weekly

| Metric | Red Flag |
|--------|----------|
| Disapproval rate | >5% or increasing trend |
| Impression share (paid) | <50% in target categories |
| CTR | Below category median |
| Click-to-conversion rate | <1% for most categories |
| Price competitiveness % | >30% of products uncompetitive |

---

## 5. Disapproval Workflows

### Top 10 Disapproval Reasons and Fix Paths

| # | Reason | Cause | Fix | Timeline |
|---|--------|-------|-----|----------|
| 1 | Misrepresentation | Misleading claims, missing business info | Remove superlatives, add return policy, add About Us page | 3-7 days, may need manual review |
| 2 | Price Mismatch | Feed price ≠ landing page price | Sync feed price to page exactly; check currency | 24-72h re-crawl |
| 3 | Availability Mismatch | Feed says in stock, page says out of stock | Sync inventory feed; increase update frequency | Next crawl |
| 4 | Missing GTIN | Has manufacturer GTIN but not in feed | Add GTIN or set `identifier_exists: no` | Immediate on next processing |
| 5 | Image Overlay | Watermarks, promo text on main image | Replace with clean product image | 24-72h re-crawl |
| 6 | Landing Page Error | 404/500 errors, geo-blocking Googlebot | Fix URLs; unblock Googlebot | Next crawl |
| 7 | Insufficient Product Data | Title/description too short or generic | Title >30 chars with brand+type; description >500 chars | Immediate |
| 8 | Missing Shipping Weight | Carrier-calculated rates but no weight in feed | Add `shipping_weight` or switch to flat-rate | Immediate |
| 9 | Restricted Product | Regulated category without verification | Verify compliance; apply for merchant verification if required | Varies |
| 10 | Duplicate Item ID | Same ID reused for different products | Assign unique, stable IDs per variant | Immediate |

### Disapproval Triage Matrix

| Volume | Same Reason? | Action |
|--------|-------------|--------|
| >100 products | Yes | Systematic root cause — fix feed template or feed rule, not individual items |
| >100 products | No | Group by reason, fix highest-volume first |
| 10-100 products | — | Fix in bulk via supplemental feed or feed rules |
| <10 products | — | Fix individually; watch for pattern |

### Appeal Process
1. Fix the issue first. Never appeal without fixing.
2. Wait 24-72 hours for automatic re-crawl.
3. If not resolved: Request manual review (Diagnostics > Item Issues > Request Review).
4. One appeal at a time. 7-day cooldown applies for repeated policy violations.

---

## 6. Feed Management

### Feed Method Decision Tree

```
Platform has native GMC integration (Shopify, WooCommerce)?
  YES → Use platform plugin as primary feed
        Need to override attributes the plugin doesn't support?
          YES → Add supplemental feed for overrides
          NO  → Plugin-only is sufficient
  NO  → Have developer resources?
        YES → Content API (real-time; best for >10K SKUs or fast inventory)
        NO  → Scheduled fetch (XML/CSV hosted on your server; update at least daily)
```

### Feed Types

| Feed Type | Use Case | Update Frequency |
|-----------|----------|-----------------|
| Primary feed | All products, all required attributes | Daily minimum; every 6h for fast-moving inventory |
| Supplemental feed | Override/add attributes without touching primary | As needed |
| Feed rules | Transform data at processing time (regex, lookups) | Applied every processing run |
| Content API | Real-time individual product updates | Real-time; 100K requests/day limit |
| Automated feeds | Google crawls your site | Google's schedule (not your control) |

### Supplemental Feed Strategy

Use supplemental feeds for:
- **Custom labels** — campaign segmentation (margin tiers, seasonality, priority)
- **Title A/B testing** — optimized titles without touching your CMS
- **Missing GTINs** — lookup table mapped to product IDs
- **Promotion IDs** — linking products to active promotions
- **Seasonal overrides** — holiday titles, temporary attribute changes

Supplemental feeds match on `id` — must exactly match the primary feed `id`.

---

## 7. Shopping Campaign Readiness

### Pre-Launch Checklist

| Check | Requirement |
|-------|-------------|
| Feed health score | >80 (Section 1 framework) |
| Disapproval rate | <5% of active products |
| Price competitiveness | >60% of products within +10% of benchmark |
| Landing page speed | <3 seconds, mobile-friendly |
| Conversion tracking | Google Ads tag firing, revenue tracking verified |
| Shipping info | Accurate in feed or account settings |

### Standard Shopping vs Performance Max

| Factor | Standard Shopping | Performance Max |
|--------|------------------|----------------|
| Query control | High (negatives, search term reports) | Low (limited insights) |
| Bidding | Manual CPC or Target ROAS | Automated only |
| Best for | Tight ROAS targets, query-level strategy | Broad reach, new advertisers, >30 conv/month |
| Min daily budget | $5-10/day viable | $50-100/day recommended |
| Ramp-up | Immediate | 2-4 week learning phase |

### Custom Label Strategy

| Slot | Use | Example Values |
|------|-----|----------------|
| `custom_label_0` | Margin tier | high_margin, medium_margin, low_margin |
| `custom_label_1` | Product priority | hero, standard, long_tail |
| `custom_label_2` | Seasonality | evergreen, summer, holiday, clearance |
| `custom_label_3` | Price range | under_25, 25_to_100, over_100 |
| `custom_label_4` | Performance tier | top_seller, average, underperformer, new |

### ROAS Targets by Category (Starting Points)

| Category | Conservative ROAS | Aggressive ROAS |
|----------|------------------|-----------------|
| Apparel | 400-600% | 200-300% |
| Electronics | 600-800% | 300-500% |
| Home & Garden | 400-600% | 200-400% |
| Health & Beauty | 300-500% | 150-300% |
| Grocery | 200-400% | 100-200% |

---

## Output Format

- Start with a **Feed Health Score** (0-100) and top-line summary
- Group findings into: **Critical** (disapprovals, policy) → **High** (data quality, price) → **Medium** (optimization) → **Low** (nice-to-have)
- Include specific product counts and percentages per issue
- Provide exact fix instructions, not general advice
- Mark estimates with ⚠️ when based on incomplete data
- End with a **prioritized action plan** (numbered, with effort: 5min / 30min / 2hrs / half-day)
- Include a **7-day and 30-day check-in plan**
