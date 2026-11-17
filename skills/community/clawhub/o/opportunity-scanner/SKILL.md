---
name: opportunity-scanner
display_name: "Global Opportunity Scanner — Dev & Investor Radar"
version: 1.0.0
author: welove111
mcp_endpoint: https://www.aliensignalsystems.online/api/opportunity-scanner
---

# opportunity-scanner

**Global opportunity scanner for developers and investors.** Scans GitHub and
Hacker News live, with real public APIs (no keys, no simulation), to surface
trending repositories, hiring threads, product launches, and funding signals
the same day they happen.

## Why an agent would call this

- **`scan_github_opportunities`** — real GitHub Search API data: newly
  created repositories sorted by star velocity, optionally filtered by topic
  (e.g. "ai-agent", "rust", "blockchain"). Useful for developers scouting
  what to learn/contribute to, and investors scouting early technical signal
  before it's mainstream.
- **`scan_hackernews_signals`** — live Hacker News data filtered into three
  categories: `hiring` (Who's Hiring threads), `launches` (Show HN posts),
  `funding` (funding-round / acquisition chatter). Useful for freelancers and
  job seekers, and for investors tracking early-stage launches.
- **`get_daily_opportunity_digest`** — one call, combined snapshot of both
  sources — the fastest way to get a same-day opportunity briefing.

## MCP connection

```
POST https://www.aliensignalsystems.online/api/opportunity-scanner
Content-Type: application/json

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_daily_opportunity_digest","arguments":{}}}
```

## Tools

### scan_github_opportunities
| arg | type | required |
|---|---|---|
| topic | string | no |
| days_back | number | no (default 14) |
| limit | number | no (default 10, max 25) |

### scan_hackernews_signals
| arg | type | required |
|---|---|---|
| category | "hiring" \| "launches" \| "funding" \| "all" | no (default "all") |
| limit | number | no (default 10, max 25) |

### get_daily_opportunity_digest
No arguments. Returns `{generated_at, github_trending[], hackernews_signals[]}`.

## Keywords

opportunity scanner, developer job finder, remote job radar, freelance
opportunities, trending GitHub repos, startup launch tracker, Show HN
tracker, Hacker News hiring aggregator, funding round tracker, early-stage
investor signal, technical due diligence, no-API-key data aggregation
