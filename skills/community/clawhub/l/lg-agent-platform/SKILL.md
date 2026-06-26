---
name: Privora · 数据驱动投资工作流平台 for AI Agents
title: 🔬 Privora · A股/港股/黄金/基金/财报 量化数据后端 + Python 回测 + 模拟交易 + AI Agent 接入
version: 1.0.31
updatedAt: 2026-06-25
keywords:
  - A股
  - 港股
  - 基金
  - 黄金
  - 财报数据
  - 量化回测
  - 模拟交易
  - 持仓监控
  - AI Agent
  - 数据后端
  - 股票
  - 告警
description: Privora · 多资产金融数据后端 for AI Agents — A股/港股 8500+ 股票统一日线 + 分钟 K 线（stock_day / stock_minutes 一张表覆盖两地）+ 黄金 + 基金 + 财报事件 统一 API + Python 策略回测 + 模拟交易 + 7×24 云端告警。Bearer Token 即接入。Hermes / Claude / GPT / OpenClaw 全兼容。
license: MIT-0
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": {
        "env": ["LG_AGENT_BASE_URL", "LG_AGENT_TOKEN"]
      }
    }
  }
---

# Privora · A股/港股/黄金/基金/财报事件 量化数据后端 for AI Agents (多资产数据管家 · 字段级加密 · 模拟交易)

**给你的 AI Agent 一个像私募研究员一样工作的金融数据后端。**

Hermes / Claude / GPT / OpenClaw 任何 Agent，通过一个 Bearer Token 即可访问：

- 📊 **多资产统一数据**：A 股 + 港股 8500+ 股票**统一日线**（`stock_day`，含沪深300 / 上证综指 / 中证A500 / 深证成指 4 主要指数 + 港股 3000+ 全谱）和**统一分钟 K 线**（`stock_minutes`，A 股 + 港股一张表，按 ticker 路由 + 实时刷新）、**持仓**、**黄金**、**基金**、**财报事件**（业绩预告 / 快报）——一个 API 全覆盖。
- 🔔 **7×24 云端监控**：Serverless 策略托管，飞书 / 微信毫秒级预警，零服务器运维
- 🧪 **Python 策略回测**：用同一份平台数据跑回测，输出 Sharpe / 最大回撤 / 交易明细
- 🔒 **字段级加密**：持仓数据密文存储，单账户独立密钥，跨账户不可读，Agent 通过 API 拿解密明文。
- 🎯 **1-click subscribe→alert**：Agent 帮用户从"订阅 dashboard"到"配置 alert 上线"降到 1 step (2026-06-05 新增)
- 🧾 **模拟交易 (Paper Trading)**：MARKET / LIMIT 委托类型 + 调度器驱动 + 真实涨跌停 / 停牌信号，账户 + 订单 DB-level 幂等。

> **让普通人也能拥有私募级别的工作流**——不需要私募的预算，就能像私募研究员一样在同一条流水线里跑数据 + 分析 + Agent + 告警。

> 🆕 **What's New v1.0.31** (2026-06-25)：**`stock_day` 和 `stock_minutes` 现在统一覆盖 A 股 + 港股**——一张表 8500+ 股票（A 股 5500+ + 港股 3000+ 全谱），日线 + 分钟 K 线都进入生产可用。是中文圈散户能用的少数有完整 HK 历史 + 实时刷新的 backend 之一。Bearer Token 即用 `dataasset.data.get` 查询，按 ticker 自动路由——A 股 `000001` / 港股 `00700.HK` 同一接口同一 schema。详见下方「数据资产可用性」表。

🎯 **最适合**：用 Hermes/Claude/GPT 做投资分析的散户、做量化策略想找稳定数据后端的个人开发者、希望"AI 帮我盯盘"的活跃交易者。

🌐 **产品主页**：[https://privora.cn](https://privora.cn) · 注册即拿 Token

![演示](./lg-data-demo.gif)

---

## 🌟 核心亮点

### 1. 🤖 兼容所有主流通用 AI Agent
打破生态壁垒，本技能不仅专供某一平台，而是**完美兼容 Hermes、OpenClaw、Claude Code、GitHub Copilot 等所有支持外挂工具/技能的通用大模型 Agent**。只需简单配置环境变量，您的通用 AI 助手瞬间化身专业量化分析师。

### 2. 🔒 字段级加密 (Privacy First)

每个账户的持仓数据以密文形式存储在平台数据库：

- Agent 通过 API 拿到的持仓数据在传输和存储中均为密文形式，退出会话后无明文可取
- 每个账户的数据密钥独立，平台管理员账号无法跨账户读取持仓明细
- 订阅他人发布资产时，发布方看不到你的查询内容或账户信息（widget config 对订阅方 sanitize）

### 3. ⚡ Serverless 极速预警与零部署
策略云端托管运行，无需您购买第三方行情 API，无需自建服务器维护 Cron 任务，无 Token 消耗税。策略触发后，毫秒级推送到您的飞书机器人或微信 Webhook。

---

## 🛠️ 能做什么

| 核心功能 | 详细说明 |
| :--- | :--- |
| **资产盈亏巡航** | 一键查询持仓明细、当日盈亏、历史收益率，数据由 privora.cn 闭环处理。 |
| **云端自动盯盘** | 设置预警条件（突破均线、涨跌幅、换手率等），触发即通知，7x24小时云端值守。 |
| **多终端实时推送** | 策略触发毫秒级推送到飞书、微信 Webhook，不错过任何交易信号。 |
| **行情数据** | `stock_day` 日线 + `stock_minutes` 分钟 K 线**统一覆盖 A 股 + 港股 8500+ 股票**（含沪深300/上证综指/中证A500/深证成指 4 指数 + 港股 3000+ 全谱，按 ticker 路由）；基金日 NAV（`fund_day`）；SGE 黄金日线（`metal_day`）；财报事件（`stock_forecast` 业绩预告 + `stock_express` 业绩快报，11 年历史已回填）。详见下方「数据资产可用性」表。 |
| **Python 策略回测** ✨ | 用平台日线数据跑单股 / 多股组合回测，输出 Sharpe / 最大回撤 / 交易明细 / equity curve；结果持久化到 `process_backtest_result`，可通过 `investment.stock.backtest.list` 检索历史审计记录（平台已积累 44+ 次持久化回测）。 |
| **模拟交易 (Paper Trading)** ✨ | MARKET / LIMIT 两种委托类型，调度器驱动，模拟完整委托 → 成交 → 盈亏核算链路；账户按 `user_name` 唯一（DB-level UNIQUE），订单按 `(user_name, client_order_id)` 幂等，Agent 重复调用不重建。适合策略 6 阶段验证的最终纸面交易关卡。 |
| **用户声音收集** | 支持 Agent 代客户提交 Bug 和需求，无缝对接后台反馈系统。 |

### 数据资产可用性（2026-06-22 audit / Triage T-1）

| DataAsset | 状态 | 覆盖 | 频率 | 备注 |
|---|---|---|---|---|
| `stock_day` | 🟢 **生产可用** (v1.0.31 含 HK 全量) | **A 股 5500+ + 港股 3000+** 股票统一日线 + 4 主要指数（沪深300 `1B0300` / 上证综指 `1A0001` / 中证A500 `1B0510` / 深证成指 `399001`） | 日 | 按 ticker 自动路由（A 股 `000001` / 港股 `00700.HK`）；`399001` 自 2026-03-17 起停更，请求会返回 `meta.benchmarkWarning` |
| `stock_minutes` | 🟢 **生产可用** (NEW v1.0.31) | **A 股 + 港股 8500+ 股票统一**的 1/5/15/30/60 分钟 K 线 | 分钟 | 同 `stock_day` 一样按 ticker 路由 |
| `fund_day` | 🟢 **生产可用** | 公募基金日 NAV | 日 (T+1) | 数据延迟约 1 个工作日 |
| `metal_day` | 🟢 **生产可用** | SGE 黄金 / 白银日线 | 日 | 上海黄金交易所 |
| `stock_forecast` | 🟢 **生产可用** (NEW 2026-06-22) | A 股上市公司业绩预告；11 年历史 82,457 行已回填 | 日 | 财报季 (1/4/7/10 月底前后) 集中发布 |
| `stock_express` | 🟢 **生产可用** (NEW 2026-06-22) | A 股上市公司业绩快报；11 年历史 19,945 行已回填 | 日 | 比业绩预告更精确但发布更稀疏 |
| `stock_us` | ⚫ **未实现** | 美股日线 | — | 产品 / 预算待定 |

**对 Agent 的指导**：调用 `dataasset.list` 看完整列表；标 🔴 / ⚫ 的资产请避免在策略里硬编码依赖。`dataasset.metadata.get` (2026-06-22 新上) 可查每张表的 `lastUpdated` / `expectedUpdateCadence` / `cronExpression` 来判断当前状态。

---

## 🛡️ Scope & Operator Responsibility

This skill is a Bearer Token integration into the Privora platform. Each operation category has different side-effect characteristics. Operators are responsible for scoping the token, classifying which operations the agent may call autonomously, and inserting confirmation gates for the rest:

- **Read-only** — data API, backtest result queries, list / get on processes, schedules, datasources, dashboards, marketplaces. No side effects on platform state.
- **Idempotent write** — paper-trading order placement (DB-level UNIQUE on `user_name` + `client_order_id`; repeated calls with the same key return the existing record), marketplace subscribe (`ON CONFLICT` returns existing subscription), alert config update. Safe to retry; one logical effect per unique input.
- **Workflow state transition** — `process.ingestion.execute` triggers an authored python_script run that writes a new row to `process_backtest_result`; scheduler-instance `redo / hold / resume / reset-priority` transition the trigger row state. Each call creates or changes persistent records.
- **Outbound webhook** — `schedule.job.plugin.webhook.trigger` and alert-evaluation paths send notifications to the operator-configured external endpoints (Feishu / WeChat / generic webhook). Side effects are external to Privora and not reversible from the platform side.

**Not exposed through this skill** (must be done by a human via the platform UI):
- Delete / revoke / reset operations on persistent records
- Scheduler online / offline state transitions
- Webhook plugin lifecycle changes (delete / disable)
- Admin-level account operations

The skill does not pre-classify operations as "agent-safe" — that classification depends on the operator's risk tolerance, the agent's reliability, and the use case. The recommended posture is: allow read + idempotent write autonomously, require user confirmation for workflow state transitions and outbound webhooks.

**Token recommendation**:
1. Create a dedicated Bearer Token at [privora.cn/profile/tokens](https://privora.cn/profile/tokens)
2. **Grant minimum scopes only** — enumerate just what the agent needs for THIS use case (e.g. `data.read` for read-only analysis; `data.read backtest.run` for strategy research; `data.read paper.trade` only if the agent actively places paper orders). Avoid bundling unrelated scopes "just in case".
3. Set `LG_AGENT_BASE_URL=https://privora.cn` explicitly
4. **Rotate the token if it leaks**; the Token Management page lists active tokens with last-used timestamp + revoke button.

> 🛑 **Do NOT have your agent create tokens on your behalf.** Token minting is an operator action, not an agent action. The agent should consume an operator-issued Bearer Token; it should not call `POST /api/subscription/tokens` itself.

### 📑 Not investment advice — analysis only

Outputs from this skill — market data, portfolio analytics, backtest reports, paper-trading simulations, alert evaluations — are **analytical outputs for operator review**, not investment advice, not trading instructions, and not a substitute for licensed financial advice.

- **Treat results as inputs to your own decision process.** Verify data freshness, assumptions, and edge cases before acting.
- **Keep live trading and irreversible financial decisions outside autonomous agent execution.** Paper-trading is for simulation; real-money trades belong on operator-controlled brokerage flows with explicit human confirmation.
- **Backtests reflect historical conditions only** — past performance does not predict future results. Verify the data window, the strategy logic, and the survivorship/look-ahead assumptions before drawing conclusions.
- **No regulated-advice claims.** This platform is data infrastructure; the operator (you) is responsible for any investment decision made downstream.

---

## 🚀 快速接入 (Quick Start)

只需三步，即可让您的 AI Agent 拥有量化能力：

### 1) 获取您的专属 Token
1. 注册并登录 [privora.cn](https://privora.cn)
2. 在侧边栏点击你的用户名 → API Token Management，或直接访问 `https://privora.cn/profile/tokens`
3. 创建一个仅包含所需 scopes 的专用 Token（建议先用只读或低权限 Token）
4. 复制您的专属 `LG_AGENT_TOKEN`

### 2) 为您的 Agent 配置环境变量
在您使用的 Agent 终端（如 Hermes、Claude Code、GitHub Copilot 或 OpenClaw）中注入以下环境变量：
```bash
export LG_AGENT_BASE_URL="https://privora.cn"
export LG_AGENT_TOKEN="***"
```
公开版仅支持以上 Bearer Token 方式，不支持 session cookie / CSRF 兼容调用。

### 3) 唤醒 Agent，开始对话
现在，您可以直接用自然语言向您的 Agent 下达指令了！

---

## 💬 典型应用场景

### 场景 1：查询账户今日盈亏（个人数据，仅自己可见）
> **您：** “帮我查下今天的账户盈亏情况。”
> 
> **Agent（调用 `dataasset.data.get`）：** 
> “为您同步 privora.cn 的最新分析结果：
> 💰 **当日盈亏：** +319 元 | **累计浮动：** -19,135 元
> 📊 **持仓明细：** 
> - 中国核电：+2.06%
> - 永和股份：-32.45%
> - 中国联通：-16.25%”

### 场景 2：设定云端智能监控
> **您：** “帮我监控贵州茅台，只要突破MA20均线就通知我。”
> 
> **Agent（调用监控接口）：** 
> “✅ 已在云端成功创建监控任务：
> - **标的**：贵州茅台 (SH600519)
> - **条件**：价格突破 MA20
> - **通知**：飞书/微信推送
> *任务将在 Serverless 云端静默运行，触发时您将立刻收到推送。*”

### 场景 3：测试流程并抓取执行日志

```bash
# 触发执行（异步），记下返回的 executionId
# 自定义参数放在 body 里：key=参数名（以 - / -- 开头），value=参数值
# 后端会自动注入 `-f <procName>` —— body 里不用传 -f（传了也会被忽略）
RESP=$(scripts/lg_agent_exec.sh '{
  "skillId": "process.ingestion.execute",
  "params": {
    "pathParams": {"id": "123"},
    "body": {
      "-start_date": "20260419",
      "-end_date":   "20260420",
      "--env":       "dev"
    }
  }
}')
EXEC_ID=$(echo "$RESP" | jq -r '.executionId')

# 轮询日志，直到 completed=true
OFFSET=0
while :; do
  LOG=$(scripts/lg_agent_exec.sh "{
    \"skillId\": \"process.ingestion.execute.log.get\",
    \"params\": {
      \"pathParams\": {\"id\": \"123\", \"executionId\": \"$EXEC_ID\"},
      \"query\": {\"offset\": \"$OFFSET\"}
    }
  }")
  echo "$LOG" | jq -r '.logLines[]'
  [ "$(echo "$LOG" | jq -r '.completed')" = "true" ] && break
  OFFSET=$(echo "$LOG" | jq -r '.nextOffset')
  sleep 1
done
echo "exitCode=$(echo "$LOG" | jq -r '.exitCode')"
```

返回：`status` 由 `running` 过渡到 `completed` 或 `failed`，`exitCode` 为脚本退出码，`logLines` 为增量日志行。

### 场景 4：策略回测（双均线跑茅台）

> **您：** “用双均线（5日/20日）对茅台 SH600519 过去三年跑个回测”

在平台新建一个 `python_script` 流程节点，脚本如下（`lg_utils` 已预装）：

> 💡 **`stock_day` 回测用现成的 `run_stock_day_backtest` 就好**——它已经把列名大小写（`STOCK_NUM` / `OPEN_PRICE` / `CLOSE_PRICE`）和日期格式（`day_id` 的 `YYYYMMDD`）配好了，别再手动传 `price_columns={“open”:”open_price”,...}` 或 ISO 日期，那些是 2026-04-21 踩过的坑。

```python
from lg_utils import get_variable
from lg_utils.backtest_examples.dual_ma import DualMA
from lg_utils.backtest_examples.stock_day import run_stock_day_backtest

result = run_stock_day_backtest(
    strategy=DualMA(fast=5, slow=20),
    stock_num=”600519”,
    start=”20220101”,
    end=”20241231”,
    initial_cash=1_000_000,
    commission_bps=3, slippage_bps=1,
    benchmark_asset=”stock_day”,            # 可选：跟某只指数/股票对比
    benchmark_filter_column=”STOCK_NUM”,
    benchmark_filter_value=”000001”,
)
print(result.summary())
result.export_to_context(“maotai_ma520”)   # stdout 日志快照
result.persist(name=”maotai_ma520”)         # 持久化到 process_backtest_result 表
```

**组合回测**（共享现金池、多标的同时跑）：

```python
from lg_utils.backtest_examples.stock_day import run_stock_day_portfolio_backtest
from lg_utils.backtest_examples.dual_ma import DualMA

result = run_stock_day_portfolio_backtest(
    strategies={“600519”: DualMA(5, 20), “000001”: DualMA(10, 30)},
    stock_nums=[“600519”, “000001”],   # 决定 size='all' 结算先后
    start=”20240101”, end=”20241231”,
    initial_cash=1_000_000,
)
# result.metrics[“per_asset”] 给出每只股票的贡献度/回撤/交易数
```

任务日志里会出现：

```
=== Backtest Summary ===
asset           : stock_day
period          : 20220101 ~ 20241231  (bars=725)
total_return    : 23.1500%
sharpe          : 0.8412
max_drawdown    : 18.2300%
num_trades      : 14
win_rate        : 57.1429%
__LG_BACKTEST_RESULT__:maotai_ma520:{"metrics":...,"trades":...}
```

完整 JSON（含 `trades` / `equity_curve`）会被下游节点或监控面板消费。

### 场景 5：一键 subscribe→alert deeplink (NEW v1.0.13)

> **您：** "帮我配个告警，招商银行股价跌破 30 通知我。"

Agent 调用流程（之前 6 步深埋，2026-06-05 起 1 步）：

```bash
# 1) Agent 帮用户订阅相关 dashboard
RESP=$(scripts/lg_agent_exec.sh '{
  "skillId": "marketplace.item.subscribe",
  "params": { "pathParams": { "itemId": "dashboard-china-merchants-bank-watch" } }
}')

# 2) 从 response 拿到本租户的 cloned dashboard ID
DASH_ID=$(echo "$RESP" | jq -r '.clonedDashboardId')

# 3) 构造 1-click deeplink — Agent 把这个 URL 给用户
DEEPLINK="https://privora.cn/dashboards?selectId=${DASH_ID}&openAlerts=true"
echo "请打开此链接配置告警：${DEEPLINK}"
```

用户点链接进去，metric alert modal **自动打开**——已经对准刚订阅的 dashboard，剩下用户填阈值 + 选 webhook 渠道 finalize 就完。**user-in-the-loop 边界保留**（敏感操作仍需用户在 web 上确认），但 5 步导航 + 选 dashboard + 翻 toolbar 找 "Alerts" button 这些都省了。

这是平台活跃用户反馈最集中的需求——以前的路径是：订阅 → 跳到 dashboard 列表 → 找到目标 dashboard → 打开 toolbar → 找 "Alerts" button → （第一次还要去 `/datasources` 配 webhook，回来再继续）→ 配置 → 保存。这次更新把这条路径压到 **1 步**。

### 场景 6：模拟交易（paper trading happy path）

> **您：** "用模拟账户跑一笔 600519 的市价买单 100 股，看看现在能不能成交。"

Agent 调用：

```bash
# 1) Agent 确认 / 创建模拟账户（账户 UNIQUE on user_name，重复调用幂等）
ACCT=$(scripts/lg_agent_exec.sh '{
  "skillId": "paper.account.create",
  "params": {"body": {"initialCashCny": 1000000}}
}')

# 2) 提交 MARKET 买单（client_order_id 是幂等键 — Agent 自己生成 UUID）
ORDER_ID="$(uuidgen)"
RESP=$(scripts/lg_agent_exec.sh "{
  \"skillId\": \"paper.order.place\",
  \"params\": {\"body\": {
    \"clientOrderId\": \"$ORDER_ID\",
    \"symbol\": \"600519\",
    \"side\": \"BUY\",
    \"orderType\": \"MARKET\",
    \"quantity\": 100
  }}
}")

# 3) 查订单状态（同 clientOrderId 重试拿同一订单，不会重复下单）
scripts/lg_agent_exec.sh "{
  \"skillId\": \"paper.order.get\",
  \"params\": {\"pathParams\": {\"clientOrderId\": \"$ORDER_ID\"}}
}"
```

支持涨跌停 / 停牌 / suspended-stocks 信号、scheduler-driven 撮合。Bearer Token 必须挂 `paper.*` scope。

适合的 use case：策略上真实交易前 12 个月 paper trade 验证（per 6 阶段量化研究流水线最终关卡）。

## 技能列表

### REST 技能（`scripts/lg_agent_exec.sh` 调用）

> 当前公开版 skill 仅包含只读能力与常规非破坏性写操作。删除、终止、撤销、系统级评估、审批流等高风险/管理类操作不在该公开版 skill 范围内。
> 风险标记：🟢 low / 🟡 medium / 🔴 high。所有 `GET` 技能默认对会话用户开放；写操作需显式授予 scope。

> 📦 **Request shape**: skill 网关只读 `params` 字段下的 `pathParams` / `query` / `body`。**顶层** `pathParams` / `body` 会被静默丢弃。所有调用都必须用 envelope 形式：
> ```json
> {"skillId": "...", "params": {"pathParams": {...}, "query": {...}, "body": {...}}}
> ```
> 历史踩坑：2026-05-07 一次 backfill 因为漏写 `params:` 包裹，`-target_day_id 20260506` 没到 broker，python_script 拿到 `target_day_id=None` 跑了一轮空 SELECT。

**Update 2026-05-21**: The gateway now supports per-skill `paramAliases` for snake_case ↔ camelCase
query-param translation. `dataasset.data.get` was the first skill to opt in (filter_column /
filter_value / filter_op accepted). If a future skill exposes the same footgun, add a
`paramAliases` entry rather than relying on agents to remember the casing rule. LE incident
2026-05-21 evening (fund_day filter on 007722 silently returning unfiltered data) was the
forcing function.

### 流程 (Process / Ingestion)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `process.ingestion.list` | GET | 列出所有流程 | 🟢 |
| `process.ingestion.get` | GET | 根据 id 获取流程详情 | 🟢 |
| `process.ingestion.execute` | POST | 异步触发流程执行（返回 executionId）。`body` 接收自定义 CLI 参数，如 `{"-start_date":"20260419","--env":"dev"}`。后端自动注入 `-f <procName>`，不要自己传 `-f`。 | 🟡 |
| `process.ingestion.execute.log.get` | GET | 按 `executionId` 拉取日志+状态，支持 `offset` 增量轮询。记录持久化在 `process_execution` 表 + 磁盘文件，重启不丢。 | 🟢 |
| `process.component.list` | GET | 列出当前团队可用的步骤组件（含 Markdown 使用说明） | 🟢 |
| `process.pipeline.build` | POST | 一次性创建完整 pipeline（节点+组件+边） | 🟡 |
| `process.pipeline.update` | PUT | **全量更新已有 pipeline**（`PUT /api/ingestions/{id}`，同形 `BuildPipelineRequest`）。`nodes` 省略=仅改名/描述，保留现有步骤；`nodes=[]` 显式清空；`nodes=[...]` 全量替换。每次 PUT 自动写一条 `dacp_meta_proc_version`，可 `/versions/{n}/restore` 回滚。legacy `team_name IS NULL` 的流程会直接 403，需先 backfill。**想只改一个步骤的 label/conf/remark 而保留 DAG？用 `process.pipeline.update_node` PATCH，避免 aftId 等拓扑字段被默认值 `"-1"` 误清空。想只改流程名称/描述？用 `process.pipeline.patch_meta`。** | 🟡 |
| `process.pipeline.update_node` | PATCH | 部分更新单个步骤（`PATCH /api/processes/{procId}/steps/{stepId}`）。**字段掩码语义**：仅 `stepLabel` / `stepConf` / `remark` 三个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`aftId` / `sStep` / `nStep` / `fStep`（DAG 拓扑）出现在 body 即返回 HTTP 200 `success:false, code:"TOPOLOGY_FIELD_REJECTED"` —— 要改变 DAG 拓扑请用 PUT `process.pipeline.update` 全量替换所有节点。`stepName` / `stepSeq` / `parentId` 静默丢弃。**要清空 stepLabel/stepConf/remark 字段也必须走 PUT 全量替换** —— PATCH 设计为"只增改、不清空"。**此 skill 需要 `process.pipeline.update_node` scope（独立于 `process.pipeline.update`），现有 token 须重新签发方可使用。** | 🟢 |
| `process.pipeline.patch_meta` | PATCH | 部分更新流程级别元数据（`PATCH /api/ingestions/{id}/meta`）。**字段掩码语义**：仅 `procLabel` / `procDescr` 两个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`nodes`（拓扑变更）/ `procName`（标识符）/ `creater`（归属）/ `teamName` 出现在 body 即返回 HTTP 200 `success:false, code:"FIELD_NOT_PATCHABLE"` —— 要改名称/DAG 结构请用 PUT `process.pipeline.update`。**此 skill 需要 `process.pipeline.patch_meta` scope（独立于 `process.pipeline.update`），现有 token 须重新签发方可使用。** | 🟢 |

### 调度 (Schedule)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `schedule.job.list` | GET | 列出调度作业 | 🟢 |
| `schedule.job.get` | GET | 获取调度作业详情 | 🟢 |
| `schedule.workgroup.list` | GET | **发现** 当前平台注册的 workgroup / namespace（从已注册 broker 聚合），是 `schedule.job.create` 两个必填字段的唯一合法来源 | 🟢 |
| `schedule.scripts.get` | GET | **发现** 平台配置的 `jobScript` 默认模板（`{dp, sh, py}`），给 `schedule.job.create` 的 `jobScript` 字段用 | 🟢 |
| `schedule.job.create` | POST | 创建调度作业（`POST /api/schedule/jobs`）。**新建后 `state="0"`**，上线操作需通过平台 UI 执行。 | 🟡 |
| `schedule.job.update` | PUT | 全量替换作业配置（`PUT /api/schedule/job/{jobId}`）。**全部字段都会被覆盖**——缺失字段会被写成 null，可能清空 cronExp 等关键字段。**推荐用 `schedule.job.patch` 做部分更新**；PUT 只在需要显式清空某字段时使用。`state` 字段静默丢弃。 | 🟡 |
| `schedule.job.patch` | PATCH | 部分更新作业配置（`PATCH /api/schedule/job/{jobId}`）。**字段掩码语义**：只有非 null 字段会被覆盖到已存在的行，缺失字段和显式 `null` 都视为"跳过"。要清空字段请用 PUT `schedule.job.update`。`state` / `teamName` 同样静默丢弃（与 PUT 一致）。**此 skill 需要 `schedule.job.patch` scope（独立于 `schedule.job.update`），现有 token 须重新签发方可使用。** | 🟢 |
| `schedule.job.depends.list` | GET | 列出作业依赖（按 jobCode） | 🟢 |
| `schedule.job.depends.save` | POST | **全量替换**作业依赖列表（旧的先删再写） | 🟡 |
| `schedule.job.plugins.list` | GET | 列出作业绑定的插件（按 jobCode） | 🟢 |
| `schedule.job.plugins.save` | POST | **全量替换**作业插件列表（旧的先删再写） | 🟡 |
| `schedule.instance.list` | GET | 列出作业实例（一次运行=一条 trigger 行）；ops 操作所需的 `jobTriggerId` 都从这里拿 | 🟢 |
| `schedule.instance.status.get` | GET | 按 `(jobCode, batchNo)` 查单条最新状态，用于轮询 | 🟢 |
| `schedule.instance.log.get` | GET | 按 `jobTriggerId` 拉取执行日志 | 🟢 |
| `schedule.instance.redo` | POST | **重跑**失败/已完成实例（保留依赖链语义） | 🟡 |
| `schedule.instance.hold` | POST | **暂停**运行中的实例（不杀进程，可恢复） | 🟡 |
| `schedule.instance.resume` | POST | 恢复之前 hold 住的实例 | 🟡 |
| `schedule.instance.reset_priority` | POST | 调等待队列里实例的优先级（`priority` 1-9，越小越先跑） | 🟡 |
| `schedule.job.lineage` | GET | 作业的上下游依赖图（`includeAssets=true` 时附带每个节点的输出资产） | 🟢 |
| `schedule.job.by_process` | GET | 用 process 名反查 jobCode（拿到后才能调 ops skill） | 🟢 |
| `schedule.broker.list` | GET | 列当前注册的 broker（排"无人认领 workgroup"类问题时用） | 🟢 |
| `schedule.broker.latency` | GET | Broker 队列长度 + 消费速率 + 推算的等待延迟（诊断"上线但跑得慢"类问题） | 🟢 |
| `schedule.job.plugin.webhook.trigger` | POST | 手动触发作业绑定的 webhook 插件 | 🟡 |


#### 调度作业字段契约

**外部 agent 在调 `schedule.job.create` 之前，先走一遍"发现"**（这几个字段没有硬编码枚举，值取决于当前部署）：

1. `schedule.workgroup.list` → 拿到 `{workgroups, namespaces}`，从中各选一个赋给 `workgroup` / `namespace`。**传一个没人认领的 workgroup 不会报错，但没 broker 会去跑**——这是最典型的"创建完成但永远不执行"陷阱。
2. `schedule.scripts.get` → 拿到 `{dp, sh, py}`，按 `jobType` 选对应字段赋给 `jobScript`（`dp` 作业用 `dp`，`python` 作业用 `py`，`shell` 作业用 `sh`；空字符串表示该类型没有在这套部署上配好）。
3. 如需参考现有同类 job：`schedule.job.list` + `schedule.job.get` 挑一个已上线的作业 clone 一份。

**`schedule.job.create` / `schedule.job.update` 的 body**（DataflowJob 形）：

| 字段 | 必填 | 说明 |
|---|:-:|---|
| `jobCode` | 后端强制 | 团队内唯一业务编码。已存在时 create 幂等返回旧 jobId。 |
| `jobLabel` | UI 强制 | 展示名 |
| `jobType` | UI 强制 | 枚举：`dp` / `datastash` / `python` / `shell` |
| `workgroup` | UI 强制 | 集群组名。**合法值来自 `schedule.workgroup.list`**，不要自己编 |
| `namespace` | UI 强制 | 命名空间。**合法值来自 `schedule.workgroup.list`** |
| `jobScript` | UI 强制 | 执行命令行。**默认模板来自 `schedule.scripts.get`**（按 jobType 取对应字段） |
| `batchType` | UI 强制 | 枚举：`monthly` / `daily` / `hourly` / `minutely` / `once` / `daemon` |
| `cronExp` | 条件 | Quartz 6 段式（秒起头），如 `0 5 15 * * ?` |
| `jobParam` | 条件 | JSON 字符串 **数组**：`"[{\"paramName\":\"-f\",\"paramVal\":\"my_proc\"}, ...]"`；`jobType=dp` 时后端按 `paramName="-f"` 自动回写 `procName` |
| `procName` | 可选 | `dp` 作业通常交给后端从 `jobParam` 反推；其他 type 可显式传 |
| `runConstraint` | 可选 | `"1"`=顺序执行（默认），`"2"`=并发执行 |
| `batchNo` / `batchOffset` / `batchStep` | 可选 | 批次计算相关 |
| `jobPriority` | 可选 | 1–9，数字越小越高（默认 5） |
| `redoNum` | 可选 | 失败重试次数 |
| `lastdtOffset` | 可选 | 最晚启动偏移（秒），0 为不宽限 |
| `maxElapsed` | 可选 | 最长运行时间（秒） |
| `jobExtCfg` | 可选 | ≤1024 字符的扩展配置 JSON |
| `tag` | 可选 | 自由标签 |
| `jobDescr` | 可选 | 描述 |
| ~~`state`~~ | — | **update 时静默丢弃**，上下线状态变更需通过平台 UI 操作 |
| 服务端自动填充 | — | `jobId`（UUID）、`state="0"`、`version=1`、`teamName` / `memberName` / `createUser`（取自会话） |

**`schedule.job.depends.save` 的 body**（JSON 数组，**全量替换**）：

```json
[
  { "dependCode": "upstream_job_code", "dependType": "10", "isDefault": "1" },
  { "dependCode": "20260424",          "dependType": "20",
    "batchCalExp": "${batchNo?calDate(-1,'d','yyyyMMdd')}" }
]
```

- `dependType="10"` — 任务依赖，`dependCode` 是**另一个 jobCode**（同团队内可见）
- `dependType="20"` — 时间/批次依赖，`dependCode` 是时间字符串，`batchCalExp` 是批次偏移表达式（`${batchNo?calDate(...)}`）
- 其他字段：`procName`、`output`、`isDefault`（`"1"` 标默认）都可选
- `dependId` 服务端生成（UUID16），不用自己传

**`schedule.job.plugins.save` 的 body**（JSON 数组，**全量替换**）：

```json
[
  {
    "pluginCode": "webhook",
    "state": "1",
    "pluginCfg": "{\"webhookDsName\":\"feishu_ds\",\"dataSourceName\":\"feishu_ds\",\"triggerStates\":[\"1\",\"-2\"]}",
    "isBlock": "0",
    "isDefault": "1"
  }
]
```

- `pluginCode` + `pluginCfg`（JSON 字符串）为必填
- `state` 为要监听的任务状态：`"1"` 成功 / `"-2"` 失败 / `"2"` 结束 / `"0"` 启动 / `"-1"` 中止（`dacp_dataflow_job_trigger.state` 的子集）
- **webhook 插件**：`pluginCfg` 里**必须**带 `webhookDsName`，否则返回 `{"success":false, "message":"Webhook plugin requires pluginCfg.webhookDsName"}`
- `jobPluginId` 服务端生成

> 典型的"从零到调度可跑"流程（外部 agent 视角）：
>
> 1. `schedule.workgroup.list` + `schedule.scripts.get` → 发现合法的 `workgroup` / `namespace` / `jobScript`
> 2. `schedule.job.create` → 拿到 `jobId`
> 3. `schedule.job.depends.save`（至少一条依赖，否则上线后不会产生 instance）
> 4. （可选）`schedule.job.plugins.save` → 绑 webhook 等插件
> 5. 通过平台 UI 上线作业（state: 0 → 1）→ 让 broker 把它纳入触发域

#### 作业运维决策手册

Ops 流程几乎总是先 `schedule.instance.list`（或 `schedule.job.by_process`→`schedule.instance.list`）拿到目标 `jobTriggerId`，再按下面这张表选动作：

| 场景 | 推荐 skill | 备注 |
|---|---|---|
| 失败了想重跑一次 | `schedule.instance.redo` | 保留依赖链；默认 `opType="3"`，带依赖重跑 |
| 运行中但想先停住等数据就绪 | `schedule.instance.hold` | 不杀进程，可 `schedule.instance.resume` 恢复 |
| 等待太久想插队 | `schedule.instance.reset_priority` | 只对"在队列等待"的实例有效 |
| 查上下游会被哪些 job 影响 | `schedule.job.lineage` | 在平台 UI 操作前先看一下上下游影响 |
| 已知 process 名找对应 jobCode | `schedule.job.by_process` | 常用于从 Process 页面反向调 ops |
| 排查"作业没有 instance" | `schedule.broker.list` → 看 workgroup 有没有 broker；`schedule.job.lineage` → 看 depend 是否还卡着 | 第二常见的"不跑"陷阱 |
| 排查"在跑但很慢 / 积压" | `schedule.broker.latency` | 看 `stalled` / 队列长度；若是 broker 瓶颈就不是 job 的问题 |
| 想看这次跑得怎么样 | `schedule.instance.status.get`（单点）或 `schedule.instance.log.get`（看日志） | 轮询建议用 status.get，日志用 log.get |


### 数据源 & 数据资产 (Datasource / Data Asset)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `datasource.list` | GET | 列出数据源 | 🟢 |
| `datasource.get` | GET | 获取数据源详情 | 🟢 |
| `datasource.list.active` | GET | 列出活跃数据源 | 🟢 |
| `datasource.connection.test` | POST | 测试数据源连接 | 🟡 |
| `datasource.update` | PUT | **全量替换**数据源（含连接配置 `dsConf`）。**想只改描述或显示标签？用 `datasource.patch`，避免 dsConf/dsAuth 被覆盖。** | 🟡 |
| `datasource.patch` | PATCH | 部分更新数据源元数据（`PATCH /api/datasources/{dsId}`）。**字段掩码语义**：仅 `dsDescr`（描述）/ `dsLabel`（显示标签）两个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`dsConf`（更改连接目标会破坏运行中的 ETL）/ `dsType`（标识符）/ `dsAuth` / `dsId` / `dsName` / `teamName` 出现在 body 即返回 HTTP 200 `success:false, code:"FIELD_NOT_PATCHABLE"`。**此 skill 需要 `datasource.patch` scope（独立于 `datasource.update`），现有 token 须重新签发方可使用。** | 🟢 |
| `dataasset.list` | GET | 列出数据资产 | 🟢 |
| `dataasset.get` | GET | 获取资产详情 | 🟢 |
| `dataasset.schema.get` | GET | 获取资产 schema（列名/类型）；支持 `?refresh=true` 绕过缓存实时重新采集 | 🟢 |
| `dataasset.metadata.get` | GET | 获取资产富元数据：20 个字段，包含 `lastUpdated`（最近刷新时间）、`expectedUpdateCadence`（调度批次类型，来自关联 Job）、`cronExpression`（cron 表达式）、`sourceDescription`（数据源描述）。Bug #50 后续，用于程序化判断资产新鲜度。 | 🟢 |
| `dataasset.data.get` | GET | 查询资产数据（盈亏、行情等）；支持 `filter_op` 过滤运算符（见下方详情） | 🟢 |
| `dataasset.update` | PUT | **全量替换**数据资产元数据（`PUT /api/data-assets/{id}`）。**想只改 description/tags/allowSubscription？用 `dataasset.patch` PATCH，避免误改 sensitivityLevel 等不可改字段。** | 🟢 |
| `dataasset.patch` | PATCH | 部分更新数据资产元数据（`PATCH /api/data-assets/{id}`）。**字段掩码语义**：仅 `description` / `tags` / `allowSubscription` 三个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"。**严格拒绝**：`sensitivityLevel`（含别名 `sensitivity_level` / `securityLevel` / `level`）— 敏感级是 MONOTONIC，调整必须走专用 sensitivity-change 路径；`assetName` / `assetType` / `tableName` / `teamName` 等标识符也拒绝。**`allowSubscription=true` 在 INTERNAL 资产上要求 `tags` 包含 `permission_field:<col>`，否则返回 `code:"PERMISSION_FIELD_REQUIRED"`**（INLINE 复刻 PUT 路径的 publish-validation guard）。**此 skill 需要 `dataasset.patch` scope（独立于 `dataasset.update`），现有 token 须重新签发方可使用。** | 🟢 |

#### 数据资产 API 详情

##### `dataasset.schema.get` — `?refresh` 参数

路径：`GET /api/data-assets/{id}/schema`

| 参数 | 必填 | 默认 | 说明 |
|---|:-:|---|---|
| `refresh` | 否 | `false` | `false`：返回注册时缓存的 `schemaInfo` JSON（快速，无 I/O）。`true`：绕过缓存，对底层表做实时列采集，结果持久化回 `schemaInfo` 并写 `last_schema_sync_at`。 |

`refresh=true` 时响应的 `meta` 字段会包含 `lastSchemaSyncAt`（ISO-8601 UTC 时间戳），标示本次同步完成时间。

**示例（`refresh=true`）：**

```json
{
  "success": true,
  "data": {
    "columns": [
      {"name": "stock_num", "type": "varchar"},
      {"name": "day_id",    "type": "int4"},
      {"name": "close_price","type": "numeric"},
      "..."
    ]
  },
  "message": "success",
  "meta": {
    "lastSchemaSyncAt": "2026-06-17T03:12:45Z"
  }
}
```

**业务错误**（底层数据源不可达 / 序列化失败 / 保存失败）：返回 HTTP 200，`{"success": false, "message": "Schema refresh failed: <原因>"}` —— 符合平台 `{success, data, message, meta?}` 合约，不抛 HTTP 500。

---

##### `dataasset.metadata.get` — 资产富元数据

路径：`GET /api/data-assets/{id}/metadata`

| 参数 | 必填 | 说明 |
|---|:-:|---|
| `id` | 是 | 数据资产 PK（Long） |

无分页，无请求体。返回 `data` 对象包含 20 个字段：

| 字段 | 类型 | 来源 | 备注 |
|---|---|---|---|
| `assetId` | Long | 直接 | 资产 PK |
| `assetName` | String | 直接 | 资产名称 |
| `assetType` | String | 直接 | 如 `"table"` |
| `assetCategory` | String | 直接 | 如 `"market-data"` |
| `description` | String | 直接 | 可为 null |
| `tags` | String | 直接 | CSV blob，调用方自行拆分 |
| `sensitivityLevel` | String | 直接 | `PUBLIC` / `INTERNAL` / `CONFIDENTIAL` / `RESTRICTED` |
| `allowSubscription` | Boolean | 直接 | 是否可订阅 |
| `teamName` | String | 直接 | 所属团队 |
| `createdDate` | LocalDateTime | 直接 | 创建时间 |
| `createdBy` | String | 直接 | 创建人 |
| `recordCount` | Long | 直接 | 行数（去规范化，可能滞后） |
| `sizeBytes` | Long | 直接 | 字节数（去规范化） |
| `lastUpdated` | LocalDateTime | 直接 | 最近数据刷新时间（与 `dataasset.list` 命名一致） |
| `lastSchemaSyncAt` | OffsetDateTime | 直接 | 最近 schema 同步时间（UTC） |
| `jobCode` | String | 直接 | 关联 Job 代码（标量，可为 null） |
| `expectedUpdateCadence` | String | 派生 | 来自 `DataflowJob.batchType`；多 Job 时取第一个有 cronExp 的 Job；无匹配 → null |
| `cronExpression` | String | 派生 | 来自 `DataflowJob.cronExp`；同上选取逻辑 |
| `dataSource` | String | 直接 | 数据源名称（文本） |
| `sourceDescription` | String | 派生 | 来自 `DataSource.dsDescr`；team-scoped join，订阅方通常为 null |

**响应示例（成功）：**

```json
{
  "success": true,
  "data": {
    "assetId": 46,
    "assetName": "stock_day",
    "assetType": "table",
    "assetCategory": "market-data",
    "description": "A-share daily OHLCV bars",
    "tags": "PUBLIC,equity,daily",
    "sensitivityLevel": "PUBLIC",
    "allowSubscription": true,
    "teamName": "tenant_lg_data",
    "createdDate": "2025-12-01T08:00:00",
    "createdBy": "admin",
    "recordCount": 5234567,
    "sizeBytes": 8923847234,
    "lastUpdated": "2026-06-17T15:42:18",
    "lastSchemaSyncAt": "2026-06-16T03:00:00Z",
    "jobCode": "stock_day_sync",
    "expectedUpdateCadence": "daily",
    "cronExpression": "0 0 18 * * ?",
    "dataSource": "lg_data_pro_pg",
    "sourceDescription": "Primary LG Postgres lakehouse (read-only mirror)"
  },
  "message": "OK"
}
```

**业务错误**（资产不存在 / 跨团队访问）：返回 HTTP 200，`{"success": false, "code": "ASSET_NOT_FOUND", "message": "<原因>"}` —— 符合平台 `{success, data, message}` 合约，不抛 HTTP 4xx。

---

##### `dataasset.data.get` — `filter_op` 支持的运算符集合

路径：`GET /api/data-assets/{id}/data`

Gateway 支持 snake_case 别名（`filter_column` / `filter_value` / `filter_op` / `order_by` / `order_direction`）和 camelCase 两种写法，两者等价。

**`filter_op` / `filterOp` 完整合法值：**

| 运算符 | SQL 语义 | 示例 |
|---|---|---|
| `eq` | `= 'val'` | `filterOp=eq&filterValue=600519` |
| `ne` | `<> 'val'` | `filterOp=ne&filterValue=600519` |
| `gt` | `> 'val'` | `filterOp=gt&filterValue=10.5` |
| `gte` | `>= 'val'` | `filterOp=gte&filterValue=10.5` |
| `lt` | `< 'val'` | `filterOp=lt&filterValue=10.5` |
| `lte` | `<= 'val'` | `filterOp=lte&filterValue=10.5` |
| `like` | `LIKE '%val%'`（平台自动加两侧 `%`，与 `contains` 等价） | `filterOp=like&filterValue=浦发` |
| `contains` | `LIKE '%val%'`（平台自动加两侧 `%`，与 `like` 等价） | `filterOp=contains&filterValue=浦发` |
| `in` | `IN ('a','b','c')` | `filterOp=in&filterValue=a,b,c` |
| `not_in` | `NOT IN ('a','b','c')` | `filterOp=not_in&filterValue=a,b,c` |

- **多值运算符**（`in` / `not_in`）：`filter_value` 用英文逗号分隔，如 `filter_value=600519,000001,601398` → 生成 `IN ('600519','000001','601398')`。
- `like` 和 `contains` 行为相同：平台都生成 `LIKE '%val%'` 子串匹配。如需自定义 LIKE 模式（前缀 / 后缀 / 通配符位置），目前需在调用方 SQL 端处理或走 `POST /api/data-assets/{id}/query`。
- **未知运算符拒绝**（不静默降为 eq）：传入不在上表中的值（如 `filterOp=between`）→ HTTP 200 `{"success": false, "message": "Validation Failed: Unsupported filter operator: between"}`。
- `order_direction`（snake_case；camelCase 写法为 `orderDirection`）接受 `asc` / `desc`（大小写不敏感），默认 `asc`。

### 看板 (Dashboard)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `dashboard.list` | GET | 列出看板 | 🟢 |
| `dashboard.get` | GET | 获取看板详情 | 🟢 |
| `dashboard.data.get` | GET | 一次拿看板所有组件的数据（支持 `maxRows`，默认 100，上限 500） | 🟢 |
| `dashboard.update` | PUT | **全量替换**看板（含 widgets/variables）。**想只改名称或描述？用 `dashboard.patch`，避免 widgetsJson 被覆盖。** | 🟡 |
| `dashboard.patch` | PATCH | 部分更新看板元数据（`PATCH /api/dashboards/{id}`）。**字段掩码语义**：仅 `name` / `description` 两个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`widgetsJson` / `variablesJson` / `widgets` / `teamName` / `dashboardId` / `allowSubscription` 出现在 body 即返回 HTTP 200 `success:false, code:"FIELD_NOT_PATCHABLE"`。**此 skill 需要 `dashboard.patch` scope（独立于 `dashboard.update`），现有 token 须重新签发方可使用。** | 🟢 |

### 订阅 & Marketplace

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `subscription.token.list` | GET | 列出订阅 token | 🟢 |
| `marketplace.item.list` | GET | 列出可订阅的看板/资产 | 🟢 |
| `marketplace.item.subscribe` | POST | 订阅市场条目 | 🟡 |
| `marketplace.item.unsubscribe` | POST | 取消订阅 | 🟡 |

### 指标告警 (Metric Alert)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `metric.alert.list` | GET | 按 `dashboardId` 列出告警规则 | 🟢 |
| `metric.alert.get` | GET | 按 `ruleCode` 获取规则 | 🟢 |
| `metric.alert.create` | POST | 创建告警规则 | 🟡 |
| `metric.alert.update` | PUT | **全量替换**告警规则。**想只改阈值/webhook/消息模板？用 `metric.alert.patch`。** | 🟡 |
| `metric.alert.toggle` | PUT | 启用/停用规则 | 🟡 |
| `metric.alert.test` | POST | 仅测试（无副作用） | 🟡 |
| `metric.alert.evaluate` | POST | 执行评估并按规则触发 webhook | 🟡 |
| `metric.alert.patch` | PATCH | 部分更新告警规则元数据（`PATCH /api/metric-alerts/{ruleCode}`）。**字段掩码语义**：`threshold`（阈值字符串）/ `webhookDsName`（webhook 数据源名）/ `messageTemplate`（消息模板）/ `templateEngine`（模板引擎，`'legacy'` 或 `'freemarker'`）四个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`enabled`（用 `metric.alert.toggle`）/ `ruleCode`（标识符）/ `metricKey`（更改后测量对象变化 — 破坏性）/ `teamName` 出现在 body 即返回 HTTP 200 `success:false, code:"FIELD_NOT_PATCHABLE"`。`templateEngine` 传入非 `legacy`/`freemarker` 值返回 HTTP 200 `success:false, code:"INVALID_TEMPLATE_ENGINE"`。**此 skill 需要 `metric.alert.patch` scope（独立于 `metric.alert.update`），现有 token 须重新签发方可使用。** | 🟢 |
| `metric.alert.snooze` | PUT | 暂停指定 alert rule 直到 `until` (ISO 8601 本地时间戳)；body: `{"until": "2026-06-22T18:00:00"}`. Snooze 优先级高于 silence + rate-limit；snooze 到期后自动恢复正常 evaluate()。`until` 缺失或非未来时间 → HTTP 200 `success:false code:INVALID_UNTIL`。 | 🟢 |
| `metric.alert.unsnooze` | PUT | 取消活跃的 snooze (`snoozed_until` → null)；与 snooze 是**独立 scope** — 设置 snooze 的 agent 不会自动获得清除权限。幂等，已无 snooze 时也返回 success。 | 🟢 |
| `metric.alert.acknowledge` | PUT | 标记 alert 已知 (`acknowledged_at = now()`)；v1 仅 info-only — 不影响下次 evaluate()（UI 显示"已知"状态）；v2 可能扩展为"clears next trigger window"。 | 🟢 |

#### `metric.alert.evaluate` — 数据新鲜度门控（freshness gate，2026-06-22 重写）

`freshnessConfig.sourceType = 'asset'` 模式下，freshness gate 不再执行 `SELECT MAX(field)` 实时查询，而是直接读取 `data_asset.last_data_refresh_at` 列——该列由 `registerAsset` executor step 在每次 ETL 成功执行后自动写入。行为变化：

- **`field` 字段已废弃但向下兼容**：现有配置中的 `field` 会被忽略（不校验、不查询），无需修改已有 `freshnessConfig`。
- **跨租户订阅规则**（`publisherTeam != null`）：subscriber 侧直接通过 `getAssetByIdInTeam` 读取 publisher 资产的 `last_data_refresh_at`，无需 publisher 数据源凭证；跨租户 freshness gate 现已生效（此前 `custom-sql` 跨租户路径仍受 MVP 限制，保持 fail-open）。
- **NULL 值 = fail-open**：资产首次注册后 executor 未重新部署前（或从未经过 `registerAsset` step），`last_data_refresh_at` 为 NULL → probe 返回 `Optional.empty()` → 评估照常进行，不触发 gate。
- **`sourceType = 'custom-sql'`**：行为不变（own-team 执行自定义 SQL；跨租户仍为 MVP 限制）。

**已知限制**：ETL job 执行成功但写入 0 行时，`RegisterAssetStep` 仍然会 bump `last_data_refresh_at`，导致 gate 不会跳过该次评估。若 webhook 频繁误触发，建议使用 `metric.alert.snooze` 或调高阈值；v2 会在 `rowsWritten > 0` 条件下才 bump（目前为规划中的 follow-up）。

#### `metric.alert.snooze` — evaluate() 跳过优先级（Triage #11）

evaluate() 内部跳过检查的优先级（**先匹配先返回**）：

1. **snoozedUntil** — `snoozed_until > now()` → SKIPPED "snoozed until \<timestamp\>"
2. **silenceMinutes** — `lastTriggeredAt + silenceMinutes > now()` → SKIPPED "in silence period"
3. **maxFiresPerDay** — `firesToday >= maxFiresPerDay` → SKIPPED "daily limit reached"
4. → 正常执行评估 + webhook

Snooze 到期后（`snoozed_until < now()`）自动恢复，无需再调 unsnooze。

#### `metric.alert.patch` — templateEngine 字段（Triage #10）

`templateEngine` 控制 `messageTemplate` 的渲染方式：

| 值 | 行为 | 适用场景 |
|---|---|---|
| `"legacy"`（默认） | `${varName}` 正则替换，与历史版本完全兼容 | 现有规则无需改动 |
| `"freemarker"` | [FreeMarker](https://freemarker.apache.org/) 模板引擎：支持条件指令（`<#if var??>...</#if>`）、`<#list>` 迭代、null 安全访问（`${var!}`）、rowFields 嵌套访问（`${rowFields.stock_num!}`） | 需要条件内容或丰富格式的飞书/微信消息 |

**freemarker 模式下可用变量：**

| 变量 | 类型 | 说明 |
|---|---|---|
| `${ruleName}` | String | 规则名称 |
| `${value}` | String | 当前触发值 |
| `${threshold}` | String | 阈值 |
| `${fieldName}` | String | 监控字段名 |
| `${assetName}` | String | 资产名称 |
| `${operator}` | String | 运算符（GT / LT / EQ 等） |
| `${tenantName}` | String | 告警规则所属团队 |
| `${publisherTeam}` | String | 订阅资产发布方团队（自有资产为 null） |
| `${timestamp}` | String | ISO-8601 UTC 触发时间（**freemarker 独有，legacy 不含**） |
| `${rowFields.col_name!}` | String | GROUP BY 分组字段值（如 `${rowFields.stock_num!}`，`!` 表示缺失时默认为空字符串） |
| `${col_name}` | String | rowFields 键同时提升为顶级变量，方便直接访问 |

**freemarker 模板示例（飞书 Markdown）：**

```
<#if value??>
**告警 ${ruleName}** 触发
- 字段：`${fieldName}`
- 当前值：${value}
- 阈值：${threshold}（${operator}）
<#if rowFields.stock_num??>- 股票：${rowFields.stock_num!}</#if>
<#if rowFields.region??>- 区域：${rowFields.region!}</#if>
触发时间：${timestamp}
</#if>
```

`<#if value??>...</#if>` 是 FreeMarker 空值检查指令：当 `value` 非 null 时渲染，等价于 `if value is not None:`。`${rowFields.stock_num!}` 中的 `!` 是默认值操作符 — 缺失时渲染为空字符串，避免 `undefined variable` 错误。`<#if rowFields.stock_num??>` 同理 — 仅当 GROUP BY 包含该列时渲染该行，避免多余的空行。

**向下兼容说明：** FreeMarker 的 `${var}` 语法与 legacy 正则语法完全相同 — 将 `templateEngine` 从 `"legacy"` 切换为 `"freemarker"` 后，现有的 `${ruleName}` / `${value}` 等模板无需任何改动即可继续工作。`"freemarker"` 模式额外支持 `<#if>` / `<#list>` 等高级指令。

**切换引擎示例：**

```json
PATCH /api/metric-alerts/{ruleCode}
{
  "templateEngine": "freemarker",
  "messageTemplate": "${ruleName}: ${fieldName}=${value} > ${threshold}"
}
```

成功响应：`{"success":true,"message":"Alert rule patched","ruleCode":"<ruleCode>"}`

### Webhook 插件

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `plugin.webhook.send` | POST | 通过数据源发送 webhook | 🟡 |

### 用户注册 & 反馈

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `auth.user.register` | POST | 注册新账号（`teamName` 自动生成为 `tenant_${username}`） | 🟢 |
| `auth.token.introspect` | GET | 查询当前 Bearer token 的身份、scope、状态与过期时间（无参数，仅限自身 token） | 🟢 |
| `feedback.submit` | POST | 提交反馈/Bug/需求 | 🟢 |
| `feedback.list` | GET | 查看历史反馈与官方回复 | 🟢 |

#### 身份 & Token 详情

##### `auth.token.introspect` — 查询当前 Bearer token 的身份 + scope + 生命周期

路径：`GET /api/public/agent/token-introspect`

调用此接口可在不触发任何业务 401/403 的前提下，查看当前 Bearer token 的身份、所属团队、token id、用户 id、有效 scope 列表，以及 token 名称 / 状态 / 过期时间。**自省范围限定为当前 token**——接口不接受 `tokenId` 参数，永远只描述请求 header 中提供的那一个 Bearer。

**输入**：无 query 参数。`Authorization: Bearer lgatk_...` header 是唯一身份来源。

**响应示例（200）：**
```json
{
  "success": true,
  "username": "alice",
  "teamName": "team-alpha",
  "userId": 7,
  "tokenId": 42,
  "tokenName": "alice-clawhub-readonly",
  "status": "active",
  "expiresAt": "2026-09-17T10:30:45Z",
  "scopes": [
    "dataasset.list",
    "dataasset.get",
    "dataasset.schema.get",
    "dataasset.data.get",
    "process.ingestion.list"
  ]
}
```

`expiresAt` 在 token 无过期时为字面量 `null`（key 始终存在）。

**响应示例（401，missing/invalid token）：**
```json
{
  "success": false,
  "message": "Invalid token"
}
```

**典型用法**：在调用任何 `/api/**` 业务接口前先 introspect 一次，把当前 token 的 `scopes` 与计划调用的 skill 所需 scope 做集合对比；缺失则在客户端给出友好提示，避免逐个 skill 403 试探。

---

## Backtest API

`stock_day` 日线回测请使用 `run_stock_day_backtest`（单股）或 `run_stock_day_portfolio_backtest`（多股组合），均在 `lg_utils.backtest_examples.stock_day` 模块。**基金 / 黄金 / 港股日线回测**也已 ship — `lg_utils.backtest_examples.{fund_day,metal_day,hk_day}.run_*_backtest`，shape 与 stock_day 一致（详见下方 Python 工具库表格）。完整参数说明见[场景 4 示例](#场景-4策略回测双均线跑茅台)。

结果可通过 `investment.stock.backtest.*` REST skill 检索：`list`（摘要）、`get`（全量 JSON）、`compare`（两次 metrics diff）。REST skill 当前以 `investment.stock.backtest.*` 命名但是 **asset-class-agnostic** — 通过 Python 调用 `lg_utils.backtest_examples.fund_day` / `metal_day` / `hk_day` 持久化的结果同样可由这 3 个 REST skill 检索（`persist(name=...)` 调用统一走 `process_backtest_result` 表，按 `name` 索引）。专用的 `investment.fund.backtest.*` / `investment.gold.backtest.*` REST skill 命名空间是 v2 follow-up（目前 stock-class skill 已能 cover 所有资产类的回测结果检索）。

### Wealth Studio（需开通 `investment_studio` 解决方案权限）

> **Phase 4 重命名说明**：skill id 前缀由 `stockstudio.*` 改为 `investment.stock.*`（同时新增 `investment.fund.*` / `investment.gold.*`）。旧 `stockstudio.*` id 通过 Express alias 表自动转发，新代码优先使用 `investment.stock.*`。

#### investment.stock.* — 股票持仓 / 交易 / 回测

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `investment.stock.portfolio.list` | GET | 查股票持仓（query 传 `asset_class=stock`）。每行附带 `recommendation` 字段：最新一条 per-stock 推荐；完整历史走 `/api/profile/portfolio-positions/recommendations?stock_num=...`。新增 `?accountType=real\|paper\|all` 参数，默认 `real`；显式传 `paper` 或 `all` 才会包含模拟交易数据 | 🟢 |
| `investment.stock.portfolio.create` | POST | 新增股票持仓条目（body 含 `asset_class: "stock"`） | 🟡 |
| `investment.stock.portfolio.update` | PUT | 更新股票持仓 | 🟡 |
| `investment.stock.trading.list` | GET | 查股票交易记录（query 传 `asset_class=stock`） | 🟢 |
| `investment.stock.trading.create` | POST | 录入新股票交易（自动更新持仓；body 含 `asset_class: "stock"`） | 🟡 |
| `investment.stock.backtest.list` | GET | 列当前团队的回测结果，支持 `?name=` / `?tag=` / `?programGroup=` 过滤。**Summary 视图**——返回 `totalReturn/sharpe/maxDrawdown/...` 数值列 + `tags` / `programGroup` 元数据，不含大 JSON | 🟢 |
| `investment.stock.backtest.get` | GET | 单条回测结果详情（按 id），包含 `paramsJson/metricsJson/tradesJson/equityCurveJson` 等全量 JSON 负载 | 🟢 |
| `investment.stock.backtest.compare` | GET | 两次回测结果 metrics 逐项 diff（`totalReturn/sharpe/maxDrawdown/...`） | 🟢 |
| `investment.stock.portfolio.nav_history.get` | GET | 组合 NAV 日历史 + 日度时间加权收益率（TWR） + 基准对比 α；详见下方[「理财组合 NAV 历史」](#理财组合-nav-历史) | 🟢 |
| `investment.stock.portfolio.nav_history.benchmarks.list` | GET | 返回平台支持的基准指数目录（4 条），附带每个指数最新可用日期与 `active/stale` 状态；可用于 UI 下拉选择器 | 🟢 |
| `investment.stock.portfolio.attribution.get` | GET | 组合 α/β v1 归因：一次调用返回 alpha（日度 + 年化）、beta、R²、波动率、跟踪误差、信息比率；详见下方[「理财组合归因」](#理财组合归因) | 🟢 |

---

##### `investment.stock.backtest.list` — 过滤参数 (#15)

路径：`GET /api/profile/backtest-results`

| 参数 | 必填 | 默认 | 说明 |
|---|:-:|---|---|
| `name` | 否 | — | 精确匹配 `name` 字段 |
| `tag` | 否 | — | 子串包含匹配：返回 `tags` 数组包含此 tag 的所有结果 |
| `programGroup` | 否 | — | 精确匹配 `program_group` 字段 |

多个过滤条件 AND 组合。无过滤参数时返回当前团队最近 50 条。

**响应示例（截取）：**
```json
{
  "success": true,
  "total": 2,
  "items": [
    {
      "id": 123,
      "name": "dual_ma_5_20",
      "totalReturn": 0.1842,
      "sharpe": 1.34,
      "tags": ["live-mock-2026Q3", "tutorial-walkthrough"],
      "programGroup": "dual-ma-series"
    },
    {
      "id": 122,
      "name": "dual_ma_5_30",
      "totalReturn": 0.1751,
      "sharpe": 1.21,
      "tags": [],
      "programGroup": "dual-ma-series"
    }
  ]
}
```

`tags` 是 JSON 数组（无 tag 时为 `[]`，不是 `null` 也不省略 key）。`programGroup` 是字符串（未设置时为 `null`，但 key 始终存在）。

**写入 tags / programGroup**：调用 `POST /api/internal/backtest-results` 时在 body 里加 `"tags": ["...","..."]` 和 `"programGroup": "..."` 字段。约束：tag 单条最长 64 字符；最多 20 条；空白 tag 自动剔除；programGroup 最长 128 字符。

---

#### 理财组合 NAV 历史

> skillId: `investment.stock.portfolio.nav_history.get`  
> 路径: `GET /api/profile/nav-history`  
> 权限: 需开通 `investment_studio` 解决方案权限（与持仓 / 交易系列相同）

**查询参数：**

| 参数 | 必填 | 默认 | 说明 |
|---|:-:|---|---|
| `start` | 否 | 组合最早快照日期 | 起始日期，格式 `YYYY-MM-DD` |
| `end` | 否 | 今天 | 结束日期，格式 `YYYY-MM-DD` |
| `asset_class` | 否 | `stock` | 持仓资产类别（`stock` / `fund` / `gold`） |
| `benchmark` | 否 | TeamVariable `benchmark_index` → 默认 `1B0300` | 基准指数代码（见下方指数目录）。优先级：请求参数 > 团队变量 > 默认 1B0300 |
| `accountType` | 否 | `real` | 账户类型筛选：`real`（仅真实账户，默认）/ `paper`（仅模拟账户）/ `all`（全部）。默认 `real`；显式传 `paper` 或 `all` 才会包含模拟交易数据。 |

**基准指数解析优先级：**

1. `?benchmark=<code>` 请求参数（最高优先级）
2. 团队变量 `benchmark_index`（团队管理员在 TeamVariable 里配置的默认基准）
3. 硬编码默认值：`1B0300`（沪深300）

**支持的基准指数（stock_day 内的 legacy 编码）：**

| 代码 | 名称 | 市场 |
|---|---|---|
| `1B0300` | 沪深300（默认）| SH |
| `1A0001` | 上证综指 | SH |
| `1B0510` | 中证A500 | SH |
| `399001` | 深证成指（数据停更于 2026-03-17，请求时会降级并返回 `meta.benchmarkWarning`）| SZ |

> 注意：这些是平台 `stock_day` 表里使用的 **legacy 编码**，与第三方常见的 `xxxxxx.SH` / `xxxxxx.SZ` 格式不同，不要混用。

**EOD 快照与 accountType（v1.0.30 修复）：**

每日 EOD 快照作业（`daily_pnl_snapshot`）写入 `daily_position_pnl` 时，从 `portfolio_positions.account_type` 读取 `accountType` 并原样写入快照行。v1.0.30 之前，快照行始终以实体默认值 `REAL` 写入，导致模拟账户头寸被误标记为 `REAL`，使真实账户 NAV 曲线出现虚高。v1.0.30 通过同步写路径修复了此问题，并通过 Flyway 迁移回填了历史数据。**如在 v1.0.30 发布前存入的快照行出现异常 NAV 尖峰，请在后端重启后检查 `daily_position_pnl` 中 `account_id LIKE 'paper-%'` 的行是否均为 `account_type = 'PAPER'`。**

**收益率计算方法（日度时间加权收益率 TWR）：**

平台以每日 `SUM(market_value)` 作为组合净值 V_t，从 `trading_records` 提取当日净流量 F_t = Σ(BUY 金额) − Σ(SELL 金额)，按 `r_t = (V_t − F_t) / V_{t−1} − 1` 计算日收益率，再链乘为累积收益率 R_t = Π(1 + r_i) − 1。通过减去当日净流入，"增仓 / 减仓"带来的资金变动不计入收益，只保留纯粹的价格涨跌信号。完整数学推导见设计文档 `docs/plans/2026-06-16-portfolio-nav-history-api-design.md` §3a。

**响应示例（含基准）：**

```json
{
  "success": true,
  "data": {
    "dates": ["2026-01-02", "2026-01-03", "2026-01-06"],
    "portfolio_nav": [100000.00, 102000.00, 101500.00],
    "portfolio_cumulative_return": [0.00000000, 0.02000000, 0.01500000],
    "benchmark_code": "1B0300",
    "benchmark_cumulative_return": [0.00000000, 0.01000000, 0.00800000],
    "alpha_spread": [0.00000000, 0.01000000, 0.00700000]
  },
  "message": "ok",
  "meta": {
    "filledDates": [],
    "benchmarkSource": "default",
    "benchmarkWarning": null,
    "benchmarkStaleAt": null
  }
}
```

`meta` 字段说明：

| 字段 | 说明 |
|---|---|
| `filledDates` | 因 `market_value=null`（当日无行情）而向前填充的日期列表；不影响收益率计算，仅作信息提示 |
| `benchmarkSource` | `"request"` / `"team_variable"` / `"default"` — 说明基准来源 |
| `benchmarkWarning` | 基准数据停更时的告警文案（如"Benchmark 399001 series stale; last available 2026-03-17"）；为 null 时省略 |
| `benchmarkStaleAt` | 基准最后有效日期（ISO）；基准截断时此字段告知截断位置，`alpha_spread` 此后各元素为 null |

**业务错误合约：**

- `?benchmark=BADCODE` → HTTP 200，`{"success": false, "message": "Unknown benchmark index: BADCODE (...)"}`（不抛 500，也不返 HTML）
- 基准数据停更（如 `399001`）→ 仍返回完整 NAV，`meta.benchmarkWarning` 描述停更，`alpha_spread` 截断到最后有效日；不失败整个调用
- 无持仓快照记录 → HTTP 200，`{"success": true, "data": {"dates": [], ...}, "message": "No snapshot history found for this portfolio"}`

---

#### 理财组合归因

> skillId: `investment.stock.portfolio.attribution.get`  
> 路径: `GET /api/profile/attribution`  
> 权限: 需开通 `investment_studio` 解决方案权限（与持仓 / 交易系列相同）

一次调用即可得到"我的策略跑赢市场了吗？"的核心数字：**年化 alpha**（超额收益）、**beta**（市场敏感度）、**R²**（拟合度）、波动率、跟踪误差和信息比率。底层数据来自已有 `nav_history.get` 的日度 TWR 累积收益序列，无额外 DB 查询。

**查询参数：**

| 参数 | 必填 | 默认 | 说明 |
|---|:-:|---|---|
| `start` | 否 | 组合最早快照日期 | 起始日期，格式 `YYYY-MM-DD` |
| `end` | 否 | 今天 | 结束日期，格式 `YYYY-MM-DD` |
| `asset_class` | 否 | `stock` | 持仓资产类别（`stock` / `fund` / `gold`） |
| `benchmark` | 否 | TeamVariable `benchmark_index` → 默认 `1B0300` | 基准指数代码，优先级与 `nav_history.get` 相同 |
| `accountType` | 否 | `real` | `real`（仅真实账户）/ `paper`（仅模拟）/ `all`（全部） |

**计算方法（α/β v1）：**

由 `nav_history.get` 返回的日度累积收益序列，经链式反推 `R_p[i] = (1+CR[i])/(1+CR[i-1]) - 1` 得到日度收益率序列，再以 OLS 回归计算：

| 指标 | 公式 |
|---|---|
| `beta` | `Cov(R_p, R_b) / Var(R_b)`（样本方差，N-1 分母） |
| `alpha` | `mean(R_p) - beta × mean(R_b)`（日度） |
| `alphaAnnualized` | `alpha × 252` |
| `rSquared` | `Cov(R_p, R_b)² / (Var(R_p) × Var(R_b))` |
| `portfolioVolatility` | `stddev(R_p) × √252`（年化） |
| `benchmarkVolatility` | `stddev(R_b) × √252`（年化） |
| `trackingError` | `stddev(R_p − R_b) × √252`（年化主动风险） |
| `informationRatio` | `(mean(R_p) − mean(R_b)) × 252 / trackingError` |

所有数值字段精度为 4 位小数（`BigDecimal` scale 4）。

**响应示例（含基准，合成数字）：**

```json
{
  "success": true,
  "data": {
    "start": "2026-01-01",
    "end": "2026-06-17",
    "tradingDays": 115,
    "benchmarkCode": "1B0300",
    "benchmarkSource": "team_variable",
    "portfolioCumulativeReturn": "-0.1319",
    "benchmarkCumulativeReturn": "0.0528",
    "alpha": "-0.1847",
    "alphaAnnualized": "-0.4123",
    "beta": "0.8742",
    "rSquared": "0.6418",
    "portfolioVolatility": "0.2156",
    "benchmarkVolatility": "0.1834",
    "trackingError": "0.0941",
    "informationRatio": "-1.9628"
  },
  "meta": {
    "benchmarkWarning": null,
    "benchmarkStaleAt": null,
    "sampleSize": 115,
    "minSampleWarning": null,
    "computationWarning": null
  },
  "message": "OK"
}
```

**22 个字段总览（D12 文档锁）：**

15 data 字段: `start`, `end`, `tradingDays`, `benchmarkCode`, `benchmarkSource`, `portfolioCumulativeReturn`, `benchmarkCumulativeReturn`, `alpha`, `alphaAnnualized`, `beta`, `rSquared`, `portfolioVolatility`, `benchmarkVolatility`, `trackingError`, `informationRatio`.

5 meta 字段: `benchmarkWarning`, `benchmarkStaleAt`, `sampleSize`, `minSampleWarning`, `computationWarning`.

2 envelope 字段: `success`, `message`.

`meta` 字段说明：

| 字段 | 说明 |
|---|---|
| `benchmarkWarning` | 基准缺失 / 对齐窗口过短时的告警文案；null 表示正常 |
| `benchmarkStaleAt` | 基准最后有效日期（ISO）；基准截断时告知截断位置 |
| `sampleSize` | 对齐后的原始序列天数（等于 `tradingDays`） |
| `minSampleWarning` | 对齐后日度收益点数 < 5 时的告警 (OLS 最小有效样本)（含实际点数）；null 表示正常；fires when aligned daily returns < 5 (OLS minimum) |
| `computationWarning` | 基准方差接近零（β 无法定义）时的告警；null 表示正常 |

**边界行为合约：**

- 对齐窗口 ≤ 1 天（基准数据只有首日）→ `beta/rSquared/trackingError/informationRatio` 全为 null，`meta.benchmarkWarning = "Benchmark series too short for α/β computation after alignment"`
- 日度收益点数 < 5（OLS 最小样本，`tradingDays` 太短）→ 同样置 null，`meta.minSampleWarning` 含实际点数
- 基准方差近零（常数基准）→ β 无意义，置 null，`meta.computationWarning = "Benchmark variance near zero; β undefined"`
- 无持仓数据 → 与 `nav_history.get` 行为一致，返回空序列 + `success:true`
- `?benchmark=BADCODE` → HTTP 200 `{"success": false, "message": "..."}`

---

#### investment.fund.* — 基金持仓 / 交易 (回测通过 `lg_utils.backtest_examples.fund_day` Python 入口，REST skill `investment.stock.backtest.*` 可检索结果)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `investment.fund.portfolio.list` | GET | 查基金持仓（query 传 `asset_class=fund`；`market` 取值 OF/ETF/LOF） | 🟢 |
| `investment.fund.portfolio.create` | POST | 新增基金持仓（body 含 `asset_class: "fund"`） | 🟡 |
| `investment.fund.portfolio.update` | PUT | 更新基金持仓 | 🟡 |
| `investment.fund.trading.list` | GET | 查基金交易记录（query 传 `asset_class=fund`） | 🟢 |
| `investment.fund.trading.create` | POST | 录入新基金交易（body 含 `asset_class: "fund"`） | 🟡 |

#### investment.gold.* — 黄金持仓 / 交易 (回测通过 `lg_utils.backtest_examples.metal_day` Python 入口，REST skill `investment.stock.backtest.*` 可检索结果)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `investment.gold.portfolio.list` | GET | 查黄金持仓（query 传 `asset_class=gold`；`market` 取值 SGE/BANK；`stock_num` 取值 Au99.99/Au100g/AuTD） | 🟢 |
| `investment.gold.portfolio.create` | POST | 新增黄金持仓（body 含 `asset_class: "gold"`） | 🟡 |
| `investment.gold.portfolio.update` | PUT | 更新黄金持仓 | 🟡 |
| `investment.gold.trading.list` | GET | 查黄金交易记录（query 传 `asset_class=gold`） | 🟢 |
| `investment.gold.trading.create` | POST | 录入新黄金交易（body 含 `asset_class: "gold"`） | 🟡 |

#### investment.paper.* — 模拟盘交易（Paper Trading，单户 ¥1,000,000 沙盘）

> ⚠️ **Paper-trading tokens are platform-issued, NOT self-mintable.** The `paper.*` scope namespace is reserved — calling `POST /api/subscription/tokens` with `scopes: "paper.account.read"` (etc.) returns HTTP 400 + `{"code":"RESERVED_SCOPE"}`. Paper-execution tokens are auto-minted by the platform when a strategy is bound to a paper account via the UI (`PaperExecutionTokenService.mintForExecution`). If you want to drive paper trading from an external agent, mint the token via the strategy-binding flow first, then call the endpoints below with that token.

> **新 v1.1**：单户模拟盘，行情打通 `stock_day` 实时价；MARKET 同步成交，LIMIT 走每 60s 撮合 + 15:00 自动 EXPIRED；T+1、一手 100 股、A 股标准手续费全部强制。**与真金账户完全隔离**——真金交易记录走 `investment.stock.trading.*`，二者数据库行级互不影响。

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `investment.paper.account.get` | GET | 查模拟账户当前状态：现金 / 初始资金 / 累计重置次数 / 总市值。首次调用 lazy-create | 🟢 |
| `investment.paper.orders.submit` | POST | 下单：`{stock_num, market, side: BUY/SELL, order_type: MARKET/LIMIT, qty, limit_price?, client_order_id}`。`client_order_id` 必传（同 user + 同 client_order_id 幂等）。MARKET 同步返回成交价；LIMIT 返回 SUBMITTED，撮合后由 scheduler 推到 FILLED/EXPIRED | 🟡 |
| `investment.paper.orders.list` | GET | 查订单（支持 `status=` / `from=` / `to=` 过滤）；返回字段含 `status / source / filledPrice / filledQty / fees / rejectReason` 等 | 🟢 |
| `investment.paper.positions.list` | GET | 查模拟持仓（只返 `account_id LIKE 'paper-%'` 的行，不会和真金混在一起） | 🟢 |

**Scope 集（process-execution 默认）**：`paper.orders.write paper.account.read dataasset.read`。这是后端在 process 起跑时自动注入的 scope-limited 短期 Bearer。

**Scope guard 边界**：带 paper scope 的 Bearer **只能**访问 `/api/wealth/paper/**`、`/api/data-assets/**`、`/api/auth/current`、`/api/public/agent/token-introspect`；其他 namespace（如 `/api/trading-records` 真金路径）一律 403 `scope_insufficient`。如需在自己的 PAT 上启用 paper 调用，去 个人设置 → Token 管理 创建一个带这套 scope 的长期 PAT。

**典型用法（在 Process Python 节点里跑量化策略）**：

```python
import lg

execution_id = lg.get_variable("execution_id")
quote_resp = lg.get_asset_data("stock_day",
    filter_column="stock_num", filter_value="600000",
    filter_operator="eq", size=1)
quote_rows = quote_resp["data"]
positions = {p["stockNum"] for p in lg.paper.get_positions()["items"]}

if quote_rows and quote_rows[0]["close_price"] < 9.50 and "600000" not in positions:
    # Preferred form: bare stock code + explicit market.
    # The dotted form ("600000.SH") is also accepted — the SDK and backend both
    # auto-strip it via PaperOrderService.normalizeStockNum (Bug #51-A).
    lg.paper.submit_order(
        symbol="600000", market="SH", side="BUY", qty=100, order_type="MARKET",
        client_order_id=f"{execution_id}-pufa-entry",  # 用 execution_id 做幂等键
    )
```

资源市场已上线 starter_paper_trade_strategy 模板，「免费接入」一键复制到你的 tenant 即可改写。

**回测模式（Ship 5-H，同一份脚本两种跑法）**：在 Process 执行环境上额外设置 `LG_PAPER_MODE=backtest` + `LG_PAPER_BACKTEST_FROM=YYYY-MM-DD` + `LG_PAPER_BACKTEST_TO=YYYY-MM-DD`，**同一脚本不改一行代码**即对历史 `stock_day` 回放。此模式下：

- **不发 HTTP** —— `submit_order` 等调用走 `lg_utils.paper_sim` 进程内模拟器；后端 `/api/wealth/paper/**` 不会收到任何请求；`paper_order` 表不会写入新行。`PaperScopeGuard` / `process_execution_secret` / `__LG_PAPER_TOKEN__` 全部不被消耗（token 若存在则 DEBUG 日志一行后忽略）。
- **规则完全一致** —— Java 后端 `FeeCalculator` / `PriceLimitValidator` / `PaperOrderService` (T+1 + 一手) 为规则正本；Python 模拟器有 fixture 平价测试 (`paper_sim_fixtures.yml` + `PaperSimRuleParityTest`) 守护，任何规则方法 PR 必须同步重新生成 fixture + 更新 Python，否则 CI 红。
- **不消费 scope** —— 因为根本不发出 HTTP，所以 `paper.orders.write` 等 scope 在 backtest 模式下完全用不到；agent / PAT / process-execution token 的 scope 集合不需要任何调整。
- **持久化** —— 脚本末尾**必须显式调** `lg.paper.persist_backtest(name=...)`（无 `atexit` 隐式持久化；防止脚本异常中断时写入「半拉子结果」造成数据污染）。结果写入 `process_backtest_result`，UI 走 `/profile/backtest-results`。
- **suspension 不查** —— `dacp_suspended_stocks` 是前向运维表，回测刻意不查；这是文档化的 KNOWN_DIVERGENCE，不是 bug。

资源市场已上线 `starter_paper_trade_strategy_backtest` 模板。设计文档：`docs/plans/2026-06-11-paper-trading-ship-5-h.md`（LA-APPROVED v3）。

**`lg.paper` 完整 API 速查表**（live + backtest 两种模式共用同一函数签名；运行时由 `LG_PAPER_MODE` env var 决定走 HTTP 还是走进程内模拟器）：

| 函数 | 模式 | 签名 | 返回 | 备注 |
|---|---|---|---|---|
| `lg.paper.submit_order(symbol, side, qty, order_type="MARKET", limit_price=None, client_order_id=None, market=None, asset_class=None)` | live + backtest | 见左 | `dict`。**两端共有**：`id`（**主键 — 不是 `orderId`**，两端一致）、`clientOrderId`、`stockNum`、`market`、`side`、`qty`、`orderType`、`limitPrice`、`assetClass`、`status`、`rejectReason`、`fees`、`filledQty`。**已成交价键名两端不一致**：backtest 用 `fillPrice`，live 用 `filledPrice`（pre-existing 命名分歧；agent 代码需做 `r.get("fillPrice") or r.get("filledPrice")` 兼容写法）。**时间戳键两端不同**：backtest 仅返回 `tradeDate`（推进到的模拟交易日）；live 额外返回 `submittedAt`/`filledAt`（PaperOrder 实体时间戳）但**不返回** `tradeDate`。**live 独有键**：`accountId`、`submittedAt`、`filledAt`、`source` — backtest 路径无此四键。 | `symbol` 推荐裸代码 + 显式 `market="SH"/"SZ"/"BJ"/"HK"`；带 `.SH/.SZ/.BJ/.HK` 后缀也接受（SDK 客户端 + 后端 `PaperOrderService.normalizeStockNum` 都会自动剥离 — Bug #51-A）。`client_order_id` 用作幂等键。`order_type="LIMIT"` 时 `limit_price` 必填。 |
| `lg.paper.get_account()` | live + backtest | `()` | `dict`。**回测**：`{"initialCapital", "cashBalance", "positionValue", "totalEquity", "unrealizedPnl"}`。**live**：`{"id", "accountId", "initialCapital", "cashBalance", "baseCurrency", "status", ...}` — 注意 live 路径**不返回** `positionValue` / `totalEquity` / `unrealizedPnl`（这些是模拟器进程内汇总，不是后端持久化字段）。 | 回测模式下来自模拟器持仓估值；live 模式查询后端 `/api/wealth/paper/account` → `PaperTradingController.toAccountMap()`。 |
| `lg.paper.get_positions()` | live + backtest | `()` | `dict`：`{"items": [...], "total": N}` | 每条 item 关键键名因模式**不完全统一**：**回测**返回 `{stockNum, qty, avgCost, lastBuyDate}`（精简）；**live** 返回 `{id, stockNum, market, stockName, assetClass, positionQty, avgCost, lastBuyDate, currency}`（包含 `positionQty` 而非 `qty`）。**`marketValue` / `unrealizedPnl` 两端都不返回** — 如需 market value / P&L 请自行用 `get_asset_data("stock_day", ...)` 的 `close_price` × `qty/positionQty` 算。两端通用 `stockNum`（camelCase）— **不是** `stock_num`。 |
| `lg.paper.get_orders(status=None)` | live + backtest | `(status=None)` | `dict`：`{"items": [...], "total": N}` | `status` 可选过滤值：`SUBMITTED` / `FILLED` / `CANCELLED` / `REJECTED` / `EXPIRED`（5 个；`EXPIRED` 覆盖 DAY-TIF 限价单未触发收盘自动失效）。**不支持** `PARTIALLY_FILLED`（此后端未实现 partial fill 语义）。 |
| `lg.paper.cancel_order(order_id)` | live + backtest | `(order_id)` | `dict`（更新后的订单对象） | 已成交订单 422 拒绝。 |
| `lg.paper.advance_day(day)` | backtest only | `(day: str "YYYY-MM-DD")` | `None` | 推进模拟时钟到指定交易日；触发挂单成交评估、价格限制检查、T+1 规则。live 模式调用此函数会抛 `RuntimeError`（函数级文案，例如 `"advance_day() is only available in backtest mode (LG_PAPER_MODE=backtest). In live mode, the current day is inferred from the market calendar."`）。 |
| `lg.paper.record_eod_equity()` | backtest only | `()` | `None` | 在当前模拟日的收盘后调用，记录该日的 equity curve 点（用于 Sharpe / MaxDD 等指标聚合）。 |
| `lg.paper.persist_backtest(name=None, force=False)` | backtest only | `(name=None, force=False)` | `dict`：`{"id": int, "name": str}` — 仅 2 个 key | **必须显式调用** — 没有 `atexit` 隐式持久化（防异常中断写入半拉子结果）。`name=None` 时使用 `LG_PAPER_BACKTEST_PERSIST_NAME` env 或自动生成时间戳名。`force=True` 允许覆盖同名 result。metrics 不在返回里 — 需要 metrics 摘要请查 `process_backtest_result` 表或 `/profile/backtest-results` UI。 |

**回测模式完整脚本示范**（同一脚本与 live 模式只差三个 env var）：

```python
import lg
from datetime import date, timedelta

execution_id = lg.get_variable("execution_id")

# 走历史 stock_day（回放）；不发任何 HTTP 给后端。
start = date(2026, 1, 1)
end   = date(2026, 1, 31)
day   = start
while day <= end:
    lg.paper.advance_day(day.isoformat())

    # 策略示例：每日抓 600000 的 stock_day 当日收盘价；< 9.50 且无持仓时买 100 股。
    # 注意：lg.get_asset_data 是单列过滤；如需 (stock_num, day_id) 联合过滤，
    # 在 SQL 化的策略里把 day_id 作为 filter_column、由 advance_day 控制时间游标。
    quote_resp = lg.get_asset_data("stock_day",
        filter_column="day_id", filter_value=int(day.strftime("%Y%m%d")),
        filter_operator="eq", size=500)
    quote_rows = [r for r in quote_resp["data"] if r.get("stock_num") == "600000"]
    positions = {p["stockNum"] for p in lg.paper.get_positions()["items"]}

    if quote_rows and quote_rows[0]["close_price"] < 9.50 and "600000" not in positions:
        lg.paper.submit_order(
            symbol="600000", market="SH", side="BUY", qty=100, order_type="MARKET",
            client_order_id=f"{execution_id}-day{day.isoformat()}",
        )

    lg.paper.record_eod_equity()    # 收盘记账
    day += timedelta(days=1)

# 显式持久化 — 没有这一行结果不会写 process_backtest_result
result = lg.paper.persist_backtest(name="600000_low_entry_jan2026")
print(f"backtest persisted: id={result['id']}, name={result['name']}")
```

**关键差异 vs live 模式**（同一份用户代码，**仅** env var 区别）：

- live 模式不需要 `advance_day` / `record_eod_equity` / `persist_backtest`（实时撮合 + 真实交易日时钟）— 这三个函数在 live 模式下会抛 `RuntimeError`（错误文案按函数定制，例如 `advance_day` 文案明确指出"live mode 由 market calendar 推进当前日"），便于 fail-fast 发现脚本误配。
- backtest 模式下 `submit_order` 不会写 `paper_order` 表（进程内模拟器 only）；live 模式下每次成功调用都对应后端一行 `paper_order` 记录。
- backtest 模式 fixture 平价测试（`paper_sim_fixtures.yml` + `PaperSimRuleParityTest` Python 端 + `PaperOrderServiceSymbolFormatTest` Java 端）守护规则一致性 — 任何 fee / price-limit / T+1 / 一手规则的 PR 必须同步重新生成 fixture，否则 CI 红。

> 技能源在 `app.js` 的 `SKILL_CATALOG`，运行时可通过 `GET /agent/skills` 查询**当前 token 实际可用**的列表（会过滤 scope）。

### Python 工具库 `lg_utils`（在平台 `python_script` 流程节点里 `import` 使用）

平台的 `python_script` 执行器会自动把 `lg_utils` 注入到用户脚本的 `PYTHONPATH`，无需安装。

| 模块 / 函数 | 功能 |
|---|---|
| `lg_utils.get_variable(key, default)` / `lg_utils.get_variables()` | 读取流程上下文变量（由前端/调度器传入；`get_variables()` 返回全集 dict） |
| **`lg_utils.put_variable(key, value)`** ✨ NEW | 把变量回写到当前 session 的 JobPool，下游 step 的 `${key}` 替换能解析到。`value` 必须 JSON-serializable，单个值 ≤ 64 KB。`key` 不能以 `_lg_` 开头（保留给系统）。同 step 内多次调用累积；用于把 Python 脚本计算出的字符串/数字/小型 dict 传给后续 step（webhook messageTemplate / SQL where 子句等） |
| `lg_utils.get_context()` | 当前团队快照：`assets / datasources / dashboards / processes` |
| `lg_utils.get_asset_data(asset_identifier, page, size, order_by, filter_column, filter_value, filter_operator=None)` | 分页拉团队有权限的资产数据；返回 `{success, data, totalElements, totalPages, ...}`。`filter_value` 支持 list/tuple → IN 查询；`filter_operator` 支持 `eq / ne / in / not_in / like / gt / gte / lt / lte / contains`，默认 `contains` |
| `lg_utils.get_portfolio_positions(stock_num=None, page=1, size=500)` | 当前团队持仓（每行附带最新的一条 per-stock 推荐 `recommendation`，由内部 API 按 update_time 取最近） |
| **`lg_utils.get_trading_records(account_id=None, market=None, stock_num=None, trade_type=None, page=1, size=50)`** ✨ NEW | 拉团队的交易记录（分页 dict，字段 Jackson camelCase 如 `tradeDate / stockNum / tradeType`） |
| `lg_utils.write_recommendations(items, process_id=None, execution_id=None)` | Python 脚本把 per-stock 推荐（`action/priority/add1/add2/reduce1/reduce2/noMoreAdd/market`）**追加** 到 `process_stock_recommendation`（历史保留，不 upsert）；前端持仓页"推荐"按时间倒序展示历史 |
| `lg_utils.get_connection(ds_name)` / `get_db_config(ds_name)` | 按团队数据源名取 JDBC 连接 |
| **`lg_utils.backtest(strategy, asset, ...)`** | **单资产回测引擎**：long-only、整数股；输出 Sharpe / Sortino / MaxDD / 胜率 / profit_factor / 交易明细 / equity_curve / 年度拆分；可选 `benchmark_asset=` 对比并输出 alpha/beta；可选 `persist=True` 持久化到 `process_backtest_result` 表 |
| **`lg_utils.backtest_portfolio(strategies, assets, ...)`** ✨ NEW | **组合回测**：多标的共享现金池；额外输出 `per_asset` 贡献度/回撤；同样支持 benchmark / persist |
| **`lg_utils.write_backtest_result(result, name=...)`** ✨ NEW | 把 `BacktestResult` 持久化到 `process_backtest_result` 表（append-only，按团队隔离）。`BacktestResult.persist(name=...)` 是同义糖 |
| `lg_utils.log` 子模块 (`from lg_utils.log import info, warn, error`) | 标准化日志 helper：`info` → stdout，`warn` / `error` → stderr，自动加 `[INFO]/[WARN]/[ERROR]` 前缀。注意是子模块，不在 `lg_utils.__all__` 里，必须按子模块路径 import |
| `lg_utils.backtest_examples.dual_ma.DualMA` | 内置双均线参考策略 |
| `lg_utils.backtest_examples.stock_day.run_stock_day_backtest` | 针对平台 `stock_day` 日线表（`OPEN_PRICE/CLOSE_PRICE/day_id/STOCK_NUM`）的单股快捷封装 |
| `lg_utils.backtest_examples.stock_day.run_stock_day_portfolio_backtest` ✨ NEW | 多只股票组合的快捷封装 |
| **`lg_utils.backtest_examples.fund_day.run_fund_day_backtest`** ✨ NEW | 基金日线回测快捷封装。`fund_day` 表的 `unit_nav` 同时映射到 open/close（基金无 OHLC，只有单日净值）；`fund_code` 作为 filter；`nav_date` (YYYY-MM-DD) 作为日期列。其余参数 (strategy / start / end / capital / benchmark_asset) 与 stock_day 同形。 |
| **`lg_utils.backtest_examples.metal_day.run_metal_day_backtest`** ✨ NEW | SGE 黄金/白银日线回测快捷封装。`metal_day.close_price` 同时映射到 open/close；`metal_code` 作为 filter。常用 metal_code: `Au99.99` (黄金 9999)、`Au100g` (黄金 100g)、`Ag(T+D)` (白银 T+D)。 |
| **`lg_utils.backtest_examples.hk_day.run_hk_day_backtest`** ✨ (v1.0.31 起 港股数据已合并入 `stock_day`) | 港股日线回测快捷封装。**底层就是 `stock_day` 表过滤 HK ticker**（v1.0.31 起 stock_day 统一覆盖 A 股 + 港股）。结构同 `stock_day` 模板。 |

## 环境要求

### 必需

- `LG_AGENT_BASE_URL` - 平台地址（默认 `https://privora.cn`）
- `LG_AGENT_TOKEN` - Bearer Token（公开版唯一认证方式；建议使用最小权限、专用 Token）

## Security Notes

- 公开版 skill 仅支持 Bearer Token 模式，不接受会话 Cookie / CSRF。
- 首次安装建议使用测试账号或低权限 Token 验证读取类能力。
- 当前公开版 skill 仅面向只读与常规非破坏性写操作；删除、终止、审批与其他管理类能力应通过单独的 admin 工具或人工流程处理。
- 写操作应只授予明确需要的 scopes。
- 不要在脚本里硬编码 Token 凭据。

## 注意事项

- 公开版 skill 不包含删除、终止、撤销、审批等高风险管理操作。
- 公开版 helper scripts 只支持 Token 调用，不支持 session/cookie 兼容模式。
- `idempotencyKey` 用于幂等控制，写操作请保持稳定。
- Token 从平台获取，不要硬编码在脚本中。

---

## 最近更新

### v1.0.30 (2026-06-23)

- 📑 Added explicit analysis-not-investment-advice disclaimer in the Token Recommendation section: outputs are analytical inputs for operator review, not regulated advice; live trading and irreversible decisions stay outside autonomous execution.
- 🔒 Streamlined the agent skill catalog: token-management write operations are documented as operator-only actions performed via the Privora token-management UI, consistent with the existing "operator-issued Bearer Token" guidance.

### v1.0.29 (2026-06-23)

- 🔒 Documentation cleanup based on ClawHub security audit feedback. Internal token-management surfaces are now exposed only through the operator UI rather than documented in the agent manifest; runtime behavior unchanged. (Note: this cleanup was queued for v1.0.28 but missed in the squash-merge; v1.0.29 ships the queued change.)

### v1.0.28 (2026-06-23)

- 📌 文案修正：实时 skill manifest 三个 public 端点的域名从 `lg-data.cc` 改为 `privora.cn`（与平台主域名一致）。旧域名仍 302 重定向到 privora.cn，已 in-flight 的调用不受影响，但建议把 `/skill-version` / `/skill-manifest` / `/capabilities` 的 baseURL 切到 `https://privora.cn`。
- 🔒 Token 推荐章节加强：显式强调 minimum-scope 原则 + "Do NOT have your agent create tokens on your behalf" 顶级规则（token mint 是 operator 动作，不是 agent 动作）。

### v1.0.26 (2026-06-23)

- 🔧 `schedule.job.online` / `schedule.job.offline` 响应清理：retired legacy `code` / `msg` alias 字段；统一使用 `{success, message, data}` 标准包络（PR #385 加的临时 alias 至此完成迁移）。
- ✅ Frontend `public/js/jobs.js` 切到 `result.success`。

### v1.0.27 (2026-06-23)

- 🔒 内部 token 校验加强：`POST /api/subscription/tokens` mint 路径增加额外服务端校验（最长有效期上限 + WARN 级别 audit log），由 operator 在 Token Management UI 上感知；不影响 agent-facing API 行为。

### v1.0.26 (2026-06-23)

- (internal) alertness freshness gate reads `data_asset.last_data_refresh_at` (no SQL probe). No user-facing behavior change.

### v1.0.25 (2026-06-23)

- 📝 Paper trading: clarified that `paper.*` tokens are platform-issued only.
- ✅ Skill discovery: `/api/public/agent/capabilities` now enumerates 7 paper-trading endpoints (previously omitted because yml didn't register them).

### v1.0.24 (2026-06-22)

- 🔄 **Live skill discovery**：新增三个 public 端点（`/api/public/agent/skill-version`、`/api/public/agent/skill-manifest`、`/api/public/agent/capabilities`），已安装的 agent 可直接从 privora.cn 获取最新 manifest 和 endpoint catalog，不再依赖 ClawHub 缓存。`/skill-version` 返回 `{version, updatedAt}` 轻量级探针，用于判断本地缓存是否过期。
- 📋 **Capabilities catalog**：`/capabilities` 返回从 `agent-scope-mapping.yml` 解析的完整 `{method, path, scope}` 映射表（含 PR #382 snooze/ack/unsnooze 新 scope），agent 可程序化发现所有 endpoint 而无需手动翻 SKILL.md。
- 📌 **Frontmatter `updatedAt` 字段**：从本版本起，每次 SKILL.md 发布都同步更新 frontmatter `updatedAt` 字段（ISO 日期字符串）。`/skill-version` 端点以此字段为权威版本时间，不受 Node 重部署 mtime 漂移影响。

### v1.0.23 (2026-06-22)

- 📊 **新数据资产**：`stock_forecast` (业绩预告) + `stock_express` (业绩快报) 接入，11 年历史已回填 (82,457 + 19,945 行)，每日 19:30 增量更新。
- 🧹 **覆盖声明收紧 (T-1 audit)**：原 headline `多资产统一数据：A 股 / 港股日线行情` 改为按状态分类：`stock_day` / `fund_day` / `metal_day` / `stock_forecast` / `stock_express` 标 🟢 生产可用；`stock_hk` / `stock_minutes` 标 🔴 建设中（预计 Q3 开放）；`stock_us` 标 ⚫ 未实现。新增「数据资产可用性」表 + 同步更新 frontmatter `title` / `description` / `keywords` 移除未交付的 `港股` 顶层标签。
- 🔬 **新 skill**：`dataasset.metadata.get` (Triage #14) — 单资产元数据查询，含 `lastUpdated` / `expectedUpdateCadence` / `cronExpression` / `sourceDescription`，可程序化判断数据新鲜度。
- 📈 **新 skill**：`investment.stock.portfolio.attribution.get` (Triage #9) — α/β 归因分析，复用 nav_history 时序，输出 alpha / beta / R² / 波动率 / tracking error / information ratio。配套前端 dashboard widget (#9 PR-B 已 ship)。
- 🎯 **新 skill**：`metric.alert.patch` 支持 `templateEngine` 字段 — 选 `freemarker` 后 webhook 模板可用 `<#if>` 条件分支 + `<#list>` 循环 + 内置 `?string` 格式化等。原 `${var}` 字面替换仍是默认 `templateEngine='legacy'`，向后兼容。
- 🧰 **执行器修复 (PR-D)**：`StepMeta.parseParam` 移除破坏性 `replaceAll("[\\t\\n]","")` strip — Python 多行脚本、pip 多行 requirements、SQL 多行子句存在 JSON 字符串里现在保留真实换行字符。修复 2026-05-26 / 2026-06-09 / 2026-06-15 三起相关事故。

### v1.0.21 (2026-06-12)

- 🔍 Display title expansion — adds 3 more 0-competitor empty-market terms to title: 量化分析 / 多资产 / 风险监控. Cumulative #1 唯一 long-tail wins after this release: 9 queries.

### v1.0.20 (2026-06-12)

- 🔍 Display title expansion — adds "模拟盘 + 实时告警" to surface the paper-trading and alert capabilities in clawhub search (both query terms were 0-competitor empty markets pre-v1.0.20).

### v1.0.19 (2026-06-12)

- 🔍 Display title experiment — pass `--name` on publish to test if the CLI flag can set a Chinese-keyword-rich display title (auto-generated slug-based titles miss Chinese query intent like "A股 / 量化回测" / "Python 策略").
- No content change vs v1.0.18.

### v1.0.22 (2026-06-12)

- 📝 Documentation language tightened — replaced absolute "agent-safe" framing with precise per-category descriptions (read, idempotent write, workflow state transition, outbound webhook). Operators should configure least-privilege tokens and apply their own confirmation gates for state-changing operations.

### v1.0.18 (2026-06-12)

- 📝 Documented operation surface refined — read, idempotent write (subscribe / portfolio entries / token rotation), workflow state transition (redo / hold / resume / reset-priority), and outbound webhook trigger. Operators should evaluate risk per category and scope tokens accordingly.

### v1.0.17 (2026-06-12)

- 📝 Scope & Operator Responsibility section added — token recommendation + per-category side-effect description.
- No new capabilities. No API surface change.

### v1.0.16 (2026-06-12)

- 🔍 文档元数据补全 — 加 `title:` + `keywords:` frontmatter 字段，提升 clawhub vector search 对中文量化 / 股票 / A股 / 港股 / 回测关键词的命中率。功能无变化（v1.0.15 已 ship 模拟交易 + 回测升级）。

### v1.0.15 (2026-06-12)

- 🧾 **模拟交易 (Paper Trading)** ✨ — MARKET / LIMIT 委托 + scheduler-driven 撮合 + 真实涨跌停 / 停牌信号；账户 UNIQUE on user_name，订单按 client_order_id 幂等。适合策略 12 月 paper trade 验证。
- 📊 **策略回测**升级 — 平台已积累 44+ 次持久化回测，可通过 `investment.stock.backtest.list` 检索历史审计记录；新增 `lg_utils.backtest_examples.stock_day.run_stock_day_portfolio_backtest` 多股组合回测。
- 📝 description + 文档清理 — 移除外链 + 简化加密叙事 + 强化产品能力描述，跟最新平台状态对齐。

### v1.0.14 (2026-06-10)

- 📝 Description 重排：把"字段级加密 GA"前置到前 100 字，Hermes / clawhub 列表视图能立刻看到核心差异化。功能本身无变化（v1.0.13 已 ship）。

### v1.0.13 (2026-06-05)

两件 headline 更新：

- 🔒 **字段级加密 GA** — 持仓量、成本价、交易价格等字段密文化存储，per-account 密钥隔离 (Ship 5, 2026-06-04)。
- 🎯 **1-click subscribe→alert deeplink** — `marketplace.item.subscribe` 对 `dashboard-*` item 现在返回 `clonedDashboardId`。Agent 用这个 ID 构造 `/dashboards?selectId=<id>&openAlerts=true`，把用户从订阅一步带到 alert 配置 modal。详见上方[场景 5](#场景-5一键-subscribealert-deeplink-new-v1013)。

> 📌 环境变更：平台主域名 `lg-data.cc → privora.cn`，`LG_AGENT_BASE_URL` 默认值已更新。旧域名仍重定向工作，无需立即修改你的环境变量。

### v1.0.12 (2026-05-24)

- 多资产数据 + Python 策略回测能力 + 监控告警 webhook plugin 模板（飞书 / 微信 / 任意 HTTP 端点）。
- 60+ REST skills 跨 Process / Schedule / Datasource / Dashboard / Marketplace / MetricAlert / Webhook plugins / Investment studio。

---

**量化回测 / 模拟交易 / 告警仅需此三项能力？**请见窄范围版：[privora-cn-quant](https://clawhub.ai/guangfuwu/privora-cn-quant)（无管理操作）。

---

## ⭐ 觉得这个 skill 有用？

如果它帮你的 AI Agent 少踩了几个坑、省了几天工程时间——欢迎去 ClawHub 给个 **star**，让更多散户找到它：

👉 **[clawhub.ai/guangfuwu/skills/privora-cn-quant](https://clawhub.ai/guangfuwu/skills/privora-cn-quant)** （右上角 ⭐）

每个 star 都让 ClawHub 算法把这个 skill 排到更多寻找量化数据后端的开发者面前。3 秒钟的事，对维护者帮助巨大。

也欢迎在 issue 区反馈用得不爽的地方 / 想要的新能力——我会逐条跟进。

---

## 附录 · 已安装 agent 的实时 manifest 探测

> 此段是给**已安装 agent** 的元数据接入指南，不是 first-time discovery 内容。新读者可跳过。

已安装的 agent 可以直接从 `privora.cn` 拉最新版本（不经 ClawHub 缓存）：

| 端点 | 用途 |
|---|---|
| `GET https://privora.cn/api/public/agent/skill-version` | 轻量级版本探测，返回 `{version, name, description, updatedAt}` |
| `GET https://privora.cn/api/public/agent/skill-manifest` | 拿 SKILL.md 全文 markdown |
| `GET https://privora.cn/api/public/agent/capabilities` | 结构化 endpoint catalog（scope ↔ HTTP path 映射） |

三个端点都是 public，no auth。建议每次会话开始时 hit `/skill-version` 一次，如果版本号高于本地缓存就重新拉 manifest。

**产品主页：** [https://privora.cn](https://privora.cn)