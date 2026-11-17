---
name: industry-prosperity-tracker
display_name: 板块景气度查询
description: >
  跟踪任意行业景气度，用 A 股龙头股财务数据 + 宏观指标（PMI/PPI/进出口）计算综合景气评分（0-100），
  判断行业处于上行周期、下行周期还是拐点区域。支持内置行业（半导体、医药、新能源、消费品）和任意自定义行业。
category: finance
emoji: 📊
author: sunso
version: 2.0.3
license: MIT
tags:
  - finance
  - industry-research
  - macro-data
  - stock-analysis
trigger_keywords:
  - 行业景气度
  - 景气跟踪
  - 半导体景气
  - 消费景气
  - 新能源景气
  - 医药景气
  - 行业周期
  - 高频指标跟踪
  - 景气分
  - prosperity tracker
  - industry cycle
  - boom indicator
---

# 板块景气度查询

## What this Skill does

When a user wants to track an industry's prosperity / business cycle status, this Skill:

1. Identifies the industry (built-in sector or user-specified custom sector)
2. Selects representative leading stocks for that industry (from built-in config or AI knowledge)
3. Fetches the latest macro + stock financial data via `scripts/fetch_indicators.py` (using free public data sources only via AKShare)
4. Calculates a composite prosperity score (0-100) via `scripts/calculate_score.py`
5. Generates a one-page prosperity dashboard via `scripts/generate_report.py` using `assets/report_template.html`
6. Outputs: overall score, direction judgment, indicator detail table, key signals, compliance disclaimer

## Architecture: Universal Engine + Dynamic Stock Selection

This Skill uses a **generic indicator framework** that works for any industry:

**Universal Macro Layer (40% weight, same for all industries):**
- Leading: Official PMI (15%), Caixin PMI (15%), PPI YoY (10%)
- Coincident: Export YoY (15%), Import YoY (10%)

**Dynamic Stock Layer (60% weight, per-industry):**
- Coincident: Leading stocks' quarterly revenue QoQ (15%, auto-split among stocks)
- Lagging: Leading stocks' quarterly gross margin QoQ (20%, auto-split among stocks)

Weights are **automatically distributed** based on the number of stocks provided. No manual weight configuration needed.

## How to use

### Step 1: Identify the industry

When a user says something like "看医药行业景气度" or "帮我跟踪新能源板块":

1. Check if the industry is in `BUILTIN_SECTORS` (see `scripts/fetch_indicators.py`):
   - `semiconductor` (半导体): 北方华创, 韦尔股份
   - `pharma` (医药): 恒瑞医药, 药明康德, 片仔癀
   - `new_energy` (新能源): 宁德时代, 比亚迪
   - `consumer` (消费品): 贵州茅台, 五粮液

2. If built-in: use directly.

3. If NOT built-in (e.g. user says "看军工行业"):
   - **You (the AI) select 2-5 representative leading stocks** for that industry based on your knowledge
   - Example for 军工: 600760(中航沈飞), 002179(中航光电), 000768(中航西飞)
   - Pass them via `--stocks` parameter: `--stocks "600760:中航沈飞,002179:中航光电,000768:中航西飞" --sector-name "军工"`

### Step 2: Fetch data

Run `scripts/fetch_indicators.py`:

```bash
# Built-in industry
python scripts/fetch_indicators.py --sector semiconductor

# Custom industry (AI picks stocks)
python scripts/fetch_indicators.py --sector military --sector-name "军工" \
    --stocks "600760:中航沈飞,002179:中航光电,000768:中航西飞"

# List all built-in sectors
python scripts/fetch_indicators.py --list-sectors
```

Output: `data/{sector}_latest.json`

### Step 3: Calculate score

```bash
python scripts/calculate_score.py --input data/{sector}_latest.json --output data/{sector}_scored.json
```

### Step 4: Generate report

```bash
python scripts/generate_report.py --input data/{sector}_scored.json --output output/{sector}_report.html
```

### Step 5: Present

Present the generated HTML report to the user with a summary of the score and key signals.

## AI Stock Selection Guidelines

When selecting representative stocks for a new industry, choose stocks that are:
1. **Market leaders** in their sub-sector (top revenue or market cap)
2. **Representative of the industry's value chain** (not just one sub-segment)
3. **Listed on A-share exchanges** (6-digit codes: 6xxxxx SH or 0/3xxxxx SZ)
4. **Have at least 4 quarters of financial data** (needed for QoQ calculation)
5. **Pure-play or industry-dominant** (avoid conglomerates where the industry is a minor segment)

Good examples:
- 军工: 中航沈飞(600760), 中航光电(002179), 中航西飞(000768) — covers aircraft + components
- 化工: 万华化学(600309), 华鲁恒升(600426) — covers PU + coal chemical
- 房地产: 保利发展(600048), 招商蛇口(001979) — covers top developers
- 银行: 招商银行(600036), 兴业银行(601166) — covers retail + interbank

## Built-in industries

| Sector ID | Name | Stocks | Indicators |
|-----------|------|--------|------------|
| semiconductor | 半导体 | 北方华创(002371), 韦尔股份(603501) | 9 (5 macro + 4 stock) |
| pharma | 医药 | 恒瑞医药(600276), 药明康德(603259), 片仔癀(600436) | 11 (5 macro + 6 stock) |
| new_energy | 新能源 | 宁德时代(300750), 比亚迪(002594) | 9 (5 macro + 4 stock) |
| consumer | 消费品 | 贵州茅台(600519), 五粮液(000858) | 9 (5 macro + 4 stock) |

To add a new built-in industry: add an entry to `BUILTIN_SECTORS` dict in `scripts/fetch_indicators.py`.

## Data sources

All data sources are from the compliance whitelist. See `references/data_sources.md` for details.

Key principle: this Skill uses free public data exclusively via AKShare open-source library. Data sources include National Bureau of Statistics (PMI, PPI), Customs General Administration (exports, imports), and exchange-disclosed financial reports (stock Financial Abstract). No paid terminal data (Wind, Bloomberg, iFinD) is used.

## Compliance

This Skill provides data aggregation and indicator calculation only. It does NOT:
- Recommend buying or selling any security
- Predict price movements or returns
- Provide target prices or investment ratings
- Guarantee any investment outcome

Every output includes the disclaimer:
"本工具仅提供数据整理和指标计算服务，不构成任何投资建议。历史数据不代表未来表现。数据可能存在延迟。"

See the bottom of `assets/report_template.html` for the fixed disclaimer footer.

## Scoring methodology summary

- Each indicator is scored: +1 (improving), 0 (flat), -1 (deteriorating) based on MoM/QoQ change
- Weighted sum produces a raw score in [-1, +1]
- Converted to 0-100 scale: score = (raw + 1) * 50
- Interpretation: >60 = upcycle, 40-60 = neutral/turning, <40 = downcycle
- 3-period moving average applied for trend smoothing

See `references/scoring_methodology.md` for full details.

## Output format

The report includes:
- Industry name and reporting period
- Composite prosperity score (0-100) with visual gauge
- Direction indicator (upcycle / downcycle / turning point)
- Indicator detail table (name | latest value | MoM change | direction | weight | contribution)
- Top 3 positive signals and top 3 negative signals
- 6-month historical score trend
- Compliance disclaimer footer
