---
name: market-news-aggregator
description: Aggregate, classify, summarize, and analyze market news from Chinese financial portals (Sina Finance, EastMoney, Hexun, Jin10). Use for (1) pre-market briefing on overnight news, (2) intraday real-time alerts for market-moving events, (3) end-of-day news review. Supports sector classification, sentiment tagging, keyword extraction, and importance ranking.
emoji: 📰
---

# Market News Aggregator — 市场新闻聚合

## Overview

聚合国内财经网站新闻，按品种/板块分类，生成摘要、提取关键词、判断情绪（偏多/偏空/中性），并按重要度排序。适用于盘前/盘中/盘后三个场景。

## Data Sources — 数据源

| Source | URL | Coverage | Notes |
|:-------|:----|:---------|:------|
| 新浪财经 | `https://finance.sina.com.cn/` | 要闻、宏观、行业、个股 | 资讯页可导航 |
| 东方财富 | `https://www.eastmoney.com/` | 快讯、研报、公告、宏观 | 滚动新闻量最大 |
| 和讯网 | `https://www.hexun.com/` | 期货、外汇、宏观 | 偏大宗商品 |
| 金十数据 | `https://www.jin10.com/` | 实时快讯、数据公布、事件预警 | 速度快、偏交易 |

### News Categories — 分类体系

```
宏观宏观 — 宏观经济政策、GDP、CPI、PMI、利率、汇率
农产品 — 大豆、玉米、棉花、白糖、生猪、鸡蛋等
有色 — 铜、铝、锌、铅、镍、锡、黄金、白银
黑色 — 铁矿石、螺纹钢、焦煤、焦炭、热卷
能源化工 — 原油、甲醇、PTA、纯碱、尿素、橡胶、燃料油
股指 — IF、IC、IH、IM 及大盘指数
```

## Workflow

### Step 1: Determine Fetch Target

Based on the user's request, pick the right source(s) and category:

| Scenario | Recommended Source(s) | Depth |
|:---------|:---------------------|:------|
| 盘前隔夜消息 (pre-market) | 新浪财经 + 金十数据 | 综合 |
| 盘中异动 (intraday alert) | 金十数据 快讯 | 实时 |
| 盘后回顾 (EOD review) | 东方财富 + 新浪财经 | 深度 |
| 特定品种 (specific product) | 和讯网 | 垂直 |

### Step 2: Fetch Using web_fetch

Use the `web_fetch` tool with `extractMode=text` to get clean text content. Set `maxChars` appropriately:

```yaml
web_fetch:
  url: "<source-url>"
  extractMode: text
  maxChars: 8000   # per page, enough for ~5-10 headlines + snippets
```

**Example fetches:**

- 新浪财经要闻: `https://finance.sina.com.cn/`
- 新浪财经期货: `https://finance.sina.com.cn/futures/`
- 东方财富快讯: `https://www.eastmoney.com/`
- 金十数据: `https://www.jin10.com/`

**Respect robots.txt**: Use moderate fetch intervals and reasonable maxChars. Do not scrape at high frequency.

### Step 3: Classify News by Sector

Parse fetched text and classify each news item. Look for **keywords** in headline and body:

| Sector | Trigger Keywords |
|:-------|:----------------|
| 宏观 | 央行、MLF、降准、降息、GDP、CPI、PMI、进出口、美联储、非农、加息、数据 |
| 农产品 | 豆粕、豆油、玉米、棉花、白糖、生猪、鸡蛋、棕榈、菜油、USDA |
| 有色 | 铜、铝、锌、铅、镍、锡、黄金、白银、LME、库存、矿 |
| 黑色 | 螺纹、铁矿、焦煤、焦炭、热卷、限产、粗钢、地产、基建 |
| 能源化工 | 原油、甲醇、PTA、纯碱、尿素、橡胶、燃料油、OPEC、EIA、炼厂 |
| 股指 | 沪指、创业板、上证、深证、北向、涨停、成交量、A股 |

**Output format** — group news under their sector heading:

```
### 🏛️ 宏观宏观
1. [标题] — 摘要（来源，时间）
2. [标题] — 摘要（来源，时间）
```

### Step 4: Generate Summary (AI)

For each news item (or at least the top 5-8 most important ones), produce a **one-line summary**:

- **Length**: 20-40 Chinese characters max
- **Style**: Concise, fact-only, no opinion
- **Focus**: What happened + why it matters to markets

Example:
```
❌ 不好: "央行宣布降准0.5个百分点，市场流动性得到改善"
✅ 好: "央行降准0.5%，释放长期资金约1万亿"
```

### Step 5: Extract Keywords

Extract 2-5 key terms per news item. Prioritize **actionable terms** that traders care about:

- Policy actions: "降准", "加息", "限产", "收储"
- Price levels: "突破 XXXX", "创 X 年新高"
- Supply/demand: "减产", "累库", "检修", "开工率"
- Events: "交割", "移仓", "基差", "价差"

### Step 6: Sentiment Analysis

Tag each news item with a **sentiment direction**:

| Tag | Meaning | When to Use |
|:----|:--------|:------------|
| 🟢 **偏多** | 利好/利多 | Positive for price (supply cut, policy support, strong demand) |
| 🔴 **偏空** | 利空/利淡 | Negative for price (supply surge, policy tightening, weak data) |
| ⚪ **中性** | 中性/无明确方向 | Informational, mixed signals, or unclear impact |

Apply sentiment **relative to the sector/contract**, not the general economy. E.g., "原油增产" = 🔴 偏空 for oil.

### Step 7: Importance Ranking

Rank news items by **market impact** (high → low):

| Level | Score | Criteria |
|:------|:------|:---------|
| 🔴 **重大** | ★★★ | Policy shifts, unexpected data, major supply disruption |
| 🟡 **重要** | ★★ | Routine data release, moderate supply change, meeting results |
| ⚪ **一般** | ★ | Commentary, ordinary operations, non-market-moving |

### Step 8: Format Final Output

Use this output format as the final presentation:

```
📰 市场新闻聚合 — [日期/时段]

━━━ 🔴 重大关注 ━━━

1. [标题]（来源）
   摘要：XXX
   关键词：XXX, XXX
   情绪：🟢 偏多 / 🔴 偏空 / ⚪ 中性

2. ...

━━━ 🟡 重要信息 ━━━

...

━━━ ⚪ 一般资讯 ━━━

...

━━━ 📊 分板块汇总 ━━━

🏛️ 宏观宏观：[N] 条 | 🟢X  🔴X  ⚪X
🌾 农产品： [N] 条 | 🟢X  🔴X  ⚪X
🏭 有色：   [N] 条 | 🟢X  🔴X  ⚪X
⛏️ 黑色：   [N] 条 | 🟢X  🔴X  ⚪X
🛢️ 能源化工：[N] 条 | 🟢X  🔴X  ⚪X
📈 股指：   [N] 条 | 🟢X  🔴X  ⚪X
```

## Usage Scenarios

### 盘前（Pre-market, 08:00-08:30）

1. Fetch from 新浪财经 + 金十数据
2. Focus on **overnight** (隔夜) — US markets, EU markets, macro data releases
3. Special attention to: USDA reports, EIA data, Fed speeches, OPEC statements
4. **Goal**: Identify what moved overnight and prepare for 09:00 open

**Quick check command:**
```yaml
web_fetch:
  url: "https://www.jin10.com/"
  extractMode: text
  maxChars: 6000
```

### 盘中（Intraday, 09:00-15:00）

1. Check 金十数据 快讯 every 30-60 minutes
2. Key triggers: sudden price spikes, volume surges, government announcements
3. Filter for: **品种关键词** that match the user's current positions
4. **Goal**: Alert on real-time catalysts affecting open positions

### 盘后（EOD, 15:00-17:00）

1. Fetch from 东方财富 + 新浪财经 — deeper coverage
2. Summarize **all** market-moving news from the day
3. Include: data calendar (what came out, actual vs expected), policy announcements
4. **Goal**: Provide a complete picture for end-of-day position review

## Scripts

### `scripts/fetch_news.py`

A Python script for batch fetching from multiple sources. Use when the user needs a consolidated multi-source fetch (not individual page fetches via web_fetch).

```bash
python scripts/fetch_news.py --sources sina,jin10 --sectors macro,agri --max-items 20
```

**Parameters:**
- `--sources`: Comma-separated source list (sina, eastmoney, hexun, jin10)
- `--sectors`: Filter by sector keywords
- `--max-items`: Max items to return (default 20)
- `--output`: Output format (text, json)

## Important Notes

- **Don't over-fetch**: One fetch per source per scenario is enough. ~5-8k chars per fetch.
- **Source attribution**: Always include the source name for each news item — credibility matters.
- **Timestamps**: Include approximate time if available (e.g., "10:23", "昨夜").
- **Cross-reference**: When a key event is reported differently across sources, note discrepancies.
- **No forward-looking statements**: Summarize what happened, don't predict outcomes.
- **Respect robots.txt**: Do not scrape at high frequency; reasonable intervals only.
