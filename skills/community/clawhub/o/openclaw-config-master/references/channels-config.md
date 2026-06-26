# Channels Configuration — OpenClaw 2026.4.1

> **完整配置文档** — 本文件涵盖所有 channel provider 的配置字段。
> Feishu 的完整文档另见 [飞书插件技能](../openclaw-lark/skills/)。

---

## 通用 Channel 字段

### DM / Group 访问策略

所有 channel 都支持 DM 策略和 Group 策略：

| DM policy | 行为 |
|-----------|------|
| `pairing`（默认）| 未知发送者获得一次性配对码；所有者需审批 |
| `allowlist` | 仅 `allowFrom` 中的发送者（或已配对）可交互 |
| `open` | 允许所有入站 DM（需 `allowFrom: ["*"]`）|
| `disabled` | 忽略所有入站 DM |

| Group policy | 行为 |
|-------------|------|
| `allowlist`（默认）| 仅匹配允许列表的群组 |
| `open` | 绕过群组白名单（仍需 mention） |
| `disabled` | 屏蔽所有群组消息 |

### 通用 Channel 字段

| 字段 | 类型 | 描述 |
|------|------|------|
| `enabled` | boolean | 是否启用该 channel |
| `dmPolicy` | enum | DM 策略：`pairing` \| `allowlist` \| `open` \| `disabled` |
| `allowFrom` | array | DM 白名单（open_id / userId / `"*"`）|
| `groupPolicy` | enum | Group 策略：`allowlist` \| `open` \| `disabled` |
| `groupAllowFrom` | array | Group 白名单 |
| `groups` | object | Per-group 配置：`{ "*": { requireMention: true } }` |
| `mediaMaxMb` | number | 媒体文件最大 MB |
| `historyLimit` | integer | 历史消息加载条数 |
| `reactionNotifications` | enum | 消息反应通知：`off` \| `own` \| `all` \| `allowlist` |
| `requireMention` | boolean | 群组中是否必须 @mention 才响应 |
| `typingIndicator` | enum | 打字指示器：`off` \| `message` \| `indicator` |
| `resolveSenderNames` | boolean | 解析发送者姓名 |
| `webhookPath` | string | Webhook 路径 |
| `connectionMode` | enum | 连接模式：`websocket`（飞书专属）|

---

## Telegram

```json5
"channels": {
  "telegram": {
    "enabled": true,
    "botToken": "YOUR_BOT_TOKEN",
    "dmPolicy": "allowlist",
    "allowFrom": ["577958597"],
    "groups": {
      "*": {
        "requireMention": true
      }
    },
    "groupPolicy": "allowlist",
    "replyToMode": "first",
    "linkPreview": true,
    "streaming": "partial",
    "actions": {
      "reactions": true,
      "sendMessage": true
    },
    "reactionNotifications": "own",
    "mediaMaxMb": 100,
    "retry": {
      "attempts": 3,
      "minDelayMs": 400,
      "maxDelayMs": 30000,
      "jitter": 0.1
    },
    "network": {
      "autoSelectFamily": true,
      "dnsResultOrder": "ipv4first"
    },
    "proxy": "socks5://localhost:9050",
    "webhookUrl": "https://example.com/telegram-webhook",
    "webhookSecret": "secret",
    "webhookPath": "/telegram-webhook",
    "customCommands": [
      { "command": "backup", "description": "Git backup" },
      { "command": "generate", "description": "Create an image" }
    ],
    "historyLimit": 50,
    "configWrites": false,
    "modelByChannel": {
      "-1001234567890": "minimax/MiniMax-M2.7-highspeed"
    }
  }
}
```

### 完整字段索引

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `enabled` | boolean | true | 启用 Telegram |
| `botToken` | string | **必填** | Bot Token |
| `dmPolicy` | enum | `pairing` | DM 策略 |
| `allowFrom` | array | `[]` | DM 白名单 |
| `groups` | object | `{}` | Per-group 配置 |
| `groups.*.requireMention` | boolean | true | 群组是否需要 @mention |
| `groups.*.allowFrom` | array | `[]` | 群组白名单 |
| `groups.*.systemPrompt` | string | - | 群组系统提示词 |
| `groups.*.topics` | object | `{}` | Per-topic 配置 |
| `groupPolicy` | enum | `allowlist` | Group 策略 |
| `groupAllowFrom` | array | `[]` | Group 白名单 |
| `replyToMode` | enum | `first` | 回复模式：`off` \| `first` \| `all` |
| `linkPreview` | boolean | true | 启用链接预览 |
| `streaming` | enum | `off` | 流式模式：`off` \| `partial` \| `block` \| `progress` |
| `actions.reactions` | boolean | true | 启用表情反应 |
| `actions.sendMessage` | boolean | true | 启用发送消息 |
| `reactionNotifications` | enum | `own` | 反应通知模式 |
| `mediaMaxMb` | number | 100 | 媒体文件最大 MB |
| `retry.attempts` | integer | 3 | 重试次数 |
| `retry.minDelayMs` | integer | 400 | 最小重试延迟 |
| `retry.maxDelayMs` | integer | 30000 | 最大重试延迟 |
| `retry.jitter` | number | 0.1 | 重试抖动因子 |
| `network.autoSelectFamily` | boolean | true | 自动选择网络协议族 |
| `network.dnsResultOrder` | enum | `ipv4first` | DNS 结果顺序 |
| `proxy` | string | - | SOCKS5 代理 URL |
| `webhookUrl` | string | - | Webhook URL |
| `webhookSecret` | string | - | Webhook 密钥 |
| `webhookPath` | string | `/telegram-webhook` | Webhook 路径 |
| `customCommands` | array | `[]` | 自定义命令菜单 |
| `historyLimit` | integer | 50 | 历史消息限制 |
| `configWrites` | boolean | true | 允许 Telegram 写入配置 |
| `modelByChannel` | object | `{}` | 按 ChatID 固定模型 |
| `defaultAccount` | string | - | 默认账号 ID（多账号场景）|
| `accounts` | object | `{}` | 多账号配置 |

### 多账号配置

```json5
"channels": {
  "telegram": {
    "accounts": {
      "default": {
        "name": "Primary bot",
        "botToken": "123456:ABC..."
      },
      "alerts": {
        "name": "Alerts bot",
        "botToken": "987654:XYZ..."
      }
    }
  }
}
```

---

## Feishu（飞书）

```json5
"channels": {
  "feishu": {
    "enabled": true,
    "appId": "cli_xxx",
    "appSecret": "YOUR_APP_SECRET",
    "domain": "feishu",
    "connectionMode": "websocket",
    "webhookPath": "/feishu/events",
    "dmPolicy": "allowlist",
    "allowFrom": ["ou_xxx"],
    "groupPolicy": "allowlist",
    "groupAllowFrom": ["ou_xxx"],
    "groups": {
      "*": {
        "enabled": true
      }
    },
    "reactionNotifications": "own",
    "typingIndicator": true,
    "resolveSenderNames": true,
    "requireMention": true
  }
}
```

### 完整字段索引

| 字段 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `enabled` | boolean | **必填** | 启用飞书 |
| `appId` | string | **必填** | 应用 ID（`cli_xxx`）|
| `appSecret` | string | **必填** | 应用密钥 |
| `domain` | string | `feishu` | 域名标识 |
| `connectionMode` | enum | `websocket` | 连接模式：`websocket` \| `webhook` |
| `webhookPath` | string | `/feishu/events` | Webhook 路径 |
| `dmPolicy` | enum | `pairing` | DM 策略 |
| `allowFrom` | array | `[]` | DM 白名单（open_id）|
| `groupPolicy` | enum | `allowlist` | Group 策略 |
| `groupAllowFrom` | array | `[]` | Group 白名单 |
| `groups` | object | `{}` | Per-group 配置 |
| `groups.*.enabled` | boolean | true | 启用该群 |
| `groups.*.requireMention` | boolean | true | 是否需要 @mention |
| `groups.*.skills` | array | `[]` | 群组专用技能 |
| `groups.*.systemPrompt` | string | - | 群组系统提示词 |
| `reactionNotifications` | enum | `own` | 反应通知模式 |
| `typingIndicator` | boolean | false | 启用打字指示器 |
| `resolveSenderNames` | boolean | true | 解析发送者姓名 |
| `requireMention` | boolean | true | DM 中是否需要 mention |
| `configWrites` | boolean | true | 允许飞书写入配置 |

### ⚠️ Feishu 配置注意事项

**必须同时满足以下条件才能正常工作：**

1. `channels.feishu.enabled: true` ✓
2. `plugins.entries.feishu.enabled: true`（飞书插件必须启用）
3. `plugins.installs` 中有飞书插件安装记录
4. `channels.feishu.appId` / `appSecret` 与插件中的凭证一致

```json
// ✅ 正确配置示例
"channels": {
  "feishu": {
    "enabled": true,
    "appId": "cli_xxx",
    "appSecret": "YOUR_SECRET"
  }
},
"plugins": {
  "entries": {
    "feishu": {
      "enabled": true
    }
  }
}
```

如果只有 channel 启用但 plugin 禁用，或者反过来，Gateway 会输出警告且飞书 channel 无法正常工作。

---

## Discord

```json5
"channels": {
  "discord": {
    "enabled": true,
    "token": "YOUR_DISCORD_BOT_TOKEN",
    "dmPolicy": "pairing",
    "allowFrom": ["1234567890"],
    "guilds": {
      "123456789012345678": {
        "slug": "my-server",
        "requireMention": false,
        "ignoreOtherMentions": true,
        "reactionNotifications": "own",
        "users": ["987654321098765432"],
        "channels": {
          "general": { "allow": true },
          "help": {
            "allow": true,
            "requireMention": true,
            "skills": ["docs"],
            "systemPrompt": "Short answers only."
          }
        }
      }
    },
    "historyLimit": 20,
    "textChunkLimit": 2000,
    "chunkMode": "length",
    "streaming": "off",
    "maxLinesPerMessage": 17,
    "replyToMode": "off",
    "reactionNotifications": "own",
    "actions": {
      "reactions": true,
      "messages": true,
      "threads": true,
      "pins": true
    },
    "mediaMaxMb": 8,
    "retry": {
      "attempts": 3,
      "minDelayMs": 500,
      "maxDelayMs": 30000,
      "jitter": 0.1
    },
    "threadBindings": {
      "enabled": true,
      "idleHours": 24,
      "maxAgeHours": 0,
      "spawnSubagentSessions": false
    },
    "voice": {
      "enabled": true,
      "autoJoin": [
        {
          "guildId": "123456789012345678",
          "channelId": "234567890123456789"
        }
      ],
      "daveEncryption": true,
      "decryptionFailureTolerance": 24
    },
    "autoPresence": {
      "healthy": "online",
      "degraded": "idle",
      "exhausted": "dnd"
    }
  }
}
```

---

## Slack

```json5
"channels": {
  "slack": {
    "enabled": true,
    "botToken": "xoxb-...",
    "appToken": "xapp-...",
    "dmPolicy": "pairing",
    "allowFrom": ["U123", "U456"],
    "channels": {
      "C123": {
        "allow": true,
        "requireMention": true,
        "allowBots": false
      },
      "#general": {
        "allow": true,
        "requireMention": true,
        "users": ["U123"],
        "skills": ["docs"],
        "systemPrompt": "Short answers only."
      }
    },
    "historyLimit": 50,
    "replyToMode": "off",
    "streaming": "partial",
    "nativeStreaming": true,
    "reactionNotifications": "own",
    "reactionAllowlist": ["U123"],
    "actions": {
      "reactions": true,
      "messages": true,
      "pins": true,
      "memberInfo": true,
      "emojiList": true
    },
    "slashCommand": {
      "enabled": true,
      "name": "openclaw",
      "sessionPrefix": "slack:slash",
      "ephemeral": true
    },
    "thread": {
      "historyScope": "thread",
      "inheritParent": false
    },
    "typingReaction": "hourglass_flowing_sand",
    "textChunkLimit": 4000,
    "chunkMode": "length",
    "mediaMaxMb": 20
  }
}
```

---

## WhatsApp

```json5
"channels": {
  "whatsapp": {
    "enabled": true,
    "dmPolicy": "pairing",
    "allowFrom": ["+15555550123"],
    "textChunkLimit": 4000,
    "chunkMode": "length",
    "mediaMaxMb": 50,
    "sendReadReceipts": true,
    "groups": {
      "*": { "requireMention": true }
    },
    "groupPolicy": "allowlist",
    "groupAllowFrom": ["+15551234567"],
    "historyLimit": 50
  }
}
```

---

## Signal

```json5
"channels": {
  "signal": {
    "enabled": true,
    "account": "+15555550123",
    "dmPolicy": "pairing",
    "allowFrom": ["+15551234567", "uuid:123e4567-e89b-12d3-a456-426614174000"],
    "reactionNotifications": "own",
    "historyLimit": 50,
    "configWrites": true
  }
}
```

---

## iMessage (macOS)

```json5
"channels": {
  "imessage": {
    "enabled": true,
    "cliPath": "imsg",
    "dbPath": "~/Library/Messages/chat.db",
    "remoteHost": "user@gateway-host",
    "dmPolicy": "pairing",
    "allowFrom": ["+15555550123", "user@example.com"],
    "historyLimit": 50,
    "includeAttachments": false,
    "attachmentRoots": ["/Users/*/Library/Messages/Attachments"],
    "mediaMaxMb": 16,
    "service": "auto",
    "region": "US"
  }
}
```

---

## 通用 Channel 配置字段速查

| 字段 | 适用 Channel | 描述 |
|------|-------------|------|
| `dmPolicy` | 全部 | DM 策略 |
| `allowFrom` | 全部 | DM 白名单 |
| `groupPolicy` | 全部 | Group 策略 |
| `groupAllowFrom` | 全部 | Group 白名单 |
| `groups` | 全部 | Per-group 配置对象 |
| `groups.*.requireMention` | TG/DC/Slack/GC/WS/iMsg | 群组是否需要 @mention |
| `groups.*.systemPrompt` | TG/DC/Slack/GC | 群组系统提示词 |
| `groups.*.skills` | TG/DC/Slack/GC | 群组专用技能 |
| `mediaMaxMb` | 全部 | 媒体文件最大 MB |
| `historyLimit` | 全部 | 历史消息条数 |
| `reactionNotifications` | 全部 | 反应通知模式 |
| `typingIndicator` | GC/Feishu/iMsg | 打字指示器 |
| `resolveSenderNames` | Feishu | 解析发送者姓名 |
| `requireMention` | TG/Feishu/GC | DM 中是否需要 mention |
| `webhookPath` | Feishu/TG | Webhook 路径 |
| `connectionMode` | Feishu | 连接模式 |
| `streaming` | TG/Slack/Discord | 流式模式 |
| `replyToMode` | TG/Slack/Discord | 回复模式 |
| `customCommands` | TG | 自定义命令菜单 |
| `modelByChannel` | TG/Discord/Slack | 按 ChatID 固定模型 |
| `defaultAccount` | 多账号 channel | 默认账号 |
| `accounts` | TG/Discord/Slack/WS | 多账号配置 |
| `configWrites` | TG/Slack/Signal/iMsg/IRC/Mattermost | 允许 channel 写入配置 |
