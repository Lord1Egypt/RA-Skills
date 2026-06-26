---
name: option_whales
description: Query real-time option flow intelligence and generate AI-powered trade analysis reports. Use when users ask about option flow, unusual options activity, institutional positioning, market sentiment from derivatives, or AI trade reports.
homepage: https://www.optionwhales.io
metadata: {"openclaw": {"emoji": "🐋", "requires": {"anyBins": ["python3", "python"], "env": ["OPTIONWHALES_API_KEY"]}, "primaryEnv": "OPTIONWHALES_API_KEY"}}
---

# OptionWhales Intelligence Skill

Two capabilities in one skill:

1. **Option Flow** — query the OptionWhales Pro API for real-time institutional
   option flow analysis (intent momentum, abnormal trades, rankings).
2. **AI Reports** — generate and retrieve AI-powered trade analysis reports via
   a 22-node LLM pipeline (market analysis, flow, fundamentals, news, bull/bear
   debate, risk assessment, BUY/SELL/HOLD recommendation).

> **Free tier available!** Sign up at https://www.optionwhales.io to get a free
> API key instantly — no credit card required.

## When to Use

✅ USE this skill when:
- "What's the option flow on AAPL today?"
- "Show me unusual options activity"
- "What are institutions buying?"
- "Is there bullish or bearish momentum in TSLA?"
- "Show me the top momentum tickers"
- "Generate an AI report for TSLA"
- "What's the AI analysis on SPY today?"
- "Show my report history"
- "Check my report generation quota"

## When NOT to Use

❌ DON'T use this skill when:
- Stock price quotes only → use a stock/market data skill
- Historical stock charts → use a charting skill
- GEX / gamma exposure queries → not exposed via API
- Options pricing or Greeks calculation → use a quant tool
- Crypto or forex → this is US equity options only

## Setup

### Option Flow (required)

Requires an OptionWhales API key.

- **Free key:** Sign up at https://www.optionwhales.io/settings/api-keys
- **Pro key:** Full access — all tickers, all fields, historical sessions

```bash
export OPTIONWHALES_API_KEY="ow_free_your_key_here"  # or ow_pro_...
```

### AI Reports (optional)

Requires an AI service Bearer token (contact system administrator).

```bash
export AI_API_TOKEN="your_bearer_token_here"
```

---

# Part 1 — Option Flow API

Base URL: `https://api.optionwhales.io/v1`

All requests require header: `X-API-Key: $OPTIONWHALES_API_KEY`

## Flow API Reference

### Current Flow Rankings

```bash
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/flow/current" | python3 -m json.tool
```

Response includes per-ticker: `intent_primary` (Directional/Gamma/LongVol/ShortVol/Mixed),
`direction_bias` (bullish/bearish/neutral), `intent_confidence` (0-1), `momentum_fast`,
`momentum_slow`, `coherence_last`, `strength_last`, `key_strikes`.

### Ticker Detail (Clusters + Time Series)

```bash
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/flow/current/AAPL" | python3 -m json.tool
```

Returns: `ranking` (summary), `clusters` (strategy clusters with dollar Greeks),
`cluster_trades` (individual trades), `time_series` (30-min momentum buckets).

### Historical Sessions

```bash
# System health and session status
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/flow/sessions" | python3 -m json.tool

# Get a specific session's rankings
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/flow/2025-06-02" | python3 -m json.tool

# Get a specific ticker from a historical session
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/flow/2025-06-02/AAPL" | python3 -m json.tool
```

### Momentum Rankings

```bash
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/momentum/rankings" | python3 -m json.tool
```

### Momentum History

```bash
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/momentum/AAPL/history" | python3 -m json.tool
```

### Abnormal Trades

```bash
# Current session
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/abnormal-trades/current" | python3 -m json.tool

# Historical session
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/abnormal-trades/2025-06-02" | python3 -m json.tool
```

### Account Usage

```bash
curl -s -H "X-API-Key: $OPTIONWHALES_API_KEY" \
  "https://api.optionwhales.io/v1/account/usage" | python3 -m json.tool
```

### WebSocket — Real-Time Abnormal Trades (Pro Only)

```bash
python3 -c "
import asyncio, websockets, json
async def stream():
    uri = 'wss://api.optionwhales.io/v1/ws/abnormal-trades?api_key=YOUR_PRO_KEY'
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({'type': 'subscribe', 'tickers': ['AAPL', 'NVDA', 'TSLA']}))
        async for msg in ws:
            data = json.loads(msg)
            if data['type'] == 'abnormal_trade':
                print(json.dumps(data['data'], indent=2))
asyncio.run(stream())
"
```

## Flow Helper Script

```bash
# Current flow rankings
python3 {baseDir}/scripts/optionflow.py flow

# Flow for specific ticker
python3 {baseDir}/scripts/optionflow.py flow --ticker AAPL

# Historical session flow
python3 {baseDir}/scripts/optionflow.py flow --session 2025-06-02

# Momentum rankings
python3 {baseDir}/scripts/optionflow.py momentum

# Top 5 momentum tickers
python3 {baseDir}/scripts/optionflow.py momentum --top 5

# Current abnormal trades
python3 {baseDir}/scripts/optionflow.py abnormal

# Historical abnormal trades
python3 {baseDir}/scripts/optionflow.py abnormal --session 2025-06-02
```

## Interpreting Flow Results

### Intent Types
| Intent | Meaning |
|--------|---------|
| **Directional** | Net delta-dominant flow — strong directional bet |
| **Gamma** | Gamma-dominant — positioning for rapid price moves |
| **LongVol** | Buying volatility (long vega, positive theta risk) |
| **ShortVol** | Selling volatility (short vega, positive theta) |
| **Mixed** | No dominant Greek — conflicting signals |

### Direction Bias
- **bullish**: Net positive delta flow
- **bearish**: Net negative delta flow
- **neutral**: Delta share below 15% of total flow

### Confidence Score
0–1 scale combining flow coherence (how aligned the trades are) and strength
(total dollar Greek magnitude). Above 0.7 is high conviction.

### Momentum
- `momentum_fast` (α=0.35): responsive to recent flow changes
- `momentum_slow` (α=0.15): trend-smoothed
- Positive = bullish acceleration, negative = bearish acceleration

---

# Part 2 — AI Report Service

Base URL: `https://ai-service-production-b44b.up.railway.app`

All requests require header: `Authorization: Bearer $AI_API_TOKEN`

## Credit System

| Tier | Credits/Day | Can Generate? |
|------|-------------|---------------|
| FREE | 0 | No — hard-blocked |
| TRIAL | 5 | Yes |
| PRO | 5 | Yes |
| ADMIN | Unlimited | Yes |

Additional constraints:
- 5-minute cooldown per ticker after a successful generation
- ≥10% premium increase required to regenerate for the same ticker
- Credits reset daily at 12:00 AM ET

## AI Report API Reference

### Generate a Report

```bash
curl -s -X POST \
  -H "Authorization: Bearer $AI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user@example.com","user_tier":"PRO","ticker":"TSLA","session_date":"2026-03-25","session_type":"live","large_orders":[]}' \
  "https://ai-service-production-b44b.up.railway.app/reports"
```

Returns: `{"job_id": "abc-123", "status": "queued", "message": "..."}`

### Poll Job Status

```bash
curl -s -H "Authorization: Bearer $AI_API_TOKEN" \
  "https://ai-service-production-b44b.up.railway.app/reports/{job_id}"
```

### Fetch Report (JSON)

```bash
curl -s -H "Authorization: Bearer $AI_API_TOKEN" \
  "https://ai-service-production-b44b.up.railway.app/reports/by-id?user_id=user@example.com&ticker=TSLA&trading_day=2026-03-25&report_id=rpt-456"
```

### Fetch Report (Markdown)

```bash
curl -s -H "Authorization: Bearer $AI_API_TOKEN" \
  "https://ai-service-production-b44b.up.railway.app/reports/{job_id}/artifact/md"
```

### Report History

```bash
curl -s -H "Authorization: Bearer $AI_API_TOKEN" \
  "https://ai-service-production-b44b.up.railway.app/reports/history?ticker=TSLA&trading_day=2026-03-25&user_id=user@example.com"
```

### Per-Ticker Summary

```bash
curl -s -H "Authorization: Bearer $AI_API_TOKEN" \
  "https://ai-service-production-b44b.up.railway.app/reports/history/summary?user_id=user@example.com&trading_day=2026-03-25"
```

### Check Quota

```bash
curl -s -H "Authorization: Bearer $AI_API_TOKEN" \
  "https://ai-service-production-b44b.up.railway.app/quotas?user_id=user@example.com&tier=PRO"
```

### Check Eligibility

```bash
curl -s -X POST \
  -H "Authorization: Bearer $AI_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user@example.com","user_tier":"PRO","ticker":"TSLA","session_date":"2026-03-25","session_type":"live","large_orders":[]}' \
  "https://ai-service-production-b44b.up.railway.app/eligibility"
```

### Health Check

```bash
curl -s -H "Authorization: Bearer $AI_API_TOKEN" \
  "https://ai-service-production-b44b.up.railway.app/health"
```

## AI Report Helper Script

```bash
# Generate a report
python3 {baseDir}/scripts/aireport.py generate --ticker TSLA --user-id user@example.com --user-tier PRO

# Check job status
python3 {baseDir}/scripts/aireport.py status --job-id abc-123

# Fetch report (JSON)
python3 {baseDir}/scripts/aireport.py report --user-id user@example.com --ticker TSLA --trading-day 2026-03-25 --report-id rpt-456

# Fetch report (Markdown)
python3 {baseDir}/scripts/aireport.py report --job-id abc-123 --format markdown

# Browse existing reports
python3 {baseDir}/scripts/aireport.py summary --user-id user@example.com --trading-day 2026-03-25

# List reports for a ticker
python3 {baseDir}/scripts/aireport.py history --ticker TSLA --trading-day 2026-03-25 --user-id user@example.com

# Check quota
python3 {baseDir}/scripts/aireport.py quota --user-id user@example.com --tier PRO

# Check eligibility
python3 {baseDir}/scripts/aireport.py eligibility --ticker TSLA --user-id user@example.com --user-tier PRO

# Service health
python3 {baseDir}/scripts/aireport.py health
```

## Interpreting AI Report Results

### Decision Actions
| Action | Meaning |
|--------|---------|
| **BUY** | Bullish — AI recommends long exposure on the underlying |
| **SELL** | Bearish — AI recommends short exposure / protective puts |
| **HOLD** | Neutral — no new directional exposure recommended |

### Confidence Score
0–100 scale reflecting the AI pipeline's conviction. Above 70% = high conviction;
below 50% = conflicting signals.

### Report Sections
| Section | Content |
|---------|---------|
| Option Flow | Institutional flow analysis, intent momentum, flow coherence |
| Abnormal Flow | Large/unusual trades flagged by the detection engine |
| Market Structure | GEX levels, call/put walls, max pain, key strike zones |
| Market | Macro indicators, OHLCV, technical levels |
| Fundamentals | Company fundamentals, valuation metrics |
| News | Recent news sentiment analysis |
| Debate | Bull vs Bear researcher arguments with judge decision |
| Risk | Three-analyst risk assessment (aggressive, conservative, neutral) |

---

## Example Queries → Commands

| User asks | Tool |
|-----------|------|
| "What's the flow today?" | `python3 {baseDir}/scripts/optionflow.py flow` |
| "Show TSLA option activity" | `python3 {baseDir}/scripts/optionflow.py flow --ticker TSLA` |
| "Top momentum tickers" | `python3 {baseDir}/scripts/optionflow.py momentum` |
| "Any unusual trades?" | `python3 {baseDir}/scripts/optionflow.py abnormal` |
| "Is AAPL bullish or bearish?" | `python3 {baseDir}/scripts/optionflow.py flow --ticker AAPL` → check `direction_bias` |
| "Generate AI report for TSLA" | `python3 {baseDir}/scripts/aireport.py generate --ticker TSLA --user-id <user> --user-tier PRO` |
| "Show my report history" | `python3 {baseDir}/scripts/aireport.py summary --user-id <user> --trading-day <today>` |
| "Check my report quota" | `python3 {baseDir}/scripts/aireport.py quota --user-id <user> --tier PRO` |
| "Show my API usage" | `python3 {baseDir}/scripts/optionflow.py usage` |

## Notes

- Option flow data updates every 30 minutes during market hours (9:30 AM – 4:00 PM ET)
- Final daily data available after 7:30 AM ET next trading day (with full OI deltas)
- **Free tier:** 10 requests/minute, 200/day; top 3 tickers, last 5 abnormal trades
- **Pro tier:** 60 requests/minute, 5000/day; all tickers, all fields, WebSocket, historical sessions
- AI reports take 30–90 seconds to generate (22-node pipeline)
- US equity options only (no futures, crypto, or forex)
