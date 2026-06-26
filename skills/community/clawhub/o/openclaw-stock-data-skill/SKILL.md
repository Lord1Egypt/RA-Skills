---
name: openclaw-stock-skill
description: 使用 data.diemeng.chat 提供的接口查询股票日线、分钟线、财务指标等数据，支持 A 股等市场。
user-invocable: true
metadata: {
  "openclaw": {
    "emoji": "📈",
    "skillKey": "openclaw-stock-skill",
    "requires": { "env": ["STOCK_API_KEY"] },
    "primaryEnv": "STOCK_API_KEY"
  }
}
---

本技能教会代理如何使用你自建的股票数据服务（线上域名 `https://data.diemeng.chat`），通过 **API Key** 进行鉴权，查询股票的日线、分钟线、财务指标等数据。

> ⚙️ **API Key 配置约定**
>
> - OpenClaw 会按照 [`skills.entries.<key>` 配置](https://docs.openclaw.ai/tools/skills-config) 把 API Key 和自定义配置注入到进程环境变量中。
> - 本技能约定使用环境变量 **`STOCK_API_KEY`** 作为主密钥，并在 `metadata.openclaw.primaryEnv` 中声明，以便通过 `skills.entries.openclaw-stock-skill.apiKey` 统一配置。
> - 推荐的 OpenClaw 配置示例（`~/.openclaw/openclaw.json`）：
>
> ```json5
> {
>   skills: {
>     entries: {
>       "openclaw-stock-skill": {
>         enabled: true,
>         // 建议在 OpenClaw UI 的 Skill 参数面板里填写 apiKey，
>         // Gateway 会自动将其写入 STOCK_API_KEY 环境变量
>         apiKey: { source: "env", provider: "default", id: "STOCK_API_KEY" },
>         env: {
>           // 可在这里直接写死，或通过系统环境变量覆盖
>           STOCK_API_KEY: "YOUR_REAL_STOCK_API_KEY"
>         },
>         config: {
>           // 可选：覆盖默认域名
>           baseUrl: "https://data.diemeng.chat"
>         }
>       }
>     }
>   }
> }
> ```
>
> 参考文档：[Skills Config](https://docs.openclaw.ai/tools/skills-config)、[Skills](https://docs.openclaw.ai/tools/skills)

## 总体说明

- **基础域名**：默认使用 `https://data.diemeng.chat`，如存在 `skills.entries.openclaw-stock-skill.config.baseUrl` 则优先使用配置中的 `baseUrl`。
- **鉴权方式**：所有需要权限的接口都必须带上 API Key：
  - 首选 HTTP Header：`apiKey: <STOCK_API_KEY>`（推荐）
  - 兼容 Header：`X-API-Key: <STOCK_API_KEY>`
  - 后端也支持在 JSON body 中携带 `apiKey` 字段，但为了安全与规范，本技能**统一通过 Header 传递**。
- **返回结构**：
  - 大多数接口返回：`{ "code": 200, "msg": "成功", "data": { ... } }`
  - 少数列表类接口直接返回数组或简单结构，实际响应以 JSON 为准。
- **限流与黑名单**：
  - API Key 及 IP 都有严格限流与黑名单逻辑：
    - 无效 API Key 多次尝试会触发封禁（参见后端 `DataAccessVerifier` 实现）。
    - 需优先缓存和复用同一 API Key，不要在循环中频繁切换。

## 能力概览（建议的工具意图）

代理应将本技能视作一组 HTTP 能力，而不是单一接口：

- **get_stock_daily_bars**：查询指定股票在某一时间区间内的日线 K 线数据。
- **get_stock_intraday_bars**：查询分钟级（1/5/15/30/60 分钟）历史数据。
- **get_stock_finance_factors**：查询日度财务因子（PE、PB、换手率等）。
- **get_stock_list**：查询股票基础信息列表，用于代码／名称搜索。
- **get_stock_valuation**：查询估值列表和详细估值信息。
- **get_stock_calendar_and_snapshot**：查询交易日历和当日快照。

代理在规划调用时，应根据用户自然语言意图，选择以上能力并组合使用。

## 接口详情与调用规范

### 1. 日线数据：`POST /api/stock/daily`

- **URL**：`{baseUrl}/api/stock/daily`
- **方法**：`POST`
- **Headers**：
  - `Content-Type: application/json`
  - `apiKey: <STOCK_API_KEY>`
- **请求体 JSON**（后端 `DailyDataRequest`）：

```json
{
  "stock_code": "000001.SZ",
  "start_time": "2024-01-01",
  "end_time": "2024-01-31",
  "page": 0,
  "page_size": 1000
}
```

- 说明：
  - `stock_code` 可以是单个字符串，也可以是字符串数组。
  - `start_time`、`end_time` 格式为 `YYYY-MM-DD`。
  - 支持分页，`page` 从 0 开始。
- 响应主体（简化）：
  - `data.total`：总记录数
  - `data.list`：每条记录包含 `stock_code`, `trade_date`, `open`, `high`, `low`, `close`, `vol`, `amount` 等字段，价格与成交量已在后端统一保留 2 位小数。

> 代理在需要“某股某段时间的日 K 线”时，应优先选择该接口。

### 2. 分钟级历史数据：`POST /api/stock/history`

- **URL**：`{baseUrl}/api/stock/history`
- **方法**：`POST`
- **Headers**：同上
- **请求体 JSON**（后端 `HistoryDataRequest`）：

```json
{
  "stock_code": "000001.SZ",
  "level": "5min",
  "start_time": "2024-01-01 09:30:00",
  "end_time": "2024-01-01 15:00:00",
  "page": 0,
  "page_size": 1000
}
```

- 字段说明：
  - `level`：`"1min" | "5min" | "15min" | "30min" | "60min"`
  - `start_time` / `end_time`：
    - 允许仅日期（自动补全 00:00:00 和 23:59:59）
    - 或完整时间戳 `YYYY-MM-DD HH:MM:SS`
- 响应主体（简化）：
  - `data.list` 中每条包含：`stock_code`, `trade_time`, `open`, `high`, `low`, `close`, `vol`, `amount`。

> 用于用户询问“某天/某段时间内的分钟级行情、分时数据”等场景。

### 3. 财务与因子（行情因子）：`POST /api/stock/finance`

- **URL**：`{baseUrl}/api/stock/finance`
- **方法**：`POST`
- **请求体 JSON**（后端 `FinanceDataRequest`）：

```json
{
  "stock_code": "000001.SZ",
  "start_time": "2024-01-01",
  "end_time": "2024-03-31",
  "page": 0,
  "page_size": 1000
}
```

- 主要返回字段（列表中每条）：
  - `trade_date`, `close`, `turnover_rate`, `turnover_rate_f`, `volume_ratio`, `pe`, `pe_ttm`, `pb`, `ps`, `ps_ttm`, `dv_ratio`, `dv_ttm`, `total_share`, `float_share`, `free_share`, `total_mv`, `circ_mv` 等。

> 适合估值分析、换手率、成交金额、市值等相关问题。

### 4. 股票基础信息列表：`GET /api/stock/list`

- **URL**：`{baseUrl}/api/stock/list`
- **方法**：`GET`
- **Query 参数**：
  - `stock_code`（可选）：精确股票代码筛选
  - `page`：默认 0
  - `page_size`：默认 20000
- 响应（封装在统一 `success` 结构中）：
  - `data.total`
  - `data.list`：包含 `stock_code`, `name`, `area`, `industry`, `list_date`, `symbol`, `list_status`, `delist_date`, `is_hs` 等。

> 当用户只给出股票名称、地区、行业等描述时，可先通过该接口获取匹配列表，再提示用户选择具体代码。

### 5. 估值列表与详细估值：`GET /api/stock/valuation` & `GET /api/stock/valuation/list`

#### 5.1 综合估值列表：`GET /api/stock/valuation`

- **URL**：`{baseUrl}/api/stock/valuation`
- **方法**：`GET`
- **说明**：
  - 无需请求体，通过 API Key 权限控制访问。
  - 内部会聚合 `stock_finance_daily`, `stock_industry`, `stock_ten_year_growth` 等多张表，返回 `StockValuationItem` 列表。
- 典型字段：
  - `stock_code`, `stock_name`, `level1_name`, `level2_name`, `level3_name`
  - `pe_ttm`, `pe_percentile`, `latest_price`, `dividend_yield_ttm`
  - 行业相关：`industry_avg_pe`, `industry_pe_rank`, `sector_pe_median`, `sector_pe_rank`
  - 成长与财务：`eps`, `roe`, `roa`, `eps_growth_10y`, `roe_growth_10y`, `avg_dividend_10y` 等。

> 当用户提问如“某只股票在行业内估值水平如何”“给我按市盈率从低到高列出某行业股票”时应优先考虑调用该接口。

#### 5.2 简化估值列表：`GET /api/stock/valuation/list`

- **URL**：`{baseUrl}/api/stock/valuation/list`
- **方法**：`GET`
- **Query 参数**：
  - `sort_by`：`pe_ttm | pe_percentile | dividend_yield_ttm | industry_pe_rank`（默认 `pe_ttm`）
  - `sort_order`：`asc | desc`（默认 `asc`）
  - `industry`（可选）
  - `limit`（默认 100）
  - `offset`（默认 0）

> 适合只需要“按某个指标排序的前 N 个股票”的场景。

### 6. 交易日历与快照：`GET /api/basic/calendar` & `GET /api/basic/snapshot`

#### 6.1 交易日历：`GET /api/basic/calendar`

- **URL**：`{baseUrl}/api/basic/calendar`
- **方法**：`GET`
- **Query 参数**：
  - `start_time`: `YYYY-MM-DD`
  - `end_time`: `YYYY-MM-DD`
- 响应：
  - `data` 为数组，每条含 `date`, `is_open`（1 为交易日，0 为休市）。

> 当用户问“某段时间哪些是交易日”“下一个交易日是什么时候”等，可使用此接口。

#### 6.2 快照：`GET /api/basic/snapshot`

- **URL**：`{baseUrl}/api/basic/snapshot`
- **方法**：`GET`
- **Query 参数**：
  - `stock_code`（可选）
  - `page`, `page_size`
- 返回最新一笔集合竞价数据的汇总，字段包括价格、成交量、买卖盘等。

> 当用户需要“当前（最近一次）盘口快照”或大盘扫描时，可使用此接口。

## 调用策略与最佳实践

1. **API Key 获取与使用**
   - 优先从环境变量 `STOCK_API_KEY` 读取（由 OpenClaw 按 `skills.entries.openclaw-stock-skill.apiKey` 注入）。
   - 若环境变量缺失，可根据用户在 Skill 配置面板中输入的值（通常同样会映射到该环境变量）进行调用。
   - 不要在 URL Query 中传递 `apiKey` 或 `api_key`，后端会视为安全风险。

2. **错误处理**
   - `code = 401`：API Key 无效或缺失，应提示用户检查在 OpenClaw Skill 配置中的 API Key。
   - `code = 403`：权限不足或下载次数/访问次数限制，应向用户说明权限/限流约束。
   - `code = 429`：请求过于频繁，需减少调用频率或提示用户稍后再试。

3. **分页与大数据量**
   - 若 `data.total` 很大，代理应分批分页请求，并在回答中做汇总，而不是一次性获取全部数据。
   - 对于分钟级或 tick 级大数据量，应在对话中与用户确认时间范围和精度，避免无谓的海量下载。

4. **单位与精度**
   - 价格、成交量等字段在后端已经统一保留 2 位小数；如需展示给用户，可直接使用或再格式化。
   - 分红相关字段在估值接口中已做 10 年平均等处理，解释时注意说明口径（年化、近 10 年等）。

## 使用示例（给代理的思路）

- 当用户说：**“帮我查一下 000001.SZ 在 2024 年 1 月份的日 K 线”**
  1. 调用 `POST /api/stock/daily`，`stock_code = "000001.SZ"`，时间区间为 `2024-01-01` 至 `2024-01-31`。
  2. 对返回的 `data.list` 进行整理，总结涨跌幅、最大回撤、平均成交额等。

- 当用户说：**“按市盈率从低到高列出券商行业的前 20 只股票”**
  1. 调用 `GET /api/stock/valuation/list`，设置 `industry = "证券"`（或其它后端行业名称）、`sort_by = "pe_ttm"`, `sort_order = "asc"`, `limit = 20`。
  2. 将结果按表格形式展示，并简要点评估值分布。

- 当用户说：**“这周哪些天是交易日？”**
  1. 根据当前日期计算一周范围，调用 `GET /api/basic/calendar`。
  2. 将 `is_open = 1` 的日期列出，说明哪些是交易日。

本技能不包含额外可执行脚本，完全通过指导代理调用现有 HTTP 接口工作。所有请求都应优先使用 `STOCK_API_KEY` 环境变量，并遵守上述限流与安全约定。

