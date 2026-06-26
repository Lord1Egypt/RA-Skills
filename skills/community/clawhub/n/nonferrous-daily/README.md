# metal-price 🦞

> AI-powered non-ferrous metals daily briefing — data collection + professional analyst report via Telegram.

A lightweight Node.js system that collects real-time base metals prices from multiple free sources, aggregates market news and forum sentiment, then delivers a professional trading-style analysis to Telegram every day at 14:00 CST (after China's morning session closes).

## Features

- 📊 **Multi-source price aggregation** — Yahoo Finance (USD), CCMN 長江有色 (CNY), SMM/Westmetall cross-checks
- 📰 **News & sentiment** — Google News (CN+EN) with 48h filter, SMM 快訊, Reddit r/Commodities 異動偵測
- 🏦 **Investment bank signals** — 自動抽取高盛/摩根大通/花旗的基本金屬觀點
- 📈 **Technical** — forward curve (spot/+2M/+6M), basis, contango/backwardation detection
- 📦 **庫存三件套** — 交易所 / 保稅 / 社會庫存（佔位兜底），周環比箭頭
- 🚢 **進口盈虧/到岸成本** — Cu/Zn/Ni 匯率+外盤→內盤，盈虧/壓力標註
- 📊 **信號摘要** — 庫存 / 基差 / 進口盈虧 / 需求 四維 +/0/- 打分
- 🌡️ **宏觀溫度計** — DXY / VIX / CRB（佔位）/ 10Y，提示風險開關
- 🔮 **Cross reasoning** — 宏觀 × 庫存 × 結構 × 情緒，段落式分析 + 操作參考
- ⏰ **14:00 CST timing** — after China morning session + LME overnight data
- 🚫 **Zero paid APIs** — all free data sources; no API key required

## Metals Covered

| Metal | USD Source | CNY Source |
|-------|------------|------------|
| Copper (Cu) | Yahoo `HG=F` + COMEX forwards | CCMN 長江有色 + SMM 交叉驗證 |
| Zinc (Zn)   | Westmetall LME Cash | CCMN 長江有色 + SMM 交叉驗證 |
| Nickel (Ni) | Westmetall LME Cash | CCMN 長江有色 + SMM 交叉驗證 |
| Cobalt (Co) | TradingEconomics (USD) | CCMN 長江有色 |
| Bismuth (Bi)| SMM CIF USD/kg | SMM 精鉍 |
| Magnesium (Mg) | — | CCMN 1#鎂 |

## Architecture

```
fetch-all-data.mjs          ← Master data script (≤3s, runs in parallel)
  ├── Yahoo Finance           USD spot + forward contracts
  ├── CCMN 長江有色 API        CNY spot prices (Cu/Zn/Ni/Co + 30 others)
  ├── Stooq                   Bismuth USD/t
  ├── LME inventory           3 methods, all Cloudflare-blocked (returns null)
  ├── Google News RSS (CN)    Chinese metals news
  ├── Google News RSS (EN)    Investment bank base metals analysis
  ├── SMM 上海有色網           Flash news headlines
  └── Reddit r/Commodities    Top (weekly) + Hot (realtime) with metal keyword filter
                              + surging post detection (hot but not in top)

send-telegram.mjs            ← Utility: pipe JSON or arg to Telegram Markdown message
```

The actual analysis/briefing is written by an AI agent (Claude) that runs `fetch-all-data.mjs`, reads the JSON, fetches 2 news articles, and composes a professional trading brief.

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/RAMBOXIE/metal-price.git
cd metal-price
# No npm install needed — zero external dependencies
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your Telegram bot token and chat ID
```

### 3. Run data collection

```bash
node scripts/fetch-all-data.mjs
```

Output is a JSON object with prices, forwards, inventory, news, ibNews, and forumSentiment.

### 4. Send a message

```bash
# Send a string
node scripts/send-telegram.mjs "Hello from metal-price 🦞"

# Pipe JSON summary
node scripts/fetch-all-data.mjs | node scripts/send-telegram.mjs
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (from @BotFather) | ✅ |
| `TELEGRAM_CHAT_ID` | Target chat/channel ID | ✅ |
| `METAL_PRICE_API_KEY` | metalpriceapi.com key (free tier = precious metals only, not used) | ❌ |
| `ALPHA_VANTAGE_KEY` | Alpha Vantage key (monthly copper only, not used) | ❌ |

## Output JSON Structure

```json
{
  "date": "2026-03-15",
  "dataDate": "2026-03-13",
  "isMarketOpen": false,
  "marketNote": "休市：數據截至 2026/03/13（上個交易日）",
  "changeNote": "所有漲跌均為日環比（vs 前一交易日收盤）",
  "prices": {
    "copper":  { "usd": 5.757, "usdChangePct": 0.75, "usdUnit": "USD/lb", "cny": 100690, "cnyChange": -330 },
    "zinc":    { "usd": null,  "usdChangePct": null,  "usdUnit": "USD/t",  "cny": 24130,  "cnyChange": -220 },
    "aluminum":{ "usd": 3423,  "usdChangePct": 1.18,  "usdUnit": "USD/t",  "cny": null,   "cnyChange": null },
    "nickel":  { "usd": null,  "cny": 141750, "cnyChange": 600 },
    "cobalt":  { "usd": null,  "cny": 432000, "cnyChange": 0 },
    "bismuth": { "usd": 2272,  "usdUnit": "USD/t", "source": "Stooq/BI.F", "reliabilityNote": "..." }
  },
  "forwards": {
    "copper": {
      "spot": { "price": 5.757, "symbol": "HG=F",      "expiry": "2026-03" },
      "near": { "price": 5.757, "symbol": "HGK26.CMX", "expiry": "2026-05" },
      "far":  { "price": 5.873, "symbol": "HGU26.CMX", "expiry": "2026-09" }
    }
  },
  "inventory": { "copper": null, "note": "LME blocked by Cloudflare (403)" },
  "news": [ { "title": "...", "url": "..." } ],
  "ibNews": [ { "title": "Goldman Sachs expects copper...", "url": "..." } ],
  "forumSentiment": {
    "smmHighlights": "【SMM快訊】...",
    "redditSummary": "[31↑] Copper supply concerns...",
    "redditSurging": "[🔥] Sudden copper mine shutdown...",
    "xueqiuSummary": null
  }
}
```

## Data Sources & Status

| Source | Status | Data |
|--------|--------|------|
| Yahoo Finance (HG=F) | ✅ Free | Copper USD spot + forward contracts |
| Yahoo Finance (ALI=F) | ✅ Free | Aluminum USD spot |
| Yahoo Finance (ZNC=F) | ❌ Disabled | Stale prevClose (2019), changePct unreliable |
| CCMN 長江有色 | ✅ Free | Cu/Zn/Ni/Co/Pb/Sn + 30 metals CNY |
| Stooq (BI.F) | ⚠️ Unreliable | Bismuth USD/t, price validity unconfirmed |
| LME official | ❌ Cloudflare 403 | All 3 fetch methods blocked |
| SMM 上海有色 | ✅ Headlines free | Flash news, prices require login |
| Reddit r/Commodities | ✅ JSON API | Top + Hot + surging detection |
| Google News RSS | ✅ Free | CN metals news + EN IB analysis |
| 雪球 Xueqiu | 🔒 Login required | Not implemented |

## Known Limitations

- **LME inventory**: All fetch methods return HTTP 403 (Cloudflare). Reported as `null` in output.
- **Bismuth (Bi)**: Stooq `BI.F` price ($2,272/t) is below market average ($6,600–$13,200/t). Reliability unconfirmed — use with caution.
- **Zinc USD**: Yahoo `ZNC=F` has a stale `prevClose` from 2019, making `changePct` meaningless. Disabled; CNY via CCMN still works.
- **Nickel/Cobalt USD**: Yahoo Finance has no LME Ni/Co contracts. CNY via CCMN only.

## 声明（ClawHub 发布要求）

- 本项目仅提供公开数据的整理与研究，不构成投资建议或收益承诺。
- 所有行情与资讯来自第三方公开来源，可能存在延迟、缺失或口径差异，请在交易前二次核验。
- 趋势与预警信号用于辅助决策，不替代仓位管理、风控纪律与独立判断。
- 项目不包含付费接口密钥、侵权数据或绕过访问控制的实现。

## License

MIT
