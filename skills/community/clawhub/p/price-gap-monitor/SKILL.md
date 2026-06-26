---
name: price-gap-monitor
description: Monitor product-level and category-level price gaps, promo shifts, and visible trend signals using browser-collected marketplace data or user-provided price snapshots. Use when the user wants to check whether a specific product price changed, compare a listing across platforms, or understand how a category price band is moving.
---

# Price Gap Monitor

Track visible price movement without pretending to know private marketplace data.

This skill supports **two operating modes** under the same name.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Data source selection | Browser-collected live snapshots from 3+ platforms with normalized timestamps | User-provided snapshots from 2 platforms with date context | Single screenshot with no timestamp or platform context |
| Price normalization | Unit price + currency + shipping aligned across all listings | Prices compared in same currency but shipping not factored | Raw prices compared across different units or currencies |
| Trend evidence strength | 3+ time-separated snapshots showing consistent direction | 2 snapshots with clear delta and date labels | Single snapshot described as a "trend" |
| Coverage labeling | Explicit platform list, search terms used, and gaps noted | Platforms listed but coverage gaps not mentioned | "Full market analysis" claimed from partial data |
| Competitive context | Price positioned against 5+ visible competitors with ranking | Compared to 2-3 key competitors | Compared to a single competitor or no context |
| Recommendation quality | Specific action with margin impact estimate and timeline | Directional recommendation with general reasoning | Vague "monitor the market" without actionable next steps |
| Anomaly handling | Outliers flagged, investigated, and explained or excluded | Outliers noted but not investigated | Outliers silently included or excluded without mention |
| Evidence honesty | Every claim tied to a visible, timestamped source | Most claims sourced but some inferred | Fabricated history or unverifiable claims presented as fact |

## Solves

- **Blind pricing decisions**: Seller is setting or adjusting prices without checking what competitors actually charge on visible marketplaces.
- **Cross-platform price drift**: Same product listed at different prices across Amazon, Walmart, Temu, TikTok Shop — seller doesn't know where they're under or over.
- **Promo impact blindness**: Competitor ran a flash sale or coupon and the seller missed it, losing traffic without understanding why.
- **Category-level mispricing**: Seller positioned in a price band that doesn't match the visible market center, either leaving money on the table or pricing themselves out.
- **Snapshot vs. trend confusion**: Seller reacts to a single price check as if it's a trend, making premature adjustments.
- **Margin floor violations**: Price changes made reactively without checking whether the new price still clears minimum margin requirements.
- **Fabricated data reliance**: Previous analyses or tools claimed access to private sales data, BSR history, or internal marketplace metrics — this skill provides honest, evidence-based alternatives.

## Mode A — Product-level price trend monitoring

Use this mode when the user asks about:

- one specific product
- one brand-specific model
- one ASIN / listing / SKU
- one named product across multiple platforms

## Mode B — Category price-band monitoring

Use this mode when the user asks about:

- a product category
- a keyword-defined market
- a visible price band
- cross-platform category pricing patterns

## Browser-first guidance

When live browsing is available, prefer browser-collected data over asking the user to provide snapshots. The browser can visit marketplace search pages, product listing pages, and category pages to collect visible price signals in real time.

### When to suggest logged-in browsing

Suggest the user log in to their marketplace account when:

- guest pages show limited results or fail to load correctly
- location, cart, or account state is clearly affecting visible listings
- the task requires going deeper than a shallow guest snapshot

Suggested user-facing reminder:
- "If you want a cleaner and more complete Amazon read, log in first. Logged-in browsing usually gives more stable category pages, better listing continuity, and fewer interruptions."

Do not claim login guarantees full data access. Present it as a practical way to improve visibility and continuity.

## Core job

The goal is to produce a **decision-ready price snapshot with honest trend interpretation**.

This skill may use:
1. user-provided price snapshots, or
2. browser-collected public marketplace data

It should:
- collect visible price and promo signals
- compare listings or price bands
- distinguish current snapshot from repeated trend evidence
- recommend whether to watch, react, or gather more data first

It must **not** fabricate hidden marketplace history, real sales counts, or full competitive intelligence that isn't visible on public pages.

## Inputs

### Input type A — user-provided snapshots
- competitor price tables
- prior exported marketplace snapshots
- your current price baseline
- target margin floor
- promo windows or campaign timing

### Input type B — browser-collected public data
- a product model name
- an ASIN / SKU / listing URL
- a category keyword
- target platforms (Amazon, Temu, TikTok Shop, Walmart, etc.)
- market / locale (US, UK, JP, DE, etc.)

## Workflow

### Mode A — Product-level workflow

1. **Define the exact product scope.**
   - Confirm the specific product name, model, ASIN, or SKU.
   - Identify which platforms to check (default: Amazon, Walmart, Temu).
   - Record the user's current price and margin floor.

2. **Collect visible public signals.**
   - For each platform, search for the exact product or closest match.
   - Record: listing price, shipping cost, any visible coupons or promos, seller name, listing date if visible.
   - Take note of "Sponsored" vs organic placement.
   - Capture the timestamp of each observation.

3. **Normalize comparison points.**
   - Convert all prices to the same currency.
   - Calculate unit price if products come in different pack sizes.
   - Add shipping to get landed cost where visible.
   - Flag any listings that are clearly different products (wrong model, refurbished, etc.).

4. **Determine evidence strength.**
   - Single snapshot = "current position only, no trend."
   - Two snapshots with time gap = "directional signal, not confirmed trend."
   - Three or more time-separated snapshots = "visible trend with stated confidence."

5. **Produce the result.**
   - Fill in the output template (see `references/output-template.md`).
   - Include executive summary, snapshot data, comparison, trend assessment, and recommendation.
   - Never claim more confidence than the evidence supports.

### Mode B — Category-level workflow

1. **Define the category scope.**
   - Confirm the category keyword, price band of interest, and target platforms.
   - Ask whether the user wants top-10, top-20, or broader coverage.

2. **Collect visible top listings.**
   - Search each platform for the category keyword.
   - Record the first 10-20 organic results: price, title, seller, rating count, any promo badges.
   - Note any sponsored listings separately.

3. **Cluster the market.**
   - Group listings into price bands (e.g., budget < $15, mid $15-30, premium > $30).
   - Calculate band center, min, max for each cluster.
   - Identify where the user's product sits relative to clusters.

4. **Determine evidence strength.**
   - Apply the same snapshot vs. trend rules as Mode A.
   - For categories, also note: search result count, how many pages deep you went, any platform-specific filters applied.

5. **Produce the result.**
   - Fill in the category-level output template.
   - Include band analysis, competitive position, and recommended pricing action.

## Trend interpretation rules

1. **Single snapshot rule**
   - If only one fresh snapshot is available, describe the result as "current observed position" — never as a trend, movement, or shift.
   - Recommended language: "As of [date], the visible price is..."

2. **Two-snapshot rule**
   - With two time-separated observations, label the change as a "directional signal" and explicitly note the time gap.
   - Recommended language: "Between [date1] and [date2], the visible price moved from X to Y — this is a directional signal, not a confirmed trend."

3. **Trend-confirmed rule**
   - Three or more consistent, time-separated observations in the same direction may be labeled a "visible trend."
   - Always state the number of observations, the time span, and the direction.

4. **Partial coverage rule**
   - If less than 60% of the market is visible, clearly label the result as partial coverage.
   - Never present partial scraping as full category or full brand coverage.

5. **History rule**
   - Never fabricate prior price history.
   - Never imply long-term movement when only current public pages were checked once.

## Worked Example 1 — Product-level (Mode A)

**User request:** "Check how my silicone baking mat is priced vs competitors on Amazon and Walmart. My current price is $12.99, margin floor is $9.50."

**Step 1 — Define scope:**
Product: Silicone Baking Mat, Half Sheet Size. Platforms: Amazon US, Walmart US. Current price: $12.99. Margin floor: $9.50.

**Step 2 — Collect signals (browser):**

| Platform | Listing | Price | Ship | Promo | Seller | Timestamp |
|---|---|---|---|---|---|---|
| Amazon | Silicone Baking Mat Set (2pk) | $11.97 | Free (Prime) | 5% coupon | KitchenPro | 2025-05-01 14:30 UTC |
| Amazon | Premium Silicone Mat - Half | $14.49 | Free (Prime) | None | BakeRight | 2025-05-01 14:31 UTC |
| Amazon | Silicone Baking Mat | $9.99 | +$3.49 | Lightning Deal | ValueBake | 2025-05-01 14:31 UTC |
| Walmart | Silicone Baking Mat | $10.88 | Free (W+) | Rollback | MainStay | 2025-05-01 14:35 UTC |
| Walmart | Mainstays Silicone Mat 2pk | $12.47 | Free (W+) | None | Walmart | 2025-05-01 14:36 UTC |

**Step 3 — Normalize:**
- Convert 2-packs to per-unit: KitchenPro = $5.99/mat, Walmart 2pk = $6.24/mat.
- Add shipping: ValueBake landed = $13.48 (2pk not comparable — single mat).
- Flag: KitchenPro and Walmart 2pk are multi-packs; direct comparison requires noting pack size.

**Step 4 — Evidence strength:**
Single snapshot (one collection session on 2025-05-01). Result: "Current position only, no trend."

**Step 5 — Result summary:**
"As of May 1 2025, your $12.99 single mat sits in the mid-range. Single-mat competitors range $9.99–$14.49 on Amazon and $10.88–$12.47 on Walmart. One Amazon competitor (ValueBake) is running a Lightning Deal at $9.99 + $3.49 shipping. Your price clears the $9.50 margin floor. Recommendation: No immediate action needed. The Lightning Deal is temporary. Suggest re-checking in 48 hours to confirm ValueBake returns to regular pricing."

## Worked Example 2 — Category-level (Mode B)

**User request:** "What does the portable blender category look like on Amazon US right now? I'm launching at $24.99."

**Step 1 — Define scope:**
Category: "portable blender." Platform: Amazon US. User's planned launch price: $24.99. Coverage: top 15 organic results.

**Step 2 — Collect top listings:**

| Rank | Title (short) | Price | Rating Count | Promo | Seller |
|---|---|---|---|---|---|
| 1 | BlendJet 2 | $33.99 | 142,000 | None | BlendJet |
| 2 | PopBabies Personal | $23.99 | 28,500 | 10% coupon | PopBabies |
| 3 | Hamilton Beach | $19.99 | 15,200 | None | Hamilton |
| 4 | Ninja Blast | $39.99 | 8,400 | None | Ninja |
| 5 | KOIOS USB Blender | $21.99 | 12,100 | Lightning | KOIOS |
| ... | (10 more listings) | $14.99–$45.99 | varies | varies | varies |

**Step 3 — Cluster:**
- Budget (< $20): 4 listings, band center $17.49
- Mid ($20–$30): 6 listings, band center $24.32
- Premium (> $30): 5 listings, band center $37.99

**Step 4 — Evidence strength:**
Single snapshot, 15 of estimated 400+ results. Partial coverage (~4%).

**Step 5 — Result summary:**
"As of this snapshot, the mid-band ($20–$30) is the most crowded segment with 6 of the top 15 results. Your $24.99 launch price sits almost exactly at the mid-band center ($24.32). The segment leader (BlendJet, $33.99) has massive review count dominance. At $24.99 you'll compete directly with PopBabies ($23.99 + 10% coupon = ~$21.59 effective) and KOIOS ($21.99 with Lightning Deal). Recommendation: Your price is viable for launch but you'll face coupon/deal pressure from established mid-band sellers. Consider whether a launch coupon at $21.99 would help with initial velocity without dropping below margin floor."

## Common mistakes

1. **Calling a single snapshot a "trend"** — One price check is a position, not movement. Always label evidence strength honestly.

2. **Ignoring pack-size differences** — Comparing a 2-pack at $11.97 to a single item at $12.99 without normalizing to per-unit price leads to wrong conclusions.

3. **Forgetting shipping costs** — A $9.99 item with $4.99 shipping is more expensive than a $13.99 Prime item. Always calculate landed cost.

4. **Treating Lightning Deals as permanent** — Temporary promotions should be flagged as time-limited. Don't recommend permanent price cuts to match a 6-hour deal.

5. **Claiming "full market coverage"** — Checking the first page of Amazon results is not a full market scan. State exactly how many listings were checked and from which platforms.

6. **Fabricating price history** — Never say "prices have been declining over the past quarter" unless you have 3+ time-separated data points showing this. If you only checked once, say so.

7. **Mixing sponsored and organic listings** — Sponsored placements appear at different prices due to advertising investment. Flag them separately and don't include them in organic price band calculations.

8. **Recommending below margin floor** — Always check the user's stated margin floor before suggesting a price drop. If the competitive pressure requires going below the floor, flag this explicitly as a trade-off decision.

9. **Ignoring platform-specific pricing rules** — Some platforms (Walmart) have price parity requirements. Don't recommend platform-specific pricing without noting potential policy conflicts.

10. **Presenting competitor prices without context** — A low-priced competitor with 12 reviews is different from one with 12,000 reviews. Include rating count and review velocity when available as context for competitive positioning.

## Resources

- [Output template](references/output-template.md) — Structured output format for both Mode A and Mode B results.
- [Pricing data collection guide](references/pricing-data-guide.md) — How to collect, normalize, and validate pricing data from marketplaces.
- [Platform comparison reference](references/platform-comparison-guide.md) — Platform-specific pricing nuances for Amazon, Walmart, Temu, TikTok Shop, and others.
