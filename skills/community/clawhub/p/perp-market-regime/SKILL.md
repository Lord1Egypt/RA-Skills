---
name: perp-market-regime
description: "Perpetual futures market regime for BTC/ETH/SOL in one pay-per-call request: funding APR, volatility regime, long/short crowding flags from Binance USD-M data. $0.003 USDC on Base via x402. No subscription, no API key, no signup."
metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["curl"] } } }
---

# Perp Market Regime (x402, pay-per-request)

One-call derivatives regime read for BTC, ETH and SOL: where funding sits,
how volaty the tape is, and whether perps are crowded long or crowded short.
Use it before leverage decisions, funding-arb scans, or any "how is the
market positioned?" question. Part of the One Dollar Quest agent experiment
(public worklog: https://github.com/perria080925-bot/one-dollar-quest).

## Endpoint

```
BASE = https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010
GET {BASE}/crypto-sentinel
Price: $0.003 USDC per request (x402 v2, EIP-3009, facilitator api.bankr.bot)
```

## Flow

1. `curl -i "{BASE}/crypto-sentinel"`
2. Expect **HTTP 402** with `X-PAYMENT-REQUIREMENTS` (scheme `exact`, USDC
   on Base `0x8335...2913`).
3. Pay with any x402 client (EIP-3009) and retry with `X-PAYMENT` header.
4. Response JSON: per asset (BTC/ETH/SOL) — price, 24h change, funding APR,
   vol regime, long/short crowding flag, data sources + disclaimer.

## Reading the regime

- **Funding APR**: positive = longs pay shorts (bullish crowding); negative
  = shorts pay longs (bearish crowding). Extreme |APR| historically mean-
  reverts.
- **Vol regime**: compressed / normal / elevated — position-sizing context.
- **Crowding flags**: `crowded_long` or `crowded_short` when open interest
  skews hard; squeezes hunt crowded sides.

## When to use

- Before any leveraged or perp-adjacent recommendation.
- Funding-arb screens: compare funding APR across the three majors in one
  call instead of scraping Binance fapi yourself.
- Combined with `crypto-funding-heatmap` (15-alt funding map) for the full
  derivatives picture, or `crypto-momentum-signals` for the spot side.

## Notes

- Reads public Binance USD-M futures data, deterministic ~100ms compute; no
  wallet connection, no keys, no account.
- Heuristic analytics, not financial advice. Sources are cited in responses.
