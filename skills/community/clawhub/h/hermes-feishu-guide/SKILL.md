---
name: hermes-feishu-guide
description: Hermes Agent 飞书 Bot 本地部署指南（WebSocket 模式）。包含 Kimi API 配置、WebSocket vs Webhook 对比、环境变量配置等完整步骤。适合本地机器部署，不需要公网域名。
license: MIT
version: 1.1.0
---

# Hermes 飞书 Bot 本地部署指南

## 概述

Hermes Agent 从 v0.6.0 开始支持飞书（Feishu/Lark）平台。飞书国内版支持 WebSocket 模式，不需要公网域名，直接本地运行。

## 前置准备

### 1. 飞书开放平台创建应用

- 创建企业自建应用
- 获取 App ID 和 App Secret
- 启用 Bot 能力
- 开通权限：`im:message`、`im:message:send_as_bot`、`im:message:group_at_msg`（群聊@消息）

### 2. Kimi API Key

- 获取 Moonshot API Key
- 注意模型名称：`kimi-k2.5`（不是 `moonshotai/Kimi-K2.5`）

## 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.zshrc
```

## 配置环境变量

编辑 `~/.hermes/.env`：

```env
KIMI_CN_API_KEY=sk-xxx
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_CONNECTION_MODE=websocket
FEISHU_GROUP_POLICY=open        # 群聊策略：open/allowlist/disabled
GATEWAY_ALLOW_ALL_USERS=true
```

### 群聊策略说明

| 值 | 说明 |
|---|------|
| `open` | ✅ 响应任何用户的 @提及 |
| `allowlist` | ⚠️ 只响应 `FEISHU_ALLOWED_USERS` 白名单用户 |
| `disabled` | ❌ 忽略所有群聊消息 |

⚠️ **重要**：默认值是 `allowlist`，如果不在白名单，群聊 @机器人不会响应！单聊不受此限制。

## 启动网关

```bash
hermes gateway start
hermes gateway status
```

## 验证连接

```bash
tail -50 ~/.hermes/logs/gateway.log
```

看到 `connected to wss://msg-frontier.feishu.cn/ws/v2...` 表示成功。

## WebSocket vs Webhook

| 对比项 | WebSocket | Webhook |
|--------|-----------|---------|
| 需要公网域名 | ❌ | ✅ |
| 需要 HTTPS 证书 | ❌ | ✅ |
| 飞书国内版 | ✅ | ✅ |
| Lark 国际版 | ❌ | ✅ |

## 常见问题

### Q: Kimi API 认证失败

检查模型名称，去掉 `moonshotai/` 前缀，使用 `kimi-k2.5`。

### Q: 群聊 @机器人没反应

检查 `FEISHU_GROUP_POLICY` 配置：
- 默认是 `allowlist`，需要改成 `open`
- 或添加用户到 `FEISHU_ALLOWED_USERS`

### Q: 单聊可以，群聊不行

这是群聊策略限制，单聊绕过策略检查。添加 `FEISHU_GROUP_POLICY=open` 即可。

## 排障经验

### Kimi API Key 认证失败

模型名称写错：`moonshotai/Kimi-K2.5` → 正确是 `kimi-k2.5`

### 群聊 @机器人无响应

默认 `FEISHU_GROUP_POLICY=allowlist`，改成 `open`

## 参考

- [Hermes 官方文档](https://hermes-agent.nousresearch.com)
- [飞书开放平台](https://open.feishu.cn)
