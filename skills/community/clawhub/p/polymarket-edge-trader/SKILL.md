---
name: polymarket-edge-trader
description: Trades the highest-edge active AION Polymarket market matching a query using a user-supplied fair probability, AION context safeguards, and Kelly-style sizing.
metadata:
  author: "GitHub Copilot"
  version: "2.0.0"
  displayName: "Polymarket Edge Trader"
  difficulty: "intermediate"
---

# Polymarket Edge Trader

> **This is a template.** The default signal is a user-supplied fair YES probability for markets matching `MARKET_QUERY` —
> remix it with your own model output, external API, or ML prediction.
> The skill handles all the plumbing: market discovery, context safeguards, position sizing, trade execution,
> operator summaries, auto-redemption, and AION trade tagging. Your job is to provide the alpha.

## Setup

Install the AION SDK:

```bash
pip install aionmarket-sdk
```

## Key Safeguards (Built-In)

- **Risk Alerts Guard**: Skips new entries if briefing reports active risk alerts; runs de-risk logic instead.
- **Flip-Flop Detection**: Rejects markets with excessive trading reversals or discipline warnings from context.
- **Slippage Enforcement**: Enforces maximum estimated slippage threshold before showing candidates.
- **Market Context Check**: Fetches warnings, edge analysis, and trading discipline from AION API; skips if risk detected.
- **Kelly Sizing**: Uses Kelly-fraction bankroll model with configurable multiplier (`AION_KELLY_MULTIPLIER`) for position control.
- **Auto-Redeem**: Automatically claims payouts from resolved markets at each cycle start.
- **Dry-Run Default**: Only submits live orders when `--live` is explicitly passed with signed order payload.
- **Public Reasoning**: Every trade includes reasoning tied to edge signal, market state, and risk metrics.
- **Jitter Polling**: Daemon mode (`--daemon`) uses randomized wait intervals to avoid synchronized order bursts.

## What It Does

- Scans active AION Polymarket markets matching `MARKET_QUERY`
- Scores each candidate against `MODEL_PROBABILITY`
- Picks the market with the largest absolute edge
- Skips trades when edge is too small, slippage is too high, briefing risk alerts are active, or AION warns about flip-flopping
- Sizes the position with a Kelly-style bankroll model
- Prints an operator summary with risk state, decisions, and order updates
- Executes through `AionMarketClient.trade()` when you explicitly provide `--live` and a signed order payload

## Defaults

- `MARKET_QUERY=bitcoin`
- `MODEL_PROBABILITY=0.60`
- `TARGET_VENUE=polymarket`
- `MAX_MARKETS=25`
- `MAX_STAKE_USD=50`
- `MIN_EDGE=0.03`
- `MAX_SLIPPAGE_PCT=0.15`
- `STARTING_BALANCE_USD=1000`
- `AION_BASE_URL=https://pm-t1.bxingupdate.com/bvapi`
- `AION_KELLY_MULTIPLIER=0.25`
- `AION_MIN_EV=0.03`
- `WALLET_ADDRESS=`
- `AION_SIGNED_ORDER_JSON=`

## How To Run

Dry-run mode (default — no orders submitted):

```bash
python edge_trader.py
```

Scan a different market with custom probability:

```bash
python edge_trader.py --query "fed" --probability 0.64
```

Show ranked candidates before selecting best:

```bash
python edge_trader.py --show-candidates
```

Daemon mode with jitter (for cron/automaton orchestration):

```bash
python edge_trader.py --daemon --poll-interval 60
```

Live trading (requires `--live`, wallet address, and pre-signed order JSON):

```bash
WALLET_ADDRESS=0xYourWallet \
AION_SIGNED_ORDER_JSON='{"maker":"...","signer":"...","taker":"0x0000000000000000000000000000000000000000","tokenId":"...","makerAmount":"...","takerAmount":"...","side":"BUY","expiration":"...","signature":"...","salt":"...","signatureType":0,"nonce":"...","feeRateBps":"0"}' \
python edge_trader.py --query "bitcoin" --probability 0.58 --live
```

## Required Credentials

- `AION_API_KEY` is always required
- `WALLET_PRIVATE_KEY` is optional and only needed for self-custody Polymarket trading
- `WALLET_ADDRESS` is required for user-scoped briefing and live order submission
- `AION_SIGNED_ORDER_JSON` is only required for live order submission, because the AION SDK expects a complete signed order payload

## Remix Ideas

The skill's plumbing is fixed (safeguards, sizing, execution, summaries). Your alpha is:

**Signal replacement:**
- Replace `MODEL_PROBABILITY` with your own ML model output, external API call, or ensemble forecast.
- Swap `discover_markets()` for `briefing.opportunityMarkets` (pre-curated high-quality markets).
- Integrate a multi-model ensemble: call multiple probability endpoints and aggregate them.
- Use sentiment analysis, weather data, or on-chain metrics to derive fair probability.

**Advanced position management:**
- Add sell logic: close existing positions when signal flips.
- Implement rebalance logic around target portfolio weights.
- Use `get_bankroll()` to scale position size dynamically with account growth.
- Add staggered entry: split Kelly fraction across multiple limit orders at different prices.

**Extended safeguards:**
- Tighten `MIN_EDGE` for high-frequency strategies; relax for lower-frequency.
- Add custom risk filters: skip markets with high volatility, thin liquidity, or specific conditions.
- Extend auto-redeem to other venues (Kalshi, etc.) by removing venue checks.
- Integrate external alerts: pause trading if certain conditions are met from other systems.

**Operational tweaks:**
- Adjust `AION_KELLY_MULTIPLIER` for more conservative or aggressive sizing.
- Use `--max-slippage-pct` and `MAX_STAKE_USD` as dynamic parameters from a config file.
- Add custom telemetry: log trade decisions to your own database or reporting system.
- Build a CLI wrapper that spins up multiple skill instances with different queries.