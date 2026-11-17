---
name: Privora · 数据驱动投资工作流平台 for AI Agents
title: 🔬 Privora · AI Agent 投资工作流平台（A股/港股/美股/黄金/基金/财报数据 + Python 回测 + 模拟交易 + 组合归因 + 云端告警 + 流程编排）
version: 1.0.57
updatedAt: 2026-09-18
keywords:
  - A股
  - 港股
  - 美股
  - 基金
  - 黄金
  - 财报数据
  - 业绩预告
  - 现金分红
  - 分钟K线
  - K线
  - 实时行情
  - 量化回测
  - 策略沙盒
  - Python回测
  - A股模拟盘
  - 模拟交易
  - 持仓监控
  - 组合归因
  - 净值曲线
  - AI Agent
  - MCP
  - MCP Server
  - Claude Code
  - Codex
  - Cursor
  - 数据后端
  - 股票
  - 告警
  - 数据新鲜度
description: Privora · AI Agent 投资工作流平台 — Bearer Token 即接入 /agent/skills/execute 通用 dispatcher，覆盖 A 股/港股/美股/黄金/基金/财报数据 + Python 回测（含 sandbox）+ 模拟交易 + 组合归因（α/β TWR）+ 云端告警 + 流程编排。Hermes / Claude / GPT / OpenClaw 全兼容。
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

# Privora · AI Agent 投资工作流平台（Bearer Token 即接入 · A股/港股/美股/黄金/基金 数据 + 回测 + 模拟交易 + 告警 + 流程编排）

**给你的 AI Agent 一个统一的投资研究工作流后端 —— 数据查询 + 策略回测 + 组合归因 + 云端告警 + 流程编排一个 Token 全覆盖。**

Hermes / Claude / GPT / OpenClaw 任何 Agent，通过一个 Bearer Token 即可访问：

- 📊 **多资产数据（按市场段分别发布，均 🟢 生产可用）**：**日线** A 股 5500+ 股票（`stock_day`，含沪深300 / 上证综指 / 中证A500 / 深证成指 4 主要指数）+ 港股（`stock_day_hk`，如 `00700.HK`）+ 美股（`stock_day_us`，如 `AAPL`）；**分钟 K 线** A 股（`stock_kline`）+ 港股（`stock_kline_hk`），1/5/15/30/60 分钟；**持仓**、**黄金**、**基金**、**财报事件**（业绩预告 / 快报）——一个 API 全覆盖，详见下方「数据资产可用性」表。场内基金（ETF/LOF）日线（`fund_quote_day`）+ 分钟 K 线（`fund_kline`）表已就绪（🟡 尚未开放跨团队订阅，见下方表格）。
- 🔔 **7×24 云端监控**：Serverless 策略托管，飞书 / 微信毫秒级预警，零服务器运维
- 🧪 **Python 策略回测**：用同一份平台数据跑回测，输出 Sharpe / 最大回撤 / 交易明细
- 🔒 **加密静态、认证边界返明文**：持仓数据在数据库中以 per-account 独立密钥密文存储（防 DB 层泄露 + 平台 admin 跨账户读取）；**持有你 Bearer Token 的 Agent 通过 API 认证后，平台按调用者身份解密并返回明文** —— 这不是 E2E 加密，Token 授权即数据访问权。
- 🎯 **1-click subscribe→alert**：Agent 帮用户从"订阅 dashboard"到"配置 alert 上线"降到 1 step (2026-06-05 新增)
- 🧾 **模拟交易 (Paper Trading)**：MARKET / LIMIT 委托类型 + 调度器驱动 + 真实涨跌停 / 停牌信号，账户 + 订单 DB-level 幂等。

> **让普通人也能拥有私募级别的工作流**——不需要私募的预算，就能像私募研究员一样在同一条流水线里跑数据 + 分析 + Agent + 告警。

🆕 **版本与变更历史**：当前版本号以文件头 frontmatter 的 `version:` 字段为准，正文不重复这个数字；每次发布的完整变更说明见仓库内 [`CHANGELOG.md`](./CHANGELOG.md)，随包分发的历史摘要见文末 [§最近更新](#最近更新)。

🎯 **最适合**：想把整个投研工作流（数据查询 + 回测 + 模拟交易 + 告警 + 流程编排）交给 AI Agent 自动化的散户 / 小工作室；把 Hermes / Claude / GPT / OpenClaw 当量化助手用的开发者。**注意**：Bearer Token 是"工作流授权凭证"，不只是"数据 API key" —— 授予前先按 [§Scope](#scope--operator-responsibility) 分类明白**要给 Agent 哪些能力**。

🌐 **产品主页**：[https://privora.cn](https://privora.cn) · 注册即拿 Token

![演示](./lg-data-demo.gif)

---

## 🌟 核心亮点

### 1. 🤖 兼容所有主流通用 AI Agent
打破生态壁垒，本技能不仅专供某一平台，而是**完美兼容 Hermes、OpenClaw、Claude Code、GitHub Copilot 等所有支持外挂工具/技能的通用大模型 Agent**。只需简单配置环境变量，您的通用 AI 助手瞬间化身专业量化分析师。

#### 🔌 用 MCP 客户端？有原生通道，两条并存

如果你的 Agent 是 **Codex CLI / Claude Code / Cursor / Windsurf / Cline**，除了本包的环境变量 + 脚本方式，还有一个**原生 MCP** 通道:一个 stdio MCP server，把同一个 dispatcher 直接暴露成 `tools/list` / `tools/call` 工具，你的 Agent 不必再学 shell 脚本的调用形状。

**两条通道并存，没有一条被弃用**，而且它们是同一个后端接口的两个门:

- **接口完全相同** —— 都是 `GET /agent/skills` + `POST /agent/skills/execute` 这两条路由。
- **环境变量完全相同** —— 都是 `LG_AGENT_BASE_URL` + `LG_AGENT_TOKEN`。**配好了本包，就等于配好了 MCP server**，不用重新申请或配置任何东西。
- **权限完全相同** —— scope、租户绑定、`403`、`remediation` 全由后端裁定并原样返回;MCP server 自己不计算也不缓存任何授权判断。**换通道不会让同一个 token 多拿到或少拿到任何能力。**
- **新能力两边同时出现** —— MCP 的工具面是覆盖整个 catalog 的固定 dispatcher，不是手工维护的镜像。

⚠️ 它目前**还没发布到 npm**（`npm view @privora/mcp-server` 返回 404），需要从仓库检出后用绝对路径接入。用法见仓库里的 `mcp-server/README.md`（安装、客户端配置块、12 个工具、每个工具的 `annotations` 披露信号——只读 / 破坏性——以及错误映射，以及两个值得在第一次调用前读的平台坑）。annotations 是**披露，不是安全边界**：宿主可以完全忽略它们，真正且唯一不可绕过的授权判定始终在服务端 scope 校验。

**该选哪条?** 如果你的客户端原生支持 MCP，用 MCP —— Agent 少一层要学的东西。其它情况（Hermes、OpenClaw、自己写的脚本、CI 里直接 curl）继续用本包，它不会走。

### 2. 🔒 加密静态 · 认证边界返明文（Encryption-at-rest, not E2E）

每个账户的持仓数据在数据库中以 per-account 独立密钥密文存储。**这是防"库泄露 / 平台 admin 跨账户读取"的加密，不是 E2E 加密**：

- **持有你 Bearer Token 的 Agent 通过 API 认证后，平台按调用者身份解密并返回明文** —— Token 是解密权的钥匙，保管好 Token 就是保管加密防线
- 每个账户的加密密钥独立，平台管理员账号无法跨账户读取持仓明细（DB 层保证）
- 订阅他人发布资产时，发布方看不到你的查询内容或账户信息（widget config 对订阅方 sanitize）
- **给不可信 Agent 的 Token = 给它明文数据**。按 [§Scope](#scope--operator-responsibility) 授予最小 scope，不要 bundle 无关能力

### 3. ⚡ Serverless 极速预警与零部署
策略云端托管运行，无需您购买第三方行情 API，无需自建服务器维护 Cron 任务，无 Token 消耗税。策略触发后，毫秒级推送到您的飞书机器人或微信 Webhook。

---

## 🛠️ 能做什么

| 核心功能 | 详细说明 |
| :--- | :--- |
| **资产盈亏巡航** | 一键查询持仓明细、当日盈亏、历史收益率，数据由 privora.cn 闭环处理。 |
| **云端自动盯盘** | 设置预警条件（突破均线、涨跌幅、换手率等），触发即通知，7x24小时云端值守。 |
| **多终端实时推送** | 策略触发毫秒级推送到飞书、微信 Webhook，不错过任何交易信号。 |
| **行情数据** | 日线按市场段分别发布，均 🟢 生产可用：A 股（`stock_day`，沪深京 5500+ 股票 + 4 指数）、港股（`stock_day_hk`，如 `00700.HK`）、美股（`stock_day_us`，如 `AAPL`）；分钟 K 线：A 股（`stock_kline`）+ 港股（`stock_kline_hk`），1/5/15/30/60 分钟；基金日 NAV（`fund_day`）；场内基金（ETF/LOF）日线（`fund_quote_day`）+ 分钟 K 线（`fund_kline`，🟡 已建库尚未开放订阅）；SGE 黄金日线（`metal_day`）；财报事件（`stock_forecast` 业绩预告 + `stock_express` 业绩快报，11 年历史已回填）。详见下方「数据资产可用性」表。 |
| **Python 策略回测** ✨ | 用平台日线数据跑单股 / 多股组合回测，输出 Sharpe / 最大回撤 / 交易明细 / equity curve；结果持久化到 `process_backtest_result`，可通过 `investment.stock.backtest.list` 检索历史审计记录（平台已积累 44+ 次持久化回测）。 |
| **模拟交易 (Paper Trading)** ✨ | MARKET / LIMIT 两种委托类型，调度器驱动，模拟完整委托 → 成交 → 盈亏核算链路；账户按 `user_name` 唯一（DB-level UNIQUE），订单按 `(user_name, client_order_id)` 幂等，Agent 重复调用不重建。适合策略 6 阶段验证的最终纸面交易关卡。 |
| **用户声音收集** | 支持 Agent 代客户提交 Bug 和需求，无缝对接后台反馈系统。 |

### 数据资产可用性（2026-07-17 platform check）

> **发布模型说明**：底层物理表按市场是合表存储的（同一张表可能物理上含多市场行），但**对外发布是按市场段分别发布为独立 DataAsset 的**。`stock_day` 段族现已全市场覆盖并各自独立上线：A 股段 = `stock_day`，港股段 = `stock_day_hk`，美股段 = `stock_day_us`；分钟 K 线段族同理：A 股段 = `stock_kline`，港股段 = `stock_kline_hk`。三段各自独立发布、独立 asset id，调用时请用下表的 assetName，不要假设同一 asset 覆盖多市场。

| DataAsset | 状态 | 覆盖 | 频率 | 备注 |
|---|---|---|---|---|
| `stock_day` | 🟢 **生产可用** | **A 股（沪深京）5500+** 股票日线 + 4 主要指数（沪深300 `1B0300` / 上证综指 `1A0001` / 中证A500 `1B0510` / 深证成指 `399001`） | 日 | id=1；`000001` 等 A 股 ticker 自动路由（`segmentValues` SH/SZ/BJ）；`399001` 自 2026-03-17 起停更，请求会返回 `meta.benchmarkWarning` |
| `stock_day_hk` | 🟢 **生产可用** | 港股日线（如 `00700.HK`） | 日 | id=204；数据新鲜（2026-07-16 校验通过） |
| `stock_day_us` | 🟢 **生产可用** | 美股日线（如 `AAPL`） | 日 | id=206；由 `stock_day_us_backfill_to_mc` 任务从 PG 同步至 MC |
| `stock_kline` | 🟢 **生产可用** | A 股 1/5/15/30/60 分钟 K 线（`interval_type` 区分周期） | 分钟 | id=202；日线 + 日内同步，由 `stock_kline_daily_sync` 等调度维护 |
| `stock_kline_hk` | 🟢 **生产可用** | 港股 1/5/15/30/60 分钟 K 线 | 分钟 | id=207；与 `stock_kline` 同结构，段独立 |
| `stock_minutes` | ⚪ **已弃用** | (旧) 分钟 K 线，已被 `stock_kline` / `stock_kline_hk` 取代 | — | id=154；仅历史兼容保留，新集成请改用 `stock_kline`/`stock_kline_hk` |
| `fund_day` | 🟢 **生产可用** | 公募基金日 NAV | 日 (T+1) | 数据延迟约 1 个工作日；**长期回测/算收益率必须用 `adj_nav`（复权净值），不能用 `unit_nav`（会被拆分/分红污染，且约 49% 行 `adj_nav` 为 NULL）**——详见下方「`adj_nav` 缺失信号」一节 |
| `fund_quote_day` | 🟡 **数据已就绪，尚未开放跨团队订阅** | 场内基金（ETF/LOF）价格日线；PG 单表不分区；`market` ∈ {ETF, LOF}——**与 `fund_day`/`fund_codes` 的 `{E,O}` 词表不同，跨表 join 只能用 `fund_code`**；`turnover` 是成交额（元），不是换手率 | 日 | `source` 分 `akshare_hist_em`（官方历史，`is_final=true`/`calibration_status='confirmed'`）与 `fund_realtime_t0`（当日 T+0 推导，`is_final=false`/`pending`）；两者交叉验证收盘价/成交量完全一致；详见下方「场内基金 K 线」一节 |
| `fund_kline` | 🟡 **数据已就绪，尚未开放跨团队订阅** | 场内基金（ETF/LOF）分钟 K 线，`interval_type` ∈ {1m,5m,15m,30m,60m}（无 1d，日线见 `fund_quote_day`） | 分钟 | PG 原生 RANGE 分区表（按 `day_id`），**保留期仅 3 天**（非 MC 资产，不受 ODPS 分区自动注入影响）；`bar_time` 是 VARCHAR 不是 timestamp；`tick_count` 量化稀疏度；详见下方「场内基金 K 线」一节 |
| `metal_day` | 🟢 **生产可用** | SGE 黄金 / 白银日线 | 日 | 上海黄金交易所 |
| `stock_forecast` | 🟢 **生产可用** (NEW 2026-06-22) | A 股上市公司业绩预告；11 年历史 82,457 行已回填 | 日 | 财报季 (1/4/7/10 月底前后) 集中发布 |
| `stock_express` | 🟢 **生产可用** (NEW 2026-06-22) | A 股上市公司业绩快报；11 年历史 19,945 行已回填 | 日 | 比业绩预告更精确但发布更稀疏 |
| `stock_dividend` | 🟢 **生产可用** (NEW v1.0.32) | A 股上市公司现金分红事件；进入 `portfolio.attribution` 归因 | 事件驱动 | 除权除息日发布 |

**对 Agent 的指导**：调用 `dataasset.list` 看完整列表；标 🔴 / ⚫ / ⚪ 的资产请避免在策略里硬编码依赖（⚪ = 已弃用，改用其后继 asset）。`dataasset.metadata.get` (2026-06-22 新上) 可查每张表的 `lastUpdated` / `expectedUpdateCadence` / `cronExpression` 来判断当前状态——**2026-09 起这个 scope 已在默认 `read-data` 预设里**，用默认预设建的 token 直接调即可，无需额外勾选。

> 📌 本节是 **2026-07-17 的一次平台盘点快照**，随时间推移可能与实际覆盖漂移。各已发布资产的完整覆盖范围、分市场明细、更新频率与数据起始日期，见持续维护的公开清单页：[privora.cn/features/realtime-minute-data-coverage](https://privora.cn/features/realtime-minute-data-coverage)（按六类分组，含 A股/港股/美股/北交所分市场明细）。

---

## 🛡️ Scope 与操作者责任

本 skill 是通过 Bearer Token 对接 Privora 平台的能力。操作类别的副作用不同，**操作者负责按类别 scope token 并为需要的类别加入确认门槛**：

- **只读**（Read-only）—— 数据 API、回测结果查询、流程/调度/数据源/仪表盘/市场的 list/get。**平台状态零副作用**。
- **幂等写**（Idempotent write）—— 模拟交易下单（DB 层 UNIQUE on `user_name` + `client_order_id`，同 key 重试返回同一记录）、marketplace subscribe（ON CONFLICT 返回已有订阅）、告警配置更新。**同输入多次调用只产生一次逻辑效果，可安全重试**。
- **流程状态转移**（Workflow state transition）—— `process.ingestion.execute` 触发已授权 python_script 运行并写入 `process_backtest_result` 表；scheduler-instance 的 `redo / hold / resume / reset-priority` 转移 trigger row 状态。**每次调用创建或修改持久化记录**。
- **确认门槛类**（Confirm-gated destructive/high-risk）—— 一小撮删除 / 撤销 / reset / 调度作业上下线操作 Bearer token **可达**，但单次调用永远不会直接执行——必须先完成两步确认握手，完整列表见下方 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake)。
- **外发 webhook**（Outbound webhook）—— `schedule.job.plugin.webhook.trigger` 与告警评估路径向操作者配置的外部端点（飞书 / 微信 / 通用 webhook）发送通知。**副作用在 Privora 之外，平台不可撤销**。

**本 skill 部分暴露**（其余需人在 platform UI 手动完成）：
- 持久化记录的删除 / 撤销 / reset 操作 —— **一小撮**（流程删除、告警规则删除、team Python 模块删除、订阅 token 撤销、模拟盘账户 reset 等）经两步确认握手后可达，见上方「确认门槛类」；**多数**删除操作（如投资组合 / 交易记录删除）仍不在本 skill 范围内。
- 调度器 online / offline 状态转移 —— `schedule.job.online` / `schedule.job.offline` **可达**，同样需要两步确认握手，见上方「确认门槛类」——这两个操作不是"不暴露"。
- Webhook 插件生命周期变更（删除 / 禁用）—— `schedule.job.plugins.save`（详见下方作业插件小节，[§调度作业字段契约](#调度作业字段契约)）可全量替换一个作业绑定的插件列表（旧绑定先整体删除再写入新列表），**且不经确认握手**——传入的数组即视为该作业插件的完整期望状态，遗漏的既有绑定会被静默清空，不是增量操作。调用前请先 `schedule.job.plugins.list` 确认当前绑定，再拼出完整数组。
- 管理员级账户操作 —— 不暴露，需通过 platform UI 完成。

本 skill **不预先声明**任何操作是"agent-safe"——这个分类取决于操作者的风险偏好、agent 的可靠性、以及具体用例。**推荐姿势**：只读 + 幂等写允许 agent 自主调用；流程状态转移和外发 webhook 建议先经过用户确认门槛（约定俗成，非平台强制）；标记 `confirmRequired:true` 的高风险操作则由**平台强制**要求两步确认握手，不依赖操作者自律——**但这道门防的是单次误触，不是他人审批**：两步可以由同一个 agent 完成（`approval_mode='self-confirm'`，`approver_user` 就是 requester 本人，见下方 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake)）；要真正的人工把关，只有两条路：不授予这些 scope，或走平台 UI 由管理员 approve/reject。另外请注意上面「Webhook 插件生命周期变更」是**例外**：风险不低（全量替换、旧绑定先删），却不在 `confirmRequired` 名单内，调用前务必自行核实完整期望状态。

### 📋 场景 → scope 速查表

**新建 token 的默认 scope 就能取数**（2026-08-03 起）。点"创建"不改任何选项，你会得到
`read-data` 这一组：

```
dataasset.list  dataasset.get  dataasset.schema.get  dataasset.metadata.get
dataasset.data.get  dataasset.data.getRealtime  marketplace.item.list
```

需要别的能力时，按场景挑一组（token 创建页有同名的场景按钮，点一下即可全选）：

| 场景 | preset id | scopes |
|---|---|---|
| 取行情 / 资产数据（**默认**） | `read-data` | `dataasset.list` `dataasset.get` `dataasset.schema.get` `dataasset.metadata.get` `dataasset.data.get` `dataasset.data.getRealtime` `marketplace.item.list` |
| 读取数据 + 管理市场订阅（**含写权限**：订阅市场条目拿自己团队的 `clonedAssetId` 等；取消订阅会**删除**该团队克隆副本） | `subscribe-and-read` | `read-data` 全部 + `marketplace.item.subscribe` `marketplace.item.unsubscribe` |
| 读仪表板 | `read-dashboard` | `read-data` 全部 + `dashboard.list` `dashboard.get` `dashboard.data.get` |
| 触发并追踪流程 | `run-process` | `process.ingestion.list` `process.ingestion.get` `process.component.list` `process.ingestion.execute` `process.ingestion.execute.log.get` |
| 配置指标告警（不含建通知通道） | `manage-alerts` | `metric.alert.list` `metric.alert.get` `metric.alert.create` `metric.alert.update` `metric.alert.toggle` `metric.alert.test` |
| 实时告警（通道 + 规则，端到端） | `realtime-alerting` | `dataasset.{list,get,schema.get,metadata.get,data.get}` `datasource.list` `alert.channel.create` `plugin.webhook.send` `metric.alert.{list,get,create,update,patch,toggle,test,snooze,unsnooze,acknowledge}` |
| 读写持仓与交易（**含写权限**） | `portfolio` | `investment.stock.portfolio.{list,create,update}` `investment.stock.trading.{list,create}` `investment.stock.watchlist.list` `investment.stock.signal.{list,get}` `investment.fund.portfolio.{list,create}` `investment.fund.trading.{list,create}` `investment.gold.portfolio.{list,create}` `investment.gold.trading.{list,create}` |

**三个查询入口**（三处读的是同一份定义，不会互相打架）：

| 你是谁 | 去哪查 |
|---|---|
| 人 | [privora.cn/profile/tokens](https://privora.cn/profile/tokens) 创建 token 时的场景按钮 |
| Agent | `GET /agent/scope-presets` —— 返回 `{presets[], defaultScopes[], grantedScopes[]}`，每个 preset 带 `scopes[]`、`skillIds[]` 和 `satisfied`（当前 token 是否已满足） |
| Agent | `GET /agent/skills` —— **全量**技能目录。每条带 `granted`（你现在能不能跑）、`scope`（需要哪个 scope）、`params` schema、`exampleInvocation`。跑不了的条目额外带 `presetsGrantingScope` |

> `GET /agent/skills` 过去只返回你**已有** scope 的技能，所以 scope 不足时你根本看不到目标技能存在，
> 只能靠猜 skillId。现在默认返回全量并用 `granted` 标注；要恢复旧行为传 `?granted=true`。

**scope 不足时不用猜**：403 响应体直接给出 `requiredScope`、你当前的 `grantedScopes`、
哪个 preset 含它（`presetsGrantingScope`）以及去哪改（`remediationUrl`）。
skillId 写错时 400 响应体给 `didYouMean[]` 候选。

**Token 使用建议**：

1. 在 [privora.cn/profile/tokens](https://privora.cn/profile/tokens) 创建专用 Bearer Token
2. **最小 scope 原则** —— 只授予当前 use case 需要的 scope。只读分析用默认的 `read-data` 就够；
   要跑流程再加 `run-process`；agent 真的要下模拟单才加 `paper.*`（该命名空间由平台内部签发，
   见下方"模拟交易"章节）。**不要为"以防万一"打包无关 scope**。
3. 明确设置 `LG_AGENT_BASE_URL=https://privora.cn`
4. **Token 泄露立即 rotate** —— Token Management 页面列出所有活跃 token 及最后使用时间戳和 revoke 按钮

> 🛑 **绝对不要让你的 agent 代替你 mint token**。Token 创建是 operator 动作，不是 agent 动作。Agent 应该消费 operator 签发的 Bearer Token，**不应该**自己调 `POST /api/subscription/tokens`。

### 📑 输出仅供分析参考，不构成投资建议

本 skill 的输出（行情数据 / 组合分析 / 回测报告 / 模拟交易 / 告警评估）是**供操作者审查的分析结果**，不是投资建议、不是交易指令、也不能替代持牌财务咨询。

- **把结果作为你自己决策过程的输入** —— 使用前请自行验证数据新鲜度、假设、边界情况
- **实盘交易和不可逆的财务决策不应放在 agent 自动执行链路里** —— 模拟交易只是模拟；真钱交易必须走由操作者控制的券商链路并显式确认
- **回测反映的是历史条件** —— 过去表现不预测未来结果。使用前请确认数据窗口、策略逻辑、以及生存偏差 / look-ahead 假设
- **无监管咨询声明** —— 本平台是数据基础设施；下游任何投资决策由操作者本人（你）负责

---

## 🚀 快速接入 (Quick Start)

### 0) ⚡ 30 秒试一下（不需要注册 / 不需要 Token）

装完 skill 想立刻看看能干什么？**打开** [privora.cn/marketplace](https://privora.cn/marketplace)：

- 无需登录，直接浏览公开挂牌的 A 股 / 港股 / 美股 / 黄金 / 基金 / 财报事件等数据资产
- 想一眼看完**全部已发布资产**的覆盖范围 / 更新频率 / 数据起始日期，不用一个个点开？看公开清单页 [privora.cn/features/realtime-minute-data-coverage](https://privora.cn/features/realtime-minute-data-coverage)
- 每个资产可以点进去看 25 行样本数据 + 20 字段元信息（`lastUpdated` / 数据源 / cron 表达式等）
- 看到有价值的资产？**不要记这里显示的 numeric id**：那是发布方团队的 id，拿去调你自己的 Bearer Token 接口只会 404——订阅后你自己团队会拿到一份**全新数字 id** 的克隆资产，两者不是同一个数。**拿自己团队 id 最直接的办法**：走 §1 - §3 注册拿 Token——**`marketplace.item.subscribe` 不在默认 `read-data` 预设里**，预设场景按钮里只有 `subscribe-and-read` 带它，创建 token 时请选 `subscribe-and-read` 预设（或手动勾选 `marketplace.item.subscribe` / `marketplace.item.unsubscribe` 这两个 scope），用默认 `read-data` 预设建的 token 调这一步会 403——然后调 `marketplace.item.subscribe`（幂等——哪怕你之前已经订阅过，重复调用同一个 item 也照样成功），响应体里的 `clonedAssetId` 就是你自己团队里那份克隆资产的数字 id，直接拿去跑 §4 First Call Recipe（2 步 / 约 1 分钟）验证 Bearer Token 对同一资产能跑通。**兜底路径**：如果响应丢了这个字段、或你不想再调一次 subscribe，`dataasset.list` 里按 `tags` 含 `Subscribed` 也能扫到同一份克隆资产的 id
- 觉得样本还不够？往下走 §1 - §4 注册生成 Bearer Token 拿完整访问权（分页 / 过滤 / 更高 rate limit / 写操作 / Agent 集成）

**为什么先看再注册**：Privora 是投研工作流平台，"你的数据是否值得订阅"应该 30 秒能判断 —— 不需要注册墙。marketplace UI 是**发现工具**，Bearer Token 是**同一批数据的程序化访问入口**，两者对应关系明确。

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
公开版主要走以上 Bearer Token 方式；如果 Agent 只是浏览 marketplace / 预览已发布看板 & 资产，也可以走**匿名模式**（不需要 token，见下方 [§🌐 匿名预览](#anonymous-preview)）。session cookie / CSRF 兼容调用不支持。

### 3) 唤醒 Agent，开始对话
现在，您可以直接用自然语言向您的 Agent 下达指令了！

### 4) ⚠️ 做出你的第一次成功 API 调用（2 步走 + 1 步可选 / 避免最常见的 500 和 403）

**最容易踩的坑**：URL 里的 `{id}` 必须是**数字型 asset ID**（如 `42`），**不是 asset 名字**（如 `fund_day` / `stock_day`）。传成名字后端 Spring 转 Long 失败会返回 500——错误信息不会明确告诉你原因。

**正确的 recipe**（用默认 `read-data` 预设的 token 即可全部跑通）：

```bash
# Step 1: 先 list 拿数字 id ← 别跳过这步
curl -H "Authorization: Bearer $LG_AGENT_TOKEN" \
  https://privora.cn/api/data-assets | jq '.data[] | {id, assetName}'
# 输出示例：
# {"id": 42, "assetName": "fund_day"}
# {"id": 8,  "assetName": "stock_day"}
# {"id": 15, "assetName": "stock_dividend"}

# Step 2: 用数字 id (不是 assetName!) 查实际数据
curl -H "Authorization: Bearer $LG_AGENT_TOKEN" \
  "https://privora.cn/api/data-assets/42/data?page=1&size=10"
```

**Step 1 返回 `[]`？** 这对刚注册、没有自有资产、也没有订阅任何 marketplace 条目的团队是预期结果，不是 bug——你的团队此时确实没有任何 `dataasset.list` 能看到的资产。见上方 [§0](#0-⚡-30-秒试一下不需要注册-不需要-token) 的 subscribe → `clonedAssetId` 路径：调 `marketplace.item.subscribe` 需要持有该 scope 的 token（预设场景按钮里只有 `subscribe-and-read` 带它，默认 `read-data` 预设没有），拿到 `clonedAssetId` 后回来重跑本节 Step 1，这时就能在列表里看到刚订阅的克隆资产了。

**（可选）Step 3：查富元数据**——`GET /api/data-assets/{id}/metadata`（对应 skill `dataasset.metadata.get`）**2026-09 起已在** Token Management 页面 `read-data` 默认预设里，用默认预设建的 token 直接调即可：

```bash
curl -H "Authorization: Bearer $LG_AGENT_TOKEN" \
  https://privora.cn/api/data-assets/42/metadata
```

**Agent 侧用 `lg_agent_exec.sh` 调用同理**（v1.0.45 起支持命名参数扁平写法，不用手拼 JSON）：

```bash
scripts/lg_agent_exec.sh dataasset.list
scripts/lg_agent_exec.sh dataasset.data.get id=42 filter_column=stock_num filter_value=600519
# scripts/lg_agent_exec.sh dataasset.metadata.get id=42  ← 可选；2026-09 起已在默认 read-data 预设里，直接跑即可
```

`id` **必须是数字**（先 `dataasset.list` 拿到再传，不是资产名字如 `fund_day`）。想看某个 skill 接受哪些 key，先 `scripts/lg_agent_list.sh describe dataasset.data.get` 看 schema + 示例，再照着填。

**如果你已经踩到 500**：不用改代码逻辑，只需把 `{name}` 换成对应的数字 id 即可。数据资产的可用列表见下方「[数据资产可用性](#数据资产可用性2026-06-22-audit--triage-t-1)」表 —— 那里的名字对应 `dataasset.list` 返回的 `assetName` 字段，需要先 list 拿到本 team 里对应的数字 id。

---

<a name="anonymous-preview"></a>
## 🌐 匿名预览（无 token）

如果 Agent 只是想**浏览 marketplace 或预览已发布的看板/数据资产/流程**——比如帮用户看看 Privora 有什么数据源、有哪些现成看板可订阅、某个流程做什么用——**不需要 Bearer Token 也能直接跑**。这条通路和 [privora.cn/marketplace](https://privora.cn/marketplace) 页面上未登录访客看到的内容是**同一套数据**，只是把它变成 machine-readable 的 skill 调用。

### 什么时候用

- 用户还没注册，Agent 想先展示"这平台上有啥"
- 用户已注册但当前 session 没配 token，你想让 Agent 先给个 marketplace 摘要
- Agent 在做 discovery / recommendation，不需要写权限、也不涉及用户私有数据

### 怎么用

**留空 `LG_AGENT_TOKEN` 或直接不传 `Authorization` header** 即可：

```bash
# 无 token 调用 —— 直接返回 mode:"anonymous" + 10 个可用 skill
curl https://privora.cn/agent/skills

# 无 token 拿 marketplace 列表
# Windows Git Bash 提醒：curl.exe 是原生 Windows 程序，MSYS2 会按本地 ANSI 代码页重编码命令行参数，
# 如果把下面的 body 换成含中文/非 ASCII 的内容（如搜索关键字），-d '...' 会被静默改坏——改用 --data-binary @file。
printf '%s' '{"skillId":"marketplace.item.list"}' > /tmp/lg_body.json
curl -X POST https://privora.cn/agent/skills/execute \
  -H "Content-Type: application/json" \
  --data-binary @/tmp/lg_body.json

# 无 token 拿某个已发布看板的 widget 数据（同上：非 ASCII 内容一律 --data-binary @file，不要用 -d）
printf '%s' '{"skillId":"dashboard.data.get","params":{"pathParams":{"id":"<published-dashboard-uuid>"}}}' > /tmp/lg_body.json
curl -X POST https://privora.cn/agent/skills/execute \
  -H "Content-Type: application/json" \
  --data-binary @/tmp/lg_body.json
```

响应体的 `mode` 字段会明确标 `"anonymous"`，`grantedScopes` 列出下方 10 个允许的 skill。

### 匿名模式可用的 skill（全部只读）

| skillId | 用途 |
|---|---|
| `marketplace.item.list` | 列出所有可订阅的 marketplace 条目（看板 / 资产 / 流程）—— **discovery 入口** |
| `dashboard.get` | 按 id 拿某个已发布看板的元数据 + widget 定义 |
| `dashboard.data.get` | 一次拿某个已发布看板所有 widget 的数据 |
| `dataasset.get` | 拿某个 `allowSubscription=true` 资产的详情 |
| `dataasset.schema.get` | 拿该资产的列 schema |
| `dataasset.metadata.get` | 拿该资产的富元数据（`lastUpdated` / `expectedUpdateCadence` / cron / 数据源描述等 20 字段）|
| `dataasset.data.get` | 拿该资产的历史数据（预览有效范围内）|
| `dataasset.data.getRealtime` | 拿该资产的实时镜像数据（若配置了 realtime mirror）|
| `process.ingestion.get` | 拿某个 `allowSubscription=true` 流程的结构（**不含 stepCfg 源码**）|
| `process.component.list` | 列平台可用的步骤组件类型（rendering diagram preview 用）|

### 硬性约束

- **只读白名单**：**仅上表 10 个 skill** 可调，其余 skill（包括其它只读 GET，如 `investment.stock.portfolio.list` / `dashboard.list` / `dataasset.list`）无论是否存在都返回 403 `missing-scope`。任何写操作（subscribe / create / update / delete）同样 403；哪怕手工构造匿名 PUT/POST 到底层 `/api/**`，Node 代理层也会先 401 拦截，不会到 Spring。
- **每 IP 限流（三桶，任一超限即 429）**：

  | 桶 | 范围 | 限额 | 429 响应体 |
  |---|---|---|---|
  | 通用桶 | 所有匿名 skill | 60 / IP / 分钟 | `{"success":false, "message":"Too many anonymous agent requests, ..."}` (无 `bucket` 字段) |
  | 数据爆发桶 | `dataasset.data.get` + `dataasset.data.getRealtime` | 10 / IP / 分钟 | `{"success":false, "traceId":"...", "message":"Anonymous data-fetch burst-limit exhausted (10/min per IP). ...", "bucket":"burst"}` |
  | 数据日总桶 | 同上 | 100 / IP / 天 | `{"success":false, "traceId":"...", "message":"Anonymous data-fetch daily budget exhausted (100/day per IP). ...", "bucket":"daily"}` |

  收到 429 时读 `response.body.bucket` 判断：`"burst"` 等 60 秒重试；`"daily"` 今日不再放行该 skill，建议引导用户注册 Bearer Token；无 `bucket` 字段则是通用 60/min 桶命中。

  **Rate-limit 存储：** v1.0.37 起三桶都存 Redis sorted sets (`anonratelimit:{burst,daily,general}:<ip>`)，通过 Lua 原子脚本实现 sliding window。fleet 内所有 Node worker + 所有 host 共享一份 counter，反爬承诺**真的**成立。**Redis 不可用时 fail-open**：静默放行 + ERROR 日志 `event:"rate-limit-redis-fail"`，反爬承诺仅在 Redis 健康时有效（运维监控 fail-open 日志识别异常）。
- **preview token 服务端自动签**：不用你手工去 `/preview-token` 拿；Node 按 skill 类型选：dashboard 类（`dashboard.get` / `dashboard.data.get`）**要求调用方在 `params.pathParams.id` 里传目标看板 id**，Node 会用该 id 签 dashboardId-bound token；未传 id 或其它 skill 一律降级为 `standalone` sentinel（等同 dataasset 类行为）。
- **无效 Bearer 不降级**：如果传了 `Authorization: Bearer <bogus>`，返回 401 而**不会**悄悄退回匿名模式给你部分数据。要匿名就别传 header。
- **无跨租户 leak**：所有资产读都走 `canReadAsset` gate；只有 `allowSubscription=true` 的资产/看板/流程会被返回，其它一律 404。跟浏览器 `/marketplace` 未登录访客看到的是同一套子集。
- **Dashboard-scoped token 不能跨团枚举**：dashboard-A（发布者 = team-A）签的 preview token 无法通过 `dataasset.metadata.get` 读到 team-B 的资产元信息，哪怕 team-B 资产 `allowSubscription=true`。仅 `standalone` sentinel token 可读所有公开挂牌资产。

### 匿名模式下的**能力受限**（订阅后才解锁）

数据获取类 skill（`dataasset.data.get` / `dataasset.data.getRealtime` / `dataasset.get` / `dataasset.metadata.get` / `process.ingestion.get`）在匿名模式下**服务端会自动应用以下约束**，参数会被静默改写或剥离——不是 400，你的 curl 依然能正常拿到响应，但拿到的不是你请求的形状：

- **分页强制固定 `page=1, size=25`**：传任何其他值都被服务端硬覆盖。响应 `pageSize=25, currentPage=1`。想拿更多请订阅后用 Bearer Token 调。
- **过滤 / 排序参数被静默清空**：`filterColumn / filterValue / filterOp / orderBy / orderDirection` 一律置 `null` 再进服务层。想按条件过滤请订阅后再来。
- **发布者身份字段被剥离**（`dataasset.get`）：`dataSource / realtimeDataSource / businessOwner / technicalOwner / teamName / jobCode / createdBy / createdDate / updatedBy / updatedDate` 一律返回 `null`。Metadata map 中 `teamName / dataSource / jobCode / createdBy / createdDate / sourceDescription` 也被剥离。
- **`process.ingestion.get` 的 `stepCfg` 被剥离**：匿名调用者拿不到 process step 的源码 / SQL / Python 内容。
- **`totalElements` 是哨兵值 `0`，不是真实总数**：匿名调用不消耗后端 `COUNT(*)` 查询（防止 JDBC 池 DoS）。分页导航请以 `data.length` 为准。

配合分页固定 + rate limit，匿名调用者理论上每 IP 每天最多拿到 2,500 行数据（100 次 × 25 行）——真的想跑分析请注册。

### 匿名模式下常见的误用

- ❌ 不要**基于匿名 preview 数据做投资决策** —— 25 行不是完整数据集，这只是"试读"，不是"取样"。
- ❌ 不要**用多 IP 池绕 rate limit** —— 我们记录并封 IP 池行为，正确路径是注册 Bearer Token。
- ❌ 不要**期望 `totalElements` 反映真实行数** —— 匿名调用永远返回 0，这是设计意图，不是 bug。
- ❌ 不要**在匿名模式下尝试 `filterColumn=...`** —— 参数会被静默丢弃，返回的是无过滤的前 25 行，不是过滤后的结果。

> **技术契约锚点**（review 用）：匿名 skill 白名单 = Node `app.js` 的 `ANONYMOUS_SKILL_SCOPES` 常量；匿名 rate limit = `canAnonymousAgentCall` (60/min) + `canAnonymousDataFetchCall` (10/min burst + 100/day daily)；preview + HMAC 验证 = `docs/auth-flow-invariants.md` §1 + §2.6 + §2.6.1；能力锁定实现与残留 test 缺口 = `docs/plans/2026-07-07-anon-preview-dataasset-lockdown.md`。

### 从匿名 → 注册的漏斗

匿名浏览完，如果用户想真正订阅一个看板 / 用私有数据 / 跑回测，需要**注册并领 token**：

- 引导用户去 `https://privora.cn/register`（`marketplace.item.subscribe` 是 🟡 写操作，不在匿名 scope 里）
- 或直接调 `auth.user.register` skill（也在匿名 scope 之外 —— 需要一层 signup 意图确认，见 §用户注册 & 反馈）

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
# 自定义 CLI 参数直接当 flat key 传（key 以 - / -- 开头，与 process.ingestion.execute
# 的 Map<String,String> body 逐字对应）。后端会自动注入 `-f <procName>` —— 不用自己传 -f。
RESP=$(scripts/lg_agent_exec.sh process.ingestion.execute id=123 \
  -start_date=20260419 -end_date=20260420 --env=dev)
EXEC_ID=$(echo "$RESP" | jq -r '.executionId')

# 轮询日志，直到 completed=true
OFFSET=0
while :; do
  LOG=$(scripts/lg_agent_exec.sh process.ingestion.execute.log.get \
    id=123 executionId="$EXEC_ID" offset="$OFFSET")
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
RESP=$(scripts/lg_agent_exec.sh marketplace.item.subscribe itemId=dashboard-china-merchants-bank-watch)

# 2) 从 response 拿到本租户的 cloned dashboard ID
DASH_ID=$(echo "$RESP" | jq -r '.clonedDashboardId')

# 3) 构造 1-click deeplink — Agent 把这个 URL 给用户
DEEPLINK="https://privora.cn/dashboards?selectId=${DASH_ID}&openAlerts=true"
echo "请打开此链接配置告警：${DEEPLINK}"
```

用户点链接进去，metric alert modal **自动打开**——已经对准刚订阅的 dashboard，剩下用户填阈值 + 选 webhook 渠道 finalize 就完。**user-in-the-loop 边界保留**（敏感操作仍需用户在 web 上确认），但 5 步导航 + 选 dashboard + 翻 toolbar 找 "Alerts" button 这些都省了。

这是平台活跃用户反馈最集中的需求——以前的路径是：订阅 → 跳到 dashboard 列表 → 找到目标 dashboard → 打开 toolbar → 找 "Alerts" button → （第一次还要去 `/datasources` 配 webhook，回来再继续）→ 配置 → 保存。这次更新把这条路径压到 **1 步**。

### 场景 6：模拟交易（paper trading）—— 暂不可自助，走 Process Python 节点（#787）

> **您：** "用模拟账户跑一笔 600519 的市价买单 100 股，看看现在能不能成交。"

**这条路径目前不能靠通用 Agent + 本包 Bearer Token 一次调用走完。** 本节曾给出一段示例，调用 `paper.account.create` / `paper.order.place` / `paper.order.get` 三个 id —— **均不存在于 catalog**，跑起来只会拿到 `400 Skill not found`（#787）。而且光改 id 也走不通：`paper.*` 是**保留 scope 命名空间**——自己去 个人设置 → Token 管理 创建一个带 `paper.account.read` / `paper.orders.write` 的 PAT，后端会直接拒绝 `400 RESERVED_SCOPE`，不存在"自助签发"这条路。

真实能力叫 `investment.paper.*`（见下方「investment.paper.\* — 模拟盘交易」小节，含真实 skillId `investment.paper.account.get` / `investment.paper.orders.submit` / `investment.paper.orders.list` / `investment.paper.positions.list`），但入口不是 `scripts/lg_agent_exec.sh`，而是**一个 Process 里的 `python_script` 节点**，节点里用 `lg.paper.*` SDK（`lg.paper.get_account()` / `lg.paper.submit_order(...)` / `lg.paper.get_orders(...)`）发起调用。Process 起跑时，后端会给这个节点自动注入一个 scope 限定的短期 Bearer（`paper.orders.write paper.account.read dataasset.read`）——Agent 不需要、也不能自己去申请这个 token。

**该怎么做**：

1. 市场已有现成模板 `starter_paper_trade_strategy`——`marketplace.item.subscribe` 一键复制到你的 tenant，改写里面的 `lg.paper.submit_order(...)` 调用即可，不需要从零搭 Process。
2. 若要从零建：用 `process.create`（`kind: "run_python"`）建一个含模拟下单脚本的步骤，`process.ingestion.execute` 跑起来——节点内的 `lg.paper.*` 调用由平台自动授权，不经过本包的 Bearer。
3. 若确实需要在 Process 之外、从外部 Agent 直接调 `investment.paper.*`：只能由平台管理员按"策略绑定模拟账户"流程走 UI 手动铸一个 process-execution token 再转交给你的 Agent——**这不是本包能自助完成的操作**，不要承诺用户"改个 id 就行"。

支持涨跌停 / 停牌 / suspended-stocks 信号、scheduler-driven 撮合。适合的 use case：策略上真实交易前 12 个月 paper trade 验证（per 6 阶段量化研究流水线最终关卡）——但入口是 Process 编排，不是本包 Bearer 的直接调用。

## 技能列表

### REST 技能（`scripts/lg_agent_exec.sh` 调用）

> 公开版 skill 覆盖 4 类操作，见 [§🛡️ Scope & Operator Responsibility](#scope--operator-responsibility) 完整的 read / idempotent-write / workflow-transition / outbound-webhook 分类。**大部分**删除、撤销等破坏性/管理类操作不在本 skill 范围内，需通过 platform UI 或 admin 工具完成；**例外**是标记 🔴/🟡 且 `confirmRequired:true` 的一小撮 workflow-transition 类操作（`process.ingestion.delete` 等 14 个，见下方 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake)），这些 Bearer token 可达，但必须先完成两步确认握手——单次调用不会直接执行。系统级审批（管理员 approve/reject 一个陌生人发起的请求）仍然不在本 skill 范围内，需要 platform UI。
> 风险标记：🟢 low / 🟡 medium / 🔴 high。所有 `GET` 技能默认对会话用户开放；写操作需显式授予 scope。

> 📦 **Request shape (v1.0.45+)**: 命名参数扁平写法 —— 直接用 `key=value` 传参，不用手拼 JSON：
> ```bash
> scripts/lg_agent_exec.sh dataasset.data.get id=42 filter_column=code filter_value=000135
> ```
> 等价于旧 envelope 形式 `{"skillId":"dataasset.data.get","params":{"pathParams":{"id":42},"query":{"filter_column":"code","filter_value":"000135"}}}`——网关会按每个 skill 的 path 模板自动把 flat key 分类到 `pathParams` / `query` / `body`。`key=value` 一律当字符串（保留 `stock_num=000135` 这类前导零）；数字/布尔/数组用 `key:=value`（如 `qty:=100`）。**旧 envelope 形式 100% 继续可用，两种写法可以在同一次调用里混用**（例：数组 body 用 `--json`，path 参数用 flat key）。想看某个 skill 接受哪些 key，跑 `scripts/lg_agent_list.sh describe <skillId>`。完整规则 + 历史踩坑 + envelope 手工写法见文末 [§高级 / 兼容性附录](#高级--兼容性附录)。

#### 高风险操作确认握手 (confirm handshake)

14 个标记 `confirmRequired:true` 的技能对 Bearer token 可达（`process.ingestion.delete`、`schedule.job.{online,offline,delete}`、`schedule.instance.{redo,hold,kill,cancel,force_start,mark_success}`、`subscription.token.revoke`、`metric.alert.delete`、`investment.paper.account.reset`、`team.python.method.delete`），但**单次调用永远不会直接执行**——第一次调用总是返回 HTTP 409，必须完成两步握手才能真正执行。（另有 6 个 `investment.{stock,fund,gold}.{portfolio,trading}.delete` 目前设计上暂不对 token 开放，见下方「不可达」说明。）

**① 第一次调用（不带 `approvalId`）→ 总是 409：**

```bash
scripts/lg_agent_exec.sh process.ingestion.delete id=42
```

```json
{
  "success": false,
  "traceId": "...",
  "message": "Approval required for high-risk action",
  "requiredScope": "process.ingestion.delete",
  "confirmRequired": true,
  "approvalId": 27,
  "expiresAt": "2026-08-18T19:30:00",
  "skillId": "process.ingestion.delete",
  "next": "self-confirm-or-await-admin-then-resend",
  "nextAction": {
    "method": "POST",
    "url": "/agent/skills/execute",
    "body": {
      "skillId": "process.ingestion.delete",
      "params": { "pathParams": { "id": 42 }, "approvalId": 27 }
    }
  },
  "hint": "approvalId must be nested inside \"params\" (params.approvalId), never a sibling of \"skillId\" — see nextAction for the exact resend request. Optionally POST /api/agent/approvals/27/confirm ahead of time to self-confirm without waiting for the resend (idempotent — resending via nextAction afterwards still succeeds either way). Window closes at expiresAt."
}
```

**② 把 ① 的内容原样展示给人类，等待其同意**（这是防误操作装置，不是授权检查——真正的权限仍然是 token 的 scope；见 [§🛡️ Scope & Operator Responsibility](#scope--operator-responsibility)）。

**③ 重发，把 `approvalId` 嵌进 `params` 里 → 200：**

`nextAction.body` 就是可以直接拿去重发的完整请求体——**逐字**用它，不要自己重新拼：

```bash
# Windows Git Bash 提醒：--data '...' 把 body 放进命令行参数，curl.exe 是原生 Windows 程序，
# MSYS2 会按本地 ANSI 代码页重编码 argv——如果 approve/reject 理由等字段含中文/非 ASCII，
# 内容会被静默改坏。优先用下面的 lg_agent_exec.sh；必须裸 curl 时改用 --data-binary @file。
curl -X POST "$LG_AGENT_BASE_URL/agent/skills/execute" \
  -H "Authorization: Bearer $LG_AGENT_TOKEN" -H "Content-Type: application/json" \
  --data '{"skillId":"process.ingestion.delete","params":{"pathParams":{"id":42},"approvalId":27}}'
```

优先用 `lg_agent_exec.sh` 的扁平写法（也修好了上面这个 Windows 编码坑），`approvalId` 作为一个 flat key 传即可（网关不会把它当作业务参数转发下游，也不会因为它出现在 `params` 顶层而拒绝识别）：

```bash
scripts/lg_agent_exec.sh process.ingestion.delete id=42 approvalId:=27
```

**唯一会生效的判据是 `params.approvalId`。**踩坑记录（issue #74，2026-08-18 修复）：

- ❌ `{"skillId":"process.ingestion.delete","approvalId":27,"params":{"pathParams":{"id":42}}}`——`approvalId` 和 `skillId` 同级、不在 `params` 里，**网关只会把顶层的 `pathParams`/`query`/`body` 折进 `params`，`approvalId` 不在这个白名单内**，会被静默丢弃，网关认为你还没有 approvalId，重新建一条 pending 审批（`approvalId` 会一次次往上涨），永远卡在 ①。
- ❌ 单独发 `confirm:true`（不带 approvalId，或 approvalId 放错位置）——`confirm` 字段本身**不会被读取**，只是网关内部保留字（防止它泄漏到下游请求），加不加、真不真都不影响判定。
- ✅ 只有 `params.approvalId`（嵌套在 `params` 内）才会被网关识别为「已经有一个待处理的审批」。

`expiresAt` 是这条审批任务的过期时间（TTL 10 分钟）——超时后 `approvalId` 失效，重发 ③ 也会 409，须重新走 ①。

**（可选）提前自确认**：`agent-skill/scripts/lg_agent_approval.sh confirm <approvalId>` 直接命中 `POST /api/agent/approvals/{id}/confirm`（同一 requester 才能确认自己发起的审批），可以在等待人类确认期间提前调用；之后按 ③ 正常重发仍会成功（幂等）。这**不是**必需步骤——③ 本身已经原子地完成"自确认 + 消费"，`confirm` 只是给需要分两次操作的场景用的便利工具。管理员批准/拒绝走 `lg_agent_approval.sh approve|reject`（需要 `userLevel>=8`，非管理员 token 调用会 403——这不是本 skill 的入口，除非你就是管理员）。

**不可达（暂不支持）**：`investment.{stock,fund,gold}.{portfolio,trading}.delete`（6 个）目前设计上对 token 模式仍然 409——它们背后共用的几个 handler 目前只能声明单一权限校验字符串，无法表达"以下 12 个 scope 名中的任意一个"，属于已知限制，不是本次修复范围。

##### 409 响应辨析（仅限 token 模式的确认握手 409）

本节只覆盖上面**确认握手**流程里出现的 409——即 `confirmRequired:true` 技能在 token 模式下走 ①/②/③ 过程中收到的 409。判别请优先看 `status` 字段；只有响应没带 `status` 时才退回看 `message` 原文。

| 情形 | 信号 | 可恢复？ |
|---|---|---|
| 技能不在可握手集合内（即那 6 个 `investment.*.delete`） | 无 `status`；`message` 原文为 `"High-risk approval flow for token mode is not enabled yet for this skill"` | **否 —— 终态**，换个技能/等待后端扩大集合，重试无用 |
| ① 第一次调用的响应 | 带 `approvalId` + `nextAction` | 是 —— 照 §②③ 走握手 |
| `status:"expired"` | `message` 为 `"approval task expired"` | 是 —— 从 ① 重新开始 |
| `status:"rejected"` / `"consumed"` / `"unknown"`（resend 时先命中 self-confirm 端点，这是 token 模式下**最常见**的一类） | `message` 原文为 `"approval task is not pending"`，仅靠 `status` 字段区分三种原因；同一状态族在更窄的竞态窗口下（confirm 成功后、consume 执行前被并发消费）也可能改由 consume 端点报出 `message` 原文 `"approval is not approved"`——两种 message 字符串对应同一组 `status` 取值，都只能靠 `status` 区分 | 是 —— 从 ① 重新开始 |
| `"approval task not found"` / `"approval task owner mismatch"` / `"approval skill mismatch"` / `"approval team mismatch"` / `"approval scope mismatch"` / `"approval payload hash missing or mismatched"` | 只有 `message`，无 `status` | **否 —— 调用方自身的 bug**，不是重试能解决的（`approvalId` 传错、跨用户/跨团队复用、resend body 与①不一致等） |
| `PROCESS_NAME_EXISTS`（`process.create` / `process.pipeline.build`） | `code:"PROCESS_NAME_EXISTS"` | 与确认握手无关，非破坏性——换个 `name` 重试即可 |

**范围声明**：session 模式（Cookie 会话）另有一条独立的幂等冲突 409（`app.js:2854`，仅在 `mode !== 'token'` 时触发），本节**不覆盖**——它对本 skill 的 Bearer token 使用者结构性不可达（公开版 skill 只支持 Bearer Token 模式，见 [§Security Notes](#security-notes)），是一个本 PR 不修的、独立的既有未文档化缺口，这里明确写出原因而不是略过不提。

### 流程 (Process / Ingestion)

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `process.ingestion.list` | GET | 列出所有流程 | 🟢 |
| `process.ingestion.get` | GET | 根据 id 获取流程详情 | 🟢 |
| `process.ingestion.execute` | POST | 异步触发流程执行（返回 executionId）。`body` 接收自定义 CLI 参数，如 `{"-start_date":"20260419","--env":"dev"}`。后端自动注入 `-f <procName>`，不要自己传 `-f`。 | 🟡 |
| `process.ingestion.execute.log.get` | GET | 按 `executionId` 拉取日志+状态，支持 `offset` 增量轮询。记录持久化在 `process_execution` 表 + 磁盘文件，重启不丢。 | 🟢 |
| `process.component.list` | GET | 列出当前团队可用的步骤组件（含 Markdown 使用说明） | 🟢 |
| `process.pipeline.build` | POST | 一次性创建完整 pipeline（节点+组件+边）。**`python_script` 节点的 `stepCfg` 必须使用执行器字段名 `"script"`（不是 `"pythonScript"`）**，例：`{"script":"import sys\nprint(sys.version)","requirements":"pandas"}`。`process.component.list` 返回的 form-schema 中的显示名 `pythonScript` 是 UI 表单专用名，不等于执行器运行时 JSON key——混用会导致执行时报 "Python script is empty or NULL"（2026-07-10 incident，已在后端加翻译层向前兼容，但规范写法仍推荐用 `script`）。 | 🟡 |
| `process.create` | POST | **业务字段封装层**（`POST /api/ingestions/create-simple`），比 `process.pipeline.build` 更简单：不需要知道 node id / stepSeq / `aftId`/`sStep`/`nStep`/`fStep` 拓扑字段 / 画布坐标 / 执行器 stepCfg 信封——只填 `{name, description?, steps:[{kind, label?, ...}]}`，后端自动组装成 `process.pipeline.build` 同款请求并复用同一条持久化路径。`kind` 是封闭枚举，只支持**单链路顺序执行**（不支持分支/for 循环/if 节点，那些场景仍用 `process.pipeline.build`）。详见下方 [`process.create` 详情](#processcreate-详情)。 | 🟡 |
| `process.pipeline.update` | PUT | **全量更新已有 pipeline**（`PUT /api/ingestions/{id}`，同形 `BuildPipelineRequest`）。`nodes` 省略=仅改名/描述，保留现有步骤；`nodes=[]` 显式清空；`nodes=[...]` 全量替换。每次 PUT 自动写一条 `dacp_meta_proc_version`，可 `/versions/{n}/restore` 回滚。legacy `team_name IS NULL` 的流程会直接 403，需先 backfill。**想只改一个步骤的 label/conf/remark 而保留 DAG？用 `process.pipeline.update_node` PATCH，避免 aftId 等拓扑字段被默认值 `"-1"` 误清空。想只改流程名称/描述？用 `process.pipeline.patch_meta`。** | 🟡 |
| `process.pipeline.update_node` | PATCH | 部分更新单个步骤（`PATCH /api/processes/{procId}/steps/{stepId}`）。**字段掩码语义**：仅 `stepLabel` / `stepConf` / `remark` 三个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`aftId` / `sStep` / `nStep` / `fStep`（DAG 拓扑）出现在 body 即返回 HTTP 200 `success:false, code:"TOPOLOGY_FIELD_REJECTED"` —— 要改变 DAG 拓扑请用 PUT `process.pipeline.update` 全量替换所有节点。`stepName` / `stepSeq` / `parentId` 静默丢弃。**要清空 stepLabel/stepConf/remark 字段也必须走 PUT 全量替换** —— PATCH 设计为"只增改、不清空"。**此 skill 需要 `process.pipeline.update_node` scope（独立于 `process.pipeline.update`），现有 token 须重新签发方可使用。** | 🟢 |
| `process.pipeline.patch_meta` | PATCH | 部分更新流程级别元数据（`PATCH /api/ingestions/{id}/meta`）。**字段掩码语义**：仅 `procLabel` / `procDescr` 两个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`nodes`（拓扑变更）/ `procName`（标识符）/ `creater`（归属）/ `teamName` 出现在 body 即返回 HTTP 200 `success:false, code:"FIELD_NOT_PATCHABLE"` —— 要改名称/DAG 结构请用 PUT `process.pipeline.update`。**此 skill 需要 `process.pipeline.patch_meta` scope（独立于 `process.pipeline.update`），现有 token 须重新签发方可使用。** | 🟢 |

> ⚠️ **推大 `stepCfg` / pipeline 载荷（`process.pipeline.build` / `process.pipeline.update` /
> `process.pipeline.update_node` / `process.create`）之前请先看这条（v1.0.56 起）：**
> `POST /agent/skills/execute` 是这几个 skill 共用的唯一 dispatcher，后端专门为它把 JSON body
> 上限放宽到 **262,144 字节**（`lib/body-parser-limits.js` 的 `LARGE_JSON_LIMIT='256kb'`，
> 平台大多数路由是 100KB 默认值）——这也是为什么这几个 skill 的 payload 会比大多数 skill
> 更容易撞到本节要说的这条**更窄**的本地限制：`scripts/lg_agent_exec.sh` / `lg_agent_approval.sh`
> 把请求体和凭据一起放进同一条 curl `-K -` 配置流发送，转义后的那一行不能超过 **102,400 字节**——
> 引号密集的 JSON（`stepCfg`/SQL/脚本正文常见）转义后大约翻倍，所以**原始 body 约 77KB 起就可能
> 撞上这条本地限制**，即使后端本可以收下（262,144 字节上限还没到）。这条限制在 curl 7.81–8.1.x
> （Ubuntu 22.04、Debian 12 的系统自带版本）上是 curl 自己真实的配置行上限；curl 8.2.0（2023-07）
> 起该上限被 curl 官方抬到 10 MiB，但这个 wrapper **不探测本地 curl 版本**，对所有宿主统一取较低的
> 那个数字（换取"同一份脚本到处行为一致"），所以在新版 curl 上这条 102,400 是 wrapper 自己的保守
> 选择，不是 curl 的限制。**遇到时的可行做法**：把大 `stepCfg` 拆成多次 `process.pipeline.update_node`
> PATCH 调用，或改走平台网页 UI 直接编辑；不要指望升级本机 curl 能绕开（本 wrapper 不会因此放宽）。
> 公网 `privora.cn` 入口不受影响——那里 nginx 在约 5–8KB 就已经 414（见下方"最近更新"）。

#### `process.create` 详情

路径：`POST /api/ingestions/create-simple`，scope `process.create`（独立于 `process.pipeline.build`，现有 token 须重新签发方可使用）。

**为什么需要它**：`process.pipeline.build` 要求调用方懂平台内部的 DAG 拓扑（node id、`stepSeq`、`aftId`/`sStep`/`nStep`/`fStep` 边字段、画布 x/y/width/height）和执行器 `stepCfg` JSON 信封格式。`process.create` 只暴露业务字段——一个有序、有类型的步骤列表；封装层在服务端补平台管道，不生成任何业务代码（SQL/Python/消息文本仍由调用方自己写）。

**请求体**：

```json
{
  "name": "fund_dividend_wrapper_test",
  "description": "可选描述",
  "steps": [
    { "kind": "run_sql", "label": "create tables", "sql": "CREATE TABLE IF NOT EXISTS ...", "dataSourceName": "pg_main" },
    { "kind": "run_python", "label": "fetch akshare", "script": "import akshare as ak\nprint(ak.fund_fh_em())", "pipRequirements": ["akshare"] },
    { "kind": "run_python", "label": "tushare enrich", "script": "import tushare as ts\n# ...", "pipRequirements": ["tushare"] },
    { "kind": "print_summary", "label": "done", "message": "fund_dividend ingest complete" }
  ]
}
```

`kind` 封闭枚举，映射到真实平台组件（已核实执行器 `*StepMeta` 字段名，不是猜的）：

| `kind` | 平台组件 | 必填业务字段 | 可选字段 | 组装出的 stepCfg 信封 |
|---|---|---|---|---|
| `run_sql` | `sql` | `sql`、`dataSourceName` | — | `{"sql":..,"dsName":..,"needSplit":"true"}` |
| `run_python` | `python_script` | `script` | `pipRequirements`（字符串数组，pip 包名） | `{"script":..,"requirements":".."}`（`requirements` 由 `pipRequirements` 换行 join；未提供则省略该 key）。**注意 key 是 `script` 不是 `pythonScript`** —— 同 `process.pipeline.build` 那条 2026-07-10 坑，封装层已按执行器真实字段名组装，调用方不会踩到。 |
| `print_summary` | `print` | `message` | — | `{"message":..}` |

**body 里没有 `teamName` / `userName` 字段**——不是被忽略，是这个 DTO 上根本没有这个属性。租户归属 100% 走鉴权上下文（同 `process.pipeline.build`），payload 传了也不会被采纳。

**拓扑组装（调用方不需要关心，仅供理解结果）**：第 `i` 步（1-based）node id = `"<name>_step<i>"`，`stepSeq="<i>"`，画布自动横向布局（120×60，间距 220）。相邻两步之间只支持**单链路顺序执行**——`step[i]` 的 `sStep` 与 `aftId` 都指向 `step[i+1]` 的 `stepSeq`，`nStep`/`fStep` 保持 `"-1"`。这是 **fail-fast** 语义：任一步骤失败即中止整个 pipeline，不会静默跳到下一步。**不支持分支 / for 循环 / if 节点 / 并行**——那些场景请用 `process.pipeline.build` 或先用 `process.create` 建好线性骨架、再用 `process.pipeline.update` 全量替换加拓扑。

**返回**：与 `process.pipeline.build` 相同的信封 `{success, data:{id,name,description,created,teamName}, message}`。`name` 冲突返回 HTTP 409 `{success:false, code:"PROCESS_NAME_EXISTS"}`；`steps` 缺失某个 `kind` 必填字段返回 HTTP 400 `{success:false, code:"VALIDATION_FAILED", message:"..."}`。

**示例调用：**

```bash
scripts/lg_agent_exec.sh process.create name=fund_dividend_wrapper_test --json '{"body":{
  "description":"fund dividend ingest",
  "steps":[
    {"kind":"run_sql","label":"create tables","sql":"CREATE TABLE IF NOT EXISTS fund_dividend (...)","dataSourceName":"pg_main"},
    {"kind":"run_python","label":"fetch akshare","script":"import akshare as ak\nprint(ak.fund_fh_em())","pipRequirements":["akshare"]},
    {"kind":"run_python","label":"tushare enrich","script":"import tushare as ts\n# ...","pipRequirements":["tushare"]},
    {"kind":"print_summary","label":"done","message":"fund_dividend ingest complete"}
  ]
}}'
```

### 团队 Python 模块 (Team Python Methods)

团队级可复用 Python 模块（`team_lib`）——`enabled` 的模块可在 `python_script` 流程步骤里以 `from team_lib.<name> import ...` 导入。执行器每次运行前都会把所有 `enabled` 行重新物化成 `team_lib` 包（先整体删除、再重建），所以这里的改动从**下一次**运行才生效，不是立即生效。跨团队或不存在的 id 一律返回 403（不是 404，避免 id 枚举）。

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `team.python.method.list` | GET | 列出当前团队的可复用 Python 模块。返回 `id` / `name` / `code`（完整源码，不截断）/ `description` / `enabled` / `created_by` / `updated_at`。 | 🟢 |
| `team.python.method.get` | GET | 按 id 获取单个模块详情（含完整 `code`）。 | 🟢 |
| `team.python.method.create` | POST | 新建一个团队级可复用 Python 模块。`name` 必须匹配 `^[a-z][a-z0-9_]{0,127}$`；撞上保留包名（`team_lib`/`__init__`/`__main__`）或 Python 关键字/软关键字（如 `class`/`import`/`match`/`case`）会 400（会成为字面上的 `team_lib/<name>.py` 模块文件）；同团队内 `name` 唯一，重复返回 409 "Module name already exists"。`code` 落库前会过一遍安全黑名单（`os.system(`、`subprocess.*(`、`eval(`、`exec(`、`__import__(`、`os.environ`、`socket.socket(`、`shutil.rmtree(` 等），命中即 400 "Security check failed: code contains forbidden pattern [...]"——这是防误用护栏，不是沙箱边界。`enabled` 默认 `true`；设为 `false` 可先保存、暂不物化进 `team_lib`。 | 🟡 |
| `team.python.method.update` | PUT | 按 id 部分更新（**字段掩码语义**：只有 body 里出现的字段会被改；`name` / `team_name` 通过此接口不可改）。`code` 若出现须非空，且过与 create 相同的安全黑名单。 | 🟡 |
| `team.python.method.delete` | DELETE | **永久删除**一个团队 Python 模块。**不可恢复**——代码行被硬删（`repo.delete`，无软删除/版本历史），且从**下一次** `python_script` 执行开始，任何依赖 `from team_lib.<name> import ...` 的脚本都会抛 `ImportError`（物化是"每次运行先删再重建"，正在跑的执行不受影响，但之后每一次都会受影响）。经两步确认握手，见 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake)。 | 🔴 |

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
| `schedule.job.depends.list` | GET | 列出作业依赖（按 jobCode）。每行带 `dependGroup`——同组 OR、组间 AND | 🟢 |
| `schedule.job.depends.save` | POST | 全量替换作业依赖列表（旧的先删再写，不经确认握手——传入数组即为完整期望状态，遗漏的依赖会被静默清空）。支持按 `dependGroup` 分组做 OR/AND 组合 | 🟡 |
| `schedule.job.plugins.list` | GET | 列出作业绑定的插件（按 jobCode） | 🟢 |
| `schedule.job.plugins.save` | POST | 全量替换作业插件列表（旧的先删再写，不经确认握手——传入数组即为完整期望状态，遗漏的绑定会被静默清空） | 🟡 |
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
  { "dependCode": "upstream_a", "dependType": "10", "dependGroup": "g1" },
  { "dependCode": "upstream_b", "dependType": "10", "dependGroup": "g1" },
  { "dependCode": "20260424",   "dependType": "20",
    "batchCalExp": "${batchNo?calDate(-1,'d','yyyyMMdd')}" }
]
```
上面这份表示 `(upstream_a OR upstream_b) AND 时间依赖`。

- `dependType="10"` — 任务依赖，`dependCode` 是**另一个 jobCode**（同团队内可见）
- `dependType="20"` — 时间/批次依赖，`dependCode` 是时间字符串，`batchCalExp` 是批次偏移表达式（`${batchNo?calDate(...)}`）
- `dependGroup`（可选）——**分组键：同组 OR、组间 AND**。同一个非空 `dependGroup` 的多行任一满足即算该组满足；不同组（包括每一行 `dependGroup` 为空/不传，各自独立成组）之间要求全部满足——即退化为原来的全 AND 语义。合法格式 `^[A-Za-z0-9_-]{1,32}$`；空白会被规范化为 `null`。**任何一行格式不合法，整次保存都会失败**（`{success:false, message}`），且**不会删除任何已有依赖行**——可以放心重试。
- 其他字段：`procName`、`output`、`isDefault`（`"1"` 标默认）都可选
- `dependId` 每次保存都由服务端重新生成（UUID16），不用自己传，也不要依赖它在两次保存之间保持不变

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
| `datasource.list` | GET | 列出数据源。**不在默认 `read-data` 预设里**——默认预设建的 token 调会 403，需在创建 token 时手动勾选这个 scope，或重新签发。 <!-- #988:not-in-default-preset --> | 🟢 |
| `datasource.get` | GET | 获取数据源详情。**不在默认 `read-data` 预设里**，同上，需手动勾选或重新签发。 <!-- #988:not-in-default-preset --> | 🟢 |
| `datasource.list.active` | GET | 列出活跃数据源。**不在默认 `read-data` 预设里**，同上，需手动勾选或重新签发。 <!-- #988:not-in-default-preset --> | 🟢 |
| `datasource.connection.test` | POST | 测试数据源连接。**不在默认 `read-data` 预设里**，同上，需手动勾选或重新签发。 <!-- #988:not-in-default-preset --> | 🟡 |
| `datasource.update` | PUT | **全量替换**数据源（含连接配置 `dsConf`）。**想只改描述或显示标签？用 `datasource.patch`，避免 dsConf/dsAuth 被覆盖。** | 🟡 |
| `datasource.patch` | PATCH | 部分更新数据源元数据（`PATCH /api/datasources/{dsId}`）。**字段掩码语义**：仅 `dsDescr`（描述）/ `dsLabel`（显示标签）两个安全字段可被更新；缺失字段、显式 `null`、**以及空字符串 `""`** 都视为"跳过"（**不**清空）。**严格拒绝**：`dsConf`（更改连接目标会破坏运行中的 ETL）/ `dsType`（标识符）/ `dsAuth` / `dsId` / `dsName` / `teamName` 出现在 body 即返回 HTTP 200 `success:false, code:"FIELD_NOT_PATCHABLE"`。**此 skill 需要 `datasource.patch` scope（独立于 `datasource.update`），现有 token 须重新签发方可使用。** | 🟢 |
| `dataasset.list` | GET | 列出数据资产 | 🟢 |
| `dataasset.get` | GET | 获取资产详情 | 🟢 |
| `dataasset.schema.get` | GET | 获取资产 schema（列名/类型）；支持 `?refresh=true` 绕过缓存实时重新采集 | 🟢 |
| `dataasset.metadata.get` | GET | 获取资产富元数据：20 个字段，包含 `lastUpdated`（最近刷新时间）、`expectedUpdateCadence`（调度批次类型，来自关联 Job）、`cronExpression`（cron 表达式）、`sourceDescription`（数据源描述）。Bug #50 后续，用于程序化判断资产新鲜度。**2026-09 起已在默认 `read-data` 预设里**，用默认预设建的 token 直接调即可。 | 🟢 |
| `dataasset.data.get` | GET | 查询资产数据（盈亏、行情等，全量历史）；支持 `filter_op` 过滤运算符（见下方详情）。MC 数据源资产速度较慢（2-5s）但包含完整历史 | 🟢 |
| `dataasset.data.getRealtime` | GET | 查询资产的 **实时镜像数据源**（PG 热窗口，最近 365 天）；低延迟，适合仪表盘 / 实时 P&L。资产未配置 `realtimeDataSource` 时返回 `{success:false, message:"This asset has no realtime mirror"}`，不抛异常。路径：`GET /api/data-assets/{id}/data-realtime` | 🟢 |
| `dataasset.history.field-as-of` | GET | 点状时间（PIT）股票状态字段查询：`is_st`（ST/暂停挂牌）、`market_board`（板块）、`delisted`（退市）、`industry`（申万行业分类）。返回指定股票在某日期上的历史状态快照。依赖 PR-B ETL 完成首次回填后方可返回实际数据；回填未完成前返回 `data:null`。**这个 scope 不在默认 `read-data` 预设里**——用默认预设建的 token 调会 403，需要在创建 token 时手动多勾这一项，或重新签发。详见下方「dataasset.history.field-as-of」节。 <!-- #988:not-in-default-preset --> | 🟢 |
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

**snake_case 别名是 agent-skill gateway 的属性，不是这个 HTTP 端点本身的属性。** 通过本技能（`dataasset.data.get` / `lg.get_asset_data`）调用时，gateway 会把 snake_case 参数名（`filter_column` / `filter_value` / `filter_op` / `filter_column_2` / `filter_value_2` / `filter_op_2` / `order_by` / `order_direction`）翻译成 camelCase 再转发给后端（`lib/skill-catalog.js` 的 `paramAliases`，经 `lib/param-aliases.js` 施加，仅在 skill-dispatch 路径生效）。**直接对底层 HTTP 端点发起裸请求（不经过 gateway）必须使用 camelCase**——snake_case 参数名会被 Spring 静默忽略（未声明的 `@RequestParam` 不报错也不生效），导致过滤器悄悄失效而不是报错。2026-07-30 起，四个资产数据 GET 端点（本端点、`dataasset.data.getRealtime`、以及两个 `/api/internal/**` 内部端点）新增了未识别 query 参数的 fail-loud 校验——裸 HTTP 调用如果误用 snake_case 名，会收到 `{"success":false,"message":"Validation Failed: Unrecognized query parameter(s): ..."}`（HTTP 200），而不是从前那样被静默丢弃、无任何信号。

**省略 `filter_op` 时的默认值**：只传 `filter_column`/`filter_value`、不传 `filter_op`（`filterOp`）时，默认运算符是 **`contains`**（`LIKE '%value%'`），**不是精确匹配**——`filter_column=fund_code filter_value=510300`（没有 `filter_op`）会匹配任何**包含** `510300` 子串的代码，不止 `510300` 本身。想要精确匹配请显式传 `filter_op=eq`。

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
| `between` ✨ 2026-07-28 | `BETWEEN 'start' AND 'end'` | `filterOp=between&filterValue=20140101,20141231` |

- **多值运算符**（`in` / `not_in`）：`filter_value` 用英文逗号分隔，如 `filter_value=600519,000001,601398` → 生成 `IN ('600519','000001','601398')`。
- `like` 和 `contains` 行为相同：平台都生成 `LIKE '%val%'` 子串匹配。如需自定义 LIKE 模式（前缀 / 后缀 / 通配符位置），目前需在调用方 SQL 端处理或走 `POST /api/data-assets/{id}/query`。
- **`between`（issue #68，2026-07-28）**：`filter_value` 必须是**恰好 2 个**用英文逗号分隔的值（`start,end`），生成 `field BETWEEN 'start' AND 'end'`。**Fail-loud，无静默降级**——以下任一情况直接返回 HTTP 200 `{"success": false, "message": "Validation Failed: ..."}`，绝不会静默退化成单值过滤或悄悄改用最新分区：
  - 只给 1 个值或给了 3+ 个值；
  - 两个值类型不一致（如一个能解析成数字、另一个不能）；
  - `start > end`（范围反了）。
- **未知运算符拒绝**（不静默降为 eq）：传入不在上表中的值（如 `filterOp=regex`）→ HTTP 200 `{"success": false, "message": "Validation Failed: Unsupported filter operator: regex"}`。
- `order_direction`（snake_case；camelCase 写法为 `orderDirection`）接受 `asc` / `desc`（大小写不敏感），默认 `asc`。

**分页上限与截断信号（feedback #69，2026-07-29，v2 修正见下）**：`dataasset.data.get` 对 MaxCompute-backed 资产（`fund_day`、`stock_day_v2` 等历史全量资产）的**每页行数硬上限是 1000 行**。PG-backed 资产（`dataasset.data.getRealtime` 的 365 天热窗口镜像）没有这个上限。

- **`size` 超过 1000 时必须同时传 `order_by`，否则直接报错（不看 page）**：MaxCompute 的分布式扫描在没有 `order_by` 时不保证行序一致——不仅是"翻页时前后两页可能对不上"，更关键的是**同一个 `page=1,size=10000` 请求重复调用两次，拿到的可能是完全不同的一批行**（这正是 2026-07 一起线上事故的根因：某每日选股流程按 `size=10000` 无排序键拉全市场数据，30 天内每天实际拿到的股票代码集合都不一样，导致移动均线永远算不出来，且流程本身"成功退出"、日志正常，是一个完全静默的失败——事故的行为特征更像是"同一个请求形状每次返回任意子集"，而不仅仅是"第二页跟第一页对不上"）。因此判定条件是 **`size > 1000` 且未传 `order_by`**——**第一次调用（`page=1`）就会报错**，不会等到翻页才发现：`{"success": false, "message": "Validation Failed: ... requires an 'orderBy' column ..."}`（HTTP 200）。
- **`size <= 1000` 永远不受此限制**，无论 `page` 多大、总行数多少——marketplace 匿名预览固定 `page=1&size=25`，`25 <= 1000` 恒成立，天然、永久豁免，不需要任何特殊处理；普通小分页翻页（如 `size=25&page=2`）也不受影响，行为与本次修复前一致（这不是本次修复的范围）。
- 当 `size` 超过 1000 **且**提供了 `order_by`（因此调用成功）时，响应里会带两个额外信号字段：`truncated: true` 和 `effectivePageSize: 1000`（实际生效的每页行数）。不超限时这两个 key **不存在**（不是 `false`/`null`，而是整个 key 缺失——沿用 `totalCountApproximate`/`totalCountTruncated` 的既有 additive-flag 惯例）。`pageSize` / `totalPages` 字段始终反映实际生效值，不会再出现"回显了 `size=10000` 但只拿到 1000 行"的自相矛盾。**换句话说，`truncated:true` 只会出现在你自己提供了排序键的成功响应里**——没有排序键的超限请求根本走不到返回结果那一步，直接报错。
  - 示例（第一次调用即可，不用先拿 page=1 再试探）：`scripts/lg_agent_exec.sh dataasset.data.get id=76 filter_column=fund_code filter_value=510300 filter_op=eq size=10000 order_by=day_id`。

**`fund_day.adj_nav` 缺失信号（feedback #64 / #73，2026-08-18，LA REVISE #2 订正措辞）**：`fund_day` 有 `unit_nav`（单位净值）和 `adj_nav`（复权净值）两列。**`unit_nav` 会被基金份额拆分 / 分红再投污染**——一旦发生拆分，`unit_nav` 会在拆分当天出现一个和真实收益完全无关的价格台阶（实例：513100 于 20220113 发生 5:1 拆分，`unit_nav` 从 5.189 跌到 1.009，凭空产生 -80.56% 的"暴跌"；`adj_nav` 同期从 5.189 平滑过渡到 5.045）。**`adj_nav` 才是唯一能正确反映基金全收益（含拆分/分红调整）的字段**，长期回测 / 算收益率 / 算相关性一律应该用 `adj_nav`，不能用 `unit_nav`。

  - **`adj_nav` 缺失是两条独立通道、两种不同性质的缺口，覆盖比例悬殊——不要把其中一条通道的情况当成全貌**：
    - **`dataasset.data.get` / `lg.get_asset_data`（MC 主数据源）**：缺口是**极少数**（2026-08-18 审计：最新一天 12,482 行里仅 5 行 `adj_nav IS NULL AND unit_nav IS NOT NULL`，且全部来自 `source='tushare_fund_nav'`）。
    - **`dataasset.data.getRealtime` / `lg.get_asset_data_realtime`（PG 实时镜像）**：缺口是**主体**（同一天 24,606 行里 12,138 行满足同一条件，除 5 行外全部来自 `source='akshare_em'`）。根因是 proc 3401（`fund_day_backfill`，写 MC）的依赖图里没有 proc 3540（`fund_day_backup_akshare`，写 PG）——MC 分区在 akshare 数据写完 PG 之前就被 tushare 数据覆盖，且从不回访旧分区，所以 akshare 来源的行**永久不会进入 MC**。这是**覆盖缺口**（行根本不存在），不是"存在但为 NULL"的缺口——对该类基金，`dataasset.data.get` 要么直接返回 0 行，要么返回一段完全没有触发下方 NULL 检查机会的历史。
    - `fund_day` 是全平台仅有的两个配置了 `realtimeDataSource` 的资产之一，dashboard widget 带 `__dashboardId` 时**无条件**走 PG 镜像——这不是边缘路径，是这类资产的主要读路径之一。
    - **注意**：本节的 `adjNavIncomplete` 信号目前只到达**直接调用** REST / `get_asset_data*` 的调用方（agent 脚本、`curl` 等）；dashboard 大盘的 table 类 widget 渲染管道（`DashboardDataService.fetchWidgetData`）在把结果交给前端之前会丢弃除 `data` 行以外的所有字段，**尚未把此信号透出到浏览器 UI** —— 这是一个更早、更大的既有缺口，不在本次改动范围内，已登记为独立 follow-up(issue #864)。
  - 因此**两条通道的响应体都会带同一个额外的 additive-only 信号字段** `adjNavIncomplete`：当返回的某一页里出现"某行 `adj_nav` 为 NULL 但 `unit_nav` 非 NULL"（即确认是真实交易日，只是复权净值缺失，不是非交易日占位行）时，该通道的响应体里会出现 `adjNavIncomplete: true`；否则该 key **不存在**（同 `truncated`/`effectivePageSize` 的 additive-flag 惯例）。**但要记住上面的覆盖比例差异**：MC 通道触发这个信号的概率极低，PG 实时通道才是这个信号真正生效的地方。
  - **`lg_utils.backtest_examples.fund_day.run_fund_day_backtest`（见下方 Python 工具库表格）内置的 fail-loud 检查只保护 MC 通道**（它调用 `get_asset_data`，从不调用 `get_asset_data_realtime`）——对 MC 里那极少数的 5 行是真保护，但对 PG 通道的 12,138 行**没有任何保护**，因为直接调用 `dataasset.data.getRealtime` / `lg.get_asset_data_realtime` 的代码根本不经过这个回测封装。**不要在看到 `adj_nav` 为 NULL 时静默退回 `unit_nav` 使用**——反馈#64 记录过真实事故：某次静默回退把 YTD 算成 -47.06%（真实约 +7~10%），与基准相关性 0.2956（真实应 >0.85）；直接读 `dataasset.data.getRealtime` 的调用方必须自己检查 `adjNavIncomplete`，不能假设有回测封装帮你挡住。
  - 这个设计是**故意的 fail-loud**，不同于 `stock_day_v2.adj_factor` 的 optional pass-through（PR #678 独立裁定过）——两者面对的是不同的数据缺口性质，选择不同的处理方式是设计决策，不是标准漂移。本次改动**不做任何推导/回填**（不会用 `unit_nav` 的日收益率累乘出一条近似 `adj_nav`），这类链式推导方案已被 LA 明确驳回（先例：`stock_day` 的 `adj_factor` 拒绝"算个替代值"，只接受权威真值 + provenance 标注）。

---

##### `dataasset.data.get` — 复合过滤（业务列 + 分区列范围，issue #68，2026-07-28）

**背景**：`dataasset.data.get` 底层对 MC（MaxCompute）分区表有一个守卫——只要请求里没有显式出现分区列（如 `fund_day` 的 `day_id`），后端会强行拼一个"最新分区"等值过滤，避免 ODPS 全表扫描报错。这个守卫本身不在本次改动范围内；本次新增的是**第二个过滤槽位**，让你能在一次调用里同时表达"业务列过滤 + 分区列范围"，从根源避开这个守卫（守卫只看过滤条件里有没有出现分区列名，不关心运算符——你自己带了范围过滤，守卫就不会再覆盖它）。

**第二过滤槽位参数**：`filter_column_2` / `filter_value_2` / `filter_op_2`（camelCase：`filterColumn2` / `filterValue2` / `filterOp2`），与主槽位 `filter_column` / `filter_value` / `filter_op` 参数形态完全一致、独立解析、用 AND 拼接。**不传时行为与之前完全一样**（不影响任何现有调用）。

**示例 —— 取基金 `510300` 在 2014 全年的历史净值序列（原始 bug #68 场景）：**

```bash
scripts/lg_agent_exec.sh dataasset.data.get id=76 \
  filter_column=fund_code filter_op=eq filter_value=510300 \
  filter_column_2=day_id filter_op_2=between filter_value_2=20140101,20141231 \
  size=500
```

不需要业务列过滤、只想拉某个分区范围内全部记录时，`between` 也可以只用主槽位、不需要第二槽位：

```bash
scripts/lg_agent_exec.sh dataasset.data.get id=76 \
  filter_column=day_id filter_op=between filter_value=20140101,20141231 size=500
```

**回测按年分块的使用指引（issue #68）**：对 MC 数据源支撑的分区资产（如 `fund_day`，assetId 76）做多年历史回测时，**不要**按天分块调用——十年历史按天拉需要约 **41 小时**（3650+ 次调用 × ~15-20s/次）。改为**按自然年分块**，用 `filter_op_2=between` 一年一次调用：`day_id BETWEEN 20140101 AND 20141231`，然后 `20150101 AND 20151231`，……。十年历史大约 **10-12 次调用**，每次 ~15-20s，总耗时约 **3-4 分钟**——比按天拉快两个数量级。客户端把每年返回的分页结果拼接起来即可得到完整序列。

`dataasset.data.getRealtime` 支持完全相同的第二过滤槽位 + `between` 运算符（走 PG 热窗口镜像，仅覆盖最近 365 天——超出该窗口的历史仍需用 `dataasset.data.get`）。

---

##### `dataasset.data.get` vs `dataasset.data.getRealtime` — 路由选择指南

> **用哪个？**
> - `dataasset.data.get` / `lg.get_asset_data` — 分析型 / 历史全量 / 完整数据。底层存储是资产的主数据源（Step 4 切换后为 MC；速度较慢 ~2-5s，但包含完整历史和全列）。
> - `dataasset.data.getRealtime` / `lg.get_asset_data_realtime` — 实时型 / 低延迟 / 热窗口（最近 365 天）。底层存储是资产的 `realtimeDataSource`（PG 镜像）。对于未配置 `realtimeDataSource` 的资产返回 `{success:false, message:"This asset has no realtime mirror"}` — 这是正常业务返回，不是异常，调用方应处理而非视为错误。

两个函数接受完全相同的参数（`asset_identifier, page, size, order_by, filter_column, filter_value, filter_operator`），返回 shape 相同，差异仅在于：
1. 路由目标不同（`/data` vs `/data-realtime`）。
2. `get_asset_data_realtime` **永不抛出异常**；所有错误（无镜像、类型不符、连接失败、认证失败）均以 `{success:false, message:...}` 返回，调用方 **必须** 检查 `result["success"]`。

> **Prerequisite**: `.getRealtime` requires the asset to have `realtimeDataSource` populated (via `PUT /api/data-assets/{id}`, an admin API). If not configured, `.getRealtime` returns `{success:false, message:"This asset has no realtime mirror"}`. Currently `stock_day` and `fund_day` are the only assets with realtime mirrors configured; other assets will return the "no mirror" response until an admin populates their `realtimeDataSource`.

> **Note for existing bearer token holders**: if you receive `403 Forbidden: missing required scope 'dataasset.data.getRealtime'` when calling this skill, your token was minted before this skill was added. Go to lg-data.cc → Token Management, edit your token, and add the `dataasset.data.getRealtime` scope. New tokens minted after 2026-07-02 automatically include all currently-registered scopes.

---

##### 场内基金（ETF/LOF）行情：`fund_quote_day` + `fund_kline`

两张表都是 PG 原生表（**不是** MaxCompute/ODPS），走 `dataasset.data.get` 的常规 PG 读路径——不受本节上方 MC-only 的「最新分区自动注入」与「`size>1000` 必须带 `order_by`」两条守卫约束（两条守卫的判定条件都显式检查 `connectionInfo.databaseType == odps`）。**当前 `allowSubscription=false`——本节只描述数据契约，不代表其它团队今天就能订阅这两张表。**

**`fund_quote_day`**（场内基金日线，PG 单表不分区）：

- `market` 列取值 `{ETF, LOF}`——**与 `fund_day.market` / `fund_codes.market` 的 `{E,O}` 是不同词表**，跨表 join 一律用 `fund_code`，不要用 `market` 做 join key。
- `turnover` 是**成交额**（元），不是换手率。
- `source` 区分两种写入来源：`akshare_hist_em`（官方历史收盘价，`is_final=true` / `calibration_status='confirmed'`）与 `fund_realtime_t0`（当日 T+0 推导值，`is_final=false` / `calibration_status='pending'`，最终会被官方值校准或在 5 次校准失败后标记 `abandoned`）。回测/长期分析优先用 `is_final=true` 的行。
- 主键 `(fund_code, day_id)`。

**`fund_kline`**（场内基金分钟 K 线，PG 原生 `RANGE (day_id)` 分区表）：

- `interval_type` ∈ `{1m, 5m, 15m, 30m, 60m}`——**没有 `1d`**，日线请用 `fund_quote_day`。
- `bar_time` 是 **VARCHAR(19)**（形如 `'2026-08-18 09:30:00'`），**不是 timestamp 类型**——不要对它调用 SQL 的 `to_char`/日期函数，会报类型错误；需要日期运算时先在客户端解析。
- **设计保留期为 3 天**（PG `RANGE (day_id)` 分区按日创建，由 proc 3389 Step 5d 按日龄丢弃超期分区，`FUND_KLINE_CUTOFF_DAYS=3`）。**该清理尚未真正执行过一次**——表 2026-08-18 才建立第一个分区，08-17 那次运行的 Step 5d 摘要是 `Age-eligible candidates: 0 / Dropped: 0`；且清理门控要求 MC 侧 `privora.fund_kline` 镜像存在才会真删（Phase 6 offload 未做，proc 3859 线上仅三步无 offload），门是 fail-safe 的，因此当前会一直 SKIP。**契约按 3 天规划，不要假设能稳定拉到更早的历史；但也不要假设旧分区此刻真的已被清理。**
- 每日典型 bar 数（ETF 众数，实测）：

  | `interval_type` | 每日典型 bar 数 | 备注 |
  |---|---|---|
  | `1m` | **237**（分布 232–239） | **不是 240**——源表并非每分钟都有 tick，缺口是正常现象不是缺陷 |
  | `5m` | 48 | — |
  | `15m` | 16 | — |
  | `30m` | 8 | — |
  | `60m` | **5**（hour-floor：09:00/10:00/11:00/13:00/14:00） | 与 `stock_kline` 一致，**不是**券商常见的 4 根 session-aligned 聚合 |

  收盘打点已钳制：不存在 `bar_time` 落在 `09:25–09:29` / `11:30` / `15:00` 的桶。
- `tick_count` 列量化该分钟内的真实采样笔数，用于判断稀疏度：**LOF 采样普遍稀疏**（覆盖率约 40%），`tick_count=1` 的 bar 必然 `open=high=low=close`——这代表"该分钟只采到一笔样本"，**不代表"该分钟无波动"**，不要把它当异常值剔除。
- `is_final=false` 是盘中快照（当日可被覆盖），`is_final=true` 是 T+1 `fund_kline_daily_sync` 定稿后的 bar（该 proc 会用 `fund_quote_day` 的收盘价回校当日最后一根 bar 的 close/high/low/volume/turnover）。**注意 `is_final=true` 目前只保证"来自已收盘并做过全天重算的源快照"，不保证"已与官方日线对账"**——对账要求 join 的 `fund_quote_day.is_final=true`（即官方值已校准），而截至目前该双源对账周期从未完整走通过（例如 2026-08-18 的全天重建摘要 `unreconciled_fund_codes: 1947`，覆盖当天全部场内基金，因上游校准源不可用导致 `fund_quote_day` 一直停在 `calibration_status='pending'`）。

**取数标准配方**：`dataasset.data.get` 只有两个过滤槽位（主槽位 + `filter_column_2`/`filter_value_2`/`filter_op_2` 第二槽位），无法同时对 `fund_code` + `interval_type` + `day_id` 三个谓词都做等值过滤。按需要哪两个维度精确定位来分配槽位：

- **某只基金某个周期的近几天全部 K 线**（不过滤 `day_id`——3 天保留期本身就是天然小结果集，`1m` 最多 ~3×237≈711 行，不会碰到 1000 行分页上限）：

  ```bash
  scripts/lg_agent_exec.sh dataasset.data.get id=<fund_kline的assetId> \
    filter_column=fund_code filter_op=eq filter_value=510300 \
    filter_column_2=interval_type filter_op_2=eq filter_value_2=1m \
    order_by=bar_time order_direction=desc size=800
  ```

  上例不带 `day_id`/`is_final` 过滤，会把当天尚未定稿的盘中数据与此前的历史 bar 一并按时间倒序捞出——需要严格区分「已定稿历史」与「当日快照」时，请在结果里按 `is_final` 或 `day_id` 分组，不要假设越靠前的行就是最终值。

- **某一天某个周期的全市场快照**（不过滤 `fund_code`——覆盖全市场 ~1950 只场内基金，`1m` 单日全量约 1950×237≈462,000 行，**必须**显式传 `order_by` 并分页拉取，一次 `size` 请求不到全量）：

  ```bash
  scripts/lg_agent_exec.sh dataasset.data.get id=<fund_kline的assetId> \
    filter_column=day_id filter_op=eq filter_value=20260818 \
    filter_column_2=interval_type filter_op_2=eq filter_value_2=1m \
    order_by=fund_code size=1000 page=1
  ```

  两张表尚未固定公开 `assetId`（当前 `allowSubscription=false`，尚未走公开发布流程）——与「快速接入」一节 Step 1 的惯例一致：**先 `dataasset.list` 按 `assetName=fund_kline` / `fund_quote_day` 查数字 id，不要硬编码猜测**。

---

##### `dataasset.history.field-as-of` — 股票 PIT 状态字段查询 (#13 PR-A/C)

路径：`GET /api/data-assets/history/field-as-of`

**Auth：** 标准 Spring Security session 或 Bearer token（`lgatk_…`）。GET 请求无需 CSRF token。Bearer token 需要 scope `dataasset.history.field-as-of`（PR-A 新增；现有 token 须重新签发方可使用）。

**依赖：** 底层表（`stock_st_history` / `stock_board_history` / `stock_delist_history` / `stock_industry_history`）由 PR-B ETL 进程回填。ETL 未运行前所有查询均返回 `data:null`，不会报错。

| 参数 | 类型 | 必填 | 说明 |
|---|---|:-:|---|
| `field` | String | 是 | 字段名，固定四选一：`is_st` / `market_board` / `delisted` / `industry` |
| `stockNum` | String | 是 | 股票代码，如 `600519.SH` / `00700.HK` |
| `asOfDate` | String | 是 | 查询日期，ISO-8601 格式 `YYYY-MM-DD` |
| `swVintage` | String | 否 | 仅 `field=industry` 时有效：`SW2014` 或 `SW2021`。缺省时自动按 `asOfDate` 选择（`asOfDate < 2021-10-01` → SW2014；否则 SW2021） |

**`field` 语义说明：**

| field | 返回类型 | 说明 |
|---|---|---|
| `is_st` | Boolean | `true` = ST/特别处理/暂停挂牌；`false` = 正常；`null` = 无历史记录（ETL 未回填或日期早于数据） |
| `market_board` | String | `主板` / `创业板` / `科创板` / `北交所` / `中小板`（v1 每日刷新，非事件驱动，精度至天）|
| `delisted` | Boolean | `true` = `delist_date <= asOfDate`；`false` = 未退市或无记录（默认 False，不返回 null）|
| `industry` | Object | 申万行业分类对象（见下方结构），`null` = 无记录 |

**`industry` 值对象结构：**

```json
{
  "l1_code":    "110000",
  "l1_name":    "食品饮料",
  "l2_code":    "110201",
  "l2_name":    "白酒",
  "sw_vintage": "SW2014"
}
```

**响应示例（field=is_st，股票在 ST 状态）：**

```json
{
  "success": true,
  "data": {
    "field":        "is_st",
    "stockNum":     "000666.SZ",
    "asOfDate":     "2022-06-01",
    "value":        true,
    "validFrom":    "2021-03-15",
    "validTo":      null,
    "source":       "namechange",
    "changeReason": "特别处理"
  },
  "message": "OK"
}
```

**响应示例（field=industry，自动选择 SW2014）：**

```json
{
  "success": true,
  "data": {
    "field":    "industry",
    "stockNum": "600519.SH",
    "asOfDate": "2020-06-15",
    "value": {
      "l1_code":    "110000",
      "l1_name":    "食品饮料",
      "l2_code":    "110201",
      "l2_name":    "白酒",
      "sw_vintage": "SW2014"
    },
    "validFrom": "2014-01-01",
    "validTo":   null,
    "source":    "index-member"
  },
  "message": "OK"
}
```

**无历史记录（ETL 未回填 / 日期早于数据）：**

```json
{
  "success": true,
  "data": null,
  "message": "No history record found for stockNum=600519.SH, field=is_st, asOfDate=2020-06-15. ETL may not yet have populated this field."
}
```

**业务错误（非法 field / 非法日期格式）：**

```json
{
  "success": false,
  "message": "Unsupported history field: 'foo'. Supported: [is_st, market_board, delisted, industry]"
}
```

**Python 快捷用法（via `lg_utils.history`）：**

```python
from datetime import date
from lg_utils.history import is_st_at, market_board_at, is_delisted_at, industry_at, load_st_history

# 单日点查
st      = is_st_at("000666.SZ", date(2022, 6, 1))           # True / False / None
board   = market_board_at("688001.SH", date(2022, 6, 1))    # "科创板" / None
delist  = is_delisted_at("000001.SZ", date(2023, 1, 1))     # True / False (never None)
ind     = industry_at("600519.SH", date(2020, 6, 15))       # dict with 5 keys / None

# 获取某股票全部 ST 历史事件列表（按 valid_from 升序）
events = load_st_history("000666.SZ")
# [{'valid_from': '2001-06-04', 'valid_to': '2001-09-18', 'is_st_value': True, ...}, ...]
```

`lg_utils.history` 模块通过 executor 内部 HTTP 调用同一个 REST endpoint，fail-soft 语义与 REST API 一致（无记录返回 `None`/`[]`，不抛异常）。

---

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
| `subscription.token.list` | GET | 列出订阅 token。**不在默认 `read-data` 预设里，预设场景按钮里也都没有它**——创建 token 时必须手动勾选这个 scope，或重新签发。 <!-- #988:not-in-default-preset --> | 🟢 |
| `marketplace.item.list` | GET | 列出可订阅的看板/资产 | 🟢 |
| `marketplace.item.subscribe` | POST | 订阅市场条目——**幂等**（`ON CONFLICT(item_code, team_name) DO UPDATE`，已订阅过再调一次同样成功）。响应体按 `itemId` 前缀带回订阅方**自己团队**的克隆 id：`asset-*` → `clonedAssetId`，`process-*` → `clonedProcessId`，`dashboard-*` → `clonedDashboardId`（见下方[场景 5](#场景-5一键-subscribealert-deeplink-new-v1013)）。这是拿"我自己团队里这份资产的数字 id 是多少"的最短路径，比 `dataasset.list` 扫 `tags` 少一次往返，见 Quick Start §0。**不在默认 `read-data` 预设里**——预设场景按钮里只有 `subscribe-and-read` 带它，创建 token 时请选这个预设（或手动勾选这个 scope）。 <!-- #988:not-in-default-preset --> | 🟡 |
| `marketplace.item.unsubscribe` | POST | 取消订阅。**不在默认 `read-data` 预设里**——预设场景按钮里只有 `subscribe-and-read` 带它,创建 token 时请选这个预设(或手动勾选这个 scope)。 <!-- #988:not-in-default-preset --> | 🟡 |

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

#### 反馈详情

##### `feedback.submit` — 提交反馈 / Bug 报告 / 功能需求

路径：`POST /api/feedback`

**必填字段：**

| 字段 | 类型 | 说明 |
|---|---|---|
| `category` | string | 反馈分类，严格枚举，见下方 |
| `subject` | string | 主题（最多 256 字符） |
| `message` | string | 详细描述 |

`category` 合法值（**严格匹配，不接受缩写**）：

```
bug_report | feature_request | general | other
```

> 注意：`"bug"`、`"feature"` 等缩写形式均为非法 category，接口将返回 HTTP 200 + `success:false`。

**可选字段：**

| 字段 | 类型 | 说明 |
|---|---|---|
| `contactEmail` | string | 联系邮箱（可选，最多 180 字符） |

**请求示例：**
```json
{
  "category": "bug_report",
  "subject": "数据资产列表加载失败",
  "message": "在工作区 A 下点击「数据资产」后页面空白，控制台显示 JSON.parse 报错。浏览器 Chrome 125，复现率 100%。",
  "contactEmail": "user@example.com"
}
```

**成功响应（HTTP 200）：**
```json
{
  "success": true,
  "message": "Feedback submitted"
}
```

**业务错误响应（HTTP 200 + `success:false`，category 非法示例）：**
```json
{
  "success": false,
  "message": "Invalid category"
}
```

**认证错误响应（HTTP 401，未登录）：**
```json
{
  "success": false,
  "message": "Authentication required"
}
```

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
| `investment.gold.portfolio.list` | GET | 查黄金持仓（query 传 `asset_class=gold`；`market` 取值 SGE/BANK；`stock_num` 取值为 SGE 规范码，2026-08-25 起共 10 个：`Au99.99` / `Au99.95` / `Au100g` / `Au(T+D)` / `mAu(T+D)` / `iAu99.99` / `iAu100g` / `iAu99.5` / `Ag99.99` / `Ag(T+D)`（即 `metal_codes` ∩ `metal_day`，全部 market=SGE；旧写法 `AuTD` 现规范化为 `Au(T+D)` 而非 `mAu(T+D)`）） | 🟢 |
| `investment.gold.portfolio.create` | POST | 新增黄金持仓（body 含 `asset_class: "gold"`） | 🟡 |
| `investment.gold.portfolio.update` | PUT | 更新黄金持仓 | 🟡 |
| `investment.gold.trading.list` | GET | 查黄金交易记录（query 传 `asset_class=gold`） | 🟢 |
| `investment.gold.trading.create` | POST | 录入新黄金交易（body 含 `asset_class: "gold"`） | 🟡 |

#### investment.paper.* — 模拟盘交易（Paper Trading，¥1,000,000 沙盘，2026-08-18 起支持多账户）

> ⚠️ **Paper-trading tokens are platform-issued, NOT self-mintable.** The `paper.*` scope namespace is reserved — calling `POST /api/subscription/tokens` with `scopes: "paper.account.read"` (etc.) returns HTTP 400 + `{"code":"RESERVED_SCOPE"}`. Paper-execution tokens are auto-minted by the platform when a strategy is bound to a paper account via the UI (`PaperExecutionTokenService.mintForExecution`). If you want to drive paper trading from an external agent, mint the token via the strategy-binding flow first, then call the endpoints below with that token.

> **新 v1.1**：单户模拟盘，行情打通 `stock_day` 实时价；MARKET 同步成交，LIMIT 走每 60s 撮合 + 15:00 自动 EXPIRED；T+1、一手 100 股、A 股标准手续费全部强制。**与真金账户完全隔离**——真金交易记录走 `investment.stock.trading.*`，二者数据库行级互不影响。

| skillId | method | 功能 | 风险 |
|---|---|---|---|
| `investment.paper.account.get` | GET | 查模拟账户当前状态：现金 / 初始资金 / 累计重置次数 / 总市值。首次调用 lazy-create 默认账户。**多账户（2026-08-18）**：可选 query `account_id=` 指定具体账户（含已归档），省略则解析为调用方的 DEFAULT 账户；不属于调用方的 account_id 一律 404 "Account not found"（不区分「存在但不是你的」与「根本不存在」） | 🟢 |
| `investment.paper.accounts.list` | GET | **新增（2026-08-18）**：列出调用方名下全部账户（含已归档），DEFAULT 账户排最前。用于发现 account.get / positions.list / orders.list 可传的 `account_id` 值——绑定到具名（非默认）账户的策略只能靠这个接口拿到自己的 accountId。复用 `paper.account.read` scope，能读默认账户的 token 无需额外授权即可调用 | 🟢 |
| `investment.paper.orders.submit` | POST | 下单：`{stock_num, market, side: BUY/SELL, order_type: MARKET/LIMIT, qty, limit_price?, client_order_id, account_id?}`。`client_order_id` 必传（同 user + 同 client_order_id 幂等）。MARKET 同步返回成交价；LIMIT 返回 SUBMITTED，撮合后由 scheduler 推到 FILLED/EXPIRED。**`account_id`（2026-08-18，实际受限）**：只有携带 `X-Agent-Mode:true` 但**不带** `X-Process-Execution-Id` 的调用（即非 Process 来源，`source=API/UI`）才能真正指向具名账户；只要请求同时带了这两个 header（`source=PROCESS`——**`lg.paper.*` Python SDK 的每一次调用都属于这一类**，因为 `_EXEC_ID` 来自调度器注入的 `execution_id` 作业变量），后端会把 account_id 强制钉死在 DEFAULT 账户，传其它值一律 HTTP 400 `"PROCESS-sourced orders must target the default account"`——即使那个账户确实是调用方自己的（`PaperTradingController.placeOrder` 的 LA REVISE v2 BLOCKER 3）。换言之：**Process Python 节点里的 `lg.paper.submit_order(account_id=...)` 今天对非默认账户必然失败**，该参数只对直接持 PAT 调 HTTP 接口（不带 execution-id header）的外部调用方有意义 | 🟡 |
| `investment.paper.orders.list` | GET | 查订单（支持 `status=` / `from=` / `to=` / `account_id=` 过滤，`account_id` 省略同样解析为 DEFAULT 账户，无 PROCESS 来源限制——与 orders.submit 不同）；返回字段含 `status / source / filledPrice / filledQty / fees / rejectReason` 等 | 🟢 |
| `investment.paper.positions.list` | GET | 查模拟持仓（只返 `account_id LIKE 'paper-%'` 的行，不会和真金混在一起）。可选 query `account_id=` 指定具体账户，省略则为 DEFAULT 账户，无 PROCESS 来源限制 | 🟢 |

**Scope 集（process-execution 默认）**：`paper.orders.write paper.account.read dataasset.read`。这是后端在 process 起跑时自动注入的 scope-limited 短期 Bearer。`investment.paper.accounts.list` 复用 `paper.account.read`，因此默认 process-execution token 已经具备列账户的能力，无需额外配置。

**Scope guard 边界**：带 paper scope 的 Bearer **只能**访问 `/api/wealth/paper/**`、`/api/data-assets/**`、`/api/auth/current`、`/api/public/agent/token-introspect`；其他 namespace（如 `/api/trading-records` 真金路径）一律 403 `scope_insufficient`。**`paper.*` 不可自助签发**——`POST /api/subscription/tokens` 传 `paper.*` scope 一律 `400 RESERVED_SCOPE`，个人设置 → Token 管理页面同理拒绝；外部 Agent 想拿到带 paper scope 的 Bearer，只能走上方「场景 6：模拟交易」一节描述的两条路（Process `python_script` 节点自动注入的短期 Bearer，或管理员按策略绑定流程手动铸的 process-execution token），**不存在自助签发这条路**。

**典型用法（在 Process Python 节点里跑量化策略）**：

```python
import lg

execution_id = lg.get_variable("execution_id")
quote_resp = lg.get_asset_data_realtime("stock_day",
    filter_column="stock_num", filter_value="600000",
    filter_operator="eq", size=1)
if not quote_resp["success"]:
    print(quote_resp["message"])
    return
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

**实时热窗口查询（`lg.get_asset_data_realtime`）**：

```python
# Real-time hot-window query (last 365 days, PG mirror, low-latency)
result = lg.get_asset_data_realtime(
    "stock_day",
    page=1, size=50,
    filter_column="day_id",
    filter_value="20260701",
    filter_op="eq",
    order_by="day_id",
    order_direction="desc",
)

if not result.get("success"):
    print(f"Realtime query failed: {result.get('message')}")
    # Common message: "This asset has no realtime mirror"
    # → Ask an admin to populate `realtimeDataSource` on the asset via
    # PUT /api/data-assets/{id}
else:
    rows = result["data"]
    total = result["totalElements"]
    print(f"Got {len(rows)} rows of {total} total")
```

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
| `lg.paper.submit_order(symbol, side, qty, order_type="MARKET", limit_price=None, client_order_id=None, market=None, asset_class=None, account_id=None)` | live + backtest | 见左 | `dict`。**两端共有**：`id`（**主键 — 不是 `orderId`**，两端一致）、`clientOrderId`、`stockNum`、`market`、`side`、`qty`、`orderType`、`limitPrice`、`assetClass`、`status`、`rejectReason`、`fees`、`filledQty`。**已成交价键名两端不一致**：backtest 用 `fillPrice`，live 用 `filledPrice`（pre-existing 命名分歧；agent 代码需做 `r.get("fillPrice") or r.get("filledPrice")` 兼容写法）。**时间戳键两端不同**：backtest 仅返回 `tradeDate`（推进到的模拟交易日）；live 额外返回 `submittedAt`/`filledAt`（PaperOrder 实体时间戳）但**不返回** `tradeDate`。**live 独有键**：`accountId`、`submittedAt`、`filledAt`、`source` — backtest 路径无此四键。 | `symbol` 推荐裸代码 + 显式 `market="SH"/"SZ"/"BJ"/"HK"`；带 `.SH/.SZ/.BJ/.HK` 后缀也接受（SDK 客户端 + 后端 `PaperOrderService.normalizeStockNum` 都会自动剥离 — Bug #51-A）。`client_order_id` 用作幂等键。`order_type="LIMIT"` 时 `limit_price` 必填。**`account_id`（2026-08-18，live 模式实际受限）**：省略/None ⇒ DEFAULT 账户（与旧行为字节级一致）。因为这个 SDK 恒定跑在 Process 执行里（`_EXEC_ID` 来自调度器注入的 `execution_id` 作业变量），后端恒把请求判为 `source=PROCESS`，而 PROCESS 来源的订单被硬性钉死在 DEFAULT 账户——传任何非默认 account_id 都会得到 HTTP 400 `"PROCESS-sourced orders must target the default account"`，哪怕那个账户确实归调用者所有。backtest 模式忽略该参数（单账户沙盘）。 |
| `lg.paper.get_account(account_id=None)` | live + backtest | 见左 | `dict`。**回测**：`{"initialCapital", "cashBalance", "positionValue", "totalEquity", "unrealizedPnl"}`。**live**：`{"id", "accountId", "displayName", "isDefault", "initialCapital", "cashBalance", "baseCurrency", "status", ...}` — 注意 live 路径**不返回** `positionValue` / `totalEquity` / `unrealizedPnl`（这些是模拟器进程内汇总，不是后端持久化字段）。 | 回测模式下来自模拟器持仓估值；live 模式查询后端 `/api/wealth/paper/account` → `PaperTradingController.toAccountMap()`。**`account_id`（2026-08-18 新增）**：省略/None ⇒ DEFAULT 账户；不属于调用方的 id 一律 404 "Account not found"。backtest 模式忽略该参数（单账户）。此函数**没有** submit_order 那条 PROCESS-来源限制——任何来源都能按 account_id 正常解析。 |
| `lg.paper.list_accounts()` | **live only** | `()` | `dict`：`{"items": [...], "total": N}`，每条 item 含 `accountId`、`displayName`、`isDefault`、`status`、`cashBalance`、`initialCapital` 等 | **2026-08-18 新增**。查询 `/api/wealth/paper/accounts`，用于发现自己名下所有账户的 `accountId`（尤其是具名/非默认账户 —没有别的方式能拿到自己的 accountId）。**backtest 模式调用会抛 `RuntimeError`**（模拟器恒为单账户，无可枚举对象）。 |
| `lg.paper.get_positions(account_id=None)` | live + backtest | 见左 | `dict`：`{"items": [...], "total": N}` | 每条 item 关键键名因模式**不完全统一**：**回测**返回 `{stockNum, qty, avgCost, lastBuyDate}`（精简）；**live** 返回 `{id, stockNum, market, stockName, assetClass, positionQty, avgCost, lastBuyDate, currency}`（包含 `positionQty` 而非 `qty`）。**`marketValue` / `unrealizedPnl` 两端都不返回** — 如需 market value / P&L 请自行用 `get_asset_data("stock_day", ...)` 的 `close_price` × `qty/positionQty` 算。两端通用 `stockNum`（camelCase）— **不是** `stock_num`。**`account_id`（2026-08-18 新增）**：同 `get_account`，无 PROCESS-来源限制；backtest 模式忽略。 |
| `lg.paper.get_orders(status=None, account_id=None)` | live + backtest | 见左 | `dict`：`{"items": [...], "total": N}` | `status` 可选过滤值：`SUBMITTED` / `FILLED` / `CANCELLED` / `REJECTED` / `EXPIRED`（5 个；`EXPIRED` 覆盖 DAY-TIF 限价单未触发收盘自动失效）。**不支持** `PARTIALLY_FILLED`（此后端未实现 partial fill 语义）。**`account_id`（2026-08-18 新增）**：同 `get_account`，无 PROCESS-来源限制；backtest 模式忽略。 |
| `lg.paper.cancel_order(order_id)` | live + backtest | `(order_id)` | `dict`（更新后的订单对象） | 已成交订单 422 拒绝。订单按全局唯一 `order_id` 寻址，不需要 `account_id`（跨用户/跨账户访问一律 403）。 |
| `lg.paper.advance_day(day)` | backtest only | `(day: str "YYYY-MM-DD")` | `None` | 推进模拟时钟到指定交易日；触发挂单成交评估、价格限制检查、T+1 规则。live 模式调用此函数会抛 `RuntimeError`（函数级文案，例如 `"advance_day() is only available in backtest mode (LG_PAPER_MODE=backtest). In live mode, the current day is inferred from the market calendar."`）。 |
| `lg.paper.record_eod_equity()` | backtest only | `()` | `None` | 在当前模拟日的收盘后调用，记录该日的 equity curve 点（用于 Sharpe / MaxDD 等指标聚合）。 |
| `lg.paper.persist_backtest(name=None, force=False)` | backtest only | `(name=None, force=False)` | `dict`：`{"id": int, "name": str}` — 仅 2 个 key | **必须显式调用** — 没有 `atexit` 隐式持久化（防异常中断写入半拉子结果）。`name=None` 时使用 `LG_PAPER_BACKTEST_PERSIST_NAME` env 或自动生成时间戳名。`force=True` 允许覆盖同名 result。metrics 不在返回里 — 需要 metrics 摘要请查 `process_backtest_result` 表或 `/profile/backtest-results` UI。 |

**回测模式完整脚本示范**（同一脚本与 live 模式只差三个 env var）：

> **Pattern note**: use `lg.get_asset_data` for backtest / historical-window loops (full history via MC after Step 4 flip); use `lg.get_asset_data_realtime` for live / paper-trade single-row lookups (hot 365-day window on PG). `.getRealtime` returns `success:false` on data older than 365 days — never use it inside backtest loops that may extend beyond a year.

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
| `lg_utils.get_asset_data(asset_identifier, page, size, order_by, filter_column, filter_value, filter_operator=None, filter_column_2=None, filter_value_2=None, filter_operator_2=None)` | 分页拉团队有权限的资产数据（历史全量，步骤 4 切换后走 MC）；返回 `{success, data, totalElements, totalPages, ...}`。`filter_value` 支持 list/tuple → IN 查询；`filter_operator` 支持 `eq / ne / in / not_in / like / gt / gte / lt / lte / contains / between`，默认 `contains`。`between` 需要恰好 2 个值（start, end，经同一 list/tuple→逗号拼接机制传入 `filter_value`），值数量不对或区间反转时后端 fail-loud 拒绝。**第二过滤槽位**（2026-07-28，issue #68 executor 侧 follow-up）：`filter_column_2`/`filter_value_2`/`filter_operator_2`，与主槽位参数形态完全一致、独立解析、AND 拼接；底层打 `GET /api/internal/asset-data/{assetId}`（`InternalPythonExecuteController`，本轮已加第二槽位参数透传）。典型用法是主槽位业务列等值过滤 + 第二槽位分区列 `between`（例如 `fund_code eq` + `day_id between`），避免触发 MC "最新分区" 自动注入 guard——一次调用即可拿到跨分区的完整历史区间，无需按天拆调用。三个新参数均可选，不传时行为与之前完全一样。失败时 **抛出 RuntimeError**。 |
| **`lg_utils.get_asset_data_realtime(asset_identifier, page, size, order_by, filter_column, filter_value, filter_operator=None, filter_column_2=None, filter_value_2=None, filter_operator_2=None)`** | 与 `get_asset_data` 参数完全相同（含 `between` 与第二过滤槽位）；内部走 `GET /api/internal/asset-data-realtime/{assetId}`，查询资产的 **实时镜像数据源**（PG 热窗口，最近 365 天）。**永不抛出异常**——所有错误（含无效 `between` 区间等业务校验错误）以 `{success:false, message:...}` 返回（无镜像 / MC 类型误配 / 连接失败 / 认证失败）；调用方须检查 `result["success"]`。适合仪表盘、实时 P&L 等低延迟场景。与 `dataasset.data.getRealtime` skill 对应。 |
| **`lg_utils.list_partitions(asset_identifier)`** ✨ NEW | 列出团队有权限资产的 MaxCompute 分区目录（`SHOW PARTITIONS`，仅元数据、不扫描数据）。对 `stock_day_v2` 这类表，一次调用 ~2.9s 拿回全部 21,885 条分区规格（同时带 `day_id` 与 `market`），替代"翻页读全表拼交易日历"的做法——后者对同一张表要 8,201 页 × ~31.7s ≈ 72 小时，且单页耗时会撞到本模块 `urlopen` 的 120s 超时（见 `docs/plans/2026-08-11-adj-factor-day-id-fetch-redesign.md` §4/§5）。**先校验白名单**（复用 `get_asset_data` 同一条 `_resolve_asset_id` 路径，只按 asset_name/asset_id 匹配，不接受裸物理表名）；底层打 `GET /api/internal/asset-partitions/{assetId}`。返回 `list[dict]`，一条分区对应一个 dict（列名→值，如 `{"day_id": "20260811", "market": "HK"}`），**不做分组/去重/排序**——按 market 取排序去重的 `day_id` 列表需调用方自己处理。仅对 MaxCompute 资产有意义；失败时 **抛出 RuntimeError**（含"该资产不是 MaxCompute 类型"）。 |
| **`lg_utils.list_partition_day_ids(asset_identifier, market=None)`** ✨ NEW | `list_partitions` 的薄封装（直接调用它，不是复制其逻辑，因此白名单校验/异常行为完全继承）：按 `market` 精确匹配过滤（不传则不过滤，返回所有 market 合并结果），提取 `day_id`，去重并**升序排序**返回 `list[str]`；无匹配结果时返回 `[]`（不是 `None`）。这就是 `stock_day_v2_hk_adj_factor_backfill/step1_sina_qfq_ingest.py` 里 `get_hk_trading_calendar` docstring 承诺的未来切换目标——`(market, ...) -> sorted list of day_id strings` 的同一契约；`list_partitions` 本身故意不做这层分组/去重/排序（多个 market 混在一起，`stock_day_v2` 全量 21,885 条里 HK 只占 ~5,977 条），这个封装才是调用方真正要用的入口。异常/校验规则与 `list_partitions` 完全一致（`PermissionError`/`RuntimeError`/`ValueError`）。 |
| `lg_utils.get_portfolio_positions(stock_num=None, page=1, size=500)` | 当前团队持仓（每行附带最新的一条 per-stock 推荐 `recommendation`，由内部 API 按 update_time 取最近） |
| **`lg_utils.get_trading_records(account_id=None, market=None, stock_num=None, trade_type=None, page=1, size=None, account_type=None)`** ✨ NEW | 拉团队的交易记录（分页 dict，字段 Jackson camelCase 如 `tradeDate / stockNum / tradeType`）。`account_type` 可选 `real`/`paper`/`all`（大小写不敏感）；**不传 = 不按账户类型过滤（真实+模拟都返回）**，不是 default 到 `real`——这一点与用户态 `/api/trading-records` 接口的默认语义不同。`size` **不传**时后端按自身默认（当前 50）取一页；若该团队匹配的总条数超过这一页能装下的数量，后端返回 `{success:false}` 业务错误（`RuntimeError`），而不是像 2026-08-18 之前那样静默截断——报错信息包含真实的 `totalElements`/`totalPages`，并点名要求显式传 `size=<n>`（feedback #71）。**显式传 `size`**（哪怕就是 `size=50`）完全维持之前的行为：不会触发上述报错，仍然会被 clamp 到 1000。失败（含上述业务错误）时**抛出 `RuntimeError`**，调用方需 try/except 或让异常向上冒泡。 |
| `lg_utils.write_recommendations(items, process_id=None, execution_id=None)` | Python 脚本把 per-stock 推荐（`action/priority/add1/add2/reduce1/reduce2/noMoreAdd/market`）**追加** 到 `process_stock_recommendation`（历史保留，不 upsert）；前端持仓页"推荐"按时间倒序展示历史 |
| `lg_utils.get_connection(ds_name)` / `get_db_config(ds_name)` | 按团队数据源名取 JDBC 连接 |
| **`lg_utils.backtest(strategy, asset, ...)`** | **单资产回测引擎**：long-only、整数股；输出 Sharpe / Sortino / MaxDD / 胜率 / profit_factor / 交易明细 / equity_curve / 年度拆分；可选 `benchmark_asset=` 对比并输出 alpha/beta；可选 `persist=True` 持久化到 `process_backtest_result` 表 |
| **`lg_utils.backtest_portfolio(strategies, assets, ...)`** ✨ NEW | **组合回测**：多标的共享现金池；额外输出 `per_asset` 贡献度/回撤；同样支持 benchmark / persist |
| **`lg_utils.write_backtest_result(result, name=...)`** ✨ NEW | 把 `BacktestResult` 持久化到 `process_backtest_result` 表（append-only，按团队隔离）。`BacktestResult.persist(name=...)` 是同义糖 |
| `lg_utils.log` 子模块 (`from lg_utils.log import info, warn, error`) | 标准化日志 helper：`info` → stdout，`warn` / `error` → stderr，自动加 `[INFO]/[WARN]/[ERROR]` 前缀。注意是子模块，不在 `lg_utils.__all__` 里，必须按子模块路径 import |
| `lg_utils.backtest_examples.dual_ma.DualMA` | 内置双均线参考策略 |
| `lg_utils.backtest_examples.stock_day.run_stock_day_backtest` | 针对平台 `stock_day` 日线表（`OPEN_PRICE/CLOSE_PRICE/day_id/STOCK_NUM`）的单股快捷封装 |
| `lg_utils.backtest_examples.stock_day.run_stock_day_portfolio_backtest` ✨ NEW | 多只股票组合的快捷封装 |
| **`lg_utils.backtest_examples.fund_day.run_fund_day_backtest`** ✨ NEW（反馈#64/#73 2026-08-18 订正：默认价格列改为 `adj_nav`，见下方专节） | 基金日线回测快捷封装。`fund_code` 作为 filter；`nav_date` (YYYY-MM-DD) 作为日期列。默认把 open/close 映射到 **`adj_nav`（复权净值）**，NOT `unit_nav`（单位净值，会被份额拆分/分红污染，不能直接当收益序列用）。`adj_nav` 约 49% 的行是 NULL——遇到"该 fund_code 某个真实交易日 adj_nav 为 NULL"时会直接 `RuntimeError` 报错并说明原因，**不会**静默退回 `unit_nav`。其余参数 (strategy / start / end / capital / benchmark_asset) 与 stock_day 同形。 |
| **`lg_utils.backtest_examples.metal_day.run_metal_day_backtest`** ✨ NEW | SGE 黄金/白银日线回测快捷封装。`metal_day.close_price` 同时映射到 open/close；`metal_code` 作为 filter。常用 metal_code: `Au99.99` (黄金 9999)、`Au100g` (黄金 100g)、`Ag(T+D)` (白银 T+D)。 |
| **`lg_utils.backtest_examples.hk_day.run_hk_day_backtest`** | 港股日线回测快捷封装。**底层是对物理 `stock_day` 表按 HK ticker 过滤**读取（港股数据现已作为独立 DataAsset `stock_day_hk` 🟢 生产可用发布，见「数据资产可用性」表）。结构同 `stock_day` 模板。 |

## 高级 / 兼容性附录

> 日常调用只需要上面 Quick Start 的 `key=value` 写法。这一节是给需要**手写 JSON envelope**、排查**参数没生效**、或给数组/嵌套 body 的少数几个 skill（`schedule.job.depends.save` / `.plugins.save` / `process.pipeline.build` / `.update`）用的参考。

### `lg_agent_exec.sh` 完整参数语法

```
lg_agent_exec.sh <skillId> [key=value ...] [key:=jsonvalue ...] [--json '<raw params json>']
lg_agent_exec.sh '<完整 envelope JSON>'          # 旧用法，仍 100% 支持
```

- **`key=value`** —— 一律当 **JSON 字符串**处理（保留 `stock_num=000135`、`day_id=20260419` 这类前导零；不要用 `key:=value` 传这些字段，会被解析成数字丢掉前导零）。
- **`key:=value`** —— 值按 **raw JSON** 解析（数字 / 布尔 / 数组 / 对象），例：`qty:=100`、`ok:=true`、`tags:=["a","b"]`。**解析失败直接报错退出**（非零 exit code + stderr 说明），不会静默退化成字符串——如果你想要的其实是字符串，改用 `key=value`。
- **`--json '<obj>'`** —— 给一个 JSON 对象当 params 的一部分，和 flat key 共存。多用于 body 是**数组/嵌套结构**的 skill（`schedule.job.depends.save`、`schedule.job.plugins.save`、`process.pipeline.build`、`process.pipeline.update`）：

  ```bash
  scripts/lg_agent_exec.sh schedule.job.depends.save jobCode=my_job \
    --json '{"body":[{"dependCode":"upstream_job","dependType":"10"}]}'
  ```

  `jobCode` 是 flat key（对应 path 模板 `{jobCode}`），`--json` 提供的 `body` 数组原样传递。**冲突时 `--json` 提供的字段优先**（同名 key 既在 `--json` 里又作为 flat key 传，`--json` 的值生效）。
- **Shell 引号提醒**：`--json` 的值本身是一段 JSON，请用**单引号**包裹整段（避免 shell 展开双引号内的 `$`/反引号）；JSON 内部的双引号无需在 shell 层再转义。数组/对象值同理。
- **旧用法完全兼容**：`lg_agent_exec.sh '<整坨 envelope JSON>'`（唯一一个参数、以 `{` 开头）按老路径直接透传，不受本次改动影响。

### `lg_agent_list.sh describe` — 查一个 skill 接受哪些 key

```bash
scripts/lg_agent_list.sh                       # 列出当前 token 可见的全部 skill
scripts/lg_agent_list.sh describe dataasset.data.get   # 只看这一个 skill 的 schema + 示例
```

响应 JSON 里每个 skill 都带 `params`（`{name, in, required, type, example?, aliases?}` 数组）和 `exampleInvocation`（一行可直接粘贴的 flat 调用示例）——这是**权威、随后端部署自动更新**的参数说明，比任何静态文档都新。

> **2026-08-03 起语义变更**：`GET /agent/skills`（含 `?skillId=` 的 describe 形态）默认返回**全量**目录，
> 不再按 granted scope 过滤。判断"能不能调"看每条的 `granted` 字段，**不要**再用"在不在列表里"来判断。
> 未授权的条目会额外带 `presetsGrantingScope`，告诉你加哪一组 scope 就能调。
> 要恢复旧的过滤行为传 `?granted=true`。匿名模式不受影响，仍然只返回白名单内的只读 skill。
> 执行授权没有变——`POST /agent/skills/execute` 仍然逐次校验 scope，看得见不等于调得动。

### Envelope 形式 & 历史踩坑（手写 JSON 时适用）

canonical envelope —— `params` 字段下嵌套 `pathParams` / `query` / `body`：

```json
{"skillId": "...", "params": {"pathParams": {...}, "query": {...}, "body": {...}}}
```

**向后兼容（自 2026-06-29 起）**：顶层 `pathParams` / `query` / `body` 会被网关自动折叠进 `params`（仅当 `params.<field>` 缺失时；非对象值跳过）。嵌套和顶层字段同时出现时，嵌套字段优先生效。

历史踩坑：2026-05-07 一次 backfill 因为漏写 `params:` 包裹（且当时 `body` 字段没有 fallback），`-target_day_id 20260506` 没到 broker，python_script 拿到 `target_day_id=None` 跑了一轮空 SELECT。2026-06-29 把 `query`/`body` 的 fallback 加齐；同期发现的 `dataasset.data.get` filter 被静默丢弃就是同源问题（用旧顶层 shape 时 filter 没注入 URL，看着 SUCCESS 但实际未过滤）。**v1.0.45 起推荐用 flat key 写法从根源避免这一整类踩坑**——flat key 由网关按 skill 的 path 模板自动分类，不存在"忘记包裹"的问题。

**`paramAliases`（2026-05-21 起）**：网关支持逐 skill 的 snake_case ↔ camelCase query 参数翻译。`dataasset.data.get` 是第一个开通的 skill（`filter_column` / `filter_value` / `filter_op` / `order_by` / `order_direction` 两种写法都接受）。触发原因是 LE 2026-05-21 晚间事故：`fund_day` 按 `007722` 过滤但静默返回未过滤数据（后端 `@RequestParam` 要 camelCase，agent 传了 snake_case，两边不匹配又没有报错）。flat key 写法同样受益于这层翻译——`filter_column=code` 这种 flat 调用会先分类进 `query`，再走 paramAliases 翻译，行为和手写 envelope 一致。

**v1.0.56 起：手写的 envelope（`lg_agent_exec.sh '<full request json>'`）和 `--json '<obj>'` 里不能含裸换行（CR/LF）。** flat key 写法不受影响（`json_escape` 内部已经把换行转成 `\n` 转义序列，产出的始终是单行 JSON）。这两条路径是把调用方原样字符串直接送进请求体的入口，请求体现在和 Bearer Token 一样走同一条 curl `-K -` 配置流发送，那条流是行分隔的，裸换行会被直接拒绝并报错（而不是尝试猜测怎么处理）——传格式化过（带缩进换行）的 JSON 前先 `tr -d '\n'` 压成单行即可。

## 环境要求

### 必需

- `LG_AGENT_BASE_URL` - 平台地址（默认 `https://privora.cn`）
- `LG_AGENT_TOKEN` - Bearer Token（公开版唯一认证方式；建议使用最小权限、专用 Token）

### 可选：自托管 / 自定义 host

**自 v1.0.55 起，`LG_AGENT_BASE_URL` 的 host 默认只接受官方域**（`privora.cn` / `www.privora.cn` / `lg-data.cc`）**和回环地址**（`localhost` / `127.0.0.1` / `[::1]`，用于本地联调）。如果你自托管了一份 `lg_web`、需要把 `LG_AGENT_BASE_URL` 指向自己的部署域名，必须额外声明：

```bash
export LG_AGENT_ALLOWED_HOSTS="my-lg.internal.example another.example"
```

- 空白分隔、可写多个 host；**精确匹配、大小写不敏感**（`My-Host.Example` 与 `my-host.example`等价）。
- **不支持通配**：`*`、`*.example.com`、空字符串一律视为无效并被拒绝——不会退化成"放行任意 host"。
- 不设置这个变量、又把 `LG_AGENT_BASE_URL` 指向非官方域时，`lg_agent_exec.sh` / `lg_agent_list.sh` / `lg_agent_approval.sh` 会在发出请求前直接拒绝，报错信息里会同时给出被拒的 host 和上面这行写法。
- **这是一处破坏性变更**：v1.0.54 及更早版本不做这层校验，任何语法合法的 https host 都会被放行。升级后若你的 Bearer Token 一直发往自托管域名，必须补上这个环境变量，否则会连不上。详见 [`CHANGELOG.md`](./CHANGELOG.md) 的 `v1.0.55` 条目。

## Security Notes

- 公开版 skill 仅支持 Bearer Token 模式，不接受会话 Cookie / CSRF。
- 首次安装建议使用测试账号或低权限 Token 验证读取类能力。
- 公开版 skill 覆盖数据查询 + 回测 + 模拟交易 + 告警 + 流程编排四大类，完整 per-category 分类（read / idempotent-write / workflow-transition / outbound-webhook）见 [§Scope](#scope--operator-responsibility)。**大部分**删除、撤销、审批等破坏性/管理类操作不在 skill 范围内，需通过 platform UI 完成；14 个标记 `confirmRequired:true` 的高风险操作例外，Bearer token 可达但必须先完成两步确认握手，见 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake)。管理员 approve/reject 陌生人发起的审批仍然不在 skill 范围内。
- 写操作应只授予明确需要的 scopes。
- 不要在脚本里硬编码 Token 凭据。

## 注意事项

- 公开版 skill 覆盖数据 + 回测 + 模拟交易 + 告警 + 流程编排；**大部分**破坏性/管理类操作（删除 / 撤销 / 审批）不在 skill 范围内，走 platform UI；14 个 `confirmRequired:true` 高风险操作例外，见 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake)。
- 公开版 helper scripts 只支持 Token 调用，不支持 session/cookie 兼容模式。
- `idempotencyKey` 用于幂等控制，写操作请保持稳定。
- Token 从平台获取，不要硬编码在脚本中。

---

## 最近更新

### v1.0.57 (2026-09-18)

- 🔌 **MCP server 新增 tool annotations + 第 12 个工具 `execute_confirm_required_skill`**（#1462 ① 路线，见 [`mcp-server/README.md`](../mcp-server/README.md) 与 `mcp-server/CHANGELOG.md` `0.1.2`）：`tools/list` 现在每个工具都带 `annotations`（10 个只读工具 `readOnlyHint:true`，新工具 `destructiveHint:true`）；`execute_skill` 对 `confirmRequired:true`（约 20 个，判定来自调用时对 catalog 的实时查询，不是静态清单）的 skillId 客户端侧拒绝，改指向新工具。annotations 是**披露，不是安全边界**——宿主可以忽略，真正的授权判定始终在服务端 scope 校验。本包自身的 REST/shell 路径不受影响。
- 🔒 **改掉一处比散文更强的过度声明——它是活的机器可读字段**：token 模式 409 响应的 `next` 字段此前写`"human-approves-then-resend-see-nextAction"`——但 `AgentApprovalService.selfConfirm()` 把 `approver_user` 设成**与 requester 同一个人**，同一个 agent 自己就能走完两步。已改为 `"self-confirm-or-await-admin-then-resend"`，下方 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake) 的示例同步更新。
- 📝 **《🛡️ Scope 与操作者责任》补一句「平台强制」的真实含义**：强制的是「两步」，不是「两个主体」——两步可以由同一个 agent 完成；要真正的人工把关，只有「不授予这些 scope」或「走平台 UI 由管理员 approve/reject」两条路。

### v1.0.56 (2026-09-18)

- **修复请求体临时文件暴露**（#1411）：`lg_agent_exec.sh` / `lg_agent_approval.sh` 不再把请求体写入临时文件（Windows/MSYS2 下该文件曾继承 `%TEMP%` 目录 ACL，任意本地用户可读）。请求体改为和 Bearer Token 走同一条 curl `-K -` 配置流发送，临时文件与其清理 trap 一并整体删除。
- **破坏性（仅限 loopback / 自托管直连场景）**：原始请求体约 77KB–256KB 这一段，走 loopback/自托管直连 Express 时不再能发送——详见上方"流程 (Process / Ingestion)"表格下方的载荷上限说明，以及 [`CHANGELOG.md`](./CHANGELOG.md) 的 `v1.0.56` 条目。公网 `privora.cn` 入口不受影响（那里 5–8KB 起就已 414）。
- 手写 envelope / `--json` 现在拒绝裸换行（见上方"Envelope 形式 & 历史踩坑"一节）。

### v1.0.55 (2026-09-15)

- 🔒⚠️ **破坏性变更：自定义 host 改为显式 opt-in**（ClawHub 复评从 `pass/clean` 掉到 `fail/suspicious`，扫描器点名 "permits arbitrary HTTPS credential recipients without an explicit custom-host opt-in"）。`scripts/lg_agent_exec.sh` / `scripts/lg_agent_list.sh` / `scripts/lg_agent_approval.sh` 的 `LG_AGENT_BASE_URL` host 校验，默认只接受官方域（`privora.cn`/`www.privora.cn`/`lg-data.cc`）+ 回环（`localhost`/`127.0.0.1`/`[::1]`）；新增 `LG_AGENT_ALLOWED_HOSTS`（空白分隔、精确匹配、大小写不敏感，**不支持通配**）用于追加自托管域名，见上方 [§可选：自托管 / 自定义 host](#可选自托管--自定义-host)。**自托管用户升级后若不设这个变量会连不上自己的部署**——这是已知且刻意的破坏，迁移只需加一行 env。随包带 `allowed-skills.txt` 的窄包（`privora-alert`）不受这个变量影响，仍只认官方域，行为不变。
- 📌 MCP server 走同一套凭据模型（`LG_AGENT_TOKEN` + `LG_AGENT_BASE_URL`）但校验逻辑独立，本次未同步加固，见 [`mcp-server/README.md`](../mcp-server/README.md) 的说明和 #1424。

### v1.0.54 (2026-09-15)

- 🔁 **Republish，覆盖三个从未发布的版本**：ClawHub 上线的仍是 `1.0.51`；`1.0.52`/`1.0.53` 都只在仓库 `SKILL.md` 里 bump 过 frontmatter，从未真正发布过。本次一次性把三版内容（见下方 `### v1.0.52`/`### v1.0.53`）连同这一版自己的改动一起发出去。
- 🔒 **随包脚本补上三处安全修复**（#1408、#1410，此前只发到过 `privora-alert` 的 1.0.5/1.0.6，一直没传导到本包）：`scripts/lg_agent_exec.sh` / `scripts/lg_agent_list.sh` 现在会校验 `LG_AGENT_BASE_URL`（拒绝非 http(s)、拒绝内嵌凭据、拒绝「明文 http + 非回环 host」——本包不带 `allowed-skills.txt`，不做官方域钉死，自托管不受影响）；默认域从 `lg-data.cc` 改为 `privora.cn`；凭据不再进 `curl` 的命令行参数（改走 `-K -` 配置流，并对写入该流的每个值做 CR/LF 拒绝与转义）；cleanup trap 不再重新解析 `TMPDIR` 派生路径。**未修**：请求体仍落盘，Windows/MSYS2 下仍继承目录 ACL（#1411，跟踪中，不在本次修复范围内）。
- 🛠️ **发布脚本 `publish.sh` 不再把 changelog 硬编码成 Bash 字符串字面量**：此前 `$CHANGELOG` 是冻结在 v1.0.49 文案上的一段字符串，四个版本（1.0.50-1.0.53）从未更新过——真正发布时会把描述别的版本的文案发到公开注册表。现在从新增的 `CHANGELOG.md` 顶部条目读取（`read_top_changelog_entry()`，同 `agent-skill-alert/publish.sh` 的形态），并加了字节长度预检（超过已验证可接受的上限就在 `--changelog-only` 阶段直接失败，不会发到一半才报错）。
- 📝 本节标题上方「最新版本」横幅不再写死具体版本号——之前的 `v1.0.45` 标注在文档里过了 9 个版本、两个月都没人更新，和上面的 changelog 硬编码是同一类缺陷。现在指向文件头 `version:` 字段 + `CHANGELOG.md` + 本节。

### v1.0.53 (2026-09-02)

- 🔌 **MCP server 章节把包名从占位符 `lg-agent-mcp-server` 改成实际认领的 `@privora/mcp-server`**（#1123/#1142）——npm 发布状态没变，仍然是**未发布**（`mcp-server/package.json` 仍是 `"private": true`），这次只是把文档里引用的包名和实际代码对齐。
- 🔒 **场景 → scope 速查表锁死到 `SCOPE_PRESETS`**（#1290），表格本身现在有机械化守卫（`test/skill-md-scope-preset-table.test.js`），防止再像 #1111 那样一次性漂移三处。`subscribe-and-read` 预设的表格行加粗标注**含写权限**：能订阅/取消订阅市场条目，**取消订阅会删除本团队的克隆副本**——不是纯只读。token 创建页的 wildcard（`*`）复选框现在有行内警告，说明勾了它就拿到包括 `paper.*` 在内的全部 scope 和所有需二次确认的破坏性操作。
- 📋 **`portfolio` 预设补上两个此前实际已经有、但表格没跟上的读 scope**：`investment.stock.watchlist.list`（#1307）和 `investment.stock.signal.{list,get}`（#1342）。都在既有 `portfolio` 预设内，没新增预设，也没加写权限。

### v1.0.52 (2026-09-02)

- 🔌 **新增「用 MCP 客户端？有原生通道，两条并存」一节**（#1140/#1141）：如果 Agent 走 Codex CLI / Claude Code / Cursor / Windsurf / Cline 等原生支持 MCP 的客户端，除了本包的环境变量 + 脚本方式，还有一个 stdio MCP server 把同一个 dispatcher 直接暴露成 MCP 工具——接口、环境变量、权限判定三处都和本包完全相同，只是换一层协议。⚠️ 当时还没发布到 npm，需要从仓库检出后用绝对路径接入，见仓库里的 `mcp-server/README.md`。

### v1.0.51 (2026-08-31)

- 🔒 **修正「Scope 与操作者责任」一节的不实声明**（ClawHub 机器扫描 v1.0.50 判 `suspicious / MEDIUM / score 45`，两处命中均锚定 :135-141）：原文声称"删除 / 撤销 / reset 操作"、"调度器 online/offline 状态转移"、"Webhook 插件生命周期变更"三类**不暴露**，但实际上前两类的一小撮操作经两步确认握手后对 Bearer token **可达**，第三类（`schedule.job.plugins.save`）则完全可达且**不经**确认握手（全量替换，旧绑定先删）。新增「确认门槛类」分类，把「不暴露」改写为「部分暴露」并逐条给出可达 / 不可达的真实边界，避免自动化审查系统把本 skill 误判得比实际更安全（Closes #1028, #1031；Related to #988, #989）。
- 🐛 **确认门槛技能计数 13 → 14**：`team.python.method.delete` 一直是 `confirmRequired:true` 且对 Bearer token 可达的技能，但四处计数（:523/:534/:1946/:1952）都还停在旧数字，且具名列表里没有它。已全部更正为 14 并补上该 skill id；新增回归测试（`test/agent-scope-presets.test.js`）把文档里这份具名列表和网关侧的可握手技能集合做相等性校验，防止两者再次静默漂移。
- 📝 **补齐 `team.python.method.*` 五个技能的文档**（此前全文 `team.python` 命中 0 处，整族未文档化）：新增「团队 Python 模块 (Team Python Methods)」小节，含 `list` / `get` / `create` / `update` / `delete`；`delete` 标注其真实不可逆语义——硬删（`repo.delete`，无软删除/版本历史），且从下一次 `python_script` 执行开始，依赖 `from team_lib.<name> import ...` 的脚本会 `ImportError`。
- 📝 **`schedule.job.plugins.save` / `schedule.job.depends.save` 行内补上"不经确认握手"的风险提示**：两者都是全量替换（旧的先删再写），传入数组即视为完整期望状态，遗漏的既有绑定/依赖会被静默清空——此前只在正文散文里各自提过一半，表格行本身没有这条警示。
- 📝 **新增「409 响应辨析」一节**（高风险操作确认握手小节内）：区分确认握手 409 里 `status`/`message` 各组合分别是"继续走握手"还是"调用方自身的 bug，重试无用"，并明确排除 session-only 的幂等冲突 409（`app.js:2854`，`mode !== 'token'` 门控）——对本 skill 的 Bearer token 使用者结构性不可达，是本 PR 不修的独立既有缺口。

### v1.0.50 (2026-08-27)

- 🐛 **修复 Quick Start §0 与 §4 First Call Recipe 自相矛盾，并纠正拿克隆资产 id 的优先路径**：§0 此前教用户"记下 numeric asset id"直接拿去调 §4 的 Bearer Token 接口——但 marketplace UI 上看到的 id 是**发布方团队的**，订阅后你自己团队会拿到一份**全新数字 id** 的克隆资产，拿发布方 id 去调自己的 Token 接口必然 404。修正后 §0 优先指向 `marketplace.item.subscribe`（`MarketplaceService.subscribe` 是 `ON CONFLICT(item_code, team_name) DO UPDATE`，幂等）响应体里的 `clonedAssetId`——**存量已订阅用户重复调用同一个 item 一样能拿到这个字段**，不是只有新订阅才有；`dataasset.list` + `tags` 含 `Subscribed` 扫描降级为兜底路径（响应丢字段，或不想再调一次 subscribe 时用）。§4 本身的教法（先 `dataasset.list` 按 assetName 查自己团队里的数字 id）一直是对的，没有改动核心步骤顺序。
- 🐛 **修复 §4 Step 2 在默认 token 上必然 403**：`dataasset.metadata.get` 不在 Token Management 页面 `read-data` 默认预设的 6 个 scope 里，照默认预设建 token 的人跑这一步必然 403。recipe 调整为 2 步核心（list → data.get，默认预设即可跑通）+ 1 步可选（metadata.get，原地注明需要额外勾选 scope），不再静默省略这个 skill。
- 🐛 **修复 `investment.paper.*` 一节自相矛盾的 token 指引**（:1700，ClawHub 扫描判 `DO_NOT_INSTALL` 的具名原因之一）：该行此前说"如需在自己的 PAT 上启用 paper 调用，去 个人设置 → Token 管理 创建一个带这套 scope 的长期 PAT"——与同一份文档 §场景 6（:506）和本节顶部警告（:1686）正相反：`paper.*` 是保留 scope 前缀，`AssetSubscriptionTokenService.rejectReservedScopes` 对任何 `paper.` 开头的 scope 无条件 `400 RESERVED_SCOPE`，个人设置页面同理拒绝，**没有自助签发这条路**。已改为与 :506/:1686 一致的说法，并指回「场景 6：模拟交易」一节而非重复第三遍。
- 📝 **`marketplace.item.subscribe` 补上 `clonedAssetId` / `clonedProcessId` 的说明**：此前只有 `clonedDashboardId`（v1.0.13）被文档化，`asset-*` / `process-*` item 拿自己团队克隆 id 的路径全文没有对应记载。现在这一 skillId 的目录行明确写出三种 `itemId` 前缀各自对应的响应字段，并指回 Quick Start §0。
- 🐛 **补齐 `dataasset.history.field-as-of`（:801）与 `dataasset.list`/`get`/`list.active`/`connection.test` 四个 `datasource.*` skill（:789-792）缺失的 scope 披露**：这几个 🟢/🟡 skill 都不在 `DEFAULT_TOKEN_SCOPES` 里，且此前在各自的目录行里零披露——`dataasset.history.field-as-of` 与 `dataasset.metadata.get` 挨着坐在同一张表，`datasource.*` 四行则紧邻 `dataasset.list`/`dataasset.get`（这两个才是真默认），都容易让人误以为"同表挨着的都在默认里"。已按 :798 的同一句式各自补上"不在默认 `read-data` 预设里"的说明。
- 🐛 **修复 §0 头条路径自己 403（LA 走 happy path 找出，本项工作里第 7 处同类缺陷、也是最重的一处）**：上一轮把 §0 改成"优先调 `marketplace.item.subscribe` 拿 `clonedAssetId`"，但没查这个 skill 本身的 scope 归属——`marketplace.item.subscribe` **不在 `DEFAULT_TOKEN_SCOPES`，也不在 `SCOPE_PRESETS` 六个预设场景按钮的任何一个里**（`lib/skill-catalog.js` 全文只在自己的 catalog 定义行出现一次）。一个在 `/profile/tokens` 点"创建"、什么都不改的新用户会在 §0 现在的头条步骤上直接 403。已在 §0（:209）和 `:1197` 的 catalog 行分别加注：创建 token 时必须手动勾选 `marketplace.item.subscribe` 这个 scope，六个预设按钮都不会自动带上它。**Update（2026-09-02，见 #1051 / `docs/plans/2026-09-01-agent-token-subscribe-preset.md`）：** 本条记录的是 2026-09-01 之前的状态，已不是现状——新增的 `subscribe-and-read` 预设（`SCOPE_PRESETS` 现为 7 个而非 6 个）现在就带这个 scope；创建 token 时选它即可，不再需要手动勾选。上面 §0 / `:1197` 两处的正文已同步更新，仅本条历史 changelog 保留原始措辞不改写。

### v1.0.49 (2026-08-18)

- 🔒 **文档化高风险操作两步确认握手**（issue #74 修复）：13 个 `confirmRequired:true` 的 Bearer-token 可达 skill（`process.ingestion.delete`、`schedule.job.{online,offline,delete}`、`schedule.instance.{redo,hold,kill,cancel,force_start,mark_success}`、`subscription.token.revoke`、`metric.alert.delete`、`investment.paper.account.reset`）此前从未文档化两步握手的真实请求形状，导致第一次调用返回 409 后无法完成第二步。新增 [§高风险操作确认握手](#高风险操作确认握手-confirm-handshake) 一节，含逐字请求/响应示例。真正的门槛是 `params.approvalId`（必须嵌套在 `params` 内，不能与 `skillId` 同级）——`confirm` 字段本身不产生任何效果，只是网关内部用于不让它泄漏到下游请求的保留字。409 响应现在额外带 `expiresAt`、`skillId`、结构化 `nextAction`（可直接拿来重发的完整请求体）。
- 🛠️ `scripts/lg_agent_approval.sh` 新增 `confirm` 动作（`POST /api/agent/approvals/{id}/confirm`），此前只有 `list-mine|list-all|approve|reject`——非管理员 token 调用 `approve` 必然 403（需要 `userLevel>=8`），而 `confirm` 才是 token 调用方本该走的自确认端点。
- 📝 `schedule.instance.redo` 的 `exampleInvocation` 移除了误导性的 `confirm=true`（该字段单独出现不会跳过确认握手）。

### v1.0.47 (2026-07-30)

- 🔗 「数据资产可用性」快照节 + Quick Start §0 各加一条指引：完整覆盖范围 / 分市场明细 / 更新频率 / 数据起始日期见持续维护的公开清单页 `privora.cn/features/realtime-minute-data-coverage`（按六类分组）。快照节本身标注为 2026-07-17 的一次性盘点，不再是权威口径。

### v1.0.46 (2026-07-17)

- 🌏 数据覆盖按市场段完整化：stock_day 段族全部 🟢 生产可用——A股 `stock_day`、港股 `stock_day_hk`、美股 `stock_day_us`（由 `stock_day_us_backfill_to_mc` PG→MC 同步）；分钟K线 `stock_kline`（A股）+ `stock_kline_hk`（港股）live；旧 `stock_minutes` 弃用。文档明确「物理合表、按市场段分别发布为独立 DataAsset」模型。

### v1.0.45 (2026-07-16)

- 🚀 **`lg_agent_exec.sh` 支持命名参数扁平调用**：`lg_agent_exec.sh dataasset.data.get id=42 filter_column=code filter_value=000135`，不用再手拼嵌套 envelope JSON。`key=value` 一律字符串（保留前导零）；`key:=value` 按 raw JSON 解析（数字/布尔/数组），解析失败 fail-loud。`--json '<obj>'` 支持数组/嵌套 body 的 skill（`schedule.job.depends.save` 等）与 flat key 混用。旧 envelope 形式 100% 继续可用，两种写法可在同一次调用里混用。
- 🔍 **discoverability**：`GET /agent/skills` 每个 skill 现在带 `params` schema（`{name,in,required,type,example?,aliases?}`）+ `exampleInvocation` 一行示例；`lg_agent_list.sh describe <skillId>` 只看一个 skill 的 schema。
- 📖 Quick Start / 典型场景示例全部改为新命名参数写法；envelope / fold-in / paramAliases 踩坑说明压缩进文末 [§高级 / 兼容性附录](#高级--兼容性附录)。

### v1.0.44 (2026-07-11)

- 🔄 内容 identical to v1.0.42（同 UX），v1.0.43 短暂回滚到 v1.0.40 SAFE 内容后发现 SkillSpector v2.3.5 在今天有 non-determinism，同 content 不同 scan 结果。既然 rollback 无法回 SAFE badge，选择保留 v1.0.42 的可读性改进（Chinese-fy Scope + What'''s-New 移底部 + marketplace §0）。

### v1.0.43 (2026-07-11)

- ⏪ 短暂 rollback 到 v1.0.40 内容尝试回 SAFE badge —— 失败（scanner non-determinism）。v1.0.44 恢复 v1.0.42 的可读性改进。

### v1.0.42 (2026-07-11)

- 📐 文档结构重组：4 个 What's-New 顶部块合并到本节；§Scope 与 §投资建议免责改为中文首要（不再中英双语介绍）。
- 🚀 Quick Start §0 30 秒试用改为指向 marketplace UI（无需注册直接浏览公开挂牌资产），移除 top-of-doc dispatcher endpoint 示例。

### v1.0.41 (2026-07-11)

- 🚀 首版 Quick Start §0 匿名试用（后在 v1.0.42 改为 marketplace UI 路径）。

### v1.0.40 (2026-07-10)

- 🔒 SkillSpector 响应：primary framing 从"金融数据后端"翻转到"AI Agent 投资工作流平台"；§2 加密段重写为"encryption at rest / 认证边界返明文"；删除 3 处矛盾的"只读能力与常规非破坏性写操作"声明。

### v1.0.38 (2026-07-10)

- 📖 Quick Start §4 加 First Call Recipe（3 步 curl：list → 拿 numeric id → data.get）说明 URL `{id}` 必须是数字型资产 ID（如 `42`），不是资产名字（如 `fund_day`）。

### v1.0.37 (2026-07-08)

- 🛡️ 匿名 rate limit 迁移到 Redis 集群共享：`10/IP/分钟 burst + 100/IP/天 daily` 承诺现在真的成立（v1.0.36 时因 PM2 cluster 被放大 ~4×）。Redis 断连时 fail-open。

### v1.0.36 (2026-07-08)

- 🌐 匿名 marketplace preview 模式全接入：`/agent/skills*` 无 `Authorization` header 自动进入 anonymous 模式，10 个只读 skill 白名单。三桶 rate limit（60/IP/分 general + 10/IP/分 data burst + 100/IP/天 data daily），任一超限 429 with `bucket` field。匿名调用强制 `page=1, size=25`，剥离发布者身份字段。

### v1.0.32 (2026-07-02)

- 📊 组合归因 (α/β)：新增 `investment.stock.portfolio.attribution.get`，跟基准做 TWR 对比。
- 📈 组合净值曲线：`portfolio.nav_history.get` 输出 NAV + 基准 overlay。
- 💰 现金分红归因：新增 `stock_dividend` 数据资产。
- 🧪 策略回测 sandbox 模式：`process.ingestion.execute --mode=backtest`。
- 🔔 告警治理 v1：`alert.snooze` / `alert.acknowledge` + Freemarker webhook 自定义 payload + 基于新鲜度的 stale 屏蔽。
- ⚡ 实时行情双路由：`dataasset.data.getRealtime` 新 skill。

### v1.0.35 (2026-07-03)

- 📝 **`dataasset.metadata.get` skill 注册**：Node `SKILL_CATALOG` 补录 `dataasset.metadata.get` 条目，覆盖 `GET /api/data-assets/{id}/metadata`（20 字段富元数据 + 新鲜度字段）。此前该 skill 在 `@RequireScope` 和 SKILL.md 均已存在，但 Node catalog 缺失导致 Agent 调用返回 HTTP 400 "Skill not found"。（feedback ID=61 gap 4）

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

**只想要"资产跌破/突破阈值就通知我"这一件事？** 本文档 97 个 skillId 里只有 20 个是这个场景需要的，别照单全收。场景化拆分版 **`privora-alert`** 把「建通道 → 建规则 → 验证 → 上线」11 步端到端流程压进一份 ≤340 行的文档：[clawhub.ai/guangfuwu/privora-alert](https://clawhub.ai/guangfuwu/privora-alert)。剩下的场景包（回测、模拟交易…）陆续拆分中，本文档在过渡期继续保留全量参考。

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
