---
name: hyperliquid-trader-record
description: Verify any Hyperliquid wallet's track record from the public ledger before copying it. Win rate, expectancy, profit factor, drawdown, equity curve, positions and anomaly flags for $0.05 per address via x402, no API key.
version: 1.0.0
homepage: https://cryptopulse.theaslangroupllc.com/api/trader-record
metadata:
  openclaw:
    emoji: "🧾"
---

# Hyperliquid Trader Record (PulseNetwork)

One job: given a Hyperliquid address, return the verifiable track record a copy-trading decision
needs, computed from the venue's public ledger. No language model, no API key, $0.05 per address
over x402. Served by CryptoPulse (PulseNetwork, The Aslan Group LLC).

## Use it when the user asks

- "Verify this wallet", "show me their track record", "what is their drawdown"
- "What is 0x...'s win rate / drawdown / expectancy?"
- "Which markets make this account its money?", "is this a market maker or a directional trader?"
- Screening candidates from `/api/top-traders` or a leaderboard before allocating

## The call

`GET https://cryptopulse.theaslangroupllc.com/api/trader-record?address=0x...&window=month`

- `address` (required): the 0x wallet. `window` (optional): day | week | month | allTime (default allTime) for the equity curve and drawdown.
- Response: `coverage` (the venue returns the most recent 2,000 fills; the span is stated),
  `trades` (closing orders, win rate on gross closed PnL and net of fees, average win and loss,
  expectancy gross and net, profit factor, largest win and loss, realized PnL gross and net of fees), `markets` (best and worst by realized PnL,
  concentration), `activity` (maker share, builder-routed share, liquidation fills, time-of-day
  profile), `drawdown` (max drawdown in USD and as a percent of equity at the peak, for the
  window), `equity_curve` (60 points), `current` (account value, open positions, leverage), and
  `anomalies` (plain-English flags: concentration, rapid opposite fills, liquidations, maker-heavy).

## How to present it

- Lead with coverage: say what span the fill statistics cover before quoting a win rate, and check `coverage.last_fill_age_days`; the venue returns the most recent 2,000 fills, which for an active account can be a single day months ago while the equity window is current (`stats_window_matches_equity_window`).
- Quote drawdown as the PnL-curve figure against equity at the peak; deposits are not losses.
- Treat anomaly flags as things to inspect, not verdicts. Rapid opposite fills can be scalping.
- This is public ledger data for an address, not an identity, and past results are not a forecast.
  Never present it as advice to copy.

## Paying

State the endpoint and the $0.05 price before the first paid call and get the user's go-ahead.
Pay exactly the signed 402 challenge, only to `theaslangroupllc.com` origins, from a key the user
configured as an environment secret or a wallet file the payment tool generated locally. A 400
means the address was rejected before settlement (nothing charged); a 502 means Hyperliquid did
not answer after the payment settled, and resending the identical request with the same
PAYMENT-SIGNATURE header within 10 minutes is honored without a second charge. Companion endpoints: `/api/top-traders` ($0.05) to find candidates,
`/api/whale-positions` ($0.03) for the live book only.
