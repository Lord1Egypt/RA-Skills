# n8n API 参考 (n8n 2.x)

## 认证方式

n8n API 使用 `X-N8N-API-KEY` 头进行 API Key 认证。

API Key 在 n8n 界面管理：
- Settings → API
- User profile → API

## 基础 URL

`{N8N_BASE_URL}/api/v1`

## 端点一览

### 工作流（Workflows）

#### 列出工作流
```
GET /workflows
Query params: ?active=true|false&cursor=string&limit=number
```

#### 获取工作流详情
```
GET /workflows/{id}
```

#### 创建工作流
```
POST /workflows
Body: workflow JSON (不要包含 active, tags, staticData, shared, pinData)
```

#### 更新工作流
```
PUT /workflows/{id}
Body: 完整 workflow JSON (PUT = 全量替换，n8n 2.x 不支持 PATCH)
```

#### 激活工作流
```
POST /workflows/{id}/activate
Body: {} 或留空
```

#### 停用工作流
```
POST /workflows/{id}/deactivate
```

#### 删除工作流
```
DELETE /workflows/{id}
```

### 执行记录（Executions）

#### 列出执行记录
```
GET /executions?limit=20&workflowId={id}&status=success|error|running
```

#### 获取执行记录详情
```
GET /executions/{id}
```

#### 删除执行记录
```
DELETE /executions/{id}
```

#### 重试执行
```
POST /executions/{id}/retry
Body: {"loadWorkflow": true}
```

#### 手动执行
```
POST /workflows/{id}/execute
Body: {"data": {...}}
```

### 凭证（Credentials）

#### 列出凭证
```
GET /credentials
```

#### 创建凭证
```
POST /credentials
Body: {"name": "...", "type": "httpHeaderAuth", "data": {...}}
```

## 常用模式

### 列出已激活的工作流
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/api/v1/workflows?active=true&limit=50"
```

### 获取工作流详情
```bash
curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/api/v1/workflows/{id}"
```

### 激活/停用工作流
```bash
# 激活
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{}" "$N8N_BASE_URL/api/v1/workflows/{id}/activate"

# 停用
curl -s -X POST -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/api/v1/workflows/{id}/deactivate"
```

### 触发 Webhook
```bash
# 正式环境 webhook（用 webhookId，不是 path 参数）
curl -s -X POST "$N8N_BASE_URL/webhook/{webhookId}" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'

# 测试 webhook
curl -s -X POST "$N8N_BASE_URL/webhook-test/{path}" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'
```

### 健康检查
```bash
ACTIVE=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/api/v1/workflows?active=true" | jq ".data | length")

FAILED=$(curl -s -H "X-N8N-API-KEY: $N8N_API_KEY" \
  "$N8N_BASE_URL/api/v1/executions?status=error&limit=100" \
  | jq '[.data[] | select(.startedAt > (now - 86400 | todate))] | length')

echo "Active workflows: $ACTIVE | Failed (24h): $FAILED"
```

## 错误处理

HTTP 状态码：
- `200` - 成功
- `400` - 错误请求（检查 body 中是否有只读字段）
- `401` - 未授权（API Key 无效）
- `404` - 未找到
- `405` - 方法不允许（n8n 2.x 不支持 PATCH）
- `500` - 服务器错误

## 环境变量

必填：
- `N8N_API_KEY` - n8n API Key
- `N8N_BASE_URL` - 基础 URL（如 http://localhost:5678）
