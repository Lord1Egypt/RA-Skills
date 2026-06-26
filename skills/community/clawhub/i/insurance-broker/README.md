# ZhenInsure 真机保险 — Insurance Broker Skill

通过 API Key 直接调用 ZhenInsure AI 保险咨询服务的轻量级通道。

## 特点

- **无业务封装**：参数原样透传，响应原样返回
- **单一入口**：一个 `proxy` action 调用所有云端 API
- **API Key 计费**：余额不足时引导到 Console 充值
- **轻量**：零外部依赖，原生 `fetch`

## 快速开始

```bash
# 安装
clawhub install insurance-broker

# 配置 API Key
claw config set ZHENINSURE_API_KEY sk_live_xxxx

# 创建对话（免费）
claw run insurance-broker proxy '{
  "endpoint": "/api/v1/skill/chat/conversations",
  "method": "POST"
}'
```

## 可用端点

| Endpoint | Method | 费用 |
|---|---|---|
| `/api/v1/skill/chat/conversations` | POST | 免费 |
| `/api/v1/skill/chat/messages` | POST | ¥0.15/次 |
| `/api/v1/skill/chat/handoff` | POST | 免费 |

## 使用示例

### 发送消息
```bash
claw run insurance-broker proxy '{
  "endpoint": "/api/v1/skill/chat/messages",
  "method": "POST",
  "body": {
    "conversation_id": "conv_xxxx",
    "message": "35岁男性，有高血压，想买重疾险，有什么推荐？"
  }
}'
```

### 请求人工转接
```bash
claw run insurance-broker proxy '{
  "endpoint": "/api/v1/skill/chat/handoff",
  "method": "POST",
  "body": {
    "conversation_id": "conv_xxxx",
    "reason": "需要人工顾问评估方案"
  }
}'
```

## API Key 获取

1. 在 [Console](https://console.zhenrobot.com/zhenins) 注册顾问账号
2. 进入 **API Keys** 页面创建 Key
3. 余额不足时进入 **Billing** 页面充值

## License

MIT
