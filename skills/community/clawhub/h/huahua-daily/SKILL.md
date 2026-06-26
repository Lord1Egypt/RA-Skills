---
name: huahua-daily
description: Use HuahuaDaily MCP to query portfolio, transactions, market data, screenshot imports, and send App-confirmed trade/import requests.
version: 2.0.6
---

# 花花日记助手（HuahuaDaily）

## 0. Compatibility

This SKILL.md intentionally uses the smallest common Agent Skills format: YAML frontmatter with only `name` and `description`, followed by Markdown instructions. Platform-specific setup for Codex, Codex CLI, Claude Code, Claude Desktop, OpenClaw, Hermes Agent, and other MCP clients belongs in README/configuration, not in this file.

## 1. 核心边界

花花日记 MCP 让 Agent 读取用户授权的云端同步数据、基金行情、交易流水和系统公告，识别截图，并向 App 发送待确认请求。

Agent 不直接写入交易、不直接导入持仓、不覆盖云同步。所有买入、卖出、持仓导入、自选导入、交易记录导入，都必须由用户在 App 确认页最终确认。

社区授权、取消授权、关注/取消关注、社区收益同步是直接后端写操作，不走 App 待确认页。只有用户明确确认该社区操作时才调用；不要把它们描述为“已发送到 App 等待确认”。

MCP 可读取完整持仓、交易流水、原始云同步快照和截图内容，可能包含金额、成本、收益率等敏感投资数据。回答时不要主动暴露超过用户问题所需的明细。

## 2. 会话启动

首次使用或不确定能力时，调用：

```json
get_tool_manifest()
```

用途：
- 确认可用工具、认证方式、安全边界。
- 不访问用户数据，不消耗行情请求。

Token 缺失、无效或过期时，提示用户在 App「小窝 / 设置 → Agent 访问令牌」重新生成，并配置环境变量 `HUAHUA_AGENT_TOKEN`。

确认当前账号信息（昵称、UID、会员状态）：

```json
get_current_user()
```

适合回答"我是谁""我的会员什么时候到期"等问题。

## 3. 查询持仓和云同步

### 3.1 用户问“今天收益/总资产/累计收益”

首选：

```json
get_summary()
```

返回重点：
- `totalMarketValue`：总市值。
- `todayProfit`：今日收益。
- `totalHoldingProfit`：持有收益。
- `cumulativeProfit`：累计收益。
- `totalReturnRate`：累计收益率。
- `dataUpdatedAt`：云同步时间。

回答时必须说明 `dataUpdatedAt`。如果时间明显旧，提醒用户在 App 执行「立即同步」。

不要为了资产概况先调用 `get_raw_sync_data()`。

### 3.2 用户问“完整持仓/自选/分组”

首选：

```json
get_records({"include_transactions": false})
```

返回重点：
- `holdings`：有持仓的基金。
- `watchlist`：自选或清仓观察项。
- `groups`：分组。
- `summary`：汇总。
- `dataUpdatedAt`：云同步时间。

云同步会保存最后一次官方净值作为恢复基线，但不会保存盘中估值等高频行情。`get_records` 会主动拉取最新行情并优先使用接口返回的官方净值计算市值；若需要盘中估算口径，再调用 `get_item_estimate` 获取 `estimatedNav`。

如果用户要求交易流水、成本来源、审计收益，再调用：

```json
get_transactions({"code": "", "include_pending": true})
```

或：

```json
get_records({"include_transactions": true})
```

### 3.3 用户问“云端是不是最新/同步是否完整”

先调用：

```json
get_sync_meta()
```

返回重点：
- `updated_at`：云端更新时间。
- `etag`：云端快照指纹。
- `size_bytes`：快照大小。

需要完整检查时调用：

```json
get_raw_sync_data({"include_json_text": false})
```

检查重点：
- `data.funds` 是否存在且非空。
- `data.groups`、`data.watchlistGroups` 是否存在。
- `data.globalTags` 是否存在。
- `meta.contains_ledger` 通常为 false，这是正常的。

只有用户明确要求导出原始 JSON 文本时，才设置 `include_json_text=true`。默认不要返回大段 JSON。

### 3.4 用户问“标签/分组”

分组：

```json
get_groups()
```

标签：

```json
get_tags()
```

使用规则：
- `get_groups()` 用于解释持仓账户分组、自选分组。
- `get_tags()` 用于解释全局标签和每只基金绑定标签。

## 4. 查询基金和市场

### 4.1 用户提供 6 位基金代码

查询实时估算：

```json
get_item_estimate({"codes": ["110022"]})
```

用途：
- “现在涨多少”
- “今天估算净值”
- “这只今天收益如何”

注意：
- `codes` 最多 50 个。
- 可批量传入，避免逐个调用。
- 结果同一 session 内缓存 60 秒。

### 4.2 用户只提供基金名称

先搜索：

```json
search_item({"query": "易方达消费"})
```

处理规则：
- 搜索结果只有一个高可信候选时，可继续查询。
- 多个候选或名称相近时，先让用户确认代码。
- 不要凭名字猜代码后直接发交易请求。

### 4.3 用户要深度分析单只基金

按需调用：

```json
get_item_detail({"code": "110022"})
get_item_history({"code": "110022"})
get_fund_fees({"code": "110022"})
get_item_dividends({"code": "110022"})
get_fund_period_rank({"code": "110022"})
get_fund_timeline({"code": "110022"})
```

选择规则：
- 当前估算/涨跌：`get_item_estimate`。
- 历史走势：`get_item_history`。
- 申购赎回费、确认天数：`get_fund_fees`。
- 分红派息：`get_item_dividends`。
- 近 1/3/6 月、1 年排名：`get_fund_period_rank`（单只）或 `get_batch_fund_period_ranks`（批量，最多 50 只）。
- 今日盘中估值曲线：`get_fund_timeline`。
- 综合详情、胜率表、持仓等深度信息：`get_item_detail`。此工具较重，不要作为日常行情首选。
- QDII 夜盘实时估值：`get_night_estimate`（需会员，美股交易时段有效）；用户在 App 添加的夜盘自选基金列表用 `get_night_watchlist`，通常先调这个再传给 `get_night_estimate`。
- 基金画像（综合信息）：`get_fund_profile`。包含费率、排名、持仓、行业、分红、风险指标等。
- 批量画像：`get_batch_fund_profiles`（最多 20 只）。

### 4.4 用户问市场整体

概览：

```json
get_overview()
```

主要指数：

```json
get_indices()
```

今日涨跌榜：

```json
get_daily_rank()
```

是否交易日：

```json
get_status()
```

### 4.5 用户问"大家都在买什么/热门基金"

持有人排行：

```json
get_holder_ranking()
```

返回 App 内持有人数最多的 30 只基金，含持有人数和涨跌幅。

### 4.6 用户问"资金在流向哪里/板块热度"

资金流向：

```json
get_fund_flow()
```

返回 `fundFlow`（基金资金流）、`sectorFlow`（板块资金流）、`polledAt`（数据时间）。
需要 PRO 会员权限。适合回答"主力资金在买什么板块""哪些基金被大额申购/赎回"等问题。

### 4.7 用户问指数/ETF 行情

目录：

```json
get_instrument_catalog()
```

实时行情：

```json
get_instrument_quotes({"codes": ["sh000300", "sh000001"]})
```

分时走势：

```json
get_instrument_timeline({"code": "sh000300"})
```

历史数据：

```json
get_instrument_history({"code": "sh000300", "period": "1m"})
```

### 4.8 用户问"跑赢大盘/对比沪深300"

默认沪深300：

```json
get_benchmark_history({"code": "sh000300"})
```

常用代码：
- `sh000300`：沪深300。
- `sh000001`：上证指数。
- `sz399001`：深证成指。
- 数字 ETF 代码也可传入，如 `510300`。

需要基金自身走势时，再调用 `get_item_history(code)`。

### 4.9 用户问 QDII 基金夜盘

QDII 基金投资美股/港股，北京时间夜间才是它们的交易时段。夜盘估值在美股交易时段（21:30–次日04:00 夏令时）提供实时持仓穿透。

**推荐流程（无需用户报代码）**：先用 `get_night_watchlist()` 读用户在 App 添加的夜盘自选列表，再用其结果调 `get_night_estimate()`：

```json
get_night_watchlist()
// 返回 {"codes": ["016665", "018147", ...], "count": N, "has_customized": true, "dataUpdatedAt": "..."}
```

若 `has_customized=false`（用户未自定义过），codes 为空，应提示用户先去 App 夜盘页面添加自选基金，或允许用户手动指定一组代码。

```json
get_night_estimate({"codes": ["016665", "018147"]})
```

`force: true` 可跳过服务端缓存强制刷新，默认 false。

返回每只基金的：
- `estimatedChangePercent`：盘后复合涨跌幅（股价×汇率）。
- `estimatedNav`：估算净值。
- `breakdown`：穿透到个股的持仓明细、股价涨跌、汇率变动、贡献度。
- `status`：`ready`（数据就绪）/ `pending`（等待开盘）/ `closed`（休市）。

注意：
- 需要 VIP 或 PRO 会员。
- 非美股交易时段返回休市状态，不是错误。
- 不要在 A 股交易时段频繁调用。
- 夜盘自选列表需要 App 至少做过一次云同步才能被 MCP 读到；旧版本 App（未升级到含夜盘同步的版本）的备份里没有 nightWatchCodes 字段，此时 `has_customized` 会是 `false`。

### 4.10 用户问交易日/T+N

下一个交易日：

```json
get_next_trading_day({"date": "2026-05-13"})
```

基金确认日期：

```json
calculate_trading_dates({
  "date": "2026-05-13",
  "time_mode": "PRE_MARKET",
  "confirm_days": 2
})
```

参数：
- `time_mode`: `PRE_MARKET` 表示收盘前，`POST_MARKET` 表示收盘后。
- `confirm_days`: T+1/T+2/T+3 等，未知时先用 `get_fund_fees(code)` 获取 `confirm_days`。

## 5. 交易请求

### 5.1 用户想买入/卖出

先确认：
- 基金代码。
- 基金名称。
- 买入或卖出。
- 金额。
- 日期，可留空让 App 使用今日。
- 分组名，如果用户指定了账户/分组。

发送请求：

```json
request_transaction({
  "item_code": "110022",
  "item_name": "易方达消费行业股票",
  "record_type": "BUY",
  "amount": 1000,
  "date": "2026-05-13",
  "note": "Agent 发起",
  "group_name": "我的账户"
})
```

规则：
- `record_type` 只能是 `BUY` 或 `SELL`。
- 如果基金代码来自搜索推断，必须先让用户确认。
- 调用后必须告诉用户：“请求已发送，请打开花花日记 App 确认后才会生效。”
- 不要说“已买入”或“已卖出”。

### 5.2 查看或撤销待处理请求

查看：

```json
get_agent_requests()
```

用户明确要求忽略/撤销时：

```json
update_agent_request({
  "request_id": "请求 id",
  "status": "DISMISSED"
})
```

不要替 App 把请求标记为 `PROCESSED`，除非用户明确要求且你知道这只是状态处理，不代表真实交易执行。

## 6. 截图导入

### 6.1 持仓/自选截图识别

持仓截图（本地路径）：

```json
import_holding_screenshots({
  "image_paths": ["/absolute/path/holding.png"],
  "import_type": "HOLDINGS"
})
```

自选截图（务必传 `import_type: "WATCHLIST"`）：

```json
import_holding_screenshots({
  "image_paths": ["/absolute/path/watchlist.png"],
  "import_type": "WATCHLIST"
})
```

Base64：

```json
import_holding_screenshots({
  "images_base64": [
    {"filename": "holding.png", "mime": "image/png", "base64": "..."}
  ],
  "import_type": "HOLDINGS"
})
```

本地路径模式会让 MCP server 读取并上传用户机器上的对应图片文件。只使用用户明确提供或当前对话中产生的截图路径；不要猜测、遍历或尝试读取无关文件。无法确认来源时优先使用 `images_base64`。

`import_type` 说明：
- `HOLDINGS`（默认）：持仓页面通常不显示基金代码，后端按名称四步匹配（可能出现模糊匹配）。
- `WATCHLIST`：自选页面明确显示 6 位代码，后端用专门 prompt 提取代码并精确匹配；AI 漏识别代码时回退名称匹配。**自选场景务必传此值**，否则会强制走名称模糊匹配。

返回重点：
- `items`：识别条目。
- `summary.total`：总条数。
- `summary.unmatched`：未匹配数量。
- `resolution_required`：是否需要轻确认。
- `resolution_reason`：轻确认原因。

用途：
- 持仓截图导入（`import_type="HOLDINGS"`）。
- 自选截图导入（`import_type="WATCHLIST"`）。

识别后不要直接声称导入完成。

### 6.2 交易记录截图识别

本地路径：

```json
import_transaction_screenshots({
  "image_paths": ["/absolute/path/transactions.png"]
})
```

Base64：

```json
import_transaction_screenshots({
  "images_base64": [
    {"filename": "transactions.png", "mime": "image/png", "base64": "..."}
  ]
})
```

同样地，`image_paths` 只可用于用户明确提供的截图文件路径。

返回重点：
- `type`: `BUY` 或 `SELL`。
- `fund_name`：截图识别名称。
- `fund_code`：匹配代码。
- `fund_real_name`：标准基金名。
- `matched`：是否匹配。
- `date`、`time_mode`、`amount`、`shares`。
- `skip` / `skip_reason`：应跳过的条目。
- `resolution_required` / `resolution_reason`。

### 6.3 Agent 轻确认规则

只在对话里确认“识别歧义”，不要让用户在对话里完成大型表格审核。

需要轻确认的情况：
- `resolution_required=true`。
- `match_status=unmatched`。
- `matched=false`。
- 多个候选基金。
- 日期缺失或明显不合法。
- 买入缺 `amount`。
- 卖出缺 `shares`。

轻确认完成后，修改 `items` 中对应字段，再发送到 App。

### 6.4 发送到 App 确认页

持仓导入：

```json
request_import_review({
  "import_type": "HOLDINGS",
  "items": [...],
  "source_note": "Agent 识别持仓截图"
})
```

自选导入：

```json
request_import_review({
  "import_type": "WATCHLIST",
  "items": [...],
  "source_note": "Agent 识别自选截图"
})
```

交易记录导入：

```json
request_import_review({
  "import_type": "TRANSACTIONS",
  "items": [...],
  "source_note": "Agent 识别交易记录截图"
})
```

限制：
- `import_type` 只能是 `HOLDINGS`、`WATCHLIST`、`TRANSACTIONS`。
- `items` 最多 300 条。
- 请求体最多 1MB。

调用后必须告诉用户：
- “已发送到 App，请打开花花日记批量确认。”
- “导入尚未完成，只有 App 确认后才会写入。”

## 7. 社区与公告

查看某基金弹幕：

```json
get_danmaku({"code": "110022"})
```

发送弹幕：

```json
send_danmaku({
  "fund_code": "110022",
  "text": "今天波动有点大"
})
```

规则：
- 只有用户明确要求发言时才调用 `send_danmaku`。
- `text` 最多 30 字。
- 弹幕颜色由 App 根据基金涨跌情况自动设置，无需手动指定。

系统公告：

```json
get_notices({"since": 0})
```

`since` 是 Unix 秒时间戳；默认 0 表示拉取最近公告。

### 7.1 喵舍社区

排行榜：

```json
get_community_ranking({"tab": "weekly"})
```

`tab` 可选 `weekly`（周收益）、`monthly`（月收益）、`total`（总收益）。

我的排名：

```json
get_community_my_rank()
```

用户详情（十大重仓前5）：

```json
get_community_user({"uid": "12345678"})
```

搜索用户（UID / 昵称）：

```json
search_community_users({"query": "花花"})
```

关注/粉丝数：

```json
get_community_stats()
```

关注列表：

```json
get_community_following()
```

社区通知（排名变化、被关注等）：

```json
get_community_notices({"since": 0})
```

授权管理：

```json
// 查询授权状态
get_community_authorization()

// 授权参与排行（须向用户确认）
authorize_community({"show_amount": false, "anonymous": false})

// 取消授权，退出排行
revoke_community_authorization()
```

关注操作：

```json
// 关注/取消关注（取反操作）
follow_community_user({"target_uid": "12345678"})
```

收益同步：

```json
// 手动同步收益到社区（通常由 App 自动完成，Agent 仅在用户明确要求时调用）
sync_community_returns({
  "weekly_return": 5.2,
  "monthly_return": 12.8,
  "total_return": 35.6,
  "fund_count": 8,
  "top_fund_code": "110022",
  "top_fund_name": "易方达消费行业"
})
```

规则：
- 社区功能需要 PRO 会员。
- `get_community_notices` 与 `get_notices` 不同：前者是个人社区通知，后者是系统公告。
- 授权、取消授权、关注/取消关注、收益同步调用后会直接生效，不会进入 App 确认页；调用前必须向用户明确确认。
- 授权操作前须向用户确认是否愿意公开持仓数据，以及是否展示金额、是否匿名。
- `follow_community_user` 是取反操作：已关注则取消，未关注则添加。
- `sync_community_returns` 的收益率参数为百分比数值（如 5.2 表示 +5.2%），而非小数。不要凭空编造收益率；只有当用户明确要求刷新社区收益，且你能从可信数据计算或用户明确提供这些数值时才调用。通常应让 App 自动完成社区收益同步。

## 8. JCTI 投资人格分析

用户完成 JCTI（韭彩测试指标）答题后，可提交四维分数获取 AI 个性化分析：

```json
analyze_jcti({
  "personality_id": "tepulang",
  "ye": 85,
  "wen": 60,
  "sui": 30,
  "duan": 45
})
```

参数：
- `personality_id`：人格 ID，可选 `tepulang`（特普朗）、`jiuhuang`（韭黄）、`faguo-dushen`（法国赌神）、`ji-wuli`（姬无力）、`yingshengchong`（应声虫）、`shanmu`（山姆）、`taozhongren`（套中人）、`tuoluowang`（陀螺王）。
- `ye` / `wen` / `sui` / `duan`：野、稳、随、短四个维度的分数，每项 0-100。

返回 AI 生成的个性化投资人格分析文本。需要 VIP 或 PRO 会员。

## 9. App 版本信息

最新版本：

```json
get_app_version()
```

返回版本号、更新日志、下载地址、是否强制更新。

版本历史：

```json
get_app_versions({"page": 1, "page_size": 5})
```

适合回答"最新版本有什么新功能""历史更新记录"等问题。

## 10. 常见降级

- `401`：Token 无效或过期，要求用户重新生成。
- `403`：权限不足或会员状态不满足；Agent Token 和多数 MCP 能力需要 PRO，部分行情/JCTI 能力可能要求 VIP 或 PRO。
- 云端无数据：要求用户打开 App 执行「立即同步」。
- 行情估算为空：可能是非交易日、盘前或数据源暂不可用，不要当作错误。
- 截图识别为空：提示用户换清晰截图，或分批上传。
- 导入请求发送成功后：不要继续追问大表格细节，等待用户在 App 确认。
- 持有人排行需要 PRO 会员，非会员返回 403。
