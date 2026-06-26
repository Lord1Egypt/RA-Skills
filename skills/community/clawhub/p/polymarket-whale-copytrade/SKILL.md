---
name: polymarket-copytrading
description: Mirror high-performing whale wallets on Polymarket. Monitors configured wallet addresses for recent trades above a size threshold and copies them automatically. Runs on Simmer with context safeguards, flip-flop detection, and slippage checks. Use when the user wants to copytrade whales, mirror wallets, follow smart money, or automate position copying on prediction markets.
metadata:
  author: ComputerByPerplexity
  version: '1.0.0'
  displayName: Polymarket Whale Copytrader
  difficulty: intermediate
  category: trading
  venue: polymarket
---

# Polymarket Whale Copytrader 🐋

Monitors a configurable list of high-performing Polymarket wallets and mirrors their recent trades — automatically.

> **This is a template.** The default signal is on-chain trade activity from configured whale wallets. Remix it by swapping in your own wallet list, adding a Polymarket leaderboard scraper to auto-discover top traders, or layering a volume filter to only copy their highest-conviction trades. The skill handles all the plumbing (trade detection, market resolution, deduplication, safeguards). You provide the wallets.

---

## Strategy

1. Every 15 minutes, scan configured whale wallets via the Polymarket CLOB API
2. Filter trades to the last `lookback_minutes` window (default: 30 min)
3. Skip trades below `min_whale_trade_usd` (default: $500) — only copy high-conviction moves
4. Resolve the Polymarket token ID to a Simmer market (searches by question, imports if needed)
5. Skip markets you already hold — no doubling up
6. Check Simmer context: skip on flip-flop warnings, high slippage, resolved markets
7. Mirror the trade with your configured position size
8. Tag all trades for per-skill volume attribution on Simmer

---

## Requirements

- `SIMMER_API_KEY` — your Simmer agent API key
- `simmer-sdk` — installed via pip
- No additional API keys needed (uses Polymarket's public CLOB + Gamma APIs)

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SIMMER_API_KEY` | required | Your Simmer API key |
| `TRADING_VENUE` | `polymarket` | `sim`, `polymarket`, or `kalshi` |
| `SIMMER_COPYTRADE_WALLETS` | built-in list | Comma-separated wallet addresses to track |
| `SIMMER_COPYTRADE_MAX_POSITION` | `10.0` | Max USD per copied trade |
| `SIMMER_COPYTRADE_MAX_TRADES` | `5` | Max trades per cron run |
| `SIMMER_COPYTRADE_LOOKBACK_MINS` | `30` | Minutes of trade history to scan |
| `SIMMER_COPYTRADE_MIN_TRADE` | `500` | Min USD value of whale trade to copy |
| `SIMMER_COPYTRADE_SIZING_PCT` | `0.05` | Portfolio % for smart sizing |
| `SIMMER_COPYTRADE_SKIP_PAID` | `true` | Skip markets with 10% taker fee |

**Set via CLI:**
```bash
python copytrading.py --set max_position_usd=25
python copytrading.py --set lookback_minutes=60
```

---

## Usage

```bash
# Install
pip install simmer-sdk

# See which wallets you're tracking + their stats
python copytrading.py --whales

# Dry run (default — no real trades)
python copytrading.py

# Live trading
python copytrading.py --live

# Portfolio-based position sizing (5% of balance per trade)
python copytrading.py --live --smart-sizing

# Show open positions
python copytrading.py --positions

# Show config
python copytrading.py --config
```

---

## Customizing Whale Wallets

The default list includes known high-volume Polymarket traders. To use your own:

```bash
export SIMMER_COPYTRADE_WALLETS="0xABC...,0xDEF...,0x123..."
```

**Finding good wallets:**
- [Polymarket leaderboard](https://polymarket.com/leaderboard) — filter by profit, not volume
- [Polymarket CLOB API](https://docs.polymarket.com) — query top traders programmatically
- Follow wallets that show consistent profit over 3+ months, not just one big win

**What makes a good whale to copy:**
- High win rate (>55%) across diverse markets, not just one category
- Trades early — not right before resolution
- Position sizes suggest conviction, not randomness

---

## Remix Ideas

**Auto-discover top wallets:**
- Query `https://gamma-api.polymarket.com/leaderboard` to dynamically update `WHALE_WALLETS`
- Rank by 30-day P&L, take the top 10, refresh weekly

**Filter by category:**
- Only copy trades in crypto, politics, or sports markets
- Add a keyword filter to `fetch_whale_recent_trades()`

**Conviction sizing:**
- Scale your copy size proportionally to the whale's position size
- If whale bets $5k, bet 1% of that ($50)

**Sentiment confirmation:**
- Only copy a whale trade if 2+ whales made the same move in the same window
- Reduces noise from individual whale mistakes

**Exit mirroring:**
- Detect when a whale exits a position and mirror the sell
- Currently the skill copies entries only; exits rely on Simmer's auto stop-loss (50%)

---

## Safety Rails

- **Flip-flop detection** — skips markets where you've been reversing
- **Slippage check** — skips illiquid markets (>15% estimated slippage)
- **Deduplication** — never copies the same market twice in one run
- **Position check** — skips markets you already hold
- **Paid market filter** — optionally skips markets with 10% taker fee
- **Simmer default limits** — $100/trade, $500/day, 50 trades/day (configurable via dashboard)
- **Dry run default** — real trades require explicit `--live`

---

## Links

- [Simmer docs](https://docs.simmer.markets)
- [Polymarket](https://polymarket.com)
- [Polymarket CLOB API](https://docs.polymarket.com)
- [Simmer skill building guide](https://docs.simmer.markets/skills/building)
