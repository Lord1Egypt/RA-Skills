---
name: polymarket-sol-momentum
description: Trades Polymarket crypto prediction markets (Solana, Bitcoin, Ethereum) using CoinGecko momentum signals. Buys YES when bullish markets are underpriced vs price trend, NO when overpriced. Runs on Simmer with built-in context checks for flip-flop detection and slippage. Use when trading crypto prediction markets based on price momentum.
metadata:
  author: ComputerByPerplexity
  version: '1.0.0'
  displayName: SOL/Crypto Momentum Trader
  difficulty: intermediate
  category: trading
  venue: polymarket
---

# SOL/Crypto Momentum Trader 🔮

Scans Polymarket for Solana, Bitcoin, and Ethereum prediction markets where the current market price diverges from CoinGecko momentum signals — and trades the gap.

> **This is a template.** The default signal is CoinGecko 24h/7d price change — remix it with your own price feed, CEX funding rates, on-chain data, or any directional signal. The skill handles all the plumbing (market discovery, edge scoring, context checks, trade execution). Your agent provides the alpha.

---

## Strategy

1. Fetch 24h and 7d price change for SOL, BTC, ETH from CoinGecko (free, no API key needed)
2. Compute a directional momentum signal: weighted blend of 24h (60%) and 7d (40%) change, normalized to ±1 at ±20% move
3. Scan active Polymarket markets matching `solana`, `bitcoin`, `ethereum`, `crypto`
4. Detect whether each market's question is bullish or bearish framing
5. Score divergence: `edge = |expected_prob − market_prob|`
6. Buy `YES` or `NO` on markets where edge exceeds threshold (default 8%)
7. Check Simmer context before each trade — skip on flip-flop warnings, high slippage, or HOLD recommendation
8. Tag all trades with `skill_slug` for per-skill volume attribution on Simmer

---

## Requirements

- `SIMMER_API_KEY` — your Simmer agent API key
- `simmer-sdk` — installed via pip (see `clawhub.json`)
- `requests` — for CoinGecko API calls
- No CoinGecko API key needed (free public endpoint)

---

## Configuration

All config via environment variables — no code edits needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `SIMMER_API_KEY` | required | Your Simmer agent API key |
| `TRADING_VENUE` | `sim` | `sim` (paper), `polymarket` (real USDC), `kalshi` (real USD) |
| `TRADE_AMOUNT_USD` | `10.0` | USD per trade |
| `DIVERGENCE_THRESHOLD` | `0.08` | Min edge to trade (8% = 0.08) |
| `MAX_TRADES_PER_RUN` | `3` | Max trades per cron cycle |

---

## Running

```bash
# Install dependencies
pip install simmer-sdk requests

# Dry run (default — no real trades)
python strategy.py

# Live trading
python strategy.py --live
```

The script defaults to dry-run mode. Pass `--live` explicitly to execute real trades. When run via ClawHub automaton, set `TRADING_VENUE=polymarket` (or `sim`) in your environment — the `--live` flag is handled automatically by the automaton entrypoint.

---

## Remix Ideas

**Swap the signal source:**
- Replace CoinGecko with Binance/Bybit REST API for real-time price + funding rate
- Use on-chain Solana data (epoch rewards, validator stake changes) as a signal
- Pull sentiment from Twitter/Reddit via a simple keyword count API

**Tune the strategy:**
- Lower `DIVERGENCE_THRESHOLD` to 5% to trade more aggressively
- Increase `TRADE_AMOUNT_USD` once you've validated edge on Simmer ($SIM)
- Add a volume filter to skip illiquid markets

**Extend asset coverage:**
- Add `"sui"`, `"bnb"`, `"matic"` to the `COINGECKO_IDS` mapping
- Point at Kalshi crypto markets: set `venue="kalshi"` and import markets first

**Layer signals:**
- Run the script twice per cycle with different signals, average the outputs
- Add a momentum confirmation filter (only trade if 1h and 24h align)

---

## Safety Rails

Built-in safeguards (via Simmer context endpoint):
- **Flip-flop detection** — skips markets where your agent has been reversing positions
- **Slippage check** — skips markets where estimated slippage > 15%
- **Edge analysis** — respects `HOLD` recommendations from Simmer's context engine
- **Simmer default limits** — $100/trade, $500/day, 50 trades/day (configurable via dashboard)

---

## Volume Attribution

All trades are tagged with `source="sdk:polymarket-sol-momentum"` and `skill_slug="polymarket-sol-momentum"`. This attributes trade volume to this skill on Simmer and qualifies for the 2% creator fee on LMSR markets you've imported.

---

## Links

- [Simmer docs](https://docs.simmer.markets)
- [CoinGecko free API](https://www.coingecko.com/en/api/documentation)
- [Polymarket](https://polymarket.com)
- [Simmer skill building guide](https://docs.simmer.markets/skills/building)
