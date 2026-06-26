---
name: gold-monitor
description: 查询实时金价、黄金价格、美元指数、原油价格、金油比及投资建议。Query real-time gold price (Au99.99/COMEX/XAU), USD index (DXY), WTI oil price, and Gold/Oil ratio with investment signals. 支持今日金价、国际金价、大宗商品行情、金油比分析。
---

# Gold Monitor

实时贵金属与大宗商品价格查询工具，含金油比（Gold/Oil Ratio）投资信号分析。数据来源：上海黄金交易所 (SGE)、COMEX、新浪财经。

## When to Use

Use this skill when the user asks about:
- 金价 / 黄金价格 / 今日金价 / 实时金价 / gold price / gold rate
- 国际金价 / COMEX金价 / XAU/USD / XAUUSD / 伦敦金
- 中国金价 / 国内金价 / Au99.99 / 上海金 / SGE金价
- 美元指数 / DXY / USD index / 美元走势
- 原油价格 / 油价 / WTI / crude oil / 国际油价
- 大宗商品行情 / 贵金属行情 / commodity prices
- 金价走势 / 金价涨跌 / 黄金涨了吗 / 金价多少
- 金油比 / gold oil ratio / 黄金原油比 / 大宗商品投资信号 / 现在适合买黄金吗

## Setup

Before first use, install dependencies:

```bash
pip install -r {{SKILL_DIR}}/requirements.txt
```

## Usage

Query all assets at once (includes gold-oil ratio):

```bash
python3 {{SKILL_DIR}}/query.py all
```

Query a single asset:

```bash
python3 {{SKILL_DIR}}/query.py AU9999    # China gold (CNY/gram)
python3 {{SKILL_DIR}}/query.py XAUUSD   # International gold (USD/oz)
python3 {{SKILL_DIR}}/query.py USIDX    # USD index (DXY)
python3 {{SKILL_DIR}}/query.py WTI      # WTI crude oil (USD/barrel)
python3 {{SKILL_DIR}}/query.py GORATIO  # Gold/Oil ratio + investment advice
```

## Output

For price assets, the script prints JSON to stdout:

```json
{
  "name": "国际黄金 COMEX",
  "symbol": "XAUUSD",
  "price": 3050.12,
  "change": 15.30,
  "change_pct": 0.50,
  "unit": "USD/oz",
  "update_time": "2026-03-27 10:30:00"
}
```

For `GORATIO`, the output includes ratio value, level, signal, and advice:

```json
{
  "symbol": "GORATIO",
  "name": "金油比",
  "ratio": 32.5,
  "gold_price": 3050.12,
  "oil_price": 93.85,
  "level": "偏高",
  "signal": "🟠 避险情绪偏强",
  "advice": "金油比高于历史均值，反映经济下行预期...",
  "update_time": "2026-03-27 10:30:00"
}
```

For `all`, the output is an array of 5 objects (4 prices + 1 ratio).

If an `"error"` field is present, that asset's data could not be fetched — tell the user.

## Gold/Oil Ratio Reference

| Level | Range | Signal | Meaning |
|-------|-------|--------|---------|
| 极度偏高 | >40 | 🔴 | Recession/crisis signal (COVID 2020 peak ~70) |
| 偏高 | 25-40 | 🟠 | Risk-off sentiment, economic slowdown |
| 正常 | 15-25 | 🟡 | Historical average (~16-17), balanced |
| 偏低 | 10-15 | 🟢 | Economic expansion, commodities strong |
| 极度偏低 | <10 | 🔵 | Oil overvalued / inflation shock |

Parse the JSON and present prices clearly with values, changes, and units. For GORATIO, highlight the `signal` and present `advice` as investment guidance.

## Network Access

This skill makes outbound HTTP requests to the following hosts only:
- `hq.sinajs.cn` — Sina Finance real-time quotes (international gold, USD index, WTI oil)
- akshare API endpoints — Shanghai Gold Exchange data (China gold Au99.99)

No credentials or API keys are required. All requests are read-only.

## Data Sources

- **China Gold (Au99.99)** — Shanghai Gold Exchange via akshare
- **International Gold (COMEX)** — Sina Finance real-time quotes
- **USD Index (DXY)** — Sina Finance real-time quotes
- **WTI Crude Oil** — Sina Finance real-time quotes
- **Gold/Oil Ratio** — Computed from COMEX gold ÷ WTI oil
