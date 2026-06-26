---
name: mentions-full
version: 1.0.0
description: Complete AI brand-visibility toolkit via MentionsAPI.com. Four tools — check mentions/ranks/citations across ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews/AI Mode, and Bing Copilot; discover queries to track; compare two brands or queries; and watch for changes over time.
license: MIT-0
author: MentionsAPI
homepage: https://mentionsapi.com
repository: https://github.com/nikhonit/llm-mentions-skills
tags:
  - mentionsapi
  - geo
  - generative-engine-optimization
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

# mentions-full

Complete AI brand-visibility toolkit via MentionsAPI.com. Use when the user **explicitly asks** whether a brand appears in AI answers, what to track, how it compares to a competitor, or to monitor it over time — across ChatGPT, Claude, Gemini, Perplexity, Google AI Overviews, Google AI Mode, and Bing Copilot.

## When to use this skill

Each tool call consumes MentionsAPI credits, so this skill activates only when the request is genuinely about measuring AI visibility — not when a brand name or query merely appears in passing.

**DO use when the user:**

- Asks whether a brand is mentioned/ranked/cited for a question → `check_mentions`
- Asks which queries to track for a brand's AI visibility → `discover_queries`
- Asks how a brand compares to a competitor in AI answers → `compare_mentions`
- Asks to be alerted when a brand's mentions, rank, or citations change → `watch_brand`

**Do NOT use when:**

- A brand or query appears incidentally (email signatures, unrelated docs, news)
- The user is discussing GEO/AI search abstractly without a specific brand + query
- The user has not signaled they want a visibility lookup

When intent is ambiguous, confirm the brand and query before calling — these tools cost credits.

## Tools

### `check_mentions` — from $0.02
Check whether `brand` is mentioned, where it ranks, and what got cited for `query`. Args: `query` (required), `brand` (required), `mode` (default `quick`), `providers` (mode:quick only), `runs` (1–7), `region`.

Modes: `quick` $0.02 (4 LLM APIs in parallel) · `ai_overview` $0.05 · `bing_copilot` $0.05 · `chatgpt_live` $0.10 · `gemini_live` $0.10 · `ai_mode` $0.10 · `perplexity_live` $0.25 (citations + fan-out) · `all_live` $0.50 (all 6 live surfaces).

Returns per-surface `{mentioned, rank, context, citations[], fan_out[]}` plus `cost_cents`, `balance_after_cents`, `cache_hit`.

### `discover_queries` — $0.50
Suggest ~50 queries worth tracking for `brand`, spanning informational, commercial, and comparison intents. Args: `brand` (required), `industry`, `count` (1–100, default 50).

### `compare_mentions` — $1.50
Compute the delta between two brands (same query) or two queries (same brand). Args: `query_a` (required), `brand_a` (required), `query_b`, `brand_b`, `mode` (`quick` | `perplexity_live`, default `quick`). Provide a second brand for competitor analysis, or a second query to compare phrasings.

### `watch_brand` — $1 per run
Create a persistent monitor that calls an HMAC-signed webhook when mentions, rank, or citations change. Args: `query` (required), `brand` (required), `webhook_url` (required), `webhook_secret` (required, ≥16 chars), `mode` (default `quick`), `interval` (`hourly` | `daily` | `weekly`, default `daily`), `trigger_on` (subset of `mention_added`, `mention_removed`, `rank_changed`, `citation_changed`). You must host the webhook endpoint; billing is per scheduled run.

**Security — read before using `watch_brand`:** the webhook receives your brand-visibility data (sensitive competitive intelligence). Use an **HTTPS** endpoint you control and never point it at a third party you don't trust. Every delivery is HMAC-signed with `webhook_secret` — **verify that signature on every request** and reject unsigned, altered, or replayed deliveries (check the timestamp/nonce). Treat `webhook_secret` like a password: ≥16 characters, stored securely, rotated if leaked.

## Authentication

Set `MENTIONSAPI_KEY` to your MentionsAPI key. Keys are `lvk_live_...` strings.

```bash
export MENTIONSAPI_KEY="lvk_live_..."
```

Get a free key with $1 credit at <https://mentionsapi.com/signup> — no card required.

## Pricing

**Pay-as-you-go. No subscriptions, no monthly tiers, credits never expire.**

- **$1 free signup credit** — no card required
- **$5 minimum top-up** — wallet balance, billed per call in real time
- Per-call cost: `check` from $0.02 (by mode) · `discover` $0.50 · `compare` $1.50 · `watch` $1/run

Failed calls are not billed.

## Errors

All functions return a Python dict. On success it's the API response; on failure it has an `error` key:

- `{"error": "auth_required", ...}` — `MENTIONSAPI_KEY` not set (includes `signup_url`)
- `{"error": "auth_invalid", ...}` — key rejected; rotate at `/app/keys`
- `{"error": "insufficient_balance", ...}` — wallet empty; includes `top_up_url`
- `{"error": "rate_limit_exceeded", ...}` — back off and retry
- `{"error": "mode_roadmap", ...}` — `deep`/`change_track` not yet shipped; use a shippable mode
- `{"error": "network" | "HTTP <code>" | "unexpected", ...}` — transport / other failures

## API reference

- Endpoint reference: <https://mentionsapi.com/docs/api/check>
- OpenAPI spec: <https://mentionsapi.com/openapi.json>
- Recipes: <https://mentionsapi.com/docs/recipes>
- Hosted MCP server (alternative to this skill): `npx @mentionsapi/mcp`

## Independence and trademarks

MentionsAPI is an independent service and is not affiliated with, endorsed by, or sponsored by OpenAI, Anthropic, Google, Microsoft, or Perplexity. "ChatGPT" is a trademark of OpenAI; "Claude" of Anthropic; "Gemini" and "AI Overviews" of Google; "Copilot" of Microsoft; "Perplexity" of Perplexity AI. All product names are the property of their respective owners.
