# ZhenInsure 真机保险 | Chat & Handoff

保险与保障咨询 Skill。通过 API Key 直接调用 ZhenInsure 后端 API，创建 AI 对话、发送消息、请求人工顾问转接。

## 核心设计

本 Skill 是透明代理通道：
- 用户指定 `endpoint` + `method` + `body`
- Skill 注入 `Authorization: Bearer {API_KEY}` header
- 请求直接转发到 `https://www.zhenins.com`
- 同步 JSON 响应原样返回（非 SSE 流式）

## 白名单端点

| Endpoint | Method | 费用 |
|---|---|---|
| `/api/v1/skill/chat/conversations` | POST | 免费 |
| `/api/v1/skill/chat/messages` | POST | ¥0.15/次 |
| `/api/v1/skill/chat/handoff` | POST | 免费 |

## 配置

```bash
claw config set ZHENINSURE_API_KEY sk_live_xxxx
```

## 用法示例

### 创建对话

```bash
claw run insurance-broker proxy '{
  "endpoint": "/api/v1/skill/chat/conversations",
  "method": "POST"
}'
```

### 发送消息

```bash
claw run insurance-broker proxy '{
  "endpoint": "/api/v1/skill/chat/messages",
  "method": "POST",
  "body": {
    "conversation_id": "conv_xxxx",
    "message": "我想了解一下重疾险"
  }
}'
```

### 请求人工转接

```bash
claw run insurance-broker proxy '{
  "endpoint": "/api/v1/skill/chat/handoff",
  "method": "POST",
  "body": {
    "conversation_id": "conv_xxxx"
  }
}'
```

## 余额不足

```json
{
  "success": false,
  "error": "insufficient_balance",
  "action": {
    "type": "recharge",
    "url": "https://console.zhenrobot.com/zhenins/billing"
  }
}
```

## 版本

2.0.2
