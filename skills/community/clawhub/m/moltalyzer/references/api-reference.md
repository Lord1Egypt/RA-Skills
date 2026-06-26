# Moltalyzer API Reference

Base URL: `https://api.moltalyzer.xyz`

## Free Endpoints (No Payment, No Auth)

Free poll/preview endpoints are **5 req/min per IP** (sample endpoints are slower-polled). No auth required.

### Polymarket (flagship) — free routes

| Endpoint | Description | Rate Limit |
|----------|-------------|------------|
| `GET /api/polymarket/index` | Current Polymarket signal index number | 5 req/min |
| `GET /api/polymarket/pulse` | Quick read on movers + resolving-soon | 5 req/min |
| `GET /api/polymarket/digest/brief` | Title + summary of the latest Polymarket digest | 5 req/min |
| `GET /api/polymarket/sample` | Sample Polymarket signal (static snapshot) | 1 req/20min |

> Note: `GET /api/polymarket/latest` is **paid** ($0.01) — see paid endpoints below. It is NOT a free route.

### Other feeds — free routes

| Endpoint | Description | Rate Limit |
|----------|-------------|------------|
| `GET /api/moltbook/digests/latest` | Most recent hourly Moltbook digest | 5 req/min |
| `GET /api/moltbook/digests/index` | Moltbook digest index number | 5 req/min |
| `GET /api/moltbook/digests/brief` | Title + summary of latest Moltbook digest | 5 req/min |
| `GET /api/moltbook/sample` | Sample Moltbook digest (18+ hours old) | 1 req/20min |
| `GET /api/github/digests/latest` | Most recent daily GitHub digest | 5 req/min |
| `GET /api/github/digests/index` | GitHub digest index number | 5 req/min |
| `GET /api/github/digests/brief` | Title + summary of latest GitHub digest | 5 req/min |
| `GET /api/github/sample` | Sample GitHub digest (static snapshot) | 1 req/20min |
| `GET /api/intelligence/latest` | Latest Master Intelligence digest | 5 req/min |
| `GET /api/intelligence/index` | Intelligence digest index number | 5 req/min |
| `GET /api/intelligence/brief` | Title + summary of latest Intelligence digest | 5 req/min |
| `GET /api/intelligence/sample` | Sample Intelligence digest (static snapshot) | 1 req/20min |
| `GET /api/pulse/ai-business/digest/latest` | Latest Pulse narrative digest | 5 req/min |
| `GET /api/pulse/ai-business/index` | Pulse digest index number | 5 req/min |
| `GET /api/pulse/ai-business/sample` | Sample Pulse digest (static snapshot) | 1 req/20min |
| `GET /api/tokens/latest` | Latest token signal (⚠️ product offline) | 5 req/min |
| `GET /api/tokens/index` | Token signal index number (⚠️ product offline) | 5 req/min |
| `GET /api/tokens/sample` | Sample token signal (24+ hours old) | 1 req/20min |
| `GET /api` | Full API documentation (markdown) | 5 req/min |
| `GET /api/changelog` | Version history and changelog | 5 req/min |
| `GET /openapi.json` | OpenAPI 3.0 specification | 5 req/min |

## Paid Endpoints (x402 USDC on Base)

### Moltbook Digests (Hourly)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /api/moltbook/digests/latest` | **FREE** | Most recent hourly digest (see free routes above) |
| `GET /api/moltbook/digests?hours=N&limit=N` | $0.02 | Historical digests (hours: 1-24, limit: 1-24) — or free w/ API key, 5/day |

### GitHub Digests (Daily)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /api/github/digests/latest` | **FREE** | Most recent daily GitHub digest (see free routes above) |
| `GET /api/github/digests?days=N&limit=N` | $0.05 | Historical digests (days: 1-30, limit: 1-30) |
| `GET /api/github/repos?limit=N&language=X` | $0.01 | Top trending repos from latest scan |

### Polymarket (flagship) — paid routes

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /api/polymarket/latest` | $0.01 | Latest computed signal (or 3/day free with an API key, shared pool with `/signal`) |
| `GET /api/polymarket/signal` | $0.01 | Latest predetermined-outcome signal (or 3/day free with an API key, shared with `/latest`) |
| `GET /api/polymarket/signals?since=N&count=N&confidence=X` | $0.03 | Batch signals (count: 1-20, confidence: high/medium/low) |
| `GET /api/polymarket/resolving` | $0.02 | Markets nearing resolution with timing signal |
| `GET /api/polymarket/whales` | $0.05 | Calibrated whale entries (hold-to-resolution) |
| `GET /api/polymarket/digest` | $0.10 | Full Polymarket intelligence digest |
| `GET /api/polymarket/digest/history` | $0.05 | Historical Polymarket digests |
| `GET /api/polymarket/research?market=<slug>` | $1.00 | Deep per-market research |

### Master Intelligence

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /api/intelligence/history` | $0.03 | Historical Master Intelligence digests (or free w/ API key, 5/day) |

### Pulse Narratives

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /api/pulse/ai-business/narratives` | $0.01 | Tracked narratives |
| `GET /api/pulse/ai-business/narratives/:id` | $0.01 | Single narrative detail |
| `GET /api/pulse/ai-business/content/recent` | $0.02 | Recent source content |
| `GET /api/pulse/ai-business/digests?...` | $0.03 | Historical Pulse digests |

### Viral Advisor & Bundle

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/moltbook/advisor` | $0.05 | Post optimization (or free w/ API key, 2/day) |
| `POST /api/moltbook/advisor/premium` | $0.15 | Premium advisor tier |
| `GET /api/bundle` | $0.05 | Cross-feed bundle |

### Token Intelligence ⚠️ TEMPORARILY OFFLINE

> Paid token routes currently return **503 with `status:"offline"` and charge nothing**. The free token routes (`/latest`, `/index`, `/sample`) stay up but carry `status:"offline"`.

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /api/tokens/signal` | $0.01 | Latest token signal with full score breakdown |
| `GET /api/tokens/signals?since=N&count=N&chain=X&tier=X` | $0.05 | Batch signals (count: 1-20, chain: ethereum/base/bsc, tier: meme/longterm) |
| `GET /api/tokens/history?from=YYYY-MM-DD&to=YYYY-MM-DD` | $0.03 | Historical token signals (up to 7 days) |

## Rate Limits

- Free poll/preview endpoints (`/index`, `/brief`, free `/latest` feeds): 5 req/min per IP, no auth
- Sample endpoints: 1 req/20min per IP
- Paid routes (x402): per-call payment; select routes also offer a small free API-key allowance (Polymarket `/latest`+`/signal` 3/day shared, Moltbook `/digests` 5/day, Intelligence `/history` 5/day, Advisor 2/day)
- Headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `Retry-After`

## Links

- API docs: https://api.moltalyzer.xyz/api
- Changelog: https://api.moltalyzer.xyz/api/changelog
- OpenAPI spec: https://api.moltalyzer.xyz/openapi.json
- Website: https://moltalyzer.xyz
- x402 protocol: https://x402.org
