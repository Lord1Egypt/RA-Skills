# n8n 节点模板参考

> 30+ 常用节点的完整 JSON 模板，可直接复制到工作流的 `nodes` 数组中。
> 每个模板包含最常用的参数配置，位置坐标需根据实际布局调整。

---

## 一、触发器节点（Triggers）

### 1. Webhook（Webhook 触发器）

```json
{
  "parameters": {
    "httpMethod": "POST",
    "path": "my-endpoint",
    "responseMode": "lastNode",
    "responseData": "lastNode",
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Webhook",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "position": [250, 300]
}
```

**responseMode 选项（n8n 2.x）：**
- `lastNode` — 等工作流执行完后返回最后一个节点的输出（**推荐**）
- `onReceived` — 立即响应 200（异步场景）
- `responseNode` — 使用 Respond to Webhook 节点自定义响应（⚠️ n8n 2.x 中容易报 `Unused Respond to Webhook node found` 错误，不推荐）

### 2. Schedule（定时触发器）

```json
{
  "parameters": {
    "rule": {
      "interval": [
        {
          "triggerAtHour": 8,
          "triggerAtMinute": 0
        }
      ]
    }
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Schedule",
  "type": "n8n-nodes-base.scheduleTrigger",
  "typeVersion": 1.2,
  "position": [250, 300]
}
```

**rule 常用模式：**
- 每小时：`{"interval": [{"triggerAtHour": 0, "triggerAtMinute": 0}]}`
- 每天 8:00：`{"interval": [{"triggerAtHour": 8, "triggerAtMinute": 0}]}`
- 每 5 分钟：`{"interval": [{"minutes": 5}]}`
- Cron 表达式：`{"interval": [{"field": "cronExpression", "expression": "0 8 * * 1-5"}]}`

### 3. Manual（手动触发）

```json
{
  "parameters": {},
  "id": "REPLACE-WITH-UUID",
  "name": "Manual Trigger",
  "type": "n8n-nodes-base.manualTrigger",
  "typeVersion": 1,
  "position": [250, 300]
}
```

### 4. Error Trigger（错误触发器）

```json
{
  "parameters": {},
  "id": "REPLACE-WITH-UUID",
  "name": "Error Trigger",
  "type": "n8n-nodes-base.errorTrigger",
  "typeVersion": 1,
  "position": [250, 300]
}
```

### 5. Chat Trigger（聊天触发器）

```json
{
  "parameters": {
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Chat Trigger",
  "type": "n8n-nodes-base.chatTrigger",
  "typeVersion": 1.1,
  "position": [250, 300]
}
```

---

## 二、数据转换节点（Transform）

### 6. Set（设置/映射字段）

```json
{
  "parameters": {
    "mode": "manual",
    "duplicateItem": false,
    "assignments": {
      "assignments": [
        {
          "id": "field-1",
          "name": "newField",
          "value": "={{ $json.body.data }}",
          "type": "string"
        }
      ]
    },
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Set Fields",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3.4,
  "position": [470, 300]
}
```

### 7. IF（条件分支）

```json
{
  "parameters": {
    "conditions": {
      "options": {
        "caseSensitive": true,
        "leftValue": "",
        "typeValidation": "strict"
      },
      "conditions": [
        {
          "id": "condition-1",
          "leftValue": "={{ $json.status }}",
          "rightValue": "success",
          "operator": {
            "type": "string",
            "operation": "equals",
            "name": "filter.operator.equals"
          }
        }
      ],
      "combinator": "and"
    }
  },
  "id": "REPLACE-WITH-UUID",
  "name": "IF",
  "type": "n8n-nodes-base.if",
  "typeVersion": 2,
  "position": [470, 300]
}
```

**connections 中 IF 的两个输出：**
```json
{
  "IF": {
    "main": [
      [{ "node": "SuccessHandler", "type": "main", "index": 0 }],
      [{ "node": "ErrorHandler", "type": "main", "index": 0 }]
    ]
  }
}
```

### 8. Switch（多路分支）

```json
{
  "parameters": {
    "dataType": "string",
    "value1": "={{ $json.type }}",
    "rules": {
      "rules": [
        {
          "value2": "email",
          "outputKey": "email"
        },
        {
          "value2": "sms",
          "outputKey": "sms"
        }
      ]
    },
    "fallbackOutput": 1
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Switch",
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3,
  "position": [470, 300]
}
```

### 9. Code JavaScript（JavaScript 代码节点）

```json
{
  "parameters": {
    "jsCode": "// 访问输入数据\nconst items = $input.all();\nconst results = items.map(item => {\n  const data = item.json;\n  return {\n    json: {\n      processed: true,\n      originalField: data.someField,\n      newField: data.someField.toUpperCase()\n    }\n  };\n});\nreturn results;"
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Code",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [470, 300]
}
```

**Code 节点关键规则：**
- 输入：`$input.all()` 获取所有项，`$input.first()` 获取第一项
- Webhook 数据：`$input.first().json.body.xxx`
- 输出：必须返回 `[{json: {...}}]` 格式的数组
- 内置函数：`$helpers.httpRequest()`, `DateTime`, `$jmespath()`

### 10. Merge（合并数据）

```json
{
  "parameters": {
    "mode": "append"
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Merge",
  "type": "n8n-nodes-base.merge",
  "typeVersion": 3,
  "position": [690, 300]
}
```

**合并模式：**
- `append` — 顺序追加
- `combine` — 按位置合并
- `combineByField` — 按字段匹配合并
- `keepKeyMatches` — 保留匹配项（集合交集）

### 11. Split In Batches（分批处理）

```json
{
  "parameters": {
    "batchSize": 50,
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Split In Batches",
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 3,
  "position": [470, 300]
}
```

**⚠️ 重要：Split In Batches 有两个输出：**
- `main[0]` = done（所有批次完成后触发一次）
- `main[1]` = each batch（每个批次触发一次，这是循环体）

### 12. Filter（过滤数据）

```json
{
  "parameters": {
    "conditions": {
      "conditions": [
        {
          "id": "condition-1",
          "leftValue": "={{ $json.status }}",
          "rightValue": "active",
          "operator": {
            "type": "string",
            "operation": "equals"
          }
        }
      ],
      "combinator": "and"
    },
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Filter",
  "type": "n8n-nodes-base.filter",
  "typeVersion": 2,
  "position": [470, 300]
}
```

---

## 三、通信节点（Communication）

### 13. Slack（发送消息）

```json
{
  "parameters": {
    "resource": "message",
    "operation": "send",
    "channel": "#general",
    "text": "={{ $json.message }}",
    "otherOptions": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Slack",
  "type": "n8n-nodes-base.slack",
  "typeVersion": 2.2,
  "position": [690, 300],
  "credentials": {
    "slackApi": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "Slack account"
    }
  }
}
```

### 14. Email Send（发送邮件）

```json
{
  "parameters": {
    "fromEmail": "noreply@example.com",
    "toEmail": "={{ $json.email }}",
    "subject": "Notification",
    "text": "={{ $json.body }}",
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Send Email",
  "type": "n8n-nodes-base.emailSend",
  "typeVersion": 2.1,
  "position": [690, 300],
  "credentials": {
    "smtp": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "SMTP account"
    }
  }
}
```

### 15. Telegram（发送消息）

```json
{
  "parameters": {
    "resource": "message",
    "operation": "send",
    "chatId": "REPLACE-WITH-CHAT-ID",
    "text": "={{ $json.message }}",
    "additionalFields": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Telegram",
  "type": "n8n-nodes-base.telegram",
  "typeVersion": 1.2,
  "position": [690, 300],
  "credentials": {
    "telegramApi": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "Telegram API"
    }
  }
}
```

### 16. WeChat Work（企业微信）

```json
{
  "parameters": {
    "resource": "message",
    "operation": "send",
    "messageType": "text",
    "text": "={{ $json.message }}",
    "toUser": "",
    "toParty": "",
    "toTag": ""
  },
  "id": "REPLACE-WITH-UUID",
  "name": "WeChat Work",
  "type": "n8n-nodes-base.wechatWork",
  "typeVersion": 1,
  "position": [690, 300],
  "credentials": {
    "wechatWorkApi": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "WeChat Work account"
    }
  }
}
```

### 17. DingTalk（钉钉）

```json
{
  "parameters": {
    "resource": "message",
    "operation": "send",
    "messageType": "text",
    "text": "={{ $json.message }}",
    "atUserIds": "",
    "atAll": false
  },
  "id": "REPLACE-WITH-UUID",
  "name": "DingTalk",
  "type": "n8n-nodes-base.dingTalk",
  "typeVersion": 1.1,
  "position": [690, 300],
  "credentials": {
    "dingTalkApi": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "DingTalk account"
    }
  }
}
```

---

## 四、网络/API 节点（Network）

### 18. HTTP Request（HTTP 请求）

```json
{
  "parameters": {
    "url": "https://api.example.com/data",
    "authentication": "genericCredentialType",
    "genericAuthType": "httpHeaderAuth",
    "method": "GET",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "Content-Type",
          "value": "application/json"
        }
      ]
    },
    "sendBody": true,
    "specifyBody": "json",
    "jsonParameters": false,
    "jsonBody": "={{ JSON.stringify($json) }}",
    "options": {
      "response": {
        "response": {
          "responseFormat": "json"
        }
      }
    }
  },
  "id": "REPLACE-WITH-UUID",
  "name": "HTTP Request",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [470, 300],
  "credentials": {
    "httpHeaderAuth": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "API Auth"
    }
  }
}
```

**HTTP Request JSON Body 配置（实测验证，关键）：**
- `sendBody: true` — 启用请求体
- `specifyBody: "json"` — 使用 JSON 格式
- `jsonParameters: false` — **必须设为 false！设为 true 直接崩溃**
- `jsonBody: "={{ {...} }}"` — 用表达式传递 JSON 对象

**HTTP Request 常用配置：**

| 参数 | 说明 | 常用值 |
|------|------|--------|
| `method` | HTTP 方法 | GET, POST, PUT, DELETE, PATCH |
| `authentication` | 认证方式 | none, genericCredentialType, oAuth2 |
| `sendBody` | 是否发送请求体 | true / false |
| `specifyBody` | 请求体格式 | json, form-urlencoded, raw |
| `response.response.responseFormat` | 响应格式 | json, text, file |

### 19. Respond to Webhook（Webhook 响应）

```json
{
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ JSON.stringify({ success: true, message: 'OK' }) }}",
    "options": {
      "responseCode": "200"
    }
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Respond to Webhook",
  "type": "n8n-nodes-base.respondToWebhook",
  "typeVersion": 1.1,
  "position": [690, 300]
}
```

> ⚠️ **n8n 2.x 严重警告：** 如果 Webhook 节点的 `responseMode` 设为 `"lastNode"`，**绝对不要**使用此节点！最后一个节点的返回值会自动作为 HTTP 响应。`respondToWebhook` 只在 `responseMode` 为 `"responseNode"` 时可用，否则会报 `Unused Respond to Webhook node found` 错误。**推荐统一使用 `responseMode: "lastNode"` + Code 节点返回响应数据**，避免使用 respondToWebhook 节点。

---

## 五、数据库节点（Database）

### 20. MySQL

```json
{
  "parameters": {
    "operation": "executeQuery",
    "query": "SELECT * FROM users WHERE status = 'active' LIMIT 100",
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "MySQL",
  "type": "n8n-nodes-base.mySql",
  "typeVersion": 2.4,
  "position": [470, 300],
  "credentials": {
    "mySql": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "MySQL account"
    }
  }
}
```

**MySQL 操作模式：**
- `executeQuery` — 执行 SQL 查询
- `insert` — 插入行
- `update` — 更新行
- `delete` — 删除行

### 21. PostgreSQL

```json
{
  "parameters": {
    "operation": "executeQuery",
    "query": "SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '1 day'",
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Postgres",
  "type": "n8n-nodes-base.postgres",
  "typeVersion": 2.6,
  "position": [470, 300],
  "credentials": {
    "postgres": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "Postgres account"
    }
  }
}
```

### 22. Redis

```json
{
  "parameters": {
    "operation": "get",
    "key": "my-cache-key"
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Redis",
  "type": "n8n-nodes-base.redis",
  "typeVersion": 1.1,
  "position": [470, 300],
  "credentials": {
    "redis": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "Redis account"
    }
  }
}
```

### 23. MongoDB

```json
{
  "parameters": {
    "operation": "find",
    "collection": "my_collection",
    "query": "={{ JSON.stringify({ status: 'active' }) }}"
  },
  "id": "REPLACE-WITH-UUID",
  "name": "MongoDB",
  "type": "n8n-nodes-base.mongoDb",
  "typeVersion": 1.1,
  "position": [470, 300],
  "credentials": {
    "mongoDb": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "MongoDB account"
    }
  }
}
```

---

## 六、文件/数据处理节点

### 24. Read/Write Files（文件读写）

```json
{
  "parameters": {
    "operation": "read",
    "fileName": "=/data/input.json",
    "dataPropertyName": "data",
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Read File",
  "type": "n8n-nodes-base.readWriteFile",
  "typeVersion": 1.1,
  "position": [470, 300]
}
```

### 25. Spreadsheet File（Excel 处理）

```json
{
  "parameters": {
    "operation": "fromFile",
    "fileFormat": "xlsx",
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Spreadsheet File",
  "type": "n8n-nodes-base.spreadsheetFile",
  "typeVersion": 2.3,
  "position": [470, 300]
}
```

### 26. HTML Extract（HTML 解析）

```json
{
  "parameters": {
    "url": "https://example.com",
    "extractionValues": {
      "values": [
        {
          "key": "title",
          "cssSelector": "h1.title",
          "returnValue": "text"
        }
      ]
    },
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "HTML Extract",
  "type": "n8n-nodes-base.html",
  "typeVersion": 2.2,
  "position": [470, 300]
}
```

---

## 七、AI 节点

### 27. AI Agent（AI 代理）

```json
{
  "parameters": {
    "agent": "conversationalAgent",
    "promptType": "define",
    "text": "={{ $json.body.message }}",
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "AI Agent",
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 1.6,
  "position": [470, 300]
}
```

### 28. OpenAI Model（OpenAI 模型）

```json
{
  "parameters": {
    "model": "gpt-4o",
    "messages": {
      "values": [
        {
          "role": "system",
          "content": "You are a helpful assistant."
        },
        {
          "role": "user",
          "content": "={{ $json.query }}"
        }
      ]
    },
    "options": {}
  },
  "id": "REPLACE-WITH-UUID",
  "name": "OpenAI",
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "typeVersion": 1.6,
  "position": [470, 300],
  "credentials": {
    "openAiApi": {
      "id": "REPLACE-WITH-CREDENTIAL-ID",
      "name": "OpenAI API"
    }
  }
}
```

---

## 八、辅助节点

### 29. Wait（等待/延迟）⚠️ 高风险

```json
{
  "parameters": {
    "amount": 5,
    "unit": "seconds"
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Wait",
  "type": "n8n-nodes-base.wait",
  "typeVersion": 1.1,
  "position": [470, 300]
}
```

> ⚠️ **实战教训：Wait 节点（特别是 Wait for Callback）可能导致工作流无法激活！** 如果遇到 `triggerCount: 0` 或激活失败，优先检查 Wait 节点。替代方案：用 Code 节点 + `await new Promise(r => setTimeout(r, 5000))` 或 IF 分支判断替代 Wait for Callback。

### 30. No Operation（空操作/占位）

```json
{
  "parameters": {},
  "id": "REPLACE-WITH-UUID",
  "name": "No Operation",
  "type": "n8n-nodes-base.noOp",
  "typeVersion": 1,
  "position": [470, 300]
}
```

### 31. Execute Workflow（执行子工作流）

```json
{
  "parameters": {
    "workflowId": "REPLACE-WITH-SUB-WORKFLOW-ID"
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Execute Workflow",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1.1,
  "position": [470, 300]
}
```

### 32. Sticky Note（便签/注释）

```json
{
  "parameters": {
    "content": "这里是注释内容，用于说明工作流的某个部分"
  },
  "id": "REPLACE-WITH-UUID",
  "name": "Sticky Note",
  "type": "n8n-nodes-base.stickyNote",
  "typeVersion": 1,
  "position": [250, 500]
}
```

---

## 节点类型完整前缀规则

在 n8n REST API 中，节点 `type` 字段使用以下前缀：

| 类别 | 前缀 | 示例 |
|------|------|------|
| 内置节点 | `n8n-nodes-base.` | `n8n-nodes-base.webhook` |
| AI/LangChain | `@n8n/n8n-nodes-langchain.` | `@n8n/n8n-nodes-langchain.agent` |
| 社区节点 | `n8n-nodes-package.xxx.` | `n8n-nodes-package.google-sheets.googleSheets` |

---

## 常用凭证类型速查

| 凭证类型 | type 值 | 用途 |
|----------|---------|------|
| API Key (Header) | `httpHeaderAuth` | 大多数 REST API |
| Basic Auth | `httpBasicAuth` | 传统 API |
| Bearer Token | `oAuth2Api` | OAuth2 流程 |
| Slack | `slackApi` | Slack 机器人 |
| Telegram | `telegramApi` | Telegram 机器人 |
| SMTP | `smtp` | 发送邮件 |
| MySQL | `mySql` | MySQL 数据库 |
| PostgreSQL | `postgres` | PostgreSQL 数据库 |
| MongoDB | `mongoDb` | MongoDB |
| Redis | `redis` | Redis 缓存 |
| OpenAI | `openAiApi` | OpenAI API |
