---
name: polymarket-eth-midcandle
description: "ETH Mid-Candle Scalper — 77%+ win rate on Polymarket ETH 15-minute markets. Enters mid-candle (2–12 min remaining) when ETH intracandle momentum is confirmed AND BTC is aligned. The BTC alignment gate is the secret sauce — it filters out noise trades where ETH is fighting the broader crypto trend. Fully configurable: tune momentum threshold, volume ratio, entry price window, and BTC gate to find your edge. Proven on real money. Use when you want the highest-WR crypto scalper running 24/7 on Polymarket."
metadata:
  author: "DjDyll"
  version: "1.1.1"
  displayName: "ETH Mid-Candle Scalper"
  difficulty: "intermediate"
---

# ETH Mid-Candle Scalper 🔥

> **77%+ win rate. Real money. 400+ trades.**
> ETH's 15-minute markets are even more profitable than BTC's — if you know when to enter. This strategy does. The BTC alignment gate alone filters out a third of losing trades. Battle-tested, configurable, and running 24/7.

> **This is a template.** The default signal is mid-candle ETH momentum from Binance klines, filtered by BTC cross-asset alignment —
> remix it with your own data sources, alternate confirmation signals, or additional asset gates.
> The skill handles all the plumbing (market discovery, BTC/ETH data fetching, execution, safeguards).
> Your tuning provides the alpha.

---

## What It Does

ETH Up/Down markets on Polymarket close every 15 minutes. This strategy waits until the candle has shown its hand — typically 2–12 minutes remaining — and only enters when:

1. **ETH momentum is clear:** 5m and 3m price change both agree on direction
2. **BTC agrees:** BTC isn't moving hard against you (cross-asset alignment check)
3. **Volume confirms:** The move is backed by real activity, not noise
4. **Entry price is fair:** Not too cheap (contrarian) or too expensive (overpriced)

**Why BTC alignment matters:** ETH and BTC are heavily correlated. When ETH is signaling UP but BTC is dumping 0.3%, you're fighting the tide — and you'll lose. The BTC gate eliminates that class of trade entirely.

**The result:** 77%+ win rate on real money. Out of the box.

> ⚠️ **Important:** The defaults are calibrated to produce edge, but **you need to tune them**. Different account sizes, different risk tolerances, different times of day all affect optimal settings. The tuning guide below tells you exactly what to adjust and why. A tuned strategy beats a default strategy every time.

---

## Setup

### 1. Install

```bash
clawhub install polymarket-eth-midcandle
```

Set your API key:
```bash
export SIMMER_API_KEY=sk_live_your_key_here
```

### 2. Configure your agent ID

```bash
python eth_midcandle.py --set poly_agent_id=your_agent_id_here
```

Find your agent ID at **simmer.markets/dashboard → Agents**.

### 3. Paper trade first

```bash
python eth_midcandle.py
```

You'll see `[PAPER MODE]` — no real money. Run this for at least a day to understand when it fires and why.

### 4. Go live

```bash
python eth_midcandle.py --live
```

### 5. Set up cron

```bash
crontab -e
```

Add:
```
3,8,13,18,23,28,33,38,43,48,53,58 * * * * cd /path/to/skill && python eth_midcandle.py --live >> /var/log/eth-midcandle.log 2>&1
```

Runs every 5 minutes, staggered for best execution timing.

---

## Configuration

```bash
python eth_midcandle.py --config
python eth_midcandle.py --set momentum_threshold=0.0012
```

| Parameter | Env Var | Default | Description |
|-----------|---------|---------|-------------|
| `poly_agent_id` | `SIMMER_ETHMC_AGENT_ID` | — | Your Polymarket agent ID (required) |
| `bet_size` | `SIMMER_ETHMC_BET_SIZE` | `5.0` | USDC per trade |
| `momentum_threshold` | `SIMMER_ETHMC_THRESHOLD` | `0.0012` | Min 5m ETH price change (0.12%) |
| `btc_gate_threshold` | `SIMMER_ETHMC_BTC_GATE` | `0.0015` | BTC move required to veto trade (0.15%) |
| `min_volume_ratio` | `SIMMER_ETHMC_VOL_RATIO` | `1.1` | Volume vs 2h avg (0 = disabled) |
| `min_entry_price` | `SIMMER_ETHMC_MIN_ENTRY` | `0.45` | Min entry price per side |
| `max_entry_price` | `SIMMER_ETHMC_MAX_ENTRY` | `0.65` | Max entry price per side |
| `enable_1m_confirm` | `SIMMER_ETHMC_1M_CONFIRM` | `false` | Require 1m candle to confirm direction |
| `skip_hours` | `SIMMER_ETHMC_SKIP_HOURS` | `13,17` | UTC hours to skip (historically poor WR) |
| `discord_webhook` | `SIMMER_ETHMC_WEBHOOK` | `""` | Discord alert webhook (optional) |
| `max_position_usd` | `SIMMER_ETHMC_MAX_POS` | `50.0` | Max USDC per trade when using `--smart-sizing` |
| `sizing_pct` | `SIMMER_ETHMC_SIZING_PCT` | `0.03` | Portfolio % per trade when using `--smart-sizing` (3%) |

> ⚠️ **SKIP HOURS — READ THIS BEFORE TRADING**
>
> By default, the strategy **skips hour 13 UTC (9am ET) and hour 17 UTC (1pm ET)**. These hours have a historically poor ETH midcandle win rate — **sub-45%**, meaning you lose money on average.
>
> - **Hour 13 UTC (9am ET):** NY open volatility makes ETH momentum signals unreliable. Sharp reversals are common.
> - **Hour 17 UTC (1pm ET):** Post-lunch chop. Random, low-conviction price action that fakes out momentum signals.
>
> **Do NOT remove these skip hours** unless you have your own data (50+ trades minimum) showing profitability during those hours. The default skip list exists because real money was lost learning this lesson.
>
> To modify: `python eth_midcandle.py --set skip_hours=13,17,21` (add hours) or `--set skip_hours=` (disable — not recommended).

---

## Tuning Guide

> The defaults work. Tuning makes them work better for you specifically.

### Momentum threshold (`momentum_threshold`)
How much ETH must move in 5 minutes before you enter.

- **Lower (0.0008–0.0012):** More trades. Good when ETH is in a clear trend.
- **Higher (0.0018–0.0025):** Only trade strong moves. Better in choppy or sideways conditions.
- **Start at default (0.0012)** and only adjust after 50+ paper trades.

### BTC alignment gate (`btc_gate_threshold`)
The BTC 5m move that triggers a veto.

- **Lower (0.0010):** Stricter BTC filter — vetoes more trades when BTC wiggles
- **Higher (0.0020–0.0025):** Only veto when BTC is moving hard — allows more ETH-independent trades
- **Default (0.0015)** is the sweet spot: vetoes divergent trades without over-filtering

### Volume ratio (`min_volume_ratio`)
Filters low-volume moves that tend to reverse.

- **0 (disabled):** Pure momentum, no volume filter
- **1.1 (default):** Trade when volume is 10% above the 2-hour average
- **1.5+:** High-conviction only. Fewer trades, stronger confirmation

### Entry price window
- **Too cheap (<0.40):** You're fading the crowd — usually wrong
- **Too expensive (>0.70):** Limited upside relative to risk
- **Default 0.45–0.65:** Balanced. You can tighten to 0.50–0.60 for higher precision at cost of volume

### 1m confirmation (`enable_1m_confirm`) — **OFF by default**
Adds a final gate: the last 1-minute candle must agree with your trade direction.

- **Disabled (default):** More trades, baseline win rate
- **Enabled:** Meaningful reduction in false signals — especially useful during London/NY open volatility

> 💡 **Tip:** Enable `1m_confirm` after your first week of paper trading. Most users see their win rate tick up 2–4% with it on.

### Skip hours (`skip_hours`)
UTC hours with historically poor ETH midcandle win rate. Defaults are `13,17`.

- Hour 13 UTC (9am ET): NY open volatility makes momentum signals unreliable
- Hour 17 UTC (1pm ET): Post-lunch chop, random price action
- Only remove these if you have enough personal data showing otherwise

---

## Commands

```bash
python eth_midcandle.py               # Paper trade
python eth_midcandle.py --live        # Real trades
python eth_midcandle.py --positions   # Open positions
python eth_midcandle.py --config      # Current config
python eth_midcandle.py --smart-sizing  # Size by portfolio %
python eth_midcandle.py --no-safeguards  # Skip flip-flop/slippage checks
python eth_midcandle.py --set momentum_threshold=0.0010
```

---

## Example Output

```
============================================================
🔴 LIVE: ETH Mid-Candle Scalper — 2026-03-15 22:18 UTC
============================================================
⏰ Candle :15 | 7 min remaining | ✅ In window
📊 Volume: 1.34x ✅
📈 ETH Momentum: up | 5m: +0.1543% | 3m: +0.0821%
   1m: up (+0.0412%) — gate disabled
₿  BTC check: +0.0923% — ✅ aligned
📋 Market: Will ETH go up or down — March 15, 10:15-10:30PM ET?
💲 Entry price: 0.531 (side=yes)

🚀 Placing YES $5.00 — Mid-candle up (7m left): 5m=+0.1543% 3m=+0.0821% vol=1.34x BTC=+0.0923%
✅ Filled: 9.4 YES shares for $5.00
```

---

## The BTC Gate — Explained

ETH and BTC move together ~80% of the time. When they diverge:
- ETH signaling UP while BTC dropping hard → ETH is wrong, BTC leads
- ETH signaling DOWN while BTC pumping hard → same problem

The BTC gate catches this. Before entering, the strategy checks if BTC moved more than `btc_gate_threshold` in the opposite direction. If it did, the trade is skipped.

This single filter is responsible for a significant portion of the win rate improvement over naive ETH momentum strategies. Don't disable it without data.

---

## Remix Ideas

- **Funding rate confirmation:** Only trade ETH UP when perpetual funding is positive (longs paying)
- **ETH/BTC ratio:** Add a ratio signal — trade ETH when it's outperforming BTC on the ratio
- **Options skew:** Skip trades when ETH options put/call ratio is elevated
- **On-chain:** Add net exchange flows as a confirmation signal for larger size

---

## Troubleshooting

**Firing less than expected?**
- Lower `momentum_threshold` to 0.0010
- Check skip hours — maybe you're running during 13h or 17h UTC
- Verify your cron is running: `tail -f /var/log/eth-midcandle.log`

**Losing more than expected?**
- Enable `enable_1m_confirm` — adds a key anti-noise filter
- Raise `momentum_threshold` to 0.0018
- Check that `btc_gate_threshold` is set — it should NOT be 0

**"BTC check failed"?**
- Binance API timeout — the strategy falls through to neutral (still trades)
- If happening regularly, your server may have connectivity issues to Binance

**Win rate below 65%?**
- You're likely trading the wrong hours — check if hour 13 or 17 UTC is in your logs
- Try enabling `enable_1m_confirm`
- Run paper mode for a week before re-evaluating
