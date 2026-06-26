---
name: kalshi-trader
description: Automated Kalshi prediction market trading bot. Sets up a fully automated trading system that scans markets every 15 minutes, researches opportunities using direct web fetches, places trades based on strict EV IRR and half Kelly criteria, monitors positions, and sends daily Telegram summaries. Use when a user wants to automate Kalshi trading, set up a prediction market bot, configure market scanning, or get daily P&L reports from Kalshi.
---

# Kalshi Trader

Automated prediction market trading on Kalshi. Scans every 15 minutes, researches before every trade, reports daily via Telegram.

## Setup (run once)

### 1. Install dependencies
```bash
pip install cryptography requests --break-system-packages
```

### 2. Store Kalshi credentials
```bash
mkdir -p ~/.kalshi && chmod 700 ~/.kalshi
nano ~/.kalshi/private_key.pem   # paste -----BEGIN RSA PRIVATE KEY----- block
chmod 600 ~/.kalshi/private_key.pem
echo "YOUR-API-KEY-ID-HERE" > ~/.kalshi/key_id.txt
chmod 600 ~/.kalshi/key_id.txt
```

Get your API key at: kalshi.com → Settings → API → Create Key

### 3. Deploy the bot
```bash
cp scripts/kalshi_bot.py ~/kalshi_bot.py
chmod 600 ~/kalshi_bot.py
```

### 4. Test connection
```bash
python3 ~/kalshi_bot.py test
```

### 5. Set up cron jobs (via OpenClaw cron tool)

**15-minute scan** (silent unless trade placed or exited):
- Schedule: `*/15 * * * *`
- Message: see references/cron-prompt.md

**Daily summary** (9am your timezone):
- Schedule: `0 9 * * *` with your timezone
- Message: "Run `python3 ~/kalshi_bot.py summary` and send daily trading report with balance, open positions, recent trades, P&L, and fees paid."

## Trading Rules

### Entry criteria
Only place a trade if **EV IRR ≥ 50%** (post-fee):
```
edge = fair_value - (market_price + entry_fee)
EV IRR = (edge / (market_price + entry_fee)) × (365 / days_to_close)
```
Minimum: EV IRR ≥ 0.50 (50%)

### Position sizing — Half Kelly
```
kelly_fraction = (edge / market_price) × 0.5
max_position = min(kelly_fraction × balance, 0.20 × balance)
contracts = floor(max_position / market_price)
```

### Exit rule
**Exit ONLY if current bid ≥ fair value estimate (net of exit fee).**
- Never use price-based stop losses — prediction markets resolve on facts, not on what other traders think
- If price drops, research whether the underlying facts changed
- Only exit early if: (a) price reached fair value, or (b) new evidence shows the outcome is unlikely

### Research approach
Use `web_fetch` as primary research tool (no quota limits). Known data sources:
- Gas prices: `https://gasprices.aaa.com/`
- Trump actions: `https://www.whitehouse.gov/presidential-actions/`
- Treasury yields: `https://home.treasury.gov/resource-center/data-chart-center/interest-rates/`
- Bitcoin/crypto: `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd`
- Weather: `https://wttr.in/CityName?format=3`
- Congress bills: `https://www.congress.gov`

Only use `web_search` for open-ended research where the URL isn't known upfront.

## Bot Commands

```bash
python3 ~/kalshi_bot.py          # scan for opportunities
python3 ~/kalshi_bot.py summary  # print P&L summary  
python3 ~/kalshi_bot.py test     # verify API connection
```

## Reporting format (include in every update)

- 💰 Cash balance
- 📦 Total position cost
- 📈 Current market value of positions
- 💹 Unrealized P&L
- 💸 Total Kalshi fees paid
- 🏦 Total portfolio value

## API reference

See references/api.md for Kalshi authentication and endpoints.

## Trade research workflow

See references/trade-research.md for finding and evaluating opportunities.
