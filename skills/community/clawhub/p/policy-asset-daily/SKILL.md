---
name: policy-asset-daily
description: "Policy-Asset Linkage Daily Report generator. Produces a bilingual (Chinese/English) single-file HTML report analyzing the transmission chain from political policy and macro signals to energy, commodities, FX, and capital markets. This skill should be used when the user asks for policy daily report, asset linkage, generate topic page, or any request to generate a daily macro strategy report linking policy events to asset class movements. Triggers: daily macro briefing, policy-asset linkage analysis, political-economic daily report, bilingual HTML market report."
agent_created: true
version: 1.0.0
---

# Policy-Asset Linkage Daily Report

## Overview

Generate a single-file, fully self-contained bilingual (Chinese/English) HTML report
that analyzes the linkage between political policy events and asset market movements
for the current system date. The report follows a macro-strategy analyst perspective,
covering five domains: political policy (including state media), international macro,
energy industry, commodities/FX, and capital markets. Output is a polished HTML page
with one-click language toggle, data-visualization aesthetic, and policy sections
highlighted to reflect their source-level importance.

## Role

Adopt the persona of a senior macro-strategy analyst specializing in interpreting the
linkage between political policy, energy, international macro, and capital markets.
Maintain analytical rigor, avoid speculation beyond what evidence supports, and clearly
distinguish between established facts and scenario-based reasoning.

## Trigger Keywords

This skill activates on: "政策日报", "资产联动", "生成专题页", "政策资产联动日报",
"政策资产联动", "macro daily", "policy-asset report".

## Information Gathering

Use WorkBuddy's web search and web fetch capabilities to retrieve real-time news and
information across the following domains:

### Search Domains

1. **Political Policy** (highest priority): Central government policy decisions, State
   Council executive meetings, gov.cn announcements, Xinhua News Agency headlines,
   People's Daily front-page reports, important speeches, Five-Year Plan updates,
   industry regulatory new policies, fiscal and tax reforms.

2. **International Macro**: Federal Reserve, ECB and other major central bank policies,
   geopolitical events, US/EU/emerging markets major macro dynamics.

3. **Energy Industry**: Crude oil, natural gas, new energy policies and price movements.

4. **Commodities/FX**: Gold, copper, US Dollar Index, RMB exchange rate, and other key
   commodities.

5. **Capital Markets**: A-shares, Hong Kong stocks, US stock major index trends and
   significant events.

### Source Priority

Refer to `references/news_sources.md` for the full ranked list of preferred sources.
Top-priority sources include: Xinhua, People's Daily, CCTV News Network, gov.cn,
CLS (财联社), Reuters, Bloomberg, Sina Finance, Eastmoney (东方财富).

### Time Dimensions

Search across three time dimensions relative to the report date:
- **Short-term**: Current day and the nearest 3 trading days
- **Medium-term**: Past month to one quarter
- **Long-term**: Past year

If same-day data is insufficient, trace back to the most recent 3 trading days.

## Workflow

### Step 1: Determine Report Date

Obtain the current system date. This becomes the report date. The date must auto-update
each time the skill runs — never use a fixed date from examples.

### Step 2: Multi-Domain News Search

Execute web searches across all five domains. For each domain:
- Search for the most recent news (short-term focus first)
- Collect source name, publication time, headline, and URL
- Aim for 5-10 raw items per domain

### Step 2.5: Key Prices Data Collection

Search for the latest prices and rates for the following categories. These will
populate the "Key Prices Dashboard" section (see Report Structure section 0):

1. **Precious Metals & Energy**: Spot gold (XAU/USD), COMEX gold futures,
   **上金所 Au9999 (国内现货金)**, **沪金主力 SHFE (国内期货金)**,
   **黄金T+D**, **周大福/老凤祥足金饰品零售价**,
   Brent crude, WTI crude, silver (optional)
2. **Cryptocurrency**: Bitcoin (BTC/USD), Ethereum (ETH/USD)
3. **FX & Commodities**: US Dollar Index (DXY), USD/CNY (onshore), USD/CNH (offshore),
   LME copper, natural gas (optional)
4. **Policy Rates & Bond Yields**: China 1Y LPR, China 5Y+ LPR, Fed funds rate,
   PBOC 1Y MLF rate, China 10Y government bond yield, US 10Y Treasury yield
5. **Global Stock Indices**: Shanghai Composite, Hang Seng, Dow Jones, S&P 500,
   Nasdaq Composite, Nikkei 225

For each price, record: value, daily change (%), source name, and update time.
Use Chinese stock market convention: red for increase (涨), green for decrease (跌).

### Step 3: Deduplication and Validation

- Remove duplicate reports across sources
- Verify each item has a real source and publication time
- Discard items lacking verifiable attribution
- Record: total raw count, deduplicated count, effective rate

### Step 4: Short-Term Core Events Extraction

Identify events from the current day or nearest 3 trading days that have direct market
sentiment impact (e.g., Politburo meetings, State Council meetings, major personnel
changes, geopolitical conflicts, sudden regulatory actions, major company moves). For
each, attach specific timing and brief impact analysis.

### Step 5: Policy-to-Asset Linkage Analysis

Construct the transmission chain from political policy / state media signals to energy,
commodities, FX, and stock markets. Express as a flow diagram (text-based or styled
HTML flow). See `references/linkage_framework.md` for the standard transmission model.

### Step 6: Scenario Reasoning

Develop 2-3 hypothesis-based forward-looking scenarios grounded in the day's news.
Format: "If [source] recently signals [topic], then [policy] may be forthcoming,
benefiting [sector/asset]."

### Step 7: Generate Bilingual HTML

Produce the final single-file HTML report using the template in
`assets/report_template.html` as the structural base. All CSS and JS must be inline.
The report must support one-click Chinese/English toggle in the top-right corner.

## Report Structure (Mandatory Sections)

The final HTML report must contain the following sections in order:

0. **Key Prices Dashboard** (📊 关键价格仪表盘): Placed immediately after the header.
   Includes a TradingView real-time ticker tape widget at the top (auto-updating, includes
   international gold XAU/USD and domestic gold SHFE:AU1!), followed
   by categorized price cards with the latest data searched in Step 2.5. Categories:
   Precious Metals & Energy (including domestic gold: Au9999, SHFE gold futures, gold T+D,
   retail jewelry gold price), Cryptocurrency, FX & Commodities, Policy Rates & Bond Yields,
   Global Stock Indices. Each card shows: name, value, daily change (red=up, green=down per
   Chinese convention), source, and time. This section provides an at-a-glance market overview.

1. **Short-Term Core Events** (📌 短期核心事件): Listed at the very front. Each entry
   includes specific time and brief impact analysis. This is the most prominent section.

2. **Core Judgment** (核心判断): One-paragraph summary of the day's market mainline logic.

3. **Data Collection Stats** (抓取与去重统计): News source count, raw items, deduplicated
   count, effective rate.

4. **Policy-to-Asset Linkage Diagram** (政策→资产联动链路图): Full transmission path from
   political policy/state media to energy, commodities, FX, equities.

5. **News by Chapter** (重点新闻分章节), strictly ordered:
   - **Political Policy** (政治政策) — MUST appear first, highlighted/bolded. Must
     separately list CCTV News Network / Xinhua / People's Daily core reports.
   - **International Macro** (国际宏观)
   - **Energy Industry** (能源产业)
   - **Commodities/FX** (商品/外汇)
   - **Capital Markets** (资本市场)

6. **Scenario Observations** (复盘观察情景): 2-3 hypothesis-based forward-looking scenarios.

### News Item Format

Each news entry must follow this format:
```
[时间] [来源] [简述] | 市场含义：xxx | 原文链接：[URL]
[Time] [Source] [Summary] | Market Implication: xxx | Source Link: [URL]
```

## Data & Authenticity Constraints

- All content must be based on real-world political-economic logic and verifiable news
  events. NEVER fabricate news that does not exist.
- Each news item must have a real source and publication time.
- If a domain has no major news on the day, mark "当日无重大更新" (No major updates
  today) and briefly cite the most recent relevant prior news.
- Do not fabricate specific macro data. If real data is unavailable, mark "待公布"
  (pending release) or use logical reasoning.
- Prefer sources from `references/news_sources.md`. For paywalled or inaccessible
  pages, use web fetch to retrieve publicly accessible content.

## HTML Design Requirements

- Single file, fully self-contained (all CSS/JS inline). Exception: the TradingView
  ticker tape widget loads an external script for real-time price data — this is the
  only external dependency and is acceptable.
- Bilingual: Chinese and English, one-click toggle in the top-right corner
- Clean, data-visualization aesthetic
- Political Policy section must be bolded/highlighted to reflect its source-level status
- Use color-coded section headers for the five domains
- Responsive layout
- Dark/light theme support preferred
- The template in `assets/report_template.html` provides the base structure, CSS
  variables, and JS toggle logic. Customize content areas but preserve the core
  framework.

## Output

Output the final HTML file to the workspace and present it to the user via the
present_files tool. The filename should follow the pattern:
`policy-asset-daily-YYYY-MM-DD.html`.

## Resources

### references/

- `news_sources.md` — Ranked list of preferred news sources by domain, with source
  reliability tiers and URL patterns for search.
- `linkage_framework.md` — Standard policy-to-asset transmission model and diagram
  structure guide.

### assets/

- `report_template.html` — Base HTML template with bilingual toggle, inline CSS,
  section layout, and placeholder content areas. Use as the structural starting point.
