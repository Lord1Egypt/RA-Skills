---
name: mcp-apps-host-dev
description: Use when developing or debugging the MCP Apps host layer in any agent application — rendering sandboxed iframe cards, bridging postMessage ↔ gateway ↔ MCP server, or fixing security/architectural issues in the card pipeline. Covers the full bridge architecture, security model, and common pitfalls. Includes Hermes Desktop as a reference implementation.
version: 2.1.0
author: ori
license: MIT
platforms: [macos, linux, windows]
---

# MCP Apps Host 开发

## Overview

MCP Apps（`io.modelcontextprotocol/ui` 扩展）让 MCP Server 在工具返回值里嵌入交互式 HTML 卡片。这张卡片是一个沙箱 iframe，通过 `postMessage` 与宿主应用通信，可以调用 MCP 工具、上报状态、发送对话消息。

本文档覆盖**任何 Agent 应用**作为 **Host（宿主端）** 的完整开发知识——从卡片渲染、桥接通信、安全边界到常见踩坑。

**这不是 MCP Server 端开发指南**（用 `fastmcp` skill 构建 MCP Server），而是 **Host 端**：接收卡片、渲染 iframe、管理沙箱安全、桥接消息。

> **参考实现**：本文以 [Hermes Agent](https://github.com/NousResearch/hermes) 桌面端为参考实现。架构模式和安全模型适用于任何 Agent 应用；附录 [Reference Implementation: Hermes Desktop](#reference-implementation-hermes-desktop) 提供角色→文件的映射。

## When to Use

- 在 Agent 应用中新增或调试 MCP Apps 卡片的渲染逻辑
- 排查卡片不显示、iframe 空白、postMessage 不通的问题
- 修改卡片渲染组件、桥接处理器、UI 缓存等 MCP Apps 相关代码
- 给桥接层加安全校验（新增工具白名单、追溯审计等）
- 理解 MCP Server → 屏幕上那张卡片的完整数据流

**不要用这个 skill 来做**：
- 构建 MCP Server 本身 → 用 `fastmcp`
- 配置 MCP Server 连接 → 用你所用 Agent 的 MCP 配置
- 与卡片无关的纯前端 UI 调整 → 用通用前端调试 skill

## 架构全景

### 数据流：从 MCP Server 到屏幕上的卡片

任何 MCP Apps Host 实现都包含以下 7 层。每层的角色名称是通用的；括号内标注 Hermes 参考实现的具体位置。

```
┌────────────────────────────────────────────────────────────┐
│ 1. MCP Server (Python, 你的服务)                            │
│    tool 返回 _meta.ui.resource = {uri, mimeType, html}      │
│    + _meta.ui.csp = {scriptSrc, connectDomains, ...}        │
└──────────────────────┬─────────────────────────────────────┘
                       │ MCP 协议 (stdio / HTTP)
┌──────────────────────▼─────────────────────────────────────┐
│ 2. Extraction Layer  (Hermes: tools/mcp_tool.py)            │
│    _extract_mcp_ui() 从 CallToolResult._meta.ui 提取卡片    │
│    _stash_mcp_ui_payload() 按 tool_call_id 暂存             │
│    → 卡片 HTML 不进模型上下文（保护 prompt cache）            │
└──────────────────────┬─────────────────────────────────────┘
                       │ pop_mcp_ui_payload(tool_call_id)
┌──────────────────────▼─────────────────────────────────────┐
│ 3. Event Bridge  (Hermes: tui_gateway/server.py)            │
│    pop_mcp_ui_payload() → payload["ui"] = {server, uri,     │
│      mimeType, html, csp}                                   │
│    → 作为 tool.complete 事件发送给渲染端                     │
└──────────────────────┬─────────────────────────────────────┘
                       │ 事件 / JSON-RPC (tool.complete)
┌──────────────────────▼─────────────────────────────────────┐
│ 4. Renderer  (Hermes: message-parts.tsx::ChainToolFallback)│
│    → hasMcpUi(result) 检测 result.ui 字段                   │
│    → <CardComponent toolCallId={...} result={...} />        │
└──────────────────────┬─────────────────────────────────────┘
                       │ 渲染
┌──────────────────────▼─────────────────────────────────────┐
│ 5. Card Component  (Hermes: mcp-app-card.tsx)              │
│    ┌──────────────────────────────────────────────┐         │
│    │ sandbox iframe (allow-scripts allow-forms)    │         │
│    │                                              │         │
│    │  [搜索结果] [商品 ¥14] [加购]                 │         │
│    │                                              │         │
│    │  用户点击 → postMessage({jsonrpc, id,         │         │
│    │    method: "tools/call",                     │         │
│    │    params: {name: "cart_add", ...}})          │         │
│    └──────────────────┬───────────────────────────┘         │
│                       │ window.addEventListener('message')  │
│                       ▼                                     │
│  Card 桥接逻辑:                                             │
│    ui/* 方法 → 本地处理（初始化、resize、model-context）      │
│    tools/call、resources/* → 转发到 Bridge Handler           │
└──────────────────────┬─────────────────────────────────────┘
                       │ 事件 / JSON-RPC
┌──────────────────────▼─────────────────────────────────────┐
│ 6. Bridge Handler  (Hermes: tui_gateway mcp.app.request)   │
│    解析 {server, toolCallId, message}                        │
│    → 转发到 Security Gate                                    │
└──────────────────────┬─────────────────────────────────────┘
                       │
┌──────────────────────▼─────────────────────────────────────┐
│ 7. Security Gate + Execution  (Hermes: mcp_tool.py           │
│    ::call_mcp_app_request)                                  │
│    校验 tool_call_id + tool name whitelist                   │
│    → 执行实际的 MCP 调用 (session.call_tool / read_resource) │
│    → 返回 JSON-RPC response                                 │
└──────────────────────┬─────────────────────────────────────┘
                       │
                       ▼ 原路返回 postMessage → iframe
```

### 两张卡片形态

MCP Server 可以通过两种方式提供卡片 HTML：

| 形态 | 来源 | 何时解析 | 示例 |
|---|---|---|---|
| **inline form** | 工具 RESULT 的 `_meta.ui.resource` 直接嵌 HTML | 每次工具调用 | login / checkout / address |
| **referenced form** | 工具 DEFINITION 的 `_meta.ui.resourceUri`（`ui://` URI）| 工具定义发现时缓存 HTML，调用时复用 | catalog_search / cart_list |

referenced form 的 HTML 是静态的（每个 `ui://` URI 只 fetch 一次，缓存在内存中），卡片通过 `ui/initialize` 的 `lastToolResult` 拿到工具数据来渲染。

### ui/initialize 握手

卡片 iframe 加载后，向 host 发送 `ui/initialize` 请求。Host 响应中携带卡片初始化所需的全部上下文：

```typescript
// Card Component — ui/initialize 响应
reply({
  result: {
    protocolVersion: ...,
    hostInfo: HOST_INFO,
    hostCapabilities: { updateModelContext: { text: {} }, message: { text: {} } },
    lastToolResult: buildLastToolResult(resultRef.current),  // 工具原始 structuredContent
    sessionId: readSessionId(resultRef.current)               // 从 structuredContent.session_id 提取
  }
})
```

- **`lastToolResult`**：从原始工具结果的 `structuredContent` 构建。referenced-form 卡片用它渲染初始视图（如商品列表），而非空白搜索页。当 `structuredContent` 不存在或 `error` 时返回 `undefined`。
- **`sessionId`**：从 `structuredContent.session_id` 提取。某些 MCP Server 要求每次 `tools/call` 都带 `session_id`。卡片通过 `ui/initialize` 拿到后，理论上应在后续 `tools/call` 中带上——但旧版卡片 SDK 不一定会这样做（见踩坑 #11）。

## Implementation Roles

任何 MCP Apps Host 实现都需要以下角色。每行列出通用职责和 Hermes 参考实现的具体位置。

```
Extraction Layer  (Hermes: tools/mcp_tool.py)
  ├── _extract_mcp_ui()           # 从 CallToolResult._meta.ui 提取 inline 卡片
  ├── _resolve_referenced_mcp_ui() # 从 tool definition 解析 referenced 卡片
  ├── _stash_mcp_ui_payload()     # 按 tool_call_id 暂存（不入模型上下文）
  ├── pop_mcp_ui_payload()        # 一次性取出，供 Event Bridge 消费
  ├── call_mcp_app_request()      # ★ 安全入口：校验 + 执行 MCP 调用
  ├── _capture_ui_tool_resources()# 工具发现时记录 referenced-form 元数据
  └── _initialize_declaring_ui()  # 握手时声明 host 支持 UI 扩展

Event Bridge  (Hermes: tui_gateway/server.py)
  ├── _on_tool_complete()         # pop_mcp_ui_payload → payload["ui"]
  └── mcp.app.request handler     # iframe 桥接请求的网关入口

Renderer  (Hermes: apps/desktop/src/components/assistant-ui/)
  ├── message-parts.tsx               # ★ 工具结果派发器 → hasMcpUi → CardComponent
  └── mcp-app-card.tsx                # ★ 卡片组件：iframe + postMessage 桥接 + session_id 注入

UI State Cache  (Hermes: apps/desktop/src/lib/chat-messages.ts)
  ├── cacheMcpUi()                # 写内存 Map + localStorage
  ├── preserveMcpUiCards()        # 读内存 → 回退 localStorage
  └── clearCachedMcpUi()         # 清两个位置

Model Communication Channel  (Hermes: apps/desktop/src/store/mcp-app.ts)
  ├── ui/update-model-context    # 静默状态快照
  └── ui/message                 # 触发对话回合

Session Controller  (Hermes: apps/desktop/src/app/contrib/wiring.tsx)
  └── $mcpAppUserMessage 订阅    # ui/message → 提交路径
```

## 渲染管线

### 卡片如何被选中渲染

Renderer 层的派发器是所有工具结果的入口。MCP Apps 卡片不按 `toolName` 匹配（工具名是动态的），而是检查 `result` 是否携带 `ui` 字段：

```typescript
// 派发器逻辑
if (hasMcpUi(props.result)) {
  return <CardComponent {...props} />
}
```

`hasMcpUi()` 检查 `result.ui` 是否存在且包含必需的 `server`、`html`、`uri` 字段。

### 检查顺序

派发器中的检查顺序很重要（以 Hermes 为例）：

1. `todo` — 提升到专用面板
2. `react_to_message`（非错误）— 隐藏
3. **`hasMcpUi(result)`** — MCP Apps 卡片 ← 我们的位置
4. `delegate_task` — 子代理委派
5. `image_generate` — 图片生成
6. `clarify` — 澄清工具
7. 其他 → 通用 fallback 行

### ⚠️ 退役渲染器陷阱

大型 Agent 应用可能有多个版本的渲染管线共存。以 Hermes 为例：`thread.tsx` 有自己的 `ChainToolFallback`，但这是退役渲染器。当前主力渲染路径是 `message-parts.tsx`。**不要在退役渲染器里加 MCP Apps 代码**——只改当前活跃的渲染器，否则卡片不显示。

## 安全边界

### 问题：沙箱 iframe 可以越权调用工具

卡片跑在 `sandbox="allow-scripts allow-forms"` 的 iframe 里，通过 postMessage 桥接到宿主。如果 Bridge Handler 不加检查，卡片发的任何 `tools/call` 都会被直接执行。一张搜索卡片理论上可以调用结账、删除订单等任意工具。

### 两层防护

**第一层 — 前端传 `toolCallId`**（Card Component）：

```typescript
// 每次桥接请求都带上原始工具调用的 ID，用于审计追溯
const res = await requestBridge('mcp.app.request', {
    server,
    toolCallId,  // ← 追溯：这个调用来自哪个卡片
    message: msg
})
```

**第二层 — 后端校验工具白名单**（Security Gate）：

```python
if method == "tools/call":
    name = params.get("name")
    # 校验：iframe 要调用的工具必须在 MCP Server 注册的工具列表中
    registered = getattr(server, "_registered_tool_names", None)
    if name and (registered is None or name not in registered):
        return {"error": {"code": -32601,
                "message": f"tool '{name}' not registered on server '{server_name}'"}}
```

`_registered_tool_names` 在 MCP 握手时从 `tools/list` 的结果中自动填充，记录该 Server 实际暴露的所有工具名。

**注意**：校验条件用 `registered is None or name not in registered`，**不要**用 `registered and name not in registered`。旧代码用 `or []` 把空列表转为 falsy 值，导致 `[] and ...` 短路跳过校验——在 tools 尚未发现或已重置为空列表时白名单形同虚设。`None`（未初始化）和 `[]`（已初始化但无工具）均应阻断所有桥接调用。

**resources/read 白名单 — `ui://` 前缀检查**（同层）：

```python
if method == "resources/read":
    uri = params.get("uri")
    # 安全：只有 ui:// 资源可通过桥接访问。非 ui:// URI
    # （db://、file:// 等）是给模型用的，不是给沙箱 iframe 的。
    if not isinstance(uri, str) or not uri.startswith("ui://"):
        return {"error": {"code": -32601,
                "message": f"resource not accessible from a card: {uri}"}}
```

和 `tools/call` 白名单是同一类防御——桥接层对每个出站方法都要校验参数合法性，不能无条件透传。

### 新增 MCP Server 时

如果新增了一个 MCP Server 并希望它的卡片能通过桥接调用工具，不需要额外配置——只要 Server 在 `tools/list` 中声明了工具，`_registered_tool_names` 就会自动包含它。

### CSP 策略：卡片资源加载

卡片在 sandbox iframe 中运行，服务端通过 `_meta.ui.csp` 声明其需要的资源权限。Host 端的 `buildCsp()` 根据此配置构建 `Content-Security-Policy`：

```typescript
function buildCsp(csp: McpUiCsp): string {
    const res = (csp.resourceDomains ?? []).join(' ').trim()
    const conn = (csp.connectDomains ?? []).join(' ').trim()
    const script = (csp.scriptSrc || "'unsafe-inline' 'unsafe-eval'").trim()

    return [
        "default-src 'none'",
        `script-src ${script}`,
        `style-src 'unsafe-inline' ${res}`.trim(),
        `img-src data: blob: ${res}`.trim(),
        `font-src data: ${res}`.trim(),
        `media-src ${res || "'none"'}`.trim(),
        `connect-src ${conn || "'none'"}`.trim(),
        "base-uri 'none'",
        'form-action *'
    ].join('; ')
}
```

**关键约束**：

- `img-src` 放行 `data: blob: https:` 和 `resourceDomains` 中的域名。DSH 默认包含 `https:` 以支持 CDN 商品图片（参见坑 #17）。如果需要更严格的限制，在 `_meta.ui.csp.resourceDomains` 中声明具体域名。
- `connect-src` 默认为 `'none'`（sandbox iframe 无 `allow-same-origin`，`'self'` 无意义）。卡片需要发起网络请求（fetch/WebSocket）时，其域名**必须**在 `connectDomains` 中声明。
- `script-src` 默认 `'unsafe-inline' 'unsafe-eval'`——卡片 HTML 中的内联脚本可以执行，但外部脚本文件需要 `scriptSrc` 额外声明。

**MCP Server 端最佳实践**：在构造 `_meta.ui.csp` 时，列出卡片 HTML 中所有引用到的外部资源域名：

```python
"_meta": {
    "ui": {
        "csp": {
            "resourceDomains": ["img.alicdn.com", "gw.alicdn.com"],
            "connectDomains": ["api.example.com"],
            "scriptSrc": "'unsafe-inline' 'unsafe-eval' https://cdn.example.com",
        }
    }
}
```

## 卡片→模型通信

MCP Apps 规范定义了两个卡片到模型的通道：

### ui/update-model-context（静默状态快照）

卡片把当前视图状态（如搜索关键词、筛选条件）发给模型，作为**下一条用户消息的不可见前缀**：

```typescript
// 规范：每次更新覆盖同一 view 的上一个快照
stageModelContext(viewId, extractTextContent(params))

// 发送下一条用户消息时：
buildOutgoingUserText(userText)
// → "卡片状态:\n搜索: 蓝牙耳机 价格<100\n\n用户输入的文本"
```

### ui/message（触发对话回合）

卡片请求模型发起一个新的对话回合。

```typescript
requestMcpAppUserMessage(text)
// → 通过消息通道 → submitText 发送路径
```

**安全：per-card debounce**。恶意/有问题的卡片在循环中连续发 `ui/message` 会触发无限次模型对话，每次消耗 API 往返 + token。`requestMcpAppUserMessage(text, debounceKey)` 按 `toolCallId` 隔离限流窗口——同一张卡片在 debounce 窗口内只放行一次，不同卡片互不阻塞。

## 常见踩坑

### 1. 卡片不显示 → 检查渲染器

**症状**：工具调用成功但看不到卡片，只看到普通的 tool fallback 行。

**排查**：
1. 确认活跃的渲染器（不是退役的）里有 `hasMcpUi` 检查
2. 打开 DevTools，在派发器里加 `console.log` 看 `result.ui` 是否存在
3. 检查 `hasMcpUi()` 的校验逻辑——需要 `server`、`html`、`uri` 三个字段都存在

### 2. 改了渲染器却没生效 → 退役渲染器陷阱

**症状**：修改了渲染逻辑并保存，但卡片行为没变。

**原因**：大型 Agent 应用可能有多个版本的渲染管线共存。你改的那个可能已经退役，当前走的是另一个。

**排查**：确认哪个渲染器是活跃路径。以 Hermes 为例：`thread.tsx` 是退役渲染器，`message-parts.tsx` 才是当前主力。两个文件各有一个 `ChainToolFallback`，只改退役的会导致卡片不显示。

### 3. iframe 空白 / postMessage 不通

**检查清单**：
- iframe 的 `sandbox` 属性是否包含 `allow-scripts`
- CSP 策略是否阻止了卡片需要的脚本/连接域名（`buildCsp()` 从 `_meta.ui.csp` 构建）
- postMessage 的 `event.source !== iframe.contentWindow` 校验是否误杀（其他 iframe 也会发 message）
- DevTools Console 搜 `[mcp-app<-card]` / `[mcp-app->card]` 看消息流（仅 DEV 模式输出）

### 4. 桥接调用失败"tool not registered"

**原因**：卡片试图调用的工具名不在 `_registered_tool_names` 中。

**排查**：
1. 确认 MCP Server 的 `tools/list` 确实声明了该工具
2. 确认 Server 在你的 Agent 应用中已成功连接
3. 重启后首次连接会重新 populate `_registered_tool_names`

### 5. referenced-form 卡片始终不渲染

referenced form 需要两步：
1. 工具定义发现时 Extraction Layer 记录 `_meta.ui.resourceUri`
2. 工具调用时解析 `ui://` 资源获取 HTML

**排查**：
- 确认 Host 在 MCP `initialize` 握手时声明了 `io.modelcontextprotocol/ui` 扩展，否则 Server 不会在工具定义中带 `_meta.ui`
- 检查 HTML 缓存是否已有内容（key 通常是 `(server_name, resourceUri)`）
- 检查 `resources/read` 调用是否成功

### 6. 大 HTML 撑爆模型上下文

MCP Apps 卡片的 HTML 完全不进模型上下文。Extraction Layer 把 HTML 暂存在进程内存中（按 `tool_call_id` 索引），只通过事件发送给渲染端。模型看到的是不含 HTML 的工具结果。

**如果实现新 Host 时发现模型回复里出现了大段 HTML**，说明 stash 逻辑没生效——HTML 泄漏到了模型上下文，prompt cache 会失效。

### 7. 新增桥接方法时忘记加安全校验

**这是最危险的模式。** Bridge Handler 中新增的任何 `if method == "xxx":` 分支，都必须检查参数合法性再透传。

- `tools/call`: 校验 name 在 `_registered_tool_names` 中 ✅
- `resources/read`: 校验 uri 以 `ui://` 开头 ✅
- 如果新增其他 bridge 方法，必须有对应的参数校验

不加校验 = 沙箱 iframe 可以调用任意 MCP Server 能力，绕过所有权限控制。

### 8. 图片 / 外部资源加载不出来

**症状**：卡片正常渲染，但图片显示空白/裂图，或 CSS 字体/媒体资源加载失败。

**原因**：CSP `img-src` / `font-src` / `media-src` 只放行了 `resourceDomains` 中声明的域名。如果 MCP Server 在 `_meta.ui.csp.resourceDomains` 里遗漏了卡片 HTML 中引用到的 CDN/图片域名，CSP 会静默阻挡这些资源。

**排查**：
1. 打开 DevTools Console，搜 `Content-Security-Policy` 违规报告（Chrome 会打印具体被挡的 URL 和指令）
2. 确认卡片 HTML 中所有 `<img src="...">`、`<link href="...">` 的域名都在 `resourceDomains` 中
3. 注意 `connect-src` 默认是 `'none'`（不是 `'self'`）——sandbox iframe 无同源概念，`'self'` 无意义
4. 确认 MCP Server 在构造 `_meta.ui.csp` 时正确填入了所需域名

**修复**：在 MCP Server 端补充 `_meta.ui.csp.resourceDomains` 和/或 `connectDomains`。

### 9. `_registered_tool_names` 为空时桥接白名单被绕过

**历史坑**：旧代码用 `registered = getattr(...) or []` + `if name and registered and ...` 做校验。当 `_registered_tool_names` 为 `[]`（尚未填充、或 disconnect 后重置）时，`[]` 是 falsy，`[] and ...` 短路跳过整个校验块——白名单形同虚设。

**已修复**：改为 `registered = getattr(...)` + `if name and (registered is None or name not in registered)`。`None`（未初始化）和 `[]`（已填充但为空）均阻断所有桥接调用。新增测试覆盖这两种情况。

### 10. CSP 排查技巧

在 DevTools Console 中执行以下检查：

```javascript
// 查看 iframe 实际应用的 CSP
const iframe = document.querySelector('iframe[title*="ui://"]')
console.log(iframe?.contentDocument?.querySelector('meta[http-equiv="Content-Security-Policy"]')?.content)

// 监听 CSP 违规（在卡片 iframe 的 console 中）
document.addEventListener('securitypolicyviolation', e => {
    console.warn('CSP blocked:', e.blockedURI, '→ directive:', e.violatedDirective)
})
```

### 11. 卡片 tools/call 缺少 session_id → 数据不渲染

**症状**：卡片渲染了但内容空白（如结账卡片"应付金额 -"，无商品信息），agent 文本回复里有完整数据。

**根因**：卡片初始化后主动通过 `tools/call` 再次调用 MCP 工具刷新数据（如 `checkout_get`、`address_form`），但旧版卡片 SDK 不会把 `ui/initialize` 响应中的 `sessionId` 转发到 `tools/call` 的 `arguments` 里。某些 MCP Server 要求每次调用必须带 `session_id`，缺少时返回 `isError: true`，卡片拿不到数据。

**修复**：Host 在代理 `tools/call` 时自动注入 `session_id`（Card Component）：

```typescript
if (method === 'tools/call') {
    const params = (msg.params ?? {}) as Record<string, unknown>
    const args = (params.arguments ?? {}) as Record<string, unknown>
    if (args.session_id === undefined) {
        const sid = readSessionId(resultRef.current)
        if (sid) {
            outgoingMsg = { ...msg, params: { ...params, arguments: { ...args, session_id: sid } } }
        }
    }
}
```

**调试技巧**：在 `ui/initialize` handler 和 `tools/call` proxy 中加 `console.log` 输出 `hasLastToolResult`、`sessionId`、`tools/call` 的请求/响应 `isError` 和 `hasSC`，通过 CDP `evaluate` 在 iframe 重载后捕获。

### 12. HMR 重载后卡片消失 → localStorage 持久化

**症状**：开发模式下 HMR 触发页面重载后，已渲染的 MCP App 卡片全部消失。

**根因**：UI State Cache 是进程内 `Map`，HMR 重载清空内存。`ui` payload 只在 `tool.complete` 事件中一次性传递（server 端 `pop_mcp_ui_payload` 是单次消费），不会被持久化到数据库。

**修复**（UI State Cache 层）：
- `cacheMcpUi()` 同时写内存 Map 和 `localStorage`（key: `mcp-ui:<sessionId>`）
- `preserveMcpUiCards()` 在内存 Map 未命中时回退读 `localStorage`
- `clearCachedMcpUi()` 同时清内存和 `localStorage`
- 跨 session ID 匹配：当 runtime session ID 与存储时的 event session ID 不一致时，扫描所有 `mcp-ui:*` localStorage 条目按 tool-call ID 匹配

**注意**：用 `localStorage` 而非 `sessionStorage`——`localStorage` 跨 HMR 重载和 app 重启都存活。

### 13. Gateway 进程挂了但 App 壳还活着 → 消息无回复

**症状**：在应用中发消息，完全没有回复，也不报错。

**根因**：如果 Agent 应用采用前后端分离架构（如 Electron + Python gateway），前端进程和后端 gateway 是两个独立进程。Gateway 可能因 API 端点超时（`stream_interrupt_abort` + `tcp_force_closed=1`）、内存耗尽或其他原因崩溃，但前端壳不会自动重启它。用户看到的是"活着但没反应"的 app。

**排查**：
```bash
# 1. 检查 gateway/backend 进程是否存活
#    Hermes: ps aux | grep "hermes_cli.main serve" | grep -v grep

# 2. 检查最新 agent 日志（是否有新 turn 记录）

# 3. 如果日志停在几分钟前且没有新 turn → gateway 挂了

# 4. 检查 API 端点是否可达
curl -s --max-time 10 "<base_url>/chat/completions" \
  -H "Authorization: Bearer <key>" \
  -d '{"model":"<model>","messages":[{"role":"user","content":"hi"}],"max_tokens":5}'
```

**修复**：杀掉残留前端进程后重启。如果 API 端点本身不稳定，考虑配置 `request_timeout` 或使用更稳定的 provider。

### 14. MCP 客户端未声明 `mimeTypes` → 工具定义中 `_meta` 被清除

**症状**：`tools/list` 返回的工具定义中 `_meta.ui` 字段为空，导致 referenced-form 卡片无法渲染（iframe 不出现）。Agent 回复正常（文本工具结果不受影响），但看不到任何 MCP Apps 卡片。

**根因**：某些 MCP Server（如 UTP CLI v0.6.15）的 `supportsMCPApps()` 函数不仅检查客户端是否声明了 `io.modelcontextprotocol/ui` 扩展键，还要求扩展数据中包含 `mimeTypes` 数组且含 `"text/html;profile=mcp-app"`。只发送空对象 `{}` 不够——Server 会认为客户端不支持 MCP Apps，清除所有工具定义的 `_meta`。

**修复**：MCP 客户端初始化时，扩展声明中必须包含 `mimeTypes`：

```typescript
const client = new Client(
  { name: 'my-host', version: '0.0.1' },
  { capabilities: {
      extensions: {
        'io.modelcontextprotocol/ui': {
          mimeTypes: ['text/html;profile=mcp-app']  // ← 必须
        }
      }
    } 
  },
)
```

**排查方法**：写一个独立的 MCP 客户端测试脚本，直接通过 stdio 连接 MCP Server，发 `tools/list`，检查返回的工具是否含 `_meta`。如果 0 个工具含 `_meta`，说明 Server 认为客户端不支持 UI 扩展——检查 `mimeTypes` 是否声明。UTP Server 源码参考：`internal/mcp/server.go` 的 `supportsMCPApps()` 函数。

### 15. 卡片渲染成功但工具结果未在卡片内展示

**症状**：iframe 正常渲染了 MCP Apps 卡片的 UI（如搜索表单），但 Agent 工具调用的结果（如搜索到的商品列表）未在卡片内部展示。卡片只显示空白表单或搜索入口，用户在卡片内看不到 Agent 已搜索到的数据。

**根因**：`lastToolResult` 的数据格式与卡片 React 应用期望的格式不匹配。卡片 React 应用期望 `CallToolResult` 形状的对象（含 `.structuredContent` 属性），但 Host 传递的是 `content`（render 输出的文本数组）或裸 `structuredContent` 值，不含 `.structuredContent` 属性包装。

UTP React 应用（"UCP Catalog v5.0.0"）的数据提取逻辑：
```javascript
// 先检查 t 本身是否有 products/product/line_items/orders
if ("products" in t || ...) return t;
// 再检查 t.structuredContent
const n = t.structuredContent;  // ← 期望 .structuredContent 属性
return n ? ("products" in n ? n : n.body ? n.body : ...) : null;
```

**与坑 #11 的区别**：坑 #11 是 `tools/call` 缺少 `session_id` 导致后续刷新失败；本坑是**初始渲染**就缺失——`ui/initialize` 的 `lastToolResult` 未被卡片 React 应用消费。

**修复**：`presentationMeta()` 必须将工具结果包装为 `CallToolResult` 形状对象传递：
```typescript
// presentationMeta 返回值
return {
  mcpApp: ui,
  lastToolResult: {
    content: result.content,
    ...(result.structuredContent !== undefined
      ? { structuredContent: result.structuredContent }
      : {}),
  },
}
```

然后 `ui/initialize` handler 从 `meta.lastToolResult` 读取并传给 iframe：
```typescript
const meta = currentBlock.meta as { lastToolResult?: unknown } | undefined
result.lastToolResult = meta?.lastToolResult ?? currentBlock.content
```

**已解决**：DSH 适配中已修复此问题（2026-08-20）。修复后卡片内成功渲染商品列表（名称、价格、销量、好评率等），不再是空表单。

### 坑 #16：readSessionId 未使用 structuredContent 路径

**现象**：P1 修复后 `meta.lastToolResult.structuredContent` 已可用，但 `readSessionId()` 仍仅从 `block.content` 文本解析 JSON 查找 `session_id`。当 content 文本不是纯 JSON（如含可读前缀），parse 失败 → `session_id` 注入失败 → 卡片内加购物车/结算等操作断掉。

**根因**：P1 修复改了数据通道（`presentationMeta` → `meta.lastToolResult`），但 `readSessionId` 没跟着更新读取路径。

**修复**：`readSessionId()` 优先从 `meta.lastToolResult.structuredContent.session_id` 读取，回退到 content 文本解析：
```typescript
const meta = block.meta as { lastToolResult?: { structuredContent?: Record<string, unknown> } } | undefined
const sc = meta?.lastToolResult?.structuredContent
if (sc && typeof sc === 'object') {
  if (typeof sc.session_id === 'string') return sc.session_id
  if (typeof sc.sessionId === 'string') return sc.sessionId
}
// Fallback: parse JSON from content text blocks...
```

**已解决**：DSH 适配中已修复此问题（2026-08-20）。

### 坑 #17：CSP img-src 阻断外部商品图片

**现象**：iframe CSP `img-src data: blob:` 仅允许 data/blob URI，阻断所有 CDN 外部商品图片（如 alicdn.com 上的商品图）。

**根因**：`buildCsp()` 默认 `img-src` 不包含 `https:` 协议，且 MCP Server 可能不在 `_meta.ui.csp.resourceDomains` 中声明图片域名。

**修复**：`buildCsp()` 默认 `img-src` 添加 `https:`：`img-src data: blob: https:`。

**已解决**：DSH 适配中已修复此问题（2026-08-20）。

### 坑 #18：ui/update-model-context 未实现（TODO 桁留）

**现象**：`ui/update-model-context` handler 仅 `console.debug` 后丢弃上下文文本，从未暂存或注入到后续消息中。卡片发送的上下文更新（如搜索关键词、筛选条件）被完全丢弃。

**根因**：初始实现标记为 TODO，未完成暂存逻辑。

**修复**：
1. 新增 `_stagedContext` Map，按 callId 暂存上下文文本
2. `ui/update-model-context` handler 写入 `_stagedContext.set(callId, text)`
3. `ui/message` handler 读取并前置到消息文本前发送，发送后清除
4. 组件卸载时清理 `_stagedContext` 条目

**已解决**：DSH 适配中已修复此问题（2026-08-20）。

## 验证清单

修改 MCP Apps Host 代码后，检查以下项目：

- [ ] 活跃的渲染派发器中有 `hasMcpUi` 检查，位于其他工具类型检查的正确位置（以 Hermes 为例：`react_to_message` 之后、`delegate_task` 之前）
- [ ] 没有在退役渲染器里添加 MCP Apps 代码
- [ ] `ui/message` 订阅在实际的 Session Controller 中（以 Hermes 为例：`ContribWiring`，不是 `DesktopController`）
- [ ] 如果改了桥接层，`toolCallId` 从 Card Component → Event Bridge → Security Gate 完整传递
- [ ] Bridge Handler 中对 `tools/call` 做了工具名白名单校验（`registered is None or name not in registered`，不依赖空列表的 falsy 短路）
- [ ] Bridge Handler 中对 `resources/read` 做了 `ui://` 前缀校验
- [ ] `tools/call` 代理路径在卡片参数缺少 `session_id` 时自动注入
- [ ] UI State Cache 同时写内存 Map 和 `localStorage`；读取时内存未命中回退 `localStorage`
- [ ] `requestMcpAppUserMessage` 有 per-card debounce，不会在紧循环中无限触发模型回合
- [ ] 单元测试通过（前端 + 后端）
- [ ] 在应用中实际渲染一张 MCP Apps 卡片，确认 iframe 显示、点击按钮能触发工具调用、卡片内数据完整（非空白）
- [ ] 开发模式下触发 HMR 重载后，已渲染的卡片仍然存活
- [ ] MCP 客户端声明了 `mimeTypes: ['text/html;profile=mcp-app']`（不只是扩展键）
- [ ] `ui/initialize` 响应中的 `lastToolResult` 是 `CallToolResult` 形状对象（含 `.structuredContent` 属性），卡片 React 应用内被消费渲染（非空白表单）
- [ ] `readSessionId` 优先从 `meta.lastToolResult.structuredContent.session_id` 读取，回退到 content 文本解析
- [ ] CSP `img-src` 包含 `https:` 以放行外部 CDN 图片
- [ ] `ui/update-model-context` 上下文暂存到 `_stagedContext` Map，在下次 `ui/message` 时前置注入并清除

## Reference Implementation: Hermes Desktop

[Hermes Agent](https://github.com/NousResearch/hermes) 桌面端是本文描述架构的参考实现。以下是角色→文件映射：

| 角色 | 文件 | 语言 |
|---|---|---|
| Extraction Layer | `tools/mcp_tool.py` | Python |
| Event Bridge | `tui_gateway/server.py` | Python |
| Renderer | `apps/desktop/src/components/assistant-ui/thread/message-parts.tsx` | TSX |
| Card Component | `apps/desktop/src/components/assistant-ui/mcp-app-card.tsx` | TSX |
| UI State Cache | `apps/desktop/src/lib/chat-messages.ts` | TS |
| Model Communication Channel | `apps/desktop/src/store/mcp-app.ts` | TS |
| Session Controller | `apps/desktop/src/app/contrib/wiring.tsx` | TSX |

**测试命令**（Hermes 仓库根目录）：
```bash
cd apps/desktop && npx vitest run src/components/assistant-ui/mcp-app-card.test.tsx src/store/mcp-app-security.test.ts
python -m pytest tests/tools/test_mcp_apps_ui.py -x
```

在其他 Agent 应用中实现 MCP Apps Host 时，按以上角色创建对应模块，分层思路和安全边界直接复用。

### Reference Implementation: DeepSeek Harness (DSH)

[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) 是一个 Cordis 插件化运行时的 Agent 应用。MCP Apps Host 通过插件包 `@deepseek-ai/dsh-mcp-apps-host` 实现，不修改 DSH 核心代码。

| 角色 | 文件 | 语言 |
|---|---|---|
| Extraction Layer + Bridge Handler | `packages/mcp/mcp-apps-host/src/index.ts` | TypeScript |
| Card Component | `packages/mcp/mcp-apps-host/src/client/McpAppCard.tsx` | TSX |
| Slot Registration + sendUserMessage | `packages/mcp/mcp-apps-host/src/client/index.ts` | TypeScript |
| Profile Overlay (连接配置) | `mcp-apps-utp.patch.yml` | YAML |

**DSH 特有的扩展点**：
- `ctx.webServer.register()`: 注册 HTTP 路由 (`/mcp-apps/<server>/bridge`)，用于 postMessage 桥接
- `presentationMeta()` 函数: 从工具执行结果的 `_meta.ui` 投射到 `result.meta.mcpApp`，流经 `ToolResultNode.meta` 到客户端 React 组件
- `tool.call.toolview` slot: 按 `mcp__<serverName>__<toolName>` key 注册自定义 React 视图

**DSH 适配中踩过的坑**：#14（mimeTypes 未声明）、#15（工具结果未在卡片内渲染）、#16（readSessionId 未用 structuredContent 路径）、#17（CSP img-src 阻断外部图片）、#18（ui/update-model-context 未实现）
