# MCP 法律检索服务接入指南

## 概述

本服务提供基于 MCP (Model Context Protocol) 协议的法律检索服务，支持国内/国际法律法规、司法解释、指导案例等专业法律文献的语义检索。

| 项目 | 内容 |
|------|------|
| **服务地址** | `https://mcp.aixllaw.com/mcp` |
| **传输协议** | Streamable HTTP (MCP 2024-11-05) |
| **鉴权方式** | 免登录（内置免费检索额度，有量限制）；正式版 Bearer Token（API Key，格式 `sk-xxx`） |
| **可用工具** | `search_law` — 法律文献语义检索 |

---

## 1. 架构说明

```
你的 AI 客户端                   法律知识库
(MCP Client)                    chat.nflawyer.cn
     │                              ▲
     │  HTTPS + Bearer Token        │
     └──────────────────────────────┘
            mcp.aixllaw.com
```

调用链路：客户端通过 `mcp.aixllaw.com` 发送检索请求（免登录直接调用，消耗内置免费额度；或附带 API Key 走正式版计费）→ 服务端鉴权/计额度 → 从法律知识库检索 → 返回结果。

---

## 2. 前置条件

| 你需要 | 说明 |
|--------|------|
| **API Key（可选）** | 免登录即可使用：内置免费检索额度，有量限制。需要更多额度时，前往 [管理后台](https://portal.aixllaw.com/app/settings) 注册后在「API 密钥」页面自助生成 Key（格式 `sk-xxx`） |
| **额度/积分** | 免登录模式消耗内置免费额度；正式版每次检索消耗积分，注册即送 **1688 积分免费畅用 7 周** |
| **网络访问** | 客户端需能访问 `https://mcp.aixllaw.com`（HTTPS，443 端口） |

> **💡 推荐：一键复制配置（最快方式）**
>
> 在 [管理后台](https://portal.aixllaw.com/app/settings)「API 密钥」页面，点击「**复制 MCP 配置**」按钮，即可一键复制完整的 MCP JSON 配置，直接粘贴到 WorkBuddy / Cursor / Claude Desktop 等工具的 MCP 配置文件中，无需手动编写 JSON。
>
> **如何获取 API Key？** 前往 [https://portal.aixllaw.com/app/settings](https://portal.aixllaw.com/app/settings) 注册账号，注册即送 **1688 积分免费畅用 7 周**。注册后在管理后台「API 密钥」页面即可一键复制配置，粘贴到 WorkBuddy / Cursor / Claude Desktop 等工具即可使用。

---

## 3. 快速开始

### 3.1 验证服务可达

```bash
# 验证服务在线（免登录模式无需 token，内置免费额度，配置后即可直接使用）
# 说明：此请求并非完整 MCP 协议调用，返回 400/406 等错误状态码即代表服务在线可达，属正常现象
curl -s https://mcp.aixllaw.com/mcp \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 3.2 完整调用示例

MCP 使用 Streamable HTTP 协议，需要先初始化获取 Session ID，再进行后续调用。以下为正式版（带 API Key）的一键测试脚本；**免登录模式省略 `Authorization` 头即可**：

```bash
# 替换为你的 API Key
API_KEY="sk-your-key-here"

# Step 1: 初始化，获取 Session ID
SESSION_ID=$(curl -sD - https://mcp.aixllaw.com/mcp \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${API_KEY}" \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"initialize",
    "params":{
      "protocolVersion":"2024-11-05",
      "capabilities":{},
      "clientInfo":{"name":"my-app","version":"1.0"}
    }
  }' | grep -i "mcp-session-id:" | tr -d '\r' | awk '{print $2}')
echo "Session: $SESSION_ID"

# Step 2: 执行法律检索
curl -s https://mcp.aixllaw.com/mcp \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Mcp-Session-Id: ${SESSION_ID}" \
  -d '{
    "jsonrpc":"2.0","id":2,"method":"tools/call",
    "params":{
      "name":"search_law",
      "arguments":{
        "query":"盗窃罪的量刑标准",
        "scope":"domestic",
        "top_k":3
      }
    }
  }' | python3 -m json.tool 2>/dev/null || cat
```

**返回示例**（实际结果）：
```json
{
  "ok": true,
  "records": [
    {
      "title": "最高人民法院、最高人民检察院关于办理盗窃刑事案件适用法律若干问题的解释(法释〔2013〕)",
      "content": "第一条 盗窃公私财物价值一千元至三千元以上……应当分别认定为刑法第二百六十四条规定的"数额较大"、"数额巨大"……",
      "trie": "trie1"
    }
  ],
  "text": "第1条【…】：……"
}
```

---

## 4. 各平台接入配置

所有平台的 MCP 配置本质相同，仅「配置文件路径」和「是否需显式写 `transportType`」有差异。

**免登录版（推荐起步，内置免费额度）**：

```json
{
  "mcpServers": {
    "law-search": {
      "url": "https://mcp.aixllaw.com/mcp"
    }
  }
}
```

**正式版（注册用户，配额更充足）**：

```json
{
  "mcpServers": {
    "law-search": {
      "url": "https://mcp.aixllaw.com/mcp",
      "headers": {
        "Authorization": "Bearer sk-your-api-key-here"
      }
    }
  }
}
```

| 字段 | 值 | 说明 |
|------|-----|------|
| `url` | `https://mcp.aixllaw.com/mcp` | MCP 服务地址 |
| `transportType` | `streamable-http` | 传输协议，仅 CodeBuddy / WorkBuddy 需显式指定，其余平台按传输类型选择即可 |
| `headers.Authorization` | `Bearer sk-xxx` | **可选**：正式版替换 `sk-xxx` 为你的 API Key；免登录模式省略整个 headers |

### 各平台差异对照

| 平台 | 配置文件位置 | 说明 |
|------|-------------|------|
| **CodeBuddy / WorkBuddy** | `~/.codebuddy/mcp.json`（不存在则新建） | 需显式写 `"transportType": "streamable-http"` |
| **Cursor / Windsurf** | 项目或用户目录下 `.cursor/mcp.json` / `.windsurf/mcp.json` | 无需 `transportType` |
| **Claude Desktop** | macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`；Windows: `%APPDATA%\Claude\claude_desktop_config.json`；Linux: `~/.config/Claude/claude_desktop_config.json` | 无需 `transportType` |
| **Cherry Studio / ChatWise / 微信 AI 平台** | 各自 MCP 插件配置界面 | 按 UI 填入：传输类型 `Streamable HTTP`、URL、`Authorization: Bearer sk-xxx` |

> 除 Cherry Studio / 微信 AI 平台等纯 UI 配置外，其余平台均可在 [管理后台](https://portal.aixllaw.com/app/settings) 点「**复制 MCP 配置**」一键复制完整 JSON，直接粘贴即可。

### 配置后生效

配置完成后需**完全退出并重新打开**客户端（仅关闭窗口不够，需退出整个进程），MCP 服务才会被加载。

**验证是否生效**：重启后问一个法律问题（如「试用期最长不超过多久？」），AI 应能调用 `search_law` 工具检索法条并返回结果。若 AI 表示找不到 `search_law` 工具，请检查：

1. 配置文件路径是否正确
2. JSON 格式是否有语法错误
3. API Key 是否以 `sk-` 开头且有效
4. 是否已完全退出重启（仅关闭窗口不够，需退出进程）

### 编程接入（Python）

推荐使用官方 `mcp` SDK：

```python
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

API_KEY = "sk-your-key-here"
MCP_URL = "https://mcp.aixllaw.com/mcp"

async def search_law(query: str):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with streamablehttp_client(MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("search_law", arguments={
                "query": query,
                "scope": "domestic",
                "top_k": 5,
            })
            return result.content

# 调用
result = asyncio.run(search_law("合同诈骗罪构成要件"))
print(result)
```

如果不想依赖 SDK，也可以直接用 HTTP 客户端实现 MCP 协议（参考 3.2 节的 curl 示例）。

---

## 5. search_law 工具参考

### 5.1 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | **是** | — | 检索关键词或自然语言问题 |
| `scope` | string | 否 | `domestic` | `domestic` 国内法律 / `international` 国际法律 |
| `top_k` | integer | 否 | `3` | 返回结果条数（1-5） |
| `score_threshold` | float | 否 | `0.5` | 相似度阈值（0-1），越高越精确但召回越少 |

### 5.2 返回结构

```json
{
  "ok": true,
  "records": [
    {
      "title": "法律文件标题",
      "content": "完整条文内容",
      "trie": "分类标记"
    }
  ],
  "text": "格式化后的文本摘要",
  "message": ""
}
```

- `ok: true` — 检索成功；`ok: false` — 出错，查看 `message` 字段
- `records` — 按相关度降序排列的结果列表
- `text` — 所有结果拼接的纯文本摘要，适合 LLM 阅读

### 5.3 使用建议

- **精确检索**：调高 `score_threshold`（如 0.7），适用于查找具体法条
- **广泛检索**：调低 `score_threshold`（如 0.3），适用于探索性研究
- **国际法律**：设置 `scope: "international"` 检索国际条约、外国法律
- **query 质量**：建议用完整的自然语言问题，而非简单关键词

---

## 6. 错误处理

### 6.1 HTTP 状态码

| 状态码 | 含义 | 原因 | 处理方式 |
|--------|------|------|----------|
| **200** | 正常 | 请求成功 | 检查响应 `ok` 字段判断业务是否成功 |
| **400** | 请求错误 | 缺少 Session ID 或参数格式错误 | 检查 MCP 协议流程是否正确 |
| **401** | 未授权 | 缺少 Bearer token 或 token 无效 | 检查 Authorization 头；如无 Key，前往 [管理后台](https://portal.aixllaw.com/app/settings) 注册获取 |
| **406** | 不可接受 | 缺少必需的 Accept 头 | 添加 `Accept: application/json, text/event-stream` |
| **421** | Host 不匹配 | 请求的 Host 头不在允许列表中 | 使用正确域名 `mcp.aixllaw.com` |
| **429** | 积分不足/用量超限 | 积分余额不够或配额用尽 | 前往 [管理后台](https://portal.aixllaw.com/app/settings) 查看余额并充值 |
| **503** | 服务过载 | 并发数达到上限（默认 10） | 按 1s → 3s → 5s 退避重试（同 SKILL.md 1.3） |

### 6.2 业务错误（HTTP 200 但 ok: false 或 HTTP 401/429）

| 错误类型 | HTTP 状态 | text 关键词 | 处理方式 |
|---------|-----------|------------|---------|
| **免登录额度用尽** | 429 | "免费额度" / "额度已用完" | 前往 [管理后台](https://portal.aixllaw.com/app/settings) 注册获取 API Key，升级正式版 |
| **未配置 Key** | 401 | "缺少 Bearer token" | 免登录模式配置即可用；如需更高配额，前往 [管理后台](https://portal.aixllaw.com/app/settings) 注册获取 Key |
| **Key 无效** | 401 | "API Key 无效" | 前往管理后台重新生成 Key |
| **积分不足** | 429 | "积分余额不足"（含余额和所需积分） | 前往管理后台查看余额并充值 |
| **用量超限** | 429 | "用量已超限" | 前往管理后台查看配额 |
| **参数为空** | 200 | "query 不能为空" | 确保 `query` 参数非空 |

> 所有 401/429 错误响应都包含 `portal.aixllaw.com` 引导链接和「注册即送 1688 积分」福利提示，可直接展示给用户。

---

## 7. 常见问题

### Q: 为什么初始化后直接调用 tools/call 报 "Missing session ID"？

A: MCP Streamable HTTP 协议要求先 `initialize`，从响应头获取 `Mcp-Session-Id`，后续所有请求都要带上这个头。参考 3.2 节的完整示例。

### Q: 返回 406 "Not Acceptable" 怎么解决？

A: 请求头中缺少 `Accept`。MCP 协议要求客户端声明接受 JSON 和 SSE 两种内容类型，添加：
```
Accept: application/json, text/event-stream
```

### Q: 检索结果为空怎么办？

A: 可能原因：
1. `score_threshold` 太高 — 尝试降到 0.3
2. `scope` 选错了 — 国内法律用 `domestic`，国际用 `international`
3. `query` 表述不够精确 — 尝试用完整的自然语言问题

### Q: 如何同时使用多个 MCP 工具？

A: 先在 `tools/list` 中获取所有可用工具列表，然后对每个工具分别调用 `tools/call`。当前 MCP Hub 只提供 `search_law` 一个工具，更多工具会陆续上线。

### Q: 可以不注册直接用吗？

A: 可以。免登录模式内置免费检索额度（有量限制），按第 4 节「免登录版」配置 `url` 即可直接使用，无需 API Key。额度用尽后，前往 [管理后台](https://portal.aixllaw.com/app/settings) 注册获取 Key 并添加 Authorization 头即可升级正式版。

### Q: API Key 从哪里获取？

A: 前往 [https://portal.aixllaw.com/app/settings](https://portal.aixllaw.com/app/settings) 注册账号，注册即送 **1688 积分免费畅用 7 周**。在管理后台「API 密钥」页面可以**一键复制配置**，粘贴到 WorkBuddy / Cursor / Claude Desktop 等工具的 MCP 配置中即可使用。Key 格式为 `sk-` 开头的字符串。

### Q: 每次检索消耗多少积分？

A: 每次 `search_law` 调用消耗一定积分。积分余额和消耗记录可在 [管理后台](https://portal.aixllaw.com/app/settings) 查看。新用户注册即送 1688 积分，可持续使用约 7 周。

---