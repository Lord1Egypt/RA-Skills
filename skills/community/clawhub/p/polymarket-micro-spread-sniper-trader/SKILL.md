---
name: polymarket-micro-spread-sniper-trader
description: Scans all Polymarket categories for tight spreads (<= 8%) combined with extreme probabilities (<= 15% or >= 85%), placing many tiny conviction-based micro bets on near-certain outcomes.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Micro Spread Sniper Trader
  difficulty: advanced
---

# Micro Spread Sniper Trader

> **This is a template.**
> The default signal is purely price-based with a strict spread filter -- no external API required. The skill discovers markets via keyword sweep (Bitcoin Up or Down, Ethereum Up or Down, Solana Up or Down, XRP Up or Down) plus a direct `get_markets(limit=100)` scan, identifies extreme probabilities where the bid-ask spread is unusually tight, and places micro-sized bets on the near-certain outcome.
> The skill handles all the plumbing (market discovery, spread filtering, volume gating, conviction sizing, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists markets across many categories. Some of these markets reach extreme probabilities (>= 80% or <= 8%) where the outcome is near-certain. The key insight: when a market also has a tight bid-ask spread (<= 8%), it means the market maker is confident in the direction and is pricing it efficiently. Wide spreads at extreme prices signal uncertainty; tight spreads signal conviction.

The skill scans for markets matching this microstructure signal using 4 keywords (Bitcoin Up or Down, Ethereum Up or Down, Solana Up or Down, XRP Up or Down) plus `get_fast_markets()` and `get_markets(limit=100)` fallback. It applies three gates: spread <= 8% (MAX_SPREAD=0.08), probability outside the 8%/80% bands (YES_THRESHOLD=0.08, NO_THRESHOLD=0.80), and volume >= $500 (MIN_VOLUME=500). Trades that pass all gates get conviction-based sizing from $2 to $10 across up to 20 concurrent micro positions.

Example: A market at p=88% with spread=5%. Spread passes (5% <= 8%). Probability passes (88% >= 80%). Conviction = (0.88 - 0.80) / (1 - 0.80) = 0.40. Size = max($2, 0.40 * $10) = $4. The skill sells NO at $4 -- backing the near-certain YES resolution.

## Edge

Tight spread + extreme probability is a market microstructure signal. A market at 90% with a 10% spread means the market maker is uncertain -- the wide spread compensates for directional risk. A market at 90% with a 5% spread means the market maker is confident and willing to offer tight pricing. The tight spread acts as a quality filter separating genuinely near-certain outcomes from noisy extreme prices in illiquid markets.

Two trade types exploit this:
- **Sell NO (p >= 80%)**: Back the near-certain YES resolution. High win rate, small profit per trade. This is the primary mode.
- **Buy YES (p <= 8%)**: Rare extreme longshot micro-bet. Very low win rate but payout is 10x+ when it hits. Only triggers at very extreme probabilities.

The portfolio is heavily weighted toward the near-certainty side (high hit rate, consistent small profits). Longshot exposure is minimal (p must be below 8%) to avoid systematic losses from betting on unlikely outcomes.

## Signal Logic

1. Discover active markets via keyword sweep across 4 terms (Bitcoin Up or Down, Ethereum Up or Down, Solana Up or Down, XRP Up or Down) plus `get_markets(limit=100)` fallback, deduplicated by market id
2. **Spread gate**: reject if `spread > MAX_SPREAD` (0.08 = 8%)
3. **Days gate**: reject if days to resolution < `MIN_DAYS` (0)
4. **Volume gate**: reject if volume < `MIN_VOLUME` ($500)
5. If `p <= YES_THRESHOLD` (0.08): buy YES -- conviction = `(0.08 - p) / 0.08`, size = `max($2, conviction * $10)`
6. If `p >= NO_THRESHOLD` (0.80): sell NO -- conviction = `(p - 0.80) / (1 - 0.80)`, size = `max($2, conviction * $10)`
7. Otherwise neutral -- skip
8. Place up to `MAX_POSITIONS` (20) micro trades per run

### Remix Signal Ideas

- **Multi-timeframe spread check**: Verify the spread has been tight for the last N hours, not just a momentary blip -- use historical orderbook snapshots if available
- **Category weighting**: Some categories (sports with known outcomes, crypto price milestones already passed) resolve more predictably at extremes -- weight conviction by category
- **Spread trend filter**: If spread is tightening over time at extreme probability, it signals increasing market maker confidence -- boost conviction
- **Correlation clustering**: When multiple related markets all show tight-spread extremes pointing the same direction, conviction should be higher
- **Time-of-day filter**: Spreads tend to be tighter during peak trading hours -- prefer trades placed when liquidity is naturally high

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `10` | Max USDC per micro trade (ceiling at 100% conviction) |
| `SIMMER_MIN_TRADE` | `2` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) -- the sniper's core filter |
| `SIMMER_MAX_POSITIONS` | `20` | Max concurrent micro positions |
| `SIMMER_NO_THRESHOLD` | `0.80` | Sell NO when market probability >= this (extreme high) |
| `SIMMER_YES_THRESHOLD` | `0.00` | YES longshot threshold (0 = disabled, NO-mode only) |
| `SIMMER_MIN_VOLUME` | `500` | Min market volume -- ensures spread is meaningful |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow imminent markets) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
