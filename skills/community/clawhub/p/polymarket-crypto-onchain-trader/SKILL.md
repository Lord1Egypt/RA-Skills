---
name: polymarket-crypto-onchain-trader
description: Trades Polymarket prediction markets on Bitcoin, Ethereum, Solana price milestones, ETF inflows, halving events, and DeFi protocol milestones. Uses three stacked structural edges — ETF flow data timing, BTC halving cycle phase, and Asian regulatory session windows — to size conviction without any external API.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Crypto & On-Chain Trader
  difficulty: advanced
---

# Crypto & On-Chain Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `onchain_bias()` — three stacked structural edges, no external API required.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Crypto markets have the most sophisticated on-chain data infrastructure of any asset class — and Polymarket's retail participants almost never use it. This skill exploits three documented structural edges without any API calls:

1. **Instrument type confidence** — ETF flow data is published daily by Farside/CoinGlass before Polymarket retail reprices. Protocol upgrade dates are posted on GitHub weeks ahead. Retail prices these as uncertain when they aren't.
2. **BTC halving cycle phase** — the halving date is mathematically predictable. The post-halving price cycle (consolidation → bull → distribution → bear) is historically documented. BTC price milestone markets get conviction adjusted by current cycle position.
3. **Asian regulatory session timing** — crypto regulatory news from Korea, Japan, and China breaks during Asian business hours. Polymarket is US-dominated — repricing lags 15–30 minutes.

## Signal Logic

### Default Signal: Conviction-Based Sizing with On-Chain Bias

1. Discover active crypto markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `onchain_bias()` — three stacked layers: instrument confidence × BTC cycle phase × timing
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### On-Chain Bias (built-in, no API required)

**Layer 1 — Instrument Type Confidence**

| Instrument type | Multiplier | Why |
|---|---|---|
| Spot ETF inflows (BlackRock, Fidelity) | **1.30x** | Daily flow data (Farside/CoinGlass) published before Polymarket reprices — biggest info gap in crypto |
| BTC halving event markets | **1.25x** | Halving date is mathematically predictable (~210,000 blocks) — retail misprices near-certain events |
| Protocol upgrade / hard fork dates | **1.20x** | Ethereum EIP / Solana upgrade timelines on GitHub and core dev calls — public weeks ahead |
| DeFi TVL / protocol milestones | **1.10x** | DeFiLlama tracks TVL in real-time — "will protocol reach $X TVL" markets lag published data |
| BTC price milestones | **1.10x × cycle** | Halving cycle multiplier applied on top (see Layer 2) |
| ETH / SOL / general ATH milestones | **1.10x** | On-chain data gives partial directional edge |
| Stablecoin / crypto regulation | **1.05x** | Regulatory calendar partially predictable |
| NFT / Ordinals milestones | **0.75x** | Narrative-driven — no on-chain predictive signal |
| Memecoin / altcoin hype | **0.70x** | Pure retail sentiment — zero predictive signal, trade very small |

**Layer 2 — BTC Halving Cycle Phase (BTC price markets only)**

The Bitcoin halving (every ~210,000 blocks, ~4 years) creates a historically documented price cycle. For BTC price milestone markets, the base type confidence is multiplied by the current cycle phase:

| Phase | Days post-halving | Multiplier | Historical pattern |
|---|---|---|---|
| Early consolidation | 0–180 | **×1.05** | Miners sell, market absorbs supply shock |
| Bull phase | 181–540 | **×1.20** | Historically strongest 12-month returns |
| Distribution | 541–900 | **×1.00** | Price peaks, direction uncertain |
| Bear phase | 901+ | **×0.85** | Fade bullish BTC price targets |

Last halving: April 19, 2024 (block 840,000). Next: ~April 2028. The skill prints `btc_cycle_day=N` on startup so you always know where you are.

**Layer 3 — Asian Session Timing**

Crypto regulatory news from South Korea, Japan, and China breaks during Asian business hours. Polymarket is US-dominated:

| Condition | Multiplier |
|---|---|
| Regulatory/ban/approval question + 01:00–09:00 UTC | **1.15x** — US retail asleep, repricing lag |
| Regulatory/ban/approval question + 13:00–21:00 UTC | **0.95x** — US prime time, priced within minutes |

Combined and capped at **1.40x**. An ETF inflow market in Asian hours → 1.30 × 1.15 = **1.40x cap**. A memecoin question at any time → **0.70x** — position sized near MIN_TRADE floor.

### Keywords Monitored

```
Bitcoin, BTC, Ethereum, ETH, Solana, SOL, crypto, ETF, halving,
all-time high, ATH, $100k, $200k, stablecoin, USDC, Tether, DeFi,
Uniswap, Aave, Layer 2, Arbitrum, Base, BlackRock, spot ETF, inflows,
hash rate, mempool, TVL, total value locked, EIP, hard fork, upgrade,
Pectra, Dencun, funding rate, open interest, exchange outflow, whale, on-chain
```

### Remix Signal Ideas

- **Farside BTC ETF flows**: Replace `market.current_probability` with daily net flow implied probability — trade the divergence between institutional flow data and Polymarket retail pricing directly
- **Glassnode free tier**: SOPR, NUPL, exchange inflow/outflow — feed into `p` to trade on-chain sentiment vs market price
- **CoinGlass funding rates**: Extreme positive funding = leveraged longs = squeeze risk → fade YES on price targets; extreme negative → fade NO
- **DeFiLlama API**: Real-time TVL for any protocol — compare to market-priced threshold for TVL milestone markets


## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `35` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `15000` | Min market volume filter (USD) — crypto needs liquidity |
| `SIMMER_MAX_SPREAD` | `0.06` | Max bid-ask spread (6%) — tighter than other traders |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution — crypto moves faster |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
