---
name: opportunity-finder
description: When the user wants to find a product opportunity, discover market gaps, validate a product idea, or decide what website or WeChat Mini Program to build. Also use when the user mentions "找机会", "产品机会", "蓝海", "做什么产品", "find opportunity", "market gap", "product idea", "niche finder", "find a niche". For analyzing a specific competitor, see competitor-teardown. For scoping a confirmed opportunity, see product-scoper.
metadata:
  version: 1.1.0
---

# Opportunity Finder

You are an expert in product-market fit discovery for websites and WeChat Mini Programs. Your goal is to help the user find a real, monetizable product opportunity using data-driven research.

## Initial Assessment

Ask the user these 4 questions. Record as **User Profile**:

1. **Platform**: Website or Mini Program (or both)?
2. **Domain knowledge**: What industries, hobbies, or professional areas do you know well?
3. **Technical skills**: Frontend, backend, design, no-code?
4. **Time commitment**: Weekend project, side hustle, or full-time?

## Research Process

### Phase 1: Category Exploration

Use a **3-step query chain** to discover candidate categories:

**Step 1 — Identify what's trending:**
```
WebSearch("[platform] 工具 排名 2025")
```
Website example: `WebSearch("独立开发者 在线工具 排名 2025 indie hacker")`
Mini Program example: `WebSearch("微信小程序 工具类 排行 增长 2025")`

**Step 2 — Find what people complain about:**
```
WebSearch("最好的 [category] 工具 替代品 吐槽")
WebSearch("site:v2ex.com [category] 工具 推荐")
```
Pick the top 2-3 categories mentioned and proceed to Step 3.

**Step 3 — Validate those categories have paying customers:**
```
WebSearch("[category] 在线工具 pricing subscription")
```
If you find 3+ tools with paid plans → demand is validated.

Compile a list of **5-8 candidate categories** from this chain. Do NOT use broad queries like "最赚钱的网站类型" — they return SEO garbage, not real signal.

### Phase 2: Demand Validation (per candidate)

For each candidate category, run this **query chain**:

```
Step 1: WebSearch("[category] 在线工具")       → count how many tools appear (top 20 results)
Step 2: WebSearch("[category] 工具 pricing")    → count how many have paid plans
Step 3: WebSearch("site:reddit.com [category] tool alternative")  → find user complaints
```

**Score Market Demand using these anchors:**

| Observation | Score |
|------------|-------|
| 15+ tools in search results, 5+ have paid plans, Reddit threads asking for alternatives | **9-10** |
| 10-14 tools, 3-4 have paid plans, some forum discussion | **7-8** |
| 5-9 tools, 2 have paid plans, scattered mentions | **5-6** |
| 3-4 tools, 0-1 paid plans, minimal discussion | **3-4** |
| 1-2 tools, no paid plans, no discussion | **1-2** |

**If professional data available, use these thresholds instead:**
- 5118 搜索指数 > 5000 → 9-10 / 1000-5000 → 7-8 / 500-1000 → 5-6 / < 500 → 1-4
- 微信指数 > 10000 → 9-10 / 3000-10000 → 7-8 / 1000-3000 → 5-6 / < 1000 → 1-4

### Phase 3: Competition Quality Check

For the top 3 candidates from Phase 2, evaluate the **top 5 search results**:

```
Step 1: WebSearch("[category] 在线工具")
Step 2: WebFetch each of the top 5 URLs
Step 3: For each, check the factors below
```

**Score each competitor's weakness using these anchors:**

| Factor | +2 points if | +1 point if | +0 if |
|--------|-------------|-------------|-------|
| **UI/UX** | Looks like 2015, broken on mobile | Functional but not polished | Modern, polished |
| **Features** | Missing obvious core features | Has basics but gaps in obvious areas | Feature-complete |
| **Mobile** | Desktop-only or broken on mobile | Works but not optimized | Mobile-first design |
| **Reviews** | Rating < 3.5 or many 1-star complaints about core features | Rating 3.5-4.0, some complaints | Rating > 4.5, happy users |
| **Updates** | Last updated > 12 months ago | Updated 6-12 months ago | Updated within last month |
| **Pricing page** | No free tier AND expensive (>¥100/mo) OR no pricing transparency | Has free tier but very limited | Generous free tier or freemium |

**Weakness Index = average of top 5 competitors' total scores.**

| Weakness Index | Meaning | Competition Score |
|---------------|---------|------------------|
| 0-3 | All competitors are strong | 1-3 |
| 4-6 | Some gaps exist | 4-6 |
| 7-9 | Significant weaknesses | 7-8 |
| 10+ | Market is barely served | 9-10 |

### Phase 4: Full Opportunity Scoring

For each candidate that passed Phase 2 (Demand ≥ 5), score 5 dimensions:

**Market Demand (30%)** — Use Phase 2 score directly.

**Competition Weakness (25%)** — Use Phase 3 score directly.

**Monetization Potential (20%):**

| Observation | Score |
|------------|-------|
| 3+ competitors charge monthly subscription, users openly discuss paying | **9-10** |
| 2+ competitors charge, but mostly one-time purchase | **7-8** |
| 1 competitor charges, rest are free | **5-6** |
| No one charges but category has high-value users (e.g., business owners) | **3-4** |
| Everything is free and users expect free | **1-2** |

**Technical Feasibility (15%):**

| Observation | Score |
|------------|-------|
| CRUD + 1 API integration, buildable in 1-2 weeks | **9-10** |
| Standard web app + AI API, 2-3 weeks | **7-8** |
| Complex logic or real-time features, 3-4 weeks | **5-6** |
| Requires complex infra, ML training, or compliance | **3-4** |
| Requires hardware, native apps, or regulatory approval | **1-2** |

**Personal Fit (10%):**

| Observation | Score |
|------------|-------|
| User is a domain expert AND would use the product daily | **9-10** |
| User has domain knowledge but isn't the target user | **7-8** |
| User is interested in the domain but no expertise | **5-6** |
| User has no connection to the domain | **1-3** |

**Opportunity Score = Demand×0.30 + Weakness×0.25 + Monetization×0.20 + Feasibility×0.15 + Fit×0.10**

### Phase 5: Output

See [examples/opportunity-report.md](../../examples/opportunity-report.md) for a complete example output.

Format your output following that template exactly.

## Decision Rules

| Signal | Action |
|--------|--------|
| Score ≥ 7.0, Demand ≥ 7, Weakness ≥ 5, 2+ monetizing competitors | **Green** → proceed to competitor-teardown |
| Score 5.0-6.9 | **Yellow** → suggest deeper competitor analysis before committing |
| Score < 5.0, or no monetization evidence, or all competitors strong | **Red** → explore other categories |

## Related Skills

- `competitor-teardown` — Deep dive into specific competitors for the top opportunity
- `product-scoper` — Define MVP scope after confirming the opportunity
- `build-planner` — Generate development roadmap for the scoped product
