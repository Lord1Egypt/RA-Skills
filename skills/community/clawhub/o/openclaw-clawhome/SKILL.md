---
name: Clawhome 连接
description: 将 OpenClaw 连接到 Clawhome 聊天平台，实现 AI 自动回复。
trigger:
  - 接入 clawhome
  - clawhome 适配器
  - wss://www.clawhome.io/ws
---

# Clawhome 连接技能

将 OpenClaw 连接到 Clawhome 平台，实现双向消息收发。

## 一键安装

```bash
openclaw plugins install "openclaw-clawhome"
```
告知 Clawhome 连接信息
```bash
openclaw config set channels.openclaw-clawhome.channelId "你的频道ID"
openclaw config set channels.openclaw-clawhome.channelSecret "你的频道密钥"
```

## 重启 Gateway

```bash
openclaw gateway restart
```

## 一句话接入

```bash
openclaw plugins install "openclaw-clawhome" && openclaw config set channels.openclaw-clawhome.channelId "你的频道ID" && openclaw config set channels.openclaw-clawhome.channelSecret "你的频道密钥" && openclaw gateway restart
```

## Clawhome 协议

### 主题

- **接收消息**: `channel/${CHANNEL_ID}/user`
- **发送消息**: `channel/${CHANNEL_ID}/agent`
- **心跳**: `channel/${CHANNEL_ID}/ping`

### 心跳格式

```json
{
    "type": "ping",
    "role": "agent",
    "timestamp": 1774245227871
}
```

### 消息格式

**文本消息:**

```json
{
    "type": "message",
    "timestamp": 1774245227871,
    "payload": "你好，我是 Clawhome 机器人"
}
```

**文件/图片消息:**

支持发送文件或图片消息，需要先调用免鉴权的上传接口获取文件 URL，再以 `file` 类型发送消息。

1. **上传文件**

```bash
curl -X POST 'https://www.clawhome.io/api/oss/upload' \
  --header 'Accept: */*' \
  --form 'file=@/path/to/your/image.png' \
  --form 'channelId=你的频道ID'
```

2. **发送文件消息**

```json
{
    "type": "file",
    "timestamp": 1774245227871,
    "payload": {
        "url": "https://www.clawhome.io/uploads/channels/123/image.png",
        "fileName": "image.png",
        "mimeType": "image/png"
    }
}
```

## 配置选项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| channelId | 频道 ID | - |
| channelSecret | 频道密钥 | - |
