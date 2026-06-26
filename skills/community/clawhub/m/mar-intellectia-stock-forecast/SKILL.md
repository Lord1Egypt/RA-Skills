---
name: intellectia-stock-forecast
description: US Stock AI Trading Assistant | SkillBoss API Hub Stock Forecast — Smart analysis of stock entry/exit points, target price predictions, probability calculations, and technical ratings. Supports "Should I Buy" investment decision Q&A.
metadata: {"openclaw":{"requires":{"bins":["curl","python3"]},"requires_env":["SKILLBOSS_API_KEY"],"install":[{"id":"python","kind":"pip","package":"requests","bins":[],"label":"Install requests (pip)"}]}}
---

# Stock Forecast (via SkillBoss API Hub)

Single-symbol **forecast** (yearly predictions) and **"Should I Buy?"** analysis via SkillBoss API Hub.

Base URL: `https://api.skillboss.com/v1`

## Overview

This skill covers two use cases:

- **Forecast (predictions):** Web search for yearly stock price predictions (2026–2035) via SkillBoss API Hub `search` type
- **Why / Should I buy (analysis):** AI chat analysis for buy/sell/hold recommendations via SkillBoss API Hub `chat` type

## When to use this skill

Use this skill when you want to:
- Get **one** stock/crypto quote + **yearly predictions** (2026–2035)
- Answer **why / should I buy** for a specific ticker with a structured rationale

## How to ask (high hit-rate)

If you want OpenClaw to automatically pick this skill, include:
- The **ticker** (e.g. TSLA / AAPL / BTC-USD)
- Either **forecast / prediction** (for predictions) or **why / should I buy** (for analysis)

To force the skill: `/skill intellectia-stock-forecast <your request>`

Copy-ready prompts:
- "Forecast for **TSLA**. Show price, probability, profit, and predictions 2026–2035."
- "Why should I buy **TSLA**? Give me a buy/sell/hold analysis."
- "Should I buy **AAPL**? Give me conclusion, catalysts, analyst rating, and 52-week range."
- "Get yearly predictions for **BTC-USD** (crypto)."

## Endpoints

| Use case | SkillBoss type | Pilot endpoint |
|---|---|---|
| Forecast (predictions 2026–2035) | `search` | `POST https://api.skillboss.com/v1/pilot` |
| Why / Should I buy analysis | `chat` | `POST https://api.skillboss.com/v1/pilot` |

## API: Forecast (stock predictions search)

- **Method:** `POST https://api.skillboss.com/v1/pilot`
- **Auth:** `Authorization: Bearer $SKILLBOSS_API_KEY`
- **Body:**
  - `type: "search"` — SkillBoss API Hub web search
  - `inputs.query`: include ticker + "stock forecast predictions 2026 2027 … 2035"
- **Returns:** `result` (structured search results with prediction data)

### Example (cURL)

```bash
curl -sS -X POST "https://api.skillboss.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"search","inputs":{"query":"TSLA stock price forecast predictions 2026 2027 2028 2029 2030 2031 2032 2033 2034 2035"},"prefer":"balanced"}'
```

### Example (Python)

```bash
python3 - <<'PY'
import requests, os
SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
r = requests.post(
    "https://api.skillboss.com/v1/pilot",
    headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
    json={"type": "search", "inputs": {"query": "TSLA stock price forecast predictions 2026 2027 2028 2029 2030 2031 2032 2033 2034 2035"}, "prefer": "balanced"},
    timeout=30)
r.raise_for_status()
results = r.json()["result"]
print(results)
PY
```

## API: Why / Should I buy (AI chat analysis)

- **Method:** `POST https://api.skillboss.com/v1/pilot`
- **Auth:** `Authorization: Bearer $SKILLBOSS_API_KEY`
- **Body:**
  - `type: "chat"` — SkillBoss API Hub LLM analysis (auto-routed)
  - `inputs.messages`: ask for buy/sell/hold recommendation with catalysts and rating
- **Returns:** `result.choices[0].message.content`

### Example (cURL)

```bash
curl -sS -X POST "https://api.skillboss.com/v1/pilot" \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"chat","inputs":{"messages":[{"role":"user","content":"Should I buy TSLA stock? Provide: conclusion (buy/sell/hold), positive catalysts, negative catalysts, analyst rating, technical analysis, entry point, target price, and 52-week range context."}]},"prefer":"balanced"}'
```

### Example (Python)

```bash
python3 - <<'PY'
import requests, os
SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
r = requests.post(
    "https://api.skillboss.com/v1/pilot",
    headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
    json={
        "type": "chat",
        "inputs": {"messages": [{"role": "user", "content": "Should I buy TSLA? Give conclusion (buy/sell/hold), positive catalysts, negative catalysts, analyst rating, and technical analysis."}]},
        "prefer": "balanced"
    },
    timeout=30)
r.raise_for_status()
content = r.json()["result"]["choices"][0]["message"]["content"]
print("analysis:", content)
PY
```

## Tool configuration

| Tool | Purpose |
|---|---|
| `curl` | One-off POST to SkillBoss API Hub |
| `python3` / `requests` | Scripts; `pip install requests` |

## Using this skill in OpenClaw

```bash
clawhub install intellectia-stock-forecast
```

Start a **new OpenClaw session**, then:

```bash
openclaw skills list
openclaw skills info intellectia-stock-forecast
openclaw skills check
```

## Disclaimer and data

- **Disclaimer:** The data and analysis from this skill are for **informational purposes only** and do not constitute financial, investment, or trading advice. Past performance and model predictions are not guarantees of future results. You are solely responsible for your investment decisions; consult a qualified professional before making financial decisions.
- **Data source:** Data is retrieved via SkillBoss API Hub web search and AI analysis. Results may vary and are not necessarily real-time. For authoritative real-time data, consult a licensed financial data provider.

## Notes

- **Forecast search:** One symbol per request; include the full year range in the query for best results.
- **Should I buy:** Use `chat` type; the LLM will provide conclusion and catalysts in structured form. Use `prefer: "balanced"` for speed or `prefer: "quality"` for more thorough analysis.
