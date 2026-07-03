# HyperNatt Terminal — signal skill (x402)

OpenClaw skill for **one** HyperNatt Decision Core endpoint: live **Mimo BTC/USDC cycle state**
(`hypernatt_mimo_cycle_state_v1`) via HTTP + x402.

**Full terminal:** 14 MCP tools at `https://hypernatt.com/mcp/protocol` — manifest-first onboarding,
MM hunt, similarity, liq radar, trap state, Li.Fi swap. See
[hypernatt-terminal quickstart](https://github.com/DIALLOUBE-RESEARCH/hypernatt-terminal/blob/main/docs/quickstart.md).

## Pricing (F40N)

| Path | Cost |
|------|------|
| MCP free tier | 10 Decision Core credits/day (no wallet) |
| HOLD on signal | Free when verdict is HOLD |
| Agent Pass | $19/mo — https://hypernatt.com/api/m2m/pass/status |
| This skill (HTTP) | $0.01 USDC/call on Base via x402 (or 200 when free credit applies) |

## What you get

- Mimo vault **cycle direction** and leg state (read-only)
- **Track record** (win rate, total trades) with Hyperliquid proof
- **Not** a trade recommendation — no SL/TP, no "BUY NOW"

## Requirements

- Wallet with USDC on **Base** (chain id 8453) for paid HTTP calls
- x402-capable client OR pre-signed `X402_PAYMENT_B64` env var

## Usage (OpenClaw)

```yaml
skill: hypernatt-btc-signal
env:
  X402_PAYMENT_B64: "<optional — base64 payment payload>"
```

```bash
python handler.py
# or
node handler.js
```

Without payment → HTTP 402 with x402 `accepts[]` (or HTTP 200 if free tier credit applies).

With valid payment → JSON summary: direction, cycle_id, track_record, disclaimer.

## Endpoints

| URL | Role |
|-----|------|
| `https://hypernatt.com/api/m2m/signal` | This skill — HTTP x402 REST |
| `https://hypernatt.com/mcp/protocol` | Full terminal — 14 MCP tools |
| `https://hypernatt.com/stats` | Free public win rate / track record |
| `https://hypernatt.com/api/m2m/pass/status` | Agent Pass / subscription status |

## MCP alternative (recommended for agents)

Connect MCP client to `https://hypernatt.com/mcp/protocol`:

1. `get_agent_manifest` (free)
2. `get_btc_usdc_signal` (free tier / HOLD free / pass / x402)

## Publisher verification (ClawHub)

This skill is **read-only HTTP + optional x402**. It does **not**:

- Request private keys in SKILL.md
- Execute shell commands on install
- Transfer funds except explicit user-initiated x402 USDC on Base

Publisher: HyperNatt / contact@hypernatt.com

## Security note (Feb 2026 ClawHub incident)

Only install skills from verified publishers. Verify this repo matches
`github.com/DIALLOUBE-RESEARCH` before use.
