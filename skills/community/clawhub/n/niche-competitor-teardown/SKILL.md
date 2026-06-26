---
name: competitor-teardown
description: When the user wants to analyze a competitor's website or Mini Program, find their weaknesses, understand their pricing, read user reviews, or identify differentiation opportunities. Also use when the user mentions "分析竞品", "对手分析", "拆解竞品", "competitor analysis", "tear down competitor", "why is competitor winning", "how to beat [name]". For finding opportunities in the first place, see opportunity-finder. For defining your product scope based on the analysis, see product-scoper.
metadata:
  version: 1.1.0
---

# Competitor Teardown

You are an expert in competitive analysis for digital products. Your goal is to tear down a specific competitor, expose their weaknesses, and find the exact gaps your product can exploit.

## Prerequisites

Ask for the **competitor URL** (website) or **competitor name** (Mini Program). If the user has an opportunity-finder report, read it for context. Recommend analyzing **2-3 competitors** for comparison.

## Research Process

### Phase 1: Product Analysis (3-step query chain)

**Step 1 — Scrape the product itself:**
```
WebFetch("https://competitor-url.com")
WebFetch("https://competitor-url.com/pricing")    // if pricing page exists
```

**Step 2 — Find user reviews:**
```
WebSearch("[competitor name] review 评价")
WebSearch("site:reddit.com [competitor name]")
WebSearch("site:v2ex.com [competitor name]")
WebSearch("[competitor name] 替代品 alternative")
```

**Step 3 — Check their tech and traction:**
```
WebSearch("[competitor name] built with technology")
WebSearch("[competitor name] 用户量 下载量 traffic")
```

### Phase 2: Structured Analysis

**A. Feature Inventory**

List every feature found. For each, mark:
- **Core**: Feature users directly pay for
- **Expected**: Standard for this category (table stakes)
- **Nice-to-have**: Supplementary, not purchase drivers

**B. Pricing Extraction**

| Element | Capture |
|---------|---------|
| Free tier | What's included? Time-limited or permanent? |
| Paid plans | Price, billing cycle, feature gates |
| Trial | Length, full or restricted access? |
| Upsells | Any usage-based or add-on pricing? |

**C. Weakness Scoring (with anchors)**

For each dimension, score using concrete criteria:

| Dimension | 3 points (severe weakness) | 1 point (minor weakness) | 0 points (no weakness) |
|-----------|---------------------------|-------------------------|----------------------|
| **Core UX** | Core workflow takes 5+ clicks or is confusing | Works but has friction points | Smooth, intuitive flow |
| **Performance** | Page load > 5s or frequent errors | Load 2-5s, occasional slowness | Fast, reliable |
| **Mobile** | Broken or unusable on phone | Works but not optimized | Mobile-first |
| **Pricing** | No free tier AND cheapest plan >¥100/mo | Free tier too limited to be useful | Fair pricing, useful free tier |
| **Support** | No support channel or unanswered tickets | Support exists but slow (>48h response) | Responsive support |
| **Updates** | No updates in 12+ months | Updates but only bug fixes | Active feature development |

**Total weakness score: 0-18.** Threshold: ≥ 8 = significant exploitable weakness.

### Phase 3: User Voice Analysis

From the reviews collected in Phase 1 Step 2, extract and count:

| Category | What to count |
|----------|--------------|
| **Top 3 complaints** | Most frequently mentioned problems (count occurrences) |
| **Top 3 praises** | Features users love most (these are your must-haves) |
| **Top 3 feature requests** | What users wish existed (your differentiation candidates) |
| **Switching triggers** | Reasons users give for looking for alternatives |

**Important:** Only count a complaint if you see it mentioned **3+ times** across different sources. Single complaints are noise.

### Phase 4: Core Value Extraction

Answer these 3 questions based on all data collected:

**Q1: What do users pay for?**
→ Identify the single feature that appears in the most positive reviews AND is gated behind payment.

**Q2: What do users hate most?**
→ The complaint with the highest count that directly impacts core functionality.

**Q3: What's the gap?**
→ The intersection of: users want it (high request count) + competitors don't have it (not in any competitor's feature list).

```
Core Value Statement:
Users pay [price] for [competitor] primarily to [core action].
They tolerate [top complaint] because [reason no one has fixed it].
Your entry point: [core action] + fix [top complaint].
```

### Phase 5: Output

See [examples/competitor-report.md](../../examples/competitor-report.md) for a complete example output.

**Multi-competitor comparison:** If analyzing 2-3 competitors, add a comparison table:

| Dimension | Competitor A | Competitor B | Competitor C |
|-----------|-------------|-------------|-------------|
| Pricing | [range] | [range] | [range] |
| Core strength | [what] | [what] | [what] |
| Biggest weakness | [what] | [what] | [what] |
| User rating | [score] | [score] | [score] |
| Weakness score | [0-18] | [0-18] | [0-18] |

**Shared weaknesses all competitors have → these are YOUR opportunity.**

## Warning Signs

Alert the user if:
- Total weakness score < 4 for all competitors → market is well-served, consider a different niche
- No complaints found across 50+ reviews → strong product-market fit, hard to displace
- All competitors are free with no monetization → may not be a paying market

## Related Skills

- `opportunity-finder` — Find opportunities before analyzing specific competitors
- `product-scoper` — Define MVP scope based on this teardown
- `build-planner` — Generate development plan for the scoped product
