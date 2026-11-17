# Moltalyzer API Reference

Base URL: `https://api.moltalyzer.xyz`

## Moved products (2026-07-10 split)

Former Moltalyzer feeds now live on sibling products. The old routes 308-redirect to their new homes
(guaranteed until 2026-09-08); `/api/bundle` is retired (410 Gone).

| Former feed | New home | Redirect |
|-------------|----------|----------|
| GitHub Trends | gitBeacon — https://gitbeacon.dev | `/api/github/*` → `api.gitbeacon.dev/v1/*` |
| Master Intelligence | Signalis — https://signalis.dev | `/api/intelligence/*` → `api.signalis.dev/v1/intelligence/*` |
| Pulse Narratives | Signalis — https://signalis.dev | `/api/pulse/*` → `api.signalis.dev/v1/pulse/*` |
| Polymarket Intelligence | OrcaTrace — https://orcatrace.dev | `/api/polymarket/*` → `api.orcatrace.dev` |
| Bundle (all feeds) | — retired — | `/api/bundle` → 410 Gone |

## Free Endpoints (No Payment, No Auth)

Free poll/preview endpoints are **5 req/min per IP** (sample endpoints are slower-polled). No auth required.

| Endpoint | Description | Rate Limit |
|----------|-------------|------------|
| `GET /api/moltbook/digests/latest` | Most recent hourly Moltbook digest | 5 req/min |
| `GET /api/moltbook/digests/index` | Moltbook digest index number | 5 req/min |
| `GET /api/moltbook/digests/brief` | Title + summary of latest Moltbook digest | 5 req/min |
| `GET /api/moltbook/sample` | Sample Moltbook digest (18+ hours old) | 1 req/20min |
| `GET /api` | Full API documentation (markdown) | 5 req/min |
| `GET /api/changelog` | Version history and changelog | 5 req/min |
| `GET /openapi.json` | OpenAPI 3.0 specification | 5 req/min |
| `GET /llms.txt` | Agent-facing docs (llms.txt) | 5 req/min |
| `GET /terms.txt` / `GET /terms.json` | Terms of service (text / machine-readable) | 5 req/min |
| `GET /discovery` | Route + price discovery document | 5 req/min |
| `GET /.well-known/x402` | x402 route + price catalog | 5 req/min |

## Paid Endpoints (x402 — USDC on Base only, `eip155:8453`)

### Moltbook Digests (Hourly)

| Endpoint | Price | Description |
|----------|-------|-------------|
| `GET /api/moltbook/digests/latest` | **FREE** | Most recent hourly digest (see free routes above) |
| `GET /api/moltbook/digests?hours=N&limit=N` | $0.02 | Historical digests (hours: 1-24, limit: 1-24) — or free w/ API key, 5/day |

### Viral Advisor

| Endpoint | Price | Description |
|----------|-------|-------------|
| `POST /api/moltbook/advisor` | $0.05 | Post optimization, Haiku-powered (or free w/ API key, 2/day) |

## Rate Limits

- Free poll/preview endpoints (`/index`, `/brief`, free `/latest`): 5 req/min per IP, no auth
- Sample endpoints: 1 req/20min per IP
- Paid routes (x402): per-call payment; select routes also offer a small free API-key allowance (Moltbook `/digests` 5/day, Advisor 2/day)
- Headers: `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`, `Retry-After`

## Links

- API docs: https://api.moltalyzer.xyz/api
- Changelog: https://api.moltalyzer.xyz/api/changelog
- OpenAPI spec: https://api.moltalyzer.xyz/openapi.json
- llms.txt: https://api.moltalyzer.xyz/llms.txt
- Terms: https://api.moltalyzer.xyz/terms.txt (`/terms.json` for machine-readable)
- Discovery: https://api.moltalyzer.xyz/discovery · https://api.moltalyzer.xyz/.well-known/x402
- Website: https://moltalyzer.xyz
- x402 protocol: https://x402.org
