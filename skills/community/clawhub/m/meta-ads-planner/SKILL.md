---
name: Meta Ads Planner
version: 1.1.0
description: Plan profitable Facebook and Instagram ad campaigns for ecommerce businesses with structured audience segmentation, creative strategy, placement optimization, bidding configuration, and budget allocation across funnel stages.
category: ecommerce
tags:
  - meta-ads
  - facebook-ads
  - instagram-ads
  - paid-social
  - ecommerce
  - advertising
  - campaign-planning
  - roas
  - audience-targeting
  - creative-strategy
  - budget-optimization
  - performance-marketing
---

# Meta Ads Planner

## Introduction

Meta advertising remains the most powerful paid acquisition channel for ecommerce. With over 3 billion monthly active users across Facebook and Instagram, the platform offers unmatched reach and a mature auction system that rewards advertisers who understand its mechanics. However, the complexity has grown dramatically between Advantage+ campaigns, dynamic creative optimization, ongoing signal loss from privacy changes, and the sheer number of configuration options.

This skill provides a systematic framework for planning Meta ad campaigns structured for profitability from day one. You will build campaigns with clear audience segments mapped to funnel stages, creative briefs tied to formats and placements, bidding strategies matched to margin structures, and budget allocations that balance prospecting with retargeting. The approach works from $3,000 to $300,000 per month.

The framework is designed for ecommerce operators, media buyers, and marketing managers who need to move beyond "boost post" tactics. It assumes you have a functioning Meta Business Manager, a properly installed Meta Pixel or Conversions API, and a product catalog.

## Quick Reference

| Aspect | Detail |
|---|---|
| Platform | Meta (Facebook + Instagram) |
| Funnel Stages | TOF (Top), MOF (Middle), BOF (Bottom) |
| Budget Split | 60% TOF / 20% MOF / 20% BOF (adjust by maturity) |
| Primary KPIs | ROAS, CPA, CPM, CTR, AOV, Conversion Rate |
| Audience Types | Lookalike, Interest-Based, Retargeting, Broad/Advantage+ |
| Creative Formats | Static Image, Video (6-15s), Carousel, Collection |
| Bidding Options | Lowest Cost, Cost Cap, Bid Cap, Min ROAS |
| Testing Framework | Creative Testing > Audience Testing > Scaling |
| Optimization Window | 3-7 days per test, 50+ conversions for significance |

## Solves

### 1. Wasted Ad Spend on Broad Audiences
Segments audiences by funnel stage and intent level, ensuring each dollar has a clear strategic purpose rather than burning budget on untargeted reach.

### 2. Poor Return on Ad Spend (ROAS)
Aligns messaging to funnel stage, matches bid strategies to margin targets, and sets clear ROAS thresholds for each campaign tier.

### 3. Wrong Audience Targeting
Builds audiences from first-party data outward to lookalikes and tested interest stacks, creating a reliable targeting hierarchy rather than relying on guesswork.

### 4. Creative Fatigue and Stagnation
Includes a structured creative testing plan with rotation schedules, format diversification, and clear criteria for retiring or iterating on creatives.

### 5. Inefficient Budget Allocation
Provides starting budget ratios by business maturity and scales dynamically based on performance data, preventing over-investment in retargeting or under-investment in prospecting.

### 6. Misaligned Bidding Strategy
Matches each bidding strategy to specific use cases and margin structures so you avoid cost spikes from lowest-cost or underdelivery from aggressive caps.

### 7. No Measurement or Testing Discipline
Defines test parameters, sample sizes, success criteria, and a decision matrix for scaling, iterating, or killing campaigns.

## Step-by-Step Workflow

### Step 1: Audit Current State
1. **Review account structure**: Document active campaigns, identify overlapping audiences and redundant campaigns
2. **Analyze 90-day performance**: Identify top campaigns by ROAS, CPA, and volume; note winning audiences and creatives
3. **Verify tracking**: Confirm Pixel fires on all key events (ViewContent, AddToCart, InitiateCheckout, Purchase); check CAPI implementation and event match quality (target 6.0+)
4. **Assess creative library**: Catalog existing assets by format, age, and performance; identify format gaps
5. **Document baselines**: Record current monthly spend, blended ROAS, CPA, and AOV

### Step 2: Define Audience Segments
1. **BOF retargeting**: Cart abandoners (7/14/30 days), checkout abandoners, product viewers, past purchasers for cross-sell
2. **MOF engagement**: Website visitors (30/60 days) excluding BOF, social engagers (30/60/90 days), video viewers (50%+ completion), email subscribers
3. **TOF prospecting**: Lookalikes (1%, 2-3%, 4-5%) from purchasers and high-AOV buyers, interest-based stacks, Advantage+ Shopping, broad targeting
4. **Exclusion strategy**: Exclude purchasers from prospecting, BOF from MOF, ensure no overlap between tiers

### Step 3: Plan Creative Strategy
1. **Map angles to funnel**: TOF (problem/solution, social proof, curiosity), MOF (education, testimonials, comparison), BOF (urgency, offers, cart reminders, reviews)
2. **Plan format mix**: Feed (1:1/4:5 static, carousel, short video), Stories/Reels (9:16 vertical video, 6-15s), Collection (hero + catalog)
3. **Define testing plan**: Test one variable at a time, 3-5 variants per ad set, weekly or biweekly creative refreshes
4. **Establish production pipeline**: Define who produces creatives, turnaround times, and UGC sourcing

### Step 4: Set Placement Strategy
1. **Review historical placement data**: Check CPM, CTR, and conversion rate by placement
2. **Configure groups**: Primary (FB/IG Feed, IG Stories, IG Reels), Secondary (FB Stories/Reels, Marketplace), Test (Messenger, Search)
3. **Match creative to placement**: Use placement asset customization; never run square images in Stories
4. **Consider Advantage+ placements** for mature campaigns with sufficient data

### Step 5: Configure Bidding
1. **Match strategy to phase**: Lowest Cost for learning, Cost Cap for scaling, Bid Cap for strict ceilings, Min ROAS for revenue optimization
2. **Set targets**: Calculate breakeven CPA (AOV x margin), set cost caps 20-30% above breakeven
3. **Plan for learning phase**: Budget for 50 optimization events per week per ad set; avoid edits that reset learning
4. **Define escalation rules**: CPA exceeds 1.5x target for 3+ days triggers intervention

### Step 6: Allocate Budget
1. **Calculate total budget**: Monthly Budget = Target Revenue / Target ROAS
2. **Allocate by funnel**: Early (70/15/15), Growth (60/20/20), Mature (50/25/25)
3. **Reserve testing budget**: 10-20% for new audiences and creative experiments
4. **Plan scaling**: Vertical (20-30% increases every 3-5 days) and horizontal (duplicate winners with new audiences)

### Step 7: Build Measurement Plan
1. **Set KPIs by stage**: TOF (CPM, CTR, CPC), MOF (engagement rate, video views), BOF (ROAS, CPA, conversion rate), Blended (MER)
2. **Define testing protocol**: 3-7 day minimum, 50+ conversions per variant, 90% confidence threshold
3. **Set review cadence**: Daily monitoring, weekly optimization, monthly strategic review
4. **Create decision matrix**: Scale (above target), Iterate (near target with fatigue), Pause (below breakeven 5+ days)

## Full Examples

### Example 1: Fashion DTC Brand Launching New Collection

**Context**: Women's fashion DTC launching a 25-piece spring collection. Current spend $15K/month, 3.2x ROAS, $85 AOV. Goal: $120K revenue in 30 days at 2.5x+ ROAS.

**Budget**: $120K / 2.5 = $48K over 30 days ($1,600/day).

**Audience Strategy**:
- TOF (60%, $28.8K): 1% LAL purchasers ($8K), 2-3% LAL high-AOV ($6K), interest stack fashion/competitors ($6K), Advantage+ Shopping ($8.8K)
- MOF (20%, $9.6K): Site visitors 30d ($4K), IG engagers 60d ($3K), email non-purchasers ($2.6K)
- BOF (20%, $9.6K): ATC 14d ($4K), collection page viewers 7d ($3K), past purchasers cross-sell ($2.6K)

**Creative**: TOF gets lifestyle lookbook video, hero carousel, UGC haul video, problem/solution static. MOF gets BTS content, testimonial carousel, product detail shots. BOF gets DPA, launch offer, social proof overlays.

**Bidding**: Lowest Cost for 7 days, then Cost Cap at $34 CPA for TOF. Min ROAS 2.5x for BOF. Creative fatigue alert at frequency 3.0+.

### Example 2: Supplements Brand Scaling $5K to $50K/Month

**Context**: Protein powder ($45), greens blend ($55), bundle ($89). Spending $5K/month at 4.1x ROAS, mostly retargeting. Goal: $50K/month at 2.8x+ blended ROAS.

**Phase 1 ($15K/month)**: Shift to 65/20/15 split. Test 4 LAL audiences and 3 interest ad sets. Produce 10 creative variants (4 static, 3 UGC video, 2 carousel, 1 collection). Lowest Cost bidding.

**Phase 2 ($30K/month)**: Scale Phase 1 winners by 25% every 5 days. Add ASC at $200/day. Expand creative (ingredient education, comparisons, transformations). Cost Cap at $18 CPA for TOF. Launch Reels/Stories campaign.

**Phase 3 ($50K/month)**: Horizontal scaling with expanded LALs (3-5%, 5-7%). Vertical scaling on top 3 campaigns. Broad targeting test. Full creative rotation (5 new/week, retire CTR below 1%). Min ROAS bidding at 2.8x.

**Final Allocation**: TOF LALs $12K, TOF Interest $6K, TOF ASC $10K, TOF Broad $4K, MOF $10K, BOF $8K.

## Common Mistakes

1. **Testing too many variables at once** — Change one thing per experiment. Multiple simultaneous changes make results uninterpretable.
2. **Killing campaigns during learning phase** — Allow 5-7 days and 50+ conversions before judging. Premature edits reset the algorithm.
3. **Ignoring retargeting frequency** — Monitor frequency; rotate creative when it exceeds 3-4. High frequency wastes budget and annoys prospects.
4. **Same creative across all funnel stages** — Cold prospects need different messaging than cart abandoners. Tailor creative to audience temperature.
5. **Desktop-first creative** — Over 90% of impressions are mobile. Design for mobile first, then adapt.
6. **Unrealistic CPA/ROAS targets** — Aggressive caps restrict delivery. Start 20-30% above goal and tighten as campaigns mature.
7. **Budget fragmentation** — Too many ad sets on a small budget means none exit learning. At $5K/month, run 3-4 ad sets maximum.
8. **Missing funnel exclusions** — Without exclusions, TOF shows ads to purchasers and BOF targets people who never visited. Always configure exclusions.
9. **Relying solely on in-platform metrics** — Cross-reference with GA, your ecommerce platform, and post-purchase surveys. Track MER as a blended metric.
10. **Scaling too fast** — 100% budget increases overnight crash performance. Scale 20-30% every 3-5 days or duplicate ad sets horizontally.

## Resources

### Meta Official
- Meta Business Help Center: Campaign objectives and optimization
- Meta Blueprint: Free advertising courses
- Meta Ads Guide: Format specs and placement details
- Conversions API documentation: Server-side tracking setup

### Recommended Tools
- Triple Whale / Northbeam: Third-party attribution
- Motion: Creative performance analytics
- Foreplay: Ad creative swipe file and competitor research
- Meta Creative Hub: Ad mockup and preview

### Key Metrics Glossary
- **ROAS**: Return on Ad Spend (revenue / spend)
- **CPA**: Cost per Acquisition (spend / conversions)
- **CPM**: Cost per 1,000 Impressions
- **CTR**: Click-Through Rate (clicks / impressions)
- **AOV**: Average Order Value
- **MER**: Marketing Efficiency Ratio (total revenue / total marketing spend)
- **LTV**: Lifetime Value
- **Thumbstop Rate**: 3-second video view rate
- **Frequency**: Average times each person sees your ad
