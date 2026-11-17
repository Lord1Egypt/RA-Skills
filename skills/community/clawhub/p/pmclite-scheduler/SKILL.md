---
name: pmclite-scheduler@zhengjinfa33
description: |
  通过 MCP 工具操作轻排桌面程序（MRP-PMC），完成生产排产、排程预演与落库、交期评审、插单评估、物料齐套检查、报工与生产看板查询。
  用户说出“帮我排产”“排一下明天的产”“这单能不能接”“交期来得及吗”“查一下工单”“齐套了吗”“缺什么料”“插个单行不行”“报工 50 件”“今天生产怎么样”“最近有哪些异常”时使用。
  不触发：新建物料/产品/BOM 等基础资料录入、财务报表、采购下单、与轻排程序无关的通用排产理论问答。

metadata:
  dumate:
    displayName: "轻排生产排产"
    summary: "驱动轻排 MRP-PMC 桌面程序完成工单排程、交期评审、插单评估与物料齐套检查；排程结果可解释、可复现，写库前必须经用户确认。"
    publisher: "广州轻排信息科技有限公司"
    icon: "assets/icon.png"
    publishedAt: 1794321600000
    version: "1.1.0"
    level: L2
    category: 生产制造
    tags: ["排产", "PMC", "齐套", "交期", "报工"]
    sensitive: false
    allow_implicit_invocation: true
---

# 轻排生产排产（pmclite-scheduler）

本技能通过 15 个 MCP 工具操作轻排桌面程序 MRP-PMC。**所有排程口径以本文为准，不要凭直觉解释排程结果。**

## 前置条件

- 用户本机需安装轻排桌面程序 **MRP-PMC**（开发商：广州轻排信息科技有限公司），并已接入 MCP（本地 stdio 通道）。
- 全部业务数据存储于用户本机加密数据库，本技能不向任何第三方服务器传输数据。
- 官方下载渠道：**https://www.pmclite.com**（唯一下载入口），安装与接入步骤见 `references/install.md`，接入模板见 `assets/mcp.json`。

## 执行指令

### 步骤 1 - 探测连接

先调用 `get_dashboard(scope="today")` 探测 pmclite 是否可用。

- 调用成功 → 进入步骤 2。
- 报“工具不存在 / 连接失败 / MCP 未连接” → 进入「未安装引导」，并按 `block` 策略停止业务操作。

### 步骤 2 - 确认业务对象

用户未说明工单号、产品、数量或日期时，先追问，不要猜：

- 排产类：问清范围（全部待排产 / 指定工单）
- 评审类：问清新单的产品、数量、期望交期
- 报工类：问清工单、工序或数量、工时

### 步骤 3 - 只读操作直接执行

以下工具只读、无副作用，可直接调用，不必逐次确认：
`get_dashboard`、`query_work_orders`、`query_master_data`、`query_records`、`estimate_hours`、`preview_schedule`、`evaluate_order`、`assess_insertion`、`check_readiness`。

### 步骤 4 - 写操作必须先确认（强制）

以下工具会落库，**执行前必须用一句话复述将写入的内容，并等待用户明确回复确认**：
`apply_schedule`、`reschedule_from_actuals`、`report_progress`、`report_incident`、`import_data`。

复述格式示例：

> 即将写入：WO-001 排到 SMT产线A，2026-11-10 → 2026-11-19（50 件，工时模型 batch 串行）。确认执行？

- 用户确认 → 执行；
- 用户拒绝或修改 → 不执行，按用户意见调整后重新确认；
- 用户未回复 → 不执行，不要默认同意。

### 步骤 5 - 输出格式

排产结果用表格：

| 工单 | 产品 | 数量 | 产线 | 起止 | 工时模型 | 结论 |

风险结论用分档表述（🔴 阻断 / 🟡 需关注 / 🟢 可执行），最后给出 1–3 条按优先级排序的具体动作，并注明每条动作责任方（销售 / 生产计划 / 采购 / 车间）。

## 排程核心口径（必读）

1. **三入口同源**：`preview_schedule` / `apply_schedule` / `reschedule_from_actuals` 复用同一排程引擎，对同一张工单给出一致结果。预演不落库，`apply_schedule` 才写入。
2. **默认串行模式**：一条产线同一天只归属一张工单（`pmcSettings.allowMixedLine=false`）。产线当天已被占用 → 整段顺延到下一个空档，**不会**与其他工单共用产线。两张工单被排到不同产线是串行模式的正常结果，不是错误。
3. **flowType 决定工时模型**：
   - `flow`（流转生产）：首件 + (N-1)×瓶颈节拍，工序重叠，工时远小于串行累加；
   - `batch`（批次生产）：各工序串行累加；
   - **flow 产品落到并行工位≤1 的产线 → 自动降级为 batch**（`hoursModel=batch_serial_downgraded`，附 `downgradeNote`）。同一张单从“3 天”变“106 天”是降级生效，不是计算错误——必须把差异原因讲给用户。
4. **产线解析优先级**：工序显式指定 > 工序 workCenter（须已配置产线详情）> 工单 assignedLine > 第一条产线。
5. **单张重排不感知队列**：`reschedule_from_actuals(work_order=X)` 只保证 X 自身合理（已完成工序钉住，剩余工时按占比摊开），**不考虑其他待排产工单对产线的占用**。单张重排后必须再跑一次全量 `preview_schedule` 核对；若其他单被挤到不合理产线，用 `apply_schedule` 重排。
6. **没有独立的冲突检测工具**：资源冲突体现在 `preview_schedule` 返回的产线分配与日历占用中——若出现同产线时间重叠，或某单被挤到非预期产线，必须主动向用户指出。

## 工具清单

| 工具 | 用途 | 口径要点 |
|------|------|----------|
| `preview_schedule` | 排程预演（不落库） | 全量排会避开已有占用；结果确认后用 apply_schedule 写入 |
| `apply_schedule` | 排程落库 | 可传 preview 结果或内部自动排 |
| `reschedule_from_actuals` | 已报工工单滚动重排 | 单张语义，见口径 5；重排后跑全量 preview 核对 |
| `estimate_hours` | 工时估算 | scope=work_order 时 line 参数生效；输出 lineSource/hoursModel |
| `evaluate_order` | 交期评审 | 新订单能不能接，返回红/黄/绿档位 |
| `assess_insertion` | 插单评估 | work_order 与 product 二选一，同时传会报错 |
| `check_readiness` | 物料齐套检查 | 支持工序级齐套 |
| `query_work_orders` | 查工单 | include=["kit"] 附带齐套结论 |
| `query_master_data` | 查产品/物料/销售订单 | entity 必填；产品详情可带 bom/routing |
| `query_records` | 查异常/报工记录 | type=incident 时用 incident_type 过滤 |
| `get_dashboard` | 生产看板 | scope=today/kpi/labor/all |
| `report_progress` | 报工 | 末道工序报满自动完成工单 |
| `report_incident` | 上报异常 | 缺料/故障/质量 |
| `get_import_schema` / `import_data` | 批量导入 | 先取 schema 再按 schema 组织数据 |

## 降级策略

| 场景 | 策略 | 具体处理 |
|------|------|----------|
| 全部工具不可用（未装程序 / MCP 未连接） | `block` | 停止业务操作，按下方「未安装引导」处理，不猜测、不伪造数据 |
| 部分工具不可用（如 `check_readiness` 报产线未配置） | `partial` | 改用 `query_work_orders(include=["kit"])` 拿齐套结论，在输出中注明“来源降级”与缺失项 |
| `preview_schedule` 失败但查询正常 | `degrade` | 只做数据核对与现状说明，**不给日期结论**，明确告知“本次未完成排程计算” |
| 写操作失败 / 鉴权失败 | `block` | 不重试、不声称成功，说明失败原因并提示用户处理后再试 |
| 用户拒绝写操作 | 不执行 | 保留已完成的分析结果，等待新的指令 |

## 未安装引导（合规，必须遵守）

判定：pmclite 工具不可用，或调用任一工具报连接错误 / 工具不存在。

1. 告知用户：本技能需要本机安装轻排桌面程序 MRP-PMC（开发商：**广州轻排信息科技有限公司**）。
2. 引导访问**唯一官方下载渠道**：**https://www.pmclite.com**。
3. 提醒用户认准官网域名 pmclite.com，**不要从第三方下载站或他人单独发来的文件安装**。
4. 安装完成后，按 `assets/mcp.json` 模板接入 MCP，详细步骤见 `references/install.md`。
5. 用户在 MCP 客户端信任 pmclite 服务后，重新调用工具验证（`tools/list` 应返回 15 个工具）。

**红线**：禁止在对话中直接传输安装包文件；禁止提供 pmclite.com 以外的任何下载链接或网盘地址；禁止代替用户执行安装、授权或信任操作；不夸大软件能力与承诺。

## 示例

**示例 1（主流程 · 排产预演 → 确认 → 落库）**

用户：帮我排一下明天要干的单。

DuMate：
先查待排产工单（`query_work_orders`），再跑 `preview_schedule`，然后回答：

| 工单 | 产品 | 数量 | 产线 | 起止 | 工时模型 | 结论 |
|---|---|---|---|---|---|---|
| WO-001 | 智能手表 | 50 | SMT产线A | 11-10 → 11-19 | batch 串行 | 🟡 料未齐 |

🔴 阻断：WO-001 缺半成品 SUB-001 50 套（库存 0），需先补产半成品工单，否则明天开不了工。
🟡 关注：flow 产品落在 1 工位产线，已按 batch 串行降级估算（50h），比 flow 模型更保守。
建议：① 生产计划 今日补建 SUB-001 工单；② 补齐后重跑预演；③ 确认后落库。

即将写入：WO-001 排到 SMT产线A，2026-11-10 → 2026-11-19。确认执行？

**示例 2（边界 · 不应触发）**

用户：帮我在轻排里新建一个产品 BOM。
DuMate：这属于基础资料录入，超出本技能范围（本技能只做排产、评审、齐套、报工）。请在轻排桌面端「产品 → BOM」中维护，或提供 Excel 由导入工具批量导入。

**示例 3（降级 · 工具不可用）**

用户：排一下明天的产。
DuMate：当前无法连接轻排（本机未安装 MRP-PMC 或 MCP 未授权），本次不做排程推算，避免给出不可靠的日期。请先到官网 https://www.pmclite.com 下载安装，并按 `references/install.md` 接入后我再执行。

## 解释结果时的禁区

- 不要把串行模式下“两单分到不同产线”解释为异常；
- 不要把 `batch_serial_downgraded` 解释为计算错误——它是 flow 模型在单工位产线上的正确降级；
- 不要把 flow 产品的工序工时直接相加（flow 是重叠模型，相加会翻倍以上）；
- 单张 reschedule 之后，不要声称“全厂排程已最优”——其他单的占用没有被重新计算；
- 不要在没有工具返回数据时编造工单号、数量、日期或 KPI。

## 企业与支持

- 开发商：广州轻排信息科技有限公司
- 官网：https://www.pmclite.com（软件下载、文档与支持的唯一官方入口）
- 数据说明：生产业务数据全部存储于用户本机，技能通过本地 MCP stdio 通道与程序通信，不经过第三方服务器。
