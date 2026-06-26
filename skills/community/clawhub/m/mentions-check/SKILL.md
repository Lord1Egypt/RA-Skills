---
name: mentions-check
version: 1.0.0
description: Check whether a brand is mentioned, ranked, and cited across AI search surfaces (ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews/AI Mode, Bing Copilot) via MentionsAPI.com. One tool, minimum surface area.
license: MIT-0
author: MentionsAPI
homepage: https://mentionsapi.com
repository: https://github.com/nikhonit/llm-mentions-skills
tags:
  - mentionsapi
  - geo
  - ai-visibility
  - brand-monitoring
  - chatgpt
  - perplexity
  - api
  - mcp
metadata:
  openclaw:
    primaryEnv: MENTIONSAPI_KEY
    homepage: https://mentionsapi.com
    requires:
      env:
        - MENTIONSAPI_KEY
---

# mentions-check

Focused AI brand-visibility skill. Use only when the user **explicitly asks** whether a brand shows up in AI answers — its mention, rank, or citations for a specific question — not when a brand name merely appears in passing.

## When to use this skill

**DO use when the user asks:**

- "Is HubSpot mentioned when people ask ChatGPT about CRMs?"
- "Does Perplexity cite Stripe for 'best payment API'?"
- "What rank does Notion get in AI answers for 'best note-taking app'?"
- "Show up in Google AI Overviews for 'project management software'?"
- "Which brands does ChatGPT name first for 'top observability tools'?"

**Do NOT use when:**

- A brand or query appears incidentally in context
- The user is discussing GEO/AI search abstractly without a specific brand + query to measure
- The user has not signaled they want a visibility check

Each call costs credits (from $0.02). When the intent is ambiguous, confirm the brand and query with the user before calling.

## Tools

### `check_mentions` — from $0.02 per call

Ask one question against one or more AI surfaces and see whether `brand` is mentioned, where it ranks, and what got cited.

Arguments:

- `query` *(required)* — the natural-language question to test, e.g. `"best CRM for startups"`
- `brand` *(required)* — the brand name to look for, e.g. `"HubSpot"`
- `mode` — which surface(s) to hit (default `quick`):
  - `quick` ($0.02) — all 4 LLM APIs in parallel (ChatGPT, Claude, Gemini, Perplexity)
  - `ai_overview` ($0.05) · `bing_copilot` ($0.05)
  - `chatgpt_live` ($0.10) · `gemini_live` ($0.10) · `ai_mode` ($0.10)
  - `perplexity_live` ($0.25) — live Perplexity UI scrape with citations + fan-out
  - `all_live` ($0.50) — all 6 live UI surfaces in one call
- `providers` — subset of `["chatgpt","claude","gemini","perplexity"]` (only applies to `mode:quick`)
- `runs` — integer 1–7, repeat the query N times to measure volatility (multiplies cost)
- `region` — locale hint, e.g. `"us"`, `"gb"`

Example response (`mode:quick`):

```json
{
  "id": "chk_...",
  "mode": "quick",
  "query": "best CRM for startups",
  "brand": "HubSpot",
  "providers": {
    "chatgpt":    { "mentioned": true,  "rank": 1,    "context": "...", "citations": [{ "url": "https://...", "title": "..." }], "fan_out": [] },
    "claude":     { "mentioned": true,  "rank": 2,    "context": "...", "citations": [], "fan_out": [] },
    "gemini":     { "mentioned": false, "rank": null, "context": "",    "citations": [], "fan_out": [] },
    "perplexity": { "mentioned": true,  "rank": 3,    "context": "...", "citations": [{ "url": "https://...", "title": "..." }], "fan_out": [] }
  },
  "cost_cents": 2,
  "balance_after_cents": 98,
  "cache_hit": false
}
```

## Authentication

Set `MENTIONSAPI_KEY` to your MentionsAPI key (format `lvk_live_...`). Free key with $1 credit at <https://mentionsapi.com/signup> — no card.

## Pricing

**Pay-as-you-go. No subscriptions, no monthly tiers, credits never expire.** $1 free signup credit, $5 minimum top-up. Per-call cost is set by `mode` (see the table above). Failed calls are not billed.

## Errors

Every call returns a Python dict. On success it's the API response; on failure it has an `error` key:

- `{"error": "auth_required", ...}` — `MENTIONSAPI_KEY` not set (includes signup URL)
- `{"error": "auth_invalid", ...}` — key rejected; rotate at <https://mentionsapi.com/app/keys>
- `{"error": "insufficient_balance", ...}` — wallet empty; top up at <https://mentionsapi.com/app/billing>
- `{"error": "rate_limit_exceeded", ...}` — back off and retry
- `{"error": "mode_roadmap", ...}` — `deep`/`change_track` are on the roadmap; use a shippable mode

## API reference

- Endpoint reference: <https://mentionsapi.com/docs/api/check>
- OpenAPI spec: <https://mentionsapi.com/openapi.json>
- Hosted MCP server (alternative to this skill): `npx @mentionsapi/mcp`

## Independence and trademarks

MentionsAPI is an independent service and is not affiliated with, endorsed by, or sponsored by OpenAI, Anthropic, Google, Microsoft, or Perplexity. All product names are the property of their respective owners.
