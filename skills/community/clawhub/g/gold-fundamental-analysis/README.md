# 📊 Gold Fundamental Analysis Skill

**Fundamental analysis for Gold (XAU/USD)** — Macro data, COT positioning, ETF flows, Fed stance & economic calendar.

<p align="center">
  <a href="https://clawhub.ai/skills/gold-fundamental-analysis"><img src="https://img.shields.io/badge/clawhub-skill-blue" alt="ClawHub"></a>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

**[🇻🇳 Tiếng Việt](README.vi.md)**

---

## 📖 Overview

**Gold Fundamental Analysis** fetches and analyzes gold fundamental data from **5 authoritative sources**, producing a structured fundamental report with Bullish/Bearish factors, a numerical score (-100 to +100), and short/medium/long-term outlooks.

Designed for **OpenClaw agents** — used both on-demand and in cron jobs for daily trading sessions (Asian/European/US).

> ⚠️ **Disclaimer:** This is a **supplementary analysis tool**, not financial advice. Investing involves risk. Always use stop-loss.

## ✨ Data Sources

| # | Source | Data | Reliability |
|---|--------|------|-------------|
| 1 | **FRED API** (St. Louis Fed) | Fed rate, CPI, Core CPI, 10Y yield, Real yield, DXY | ⭐⭐⭐⭐⭐ |
| 2 | **CFTC COT** | Managed Money long/short positions, net position | ⭐⭐⭐⭐⭐ |
| 3 | **SPDR Gold ETF (SSGA/GLD)** | AUM, NAV, estimated gold tonnes | ⭐⭐⭐⭐ |
| 4 | **Fed RSS** | Monetary policy statements (30-day window) | ⭐⭐⭐⭐⭐ |
| 5 | **ForexFactory** (via faireconomy.media) | High/medium-impact USD economic events | ⭐⭐⭐⭐ |

## 📊 Analysis Framework — 7 Pillars

| # | Pillar | Signal | Impact on Gold |
|---|--------|--------|---------------|
| 1 | **Fed Policy** | Dovish → +Bullish / Hawkish → −Bearish | ⭐⭐⭐⭐⭐ |
| 2 | **Inflation** | Rising → +Bullish (gold as hedge) | ⭐⭐⭐⭐ |
| 3 | **Real Yield** | Falling → +Bullish / Rising → −Bearish | ⭐⭐⭐⭐⭐ |
| 4 | **DXY** | Weakening → +Bullish / Strengthening → −Bearish | ⭐⭐⭐⭐⭐ |
| 5 | **ETF Flows** | Inflows → +Bullish / Outflows → −Bearish | ⭐⭐⭐ |
| 6 | **COT Positioning** | Extreme short → contrarian +Bullish / Extreme long → contrarian −Bearish | ⭐⭐⭐⭐ |
| 7 | **Upcoming Events** | FOMC/CPI/NFP within 3 days → increased volatility | ⭐⭐⭐ |

## 🚀 Installation

```bash
pip install requests
git clone https://github.com/kimminhpro/gold-fundamental-analysis-skill.git
cd gold-fundamental-analysis-skill
python3 scripts/get_gold_fundamental_data.py
```

## 🔧 Usage

```bash
# Basic — fetch all data
python3 scripts/get_gold_fundamental_data.py

# Custom FRED API key
python3 scripts/get_gold_fundamental_data.py --fred-key YOUR_FRED_KEY

# Or via env var
FRED_API_KEY=your_key python3 scripts/get_gold_fundamental_data.py
```

### Output

The script outputs structured JSON with 5 sections:

```json
{
  "timestamp": "2026-06-14T16:54:49Z",
  "macro": { "fed_rate": {...}, "cpi": {...}, "us10y_yield": {...}, "real_yield": {...}, "dxy": {...} },
  "cot": { "managed_money_long": 10833, "managed_money_short": 30133, "net_position": -19300 },
  "etf": { "aum_usd_millions": 136399.42, "estimated_tonnes": 1048.98 },
  "fed": { "stance": "neutral", "summary": "..." },
  "economic_calendar": { "upcoming_events": [...] }
}
```

## 🎯 Scoring System

Calculate **Fundamental Score** (-100 to +100):

### Bullish Factors (+)
- Fed rate cut / dovish pivot: **+20 to +30**
- CPI declining (disinflation): **+10 to +20**
- Real yield falling: **+15 to +25**
- DXY weakening: **+10 to +15**
- ETF inflows: **+10**
- COT extreme net short (< -30,000): **+10 to +15** (contrarian)

### Bearish Factors (−)
- Hawkish Fed / rate hike: **−20 to −30**
- CPI rising (reflation): **−10 to −20**
- Real yield rising: **−15 to −25**
- DXY strengthening: **−10 to −15**
- ETF outflows: **−10**
- COT extreme net long (> +150,000): **−10 to −15** (contrarian)

### Confidence Score
| Level | Meaning |
|-------|---------|
| **90%+** | All sources successful, clear alignment |
| **70–89%** | 3–4 sources successful, mostly aligned |
| **50–69%** | Mixed signals, some sources missing |
| **<50%** | High uncertainty — WARN user |

## 📋 Output Format (Agent Analysis)

After fetching JSON data, the agent produces:

```
📊 GOLD FUNDAMENTAL ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━

🐂 BULLISH FACTORS:
• Fed: rate at 3.63%, trending dovish — +25
• Real yield falling to 2.16% — +20
• COT extreme net short (-19,300) — +10

🐻 BEARISH FACTORS:
• DXY strengthening to 120.08 — -15
• CPI rising (3.33% → 3.36%) — -10

⚖️ NEUTRAL:
• Fed stance detected as neutral
• ETF holdings stable at 1,049 tonnes

📈 FUNDAMENTAL SCORE: +30 / 100
→ Neutral-to-bullish

🔭 OUTLOOK:
• Short-term (1-3 days): Bullish bias, watch FOMC
• Medium-term (1-2 weeks): Neutral bullish
• Long-term (1-3 months): Bullish (rate cut cycle)

🎯 CONFIDENCE: 85%
```

## 🏗️ Integration with OpenClaw

This skill works alongside:
- **MT5 MCP** → Technical analysis (SMC, order blocks, FVG)
- **Financial Astrology Skill** → Planetary analysis
- **Cron jobs** → 3 daily gold session analyses (Asia/EU/US)

## ⚙️ Requirements

```
requests>=2.25.0
```

## 📚 References

- FRED API: https://fred.stlouisfed.org/docs/api/fred/
- CFTC COT: https://www.cftc.gov/dea/newcot/f_disagg.txt
- SPDR Gold Shares: https://www.ssga.com/us/en/intermediary/etfs/spdr-gold-shares-gld
- Fed Press Releases: https://www.federalreserve.gov/feeds/press_monetary.xml

## 📝 License

MIT
