---
name: huahua-daily
version: 4.1.14
description: 查询和分析花花日记中的基金持仓、行情、交易、量化与社区数据，并创建需要用户在 App 内确认的交易或批量导入请求。输入是本地图片、完整导出或大型文件时使用配套 huahua CLI。
---

# 花花日记 Agent 路由

花花日记后端是同步主数据、日期语义、权限、幂等和导入规范化的业务真相；现有组合读取仍保留 MCP 兼容适配层。MCP 用于小型结构化交互；CLI 只用于文件、完整导出和本地诊断。

## 运行模式

- 本地 stdio：Token 来自 `HUAHUA_AGENT_TOKEN`，可使用配套 CLI 处理本地文件。
- 官方远程 Streamable HTTP：连接 `https://mcp.huahuadaily.cn/mcp`，客户端发送
  `Authorization: Bearer <Agent Token>`；每个用户使用自己的 Token，远程工具面不暴露 `set_token`。
- 传输方式不会让 Prompt 自动进入模型。普通请求依据工具描述直接调用；复杂任务才用
  `get_skill_context(topic="portfolio")`、`date-safety`、`quant` 等按需加载一个主题。
  只有用户明确需要完整说明时才加载 `full`。
- `core` 是高频精简工具面，`full` 是完整能力；调用前以 manifest 返回的实际 profile 为准。

## 开始会话

首次接入、配置变更或排障时调用 `get_tool_manifest`，确认 profile、版本兼容、scope 和安全边界；普通会话不要重复调用。需要用户数据的工具必须有 Agent Token；不要索取、展示或复述完整 Token。

manifest 报告版本可更新时只提示用户，不自行安装或覆盖环境。按 `backendCompatibility.components` 分别判断：量化不兼容时停止量化写入，Agent 导入不兼容时停止新导入请求，并说明原因；不要让一个组件的版本差异误伤另一组件。

## 路由顺序

依次判断：

1. 用户要完成什么业务任务；
2. 输入是文字/结构化数据还是本地文件；
3. 结果是有界回答还是完整导出；
4. 操作是只读、创建 App 待确认请求，还是直接改变状态。

不要使用“能用 CLI 就优先 CLI”或“批量导入先截图识别”作为通用规则。

## 按意图读取说明

- 持仓、收益、同步状态、交易流水、分组或偏好：读取 [references/portfolio.md](references/portfolio.md)。
- 基金搜索、估值、画像、市场、指数、QDII 夜盘或交易日：读取 [references/fund-market.md](references/fund-market.md)。
- 买卖请求、批量导入、待处理请求：读取 [references/trade-import.md](references/trade-import.md)。
- 策略上下文、历史净值、组合回放、回测或快照：读取 [references/quant.md](references/quant.md)。
- 社区、JCTI 或个人报告：读取 [references/community-reports.md](references/community-reports.md)。
- 涉及收益日期、确认日、历史回放或副作用边界：读取 [references/date-safety.md](references/date-safety.md)。
- 本地截图、完整组合/净值导出、大型报告文件或诊断：读取 [references/cli-artifacts.md](references/cli-artifacts.md)。

只读取当前任务需要的 reference；不要为简单查询加载全部说明。

## 核心选路

| 用户任务 | 默认入口 | 首选能力 |
| --- | --- | --- |
| 今日收益、总资产、持仓明细 | MCP | `get_summary` / `get_records` |
| 综合持仓投资分析、今日操作建议 | MCP | `get_quant_strategy_context(view="compact")` 单次取齐；不要再串行重复查询持仓、市场和逐基金指标 |
| 基金和市场查询 | MCP | 搜索、估值、批量画像和市场聚合工具 |
| 单笔买入或卖出 | MCP | `request_transaction` |
| 文字、表格、JSON 批量记录 | MCP | `request_import_review` |
| 本地图片或截图 | CLI | `huahua import screenshots` |
| 完整同步数据或长历史导出 | CLI | `huahua export ...` |
| 量化分析和复盘 | MCP | compact、有界或分页工具 |
| 个人报告 | MCP；大型文件用 CLI | `submit_personal_strategy_report` / `huahua report submit` |

## 通用安全边界

- `request_transaction` 和 `request_import_review` 只创建 App 待确认请求，不直接交易或写入组合。
- 创建请求后明确告诉用户“尚未完成，需在花花日记 App 中确认”。
- Agent Token 只能把请求标记为 `DISMISSED`，不能标记为 `PROCESSED`。
- 写操作重试必须复用对应的 `client_request_id` 或 `client_message_id`。
- 不调用同步写入、历史恢复、管理员报告或未在 manifest 暴露的后端接口。
- 不根据不完整估值、缺失 G 日或 stale/timeout 帧把收益解释为真实零涨跌。
- 用户没有明确要求写入、关注、授权、归档或投递时，只执行读取和分析。

## 文件与上下文边界

- 不在对话、MCP 参数或中间文本中生成、复制、拆分或重组图片 Base64。
- 本地文件只能使用用户在当前请求中明确提供的路径；不得由 Agent 猜测、搜索或扫描路径。CLI 本身不扫描目录。
- 大型结果写入文件，模型只读取摘要或必要片段。
- MCP full 中的截图 Base64 工具只用于旧调用兼容，已弃用且不属于 core；新工作流不得选择它们。

## 回答要求

- 用户问“当前、最新、刚刷新、刚修改、是否已生效”时，必须在当前轮重新调用对应工具，不能复用此前轮次的工具结果。
- 数据响应含 `retryAfterMs` 且仍为 incomplete、stale 或 computing 时，按该间隔有界重取，最多 3 次；仍未完成则明确说明补数尚未完成，不循环等待。
- 区分官方净值、盘中估算和夜盘参考，不把估算描述成已确认收益。
- 涉及组合结论时检查返回中的 freshness、complete、readyForAnalysis 和 blockingReasons。
- 基金代码或名称存在歧义时轻确认，不猜测。
- 投资分析说明依据、数据截止时间和不确定性，不承诺收益。

## 常见失败

- 401：Token 无效或过期，请用户在 App 重新生成。
- 403：scope、会员等级或写入边界不满足；不要改用更宽接口绕过。
- 409：幂等 ID 与原意图冲突；不要用同一 ID 提交不同内容。
- 413/422：按错误提示缩小文件、条目数或日期范围，不静默截断。
- 行情或上游部分失败：保留可用结果并披露不完整项，不伪造缺失数据。
