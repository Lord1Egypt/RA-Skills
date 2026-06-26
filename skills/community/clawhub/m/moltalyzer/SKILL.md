---
name: moltalyzer
version: 2.4.1
description: >-
  Real-time intelligence feeds for AI agents. Flagship: Polymarket prediction-market
  intelligence — short-window movers, calibrated whale entries, order-book microstructure, and
  resolving-soon timing across ~42,000 markets. Plus Moltbook community sentiment, GitHub trends,
  Pulse narrative intelligence, and a cross-source Master Intelligence Digest. Computed, not raw.
  Free index + preview endpoints on every feed (no auth); deeper signals are pay-per-call via x402.
homepage: https://moltalyzer.xyz
metadata:
  openclaw:
    emoji: "🔭"
    requires:
      bins: ["node"]
    install:
      - id: npm
        kind: command
        command: "npm install node-fetch"
        bins: ["node"]
        label: "Install fetch (if needed)"
---

# Moltalyzer — Real-Time Intelligence Feeds for AI Agents

API at `https://api.moltalyzer.xyz`. Real-time intelligence feeds for AI agents, **led by Polymarket prediction-market intelligence**. Every feed is free to poll — free `/index` plus preview endpoints (5 req/min per IP); deeper signals and history are pay-per-call via x402, with a small free API-key allowance on select routes.

Full API docs: [api.moltalyzer.xyz/docs](https://api.moltalyzer.xyz/docs) | OpenAPI spec: [api.moltalyzer.xyz/openapi.json](https://api.moltalyzer.xyz/openapi.json)

## Intelligence Feeds

Polymarket is the flagship feed — the deepest product, with computed signal (whale calibration, order-book microstructure, resolution timing) rather than raw odds. Paid Polymarket routes: `/latest` $0.01 (or 3/day free with an API key, shared pool with `/signal`), `/signal` $0.01 (or 3/day free with an API key, shared with `/latest`), `/signals` $0.03, `/resolving` $0.02, `/whales` $0.05, `/digest` $0.10, `/digest/history` $0.05, `/research?market=<slug>` $1.00. Free no-auth Polymarket routes: `/index`, `/pulse`, `/digest/brief`, `/sample`.

| Feed | What It Covers | Free Endpoint | Cadence |
|------|---------------|---------------|---------|
| **Polymarket (flagship)** | Movers + whale entries (hold-to-resolution calibrated) + microstructure + resolving-soon | `GET /api/polymarket/pulse` | ~10 min |
| Master Intelligence | Cross-domain synthesis of all feeds | `GET /api/intelligence/latest` | 4 hours |
| Moltbook Community | AI agent discourse & sentiment | `GET /api/moltbook/digests/latest` | 1 hour |
| GitHub Trends | New repos, emerging tools, language trends | `GET /api/github/digests/latest` | 24 hours |
| Pulse Narratives | Cross-source narrative lifecycle tracking | `GET /api/pulse/ai-business/digest/latest` | 4 hours |
| Token Signals ⚠️ | On-chain signal detection & scoring — **TEMPORARILY OFFLINE** | `GET /api/tokens/latest` | 4 minutes |

Free poll endpoints (`/index`, `/brief`, and the free `/latest` feeds — Moltbook, GitHub, Intelligence, Pulse): **5 req/min per IP, no auth needed.** Note: Polymarket `/latest` is **paid** ($0.01, or 3/day free with an API key) — its free no-auth routes are `/index`, `/pulse`, `/digest/brief`, and `/sample`.

> ⚠️ **Token Signals is temporarily offline** while its hybrid rule+LLM scoring migrates to self-hosted inference. Paid token endpoints (`/api/tokens/signal`, `/signals`, `/history`) return **503 with `status:"offline"` and no x402 charge**; free token endpoints (`/index`, `/latest`, `/sample`) stay up and carry `status:"offline"`. Poll `/api/tokens/index` — `status` returns to `"live"` on relaunch. The other five feeds are unaffected.

## Quick Start — Polling Pattern

The recommended integration pattern: poll cheap index endpoints, fetch full data only when new.

```typescript
// All free, no auth, no setup
const BASE = "https://api.moltalyzer.xyz";

// 1. Check index (unlimited, free) to detect new data
const indexRes = await fetch(`${BASE}/api/intelligence/index`);
const { index, updatedAt } = await indexRes.json();

// 2. If new, fetch brief (unlimited, free) for a quick summary
const briefRes = await fetch(`${BASE}/api/intelligence/brief`);
const brief = await briefRes.json();
// brief.data: { title, executiveSummary, sentiment }

// 3. If actionable, fetch latest (5 req/min, free) for full analysis
const latestRes = await fetch(`${BASE}/api/intelligence/latest`);
const latest = await latestRes.json();
// latest.data: { fullAnalysis, crossDomainInsights, narratives, signals, ... }
```

## Endpoint Tiers

Every feed has 3 tiers — index, brief, latest — designed for efficient polling:

| Tier | Rate Limit | Returns | Use For |
|------|-----------|---------|---------|
| `/index` | Unlimited | ID + timestamp + cadence | Change detection |
| `/brief` | Unlimited | Title + summary + key metrics | Quick situational awareness |
| `/latest` | 5 req/min | Full analysis + all structured data | Deep analysis & decision-making |

## Additional Free Endpoints

```typescript
// Sample data (older snapshots, great for testing)
await fetch(`${BASE}/api/moltbook/sample`);      // 1 req/20min
await fetch(`${BASE}/api/github/sample`);         // 1 req/20min
await fetch(`${BASE}/api/polymarket/sample`);     // 1 req/20min
await fetch(`${BASE}/api/tokens/sample`);         // 1 req/20min
await fetch(`${BASE}/api/intelligence/sample`);   // 1 req/20min

// Submit feedback on digest quality
await fetch(`${BASE}/api/intelligence/feedback`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ rating: "good", digestId: "..." }),
});
```

## Viral Advisor (Human-Facing Product)

A human-facing post optimization tool built on the same intelligence feeds. Submit a post idea, get a complete ready-to-publish post with viral scoring and data-backed suggestions. `POST /api/moltbook/advisor` ($0.05, or 2/day free with an API key). (The agent-facing intelligence feeds above, led by Polymarket, are the core product.)

```typescript
const res = await fetch(`${BASE}/api/moltbook/advisor`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "AI agents are replacing junior devs" }),
});
const data = await res.json();
// data.viralScore, data.suggestedTitle, data.suggestedContent, data.suggestions
```

> Advisor and other premium endpoints require payment. See [api.moltalyzer.xyz/docs](https://api.moltalyzer.xyz/docs) for pricing and payment options.

## Recommended Polling Intervals

| Feed | Update Cadence | Poll `/index` Every | Fetch `/latest` When |
|------|---------------|--------------------|--------------------|
| Intelligence | 4 hours | 10 minutes | Index changes |
| Moltbook | 1 hour | 5 minutes | Index changes |
| GitHub | 24 hours | 6 hours | Index changes |
| Polymarket | ~10 min | 15 minutes | Index changes |
| Pulse | 4 hours | 15 minutes | Index changes |
| Tokens ⚠️ offline | 4 minutes | 2 minutes (watch for `status:"live"`) | Index changes / relaunch |

## Error Handling

- **429** — Rate limited. Respect `Retry-After` header (seconds to wait).
- **503** — Data stale (pipeline issue). Response includes `retryAfter` field.
- **404** — No data available yet.

All responses include `RateLimit-Remaining` and `RateLimit-Reset` headers.

## Reference Docs

For full response schemas, see `{baseDir}/references/response-formats.md`.
For more code examples and error handling patterns, see `{baseDir}/references/code-examples.md`.
For complete endpoint tables and rate limits, see `{baseDir}/references/api-reference.md`.
