# OpenClaw 配置参考

## 配置文件位置

OpenClaw 按以下顺序查找配置文件：

1. `--config` 命令行参数指定的路径
2. `./openclaw.json` - 当前工作目录
3. `~/.openclaw/openclaw.json` - 用户配置目录

## 完整配置结构

```json
{
  "providers": { ... },
  "models": { ... },
  "agents": { ... },
  "channels": { ... },
  "skills": { ... },
  "security": { ... },
  "storage": { ... }
}
```

## providers 配置

### OpenAI

```json
{
  "providers": {
    "openai": {
      "apiKey": "${OPENAI_API_KEY}",
      "baseUrl": "https://api.openai.com/v1",
      "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
    }
  }
}
```

### Anthropic

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "${ANTHROPIC_API_KEY}",
      "baseUrl": "https://api.anthropic.com",
      "models": ["claude-3-opus", "claude-3-sonnet"]
    }
  }
}
```

### 自定义提供商

```json
{
  "providers": {
    "my-custom": {
      "apiKey": "${MY_API_KEY}",
      "baseUrl": "https://api.example.com/v1",
      "headers": {
        "X-Custom-Header": "value"
      }
    }
  }
}
```

## models 配置

### 模型别名

```json
{
  "models": {
    "fast": "gpt-3.5-turbo",
    "smart": "gpt-4",
    "creative": "claude-3-opus"
  }
}
```

### 模型参数覆盖

```json
{
  "models": {
    "gpt-4": {
      "temperature": 0.7,
      "maxTokens": 4096
    }
  }
}
```

## agents 配置

### 默认 Agent

```json
{
  "agents": {
    "default": {
      "model": "gpt-4",
      "provider": "openai",
      "systemPrompt": "You are a helpful assistant.",
      "temperature": 0.7
    }
  }
}
```

### 自定义 Agent

```json
{
  "agents": {
    "coder": {
      "model": "claude-3-opus",
      "provider": "anthropic",
      "systemPrompt": "You are an expert programmer...",
      "skills": ["coding-agent"],
      "tools": ["read", "write", "exec", "web_search"]
    }
  }
}
```

### Agent 选项

| 选项 | 类型 | 说明 |
|------|------|------|
| `model` | string | 使用的模型 |
| `provider` | string | 提供商名称 |
| `systemPrompt` | string | 系统提示 |
| `temperature` | number | 温度参数 (0-1) |
| `maxTokens` | number | 最大 token 数 |
| `skills` | string[] | 启用的技能 |
| `tools` | string[] | 允许的工具 |
| `metadata` | object | 自定义元数据 |

## channels 配置

### Discord

```json
{
  "channels": {
    "discord": {
      "token": "${DISCORD_TOKEN}",
      "clientId": "123456789",
      "guildId": "987654321",
      "permissions": {
        "allowlist": ["user_id_1", "role_id_2"]
      }
    }
  }
}
```

### Telegram

```json
{
  "channels": {
    "telegram": {
      "token": "${TELEGRAM_TOKEN}",
      "allowedChats": ["chat_id_1", "chat_id_2"]
    }
  }
}
```

## skills 配置

### 技能路径

```json
{
  "skills": {
    "paths": [
      "./skills",
      "./.agents/skills",
      "~/.agents/skills"
    ],
    "disabled": ["unwanted-skill"]
  }
}
```

## security 配置

### 安全选项

```json
{
  "security": {
    "elevated": {
      "allowlist": ["allowed_command_1", "allowed_command_2"]
    },
    "policy": {
      "network": "allowlist",
      "filesystem": "sandbox"
    }
  }
}
```

## storage 配置

### 存储选项

```json
{
  "storage": {
    "sessions": "./data/sessions",
    "logs": "./data/logs",
    "cache": "./data/cache"
  }
}
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENCLAW_API_KEY` | Gateway API 密钥 |
| `OPENCLAW_PORT` | Gateway 端口 |
| `OPENCLAW_CONFIG` | 配置文件路径 |
| `OPENAI_API_KEY` | OpenAI API 密钥 |
| `ANTHROPIC_API_KEY` | Anthropic API 密钥 |

---

最后更新：2026-03-13