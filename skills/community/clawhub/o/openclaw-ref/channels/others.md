# 其他渠道配置参考

## Slack

### 快速设置
1. api.slack.com → Create App → Socket Mode → Event Subscriptions
2. Bot Token Scopes: chat:write, channels:history, groups:history, im:history, users:read
3. Event Subscriptions: message.channels, message.groups, message.im, app_mention

### 最小配置
```json5
channels: {
  slack: {
    enabled: true,
    appToken: "xapp-...",     // Socket Mode token
    botToken: "xoxb-...",     // Bot token
    dmPolicy: "pairing",
    allowFrom: ["U12345678"]  // Slack用户ID
  }
}
```

### 两种模式
- Socket Mode(默认): 无需公网URL
- HTTP Webhook: 设置 `webhookUrl`

### 群组
```json5
groups: { "C12345678": { requireMention: true } }
```

## BlueBubbles (推荐iMessage)

### 快速设置
1. 安装 BlueBubbles macOS 服务器
2. 获取 API URL + 密码

### 最小配置
```json5
channels: {
  bluebubbles: {
    enabled: true,
    serverUrl: "http://localhost:1234",
    password: "${BB_PASSWORD}",
    dmPolicy: "allowlist",
    allowFrom: ["+15551234567"]
  }
}
```
功能: 编辑、撤回、特效、反应、群组管理

## iMessage (旧版，已弃用)

### 最小配置
```json5
channels: {
  imessage: {
    enabled: true,
    dmPolicy: "allowlist",
    allowFrom: ["+15551234567"]
  }
}
```
⚠️ 新设置请用 BlueBubbles

## Google Chat

### 快速设置
1. Google Cloud Console → Chat API → 创建应用
2. 配置 HTTP endpoint

### 最小配置
```json5
channels: {
  googlechat: {
    enabled: true,
    credentials: "${GOOGLE_CHAT_CREDENTIALS}",
    dmPolicy: "allowlist"
  }
}
```

## 飞书 (插件)

### 安装
```bash
openclaw plugins install openclaw-feishu
```

### 最小配置
```json5
channels: {
  feishu: {
    enabled: true,
    appId: "cli_xxx",
    appSecret: "${FEISHU_APP_SECRET}",
    dmPolicy: "allowlist"
  }
}
```

## Mattermost (插件)

### 安装
```bash
openclaw plugins install openclaw-mattermost
```

### 最小配置
```json5
channels: {
  mattermost: {
    enabled: true,
    url: "https://mattermost.example.com",
    token: "${MM_BOT_TOKEN}",
    dmPolicy: "allowlist"
  }
}
```

## LINE (插件)

### 安装
```bash
openclaw plugins install openclaw-line
```

### 最小配置
```json5
channels: {
  line: {
    enabled: true,
    channelAccessToken: "${LINE_TOKEN}",
    channelSecret: "${LINE_SECRET}",
    webhookUrl: "https://example.com/line-webhook"
  }
}
```

## Matrix (插件)

### 安装
```bash
openclaw plugins install openclaw-matrix
```

### 最小配置
```json5
channels: {
  matrix: {
    enabled: true,
    homeserverUrl: "https://matrix.org",
    userId: "@bot:matrix.org",
    accessToken: "${MATRIX_TOKEN}"
  }
}
```

## MS Teams (插件)
```bash
openclaw plugins install openclaw-msteams
```

## Nextcloud Talk (插件)
```bash
openclaw plugins install openclaw-nextcloud-talk
```

## Nostr (插件)
```bash
openclaw plugins install openclaw-nostr
```

## Twitch (插件)
```bash
openclaw plugins install openclaw-twitch
```

## 通用配置字段 (所有渠道)
| 字段 | 说明 |
|------|------|
| `enabled` | 启用/禁用 |
| `dmPolicy` | pairing/allowlist/open/disabled |
| `allowFrom` | 私信白名单 |
| `groupPolicy` | open/allowlist/disabled |
| `groupAllowFrom` | 群组发送者白名单 |
| `textChunkLimit` | 出站分块大小 |
| `mediaMaxMb` | 媒体上限 |
| `historyLimit` | 群组历史消息数 |
| `configWrites` | 允许配置写入(默认true) |
