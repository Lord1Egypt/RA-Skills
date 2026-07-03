# 花花日记 MCP 服务（HuahuaDaily）

通过 MCP 让 Codex、Codex CLI、Claude Code、Claude Code CLI、Claude Desktop、Cursor、Windsurf、OpenClaw 以及其他支持 MCP 的 Agent 读取花花日记后端数据、查询市场行情、识别截图，并向 App 发送待确认交易或导入请求。

交易和导入不会由 Agent 直接写入。Agent 只负责识别、轻确认和发起请求，最终写入必须回到花花日记 App 的现有确认页。

社区授权、取消授权、关注/取消关注、社区收益同步属于直接后端写操作，不走 App 待确认页；Agent 只有在用户明确确认该社区操作后才应调用。

MCP 可读取完整持仓、交易流水、云端实时同步主数据和截图内容，可能包含金额、成本、收益率等敏感投资数据。生成 Agent Token 即表示授权所接入的 Agent 在其权限范围内读取这些数据。

## 前置条件

- **Python 3.10+**
- 花花日记账号已开通 PRO。
- 在 App「小窝 / 设置 → Agent 访问令牌」生成新的 Agent Token；本地开发也可用 `backend/scripts/create_agent_token.py` 给测试账号生成。
- Token 只显示一次，配置为环境变量 `HUAHUA_AGENT_TOKEN`。

官方 API 默认地址：`https://api.huahuadaily.cn`，可通过 `HUAHUA_API_BASE` 覆盖。

## 安装方式

### 方式一：uvx（推荐）

[uv](https://docs.astral.sh/uv/) 是快速的 Python 包管理器，`uvx` 可直接运行 Python 工具，无需手动安装依赖。

**安装 uv**（如果尚未安装）：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**MCP 配置**：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/baiye1997/HuaHuaDailyMCP",
        "huahua-daily"
      ],
      "env": {
        "HUAHUA_API_BASE": "https://api.huahuadaily.cn",
        "HUAHUA_AGENT_TOKEN": "粘贴你的 Agent Token"
      }
    }
  }
}
```

### 方式二：pip 安装

如果不想安装 uv，可以用 pip 全局安装：

```bash
pip install git+https://github.com/baiye1997/HuaHuaDailyMCP
```

**MCP 配置**：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "huahua-daily",
      "env": {
        "HUAHUA_AGENT_TOKEN": "粘贴你的 Agent Token"
      }
    }
  }
}
```

### 方式三：本地运行

```bash
# 克隆仓库
git clone https://github.com/baiye1997/HuaHuaDailyMCP.git
cd HuaHuaDailyMCP

# 安装依赖
pip install -r requirements.txt

# 运行
HUAHUA_AGENT_TOKEN=你的Token python server.py
```

## 各 Agent 配置示例

### Claude Code

```bash
claude mcp add huahua-daily \
  -e HUAHUA_AGENT_TOKEN=你的Token \
  -- uvx --from git+https://github.com/baiye1997/HuaHuaDailyMCP huahua-daily
```

或手动编辑 `~/.claude.json`：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_API_BASE": "https://api.huahuadaily.cn",
        "HUAHUA_AGENT_TOKEN": "你的Token"
      }
    }
  }
}
```

### Claude Desktop

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或 `%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_AGENT_TOKEN": "你的Token"
      }
    }
  }
}
```

### Cursor

编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_AGENT_TOKEN": "你的Token"
      }
    }
  }
}
```

### Windsurf

编辑 `~/.windsurf/mcp.json`，格式同上。

## OpenClaw / ClawHub

```bash
clawhub install huahua-daily
```

然后配置环境变量 `HUAHUA_AGENT_TOKEN`。

## 建议 System Prompt

```text
你可以使用花花日记 HuahuaDaily MCP 工具查询用户基金持仓、交易流水、云同步状态、市场行情和公告，也可以识别截图并把导入结果发送到 App 确认页。

调用规则：
- 会话开始可调用 get_tool_manifest 自检能力和安全边界。
- 查询资产概况优先调用 get_summary；需要明细再调用 get_records。
- 需要审计交易流水或重算收益时，调用 get_transactions 或 get_records(include_transactions=true)。
- 需要完整云端实时同步主数据时，调用 get_raw_sync_data；不要默认请求 include_json_text=true。
- 若 `get_sync_meta` / `get_raw_sync_data.meta` 返回 `empty_portfolio_confirmed=true` 且 `has_restorable_sync_payload=true`，表示这是用户在 App 确认过的空组合主数据，不是云端损坏。
- 查询某只基金行情：已知代码直接 get_item_estimate；未知代码先 search_item。
- 对比单只基金不同行情源：调用 get_fund_source_previews。
- 用户想买入/卖出时，必须先确认基金名称、代码、金额、分组，再调用 request_transaction。
- request_transaction 只发送待确认信号，必须明确告知用户需要打开 App 确认。
- 用户明确要求生成个人组合报告时，可以基于其授权读取的持仓、交易和行情数据生成，并调用 submit_personal_strategy_report 投递到当前 token 用户自己的报告中心。
- submit_personal_strategy_report 需要 `messages:write` scope；如需同一个 token 同时读取持仓并投递个人报告，使用 `agent:full messages:write`。默认 `agent:full` 不含个人报告写入。
- submit_personal_strategy_report 只能写当前 Agent Token 所属用户，不能广播，不能指定 user_id，不得声称发送给所有用户。
- 不得调用 /api/hermes/reports；公开 MCP 不提供管理员公共报告写入能力。
- 截图导入先调用 import_holding_screenshots 或 import_transaction_screenshots。
- 对 unmatched / ambiguous 条目只做轻确认，补齐基金代码、日期、金额、份额等识别歧义。
- 轻确认后调用 request_import_review，把整批结果发送到 App 现有导入确认页。
- 不要直接写云同步，不要声称导入已完成；用户必须在 App 批量确认后才会写入。
- 数据来自云端实时同步主数据，MCP 固定读取结构化组合接口，不读取旧同步大包或云端历史备份快照。若用户刚在 App 操作，提醒其确认实时同步已完成再查询。
- `get_records` 的市值/持有收益只按 App 云端主数据中的官方 `lastNav` 计算；盘中估算只用于今日收益，不用于持仓市值。
- 查询 QDII 夜盘估值时，先调用 get_night_watchlist 获取用户自选列表，再调用 get_night_estimate。
- 查询资金流向时调用 get_fund_flow（需 PRO 会员）。
- 社区授权/关注/同步等写操作须向用户确认后再执行。
- 社区写操作会直接生效，不是 App 待确认请求；收益同步不要凭空编造收益率，通常交给 App 自动同步。
- 截图工具的 image_paths 会读取本机图片文件；只使用用户明确提供的路径，无法确认来源时优先使用 images_base64。
- 用户完成 JCTI 答题后可调用 analyze_jcti 获取 AI 人格分析。
- 查询 App 版本信息使用 get_app_version 或 get_app_versions。
```

## 工具能力

认证与自检：

- `set_token(token)`：运行时设置 Agent Token。
- `get_tool_manifest()`：返回能力边界、认证方式和安全说明。
- `get_current_user()`：读取当前账号和会员信息。

云端实时同步与持仓：

- `get_sync_meta()`：读取云端实时同步主数据更新时间、etag、大小，并返回最新云端历史快照摘要。
- `get_raw_sync_data(include_json_text=false)`：读取解析后的完整云端实时同步主数据，优先结构化组合接口。
- `get_records(include_transactions=false)`：读取持仓、自选、今日估算收益和汇总；会自动使用云端主数据里的全局/单基金行情源偏好。
- `get_summary()`：读取资产摘要。
- `get_transactions(code="", include_pending=true)`：读取交易流水。
- `get_groups()`：读取持仓分组和自选分组。
- `get_tags()`：读取全局标签和基金标签。
- `get_purchase_limit_watchlist()`：读取 App 限购观察列表（来自云端实时同步主数据）。

市场与基金：

- `search_item(query)`
- `get_item_estimate(codes, default_data_source_mode="huahua", data_source_mode_by_code?)`
- `get_fund_source_previews(code)`：单只基金 huahua/a/b/c 多行情源估算预览，用于解释或选择数据源。
- `get_item_detail(code)`
- `get_item_history(code)`
- `get_item_dividends(code)`
- `get_fund_timeline(code, source_mode="huahua")`
- `get_fund_fees(code)`：确认天数、申购状态、QDII/限大额日累计限购金额等交易规则。
- `get_batch_fund_fees(codes)`：批量获取费率/申购状态/限购规则，最多 50 只。
- `get_fund_period_rank(code)`
- `get_batch_fund_period_ranks(codes)`：批量获取多只基金排名，最多 50 只。
- `get_night_estimate(codes, force=false, view="forecast")`：QDII 基金夜间实时估值，含持仓穿透、汇率变动（需会员）。`force=true` 跳过服务端缓存；`view` 可为 `forecast` 或 `last_close`。
- `get_night_watchlist()`：读取用户在 App 夜盘估值页手动添加的基金代码列表（来自云端实时同步主数据），通常作为 `get_night_estimate` 的前置工具，免去用户手动报代码。
- `get_purchase_limit_watchlist()`：读取用户在 App 限购观察页保存的基金列表；可配合 `get_fund_fees` 检查申购状态和限购额度。
- `get_daily_rank()`
- `get_status()`
- `get_overview()`
- `get_sector_wind()`：板块风向，返回领涨/领跌板块和数据时间。
- `get_yesterday_rank()`：上一交易日基金涨跌榜。
- `get_fund_flow()`：资金流向数据（需 PRO 会员），返回 fundFlow、sectorFlow、polledAt。
- `get_indices()`
- `get_benchmark_history(code="sh000300")`
- `calculate_trading_dates(date, time_mode="PRE_MARKET", confirm_days=1)`
- `get_next_trading_day(date)`
- `get_fund_profile(code)`：基金画像（综合信息）。
- `get_batch_fund_profiles(codes)`：批量基金画像，最多 20 只。
- `get_holder_ranking()`：App 内持有人数排行榜。
- `get_instrument_catalog()`：指数/ETF 目录。
- `get_instrument_quotes(codes)`：指数/ETF 实时行情。
- `get_instrument_timeline(code, range="1d")`：指数/ETF 分时走势。
- `get_instrument_history(code, period="1m")`：指数/ETF 历史数据。

交易请求：

- `request_transaction(item_code, item_name, record_type, amount, date="", note="", group_name="")`
- `get_agent_requests()`
- `update_agent_request(request_id, status)`

个人报告：

- `submit_personal_strategy_report(title, summary, payload, client_message_id="")`：将个人策略报告投递到当前 Agent Token 所属用户的报告中心。需要显式 `messages:write` scope；如需同一个 token 同时读取持仓并投递个人报告，使用 `agent:full messages:write`。可基于用户明确授权的持仓、交易和行情数据生成。该工具不能广播，不能指定 `user_id`，不能写公共 Hermes 报告，也不得调用 `/api/hermes/reports`。

截图导入：

- `import_holding_screenshots(image_paths?, images_base64?, import_type="HOLDINGS")`：识别持仓/自选截图，返回 `items`、`summary`、`resolution_required` 等字段，不写入数据。`import_type` 可选 `HOLDINGS`（默认，按基金名称匹配）或 `WATCHLIST`（按 6 位代码优先精确匹配，自选截图务必传此值以提高准确率）。
- `import_transaction_screenshots(image_paths?, images_base64?)`：识别交易流水截图，返回交易类型、基金匹配、日期、金额/份额和歧义标记，不写入数据。
- `request_import_review(import_type, items, source_note?)`：把轻确认后的整批结果发送到 App 现有确认页。`import_type` 只能是 `HOLDINGS`、`WATCHLIST`、`TRANSACTIONS`。

社区与公告：

- `get_danmaku(code)`
- `send_danmaku(fund_code, text)`：发送弹幕，颜色由 App 根据涨跌自动设置
- `get_notices(since=0)`
- `get_community_ranking(tab="weekly", page=1, page_size=50)`：收益率排行榜（周/月/总）。
- `get_community_my_rank()`：我的排名。
- `get_community_user(uid)`：用户详情（十大重仓前5）。
- `get_community_stats()`：关注/粉丝数。
- `get_community_following()`：关注列表。
- `search_community_users(query)`：搜索用户（UID/昵称）。
- `get_community_notices(since=0)`：社区定向通知。
- `get_community_authorization()`：查询社区授权状态。
- `authorize_community(show_amount, anonymous)`：授权参与喵舍排行，直接生效，调用前必须确认。
- `revoke_community_authorization()`：取消授权，退出排行，直接生效，调用前必须确认。
- `follow_community_user(target_uid)`：关注/取消关注用户（取反操作），直接生效，调用前必须确认。

JCTI 投资人格：

- `analyze_jcti(personality_id, ye, wen, sui, duan)`：提交四维分数，获取 AI 个性化投资人格分析。

版本信息：

- `get_app_version()`：最新版本号、更新日志、下载地址。
- `get_app_versions(page, page_size)`：版本历史列表（分页）。

## 截图导入流程

1. Agent 调用截图识别工具，获取结构化结果。
2. Agent 只对未匹配或有歧义的条目做轻确认。
3. Agent 调用 `request_import_review` 创建一个批量导入请求。
4. App 展示一个 Agent Banner。
5. 用户点击后进入现有确认页：
   - `IMPORT_HOLDINGS` → 持仓截图导入确认页
   - `IMPORT_WATCHLIST` → 自选截图导入确认页
   - `IMPORT_TRANSACTIONS` → 交易记录截图导入确认页
6. 用户在 App 中批量编辑、分组、去重并确认后才写入。

## 数据完整性说明

云端实时同步主数据用于多端一致，包含：

- `funds`：基金、自选、持仓、成本、交易记录、标签、纪律、定投、基金级 `dataSourceMode`，以及恢复前展示所需的最后官方净值基线。
- `groups` / `watchlistGroups`：分组。
- `globalTags`：全局标签注册表。
- `fieldConfigs` / `watchlistFieldConfigs`：字段显示配置。
- `nightWatchCodes`：夜盘估值自选基金。
- `purchaseLimitWatchItems`：限购观察列表。
- `purchaseLimitWatchNightDefaultsMigrated`：限购观察是否已并入夜盘默认基金的迁移标记。
- `marketIndexSelection`：市场指数/ETF 看板选择。
- `userPreferences.fundDataSourceMode`：全局基金估值行情源模式。
- `emptyPortfolioConfirmed` / `clearedAt`：用户确认清空组合后生成的空组合主数据标记；这类主数据可恢复为空组合，不应当作异常空数据。
- `timestamp` / `version`：客户端导出时间和数据版本。

云端实时同步主数据只保留已删除基金不可重建的归档账本；当前基金的收益日历会用交易记录和历史净值重建。手动本地备份包含并恢复完整 ledger 和基金元数据，可离线恢复。

Agent 如需完整审计，应优先读取 `get_transactions` 和 `get_raw_sync_data`，不要只依赖 `get_summary`。

## 安全边界

- Agent Token 存储为 SHA256，不保存明文。
- Token 可设置有效期，可在 App 内撤销。
- 后端对 AgentToken 使用权限白名单。
- Agent Token 需要 PRO 会员；过期、撤销或会员状态不满足时会被拒绝。
- MCP 可读取敏感投资数据，包括持仓金额、交易流水和原始云端实时同步主数据；请只授权可信 Agent。
- 交易类能力只创建待确认请求，不直接写入交易。
- 截图导入只把识别结果发送到 App 确认页，不直接写入数据。
- 本地截图路径 `image_paths` 会读取并上传本机图片文件；只使用用户明确提供的路径。
- 社区授权、取消授权、关注/取消关注、社区收益同步是直接写操作，不经过 App 确认页。
- MCP 不提供云同步覆盖写入工具。
