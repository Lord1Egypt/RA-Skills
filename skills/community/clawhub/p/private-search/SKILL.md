---
name: private-search
description: Route OpenClaw web searches through privacy-respecting engines (Brave Search, Kagi, SearXNG) instead of Google or Bing. Eliminates ad-network tracking from your AI agent's research. Configurable engine, result count, and tracking-param stripping.
homepage: https://clawhub.ai/skills/private-search
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["BRAVE_API_KEY"]},"primaryEnv":"BRAVE_API_KEY","optionalEnv":["KAGI_API_KEY","SEARXNG_URL"]}}
version: 1.0.0
---

# Private Search for OpenClaw

Route all web searches through privacy-respecting engines. No ads. No tracking. No query monetization.

## Why This Exists

OpenAI now shows ads to ChatGPT users and routes queries through ad-network-partnered search APIs. OpenClaw defaults to Google/Bing-backed search — both of which monetize your queries. This skill replaces that with:

- **Brave Search** — independent index, no ad tracking, free tier available
- **Kagi** — premium ad-free search, best result quality
- **SearXNG** — fully self-hosted, zero third-party dependency

## Quick Setup (Brave Search — Recommended)

1. Get a free Brave Search API key: https://api.search.brave.com/
2. Set env var: `BRAVE_API_KEY=your_key_here`
3. Done. All agent web searches now route through Brave.

## Configuration

Set any of these in your OpenClaw environment:

| Variable | Description | Default |
|----------|-------------|---------|
| `BRAVE_API_KEY` | Brave Search API key | Required for Brave |
| `KAGI_API_KEY` | Kagi API key | Optional |
| `SEARXNG_URL` | Self-hosted SearXNG URL | Optional |
| `PRIVATE_SEARCH_ENGINE` | `brave`, `kagi`, or `searxng` | `brave` |
| `PRIVATE_SEARCH_RESULTS` | Number of results to return | `5` |
| `PRIVATE_SEARCH_STRIP_TRACKING` | Strip UTM/tracking params from URLs | `true` |

## Usage

Once configured, use web search naturally. This skill overrides the default search behavior:

```
Search for the latest OpenAI news
Find me pricing for Hetzner VPS plans
What are the top AI tools this week?
```

All queries route through your chosen private engine.

## Engine Comparison

| Engine | Cost | Privacy | Index Quality | Best For |
|--------|------|---------|---------------|----------|
| Brave | Free tier (2,000/mo) / $3/mo for 20K | High | Good | Most users |
| Kagi | $10–$25/mo | Highest | Excellent | Power users |
| SearXNG | Self-hosted (free) | Maximum | Varies | Devs/privacy maximalists |

## How It Works

This skill provides a `private_web_search` tool that:

1. Accepts a query string and optional parameters
2. Routes to your configured engine via API
3. Strips tracking parameters from all result URLs (UTM, fbclid, gclid, etc.)
4. Returns clean, structured results
5. Never logs queries to third-party ad networks

## Scripts

Run the setup script for guided configuration:

```bash
bash scripts/setup-brave-search.sh
```

## References

See `references/privacy-engines.md` for full engine documentation, pricing tiers, and self-hosting instructions for SearXNG.

## Privacy Guarantee

This skill never sends your queries to Google, Bing, or any ad-network-affiliated search provider when properly configured. Your research stays private.

---

*Published on ClawHub. Built in response to OpenAI's March 2026 ad rollout.*
