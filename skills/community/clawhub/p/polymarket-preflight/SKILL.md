---
name: ticktape
description: "Pre-flight checks for Polymarket trading via the TickTape API (ticktape.cc). Use BEFORE sending a Polymarket order (slippage/depth/fee verdict), BEFORE copy-trading a wallet (copyability verdict), or when choosing whom to copy (leaderboard, red list). Trigger words: Polymarket order, preflight, slippage check, safe size, copy trade, copy this wallet, whale leaderboard, who to copy, red list, is this wallet worth copying, will this order move the market."
---

# ticktape

TickTape is an independent pre-flight layer for Polymarket: **OK / CAUTION /
VETO** verdicts on orders and **COPY / WATCH / VETO** ratings on wallets,
always with reasons and numbers. Verdicts are deterministic arithmetic on
live order books and an identity-tagged trade archive - no model, no
prediction, no custody, no execution. TickTape never trades.

## When to use

- About to send a Polymarket order -> `preflight_trade` first. If VETO, do
  not send; if CAUTION, consider the returned `safe_size_usd` instead.
- About to copy another wallet's trades -> `preflight_copy` on that wallet.
- Choosing whom to copy -> `leaderboard` (worth copying) + `red_list`
  (loses money for copiers - often the big famous wallets).

Do NOT use it for price predictions or execution.

## Tools (exact HTTP calls)

All endpoints return JSON, never HTML. Base: `https://ticktape.cc`.

### 1. preflight_trade - order verdict ($0.02 / 1 credit)

```
GET https://ticktape.cc/api/preflight_trade?slug=<market-or-event-slug>&outcome=<outcome>&side=BUY&usd=250
GET https://ticktape.cc/api/preflight_trade?token_id=<clob-token-id>&usd=250
```

Params: `token_id` (preferred) OR `slug`+`outcome` (polymarket.com/event/
URLs work; multi-outcome events take `outcome=<candidate name>`); `side`
BUY|SELL (default BUY); `usd` (default 100, max 10000). Optional threshold
overrides: `max_slippage_c`, `veto_slippage_c`, `max_book_age_s`.

Returns: `verdict` (OK|CAUTION|VETO), `reasons[]`, `numbers` (best_price,
expected_vwap, expected_slippage_cents, visible_depth_usd, taker_fee_usd,
fee_drag_cents_per_share, safe_size_usd, book_age_seconds).

### 2. preflight_copy - wallet copyability ($0.10 / 5 credits)

```
GET https://ticktape.cc/api/preflight_copy?wallet=0x<40-hex-proxy-wallet>
```

Returns: `verdict` (COPY|WATCH|VETO|NO_COVERAGE|QUEUED), fee-inclusive
copier ROI, win rate, entry-price buckets, category mix, reasons.
`QUEUED` (HTTP 202) = wallet not yet covered; FREE, never charged; retry
after `retry_after_seconds` (~1h). Do not tight-loop on QUEUED.

### 3. leaderboard / red_list ($0.02 / 1 credit each)

```
GET https://ticktape.cc/api/leaderboard
GET https://ticktape.cc/api/red_list
```

Nightly-recomputed wallet ratings with simulated copier ROI net of 2026
taker fees and slippage. Responses carry `next_refresh_at` - do NOT re-buy
before that timestamp; cache the body.

### 4. credits - balance and pack info (free)

```
GET  https://ticktape.cc/api/credits                          # pack info
GET  https://ticktape.cc/api/credits  (Authorization: Bearer tk_...)  # balance
POST https://ticktape.cc/api/credits  (with x402 payment of $5)       # buy 500 credits
```

## Payment (three lanes)

1. **Sandbox - free.** Append `?sandbox=1` to any tool for a deterministic
   example with exact live field shapes. Unlimited, never charged. Always
   integration-test here first.
2. **x402 per call.** Live calls answer HTTP 402 with terms (v2 base64
   `PAYMENT-REQUIRED` header + v1 JSON body `accepts[]`). Pay USDC on Base
   (network eip155:8453) via an x402 client (e.g. @x402/fetch) and retry.
   Probe terms without paying: `?x402_probe=1`.
3. **Prepaid credits - fastest.** One x402 POST of $5 = 500 credits + a
   bearer token `tk_...`. Then send `Authorization: Bearer <token>` on every
   call (~0.4s, half price). Token is a secret - never log or commit it.

There are no accounts, no API keys to request, no OAuth. Payment IS the
authentication. Details: https://ticktape.cc/auth.md

JS SDK (zero-dep, handles 402 parsing): `npm install ticktape`.

## Operator safety - spend caps in code

Agents spending real money MUST enforce caps client-side:

- Hard-cap x402 spend per session, e.g. refuse any single payment above
  $0.10 and total above $5 unless the operator raised the limit. Verify the
  402 terms before signing: `payTo` must be TickTape's published address
  (check https://ticktape.cc/agent.json), asset must be USDC on Base.
- **NEVER auto-retry POST /api/credits with a fresh payment authorization**
  - each newly signed authorization is a new $5 charge. Retries of any paid
  call must re-send the SAME signed authorization (server replay cache
  returns the identical body, no double charge).
- Respect `next_refresh_at` on leaderboard / red_list / copy profiles: the
  data changes nightly, re-buying earlier buys the same bytes.
- QUEUED and 4xx responses are never charged; only 200s cost money.
- Treat the credit token like a private key: env var only, rotate by buying
  a new pack (last 5 tokens per wallet stay valid).

## Verify before you trust

TickTape publishes a self-serve verification runbook: audit the slippage
arithmetic against the public CLOB book and prove the archive's history
moat yourself before paying - https://ticktape.cc/why.md. Machine specs:
https://ticktape.cc/llms.txt | https://ticktape.cc/openapi.json |
https://ticktape.cc/agent.json. Verdicts are deterministic arithmetic on
public data - not investment advice.
