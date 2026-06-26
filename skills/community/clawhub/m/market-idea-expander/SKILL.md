---
name: business-idea-generator
description: >
  A complete end-to-end business idea generation system that takes a market segment and produces:
  (1) a structured niche breakdown across Health, Wealth, and Relationships markets,
  (2) Reddit/social media research queries to uncover real pain points,
  (3) market gap analysis with multi-framework solution generation,
  and (4) a ready-to-use landing page prompt built with BAB copywriting.
  Use this skill whenever the user wants to generate business ideas, explore market niches,
  find product opportunities, validate pain points, brainstorm SaaS/digital product ideas,
  or create landing page copy for a new business. Also trigger when the user mentions
  "market research", "niche ideas", "business opportunity", "product idea", "side hustle",
  "startup idea", "pain points", or asks "what business should I build".
---

# Business Idea Generator Skill

A structured, repeatable system to go from **zero → validated business idea → landing page** in one session.

## Workflow Overview

Run these **4 phases in sequence**, or jump to the phase the user needs. Always confirm with the user which phase they need before skipping ahead.

| Phase | Name | Output |
|-------|------|--------|
| 1 | Market Niche Explorer | Hierarchical niche breakdown |
| 2 | Pain Point Research Queries | Copy-paste social media search strings |
| 3 | Market Gap & Solution Generator | 5-framework solution concepts |
| 4 | Landing Page Generator | Full BAB-structured landing page (HTML artifact) |

---

## Phase 1 — Market Niche Explorer

**Trigger:** User wants to explore a market, says "give me random ideas", or names a specific niche.

Output a hierarchical breakdown following this structure. Go as deep as possible:

```
- [Core Market: Health / Wealth / Relationships]
  - [Category]
    - [Subcategory]
      - [Niche]
        - [Sub-Niche]
```

**Rules:**
- If user says "random" → cover all 3 core markets (Health, Wealth, Relationships)
- If user names a specific area (e.g. "alternative medicine") → start from that node, don't include other core markets
- Each level must be unique — no overlap between sibling nodes
- Generate as many entries as possible; depth over breadth

**Example output snippet:**
```
- Wealth
  - Online Business
    - Digital Products
      - Info Products
        - Notion Templates for Solopreneurs
        - AI Prompt Packs for Content Creators
        - Pine Script Strategy Templates for Traders
```

After outputting the niche map, ask:
> "Which sub-niche would you like to dig deeper into? Or shall we move straight to Phase 2 (Pain Point Research)?"

---

## Phase 2 — Pain Point Research Queries

**Trigger:** User has chosen a niche and wants to find real customer pain points.

Generate platform-specific search queries for Reddit, X (Twitter), Threads, LinkedIn, and Google validation searches.

For the full query templates and platform-specific tips, read [PAIN_POINT_QUERIES.md](PAIN_POINT_QUERIES.md).

If the user has access to web search or browser automation tools, these queries can be run directly to collect real results. Otherwise, provide the queries for the user to run manually.

After outputting queries, ask:
> "Do you already have pain points from your research? Paste them here and let's move to Phase 3 — Market Gap Analysis."

---

## Phase 3 — Market Gap & Solution Generator

**Trigger:** User provides pain points they've collected (from research or intuition).

### Input Expected
User pastes 3–10 pain points from their research.

### Your Output

First, write a short **Executive Summary** (3–4 sentences) summarizing the core market opportunity.

Then apply all **5 frameworks** below, generating 2–3 solution concepts per framework:

1. **Market Segmentation** — Find underserved sub-niches. Who's being ignored?
2. **Product Differentiation** — Premium vs. simplified versions. What would the "luxury" or "no-BS minimal" version look like?
3. **Business Model Innovation** — Same product, different monetization (subscription, freemium, done-for-you, community).
4. **Distribution & Marketing** — Underutilized channels, partnerships, content strategy.
5. **New Paradigm** — What if you applied AI, new tech, new regulations, or an emerging trend to this problem?

For each concept include:
- **Name** (descriptive, memorable)
- **2-3 sentence explanation**
- **Key features**
- **Target audience** (specific, not generic)
- **Business model** (subscription / one-time / marketplace / SaaS / service)
- **Primary differentiator** — why it's "best in its category"
- **Challenges to overcome**
- **Pain points addressed**

### Opportunity Assessment (conclude with this)

Rank the **Top 3 solutions** across all frameworks by:
1. Market size & growth potential
2. Competitive advantage sustainability
3. Implementation feasibility
4. "Best in the world" potential

After outputting, ask:
> "Want to move to Phase 4? Pick one of the solutions above and I'll build the landing page for it right away."

---

## Phase 4 — Landing Page Generator

**Trigger:** User picks a solution concept and wants a landing page.

### Input Expected
- Which solution concept they chose
- Product name (if they have one)
- Any additional context (target country, price point, CTA goal)

### Your Output

Build a **complete, single-file HTML landing page** as an artifact using the BAB (Before-After-Bridge) framework. Generate the actual HTML/CSS/JS directly — do not delegate to external page builders.

For the full landing page structure, copywriting rules, tone-by-niche table, and design-copy alignment guide, read [LANDING_PAGE_GUIDE.md](LANDING_PAGE_GUIDE.md).

---

## General Rules

1. **Always ask before skipping phases** — confirm which phase the user needs
2. **Use the user's language** — if they write in Indonesian, respond in Indonesian
3. **Be specific, not vague** — "Indonesian solopreneurs aged 25–35 who sell digital products on Tokopedia" > "small business owners"
4. **Default to action** — end every phase with a clear next step prompt
5. **Never generate generic ideas** — every concept must have a specific differentiator that makes it "best in its category"
