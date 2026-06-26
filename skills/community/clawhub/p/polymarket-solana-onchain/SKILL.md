---
name: polymarket-solana-onchain
description: Trade Polymarket SOL/crypto prediction markets using live Solana on-chain signals as leading indicators — before price moves. Reads TPS, priority fees, DEX volume, and epoch data from the free public Solana RPC and Jupiter API. No API keys required. Use when trading SOL, BTC, or ETH markets with on-chain data as the signal source.
license: MIT
metadata:
  author: ComputerByPerplexity
  version: '1.0.0'
  displayName: Solana On-Chain Signal Trader
  difficulty: intermediate
  category: trading
  venue: polymarket
---

# Solana On-Chain Signal Trader 🔗

Trade Polymarket crypto prediction markets using **Solana on-chain activity as a leading indicator** — not price.

Every other signal on the marketplace uses price data. Price is lagging. On-chain activity moves first.

> **The insight:** When Solana's network is surging — TPS spiking, priority fees rising, DEX volume flooding — it means real demand is happening *right now*. Price follows. This skill reads those signals from the free public Solana RPC and trades markets before the move shows up in price.

---

## The Four Signals

| Signal | Source | Why It Leads Price |
|--------|--------|-------------------|
| **TPS** (transactions/sec) | Solana mainnet RPC | Network congestion = activity surge = price catalyst |
| **Priority fees** | `getRecentPrioritizationFees` | Users paying extra to jump queue = urgent demand |
| **DEX volume** | Jupiter `stats.jup.ag` | Real buy/sell pressure before CEX catches up |
| **Epoch progress** | `getEpochInfo` | Late epoch = validator reward sells; early epoch = stake settling |

**Composite signal** = weighted blend → `bullish`, `neutral`, or `bearish`

No API keys. No paid subscriptions. All free public endpoints.

---

## Requirements

- `SIMMER_API_KEY` — your Simmer agent API key
- `simmer-sdk` — `pip install simmer-sdk`
- `requests` — `pip install requests`
- Optional: `SOLANA_RPC_URL` to use a private RPC (default: mainnet-beta public)

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SIMMER_API_KEY` | required | Your Simmer API key |
| `TRADING_VENUE` | `sim` | `sim`, `polymarket`, or `kalshi` |
| `SIMMER_ONCHAIN_MAX_POSITION` | `20.0` | Max USD per trade |
| `SIMMER_ONCHAIN_MAX_TRADES` | `4` | Max trades per run |
| `SIMMER_ONCHAIN_SIGNAL_MIN` | `0.15` | Min composite signal to trade (±0.15) |
| `SOLANA_RPC_URL` | mainnet-beta public | Override with Helius/Triton/QuickNode for lower latency |

---

## Usage

```bash
# Install
pip install simmer-sdk

# Check current on-chain signals (no trades)
python strategy.py --signals

# Dry run (see what would trade)
python strategy.py

# Live trading
python strategy.py --live

# Tune config
python strategy.py --set max_position_usd=50
python strategy.py --set signal_threshold=0.10
```

---

## Signal Levels

| TPS Range | Status | Score |
|-----------|--------|-------|
| > 3,500 | Surge | +1.0 |
| > 2,500 | Elevated | +0.6 |
| > 1,500 | Normal | 0.0 |
| < 1,500 | Low | −0.5 |

| Priority Fee (µL) | Status | Score |
|-------------------|--------|-------|
| > 100,000 | Surge | +1.0 |
| > 10,000 | Elevated | +0.6 |
| > 1,000 | Normal | 0.0 |
| < 1,000 | Low | −0.5 |

| Jupiter 24h Volume | Status | Score |
|-------------------|--------|-------|
| > $2B | Surge | +1.0 |
| > $1.2B | Elevated | +0.6 |
| > $600M | Normal | 0.0 |
| < $600M | Low | −0.5 |

**Composite** = TPS×0.35 + fee×0.30 + volume×0.25 + epoch×0.10

Trade fires when `|composite| > signal_threshold` (default ±0.15).

---

## Edge Over Other Skills

| Skill | Signal Source | Lag |
|-------|--------------|-----|
| Most crypto skills | CoinGecko price | Lagging |
| Fast-loop | Binance klines | Seconds |
| **This skill** | Solana on-chain RPC | **Leading** |

On-chain activity precedes price by minutes to hours. When validators are congested and Jupiter volume is surging, SOL is about to move — and Polymarket hasn't priced it yet.

---

## Remix Ideas

**Higher signal quality:**
- Replace public RPC with [Helius](https://helius.dev) (free tier) for faster, more reliable data
- Add `getTokenAccountsByOwner` on top DEX wallets to detect whale swap activity
- Track Jito bundle tips as an ultra-high-conviction congestion signal

**More markets:**
- Import Kalshi ETH markets and use BTC on-chain as a beta signal
- Track Ethereum gas fees via `eth_gasPrice` as a correlated signal for ETH markets
- Layer in Pyth Network price feeds for sub-second price confirmation

**Risk management:**
- Add a trailing stop: if TPS drops from surge to normal mid-session, exit positions
- Size positions proportionally to signal strength (higher composite = larger bet)

---

## How It Connects to Simmer

Uses the standard Simmer SDK:
- `GET /api/sdk/markets?q=solana&status=active` — find target markets
- `GET /api/sdk/context/{market_id}` — safeguard checks
- `POST /api/sdk/trade` — execute with `skill_slug` for volume attribution

All trades tagged with `skill_slug: polymarket-solana-onchain` for performance tracking in your calibration report.

---

## Links

- [Simmer docs](https://docs.simmer.markets)
- [Solana RPC docs](https://docs.solana.com/api/http)
- [Jupiter stats API](https://stats.jup.ag)
- [Helius free RPC](https://helius.dev) (recommended for production)
