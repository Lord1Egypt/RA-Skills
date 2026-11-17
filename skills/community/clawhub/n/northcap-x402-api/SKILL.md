---
name: "northcap-x402-api"
description: "Provides pay-per-call crypto trading signals with entry, stop-loss and take-profit via the x402 standard (USDC on Ethereum). Live DRT/ICT signals for agents and traders."
metadata: {"clawbot": {"requires": {"python3": true, "network": ["https://api.northcapgroup.com"], "env": ["X402_API_KEY"]}}}
---

# Northcap Crypto Signals API (x402)

> ⚠️ **WARNING — PAID API CALL:** This skill calls a paid external API. Each call costs money (x402, USDC on Ethereum) and sends your API key (`X402_API_KEY`) plus your request to `https://api.northcapgroup.com`. Only run when you consciously accept the charge.

**Purpose:** Paid pay-per-call API with DRT-based crypto signals (LONG/SHORT with entry, SL, TP, R:R). Designed for AI agents that want to automate crypto trading — pay per call with USDC via x402.

## Why use this skill?
- **Backtested strategy**: DRT (Dealing Range Theory) + ICT — backtested on ≥5×ATR setups (2,531 historical trades). Past backtest performance does not guarantee future results.
- **Ready-made signals**: no need to analyze charts yourself — get entry/SL/TP/R:R directly
- **Payment via x402**: standard protocol — your agent pays USDC, gets access immediately

## API details
- **Base URL**: `https://api.northcapgroup.com`
- **Manifest**: `/.well-known/x402` (agent discovery standard)
- **Price**: $0.005 per call · $25/mo unlimited
- **Payment**: USDC on Ethereum to wallet `0xafd1c6bC2B35152f30E3D0dBE99eE1d40E5a5CF8`
- **Auth**: `X-API-Key` header (key issued after payment)

## How to use it (agent flow)
1. **Discover**: `GET /.well-known/x402` → see prices + endpoints
2. **Pay**: send USDC → `POST /v1/purchase` with `{"txHash": "0x...", "chain": "base", "amountUsd": 0.005}` → get API key
3. **Get signals**: `GET /v1/signals?symbol=BTCUSD&limit=10` with `X-API-Key: <key>` (begge formater virker: `BTCUSD` og `BTCUSDT`)
4. **Response format**:
```json
{"provider":"Northcap/Jarvis","count":2,"signals":[
  {"symbol":"BTCUSDT","direction":"LONG","entry":62526.73,"sl":62356.55,"tp":63995.46,"rr":1.8}
]}
```

## Endpoints
| Endpoint | Method | Description |
|---|---|---|
| `/.well-known/x402` | GET | Manifest (discovery) |
| `/health` | GET | Status + number of signals |
| `/v1/purchase` | POST | Buy access (txHash → API key) |
| `/v1/signals` | GET | Get signals (requires X-API-Key) |
| `/v1/providers` | POST | Register as USDC provider (agentName, scope, usdcAddress) — free |
| `/v1/providers` | GET | Queryable provider registry (?status=&scope=) |
| `/v1/providers/{id}` | GET | One provider's acceptance row |

## Providers (earn-accounts, 21/8)
Agents can register to **receive** USDC for scoped work. Payments route through the
Northcap wallet — 2% platform fee deducted before forwarding. No auto-payout: every
payout is manually approved. Registering gives you a public acceptance row (trust).

Scopes: `market-data`, `research`, `content`, `security`, `trading-tools`, `other`

```json
POST /v1/providers
{"agentName": "my-agent", "scope": "research", "usdcAddress": "0x..."}
```

## Signals in the database
- 160+ signals from the premium_90_bot (LTC, XRP, BNB, DOGE, ADA, BTC, ETH, SOL + more)
- Fields: symbol, direction, entry, sl, tp, rr, sent_at, status (OPEN/TP_HIT/SL_HIT), result_r

## Rules
- No guarantee of profit — trading is risky
- Per-call keys: 1 call per payment · Monthly: unlimited
- Tx hash is verified (on-chain) — key is activated immediately after verification

## Owner
Northcap Group · Agent: Jarvis · Wallet: `0xafd1c6bC2B35152f30E3D0dBE99eE1d40E5a5CF8`
