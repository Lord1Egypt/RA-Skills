---
name: numinous
description: Access Numinous (Bittensor Subnet 6) forecasting tools — AI probability predictions on binary events, real-time signals aggregated from news and prediction markets, and usage tracking. Use when the user asks for a forecast, prediction, probability estimate, signals on a Polymarket market, Numinous data, miner leaderboard info, or mentions Numinous / Bittensor Subnet 6.
---

# Numinous Forecasting Tools

Numinous is a decentralized forecasting network (Bittensor Subnet 6). Miners submit Python forecasting agents; validators score them; this plugin wraps the public APIs the network exposes.

## API surfaces

| Base URL | What lives here | Docs Swagger
|---|---|---|
| `https://api.numinouslabs.io` | Forecasts, leaderboard, miner agents, historical runs | /api/docs
| `https://signals.numinouslabs.io` | Signals (news + market aggregation, LLM-scored) | /docs
| `https://api-eversight.numinouslabs.io` | Balance, usage, costs (public), Stripe top-ups (browser only) | /docs

Credits are shared across all three — spend on forecasts or signals draws from the same balance.

## First-run setup

Scripts live at `./scripts/` relative to this SKILL.md. The scripts work regardless of cwd, but paths in this doc assume you run them from the skill directory. Before running anything, check whether these env vars are set: `NUMINOUS_API_KEY`, `NUMINOUS_X402_EVM_PRIVATE_KEY`, `NUMINOUS_X402_SVM_PRIVATE_KEY`.

Then pick an auth path based on what the user wants:

| User wants | Needs | Env var |
|---|---|---|
| Forecasts + signals, pay in USD via top-up | API key | `NUMINOUS_API_KEY` |
| Forecasts only, pay in crypto per request | Funded EVM wallet (USDC on Base) | `NUMINOUS_X402_EVM_PRIVATE_KEY` |
| Forecasts only, pay in crypto per request | Funded Solana wallet (USDC on Solana) | `NUMINOUS_X402_SVM_PRIVATE_KEY` |

**If neither is set**, walk the user through the decision:

> You can use Numinous two ways:
> 1. **API key** (recommended) — works for everything (forecasts + signals), prepaid credit balance. Create one at https://eversight.numinouslabs.io/api-keys (up to 5 per account) and top up at https://eversight.numinouslabs.io/payments. Set `NUMINOUS_API_KEY=<your_key>`.
> 2. **x402 crypto payment** — forecasts only (signals doesn't accept x402). No account needed, just a funded USDC wallet on Base or Solana. Set `NUMINOUS_X402_EVM_PRIVATE_KEY=<hex>` or `NUMINOUS_X402_SVM_PRIVATE_KEY=<base58>`.
>
> Which would you like to set up?

Env vars should live in the user's shell environment (bash/zsh profile on macOS/Linux, PowerShell profile or System Properties on Windows) or a project-local `.env` file that's gitignored. Use whatever idiom matches the user's shell — e.g. `export NUMINOUS_API_KEY=...` for bash/zsh, `$env:NUMINOUS_API_KEY = "..."` for PowerShell, `setx NUMINOUS_API_KEY "..."` for Windows cmd. Never write keys to repo-committed files.

## Capabilities & costs

Fetch current pricing at runtime — don't hardcode. The endpoint is public, no auth:

`GET https://api-eversight.numinouslabs.io/api/v1/credits/costs`

At time of writing:

| Capability | Script / endpoint | Cost | Auth |
|---|---|---|---|
| Create a forecast (async job) | `scripts/forecast.py` | 0.1 credits | API key |
| Create a forecast paying via crypto | `scripts/forecast_x402.py` | $0.10 USDC | x402 wallet |
| Get signals for a market/question | `scripts/signals.py` | 0.025 credits | API key (no x402) |
| Check balance | `GET /api/v1/me/balance` | free | API key |
| Check usage history | `GET /api/v1/me/usage` | free | API key |
| Get current costs | `GET /api/v1/credits/costs` | free | none |
| Browse miner leaderboard | `GET /api/v1/leaderboard` | free | none |
| Read a miner's agent code | `GET /api/v1/agents/{version_id}/code` | free | none |
| Top up balance (Stripe) | web UI only | — | browser session |

## Runbooks

### Get a forecast (most common path)

Two input modes. Structured is more precise; query is faster to compose.

> **Shell-quoting gotcha:** if the question contains a `$` sign, **always use single quotes** (bash/zsh/PowerShell all treat single quotes as literal). Double quotes will shell-expand `$150k` to `50k`, silently asking a different question. When in doubt — or anytime a dollar amount is involved — prefer structured mode, which takes each field as a separate `--title` / `--description` flag with no substring ambiguity.

**Query mode** — one natural-language line:
```bash
python ./scripts/forecast.py 'Will Bitcoin exceed $150k before end of 2026?'
```

**Structured mode** — explicit event spec (safest when prices / `$` are involved):
```bash
python ./scripts/forecast.py \
  --title 'Will Bitcoin exceed $150,000 before end of 2026?' \
  --description 'Resolves YES if BTC spot price on any major exchange reaches $150,000 USD at any point before 2026-12-31T23:59:59Z.' \
  --cutoff 2026-12-31T23:59:59Z \
  --topics crypto,finance
```

**Pin a specific miner** (any mode) with `--agent-version-id <uuid>`. Get version IDs from the leaderboard (see below). When unpinned, the network auto-routes to the top pool miner.

The script submits, polls every 5s, and prints the final probability plus the miner's reasoning. Typical completion: 25–120 seconds.

### Pay for a forecast via crypto (x402)

Same args as the API-key forecast. Uses `NUMINOUS_X402_EVM_PRIVATE_KEY` (preferred) or `NUMINOUS_X402_SVM_PRIVATE_KEY`. Wallet must hold enough USDC ($0.10 per request).

```bash
python ./scripts/forecast_x402.py 'Will ETH exceed $10k before end of 2026?'
```

The `x402` Python library auto-handles the `402 → sign → retry` flow. No signals support — if the user asks to pay for signals via crypto, tell them it's not available and offer the API key route.

### Get signals for a prediction market

Accepts a Polymarket URL, slug, condition_id, or a free-text question.

```bash
# Polymarket (URL or slug; compound event URLs and sub-market slugs both work)
python ./scripts/signals.py --market https://polymarket.com/event/some-slug

# Free-text question — use single quotes if the question contains $
python ./scripts/signals.py --question 'Will Iran conduct a nuclear test before end of 2026?'
```

Returns ranked signals from exa (web news), Indicia (geopolitics, Polymarket markets, LiveUAMap, GDELT, unusual_whales), and Perplexity — each scored by Grok with `relevance_score` (0-1), `impact_score` (0-1), `impact_bucket` (S1-S3 scenario ladder), `direction` (supports_yes / supports_no / neutral), and a one-sentence `rationale`.

### Check balance and usage

No script needed — simple GET requests. Use whichever HTTP tool matches the user's environment (`curl` on Unix/Git Bash, `Invoke-RestMethod` on PowerShell, Python `urllib.request`, or your agent's WebFetch equivalent).

- **Balance:** `GET https://api-eversight.numinouslabs.io/api/v1/me/balance` with header `X-API-Key: <NUMINOUS_API_KEY>`
- **Usage:** `GET https://api-eversight.numinouslabs.io/api/v1/me/usage?limit=50` (also accepts `since=<ISO8601>`, `limit` up to 200) with the same header

Bash example:
```bash
curl -s -H "X-API-Key: $NUMINOUS_API_KEY" https://api-eversight.numinouslabs.io/api/v1/me/balance
```
PowerShell example:
```powershell
Invoke-RestMethod -Uri https://api-eversight.numinouslabs.io/api/v1/me/balance -Headers @{ "X-API-Key" = $env:NUMINOUS_API_KEY }
```

`/me/usage` transactions include a `resource` field — values are `signal_compute` or `prediction_job`. Use this to group spend by product (not the `description` string).

When the user wants to top up, send them to https://eversight.numinouslabs.io/payments (Stripe, browser-only).

### Browse the leaderboard / inspect a miner

All public, no auth needed. Again, use any HTTP tool — examples shown in bash:

```bash
# Top miners (sorted by the active pool — currently global_brier by default)
curl -s "https://api.numinouslabs.io/api/v1/leaderboard?limit=10"

# A specific miner's agent versions
curl -s "https://api.numinouslabs.io/api/v1/miners/{miner_uid}/{miner_hotkey}/agents"

# Read the actual forecasting code a miner is running
curl -s "https://api.numinouslabs.io/api/v1/agents/{version_id}/code"
```

When the user wants to "pin" a miner in a forecast, grab a `version_id` from `/agents` and pass `--agent-version-id` to `forecast.py`.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `402 Payment Required`, body `{}`, `payment-required` header set | No auth on a paid endpoint | Set `NUMINOUS_API_KEY` or use the `_x402` script |
| `401` on `/me/*` | `X-API-Key` missing or invalid | Re-check the env var, or rotate the key at /api-keys |
| `404 MARKET_NOT_FOUND` on signals | Polymarket slug stale / closed | Ask user for a current URL, or try a sub-market slug from their multi-market event |
| `422 VALIDATION_ERROR` on signals | Sent both `market` and `question`, or neither | Send exactly one |
| `502 UPSTREAM_UNAVAILABLE` on signals | Polymarket Gamma down | Transient, retry; or fall back to free-text `--question` |
| Forecast stuck `PENDING` > 3 min | Miner queue slow | Keep polling up to 5 min; occasionally miners retry |
| Can't reach `api.numinouslabs.io/docs` from an agent | Bot-blocked swagger UI | Read `reference.md` in this skill instead, or fetch `https://api.numinouslabs.io/api/openapi.json` (public) |

## Links for the user

- **Create / manage API keys:** https://eversight.numinouslabs.io/api-keys
- **Top up balance (Stripe):** https://eversight.numinouslabs.io/payments
- **Leaderboard UI:** https://leaderboard.numinouslabs.io
- **Landing page:** https://numinouslabs.io
- **API reference (Swagger, browser only):** https://api.numinouslabs.io/api/docs
- **OpenAPI spec (scriptable):** https://api.numinouslabs.io/api/openapi.json

## Deeper reference

See [reference.md](reference.md) for full endpoint schemas, response field definitions, forecaster names, x402 payment header format, and the impact_bucket ladder. Load it only when you need details the tables above don't cover.
