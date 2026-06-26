---
name: google-finance
description: "Track stock prices and company news from Google Finance on a schedule. Use when user wants to monitor stocks, get buy/sell recommendations, check price changes, follow company news, set up stock alerts, or track portfolio symbols. Triggers: 'track stock', 'watch AAPL', 'stock alert', 'buy or sell', 'stock news', 'Google Finance'. Default watchlist: NVDA, AAPL, META, GOOGL."
homepage: https://finance.google.com
user-invocable: true
metadata: {"clawdbot": {"emoji": "📈", "requires": {"bins": ["python3"]}, "os": ["darwin", "linux", "win32"], "files": ["scripts/parse-stock.py"]}}
---

# Stock Tracker

Monitor stocks, generate buy/sell signals, and track your portfolio.

## Quick Start

**Check all watched stocks (auto-fetches data):**
```bash
python3 {baseDir}/scripts/parse-stock.py --check --summary
```

**Check single stock:**
```bash
python3 {baseDir}/scripts/parse-stock.py --check --symbol AAPL
```

**Add/remove stocks:**
```bash
python3 {baseDir}/scripts/parse-stock.py --add TSLA
python3 {baseDir}/scripts/parse-stock.py --remove TSLA
```

**Show watchlist:**
```bash
python3 {baseDir}/scripts/parse-stock.py --list
```

---

## How It Works

The `parse-stock.py` script handles everything:

1. **Fetches data** from Google Finance (no API key required!)
2. **Calculates scores** based on momentum, volume, valuation
3. **Generates signals** (BUY / HOLD / SELL)
4. **Updates state** in `~/.openclaw/workspace/stock-tracker-state.json`

### Analysis Framework

Apply the scoring framework in `{baseDir}/references/analysis-framework.md` to produce:

```
Symbol: AAPL
Price: $182.30  (+1.4% today)
Signal: BUY  [score: +6/10]
Confidence: MEDIUM

Key factors:
  ✅ Price above 50-day SMA (estimated)
  ✅ Volume 1.3× above average
  ✅ 2 positive news items in past 24h
  ⚠️  P/E 28.5 — elevated but within sector norm
  ❌ Within 3% of 52-week high (limited upside)

Recent headlines:
  • "Apple reportedly in talks with..." — Reuters (2h ago)
  • "iPhone sales beat estimates..." — Bloomberg (5h ago)

Recommendation: Consider buying on dips. Set stop-loss at 5% below current price.
```

### 4. Persist State

Store watchlist and last-seen prices in `~/.openclaw/workspace/stock-tracker-state.json`.

**Default watchlist** (pre-loaded on first run if state file does not exist):
- `NVDA:NASDAQ` — NVIDIA
- `AAPL:NASDAQ` — Apple
- `META:NASDAQ` — Meta Platforms
- `GOOGL:NASDAQ` — Alphabet (Google)

Format:
```json
{
  "watchlist": ["NVDA:NASDAQ", "AAPL:NASDAQ", "META:NASDAQ", "GOOGL:NASDAQ"],
  "lastChecked": "2026-03-03T09:00:00Z",
  "snapshots": {
    "NVDA:NASDAQ": { "price": 875.40, "change_pct": 2.1, "ts": "2026-03-03T09:00:00Z" },
    "AAPL:NASDAQ": { "price": 182.30, "change_pct": 1.4, "ts": "2026-03-03T09:00:00Z" },
    "META:NASDAQ": { "price": 512.60, "change_pct": -0.8, "ts": "2026-03-03T09:00:00Z" },
    "GOOGL:NASDAQ": { "price": 175.20, "change_pct": 0.5, "ts": "2026-03-03T09:00:00Z" }
  }
}
```

Load state at the start of every run. Compare new price against `snapshots` to compute Δ since last check.

### 5. Alert on Significant Moves

Emit a highlighted alert if any of the following thresholds are crossed:
- Price change > ±3% since last check
- Volume > 2× 30-day average
- Any headline contains keywords: `earnings`, `merger`, `acquisition`, `SEC`, `lawsuit`, `recall`, `CEO`, `bankruptcy`

---

## Setting Up a Cron Schedule

Run the following to add a recurring job that checks stocks every weekday at market open (09:30 ET) and close (16:00 ET):

```bash
# Market open — 09:30 ET (UTC-4 during EDT)
openclaw cron add \
  --name "Stock Open Check" \
  --cron "30 13 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /stock-tracker check and output a full report with buy/sell signals for all watched stocks." \
  --announce \
  --channel slack \
  --to "channel:REPLACE_WITH_CHANNEL_ID"

# Market close — 16:00 ET
openclaw cron add \
  --name "Stock Close Check" \
  --cron "0 20 * * 1-5" \
  --tz "America/New_York" \
  --session isolated \
  --message "Run /stock-tracker check and output end-of-day summary with buy/sell signals for all watched stocks." \
  --announce
```

For a simpler every-4-hours check (including after-hours):
```bash
openclaw cron add \
  --name "Stock Tracker" \
  --every 14400000 \
  --session isolated \
  --message "Run /stock-tracker check for all watched symbols. Report price changes > 1%, news, and signals."
```

See `{baseDir}/references/data-sources.md` for timezone and exchange hours reference.

---

## Output Format Rules

- Always show: symbol, price, change %, signal, top 3 headlines
- If multiple stocks: group by signal (BUY first, then HOLD, then SELL)
- Use emoji prefix: 🟢 BUY / 🟡 HOLD / 🔴 SELL
- Append `⚠️ ALERT` to any symbol that crossed a threshold
- End every report with a disclaimer: *"This is not financial advice. Data sourced from Google Finance."*

---

## Limitations & Notes

- Google Finance does not provide real-time Level 2 data; prices may be 15 min delayed for some exchanges.
- This skill cannot execute trades. Recommendations are informational only.
- For non-US stocks, use the exchange suffix (e.g. `0700.HK`, `7203.T`, `BABA.N`). See data-sources.md for the full mapping.
- If Google Finance blocks the browser session, fall back to Yahoo Finance scraping as described in data-sources.md.

---

## External Endpoints

This skill makes outbound requests to the following public URLs only:

| URL | Purpose |
|-----|---------|
| `https://www.google.com/finance/quote/*` | Stock price & stats |

No user data, credentials, or personal information is sent to any external endpoint.

---

## Security & Privacy

- **No credentials required.** All data is fetched from public Google Finance pages.
- **Local state only.** The watchlist and price snapshots are stored exclusively at `~/.openclaw/workspace/stock-tracker-state.json` on your machine. Nothing is sent to remote servers.
- **No browser required.** Data is fetched via HTTP requests and parsed from HTML. No JavaScript execution.
- **`parse-stock.py` is sandboxed.** It reads/writes only the state file at the path above. It does not access environment variables or other files.
- **Buy/sell signals are heuristic only.** No financial data or decisions are transmitted anywhere. All analysis runs locally.
