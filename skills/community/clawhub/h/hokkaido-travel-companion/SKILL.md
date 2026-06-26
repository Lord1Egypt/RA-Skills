---
name: hokkaido-travel-companion
description: "Hokkaido/Sapporo/Otaru/Yoichi travel companion protocol. Specifies how to collect, verify, store, and reuse travel knowledge with a local vault plus live search. Covers restaurants, transport, weather, budgets, and GO/NOGO guidance. NOT for non-Hokkaido trips."
---

# Hokkaido Travel Companion

A Hokkaido-specific travel companion protocol for Sapporo, Otaru, Yoichi, and Chitose Airport.

This skill is **not** a hardcoded itinerary or recommendation list. It defines how an agent should:

1. collect travel facts and user preferences,
2. verify stale or high-risk information with live sources,
3. store reusable knowledge in a local vault, and
4. guide decisions with route, budget, weather, and GO/NOGO context.

Bayesian framing: local vault = prior, live search = likelihood, updated travel note = posterior.

## Core Loop

1. **Read vault** → check prior knowledge for the query
2. **Search** → fill gaps or verify stale info (>3 months old)
3. **Update vault** → write posterior back
4. **Reply** → synthesized answer with sources

## Search Protocol (Verified)

### Tool Mapping
| Need | Tool | Verified? |
|------|------|-----------|
| Restaurant rating/hours | `web_search` → Tabelog, sapporo.travel | ✅ Yes |
| Restaurant location/route | `browser` → Google Maps | ✅ Yes |
| JR fares/schedules | `web_search` → japan-guide.com, JR Hokkaido | ✅ Yes |
| Weather | `web_search` → wttr.in (one-liner) | ✅ Yes |
| Budget tracking | `memory/travel-budget.json` (local) | ✅ Yes |

### Source Trust Hierarchy
1. **Official** — sapporo.travel, jrhokkaido.co.jp, restaurant official site
2. **Aggregator** — Tabelog (rating ≥3.5 filter), Google Maps
3. **Blog/review** — use only when 1+2 unavailable

### Verification Rules
- Hours: cross-check 2 sources before answering
- JR fares: use japan-guide.com or JR official (not blogs)
- Closed/permanently closed: always check before recommending
- Never guess walking times >10 min — verify via browser

### What NOT to do
- `web_fetch` on Google Maps → empty page (JS rendering)
- `web_fetch` on Tabelog → often blocked
- Use `browser` for Google Maps, `web_search` for everything else

## Vault Structure

Location: `references/vault/`

```
vault/
├── restaurants/
│   ├── restaurant-name.md
│   ├── ramen-shop.md
│   └── ...
├── transport/
│   ├── jr-sapporo-otaru.md
│   ├── subway-lines.md
│   └── ...
├── areas/
│   ├── sapporo-area.md
│   ├── otaru-area.md
│   └── yoichi-area.md
└── experiences/
    ├── day1-YYYY-MM-DD.md
    └── day2-YYYY-MM-DD.md
```

### Vault Node Format
```markdown
# {가게/장소명}
- type: restaurant | transport | area | experience
- visited: YYYY-MM-DD (if personal experience)
- rating: ⭐N (if visited)
- tabelog: X.XX (if known)
- hours: (verified source, date)
- address: JP address
- nearest_stn: 駅名 (Line, walk N min)
- budget: ¥range
- notes: (personal tips)
- source: where info came from
- last_updated: YYYY-MM-DD
```

### Update Rules
- **Auto-update**: any field >3 months old → re-search before answering
- **On visit**: prompt user for rating/notes → update vault
- **New discovery**: search result with Tabelog ≥3.5 → create new node
- **Closed/changed**: update node, mark status

## Budget System

### State File
`memory/travel-budget.json`:
```json
{
  "dailyLimit": 20000,
  "days": {
    "YYYY-MM-DD": {
      "spent": 0,
      "items": [{"time": "HH:MM", "name": "...", "amount": 0, "category": "food|transport|drink|activity|shop"}]
    }
  }
}
```

### GO/NOGO
When user asks about a place:
1. Check remaining daily budget
2. Estimate cost (vault → search)
3. 🟢 GO / 🔴 NOGO + balance + estimated cost
4. After 22:00: round up estimates by 20%

## Transport Output Format (Mandatory)

Every route must include:
- Station: **JP** (漢字) / **KR** (한국어) / **EN** (English)
- Line: JP + EN
- Stops count, duration, fare (IC card)
- Last train time (if evening query)

## Weather

One call: `web_search` with "wttr.in Sapporo?format=3" or "Sapporo weather today"
Include in daily plan replies.

## Emergency
- **Missed last train**: search nearby capsule hotel / taxi estimate
- **Budget blown**: suggest konbini / free activities
- **Closed venue**: search alternative within walking distance via browser

## Setup (First Use)

Ask for:
1. Daily budget (¥)
2. IC card type
3. Hotel nearest station
4. Trip dates

Save to `memory/travel-budget.json`.

## Scope

- **In scope**: Sapporo, Otaru, Yoichi, Chitose Airport
- **Out of scope**: Non-Hokkaido (do not activate)
