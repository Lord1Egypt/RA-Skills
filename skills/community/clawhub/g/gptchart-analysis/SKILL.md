---
name: gptchart-analysis
description: >
  Analyze cryptocurrency, stock, and forex trading charts using GPTChart.ai's
  AI-powered technical analysis engine. Supports basic and expert analysis
  modes with 18 technical indicators. Credits are deducted from the account
  tied to your GPTCHART_API_KEY.
version: 1.0.0
author: GPTChart.ai
tags: [trading, finance, crypto, stocks, forex, technical-analysis, charts]
user-invocable: true
metadata:
  { 'openclaw': { 'requires': { 'env': ['GPTCHART_API_KEY'] }, 'primaryEnv': 'GPTCHART_API_KEY' } }
---

# GPTChart.ai — AI Trading Chart Analysis

Use this skill to request AI-powered technical analysis on any trading symbol
(crypto, stocks, forex). Each analysis call deducts credits from the
GPTChart.ai account associated with your API key.

## Authentication

All requests must include the header:

```
Authorization: Bearer $GPTCHART_API_KEY
```

Never echo or log the value of `$GPTCHART_API_KEY` in any response.

## Base URL

```
https://gptchart.ai
```

---

## Available Endpoints

### Analysis Endpoints

| Method | Path                      | Description              |
| ------ | ------------------------- | ------------------------ |
| POST   | `/api/v2/crypto/analyze`  | Analyze cryptocurrency charts |
| POST   | `/api/v2/stock/analyze`   | Analyze stock charts     |
| POST   | `/api/v2/forex/analyze`   | Analyze forex charts     |

### Symbol Endpoints

| Method | Path                      | Description              |
| ------ | ------------------------- | ------------------------ |
| GET    | `/api/v2/crypto/symbols`  | Get available crypto symbols |
| GET    | `/api/v2/stock/symbols`   | Get available stock symbols |
| GET    | `/api/v2/forex/symbols`   | Get available forex symbols |

---

## Analysis Request Schema

All analysis endpoints (`POST /api/v2/{market}/analyze`) accept the same request structure:

| Field                | Type     | Required | Description                                                     |
| -------------------- | -------- | -------- | --------------------------------------------------------------- |
| `symbol`             | string   | Yes      | Trading symbol (e.g., `BTC-USD`, `AAPL`, `EURUSD`)              |
| `interval`           | enum     | Yes*     | Timeframe: `1m`, `5m`, `15m`, `30m`, `1H`, `4H`, `1D`, `1W`, `1M` |
| `expertMode`         | boolean  | No       | Enable advanced analysis (default: false)                       |
| `selectedIndicators` | string[] | No       | Max 3 indicator keys (see Available Indicators)                 |
| `timeframes`         | string[] | No       | Max 2 additional timeframes for expert mode                     |
| `customPrompt`       | string   | No       | Custom analysis instructions (max 3000 chars)                   |
| `analyzeRelatedNews` | boolean  | No       | Include news analysis (default: false)                          |
| `strategyId`         | string   | No       | User strategy ID for personalized analysis                      |
| `language`           | string   | No       | Response language (default: `en`)                               |

*`interval` is required unless `strategyId` is provided.

---

## Available Indicators

Use these IDs in `selectedIndicators` (max 3):

| ID          | Indicator                              |
| ----------- | -------------------------------------- |
| `sma`       | Simple Moving Average                  |
| `ema`       | Exponential Moving Average             |
| `ichimoku`  | Ichimoku Cloud                         |
| `bbands`    | Bollinger Bands                        |
| `atr`       | Average True Range                     |
| `supertrend`| Supertrend                             |
| `sar`       | Parabolic SAR                          |
| `rsi`       | Relative Strength Index                |
| `macd`      | MACD                                   |
| `kst`       | Know Sure Thing                        |
| `stoch`     | Stochastic Oscillator                  |
| `adx`       | Average Directional Index              |
| `percent_b` | %B (Percent B)                         |
| `mfi`       | Money Flow Index                       |
| `dpo`       | Detrended Price Oscillator             |
| `vwap`      | Volume Weighted Average Price          |
| `rvol`      | Relative Volume                        |
| `ad`        | Accumulation/Distribution              |

---

## Analysis Response Schema

| Field              | Type   | Description                              |
| ------------------ | ------ | ---------------------------------------- |
| `analysis`         | string | Detailed AI analysis and reasoning       |
| `entry`            | number | Suggested entry price                    |
| `stopLoss`         | number | Recommended stop-loss price              |
| `takeProfit`       | number | Target take-profit price                 |
| `confirmationPrice`| number | Price level for trade confirmation       |
| `reasoning`        | string | Concise trading rationale                |
| `bias`             | string | Market bias: `Buy`, `Sell`, or `Neutral` |
| `creditsUsed`      | number | Credits consumed for this analysis       |

---

## How to Use This Skill

### Basic Analysis

When the user asks to analyze a symbol, construct a basic request:

```bash
curl -s -X POST https://gptchart.ai/api/v2/crypto/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GPTCHART_API_KEY" \
  -d '{
    "symbol": "BTC-USD",
    "interval": "4H"
  }'
```

### Expert Analysis with Indicators

When the user wants a deep analysis with specific indicators:

```bash
curl -s -X POST https://gptchart.ai/api/v2/forex/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GPTCHART_API_KEY" \
  -d '{
    "symbol": "XAUUSD",
    "interval": "1D",
    "expertMode": true,
    "selectedIndicators": ["rsi", "macd", "bbands"],
    "timeframes": ["1D", "1W"]
  }'
```

### Expert Analysis with Custom Prompt

When the user wants a tailored analysis with specific trading rules:

```bash
curl -s -X POST https://gptchart.ai/api/v2/stock/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GPTCHART_API_KEY" \
  -d '{
    "symbol": "AAPL",
    "interval": "1W",
    "expertMode": true,
    "selectedIndicators": ["ichimoku", "vwap", "adx"],
    "customPrompt": "Focus on swing trade setups with R:R above 2"
  }'
```

### Strategy-Based Analysis

When the user has a saved strategy:

```bash
curl -s -X POST https://gptchart.ai/api/v2/crypto/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GPTCHART_API_KEY" \
  -d '{
    "symbol": "BTC-USD",
    "strategyId": "c1mEhAha9qaVpHdAKQx0"
  }'
```

### Get Available Symbols

```bash
curl -s https://gptchart.ai/api/v2/crypto/symbols \
  -H "Authorization: Bearer $GPTCHART_API_KEY"
```

---

## Presenting Results

After a successful analysis response, present the results clearly:

- State the **bias** prominently (Buy / Sell / Neutral)
- Show **Entry**, **Stop Loss**, and **Take Profit** as formatted prices
- Include the **Confirmation Price** if provided
- Summarize the **analysis** narrative in plain language
- Mention **credits used** so the user stays aware of their balance

Example format:

```
BTCUSD 4H Analysis
Bias: Buy

Entry:              $98,200
Stop Loss:          $95,800
Take Profit:        $103,500
Confirmation Price: $98,500

Summary: Price is consolidating above the 200 EMA with RSI recovering
from oversold. MACD showing bullish crossover. Setup favors long on
a breakout above $98,500 resistance.

Credits used: 3
```

---

## Error Handling

| Status | Meaning              | Action                                                |
| ------ | -------------------- | ----------------------------------------------------- |
| 400    | Bad Request          | Check symbol, interval, and request body values       |
| 401    | Unauthorized         | API key is missing, invalid, or insufficient credits  |
| 403    | Forbidden            | Subscription required — user is on Free tier          |
| 405    | Method Not Allowed   | Check HTTP method (POST for analysis, GET for symbols)|
| 429    | Rate Limited         | Wait and retry after a short delay                    |
| 500    | Server Error         | Inform user and suggest retrying in a moment          |

On a 403 error, tell the user: "A paid GPTChart.ai subscription is required to use the API. Please upgrade at https://gptchart.ai/account/pricing-plan."

---

## Setup Instructions for Users

1. Go to [https://gptchart.ai/account/api-keys](https://gptchart.ai/account/api-keys)
2. Generate a new API key
3. Add it to your OpenClaw config:

```json
{
  "env": {
    "GPTCHART_API_KEY": "your-api-key-here"
  }
}
```

Or set it as a system environment variable:

```bash
export GPTCHART_API_KEY=your-api-key-here
```

4. Install this skill: `clawhub install gptchart-analysis`
5. Ask your agent: _"Analyze BTCUSD on the 4-hour timeframe"_
