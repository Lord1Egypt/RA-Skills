---
name: gold-fundamental-analysis
description: Fetches and analyzes gold fundamental data from FRED, CFTC, SPDR ETF, and Fed RSS. Used when the user requests gold fundamental analysis, phân tích cơ bản vàng, or gold macro data. Also used by cron jobs for gold trading sessions (Asian/European/US) that need fundamental context. Returns structured JSON with macro indicators, COT positioning, ETF holdings, Fed stance, and upcoming events. The agent MUST execute the Python script to fetch data, then analyze the output to produce Bullish/Bearish/Neutral factors, a Fundamental Score (-100 to +100), and short/medium/long-term outlook.
---

# Gold Fundamental Analysis Skill

## Quick Start

Run the data fetcher script to get all fundamental data:

```bash
python3 scripts/get_gold_fundamental_data.py
```

The script outputs a JSON object with 5 sections. The agent must then analyze this data and produce a structured fundamental report.

## Data Sources

| Source | Data | Stability |
|--------|------|-----------|
| FRED API | Fed rate, CPI, Core CPI, 10Y yield, Real yield, DXY | High (stable API) |
| CFTC COT | Managed Money long/short, net position | High (public file) |
| SPDR GLD (SSGA) | AUM, NAV, estimated gold tonnes | Medium (web scrape) |
| Fed RSS | Monetary policy statements (30-day window) | High (RSS feed) |
| ForexFactory Calendar | Upcoming high/medium-impact USD events via faireconomy.media JSON | High (public JSON) |

## Analysis Framework

After fetching data, analyze these 7 pillars:

1. **Fed Policy** — Rate direction, FOMC stance. Lower rates = bullish gold.
2. **Inflation** — CPI/Core CPI trend. Rising = bullish (gold as hedge).
3. **Real Yield** — 10Y TIPS real yield. Falling real yield = bullish gold.
4. **DXY** — Dollar index. Weaker dollar = bullish gold.
5. **ETF Flows** — SPDR holdings change. Inflows = bullish.
6. **COT Positioning** — Managed Money net position. Excess long = contrarian bearish; excess short = contrarian bullish.
7. **Upcoming Events** — FOMC, CPI, NFP, etc. High-impact events = volatility ahead.

## Output Format

After analysis, the agent must produce this structured output in Vietnamese:

```
📊 PHÂN TÍCH CƠ BẢN VÀNG
━━━━━━━━━━━━━━━━━━━━━━━━

🐂 YẾU TỐ TĂNG GIÁ (Bullish):
• ...
• ...

🐻 YẾU TỐ GIẢM GIÁ (Bearish):
• ...
• ...

⚖️ YẾU TỐ TRUNG LẬP:
• ...

📈 ĐIỂM SỐ CƠ BẢN: +XX/-XX / 100
   (thang đo: -100 Bearish cực đoan ↔ +100 Bullish cực đoan)

🔭 TRIỂN VỌNG:
• Ngắn hạn (1-3 ngày): ...
• Trung hạn (1-2 tuần): ...
• Dài hạn (1-3 tháng): ...

🎯 ĐỘ TIN CẬY: XX%
```

## Scoring Guidelines

Calculate Fundamental Score (-100 to +100):

**Bullish factors (positive points):**
- Fed rate cut or dovish pivot: +20 to +30
- CPI declining (disinflation): +10 to +20
- Real yield falling: +15 to +25
- DXY weakening: +10 to +15
- ETF inflows: +10
- COT net long increasing: +5 to +10

**Bearish factors (negative points):**
- Hawkish Fed / rate hike: -20 to -30
- CPI rising (inflation): -10 to -20
- Real yield rising: -15 to -25
- DXY strengthening: -10 to -15
- ETF outflows: -10
- COT extreme net long: -5 to -10

**Adjustments:**
- COT extreme net short (> -30,000): +10 to +15 (contrarian bullish)
- COT extreme net long (> +150,000): -10 to -15 (contrarian bearish)
- Major upcoming event within 3 days: increase magnitude by 20%

## Confidence Score

- 90%+: All data sources successful, clear trend alignment
- 70-89%: 3-4 sources successful, mostly aligned
- 50-69%: Mixed signals, some sources missing
- <50%: <3 sources successful, high uncertainty — WARN the user

## Integration Notes

This skill is designed to be used:
1. **On-demand**: When user says "phân tích cơ bản vàng", "gold fundamental", etc.
2. **In cron jobs**: The 3 daily gold session analyses (Asia, EU, US) should call this script for fundamental data, then combine with MT5 MCP for technical analysis and Financial Astrology skill for astro analysis.
3. **Standalone script**: The Python script can be called from any session with full access to all data sources.

## FRED API Key

The script uses FRED API key `01fa16f50b07eb27740820fd1cdecf50`. Override with `--fred-key KEY` or `FRED_API_KEY` env var.
