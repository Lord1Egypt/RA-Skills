---
name: keep-query
description: Use when users want to query, view, check, or get statistics on their health data from Keep or Keep App, including exercise records, body measurements, health metrics, daily statistics, recent data, or historical trends. Prefer this skill for utterances like "查一下我这个月跑步的公里数", "我最近一次体重是多少", "上周运动总时长是多少", "最近的静息心率是多少", or "帮我看下4月每天的体脂率".
metadata:
  requires:
    mcp: "https://mcp.gotokeep.com/skills-mcp-gateway-page/v1"
  version: "1.0.5"
---

# Keep 数据查询工具

查询 Keep 运动品类记录、身体数据、健康数据的最近数据与统计。

## 何时必须调用

当用户在**查询、查看、统计自己的健康数据**时，优先调用本 Skill，不要先普通聊天，不要反问"要不要帮你查一下"，除非用户表达明显不想查询，或明显是在记录 / 求建议 / 闲聊。

**必定适用此 Skill 的场景**：

- 运动品类记录明细数据：如「查一下我这个月跑步的详情」「查询我本周的运动详情」「本月我的步行数多少」
- 运动品类统计数据：如「查一下我这个月跑步的公里数」「上周运动总时长是多少」「本年我运动了多长时间」
- 身体数据查询：如「我最近一次体重是多少」「帮我看下我的腰围是多少」「」
- 健康数据查询：如「我最近的饮食是什么」「我的睡眠时长是多少」「我的经期记录」

**不适用此 Skill**：

- 记录写入：如「帮我记到 Keep」「今天跑了 5km」「午餐吃了鸡胸肉」→ 交给 `keep-record`
- 提问或建议咨询：如「减脂期吃什么」「跑步配速多少合适」
- 闲聊：如「今天天气好」「帮我写周报」

**USE WHEN**：Keep, Keep App, 查询, 查一下, 看一下, 看看, 统计, 最近, 趋势, 历史, 总数, 总时长, 总公里, 几次, 多少次, 多少公里, 运动记录, 跑步记录, 骑行记录, 游泳记录, 体重查询, 体脂查询, 心率, 静息心率, 血压, 血氧, 步数, 每日统计, 每天, 这周, 这个月, 上周, 上个月, 最近一次, 最近体重, 最近体脂, 变化趋势, 运动总量, kg, 公斤, 斤, km, 公里, bpm, kcal, 千卡, 卡路里, mmHg。

**Triggers**：运动查询, 身体数据查询, 健康数据查询, 每日统计, 历史趋势, 最近数据.

## LOAD MODE
lazyLoad: false
preload: true

## Runner

本 Skill 面向 **OpenClaw / Hermes** 运行器，支持两种调用方式：

**方式 1 — exec（推荐）**：所有工具通过以下命令调用，调用约定见 [auth.md · exec 调用约定](references/auth.md#路径-b-调用约定mcp-calljs)：

```
node {baseDir}/scripts/mcp-call.js <tool> '<json>'
```

> **`{baseDir}` 占位符**：由运行器注入 Skill 的安装绝对路径。Agent 在 exec 命令里**保留字面 `{baseDir}`**，不要自己替换。

**方式 2 — 原生 MCP**：若运行器支持 streamable-http，可直接注册 MCP Server：

```json
{
  "mcpServers": {
    "keep-query": {
      "url": "https://mcp.gotokeep.com/skills-mcp-gateway-page/v1",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer ${env:keep_auth_token}"
      }
    }
  }
}
```

- 协议：JSON-RPC 2.0；`url` 只填根地址，**不要**拼接 `tools/call` / 工具名 / REST 子路径
- 运行器从环境变量读取 token 注入 HTTP header，Agent 不直接接触 token 值

## 处理流程

1. **确保已登录**：调用任何需登录工具前先检查本地凭证；无效则走 [鉴权流程](references/auth.md)。收到 `AUTH_REQUIRED` / `TOKEN_EXPIRED` 也要重登。
2. **调用 `query_tool`**：把用户原始查询原样作为 `text` 传入，**不要预分类**（不要自行拆分运动/身体/健康），由服务端识别数据域与统计口径；详见 [查询工具](references/query.md)。
3. **格式化结果**：按下方「结果呈现」给用户。

具体命令样例统一见下方 **Quick Recipes**。

## 登录顺畅性要求（OpenClaw / Hermes）

执行鉴权流程时按 [auth.md](references/auth.md) 的状态机推进，重点保证二维码可扫、跳转可点、上下文可续接：

1. `get_qrcode` 返回后，保存 `data.qrcodeId`。
2. 每次展示登录引导时必须同时给用户 `data.qrcodeUrl` 和 `data.redirectUrl`：
    - `data.qrcodeUrl`：渲染为 Markdown 图片，并附“二维码图片链接”纯文本。
    - `data.redirectUrl`：附“登录跳转链接”，用于二维码图片无法加载时点击打开。
3. 二维码消息必须包含兜底话术：**“扫码完成后，如果我没有自动继续，请回复「已完成扫码」，我会继续检查登录状态。”**
4. 优先执行 `login-wait.js <qrcodeId>` 自动等待；如果没有自动等待，用户回复「已完成扫码」后仍使用同一个 `qrcodeId` 检查状态。
5. 授权成功后执行 `persist_auth.js --token='<jwt>' --username='<name>'` 落盘，再继续原业务工具。

> 底线：不要让用户进入“被要求登录但没有可扫二维码 / 没有可点击跳转链接 / 没有下一步说明”的状态。二维码图片链接、登录跳转链接、下一步触发语和后续检查动作必须完整。

## 工具清单

由 MCP Server 的 `tools/list` 动态返回；下表是 Agent 首次使用前需要知道的骨架。**入参 / 返回字段 / 错误码以对应 reference 为准**。

| 工具 | 入参骨架 | 需登录 | 详见 |
|---|---|---|---|
| `get_qrcode` | `{ authType }` | 否 | [auth.md](references/auth.md#2-调用-get_qrcode) |
| `check_login` | `{ qrcodeId }` | 否 | 不要直接调；用 `scripts/login-wait.js`，详见 [auth.md](references/auth.md) |
| `revoke_auth` | `{}` | 是 | [revoke-auth.md](references/revoke-auth.md) |
| `query_tool` | `{ text }` | 是 | [query.md](references/query.md) |

## Quick Recipes

**Recipe 1 — 首次登录**：

```bash
node {baseDir}/scripts/mcp-call.js get_qrcode '{"authType":"openclaw"}'
# → OpenClaw Web / 聊天 UI 默认优先展示 data.qrcodeUrl（![](url) + 纯 URL）
#   若当前运行器是终端 / TUI，再补充 data.qrcodeAscii 原样打印到 stderr 作为兜底
#   详见 references/auth.md「展示策略」
node {baseDir}/scripts/login-wait.js <qrcodeId>
node {baseDir}/scripts/persist_auth.js --token='<jwt>' --username='<name>'
```

**Recipe 2 — 查询数据**：

```bash
node {baseDir}/scripts/mcp-call.js query_tool '{"text":"查一下我这个月每天跑步的公里数"}'
```

**Recipe 3 — 退出登录**：

```bash
node {baseDir}/scripts/mcp-call.js revoke_auth '{}'      # tools/list 未返回则跳过本步
node {baseDir}/scripts/persist_auth.js --clear
```

## 结果呈现

Agent 不应编造缺失数据，也不应自行计算未由上游返回的统计值。上游返回内容作为事实来源。

- **优先展示返回内容**：如果上游有返回内容，则展示完整的上游返回内容
- **空结果**：说明没有查到对应数据，并提示用户换一个时间范围或数据类型
- **错误**：保留可行动提示，例如稍后重试或重新登录
- **不要主动引导分析**：默认只做结果呈现，不主动提出“是否需要我帮你分析”“是否要进一步解读趋势”“我可以基于这些数据给你建议”等引导语。
- **不要扩展解释与统计**：不要基于返回数据自行延伸出趋势判断、健康建议、数据统计、扩展统计或原因推测。
- **分析诉求转 Keep App**：当用户明确提出“分析运动数据”“分析身体数据”“给出建议”等分析型请求时，不在当前 Skill 内做分析；仅说明当前 Skill 负责数据查询与展示，并引导用户前往 Keep App 使用相关分析能力。


## 通用错误码

仅列跨工具的通用错误。**业务错误码（登录类）见对应 reference**：

| 错误码 | 含义 | 应对 |
|---|---|---|
| `AUTH_REQUIRED` | 未登录 / token 非法 | 走 [鉴权流程](references/auth.md) |
| `TOKEN_EXPIRED` | 登录过期 | 走 [鉴权流程](references/auth.md) |
| `RATE_LIMITED` | 请求过频 | 等待 `retry_after` 秒后重试 |
| `UPSTREAM_ERROR` | Keep 服务异常 | 提示稍后重试 |
| `INVALID_ARGS` | `mcp-call.js` 用法错误（退出码 2） | 检查 `<tool_name>` 与 JSON 参数；`--list` 查工具 |

按工具的细分错误码：

- 登录 / 二维码相关：见 [auth.md · 鉴权 / 登录相关错误码](references/auth.md#鉴权--登录相关错误码)
