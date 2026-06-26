# market-breadth-analyzer

> Assess market internal health using advance/decline ratios, % above key moving averages, new highs/lows, and breadth divergence signals — all free tier endpoints from [Finskills API](https://finskills.net).

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Plan](https://img.shields.io/badge/API%20Plan-Free-brightgreen.svg)](https://finskills.net/register)
[![Category](https://img.shields.io/badge/category-market--regime-blue.svg)]()

---

## What This Skill Does

1. Fetches breadth data: advance/decline counts and volume, new 52-week highs/lows, % of stocks above 200/50 MA
2. Computes ADR, volume-weighted A/D (accumulation vs. distribution), net new highs
3. Detects bullish and bearish breadth divergences vs. index price
4. Flags narrow rallies (few stocks driving the index)
5. Outputs a Market Health Score (1–5) with actionable positioning guidance

**All API endpoints used are on the free tier — no Pro plan required.**

## Install

Add this skill via [ClawHub](https://clawhub.ai/finskills/market-breadth-analyzer):

1. Visit **[https://clawhub.ai/finskills/market-breadth-analyzer](https://clawhub.ai/finskills/market-breadth-analyzer)**
2. Click **Download zip** and follow the setup instructions
3. Set your API key: `FINSKILLS_API_KEY=your_key_here`

## Quick Start

```
You: Is the market rally broad-based or narrow right now?
Claude: [Fetches breadth data, calculates ADR, % above MAs, new highs/lows, outputs health report]
```

## Example Triggers

- `"How healthy is the market internally?"`
- `"Is this a broad rally or is it just a few mega-caps?"`
- `"Are more stocks making new highs or new lows?"`
- `"Check the advance/decline ratio today"`
- `"Is there a breadth divergence?"`

## API Endpoints Used (All Free)

| Endpoint | Data |
|----------|------|
| `GET /v1/free/market/breadth` | A/D ratio, % above MAs, new highs/lows |
| `GET /v1/market/summary` | S&P 500/Nasdaq/Russell index levels |
| `GET /v1/free/market/short-volume-top` | Most heavily shorted stocks |

## Market Health Score

| Score | Condition | Action |
|-------|-----------|--------|
| 4–5 | Healthy bull | Stay invested, buy dips |
| 3–4 | Moderate | Selective positioning |
| 2–3 | Weakening | Raise cash, reduce risk |
| 1–2 | Unhealthy | Defensive posture |

## Requirements

- **Finskills API Key**: [Register at finskills.net](https://finskills.net) (free tier available) — **all endpoints are free tier**
- **Claude** with skill support

## License

MIT — see [LICENSE](../LICENSE)
