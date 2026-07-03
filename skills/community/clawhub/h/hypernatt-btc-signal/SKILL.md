---
name: hypernatt-btc-signal
version: 2.0.0
author: HyperNatt
license: MIT
tags:
  - crypto
  - btc
  - trading-intelligence
  - x402
  - hyperliquid
  - mcp
description: >
  HyperNatt Terminal signal skill — live BTC/USDC Mimo vault cycle state via HTTP x402
  ($0.01 USDC on Base). Full terminal: 14 MCP tools, 10 free credits/day, HOLD free.
  Read-only JSON — not a trade signal.
---

# HyperNatt Terminal (signal skill)

## Summary

OpenClaw **thin wrapper** for one Decision Core endpoint: **Mimo BTC/USDC cycle state**
(`hypernatt_mimo_cycle_state_v1`) at `https://hypernatt.com/api/m2m/signal`.

For the **full agent terminal** (14 MCP tools — MM hunt, similarity, liq radar, trap state,
swap, manifest, pass status): connect MCP at `https://hypernatt.com/mcp/protocol`.

## HyperNatt Terminal (F40N)

| Tier | Detail |
|------|--------|
| **MCP free tier** | 10 Decision Core credits/day without wallet (`get_agent_manifest` first) |
| **HOLD free** | `get_btc_usdc_signal` with HOLD verdict = 0 debit (MCP; HTTP when applicable) |
| **Agent Pass** | $19/mo — `https://hypernatt.com/api/m2m/pass/status` |
| **This skill (HTTP)** | $0.01 USDC/call via x402 on Base when not covered by free tier / pass |
| **Track record** | https://hypernatt.com/stats |

Quickstart: https://github.com/DIALLOUBE-RESEARCH/hypernatt-terminal/blob/main/docs/quickstart.md

## When to use

- Agent needs **current Mimo vault cycle direction** and leg context (read-only)
- Agent needs **verifiable track record** (win rate, trade count) with Hyperliquid proof
- OpenClaw workflow prefers a **single HTTP skill** instead of full MCP

## When NOT to use

- Executing trades (read-only)
- TP/SL or entry advice (product contract forbids it)
- MM hunt, liq radar, trap state, swap → use **MCP terminal** (14 tools)
- Free public stats only → `https://hypernatt.com/stats`

## Inputs

| Env var | Required | Description |
|---------|----------|-------------|
| `X402_PAYMENT_B64` | No | Base64 x402 payment payload. If omitted, handler returns 402 instructions. |
| `HYPERNATT_SIGNAL_URL` | No | Default `https://hypernatt.com/api/m2m/signal` |

## Outputs

JSON object:

```json
{
  "product": "hypernatt_mimo_cycle_state_v1",
  "direction": "LONG|SHORT|null",
  "cycle_id": "...",
  "track_record": { "win_rate": 0.94, "total_trades": 74, "url": "https://hypernatt.com/stats" },
  "disclaimer": "Live verifiable Mimo cycle state only. Not a trade recommendation."
}
```

## Example

```bash
# Step 1 — payment instructions (or 200 if free tier credit applies)
python handler.py

# Step 2 — after x402 client signs payment
export X402_PAYMENT_B64="<base64-json>"
python handler.py
```

## Handler

- `handler.py` — stdlib + urllib (no pip deps, recommended)
- `handler.js` — Node + axios (optional; set `X402_PAYMENT_B64` after x402 signing)

## Links

| Resource | URL |
|----------|-----|
| MCP (14 tools) | https://hypernatt.com/mcp/protocol |
| Server card | https://hypernatt.com/.well-known/mcp/server-card.json |
| Stats | https://hypernatt.com/stats |
| Smithery | https://smithery.ai/servers/hypernatt/hypernatt-terminal |
| Pass status | https://hypernatt.com/api/m2m/pass/status |

## ClawHub publisher checklist

- [x] Source repo linked to verified GitHub org
- [x] No secrets in SKILL.md
- [x] Handler code reviewed (no wallet drain patterns)
- [x] Publisher verification form submitted
