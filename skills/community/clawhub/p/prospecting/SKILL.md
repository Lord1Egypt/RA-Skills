---
name: prospecting
description: >
  B2B manufacturing proactive prospecting. Search Google Maps for potential customers based on
  existing client profiles, enrich leads with business details, score and rank them, and output
  actionable CSV + JSON lead lists with custom sales openers.
  Includes chain store strategy: local call → identify procurement decision chain → escalate to corporate.
  Use when: finding new customers, prospecting, lead generation, searching for potential clients,
  building a call list, or when user mentions existing customers they want to find more like.
  Triggers: prospect, find customers, lead gen, call list, 获客, 找客户, 搜客户, 潜在客户, 主动获客
---

# Prospecting — B2B Lead Generation from Existing Customers

## Overview

Turn existing customers into a search template → find similar businesses on Google Maps → enrich → score → output actionable call lists.

**One line**: Known customer → profile → Maps search → enrich & rank → CSV call list + JSON index

## When to Use

- User gives a customer name + location and asks to find similar businesses
- User asks to build a prospect/call list
- User wants to find new clients in a specific industry (auto body, manufacturing, HVAC, etc.)

## Input Required

| Field | Required | Notes |
|-------|----------|-------|
| Company name | ✅ | Core search term |
| Location (city/state) | ✅ | Search center point |
| Product purchased | ❌ | Helps with profiling |

Even minimal input ("Bob's Auto Body, Orange CA") can start the full flow.

## Execution Flow

### Step 1: Profile the Existing Customer (8-step fixed process)

Read [references/profiling.md](references/profiling.md) for the full 8-step process. Key actions:

1. **Google Maps deep dive** — Use agent-browser to search `[company name] [location]`, extract: address, phone, rating, review count, business type, hours, website, photos, chain status
2. **Review sampling** — Sample reviews with keyword filtering (not all reviews). Generic keywords: `new, expand, equipment, upgrade, install, moved, bigger` + industry-specific keywords (e.g., for auto body: `paint booth, insurance, fleet, dealer`)
3. **Social/web enrichment** — Only for 🔴 chain (FB+LinkedIn+website) or 🟡 mid-tier (FB+website). Skip 🟢 small (no website)
4. **Output a Profile Card** — Standard format saved to `prospect-data/{batch}/profile-{name}.json`

**Tier detection** (determines enrichment depth):
- 🔴 Chain/large: name contains chain markers OR >200 reviews
- 🟡 Mid-tier: has website, 50-200 reviews
- 🟢 Small: no website, <50 reviews

### Step 2: Maps Batch Search (agent-browser automated)

**Read [references/search-strategy.md](references/search-strategy.md) for the complete search framework.**

Key principles:
- **Multi-center**: Large cities (>2M) use 4-6 search centers (e.g., Houston: Downtown, Katy, Sugar Land, The Woodlands, Baytown, Cypress)
- **Keyword matrix**: 4-6 keywords per center (core + service + equipment + brand + scene)
- **Pagination**: Scroll and load 3 times per search to get 20-30 results
- **Deduplication**: Cross-center, cross-keyword deduplication

**Search execution**:
1. For each center point × each keyword: open Google Maps, extract listings, paginate 3x
2. Collect: name, phone, address, rating, review count, business type, website status, chain markers
3. Dedup: same name + same address = duplicate
4. Remove: permanently closed, non-target industry

**Save to**: `prospect-data/{batch}/candidates-raw.txt` (raw extraction log) + `candidates.json` (deduplicated)

### Step 3: Auto-Tier Candidates

Based on Maps data, assign tiers. **Chain stores are NOT excluded** — they are valid prospects with a different approach strategy.

| Tier | Criteria | Next action |
|------|----------|-------------|
| 🔴 Chain/large | Chain name OR >200 reviews | Deep enrichment + **chain procurement strategy** |
| 🟡 Mid-tier | Has website, 50-200 reviews | Medium enrichment |
| 🟢 Small | No website, <50 reviews | Skip enrichment |

**Chain store prospecting strategy** — Read [references/chain-strategy.md](references/chain-strategy.md) for the full three-call approach:

- **Call 1**: Local store — NOT to sell, but to identify procurement decision chain
- **Call 2**: Regional/corporate — pitch to the person who can approve multi-location deals
- **Call 3**: Follow-up with proposal

Key principles:
- Chain stores have large, stable equipment needs — one deal can cover multiple locations
- Local store manager is the entry point, not the decision-maker (usually)
- Key question: "Is equipment purchasing handled locally, or should I speak with your regional/corporate procurement team?"

### Step 4: Enrich by Tier

| Tier | Action | Tools | Time |
|------|--------|-------|------|
| 🔴 Chain | Website deep + LinkedIn + news search + **chain procurement mapping** | agent-browser + agent-reach (Exa) | 3-5min each |
| 🟡 Mid | Website basics + FB | agent-browser | 1-2min each |
| 🟢 Small | **Skip** — Maps data sufficient | — | 0 |

**Chain enrichment** with agent-browser:
1. `agent-browser open "[website URL]"`
2. `agent-browser snapshot -i` → extract Services, About, Staff, Contact
3. Check for Portfolio/Cases and News/Blog pages for expansion signals
4. **For chains**: Look for corporate/region procurement contacts, preferred vendor programs, and expansion news

**Chain news search** with agent-reach:
```
mcporter call 'exa.web_search_exa(query: "[company name] expansion OR new location OR equipment", numResults: 5)'
```

**Chain procurement mapping** (chains only) — See [references/chain-strategy.md](references/chain-strategy.md) for full approach:
- Identify: local manager → regional operations manager → VP of operations / procurement director
- Sources: LinkedIn, corporate website "careers" or "partners" page, news about leadership changes
- Goal: find the person who can approve equipment purchases for multiple locations

### Step 5: Score & Rank

Match each candidate against the profile card:

| Factor | Rule | Points |
|--------|------|--------|
| Buy signal | Expansion / new service / new equipment | +5 (strong) / +3 (medium) / +1 (weak) |
| Industry match | Business type matches profile | +3 |
| Scale match | Review count / bays similar to profile | +2 |
| Service overlap | Same services as profile | +2 |
| Geo similarity | Similar area type | +1 |
| Business age | Similar years in operation | +1 |
| Chain multiplier | Chain store (multiple locations = bulk potential) | +3 |
| EV/high-end certification | EV Certified / LUXE / premium line | +4 |

**Tie-breaking**: buy signal strength → chain (bulk potential) → has phone → closer scale match

| Total score | Priority | Action |
|-------------|----------|--------|
| 10+ | 🔴 High | Call within 48h |
| 6-9 | 🟡 Medium | Call this week |
| <5 | 🟢 Low | Call when available |

### Step 6: Generate Custom Sales Openers

**Not templates — custom for each prospect based on their data.**

Opener must accomplish 3 things: (1) prove you know them, (2) state your purpose, (3) invite dialogue.

| Data source | How to use in opener |
|-------------|---------------------|
| Buy signal | "Saw you just added [service related to your product]" |
| Similar customer | "We supplied [product] to [similar customer] in your area" |
| Business type | "Since you do [their business type]..." |
| Key clues | "As an [industry certification] shop..." / "Working with [their key client]..." |
| Tier | High→emphasize quality & custom, Mid→value, Low→entry-level |
| **Chain store** | **Key opener question: "Is equipment purchasing handled locally, or should I speak with your regional/corporate procurement team?"** |
| **Premium/certified line** | **Reference their specialization: "As an EV-certified shop, you need [specific configuration] — we've done those."** |

### Step 7: Output (3-layer structure)

Save to `prospect-data/{batch}/`:

```
prospect-data/{area}-{date}/
├── index.json          ← Lightweight index, instant search
├── P001.json           ← Full detail for first prospect
├── P002.json           ← Full detail for next prospect
└── call-list.csv       ← 11-column CSV for calling
```

See [examples/](examples/) for sample output files.

Then export CSV from index + P###.json files for calling.

**index.json** — Search/filter only (few KB):
```json
{
  "batch_id": "orange-ca-2026-05-19",
  "source_customer": "ABC Auto Body",
  "generated": "2026-05-19",
  "search_areas": ["Orange CA"],
  "product": "Customizable per industry",
  "chain_strategy": "Chain stores included — call local first to identify procurement decision chain, then escalate to regional/corporate",
  "prospects": {
    "P001": {
      "name": "Bob's Auto Body",
      "city": "Orange CA",
      "priority": "高",
      "tier": "中高端-独立",
      "status": "待联系",
      "tags": ["[industry]", "[business type]"],
      "file": "P001.json"
    },
    "P013": {
      "name": "Crash Champions Orange",
      "city": "Orange CA",
      "priority": "高",
      "tier": "连锁-中高端",
      "status": "待联系",
      "tags": ["collision", "chain", "Crash Champions"],
      "file": "P013.json"
    }
  }
}
```

**P001.json** — Full detail (all collected data + contact log):
```json
{
  "id": "P001",
  "name": "Bob's Auto Body",
  "phone": "(714)555-1234",
  "city": "Orange CA",
  "tier": "Mid-high-Independent",
  "priority": "High",
  "buy_signal": "Added new [service]",
  "similar_customer": "Customer A",
  "business_type": "[industry service type]",
  "key_clues": "[specific observations from data]",
  "email": "bob@bobscorp.com",
  "chain_brand": null,
  "opener": "We supplied [product] to [similar customer] in your area — saw you recently added [service]. What [product type] are you currently using?",
  "status": "Pending",
  "contact_log": [],
  "tags": ["[industry]", "[business type]", "[certification]"],
  "maps_url": "https://maps.google.com/...",
  "rating": 4.5,
  "reviews_count": 87,
  "has_website": true,
  "website_url": "https://bobscorp.com",
  "raw_notes": "Reviews mention...",
  "source_customer": "Customer A"
}
```

**P013.json** — Chain store example:
```json
{
  "id": "P013",
  "name": "[Chain Brand] [City]",
  "phone": "(714)555-5678",
  "city": "Orange CA",
  "tier": "Chain-Mid-high",
  "priority": "High",
  "buy_signal": "National chain with stable equipment needs across locations",
  "similar_customer": "Customer A",
  "business_type": "[Industry] Chain",
  "key_clues": "[Chain brand] national chain + [city] location + online booking",
  "email": "",
  "chain_brand": "[Chain Brand]",
  "opener": "Hi, I'm with [company] — we manufacture [product]. [Chain brand] has a location here, and I'd like to learn about your equipment purchasing process. Is that handled locally, or should I speak with your regional/corporate procurement team?",
  "status": "Pending",
  "contact_log": [],
  "tags": ["[industry]", "chain", "[chain brand]", "online booking"],
  "maps_url": "https://maps.google.com/...",
  "rating": 4.6,
  "reviews_count": 120,
  "has_website": true,
  "website_url": "https://www.chainbrand.com",
  "raw_notes": "National chain. Key question: local manager vs regional purchasing.",
  "source_customer": "Customer A"
}
```

**CSV export** — 11 columns, ready to call:
```
优先级,店名,电话,城市,档位,购买信号,相似客户,业务类型,关键线索,邮箱,开场白
```

CSV columns map 1:1 to P###.json fields (priority→tier, etc.). CSV is a projection of the JSON, not a separate data source.

**Status tracking** (in P###.json, not CSV):
```
待联系 → 已联系 → 意向 / 无意向 / 回访中
                 ↘ 无人接听 → 再试
```

### Step 8: Update contact status

When user reports call results, update P###.json:
```json
"contact_log": [
  {"date": "2026-05-20", "action": "电话", "result": "无人接听", "next": "明后天再试"}
]
```
And update index.json status field accordingly.

Re-export CSV filtered by status when user needs a new call list.

## Critical Rules

1. **Every step must execute** — skip only if data source has nothing (no website = skip website enrichment)
2. **Review sampling, not all** — use tiered sampling + keyword filtering per profiling reference
3. **Social media by tier only** — 🔴 chain gets full search, 🟢 small gets nothing
4. **Opener is custom** — never use generic templates, always tailor to prospect's specific data
5. **Output is 3-layer** — index.json for search, P###.json for detail, CSV for calling
6. **CSV is a projection** — all data lives in JSON; CSV is just 11 columns exported on demand
7. **Chain stores ARE valid prospects** — do NOT exclude them. Include with a different strategy: local call first → identify procurement decision chain → escalate to regional/corporate buyer. One chain deal can equal many independent deals.
8. **Tier labels include chain distinction** — use "独立" (independent) or "连锁" (chain) suffix in tier: e.g., "中高端-独立", "连锁-中高端"
9. **Chain opener must ask about procurement** — "Is equipment purchasing handled locally, or should I speak with your regional/corporate procurement team?"
10. **Specialized/certified prospects are high priority** — certifications (EV, ISO, specific industry standards) indicate higher equipment requirements and justify premium positioning
11. **DATA INTEGRITY — NO FABRICATION** — All data in outputs MUST come from actual agent-browser searches, web_fetch calls, or other real data sources. **NEVER invent, infer, or hallucinate business details.** If a field cannot be verified from real data, mark it as `"unknown"`, `"not found"`, or `"pending verification"`. If a search returns no results or fails due to network issues, report this honestly to the user instead of generating placeholder data.
12. **TRANSPARENCY ON DATA GAPS** — If Google Maps returns restricted view (limited details), if agent-browser fails to load, or if a business has no visible phone/address/rating, document this in `raw_notes` and adjust the priority accordingly. Do not fill gaps with assumptions.
13. **VERIFICATION REQUIRED** — Before marking any prospect as "ready to call", confirm that the phone number was actually extracted from a live page (not a template). If the number is a placeholder or unverified, flag it explicitly: `"phone_status": "unverified_placeholder"`.