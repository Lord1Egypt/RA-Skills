---
name: network-request-twister
slug: network-request-twister
displayName: 网络请求修改器
version: "1.1.0"
category: 开发工具
platforms:
  - WorkBuddy
  - Claude Code
  - Cursor
description: "当用户想要观察、拦截或修改浏览器网络请求和响应时使用此 skill。Use when the user wants to observe, intercept, or modify browser network requests — monitor HTTP traffic, mock API responses, block analytics/tracking, modify request/response headers, rewrite response bodies, inject content into pages, or test web behavior under modified network conditions. Trigger even when the user doesn't use precise technical terms — 「帮我看这个网站发了什么请求」「把这个 API 的返回值改成假的」「屏蔽谷歌统计」「让页面显示不同数据」are all valid triggers. Keywords: 拦截 intercept mock 修改请求 修改响应 改包 抓包 network monitor CDP fake backend 替换返回值 注入 inject script 改 header 阻止 block request."
---

# 网络请求修改器 / Network Request Twister

通过 Chrome DevTools Protocol 实时观察和修改浏览器网络请求/响应，无需安装浏览器插件。

## 模式选择

根据用户意图选择工作模式：

| 用户意图 | 模式 | 行为 |
|----------|------|------|
| 「看看这个页面发了什么请求」「帮我抓包分析」 | 观察模式 | 输出 JSONL 网络日志，AI 分析后决定下一步 |
| 「拦截 analytics 请求」「把 API 返回值改掉」「修改 Header」 | 拦截模式 | 启动浏览器加载规则，用户在浏览器中验证 |
| 「浏览器开了吗」「有哪些标签页」 | 列目标 | 列出当前可用的浏览器标签页 |

**除非用户直接给出明确规则（如「把 /api/users 的返回值改成 XXX」），否则必须先观察再修改。**

## 执行约束

**twist 命令是纯阻塞进程，永不自动退出（行为与 `tail -f` 一致）。** 如果同步等待命令返回，Agent 将永久阻塞——因为 twist 不像普通命令那样执行完就退出，它会持续运行直到被外部终止。因此必须使用平台后台机制启动，用非阻塞方式读取输出。

启动后：
- 观察模式：后台启动 → **非阻塞轮询** stdout 读取 JSONL → 收集够数据后终止进程
- 拦截模式：后台启动 → **不读输出**（stdout 只有日志，没有结构化数据）→ 用户验证浏览器后终止进程
- **禁止等待进程退出** — twist 永不退出，等待会导致永久阻塞
- 始终通过 STDIN 管道传入规则配置，不在项目中写 `.json` 临时文件（避免残留文件污染项目）

## 观察模式

```bash
# 后台启动（阻塞进程，必须用平台后台机制执行）
python scripts/twist.py --launch --observe -u https://目标网站.com

# 只看 XHR/Fetch
python scripts/twist.py --launch --observe --observe-filter type=xhr,fetch -u https://example.com

# 只看含 "api" 的 URL
python scripts/twist.py --launch --observe --observe-filter url=api -u https://example.com

# 完整响应体（默认截断 4KB）
python scripts/twist.py --launch --observe --observe-full-body -u https://example.com

# 附加到已打开的浏览器页面（省略 -u，自动选第一个 tab）
python scripts/twist.py --observe
```

输出为 JSONL，每行一个事件，核心字段：`type`, `requestId`, `url`, `method`, `resourceType`, `requestHeaders`, `statusCode`, `body`, `bodyTruncated`。

**解读要点：** `resourceType` 区分 XHR/Fetch/Document；响应阶段才有 `statusCode` 和 `body`；`bodyTruncated: true` 表示被截断。

## 拦截模式

通过 STDIN 传入 JSON 规则配置：

```bash
# 启动浏览器 + 加载规则（阻塞进程，必须后台执行）
python scripts/twist.py --launch -u https://目标网站.com <<'EOF'
{"id":"cfg","name":"cfg","rules":[...]}
EOF

# 复用已有浏览器，页面已打开无需导航（省略 -u）
python scripts/twist.py <<'EOF'
{"id":"cfg","name":"cfg","rules":[...]}
EOF

# 复用已有浏览器更新规则（无需 --launch）
python scripts/twist.py -u https://目标网站.com <<'EOF'
{"id":"cfg","name":"cfg","rules":[...]}
EOF
```

## 规则结构

```json
{
  "id": "配置ID",
  "name": "配置名称",
  "version": "1.0",
  "rules": [
    {
      "id": "规则ID",
      "name": "规则描述",
      "enabled": true,
      "priority": 10,
      "stage": "request",
      "match": { "allOf": [...], "anyOf": [...] },
      "actions": [...]
    }
  ]
}
```

**规则要点：** `priority` 越大越优先；`allOf` 是 AND、`anyOf` 是 OR；`stage` 决定在 `request`（发请求前）还是 `response`（返回浏览器前）修改；首条匹配后不再检查后续规则。

## 条件速查

用户意图 → 条件类型。完整参数说明见 [references/conditions.md](references/conditions.md)。

| 用户说 | 条件 |
|--------|------|
| URL 等于/前缀/后缀/包含/正则 | `urlEquals` / `urlPrefix` / `urlSuffix` / `urlContains` / `urlRegex` |
| GET/POST 请求 | `method` + `values: ["GET"]` |
| XHR/JS 文件 | `resourceType` + `values: ["XHR"]` |
| 有/没有某个 Header | `headerExists` / `headerNotExists` |
| Header 等于/包含/正则 | `headerEquals` / `headerContains` / `headerRegex` |
| 有/没有某个 Query 参数 | `queryExists` / `queryNotExists` |
| Query 等于/包含/正则 | `queryEquals` / `queryContains` / `queryRegex` |
| 有/没有某个 Cookie | `cookieExists` / `cookieNotExists` |
| Cookie 等于/包含/正则 | `cookieEquals` / `cookieContains` / `cookieRegex` |
| 请求体包含字符串/JSONPath | `bodyContains` / `bodyJsonPath` |

## 动作速查

用户意图 → 动作。完整参数说明见 [references/actions.md](references/actions.md)。

| 用户说 | 动作 | 阶段 |
|--------|------|------|
| 拦截/屏蔽请求 | `block` | request |
| 修改 URL | `setUrl` | request |
| 改 HTTP 方法 | `setMethod` | request |
| 添加/修改/删除 Header | `setHeader` / `removeHeader` | request |
| 添加/修改/删除 Query | `setQueryParam` / `removeQueryParam` | request |
| 修改/删除 Cookie | `setCookie` / `removeCookie` | both |
| 修改/删除表单字段 | `setFormField` / `removeFormField` | request |
| 修改响应状态码 | `setStatus` | response |
| 替换/追加 Body | `setBody` / `appendBody` | both |
| 查找替换 Body 文本 | `replaceBodyText` | both |
| JSON Patch (RFC 6902) | `patchBodyJson` | both |
| 替换页面 HTML 元素 | `replaceElement` | response |

## 完整示例

### 屏蔽追踪请求

需求：「把所有发往 analytics 或 tracking 的请求都拦截掉」

先观察确认 URL 特征 → 再编写规则：

```json
{
  "id": "block-tracking",
  "name": "屏蔽追踪统计",
  "version": "1.0",
  "rules": [{
    "id": "rule-1",
    "name": "拦截分析请求",
    "enabled": true,
    "priority": 10,
    "stage": "request",
    "match": {
      "allOf": [{"type": "urlContains", "value": "analytics"}],
      "anyOf": [
        {"type": "urlContains", "value": "google"},
        {"type": "urlContains", "value": "tracking"}
      ]
    },
    "actions": [{"type": "block", "statusCode": 204}]
  }]
}
```

### Mock API 响应

需求：「把 `/api/users` 的返回值改成自定义 JSON」

```json
{
  "id": "mock-users",
  "name": "Mock 用户 API",
  "version": "1.0",
  "rules": [{
    "id": "rule-1",
    "name": "替换用户列表",
    "enabled": true,
    "priority": 10,
    "stage": "response",
    "match": {
      "allOf": [
        {"type": "urlContains", "value": "/api/users"},
        {"type": "method", "values": ["GET"]}
      ]
    },
    "actions": [
      {"type": "setHeader", "name": "Content-Type", "value": "application/json"},
      {"type": "setBody", "value": "{\"users\":[{\"id\":1,\"name\":\"测试用户\"}],\"total\":1}"}
    ]
  }]
}
```

## 参考文档

- [references/conditions.md](references/conditions.md) — 所有 25 种匹配条件的完整参数对照
- [references/actions.md](references/actions.md) — 所有 17 种动作的完整参数对照
- `examples/basic.json` — block 拦截 + Mock API 响应
- `examples/request-mod.json` — 请求阶段修改（setHeader、setUrl、setMethod）
- `examples/response-mod.json` — 响应阶段修改（setStatus、replaceBodyText、patchBodyJson、replaceElement）
- `examples/cookie-query.json` — Cookie 和 Query 参数修改（setCookie、removeCookie、setQueryParam、removeQueryParam）
- `examples/form-body.json` — 表单、Body 和 Header 修改（setFormField、removeFormField、appendBody、removeHeader）
- `examples/all-conditions.json` — 全部 25 种匹配条件类型示例

更多命令参数运行 `python scripts/twist.py --help` 查看。
