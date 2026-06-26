# Meta Ads Strategy Guide for Ecommerce

## Full-Funnel Campaign Architecture

### Top of Funnel (TOF) — Prospecting

**Objective**: Introduce your brand to new audiences and build retargeting pools.

**Campaign Types**:
- **Advantage+ Shopping (ASC)**: Meta's algorithmic campaign using ML to find purchasers. Best for accounts with 500+ purchases/month. Set existing customer cap at 20-30%.
- **Standard Prospecting**: Manual audience selection with lookalikes or interests. More control over audience composition.

**Key Metrics**: CPM, CTR, CPC, cost per landing page view, thumbstop rate. Evaluate on qualified traffic volume, not direct ROAS — TOF will always have the lowest ROAS of any tier.

### Middle of Funnel (MOF) — Consideration

**Objective**: Deepen engagement with people who showed initial interest but lack purchase intent.

**Campaign Types**: Engagement retargeting (site visitors, social engagers, video viewers), lead generation for email/SMS capture, content consumption campaigns driving traffic to buying guides or quizzes.

**Key Metrics**: Engagement rate, video view rate, cost per engagement, CTR to product pages.

### Bottom of Funnel (BOF) — Conversion

**Objective**: Convert high-intent prospects and drive repeat purchases.

**Campaign Types**: Dynamic Product Ads (highest ROAS type), cart abandonment retargeting, customer retention/cross-sell, promotional campaigns for warm audiences.

**Key Metrics**: ROAS, CPA, conversion rate, AOV. BOF delivers highest ROAS but has limited audience size — over-investing here without feeding TOF leads to exhaustion.

---

## Audience Building Methodology

### First-Party Data Foundation

**Customer Lists**: Upload segmented lists by recency, frequency, AOV, and LTV. High-value segments produce the best lookalike seeds.

**Pixel Event Audiences** (ranked by signal strength):
1. Purchase > 2. Initiate Checkout > 3. Add to Cart > 4. View Content > 5. Page View

Use recency windows strategically: 0-7 days for highest intent, 30-180 days for larger lookalike seeds.

**Engagement Audiences**: IG/FB profile visitors, ad engagers (saved, shared, commented), video viewers at 25/50/75/95% completion thresholds.

### Lookalike Strategy

Seed quality matters more than size. A 1% lookalike from 500 high-LTV customers outperforms one from 50K email subscribers.

**Recommended Stack**:
- Tier 1: 1% LAL purchasers, 1% LAL high-AOV, 1% LAL repeat buyers
- Tier 2: 1% LAL add-to-cart, 1% LAL email subscribers
- Tier 3: 2-3% LAL purchasers and high-AOV
- Tier 4 (scaling): 4-5% and 5-10% LALs

For testing, keep LALs separate. For scaling, stack multiple LALs into one ad set for broader algorithm optimization.

### Interest and Broad Targeting

**Interest Stacking**: Combine related interests within a single ad set (OR logic) for larger, more stable audiences. Research competitors, publications, influencers, and lifestyle correlations.

**Broad Targeting**: Zero detailed targeting works surprisingly well for accounts with strong pixel data. Meta's algorithm often finds buyers better than manual interest selection.

---

## Creative Best Practices

### By Format

**Static Images**: Bold, high-contrast visuals. Product as hero element. One clear value proposition as text overlay. Keep text under 20% of image. Test lifestyle vs. clean product shots.

**Video Ads**: Hook within 3 seconds. 6-15s for Stories/Reels, 15-30s for Feed. Design for sound-off with captions. UGC-style consistently outperforms polished brand video for direct response. Test multiple hooks with the same body.

**Carousel Ads**: First card must be strongest. Tell a sequential story (problem > solution > benefits > proof > CTA). 3-5 cards is optimal. Consistent visual style across cards.

**Collection/Instant Experience**: Strong hero image or video at top. Feature bestsellers or themed collections. One theme, one CTA, minimal friction.

### By Placement

**Feed (FB/IG)**: 1:1 or 4:5 ratio. Where most conversions occur. Longer copy works (3-5 visible lines). Carousels and collections perform well.

**Stories/Reels**: 9:16 vertical only. Native, organic feel outperforms polished ads. Front-load message in 2-3 seconds. Use motion, text overlays, stickers. Never repurpose horizontal creative.

---

## The Testing Framework

### Creative Testing (Primary Lever)

1. Launch 3-5 variants in one ad set against a proven audience
2. Equal budget distribution (not CBO) for fair exposure
3. Run 3-7 days or until 50+ link clicks per variant
4. Winner by CPA or ROAS
5. Iterate on winner: new hooks, CTAs, formats with winning angle
6. Move winner to scaling campaigns
7. Repeat every 1-2 weeks

**Test Priority**: Angle/concept > Hook > Format > Visual style > Copy length > CTA > Offer framing

### Audience Testing

Use CBO with multiple ad sets targeting different audiences. Let Meta allocate budget. Run 7-14 days. Test LAL percentages, LAL seeds, interest stacks vs. broad, and geographic expansion.

### Scaling

**Vertical**: Increase budget 20-30% every 3-5 days. If CPA spikes 30%+, revert and wait 5 days.

**Horizontal**: Duplicate winning ad sets with new audiences. Keep creative identical. Only duplicate ad sets profitable for 7+ days.

**ASC Scaling**: Budget increases of 30-50% are safe. Can increase more frequently than standard campaigns.

---

## Advantage+ Campaigns

### When to Use ASC
- 500+ monthly purchases, 5+ creative variants, spending $100+/day on prospecting

### Configuration
- Existing customer cap at 0-30%
- Upload 10-20 creative variants (mixed formats)
- Country-level targeting only
- Add Cost Cap or Min ROAS after exiting learning phase

### Limitations
- Limited audience control and transparency
- Cannot exclude specific audiences beyond existing customer cap
- Not ideal for budgets under $50/day

### Advantage+ Audience
For standard campaigns, provide 3-5 interest suggestions as directional signals. Meta expands beyond them automatically. Works well with strong creative that self-selects the right audience.

---

## Catalog Ads (Dynamic Product Ads)

### Requirements
- Product catalog in Commerce Manager with accurate data
- Pixel events mapped to catalog items (content_ids matching catalog IDs)
- Feeds updated daily minimum

### Campaign Types
- **Retargeting DPA**: Show specific products users viewed or added to cart. Highest ROAS campaign type.
- **Broad Catalog (DABA)**: Catalog products shown to prospecting audiences based on purchase likelihood prediction.

### Optimization
- Use creative overlays for pricing, discounts, or shipping badges
- Create branded catalog templates
- Test carousel vs. collection format
- Use product sets: bestsellers, new arrivals, high-margin items, seasonal collections
