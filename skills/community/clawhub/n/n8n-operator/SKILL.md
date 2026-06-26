---
name: n8n-operator
version: 2.0.0
description: n8n 工作流助手 - 通过 REST API 设计、创建、修改和管理 n8n 工作流。适合：自动化工程师、DevOps、流程编排。
metadata:
  openclaw:
    emoji: "⚙️"
    requires:
      bins: ["curl"]
      env: ["N8N_BASE_URL", "N8N_API_KEY"]
---

# n8n 工作流助手

> 通过 n8n REST API 设计、创建、修改和管理工作流。无需 MCP，纯 REST API 调用即可完全操控 n8n。

## 元信息

- **Name:** n8n-operator
- **Version:** 2.0.0
- **Author:** AI-generated for OpenClaw
- **License:** MIT
- **Dependencies:** n8n 2.x 实例 + API Key
- **Tested on:** n8n 2.14.0 (Docker, 2026-04-14)

---

## n8n 2.x 关键差异（实测验证，必须遵守）

> 以下规则经过真实 n8n 2.x 实例验证，违反任一条都会导致 API 报错。

1. **`active` 是只读字段** — 创建/更新时不传 `active`
2. **`tags` / `staticData` 是只读字段** — 创建时不传
3. **`shared` / `activeVersion` / `pinData` 是只读字段** — PUT 更新时不传
4. **激活用专用端点** — `POST /api/v1/workflows/{id}/activate`（body: `{}`）
5. **PUT 是全量替换** — 只传 `name`/`nodes`/`connections`/`settings`，否则 `must NOT have additional properties`
6. **PATCH 不支持** — n8n 2.x 返回 `PATCH method not allowed`
7. **Webhook lastNode 模式** — `responseMode: "lastNode"` 时，最后一个节点返回值自动作为 HTTP 响应，**不要加 `respondToWebhook` 节点**
8. **激活后等待 1-2 秒** — 再触发 Webhook，确保路由注册完成

---

## 何时激活

当用户请求以下操作时，自动激活此 Skill：

- 创建/修改/删除 n8n 工作流
- 激活/停用/执行 n8n 工作流
- 查看 n8n 工作流列表或执行记录
- 添加节点、连接节点
- 设计自动化流程
- 任何涉及 n8n 的请求

---

## 前置条件

### 环境变量

```
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=<your-api-key>
```

获取 API Key：n8n 界面 → Settings → API → Create an API Key

### 认证方式

所有 API 请求必须携带：
```
X-N8N-API-KEY: <N8N_API_KEY>
Content-Type: application/json
```

### 连通性检查

```bash
curl -s -o /dev/null -w "%{http_code}" -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows"
```
- `200` → 正常 | `401` → Key 无效 | `000` → 网络不通

---

## 核心工作流

Agent 必须严格遵循以下 4 阶段：

### 阶段 1：理解需求
1. 确认工作流目的和功能
2. 识别触发方式（Webhook / Schedule / Manual）
3. 列出节点和数据流向
4. 确认后进入下一阶段

### 阶段 2：规划设计
1. 从 [workflow-patterns.md](references/workflow-patterns.md) 选择架构模式
2. 绘制节点连接图
3. 从 [node-templates.md](references/node-templates.md) 选择节点配置
4. 规划错误处理策略
5. 展示设计方案，等待确认

### 阶段 3：逐步构建

```
Step 1: 创建空骨架 → 获取 workflow_id
Step 2: 逐个添加节点（每次 1-3 个）
Step 3: 建立节点连接
Step 4: GET 验证完整工作流
Step 5: 激活（用户确认后）
```

### 阶段 4：验证交付
1. 确认已激活
2. 提供 Webhook URL
3. 展示测试结果
4. 记录 workflow_id

---

## API 速查

### 基础 URL

```
{N8N_BASE_URL}/api/v1
```

### 工作流管理

| 操作 | 方法 | 端点 |
|------|------|------|
| 列表 | `GET` | `/workflows?active=true&limit=50` |
| 详情 | `GET` | `/workflows/{id}` |
| 创建 | `POST` | `/workflows` |
| 更新 | `PUT` | `/workflows/{id}`（全量替换） |
| 删除 | `DELETE` | `/workflows/{id}` |
| 激活 | `POST` | `/workflows/{id}/activate` |
| 停用 | `POST` | `/workflows/{id}/deactivate` |
| 执行 | `POST` | `/workflows/{id}/execute` |

### 凭证管理

| 操作 | 方法 | 端点 |
|------|------|------|
| 列表 | `GET` | `/credentials` |
| 创建 | `POST` | `/credentials` |

### 执行记录

| 操作 | 方法 | 端点 |
|------|------|------|
| 列表 | `GET` | `/executions?workflowId={id}&status=error&limit=20` |
| 详情 | `GET` | `/executions/{id}` |
| 重试 | `POST` | `/executions/{id}/retry` |

### 常用 curl 示例

```bash
# 列出所有工作流
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows?limit=50"

# 获取单个工作流
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows/123"

# 激活
curl.exe -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" -d "{}" "$N8N_BASE_URL/api/v1/workflows/123/activate"

# 停用
curl.exe -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows/123/deactivate"

# 删除
curl -s -X DELETE -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows/123"

# 手动执行
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" -H "Content-Type: application/json" -d '{"data": {"key": "value"}}' "$N8N_BASE_URL/api/v1/workflows/123/execute"
```

> **Windows 注意：** PowerShell 的 `curl` 是 `Invoke-WebRequest` 别名，用 `curl.exe` 调用真正的 curl。

---

## 节点数据结构

```json
{
  "parameters": {},
  "id": "unique-uuid",
  "name": "Node Display Name",
  "type": "n8n-nodes-base.xxx",
  "typeVersion": 1,
  "position": [250, 300],
  "credentials": {},
  "disabled": false
}
```

**关键规则：**
1. `type` 始终用完整格式 `n8n-nodes-base.xxx`
2. `id` 用 UUID v4
3. `name` 既是显示名称，也是 `connections` 中引用的 key
4. 建议位置间距：x=220, y=200

---

## 连接数据结构

```json
{
  "SourceNodeName": {
    "main": [
      [
        { "node": "TargetNodeName", "type": "main", "index": 0 }
      ]
    ]
  }
}
```

**三层嵌套：**
```
{源节点} → {输出类型} → [[{目标列表}]]
```

**常见模式：**

线性（A→B→C）：
```json
{"A":{"main":[[{"node":"B","type":"main","index":0}]]}},
{"B":{"main":[[{"node":"C","type":"main","index":0}]]}}
```

分支（IF→true/false）：
```json
{"IF":{"main":[[{"node":"True","type":"main","index":0}],[{"node":"False","type":"main","index":0}]]}}
```

并行（A→B+C→D）：
```json
{"A":{"main":[[{"node":"B","type":"main","index":0},{"node":"C","type":"main","index":0}]]}}
```

---

## n8n 表达式语法速查

在 `parameters` 中使用 `={{ }}` 嵌入动态值。

| 变量 | 用途 | 示例 |
|------|------|------|
| `$json` | 当前节点输入 | `{{ $json.email }}` |
| `$json.body` | Webhook 请求体 | `{{ $json.body.data }}` |
| `$json.query` | URL 查询参数 | `{{ $json.query.page }}` |
| `$node["Name"].json` | 引用指定节点输出 | `{{ $node["HTTP"].json.data }}` |
| `$now` | 当前时间 | `{{ $now.toISO() }}` |
| `$env` | 环境变量 | `{{ $env.MY_VAR }}` |
| `$input.first()` | 第一个输入项 | `{{ $input.first().json.name }}` |

**Webhook 陷阱：** POST 请求体在 `$json.body` 下，不是直接在 `$json` 下。

---

## HTTP Request 节点正确配置（实测关键）

发送 JSON body 的正确配置：

```json
{
  "parameters": {
    "sendBody": true,
    "specifyBody": "json",
    "jsonParameters": false,
    "jsonBody": "={{ JSON.stringify({key: 'value'}) }}"
  }
}
```

**关键：`jsonParameters: false` 是必须的！设为 `true` 直接崩溃。**

| 参数 | 值 | 说明 |
|------|-----|------|
| `sendBody` | `true` | 启用请求体 |
| `specifyBody` | `"json"` | JSON 格式 |
| `jsonParameters` | **`false`** | 必须为 false |
| `jsonBody` | `"={{ ... }}"` | 用表达式传递 |

---

## Gateway Cron 自动触发 n8n Webhook

当需要 OpenClaw 定时自动触发 n8n 工作流时：

**方法：直接编辑 jobs.json 文件**

```
路径：C:\Users\lujun\.openclaw\cron\jobs.json
```

在 jobs.json 中添加 cron 任务，通过 `curl.exe POST` 触发 n8n webhook URL。

**关键经验：**
- isolated session 才能正常执行完整流程（主 session 会跳过 system-event）
- 直接编辑文件比 CLI/API 更可靠
- 已配置过的 webhook 路径不要反复问用户，直接查历史记录

---

## 微信公众号 API 限制速查

通过 n8n 调用微信公众号草稿 API 时的限制：

| 限制项 | 字节数 | 中文数 | 说明 |
|--------|--------|--------|------|
| title | ≤ 20字节 | ≤ 10个 | 超过报 45003 |
| digest | ≤ 54字节 | ≤ 25个 | 超过报 45004 |
| thumb_media_id | 不能为空 | — | 先上传封面获取 |

**access_token** 有效期 7200 秒，每次发草稿前重新获取，不缓存复用。

---

## 错误处理策略

### 工作流级错误处理
```json
{
  "settings": {
    "executionOrder": "v1",
    "errorWorkflow": "error-handler-workflow-id"
  }
}
```

### 节点级错误处理
```json
{
  "name": "HTTP Request",
  "continueOnFail": true
}
```

### Error Trigger
```json
{
  "type": "n8n-nodes-base.errorTrigger",
  "typeVersion": 1
}
```

---

## 工作流设计原则

### 核心原则：防静默失败

#### 1. 幂等性
- 用什么字段判断重复？（唯一 ID / 时间戳+业务ID）
- 重试不产生重复记录

#### 2. 可观测性
- 生成 run_id 贯穿全程
- 记录每个关键节点状态

#### 3. 重试 + backoff
- 1s → 2s → 4s 递增间隔
- 最大 3 次，超过 → 人工审核队列

#### 4. No Silent Failure
- 关键计数/阈值不达标 → 立即停止并告警

### 设计检查清单
- [ ] 触发类型
- [ ] 输入 schema 和必填字段
- [ ] dedup key 是什么？
- [ ] 错误重试策略
- [ ] 哪些情况路由人工审核？
- [ ] credential 通过引用，不硬编码？

---

## Agent 操作规范

### 必须遵守
1. **先确认再操作** — 设计方案展示给用户
2. **逐步构建** — 每步 1-3 个节点
3. **每次修改后验证** — GET 确认
4. **使用描述性节点名称**
5. **记录 workflow_id**
6. **先查后建** — 避免重复

### 禁止事项
- 不跳过设计阶段直接创建
- 不在 connections 中使用节点 ID（必须用 name）
- 不硬编码凭证密码
- 不跳过连通性检查
- 不修改正在运行的工作流（先停用）
- 不使用 `n8n-nodes-base.function`（v1，已弃用），用 `n8n-nodes-base.code`（v2）

---

## 完整示例：Webhook Echo

```json
{
  "name": "Webhook Echo",
  "nodes": [
    {
      "id": "a1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [0, 0],
      "parameters": {
        "httpMethod": "POST",
        "path": "echo",
        "responseMode": "lastNode",
        "responseData": "lastNode",
        "options": {}
      }
    },
    {
      "id": "a2",
      "name": "Process & Respond",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [250, 0],
      "parameters": {
        "jsCode": "return [{ json: { received: $json.body, processed: true, time: new Date().toISOString() } }];"
      }
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Process & Respond", "type": "main", "index": 0 }]] }
  },
  "settings": { "saveManualExecutions": true, "executionOrder": "v1" }
}
```

**激活 + 测试：**
```bash
# 创建（自动获取 id）
# 激活（等 1-2 秒）
curl.exe -s -X POST -H "X-N8N-API-KEY: %N8N_API_KEY%" -H "Content-Type: application/json" -d "{}" "%N8N_BASE_URL%/api/v1/workflows/{id}/activate"

# 触发
curl.exe -s -X POST -H "Content-Type: application/json" -d "{\"hello\":\"world\"}" "%N8N_BASE_URL%/webhook/echo"
```

---

## 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 401 | API Key 无效 | 重新生成 |
| 400 `active is read-only` | 传了 `active` | 不传，用 POST /activate |
| 400 `tags is read-only` | 传了 `tags` | 不传 |
| 400 `must NOT have additional properties` | PUT 传了额外字段 | 只传 name/nodes/connections/settings |
| 405 `PATCH method not allowed` | n8n 2.x 不支持 | 用 PUT 全量替换 |
| 500 `Unused Respond to Webhook node` | lastNode 模式下用了 respondToWebhook | 删掉，用 Code 节点返回 |
| Webhook 404 | 激活后立即触发 | 等 1-2 秒 |
| Wait 节点导致激活失败 | Wait for Callback 配置问题 | 用 Code + setTimeout 替代 |
| HTTP Request 崩溃 | `jsonParameters: true` | 改为 `false` |
| 微信 45003 | title 超字节 | title[:10] |
| 微信 45004 | digest 超字节 | digest[:25] |
| 微信草稿无封面 | thumb_media_id 为空 | 先上传获取 media_id |
| Webhook 路径 404 | 用了 path 参数而非 webhookId | 用 webhookId 触发 |

---

## 实战教训汇总

### ❌ `fs` 模块被屏蔽导致文件写入失败
**解决：** 用 ReadWriteFile 节点 + Binary 数据，详见 [desktop-write.md](references/desktop-write.md)

### ❌ Wait 节点导致激活失败
**解决：** 用 Code 节点 + `await new Promise(r => setTimeout(r, 5000))` 替代

### ❌ HTTP Request jsonParameters
**解决：** 必须设为 `false`，`true` 直接崩溃

### ❌ 微信 API 字节限制
**解决：** title[:10] / digest[:25]，每次发草稿前重新获取 token

### ❌ PUT 后节点消失
**解决：** PUT 全量替换，必须包含全部节点

### ❌ Webhook URL 格式
**解决：** n8n 2.x 用 `{webhookId}` 触发，不是 path 参数

### ❌ 同一问题试错超过 3 次
**解决：** 停下来搜索文档/社区，分析根因，针对性解决

---

## 试错规则

同一问题试错超过 3 次 → 必须停止：
1. 搜索文档/社区找类似问题
2. 剖析错误根本原因
3. 制定针对性方案
4. 验证后记录

---

## 性能与监控

### 健康检查
```bash
ACTIVE=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/workflows?active=true" | jq ".data | length")
FAILED=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" "$N8N_BASE_URL/api/v1/executions?status=error&limit=100" | jq "[.data[] | select(.startedAt > (now - 86400 | todate))] | length")
echo "Active: $ACTIVE | Failed(24h): $FAILED"
```

### Python 工具
```bash
python3 scripts/n8n_api.py list-workflows --active true --pretty
python3 scripts/n8n_api.py list-executions --limit 10 --pretty
python3 scripts/n8n_optimizer.py analyze --id <id> --pretty
python3 scripts/n8n_tester.py validate --id <id> --pretty
```

---

## 参考文件

- **[node-templates.md](references/node-templates.md)** — 30+ 常用节点 JSON 模板
- **[workflow-patterns.md](references/workflow-patterns.md)** — 6 种经典架构模式
- **[desktop-write.md](references/desktop-write.md)** — n8n 写入 Windows 桌面文件（2026-04-21 实测）
