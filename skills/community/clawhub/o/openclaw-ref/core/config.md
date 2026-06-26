# 完整配置参考与示例

## 最小配置
```json5
{
  agent: { workspace: "~/.openclaw/workspace" },
  channels: { whatsapp: { allowFrom: ["+15551234567"] } }
}
```

## 推荐入门配置
```json5
{
  identity: { name: "Astral", theme: "helpful assistant", emoji: "✨" },
  agent: {
    workspace: "~/.openclaw/workspace",
    model: { primary: "anthropic/claude-sonnet-4-5" }
  },
  channels: {
    telegram: {
      botToken: "YOUR_TOKEN",
      allowFrom: ["123456789"],
      groups: { "*": { requireMention: true } }
    }
  }
}
```

## 完整配置示例
```json5
{
  // 环境变量
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
    shellEnv: { enabled: true, timeoutMs: 15000 }
  },

  // 认证
  auth: {
    profiles: {
      "anthropic:default": { provider: "anthropic", mode: "api_key" },
      "openai:default": { provider: "openai", mode: "api_key" }
    },
    order: { anthropic: ["anthropic:default"] }
  },

  // 身份
  identity: { name: "Astral", theme: "helpful assistant", emoji: "✨" },

  // 日志
  logging: {
    level: "info",
    consoleLevel: "warn",
    consoleStyle: "pretty",
    redactSensitive: "tools"
  },

  // 消息格式
  messages: {
    messagePrefix: "",
    responsePrefix: "",
    ackReaction: "👀",
    ackReactionScope: "group-mentions"
  },

  // 路由+队列
  routing: {
    groupChat: { mentionPatterns: ["@bot"], historyLimit: 50 },
    queue: {
      mode: "collect",       // collect|fifo
      debounceMs: 1000,
      cap: 20,
      drop: "summarize"      // summarize|oldest|newest
    }
  },

  // 工具
  tools: {
    policy: "full",
    media: {
      audio: {
        enabled: true,
        maxBytes: 20971520,
        models: [{ provider: "openai", model: "gpt-4o-mini-transcribe" }],
        timeoutSeconds: 120
      },
      video: {
        enabled: true,
        maxBytes: 52428800,
        models: [{ provider: "google", model: "gemini-3-flash-preview" }]
      }
    }
  },

  // 会话
  session: {
    scope: "per-sender",     // main|per-peer|per-channel-peer|per-account-channel-peer
    reset: { mode: "daily", atHour: 4, idleMinutes: 60 },
    resetByChannel: { discord: { mode: "idle", idleMinutes: 10080 } },
    resetTriggers: ["/new", "/reset"],
    sendPolicy: {
      default: "allow",
      rules: [{ action: "deny", match: { channel: "discord", chatType: "group" } }]
    }
  },

  // 智能体
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      userTimezone: "Asia/Shanghai",
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"]
      },
      imageModel: { primary: "openrouter/anthropic/claude-sonnet-4-5" },
      models: {
        "anthropic/claude-opus-4-5": { alias: "opus" },
        "anthropic/claude-sonnet-4-5": { alias: "sonnet" }
      },
      thinkingDefault: "off",
      verboseDefault: "off",
      elevatedDefault: "on",
      timeoutSeconds: 600,
      maxConcurrent: 1,
      contextTokens: 200000,
      mediaMaxMb: 5,
      heartbeat: { every: "30m", target: "last" },
      compaction: { mode: "default", reserveTokensFloor: 20000 },
      contextPruning: { mode: "adaptive", keepLastAssistants: 3 },
      subagents: { maxConcurrent: 8, archiveAfterMinutes: 60 },
      memorySearch: { extraPaths: [] }
    }
  },

  // 网关
  gateway: {
    port: 18789,
    host: "127.0.0.1",
    auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" },
    reload: { mode: "hybrid" },
    http: { endpoints: {
      responses: { enabled: false },
      chat: { enabled: false }
    }}
  },

  // 浏览器
  browser: { enabled: true, headless: true, defaultProfile: "chrome" },

  // 定时任务
  cron: { enabled: true },

  // Hooks
  hooks: {
    internal: {
      enabled: true,
      entries: { "session-memory": { enabled: true } }
    }
  },

  // 插件
  plugins: { enabled: true },

  // 命令
  commands: { config: false, debug: false, bash: false }
}
```

## 常见模式

### 多平台设置 (Telegram + WhatsApp)
```json5
channels: {
  telegram: { botToken: "TOKEN", allowFrom: ["123"] },
  whatsapp: { allowFrom: ["+155..."] }
}
```

### OAuth + API Key 回退
```json5
auth: {
  profiles: {
    "anthropic:oauth": { provider: "anthropic", mode: "oauth" },
    "anthropic:api": { provider: "anthropic", mode: "api_key" }
  },
  order: { anthropic: ["anthropic:oauth", "anthropic:api"] }
}
```

### 仅本地模型 (Ollama)
```json5
agents: { defaults: { model: { primary: "ollama/llama3.3" } } }
```

### 工作机器人 (受限访问)
```json5
{
  tools: { policy: "allowlist", allow: ["group:fs", "group:web"] },
  agents: { defaults: { sandbox: { mode: "all" } } }
}
```

## 遗漏的配置字段补充

### identity
| 路径 | 类型 | 说明 |
|------|------|------|
| `identity.name` | string | 智能体名称 |
| `identity.theme` | string | 主题描述 |
| `identity.emoji` | string | 签名emoji |

### messages
| 路径 | 类型 | 说明 |
|------|------|------|
| `messages.messagePrefix` | string | 消息前缀 |
| `messages.responsePrefix` | string | 回复前缀 |
| `messages.ackReaction` | string | 确认反应emoji |
| `messages.ackReactionScope` | string | 反应范围 |

### routing.queue
| 路径 | 类型 | 说明 |
|------|------|------|
| `routing.queue.mode` | string | collect/fifo |
| `routing.queue.debounceMs` | number | 防抖延迟(ms) |
| `routing.queue.cap` | number | 队列上限 |
| `routing.queue.drop` | string | 溢出策略(summarize/oldest/newest) |

### tools.media
| 路径 | 类型 | 说明 |
|------|------|------|
| `tools.media.audio.enabled` | bool | 启用音频转录 |
| `tools.media.audio.models` | array | 转录模型列表 |
| `tools.media.video.enabled` | bool | 启用视频理解 |
| `tools.media.video.models` | array | 视频模型列表 |

### web搜索配置
```json5
// Brave搜索 (默认)
env: { BRAVE_API_KEY: "BSA..." }

// Perplexity (通过OpenRouter)
env: { OPENROUTER_API_KEY: "sk-or-..." }
// 或直连
env: { PERPLEXITY_API_KEY: "pplx-..." }
```

### TTS配置
```json5
tts: {
  provider: "elevenlabs",    // elevenlabs|openai|deepgram
  voice: "nova",
  model: "eleven_multilingual_v2",
  speed: 1.0,
  mode: "off"               // off|always|inbound|tagged
}
```
