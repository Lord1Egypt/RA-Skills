---
name: mentions-discover
version: 1.0.0
description: Discover the queries worth tracking for a brand's AI visibility — informational, commercial, and comparison-intent prompts — via MentionsAPI.com. One tool, minimum surface area.
license: MIT-0
author: MentionsAPI
homepage: https://mentionsapi.com
repository: https://github.com/nikhonit/llm-mentions-skills
tags:
  - mentionsapi
  - geo
  - ai-visibility
  - keyword-research
  - brand-monitoring
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

# mentions-discover

Focused query-discovery skill. Use only when the user **explicitly asks** what prompts or questions they should be tracking for a brand's AI visibility — the starting query set for a GEO/monitoring program.

## When to use this skill

**DO use when the user asks:**

- "What queries should I track for Linear?"
- "Which prompts should I monitor to measure my AI visibility?"
- "Give me the commercial-intent questions buyers ask in the project-management space"
- "What comparison queries mention my competitors?"

**Do NOT use when:**

- The user already has a specific query and wants to check it — use [`mentions-check`](https://github.com/nikhonit/llm-mentions-skills/tree/main/skills/mentions-check) instead
- A brand is mentioned in passing without a request to build a tracking set
- The user has not signaled they want query suggestions

This call costs $0.50. Confirm the brand (and industry, if known) before calling.

## Tools

### `discover_queries` — $0.50 per call

Return a ranked set of candidate queries to track for a brand, spanning informational, commercial, and comparison intents.

Arguments:

- `brand` *(required)* — the brand to generate tracking queries for, e.g. `"Linear"`
- `industry` — optional context to sharpen suggestions, e.g. `"project management software"`
- `count` — how many queries to return, 1–100 (default 50)

Example response:

```json
{
  "brand": "Linear",
  "candidates": [
    { "query": "best project management tool for engineers", "intent": "commercial" },
    { "query": "Linear vs Jira",                              "intent": "comparison" },
    { "query": "what is Linear used for",                     "intent": "informational" }
  ],
  "cost_cents": 50,
  "balance_after_cents": 50
}
```

Feed the returned `query` strings into `mentions-check` (or `mentions-full`'s `check_mentions`) to measure visibility, or into `watch` to monitor them over time.

## Authentication

Set `MENTIONSAPI_KEY` to your MentionsAPI key (format `lvk_live_...`). Free key with $1 credit at <https://mentionsapi.com/signup> — no card.

## Pricing

**Pay-as-you-go. No subscriptions, no monthly tiers, credits never expire.** $1 free signup credit, $5 minimum top-up. `discover_queries` is $0.50 per call regardless of `count`. Failed calls are not billed.

## Errors

Every call returns a Python dict. On success it's the API response; on failure it has an `error` key (`auth_required`, `auth_invalid`, `insufficient_balance`, `rate_limit_exceeded`, `network`). See the [full skill](https://github.com/nikhonit/llm-mentions-skills/tree/main/skills/mentions-full) for the complete error contract.

## API reference

- Endpoint reference: <https://mentionsapi.com/docs/api/check>
- OpenAPI spec: <https://mentionsapi.com/openapi.json>
- Hosted MCP server (alternative to this skill): `npx @mentionsapi/mcp`

## Independence and trademarks

MentionsAPI is an independent service and is not affiliated with, endorsed by, or sponsored by OpenAI, Anthropic, Google, Microsoft, or Perplexity. All product names are the property of their respective owners.
