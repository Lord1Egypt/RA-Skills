# 渠道配置总览

## 支持的渠道

| 渠道 | 类型 | 说明 |
|------|------|------|
| Telegram | 内置 | Bot API (grammY)，最快设置 |
| WhatsApp | 内置 | Baileys，需二维码配对 |
| Discord | 内置 | Bot API + Gateway |
| Signal | 内置 | signal-cli，注重隐私 |
| Slack | 内置 | Bolt SDK |
| BlueBubbles | 内置 | 推荐iMessage集成 |
| iMessage | 内置 | 旧版(已弃用，用BlueBubbles) |
| Google Chat | 内置 | HTTP webhook |
| 飞书 | 插件 | 需单独安装 |
| Mattermost | 插件 | Bot API + WebSocket |
| MS Teams | 插件 | Bot Framework |
| LINE | 插件 | Messaging API |
| Matrix | 插件 | Matrix协议 |
| Nextcloud Talk | 插件 | 自托管 |
| Nostr | 插件 | NIP-04去中心化 |
| Twitch | 插件 | IRC |
| Zalo | 插件 | Bot API |
| Zalo Personal | 插件 | 二维码登录 |
| WebChat | 内置 | WebSocket UI |

## 通用配置模式

### 多账户
所有渠道支持 `channels.<channel>.accounts.<name>` 多账户模式。

### 访问控制
- `dmPolicy`: `pairing`(默认) | `allowlist` | `open` | `disabled`
- `allowFrom`: 私信白名单 (用户ID)
- `groupPolicy`: `open` | `allowlist`(默认) | `disabled`
- `groupAllowFrom`: 群组发送者白名单

### 群组配置
```json5
channels: {
  telegram: {
    groups: {
      "-1001234567890": { requireMention: false },
      "*": { requireMention: true }  // 全局默认
    }
  }
}
```
设置 `groups` 即创建允许列表，未列出的群组被拒绝。

### 渠道路由
- 回复自动路由回源渠道
- 多渠道同时运行，按聊天路由
- 私信默认共享主会话 (dmScope=main)

### CLI 管理
```bash
openclaw channels list [--json]
openclaw channels status [--probe]
openclaw channels logs [--channel telegram]
openclaw channels add --channel telegram --token $TOKEN
openclaw channels remove --channel discord --account work
openclaw channels login [--channel whatsapp]
openclaw channels logout [--channel whatsapp]
```

## 配对机制

### 私信配对
当 `dmPolicy: "pairing"` 时，未知发送者收到8字符配对码(1小时过期)，消息不处理直到批准。
```bash
openclaw pairing list <channel>           # 查看待批准
openclaw pairing approve <channel> <CODE> # 批准
```
支持: telegram, whatsapp, signal, imessage, discord, slack

### 节点配对
```bash
openclaw devices list                     # 查看设备
openclaw devices approve <requestId>      # 批准
openclaw devices reject <requestId>       # 拒绝
```

### 存储位置
- 私信配对: `~/.openclaw/credentials/<channel>-pairing.json`
- 已批准: `~/.openclaw/credentials/<channel>-allowFrom.json`
- 节点: `~/.openclaw/devices/paired.json`

## 群组行为

### 消息流程
```
groupPolicy=disabled → 丢弃
groupPolicy=allowlist → 群组在允许列表? 否→丢弃
requireMention=true → 被@提及? 否→仅存储为上下文
否则 → 回复
```

### 常见配置
| 目标 | 配置 |
|------|------|
| 允许所有群组，仅@提及回复 | `groups: { "*": { requireMention: true } }` |
| 禁用所有群组 | `groupPolicy: "disabled"` |
| 仅特定群组 | `groups: { "<id>": {} }` (无"*") |
| 仅你能触发 | `groupPolicy: "allowlist"` + `groupAllowFrom: ["+155..."]` |

### 群组会话键
- 群组: `agent:<agentId>:<channel>:group:<id>`
- Telegram话题: `...group:<id>:topic:<threadId>`
- 群组会话跳过心跳

### 群组+沙箱隔离
```json5
sandbox: { mode: "non-main" }  // 群组在Docker中运行，私信在主机
```

### 群组历史上下文
- `historyLimit`: 群组历史消息数(默认50)
- 群组消息作为上下文注入(即使未触发回复)

### 提及模式
```json5
agents: { list: [{ id: "main", groupChat: { mentionPatterns: ["@bot", "hey bot"] } }] }
// 或全局
messages: { groupChat: { mentionPatterns: ["@bot"] } }
```

### 运行时切换
```
/activation always    # 响应所有消息(仅会话级)
/activation mention   # 需要提及(默认)
```
