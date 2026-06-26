---
name: openclaw-api-reference
version: 1.0.0
description: OpenClaw API 参考 - 完整的 API 文档和示例。适合：开发者、集成场景。
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: []
---

# OpenClaw API 参考

完整的 API 文档和示例。

## 基础 URL

```
http://localhost:3000/api/v1
```

## 认证

### API Key

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:3000/api/v1/chat
```

### JWT

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:3000/api/v1/chat
```

## 聊天 API

### 发送消息

```bash
POST /api/v1/chat

{
  "message": "你好",
  "session_id": "optional-session-id",
  "model": "deepseek-chat"
}
```

**响应**：

```json
{
  "response": "你好！有什么可以帮你的？",
  "session_id": "abc123",
  "tokens": {
    "input": 5,
    "output": 10
  }
}
```

### 流式响应

```bash
POST /api/v1/chat/stream

{
  "message": "写一首诗"
}
```

**响应**（SSE）：

```
data: {"text": "春"}
data: {"text": "眠"}
data: {"text": "不"}
data: {"text": "觉"}
data: {"text": "晓"}
data: [DONE]
```

## 会话 API

### 创建会话

```bash
POST /api/v1/sessions

{
  "name": "我的会话",
  "model": "deepseek-chat"
}
```

### 获取会话

```bash
GET /api/v1/sessions/:id
```

### 列出会话

```bash
GET /api/v1/sessions
```

### 删除会话

```bash
DELETE /api/v1/sessions/:id
```

## 消息 API

### 获取消息历史

```bash
GET /api/v1/sessions/:id/messages

# 参数
?limit=50
&offset=0
&order=desc
```

### 删除消息

```bash
DELETE /api/v1/messages/:id
```

## Skills API

### 列出 Skills

```bash
GET /api/v1/skills
```

### 执行 Skill

```bash
POST /api/v1/skills/:name/run

{
  "params": {
    "key": "value"
  }
}
```

### 创建 Skill

```bash
POST /api/v1/skills

{
  "name": "my-skill",
  "description": "描述",
  "script": "echo 'hello'"
}
```

## 配置 API

### 获取配置

```bash
GET /api/v1/config
```

### 更新配置

```bash
PATCH /api/v1/config

{
  "model": "gpt-4o",
  "temperature": 0.7
}
```

## 用户 API

### 创建用户

```bash
POST /api/v1/users

{
  "email": "user@example.com",
  "password": "secure-password"
}
```

### 获取用户

```bash
GET /api/v1/users/:id
```

### 更新用户

```bash
PATCH /api/v1/users/:id

{
  "name": "新名字"
}
```

## Webhook API

### 创建 Webhook

```bash
POST /api/v1/webhooks

{
  "url": "https://your-server.com/webhook",
  "events": ["message.created", "session.created"]
}
```

### 测试 Webhook

```bash
POST /api/v1/webhooks/:id/test
```

## 错误处理

### 错误格式

```json
{
  "error": {
    "code": "INVALID_API_KEY",
    "message": "API key is invalid",
    "details": {}
  }
}
```

### 常见错误码

| 错误码 | 说明 |
|--------|------|
| INVALID_API_KEY | API Key 无效 |
| RATE_LIMIT | 请求频率超限 |
| MODEL_NOT_FOUND | 模型不存在 |
| SESSION_NOT_FOUND | 会话不存在 |
| INTERNAL_ERROR | 服务器错误 |

## SDK

### JavaScript/TypeScript

```bash
npm install openclaw-sdk
```

```javascript
import { OpenClaw } from 'openclaw-sdk';

const client = new OpenClaw({
  apiKey: 'your-api-key'
});

const response = await client.chat({
  message: '你好'
});
```

### Python

```bash
pip install openclaw
```

```python
from openclaw import OpenClaw

client = OpenClaw(api_key='your-api-key')

response = client.chat(message='你好')
```

## 需要帮助？

- API 集成：¥99
- SDK 开发：¥299
- 企业支持：¥999

联系：微信 yang1002378395 或 Telegram @yangster151

---
创建：2026-03-14
