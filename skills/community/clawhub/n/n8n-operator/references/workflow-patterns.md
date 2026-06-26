# n8n 工作流模式参考

> 6 种经典工作流架构模式，每种包含完整 JSON 示例和设计要点。
> Agent 应根据用户需求选择匹配的模式，然后在此基础上定制。
> **所有示例已适配 n8n 2.x（移除 active/tags/staticData 等只读字段）。**

---

## 模式选择指南

| 你的需求 | 推荐模式 |
|----------|----------|
| 接收外部 HTTP 请求并处理 | 模式 1：Webhook 处理 |
| 定期从 API 拉取数据 | 模式 2：定时轮询 |
| 数据库之间的数据同步 | 模式 3：数据库 ETL |
| 对话式 AI / 智能客服 | 模式 4：AI Agent |
| 定时报表 / 定时清理 | 模式 5：定时任务 |
| 批量处理大量数据 | 模式 6：分批处理 |

---

## 模式 1：Webhook 处理（最常用）

**架构：**
```
Webhook → 验证 → 转换 → 响应/通知
```

**适用场景：**
- 接收表单提交
- GitHub/GitLab Webhook
- 第三方平台回调
- 构建 API 端点

**完整 JSON 示例：**

```json
{
  "name": "Webhook Handler - Notify and Store",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "process-order",
        "responseMode": "lastNode",
        "responseData": "lastNode",
        "options": {}
      },
      "id": "webhook-001",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "conditions": {
          "conditions": [
            {
              "id": "c1",
              "leftValue": "={{ $json.body.orderId }}",
              "rightValue": "",
              "operator": { "type": "string", "operation": "notEmpty" }
            }
          ],
          "combinator": "and"
        }
      },
      "id": "if-001",
      "name": "Validate Input",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [470, 300]
    },
    {
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            { "id": "a1", "name": "orderId", "value": "={{ $json.body.orderId }}", "type": "string" },
            { "id": "a2", "name": "status", "value": "pending", "type": "string" },
            { "id": "a3", "name": "receivedAt", "value": "={{ $now.toISO() }}", "type": "string" }
          ]
        },
        "options": {}
      },
      "id": "set-001",
      "name": "Format Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [690, 200]
    },
    {
      "parameters": {
        "channel": "#orders",
        "text": "={{ 'New order: ' + $json.orderId + ' received at ' + $json.receivedAt }}"
      },
      "id": "slack-001",
      "name": "Send Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.2,
      "position": [910, 200],
      "credentials": {
        "slackApi": { "id": "CREDENTIAL_ID", "name": "Slack" }
      }
    },
    {
      "parameters": {
        "jsCode": "return [{ json: { success: true, orderId: $json.orderId } }];"
      },
      "id": "respond-001",
      "name": "Success Response",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1130, 200]
    },
    {
      "parameters": {
        "jsCode": "return [{ json: { success: false, error: 'Missing orderId' } }];"
      },
      "id": "respond-002",
      "name": "Error Response",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [690, 400]
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Validate Input", "type": "main", "index": 0 }]] },
    "Validate Input": {
      "main": [
        [{ "node": "Format Data", "type": "main", "index": 0 }],
        [{ "node": "Error Response", "type": "main", "index": 0 }]
      ]
    },
    "Format Data": { "main": [[{ "node": "Send Slack", "type": "main", "index": 0 }]] },
    "Send Slack": { "main": [[{ "node": "Success Response", "type": "main", "index": 0 }]] }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

> **n8n 2.x 关键：** 此模式使用 `responseMode: "lastNode"`，最后一个 Code 节点的返回值自动成为 HTTP 响应。不需要 `respondToWebhook` 节点。

---

## 模式 2：定时轮询

**架构：**
```
Schedule → HTTP Request → IF(有新数据?) → Process → Notify
                                    → NoOp (无数据时跳过)
```

**适用场景：**
- 定期从外部 API 拉取数据
- 监控第三方服务状态
- 定期同步外部数据

**完整 JSON 示例：**

```json
{
  "name": "Scheduled API Polling",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{ "triggerAtHour": 9 }, { "triggerAtHour": 12 }, { "triggerAtHour": 18 }]
        }
      },
      "id": "schedule-001",
      "name": "3x Daily Poll",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "url": "https://api.example.com/orders?updated_after={{ $now.minus({days: 1}).toISO() }}",
        "method": "GET",
        "options": { "response": { "response": { "responseFormat": "json" } } }
      },
      "id": "http-001",
      "name": "Fetch Orders",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [470, 300],
      "credentials": {
        "httpHeaderAuth": { "id": "CREDENTIAL_ID", "name": "API Auth" }
      }
    },
    {
      "parameters": {
        "conditions": {
          "conditions": [
            {
              "id": "c1",
              "leftValue": "={{ $json.data.length }}",
              "rightValue": 0,
              "operator": { "type": "number", "operation": "larger" }
            }
          ],
          "combinator": "and"
        }
      },
      "id": "if-001",
      "name": "Has New Data?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [690, 300]
    },
    {
      "parameters": {},
      "id": "noop-001",
      "name": "No New Data",
      "type": "n8n-nodes-base.noOp",
      "typeVersion": 1,
      "position": [910, 420]
    },
    {
      "parameters": {
        "jsCode": "const items = $input.first().json.data;\nreturn items.map(item => ({ json: item }));"
      },
      "id": "code-001",
      "name": "Split Items",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [910, 200]
    },
    {
      "parameters": {
        "channel": "#updates",
        "text": "={{ 'Processed ' + $input.all().length + ' new orders' }}"
      },
      "id": "slack-001",
      "name": "Notify",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.2,
      "position": [1130, 200],
      "credentials": {
        "slackApi": { "id": "CREDENTIAL_ID", "name": "Slack" }
      }
    }
  ],
  "connections": {
    "3x Daily Poll": { "main": [[{ "node": "Fetch Orders", "type": "main", "index": 0 }]] },
    "Fetch Orders": { "main": [[{ "node": "Has New Data?", "type": "main", "index": 0 }]] },
    "Has New Data?": {
      "main": [
        [{ "node": "Split Items", "type": "main", "index": 0 }],
        [{ "node": "No New Data", "type": "main", "index": 0 }]
      ]
    },
    "Split Items": { "main": [[{ "node": "Notify", "type": "main", "index": 0 }]] }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

---

## 模式 3：数据库 ETL

**架构：**
```
Schedule → Read DB → Transform → Write DB → Log
```

**适用场景：**
- 数据库之间数据同步
- 数据清洗和转换
- 定期数据导出

**完整 JSON 示例：**

```json
{
  "name": "Database ETL Pipeline",
  "nodes": [
    {
      "parameters": {
        "rule": { "interval": [{ "triggerAtHour": 2, "triggerAtMinute": 0 }] }
      },
      "id": "schedule-001",
      "name": "Daily 2 AM",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT id, name, email, created_at FROM users WHERE updated_at > NOW() - INTERVAL '1 day'",
        "options": {}
      },
      "id": "postgres-001",
      "name": "Read Source",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2.6,
      "position": [470, 300],
      "credentials": {
        "postgres": { "id": "CREDENTIAL_ID", "name": "Source DB" }
      }
    },
    {
      "parameters": {
        "jsCode": "return $input.all().map(item => {\n  const d = item.json;\n  return {\n    json: {\n      user_id: d.id,\n      full_name: d.name.toUpperCase(),\n      email_lower: d.email.toLowerCase(),\n      sync_time: $now.toISO()\n    }\n  };\n});"
      },
      "id": "code-001",
      "name": "Transform",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [690, 300]
    },
    {
      "parameters": {
        "operation": "insert",
        "table": "synced_users",
        "columns": "user_id,full_name,email_lower,sync_time",
        "values": "={{ $json.user_id }},{{ $json.full_name }},{{ $json.email_lower }},{{ $json.sync_time }}",
        "options": {}
      },
      "id": "mysql-001",
      "name": "Write Target",
      "type": "n8n-nodes-base.mySql",
      "typeVersion": 2.4,
      "position": [910, 300],
      "credentials": {
        "mySql": { "id": "CREDENTIAL_ID", "name": "Target DB" }
      }
    },
    {
      "parameters": {
        "text": "={{ 'ETL complete: synced ' + $input.all().length + ' users' }}"
      },
      "id": "slack-001",
      "name": "Log Result",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.2,
      "position": [1130, 300],
      "credentials": {
        "slackApi": { "id": "CREDENTIAL_ID", "name": "Slack" }
      }
    }
  ],
  "connections": {
    "Daily 2 AM": { "main": [[{ "node": "Read Source", "type": "main", "index": 0 }]] },
    "Read Source": { "main": [[{ "node": "Transform", "type": "main", "index": 0 }]] },
    "Transform": { "main": [[{ "node": "Write Target", "type": "main", "index": 0 }]] },
    "Write Target": { "main": [[{ "node": "Log Result", "type": "main", "index": 0 }]] }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

---

## 模式 4：AI Agent 工作流

**架构：**
```
Chat Trigger → AI Agent(Model + Memory + Tools) → Response
```

**适用场景：**
- 智能客服
- 文档问答
- 多步推理任务

**完整 JSON 示例：**

```json
{
  "name": "AI Chat Agent",
  "nodes": [
    {
      "parameters": { "options": {} },
      "id": "chat-001",
      "name": "Chat Trigger",
      "type": "n8n-nodes-base.chatTrigger",
      "typeVersion": 1.1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "agent": "conversationalAgent",
        "promptType": "define",
        "text": "You are a helpful assistant. Answer the user's question based on the available tools.",
        "hasMemory": true,
        "options": {}
      },
      "id": "agent-001",
      "name": "AI Agent",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.6,
      "position": [470, 300]
    },
    {
      "parameters": {
        "model": "gpt-4o",
        "options": {
          "temperature": 0.7,
          "maxTokens": 2048
        }
      },
      "id": "model-001",
      "name": "OpenAI Model",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "typeVersion": 1.6,
      "position": [250, 480],
      "credentials": {
        "openAiApi": { "id": "CREDENTIAL_ID", "name": "OpenAI" }
      }
    },
    {
      "parameters": {
        "windowSize": 10
      },
      "id": "memory-001",
      "name": "Window Buffer Memory",
      "type": "@n8n/n8n-nodes-langchain.bufferWindowMemory",
      "typeVersion": 1.1,
      "position": [470, 480]
    }
  ],
  "connections": {
    "Chat Trigger": {
      "main": [[{ "node": "AI Agent", "type": "main", "index": 0 }]]
    },
    "AI Agent": {
      "ai_languageModel": [[{ "node": "OpenAI Model", "type": "ai_languageModel", "index": 0 }]],
      "ai_memory": [[{ "node": "Window Buffer Memory", "type": "ai_memory", "index": 0 }]]
    }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

**AI 连接类型说明：**

| 连接类型 | key | 用途 |
|----------|-----|------|
| `ai_languageModel` | 模型连接 | OpenAI, Anthropic, 本地模型等 |
| `ai_memory` | 记忆连接 | BufferMemory, WindowBufferMemory 等 |
| `ai_tool` | 工具连接 | HTTP Request, Calculator, Code 等 |
| `ai_chain` | 链连接 | 嵌套链 |

---

## 模式 5：定时任务

**架构：**
```
Schedule → Fetch Data → Process → Format → Send Report
```

**适用场景：**
- 每日/每周报表
- 定期数据备份
- 定期清理任务

**完整 JSON 示例：**

```json
{
  "name": "Daily Report Generator",
  "nodes": [
    {
      "parameters": {
        "rule": { "interval": [{ "triggerAtHour": 9, "triggerAtMinute": 0 }] }
      },
      "id": "schedule-001",
      "name": "Daily 9 AM",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "url": "https://api.example.com/metrics?date={{ $now.minus({days: 1}).format('yyyy-MM-dd') }}",
        "method": "GET",
        "options": { "response": { "response": { "responseFormat": "json" } } }
      },
      "id": "http-001",
      "name": "Fetch Metrics",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [470, 300],
      "credentials": {
        "httpHeaderAuth": { "id": "CREDENTIAL_ID", "name": "API Auth" }
      }
    },
    {
      "parameters": {
        "jsCode": "const data = $input.first().json;\nconst report = {\n  date: $now.minus({days: 1}).format('yyyy-MM-dd'),\n  totalUsers: data.totalUsers,\n  activeUsers: data.activeUsers,\n  revenue: data.revenue\n};\nreturn [{ json: report }];"
      },
      "id": "code-001",
      "name": "Build Report",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [690, 300]
    },
    {
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            { "id": "a1", "name": "report", "value": "={{ '*Daily Report - ' + $json.date + '*\\n\\nUsers: ' + $json.totalUsers + ' (Active: ' + $json.activeUsers + ')\\nRevenue: $' + $json.revenue }}", "type": "string" }
          ]
        },
        "options": {}
      },
      "id": "set-001",
      "name": "Format Message",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [910, 300]
    },
    {
      "parameters": {
        "channel": "#daily-reports",
        "text": "={{ $json.report }}"
      },
      "id": "slack-001",
      "name": "Send to Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.2,
      "position": [1130, 300],
      "credentials": {
        "slackApi": { "id": "CREDENTIAL_ID", "name": "Slack" }
      }
    }
  ],
  "connections": {
    "Daily 9 AM": { "main": [[{ "node": "Fetch Metrics", "type": "main", "index": 0 }]] },
    "Fetch Metrics": { "main": [[{ "node": "Build Report", "type": "main", "index": 0 }]] },
    "Build Report": { "main": [[{ "node": "Format Message", "type": "main", "index": 0 }]] },
    "Format Message": { "main": [[{ "node": "Send to Slack", "type": "main", "index": 0 }]] }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

---

## 模式 6：分批处理 ⚠️ 含 Wait 节点风险

**架构：**
```
Trigger → Split In Batches → Process Each Batch → Delay → (循环回 Split)
                                      ↓ (done)
                                 Aggregate
```

**适用场景：**
- 批量发送通知
- 大量数据 API 写入（受 API 速率限制）
- 批量数据库更新

> ⚠️ **Wait 节点风险警告：** Wait for Callback 节点可能导致工作流无法激活。以下示例使用简单延迟 Wait，风险较低。如果遇到激活问题，改用 Code 节点的 `setTimeout` 替代。

**完整 JSON 示例：**

```json
{
  "name": "Batch Processing - Send Notifications",
  "nodes": [
    {
      "parameters": {},
      "id": "manual-001",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "jsCode": "const users = [\n  { id: 1, email: 'user1@example.com', name: 'Alice' },\n  { id: 2, email: 'user2@example.com', name: 'Bob' },\n  { id: 3, email: 'user3@example.com', name: 'Charlie' },\n  { id: 4, email: 'user4@example.com', name: 'Diana' },\n  { id: 5, email: 'user5@example.com', name: 'Eve' }\n];\nreturn users.map(u => ({ json: u }));"
      },
      "id": "code-001",
      "name": "Generate User List",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [470, 300]
    },
    {
      "parameters": { "batchSize": 2, "options": {} },
      "id": "split-001",
      "name": "Split In Batches",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [690, 300]
    },
    {
      "parameters": {
        "jsCode": "const users = $input.all();\nreturn [{ json: { batch: users.map(u => u.json.email).join(', '), count: users.length } }];"
      },
      "id": "code-002",
      "name": "Format Batch",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [910, 300]
    },
    {
      "parameters": {
        "channel": "#notifications",
        "text": "={{ 'Sending notification to: ' + $json.batch + ' (' + $json.count + ' users)' }}"
      },
      "id": "slack-001",
      "name": "Send Batch Notification",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2.2,
      "position": [1130, 300],
      "credentials": {
        "slackApi": { "id": "CREDENTIAL_ID", "name": "Slack" }
      }
    },
    {
      "parameters": {
        "jsCode": "await new Promise(r => setTimeout(r, 1000));\nreturn $input.all();"
      },
      "id": "delay-001",
      "name": "Rate Limit Delay",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [910, 500]
    }
  ],
  "connections": {
    "Manual Trigger": { "main": [[{ "node": "Generate User List", "type": "main", "index": 0 }]] },
    "Generate User List": { "main": [[{ "node": "Split In Batches", "type": "main", "index": 0 }]] },
    "Split In Batches": {
      "main": [
        [],
        [{ "node": "Format Batch", "type": "main", "index": 0 }]
      ]
    },
    "Format Batch": { "main": [[{ "node": "Send Batch Notification", "type": "main", "index": 0 }]] },
    "Send Batch Notification": { "main": [[{ "node": "Rate Limit Delay", "type": "main", "index": 0 }]] },
    "Rate Limit Delay": { "main": [[{ "node": "Split In Batches", "type": "main", "index": 0 }]] }
  },
  "settings": {
    "saveManualExecutions": true,
    "executionOrder": "v1"
  }
}
```

**Split In Batches 的连接关键点：**
- `main[0]`（done 输出）连接到"全部完成后的处理"（本例为空 = 不做后续处理）
- `main[1]`（each batch 输出）连接到循环体
- 循环体最后一个节点必须连回 Split In Batches 形成循环

**替代 Wait 节点的方案：** 用 Code 节点 `await new Promise(r => setTimeout(r, 1000))` 替代 Wait 节点，避免激活问题。

---

## 工作流创建检查清单

### 规划阶段
- [ ] 明确工作流的目的和触发方式
- [ ] 选择合适的架构模式
- [ ] 列出所有需要的节点
- [ ] 规划数据流和错误处理
- [ ] 确认需要哪些凭证

### 构建阶段
- [ ] 检查 N8N_BASE_URL 和 N8N_API_KEY 连通性
- [ ] 查询现有工作流避免重复
- [ ] 创建空工作流骨架，获取 workflow_id
- [ ] 逐步添加节点（每次 1-3 个）
- [ ] 正确建立节点连接
- [ ] 所有凭证引用使用正确的 ID

### 验证阶段
- [ ] GET 工作流确认 JSON 结构正确
- [ ] 每个节点的 name 在 connections 中正确引用
- [ ] Webhook 路径唯一不冲突
- [ ] 错误处理已配置（Error Workflow 或 continueOnFail）
- [ ] 不包含只读字段（active/tags/staticData/shared/pinData）

### 交付阶段
- [ ] 激活工作流（POST /activate）
- [ ] 等待 1-2 秒确保路由注册
- [ ] 提供工作流 ID
- [ ] 提供 Webhook URL（如有）
- [ ] 展示首次执行结果
