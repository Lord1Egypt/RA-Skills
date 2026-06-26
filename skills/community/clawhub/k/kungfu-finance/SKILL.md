---
name: kungfu_finance
description: Mainland China A-share stock and sector analysis tool (中国A股个股与板块分析). Current repo build focuses on stable deterministic products for stock snapshots, basic finance indicators, chip/price levels, sector detail lookup, plus bucket, phase-2 strategy, researcher, bayesian monitor, and preview stock/sector deep research flows.
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"skillKey":"kungfu_finance","always":false,"requires":{"bins":["node"],"optionalBins":["inkscape"],"env":["KUNGFU_OPENKEY"]},"primaryEnv":"KUNGFU_OPENKEY","install":{"node":{"packageManager":"none","bundledScripts":true}},"runtime":"bundled-node-scripts","networkSurface":["tianshan-api.kungfu-trader.com","push2.eastmoney.com","push2his.eastmoney.com","qt.gtimg.cn","ifzq.gtimg.cn","wry-manatee-359.convex.site","clawhub.ai"],"fileWrites":["~/.openclaw/workspace/finance-master/charts/","~/.openclaw/.env"],"subprocesses":["inkscape (execFileSync, fixed args, SVG→PNG conversion only)"],"homepage":"https://github.com/kungfu-trader/kungfu-skills","publisher":{"name":"kungfu-trader","contact":"https://github.com/kungfu-trader"}}}
---

# 功夫财经 | KungfuFinance

## Publisher

- **Organization**: [kungfu-trader](https://github.com/kungfu-trader)
- **Source repository**: [github.com/kungfu-trader/kungfu-skills](https://github.com/kungfu-trader/kungfu-skills)
- **Tianshan API operator**: kungfu-trader (same organization)

## Runtime Model

- **Local runtime**: Node.js `.mjs` scripts (bundled executable scripts with zero npm dependencies — no `npm install` needed)
- **Outbound APIs**:
  - `https://tianshan-api.kungfu-trader.com` — deterministic products (snapshot, finance, bucket, strategy, researcher, bayesian monitor)
  - `https://push2.eastmoney.com` / `https://push2his.eastmoney.com` — stock/sector deep research market data (free public API, no key required)
  - `https://ifzq.gtimg.cn` / `https://qt.gtimg.cn` — fallback market data via Tencent Finance (free public API, no key required)
  - `https://wry-manatee-359.convex.site` / `https://clawhub.ai` — check-update version query (ClawHub registry, public, no key required)
- **Authentication**: `KUNGFU_OPENKEY` environment variable, sent as `Authorization: Bearer <token>` (Tianshan API only; EastMoney/Tencent/ClawHub APIs require no authentication)
- **Platform header**: `KUNGFU_PLATFORM` (optional, defaults to `openclaw`)
- **File I/O**: reads bundled assets; indicator-chart flow writes SVG/PNG to `~/.openclaw/workspace/finance-master/charts/`
- **Subprocesses**: indicator-chart flow invokes `inkscape` for SVG→PNG conversion; no other subprocesses

All environment variables are read from the host process; none are accepted from user prompts.

### Optional Research Search Surface

When separately configured, stock/sector deep research may call an additional search endpoint.
This surface is **independent** from the Tianshan API and uses its own credential boundary:

| Env Var | Purpose |
|---------|---------|
| `KUNGFU_ENABLE_RESEARCH_SEARCH` | Set to `1` to enable |
| `KUNGFU_RESEARCH_SEARCH_PROVIDER` | Provider name (currently `web_search`) |
| `KUNGFU_RESEARCH_SEARCH_ENDPOINT` | Search service URL |
| `KUNGFU_RESEARCH_SEARCH_API_KEY` | Search service credential |
| `KUNGFU_RESEARCH_SEARCH_TIMEOUT_MS` | Search request timeout (default: 15000) |

When search is enabled, requests are POSTed as JSON to `KUNGFU_RESEARCH_SEARCH_ENDPOINT` with `KUNGFU_RESEARCH_SEARCH_API_KEY` as Bearer token.
`KUNGFU_OPENKEY` is **never** reused for search requests.
If search is enabled but misconfigured, the result returns `misconfigured` status instead of silently failing.

### Non-Secret Tuning Variables

| Env Var | Purpose |
|---------|---------|
| `KUNGFU_ENABLE_EXPERIMENTAL_PRODUCTS` | Set to `1` to enable unreleased products |
| `KUNGFU_RESEARCH_DEFAULT_TARGET_DATE` | Override default research date (YYYYMMDD format, for testing) |

## Rollout Status

- Deterministic products (snapshot, finance, bucket, strategy, researcher, bayesian monitor) use revalidated Tianshan backend routes
- Preview `stock-research` / `sector-research` use public EastMoney/Tencent APIs for market data — no backend dependency for these flows
- Experimental products require `KUNGFU_ENABLE_EXPERIMENTAL_PRODUCTS=1`
- Preview `stock-research` / `sector-research` produce `markdown_svg_preview` with explicit degradation reporting

## Data Handling & Network Surface

- `KUNGFU_OPENKEY` is sent **only** to `tianshan-api.kungfu-trader.com` — never to EastMoney, Tencent, or any other host
- EastMoney and Tencent Finance APIs are public and require **no authentication**
- The code contacts **no other hosts** beyond those listed in the Runtime Model table above
- Do not use this skill with secrets, personal data, or other sensitive user content

## Scope

- Mainland China A-shares only
- Direct market-data lookup stays within one stock or one sector
- No arbitrary whole-market screening
- Not for US stocks
- Not for Hong Kong stocks
- Not for cryptocurrencies
- Not for futures or forex
- No free-form SQL
- No user-facing base URL
- No user-facing runtime credential parameters

## Public Intents

Route the user into the currently enabled intent families below.
Do not expose internal product names unless needed for implementation.

### 1. Stock Snapshot

Use when the user wants one A-share stock's current state, recent走势, K-line window, holders,筹码分布,支撑压力位, or other narrow deterministic data.

Default behavior:

- Prefer the narrowest data product that answers the question
- If the stock code is unknown, prefer `instrument_name`
- If code mode is used, `exchange_id` must be `SSE` or `SZE`

### 2. Finance Analysis

Use when the user wants one A-share stock's基础财务指标或基础财务上下文。

Default behavior:

- Prefer `finance_basic_indicators` for narrow factual questions
- Prefer `finance_context` for lightweight finance context

### 3. Sector Analysis

Use when the user asks about one A-share industry or sector.

Default behavior:

- deterministic sector detail products may still use `sector_name`
- fuzzy sector resolution is not exposed as a standalone public product, but `sector-research` resolves theme words by matching against the full EastMoney concept sector list
- preview `sector-research` accepts `sector_name` or `sector_id` directly; when the local resolver cannot disambiguate, it returns `needs_input` for the user to provide a BK code

### 3C. Sector Deep Research

Use when the user wants one A-share sector's deep research, hype-cycle view, thematic thesis, dragon-head observation, committee-style bull/bear review, or a longer structured report.

Default behavior:

- current runtime only supports one mainland China A-share sector per invocation
- the preview path accepts `sector_name` or `sector_id`; `target_date` is optional and defaults to the current market date in Asia/Shanghai
- the current version is `markdown_svg_preview` and returns explicit degradations for remaining search / adapter gaps
- the result surface now also exposes the migrated orchestration contract from the original `sector-analysis` skill
- the result surface now includes `report_svg` and `quality_gate`
- structured inputs now use public EastMoney APIs: concept sector list resolution, sector constituents, sector index K-line, and per-leader stock quotes and money flow
- the sector resolver matches user input against the full EastMoney concept sector list; if ambiguous, returns `needs_input` for the user to provide a BK code
- when the separate `web_search` runtime is enabled and configured, macro / policy / catalyst / industry-trend / competition / money-flow evidence may be attached as external search evidence (7 search buckets)
- otherwise the report must surface missing search evidence as degraded coverage instead of silently inventing facts

### 3B. Stock Deep Research

Use when the user wants one A-share stock's deep research, investment thesis, catalyst map, committee-style bull/bear review, or a longer structured report.

Default behavior:

- current runtime only supports one mainland China A-share stock per invocation
- the preview path accepts optional `target_date` and defaults it to the current market date in Asia/Shanghai
- the current version is `markdown_svg_preview` and returns explicit degradations for remaining search / adapter gaps
- the result surface now also exposes the migrated orchestration contract from the original `stock-analysis-v2` skill
- the result surface now includes `report_svg` and `quality_gate`
- structured market data now comes from public EastMoney APIs: real-time quote, daily K-line, real weekly K-line (klt=102, not aggregated from daily), and 20-day money flow; Tencent Finance APIs serve as fallback
- financial statements, company profile, and other non-market data are sourced from web search (8 search buckets: macro, catalyst, risk, competition, financials, company profile, governance, sector trend)
- when the separate `web_search` runtime is enabled and configured, these evidence buckets are populated; otherwise the report surfaces explicit degradations

### 4. Bucket Flow

Use when the user wants to:

- view current-user buckets
- choose one existing bucket
- add one or more instruments into that bucket

Default behavior:

- only operate on the current authenticated user's own buckets
- do not create or delete buckets in the current release build
- when adding a batch, resolve instruments first and filter invalid ones before writing
- when required information is missing or ambiguous, return a structured `needs_input` response so the host can continue the dialogue
- if all inputs are invalid, return `needs_input` for corrected instruments instead of calling the write API

### 5. Strategy Flow

Use when the user wants to:

- view public strategies
- view public strategies by market mode
- view current-user private strategies
- query one public or private strategy on one stock
- query one public or private select strategy's whole-market picks for one day or one date range
- count buy signals for one stock across eligible public paid strategies
- batch scan one public paid strategy across multiple stocks

Default behavior:

- strategy module requires runtime auth even when listing public strategies
- public and private strategies both support single-strategy query
- public and private select strategies both support controlled whole-market result query
- private strategies do not support first-stage batch scan
- batch scan only supports public strategies with non-empty `lago_plan`
- `market-select` supports `InstrumentSelect`, `TemplateInstrumentSelect`, `BuySell`, and `TemplateBuySell`
- when `market-select` is used on `BuySell` or `TemplateBuySell`, whole-market results only return buy points
- `market-select` accepts either `target_date`, or `strategy_start_date + strategy_end_date`
- if `market-select` mixes the two date modes, or only provides half of a range, return a structured `needs_input` response
- when strategy selector or stock input is missing or ambiguous, return a structured `needs_input` response so the host can continue the dialogue
- when the selected public paid strategy lacks permission for batch scan, return a structured `blocked` response instead of pretending the scan succeeded

### 6. Researcher Flow

Use when the user wants to:

- view top researchers by score
- view one stock's covered researchers together with report titles
- view one researcher's reports

Default behavior:

- researcher module requires runtime auth
- researcher backend also enforces `Journeyman` membership or above
- `stock-reports` is a composed flow built from researcher score plus researcher report list
- `author-reports` prefers `researcher-author-id`
- if the user only gives `researcher-name`, resolve it conservatively; if not unique, return `needs_input`
- do not pretend the backend supports direct global researcher-name search if it does not

### 7. Bayesian Monitor Flow

Use when the user wants to:

- view current-user bayesian monitor tasks
- choose one existing bayesian monitor task
- inspect that task's initial report and recent monitor records

Default behavior:

- bayesian monitor module requires runtime auth
- only operate on the current authenticated user's own tasks
- current release build is read-only: do not create, delete, or run bayesian monitor tasks
- `list` returns task summaries only and must not expose full `original_report`
- `reports` supports `bayesian-task-id` and conservative `bayesian-topic` resolution
- when task selector is missing or ambiguous, return a structured `needs_input` response so the host can continue the dialogue
- when the current user has no tasks, return a structured `blocked` response instead of pretending the task exists

### 8. Indicator Chart

Use when the user wants to see one A-share stock's technical indicator chart. The script automatically renders SVG, converts to PNG via inkscape, and returns file paths (no SVG text in stdout). Supported chart types:

- `kline` — K线图 (candlestick chart with optional chip distribution overlay, price level lines, and custom annotations)
- `lushan_shadow` — 庐山照影图 (CM mountain + FC shadow dual-bar chart)
- `lushan_4season` — 庐山四季图 (GG/HY/DP lines + RS bars + bottom resonance/strong markers)
- `shuanglun` — 双轮驱动图 (K-wheel + R-wheel stacked bars with trend coloring)
- `liumai` — 六脉神剑图 (6-signal heatmap matrix with buy/sell signal row)
- `smart_money` — 聪明钱图 (smart money vs follow money dual-line chart)
- `finance_score` — 个股综合得分 (radar chart with 行业统治力/财务健康度/发展前景 three-dimensional scoring)

K-line chart additional options:
- `--with-chip-peak true` — overlay chip distribution (筹码峰) on the right side
- `--with-price-levels true` — draw support/resistance/concentration price level lines (阻力位/支撑位)
- `--annotations '[{"date":"20260328","price":15.5,"type":"buy","label":"买入点","color":"#ef4444"}]'` — mark custom points on the chart

### 9. Finance Score

Use when the user wants one A-share stock's comprehensive scoring across three dimensions:
- 行业统治力 (Industry Dominance) — scored 0-5 with S/A/B/C/D/E grade
- 财务健康度 (Financial Health) — scored 0-5 with S/A/B/C/D/E grade
- 发展前景 (Growth Potential) — scored 0-5 with S/A/B/C/D/E grade
- 综合得分 (Total Score) — 0-15

Available as both a data product (`finance_score`) and a rendered SVG chart (`indicator-chart --chart-type finance_score`).

### 10. Subscription Flow (自选)

Use when the user wants to:

- view current-user subscribed instruments (自选列表)
- add instruments to subscription (加自选)
- remove instruments from subscription (删自选)
- view anomaly report for one subscribed instrument (异动报告)
- view aggregate anomaly summary (异动汇总)

Default behavior:

- only operate on the current authenticated user's own subscriptions
- when adding, resolve instrument names first and skip invalid or duplicate entries
- `list` groups subscriptions by instrument and shows instrument name, code, auto-update status
- `anomaly` returns unusual movements sorted by date descending, plus signals count and analysis
- `summary` returns aggregate UM_ct (异动数量) and UM_SG_ct (异动信号) counts
- when required information is missing, return a structured `needs_input` response

### Not Yet Enabled In Experience Build

The following capabilities are still under route-contract cleanup and should not be used in the current public rollout:

- full finance-analysis bundles
- money flow
- fuzzy sector resolution / similar sectors
- market news lookup
- standalone fuzzy sector resolution as a separate public deterministic intent outside `sector-research`

## Intent Routing

Pick one default route from the list below.

- User asks "这只股票现在怎么样 / 最近走势 / 看看价格":
  Route to `Stock Snapshot`
- User asks "分析财报 / 财务怎么样 / 估值怎么看":
  Route to `Finance Analysis`
- User asks "分析白酒 / 算力 / 某个板块 / 某个概念":
  Route to `Sector Analysis`
- User asks "给我做贵州茅台的深度研究 / 做一个投资论题 / 看催化剂和风险 / 写一份个股深度报告":
  Route to `Stock Deep Research`
- User asks "看看我的票池 / 把这些股票加到票池里":
  Route to `Bucket Flow`
- User asks "有哪些策略 / 看看我的私人策略 / 某个策略今天有没有买卖点 / 庐山升龙今天选了哪些股票 / 某个策略最近一周选股结果 / 用某个策略扫一组股票":
  Route to `Strategy Flow`
- User asks "画一下贵州茅台的K线图 / 庐山照影 / 庐山四季 / 双轮驱动 / 六脉神剑 / 聪明钱 / 带筹码峰的K线 / 标注买卖点":
  Route to `Indicator Chart`
- User asks "贵州茅台的综合得分 / 行业统治力 / 财务健康度 / 发展前景":
  Route to `Finance Score`
- User asks "评分最高的研究员有哪些 / 某个股票有哪些研究员和研报 / 某个研究员写过哪些研报":
  Route to `Researcher Flow`
- User asks "看看我的贝叶斯监控 / 某个贝叶斯监控任务的报告 / 某个主题最近的贝叶斯监控记录":
  Route to `Bayesian Monitor Flow`
- User asks "功夫财经连接正常吗 / OpenKey 配置对吗 / health check / 检查配置":
  Route to `Health Check`
- User asks "配置 OpenKey / 设置 OpenKey / 我的 key 是 kf_xxx":
  Route to `Config OpenKey`
- User asks "看看我的自选 / 自选列表 / 我订阅了哪些股票":
  Route to `Subscription Flow` (action: list)
- User asks "把贵州茅台加入自选 / 加自选 / 订阅这些标的":
  Route to `Subscription Flow` (action: add)
- User asks "从自选中移除平安银行 / 取消订阅 / 删除自选":
  Route to `Subscription Flow` (action: delete)
- User asks "贵州茅台有什么异动 / 查看异动 / 最近的异动报告":
  Route to `Subscription Flow` (action: anomaly)
- User asks "自选整体异动情况 / 今天有多少异动 / 异动汇总":
  Route to `Subscription Flow` (action: summary)
- User asks "功夫财经有更新吗 / 检查更新 / check update / 升级 skill":
  Route to `Check Update`

If the user asks for arbitrary whole-market screening or market-news bundles, do not use this skill in the current release build.

## Input Rules

### Stock Identification

For single-stock requests, use exactly one:

- `--instrument-name`
- `--instrument-id` and `--exchange-id`

Never mix both modes.
If the stock code is unknown, prefer `--instrument-name`.
When using code mode, `--exchange-id` must be `SSE` or `SZE`.

### Stock Date Mode

For stock products and flows, use:

- `--target-date`
- optional `--visual-days-len`

### Strategy Date Mode

For strategy actions, use:

- `signal` and `count`: `--target-date` with optional `--visual-days-len`
- `batch-scan`: `--target-date`
- `market-select`: either `--target-date`, or `--strategy-start-date` plus `--strategy-end-date`

Never mix single-day mode and range mode in the same `market-select` request.

### Sector Mode

- For sector detail products, use exactly one:
  - `--sector-name`
  - `--sector-id`

Prefer `--sector-name`.
Only reuse `--sector-id` after the backend has already returned it.
The current release build does not expose fuzzy sector resolution as a standalone public data product, but `sector-research` can resolve theme words via the EastMoney concept sector list.

### Hidden Parameters

Do not generate or expose these from the model side:

- `start_date`
- `end_date`
- `is_realtime`
- `limit`
- `days`
- `periods`

## Internal Building Blocks

The internal deterministic product contract lives here:

- [data_products.md](references/schemas/data_products.md)

Use that file only when you need exact internal product names, allowed parameter shapes, or output keys.
Do not dump that whole catalog into the user-facing reasoning path by default.

Bucket flow contract lives here:

- [bucket_flow.md](references/schemas/bucket_flow.md)

Strategy flow contract lives here:

- [strategy_flow.md](references/schemas/strategy_flow.md)

Researcher flow contract lives here:

- [researcher_flow.md](references/schemas/researcher_flow.md)

Bayesian monitor flow contract lives here:

- [bayesian_monitor_flow.md](references/schemas/bayesian_monitor_flow.md)

## Research Methodologies

Documented research methods live here:

- [README.md](references/research-flows/README.md)
- [runtime_parity.md](references/research-flows/runtime_parity.md)
- [stock-analysis](references/research-flows/stock-analysis)
- [sector-analysis](references/research-flows/sector-analysis)

Use them as methodology references and migration inputs for deep research.
The repo build currently has preview CLI/runtime entrypoints via `stock-research` and `sector-research`.
The sector preview accepts `sector_name` first and uses best-effort EastMoney concept list resolution before falling back to `needs_input`.
Read `runtime_parity.md` before treating any research wrapper or asset as implementation-ready truth.

Prompt assets are flow-specific.
Do not mix finance-analysis formatting requirements into movement-analysis outputs, or vice versa.

## Standard Commands

### Stock Snapshot

```bash
node scripts/flows/run_data_request.mjs --product price_snapshot --instrument-name 贵州茅台 --target-date 20260301
```

### Sector Detail

```bash
node scripts/flows/run_data_request.mjs --product sector_performance --sector-name 白酒 --target-date 20260301
```

### Bucket List

```bash
node scripts/router/run_router.mjs bucket --bucket-action list
```

### Bucket Add

```bash
node scripts/router/run_router.mjs bucket --bucket-action add --bucket-name 观察池 --bucket-instrument 贵州茅台 --bucket-instrument 平安银行
```

### Strategy List

```bash
node scripts/router/run_router.mjs strategy --strategy-action list
```

### Strategy Signal

```bash
node scripts/router/run_router.mjs strategy --strategy-action signal --strategy-name 三分归元 --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 22
```

### Strategy Batch Scan

```bash
node scripts/router/run_router.mjs strategy --strategy-action batch-scan --strategy-id 900 --strategy-instrument 600519.SSE --strategy-instrument 000001.SZE --target-date 20260331
```

### Strategy Market Select

```bash
node scripts/router/run_router.mjs strategy --strategy-action market-select --strategy-name 庐山升龙 --target-date 20260331
```

### Stock Deep Research

```bash
node scripts/router/run_router.mjs stock-research --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120
```

### Sector Deep Research

```bash
node scripts/router/run_router.mjs sector-research --sector-name 机器人 --target-date 20260331 --visual-days-len 780
```

### Indicator Chart — K-line

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type kline --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120
```

### Indicator Chart — K-line with Chip Peak and Price Levels

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type kline --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120 --with-chip-peak true --with-price-levels true
```

### Indicator Chart — K-line with Annotations

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type kline --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 60 --annotations '[{"date":"20260310","type":"buy","label":"买入"},{"date":"20260325","type":"sell","label":"卖出"}]'
```

### Indicator Chart — 庐山照影图

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type lushan_shadow --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120
```

### Indicator Chart — 庐山四季图

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type lushan_4season --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120
```

### Indicator Chart — 双轮驱动图

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type shuanglun --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120
```

### Indicator Chart — 六脉神剑图

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type liumai --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120
```

### Indicator Chart — 聪明钱图

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type smart_money --instrument-name 贵州茅台 --target-date 20260331 --visual-days-len 120
```

### Finance Score (data only)

```bash
node scripts/flows/run_data_request.mjs --product finance_score --instrument-name 贵州茅台 --target-date 20260331
```

### Finance Score (SVG radar chart)

```bash
node scripts/router/run_router.mjs indicator-chart --chart-type finance_score --instrument-name 贵州茅台 --target-date 20260331
```

### Researcher Rank

```bash
node scripts/router/run_router.mjs researcher --researcher-action rank --researcher-rank-by 1m --researcher-limit 10
```

### Researcher Stock Reports

```bash
node scripts/router/run_router.mjs researcher --researcher-action stock-reports --instrument-name 贵州茅台
```

### Researcher Author Reports

```bash
node scripts/router/run_router.mjs researcher --researcher-action author-reports --researcher-author-id author-1
```

### Health Check

```bash
node scripts/router/run_router.mjs health
```

Returns `{ healthy: true/false, checks: { openkey, api_test } }`. Verifies KUNGFU_OPENKEY is set and authenticates against the backend.

### Config OpenKey

```bash
node scripts/router/run_router.mjs config-openkey --openkey kf_ok_live_xxxxx
```

Validates the key against the backend, then writes it to `~/.openclaw/.env`. Returns user_id and plan_code on success.

### Subscription List (自选列表)

```bash
node scripts/router/run_router.mjs subscription --subscription-action list
```

### Subscription Add (加自选)

```bash
node scripts/router/run_router.mjs subscription --subscription-action add --subscription-instrument 贵州茅台 --subscription-instrument 平安银行
```

### Subscription Delete (删自选)

```bash
node scripts/router/run_router.mjs subscription --subscription-action delete --subscription-instrument 贵州茅台
```

### Subscription Anomaly Report (异动报告)

```bash
node scripts/router/run_router.mjs subscription --subscription-action anomaly --instrument-name 贵州茅台 --target-date 20260401
```

### Subscription Summary (异动汇总)

```bash
node scripts/router/run_router.mjs subscription --subscription-action summary
```

### Check Update

```bash
node scripts/router/run_router.mjs check-update
```

Checks ClawHub registry for a newer version. Returns `{ update_available, local_version, remote_version, update_command }`. When an update is available, the agent should run the returned `update_command` (`clawhub update kungfu-finance`) in a shell to apply it.
