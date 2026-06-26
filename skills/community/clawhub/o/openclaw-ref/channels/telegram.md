# Telegram 配置参考

## 快速设置
1. @BotFather → `/newbot` → 复制 token
2. 配置 token: `channels.telegram.botToken: "123:abc"` 或 `TELEGRAM_BOT_TOKEN=...`
3. 启动网关，私信机器人，批准配对码

### 最小配置
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing"
    }
  }
}
```

## 访问控制

### 私信
- `dmPolicy`: `pairing`(默认) | `allowlist` | `open` | `disabled`
- `allowFrom`: 数字用户ID(推荐) 或 `@username`
- 配对: `openclaw pairing list telegram` → `openclaw pairing approve telegram <CODE>`

### 获取用户ID
- 私信机器人 → `openclaw logs --follow` 查找 `from.id`
- 或: `curl "https://api.telegram.org/bot<token>/getUpdates"` 读 `message.from.id`

### 群组
- `groupPolicy`: `allowlist`(默认) | `open` | `disabled`
- `groupAllowFrom`: 群组发送者白名单
- `groups`: 群组允许列表+配置

```json5
groups: {
  "-1001234567890": {
    requireMention: false,    // 不需要@提及
    allowFrom: [123, 456],    // 每群组发送者白名单
    systemPrompt: "额外提示", // 群组专用提示
    skills: ["skill1"],       // skill过滤
    enabled: true,
    topics: {
      "123": { requireMention: true }  // 话题覆盖
    }
  },
  "*": { requireMention: true }  // 全局默认
}
```

### BotFather 设置
- `/setprivacy` → Disable: 机器人可看所有群组消息
- 或将机器人设为群组管理员
- ⚠️ 切换隐私模式后需移除并重新添加机器人

## 功能配置

### 反应
```json5
reactionNotifications: "own",  // off|own|all
reactionLevel: "minimal"       // off|ack|minimal|extensive
```

### 内联按钮
```json5
capabilities: {
  inlineButtons: "allowlist"  // off|dm|group|all|allowlist
}
```
发送按钮:
```json5
{ action: "send", channel: "telegram", to: "123",
  message: "选择:", buttons: [[{text:"是",callback_data:"yes"},{text:"否",callback_data:"no"}]] }
```

### 贴纸
```json5
actions: { sticker: true }  // 默认禁用
```
缓存位置: `~/.openclaw/telegram/sticker-cache.json`

### 自定义命令 (菜单)
```json5
customCommands: [
  { command: "backup", description: "Git 备份" }
]
```
仅菜单条目，不能覆盖原生命令。

## 流式传输

### 草稿流式 (Draft Streaming)
```json5
streamMode: "partial"  // off|partial|block
```
要求: 机器人启用论坛话题模式，仅私聊。

### 分块流式 (Block Streaming)
```json5
blockStreaming: true  // 独立于草稿流式
```

## 消息限制
- `textChunkLimit`: 出站分块大小(默认4000字符)
- `chunkMode`: `length`(默认) | `newline`(按段落分割)
- `mediaMaxMb`: 媒体上限(默认5MB)
- `timeoutSeconds`: API超时(默认500)
- `historyLimit`: 群组历史消息数(默认50)
- `dmHistoryLimit`: 私信历史(用户轮次)

## 回复模式
```json5
replyToMode: "first"  // off|first|all
```
标签: `[[reply_to_current]]` `[[reply_to:<id>]]`

## 音频
- 默认发送为音频文件
- `[[audio_as_voice]]` 标签: 发送为语音备忘录
- 消息工具: `asVoice: true`

## Webhook 模式 (可选)
```json5
webhookUrl: "https://example.com/telegram-webhook",
webhookSecret: "your-secret",
webhookPath: "/telegram-webhook"  // 默认
```
默认长轮询，不需要公共URL。

## 代理
```json5
proxy: "socks5://127.0.0.1:1080"  // SOCKS/HTTP代理
```

## 网络
```json5
network: { autoSelectFamily: false }  // Node 22默认禁用避免IPv6问题
```

## 重试策略
```json5
retry: { attempts: 3, minDelayMs: 1000, maxDelayMs: 30000, jitter: true }
```

## 常见问题

**群组不响应非提及消息:**
1. BotFather `/setprivacy` → Disable
2. 移除并重新添加机器人到群组
3. `channels.telegram.groups.*.requireMention: false`

**完全看不到群组消息:**
1. 群组必须在 `groups` 中列出或用 `"*"`
2. 检查隐私模式
3. `openclaw logs --follow` 查找 "skipping group message"

**IPv6导致静默失败:**
- `dig +short api.telegram.org A` 检查DNS
- 添加 `/etc/hosts` 条目强制IPv4
- 或设置 `network.autoSelectFamily: false`

**命令不工作:**
- 确认用户ID已授权(配对或allowFrom)
- 群组中命令也需要授权
