---
name: Clawhome 连接
description: 将 OpenClaw 连接到 Clawhome 聊天平台，实现 AI 自动回复。
trigger:
  - 接入 clawhome
  - clawhome 适配器
  - wss://www.clawhome.top/mqtt
---

# Clawhome 连接技能

将 OpenClaw 连接到 Clawhome 平台，实现双向消息收发。

## 一键安装

```bash
npx -y openclaw-clawhome-cli@latest install
```
告知 Clawhome 连接信息
```bash
openclaw config set channels.clawhome.channelId "你的频道ID"
openclaw config set channels.clawhome.channelSecret "你的频道密钥"
```

## 重启 Gateway

```bash
openclaw gateway restart
```

## Clawhome 协议

### MQTT 主题

- **接收消息**: `channel/${CHANNEL_ID}/user/event`
- **发送消息**: `channel/${CHANNEL_ID}/agent/action`

### 心跳格式

```json
{
    "type": "ping",
    "role": "agent",
    "timestamp": 1774245227871
}
```

### 消息格式

```json
{
    "type": "message",
    "role": "agent",
    "timestamp": 1774245227871,
    "content": "你好，我是 Clawhome 机器人"
}
```

## 配置选项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| mqttUrl | MQTT Broker 地址 | wss://www.clawhome.top/mqtt |
| channelId | 频道 ID | - |
| channelSecret | 频道密钥 | - |
| reconnectInterval | 重连间隔(毫秒) | 5000 |
| heartbeatInterval | 心跳间隔(毫秒) | 30000 |
