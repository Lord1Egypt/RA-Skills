# OpenClaw Configuration Reference

Complete configuration options for `~/.openclaw/openclaw.json`.

## Top-Level Structure

```json5
{
  gateway: { ... },      // Gateway server settings
  agents: { ... },       // Agent runtime settings
  channels: { ... },     // Messaging channel configs
  models: { ... },       // Model provider configs
  skills: { ... },       // Skills system configs
  cron: { ... },         // Scheduled jobs
  memory: { ... },       // Memory system
  browser: { ... },      // Browser automation
  canvas: { ... },       // Canvas workspace
}
```

## Gateway Configuration

```json5
{
  gateway: {
    enabled: true,           // Enable gateway
    port: 18789,             // WebSocket port
    mode: "local",           // "local" or "remote"
    bind: "0.0.0.0",         // Bind address (0.0.0.0 for LAN)
    auth: {
      mode: "token",         // "none", "token", "password"
      token: "your-token"    // Auth token (if mode="token")
    },
    tls: {
      enabled: false,        // Enable HTTPS/WSS
      cert: "/path/to/cert",
      key: "/path/to/key"
    },
    tailscale: {
      enabled: false,        // Enable Tailscale Serve
      funnel: false          // Enable public funnel
    }
  }
}
```

## Agent Configuration

```json5
{
  agents: {
    defaults: {
      model: "anthropic/claude-opus-4-6",  // Default model
      thinking: {
        enabled: true,
        level: "medium"       // "low", "medium", "high"
      },
      workspace: "~/.openclaw/workspace",
      compaction: {
        mode: "safeguard"     // Context compaction strategy
      },
      maxConcurrent: 4,       // Max concurrent agents
      subagents: {
        maxConcurrent: 8
      },
      sandbox: {
        mode: "non-main",     // "none", "non-main", "all"
        allowlist: ["bash", "read", "write"],
        denylist: ["browser", "canvas"]
      }
    }
  }
}
```

## Model Provider Configuration

### Anthropic

```json5
{
  models: {
    providers: {
      anthropic: {
        baseUrl: "https://api.anthropic.com",
        apiKey: "${ANTHROPIC_API_KEY}",  // From credentials
        models: [
          {
            id: "claude-opus-4-6",
            name: "Claude Opus 4.6",
            contextWindow: 200000,
            maxTokens: 16384
          }
        ]
      }
    }
  }
}
```

### Volcengine (Kimi)

```json5
{
  models: {
    providers: {
      volcengine: {
        baseUrl: "https://ark.cn-beijing.volces.com/api/coding/v3",
        apiKey: "${VOLCENGINE_API_KEY}",
        models: [
          {
            id: "kimi-k2.5",
            name: "Kimi K2.5",
            contextWindow: 128000,
            maxTokens: 8192
          }
        ]
      }
    }
  }
}
```

### OpenAI

```json5
{
  models: {
    providers: {
      openai: {
        baseUrl: "https://api.openai.com/v1",
        apiKey: "${OPENAI_API_KEY}",
        models: [
          { id: "gpt-5.2", name: "GPT-5.2" },
          { id: "o3", name: "O3" }
        ]
      }
    }
  }
}
```

### Local (Ollama/LMStudio)

```json5
{
  models: {
    providers: {
      ollama: {
        baseUrl: "http://127.0.0.1:11434",
        apiKey: "ollama",
        api: "ollama",
        models: [
          {
            id: "qwen3:8b",
            name: "Qwen3 8B",
            contextWindow: 32768
          }
        ]
      }
    }
  }
}
```

## Channel Configuration

### Telegram

```json5
{
  telegram: {
    enabled: true,
    botToken: "${TELEGRAM_BOT_TOKEN}",
    dmPolicy: "open",          // "open" or "pairing"
    streaming: "partial",      // "none", "partial", "full"
    allowFrom: ["*"],          // Allowed senders
    groups: {
      "*": {
        requireMention: true,  // Require @mention
        activation: "mention"  // "mention", "always", "reply"
      }
    }
  }
}
```

### Slack

```json5
{
  slack: {
    enabled: true,
    botToken: "${SLACK_BOT_TOKEN}",
    appToken: "${SLACK_APP_TOKEN}",
    signingSecret: "${SLACK_SIGNING_SECRET}",
    dmPolicy: "pairing"
  }
}
```

### Discord

```json5
{
  discord: {
    enabled: true,
    botToken: "${DISCORD_BOT_TOKEN}",
    clientId: "${DISCORD_CLIENT_ID}",
    dmPolicy: "pairing"
  }
}
```

### WhatsApp

```json5
{
  whatsapp: {
    enabled: true,
    dmPolicy: "pairing",
    allowFrom: ["+1234567890"],
    groups: {
      "*": { requireMention: true }
    }
  }
}
```

## Skills Configuration

```json5
{
  skills: {
    install: {
      nodeManager: "npm"       // "npm" or "pnpm"
    },
    entries: {
      "skill-name": {
        enabled: true,
        apiKey: "${SKILL_API_KEY}",
        env: {
          "CUSTOM_VAR": "value"
        }
      }
    }
  }
}
```

## Cron Jobs

```json5
{
  cron: {
    enabled: true,
    jobs: [
      {
        id: "daily-report",
        schedule: "0 9 * * *",    // Cron expression
        session: "main",
        message: "Generate daily report"
      }
    ]
  }
}
```

## Memory System

```json5
{
  memory: {
    enabled: true,
    provider: "lancedb",        // "lancedb", "sqlite-vec"
    embedding: {
      provider: "openai",
      model: "text-embedding-3-small"
    }
  }
}
```

## Browser Automation

```json5
{
  browser: {
    enabled: true,
    headless: false,
    color: "#FF4500",           // Browser frame color
    profile: "~/.openclaw/browser/profile"
  }
}
```

## Canvas Workspace

```json5
{
  canvas: {
    enabled: true,
    port: 18790,                // Canvas server port
    a2ui: true                  // Enable A2UI protocol
  }
}
```

## Environment Variables

Credentials are stored in `~/.openclaw/credentials/` and referenced via `${VAR_NAME}`:

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key |
| `OPENAI_API_KEY` | OpenAI API key |
| `VOLCENGINE_API_KEY` | Volcengine (Kimi) API key |
| `GOOGLE_API_KEY` | Google AI API key |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `SLACK_BOT_TOKEN` | Slack bot token |

## Set Credentials

```bash
# Set API key
openclaw credentials set anthropic sk-ant-xxxxx

# List credentials
openclaw credentials list

# Delete credential
openclaw credentials delete anthropic
```

## Configuration Commands

```bash
# Get config value
openclaw config get agents.defaults.model

# Set config value
openclaw config set agents.defaults.model anthropic/claude-opus-4-6

# Edit config in editor
openclaw config edit

# Validate config
openclaw config validate
```
