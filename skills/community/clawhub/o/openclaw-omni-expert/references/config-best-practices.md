# OpenClaw 配置最佳实践

## 目录
- [AI 模型配置](#ai-模型配置)
- [通讯渠道配置](#通讯渠道配置)
- [网关配置](#网关配置)
- [记忆系统配置](#记忆系统配置)
- [安全配置](#安全配置)
- [性能优化](#性能优化)

---

## AI 模型配置

### 选择指南

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| 日常对话 | GPT-4o-mini | 性价比高，响应快 |
| 长文本分析 | Claude 3.5 Sonnet | 200K 上下文窗口 |
| 代码生成 | DeepSeek Coder | 专门优化，价格低 |
| 中文场景 | 通义千问 Plus | 中文能力强 |
| 隐私敏感 | Ollama (本地) | 完全离线 |
| 企业合规 | Azure OpenAI | SLA 保障 |

### 配置模板

#### OpenAI
```json
{
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "api_key": "sk-...",
    "temperature": 0.7,
    "max_tokens": 4096
  }
}
```

#### Anthropic Claude
```json
{
  "model": {
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514",
    "api_key": "sk-ant-...",
    "temperature": 0.7,
    "max_tokens": 4096
  }
}
```

#### DeepSeek
```json
{
  "model": {
    "provider": "deepseek",
    "model": "deepseek-chat",
    "api_key": "sk-...",
    "temperature": 0.7,
    "max_tokens": 4096
  }
}
```

#### Ollama (本地)
```json
{
  "model": {
    "provider": "ollama",
    "model": "llama3.3",
    "api_base": "http://localhost:11434/v1",
    "temperature": 0.7,
    "max_tokens": 4096
  }
}
```

### 参数调优

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| temperature | 随机性 | 0.7 (平衡) / 0.3 (精确) / 0.9 (创意) |
| max_tokens | 最大响应长度 | 2048-4096 |
| top_p | 核采样 | 0.9 |

---

## 通讯渠道配置

### Telegram

#### 最简配置
```json
{
  "channels": [{
    "type": "telegram",
    "enabled": true,
    "bot_token": "123456:ABC-DEF..."
  }]
}
```

#### 生产配置
```json
{
  "channels": [{
    "type": "telegram",
    "enabled": true,
    "bot_token": "123456:ABC-DEF...",
    "chat_ids": ["123456789", "-1001234567890"],
    "allow_groups": false,
    "allow_private": true,
    "rate_limit": {
      "enabled": true,
      "messages_per_minute": 20
    }
  }]
}
```

### Discord

```json
{
  "channels": [{
    "type": "discord",
    "enabled": true,
    "bot_token": "MTE...",
    "guild_id": "123456789",
    "channel_ids": ["123456789"],
    "intents": ["message_content", "guild_messages"],
    "command_prefix": "!"
  }]
}
```

### 飞书

```json
{
  "channels": [{
    "type": "feishu",
    "enabled": true,
    "app_id": "cli_...",
    "app_secret": "...",
    "bot_name": "OpenClaw Bot",
    "event_subscription": true
  }]
}
```

### 企业微信

```json
{
  "channels": [{
    "type": "wecom",
    "enabled": true,
    "corp_id": "ww...",
    "corp_secret": "...",
    "agent_id": "1000001"
  }]
}
```

### 多渠道配置

```json
{
  "channels": [
    {
      "type": "telegram",
      "enabled": true,
      "bot_token": "..."
    },
    {
      "type": "discord",
      "enabled": true,
      "bot_token": "..."
    }
  ]
}
```

---

## 网关配置

### 本地网关（开发/个人）

```json
{
  "gateway": {
    "host": "127.0.0.1",
    "port": 18789,
    "ssl": {
      "enabled": false
    },
    "cors": {
      "enabled": true,
      "origins": ["http://localhost:3000"]
    }
  }
}
```

### 远程网关（团队）

```json
{
  "gateway": {
    "host": "0.0.0.0",
    "port": 18789,
    "ssl": {
      "enabled": true,
      "cert_file": "/etc/openclaw/cert.pem",
      "key_file": "/etc/openclaw/key.pem"
    },
    "cors": {
      "enabled": true,
      "origins": ["https://your-domain.com"]
    },
    "authentication": {
      "enabled": true,
      "jwt_secret": "your-secret-key",
      "token_expiry": "24h"
    },
    "rate_limit": {
      "enabled": true,
      "requests_per_minute": 120
    }
  }
}
```

### 高可用网关（企业）

```json
{
  "gateway": {
    "cluster": {
      "enabled": true,
      "nodes": [
        {"host": "node1.example.com", "port": 18789},
        {"host": "node2.example.com", "port": 18789}
      ],
      "strategy": "round_robin",
      "health_check_interval": 30
    },
    "ssl": {
      "enabled": true,
      "cert_file": "/etc/openclaw/fullchain.pem",
      "key_file": "/etc/openclaw/privkey.pem"
    },
    "load_balancer": {
      "enabled": true,
      "health_check_path": "/api/health"
    }
  }
}
```

---

## 记忆系统配置

### 基础记忆（轻量）

```json
{
  "memory": {
    "enabled": true,
    "type": "basic",
    "max_history": 100,
    "summary_enabled": true,
    "summary_threshold": 50
  }
}
```

### 向量记忆（检索）

```json
{
  "memory": {
    "enabled": true,
    "type": "vector",
    "provider": "chroma",
    "chroma": {
      "persist_directory": "~/.openclaw/chroma",
      "collection_name": "openclaw_memory",
      "embedding_model": "text-embedding-3-small"
    }
  }
}
```

### 知识图谱记忆（复杂关系）

```json
{
  "memory": {
    "enabled": true,
    "type": "graph",
    "provider": "networkx",
    "graph": {
      "persist_file": "~/.openclaw/knowledge_graph.gpickle",
      "max_nodes": 10000,
      "inference_depth": 3
    }
  }
}
```

---

## 安全配置

### 必需安全配置

```json
{
  "security": {
    "api_key_encryption": true,
    "log_sensitive_data": false,
    "allowed_origins": ["https://your-domain.com"],
    "cors_credentials": true,
    "rate_limit": {
      "enabled": true,
      "max_requests": 100,
      "window_seconds": 60
    }
  }
}
```

### JWT 认证配置

```json
{
  "authentication": {
    "jwt": {
      "secret": "your-256-bit-secret",
      "algorithm": "HS256",
      "expiry": "24h",
      "refresh_expiry": "7d"
    },
    "allowed_users": [
      {"username": "admin", "role": "admin"},
      {"username": "user", "role": "user"}
    ]
  }
}
```

### TLS/SSL 配置

```json
{
  "ssl": {
    "enabled": true,
    "cert_file": "/path/to/cert.pem",
    "key_file": "/path/to/key.pem",
    "min_version": "TLSv1.2",
    "ciphers": "ECDHE-RSA-AES256-GCM-SHA512"
  }
}
```

---

## 性能优化

### 推荐配置

```json
{
  "performance": {
    "connection_pool": {
      "max_size": 100,
      "min_size": 10,
      "idle_timeout": 300
    },
    "cache": {
      "enabled": true,
      "provider": "redis",
      "ttl": 3600,
      "max_size": "1gb"
    },
    "streaming": {
      "enabled": true,
      "buffer_size": 4096
    },
    "async_processing": {
      "enabled": true,
      "worker_count": 4
    }
  }
}
```

### 多语言配置

```json
{
  "i18n": {
    "default_locale": "zh-CN",
    "supported_locales": ["zh-CN", "en-US", "ja-JP"],
    "fallback_locale": "en-US"
  }
}
```

---

## 完整配置示例

### 个人使用

```json
{
  "version": "1.0",
  "openclaw": {
    "data_dir": "~/.openclaw",
    "log_dir": "~/.openclaw/logs"
  },
  "model": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "api_key": "sk-...",
    "temperature": 0.7
  },
  "gateway": {
    "host": "127.0.0.1",
    "port": 18789
  },
  "channels": [{
    "type": "telegram",
    "enabled": true,
    "bot_token": "..."
  }],
  "memory": {
    "enabled": true,
    "type": "basic"
  }
}
```

### 企业部署

```json
{
  "version": "1.0",
  "openclaw": {
    "data_dir": "/var/lib/openclaw",
    "log_dir": "/var/log/openclaw",
    "plugin_dir": "/var/lib/openclaw/plugins"
  },
  "model": {
    "provider": "azure",
    "api_base": "https://xxx.openai.azure.com",
    "api_key": "...",
    "api_version": "2024-02-01",
    "deployment_name": "gpt-4o"
  },
  "gateway": {
    "cluster": {
      "enabled": true,
      "nodes": [
        {"host": "lb1.example.com", "port": 18789},
        {"host": "lb2.example.com", "port": 18789}
      ]
    },
    "ssl": {
      "enabled": true,
      "cert_file": "/etc/ssl/openclaw/fullchain.pem",
      "key_file": "/etc/ssl/openclaw/privkey.pem"
    },
    "authentication": {
      "enabled": true,
      "jwt_secret": "${JWT_SECRET}"
    }
  },
  "channels": [
    {
      "type": "feishu",
      "enabled": true,
      "app_id": "${FEISHU_APP_ID}",
      "app_secret": "${FEISHU_APP_SECRET}"
    },
    {
      "type": "wecom",
      "enabled": true,
      "corp_id": "${WECOM_CORP_ID}",
      "corp_secret": "${WECOM_CORP_SECRET}",
      "agent_id": "${WECOM_AGENT_ID}"
    }
  ],
  "memory": {
    "enabled": true,
    "type": "vector",
    "provider": "chroma",
    "chroma": {
      "persist_directory": "/var/lib/openclaw/chroma"
    }
  },
  "security": {
    "api_key_encryption": true,
    "log_sensitive_data": false
  },
  "performance": {
    "cache": {
      "enabled": true,
      "provider": "redis",
      "host": "redis.example.com",
      "port": 6379
    }
  }
}
```

---

## 环境变量

推荐使用环境变量存储敏感信息：

| 变量 | 说明 |
|------|------|
| `OPENCLAW_API_KEY` | AI 模型 API Key |
| `OPENCLAW_JWT_SECRET` | JWT 密钥 |
| `OPENCLAW_DB_URL` | 数据库连接 |
| `OPENCLAW_REDIS_URL` | Redis 连接 |

引用方式：
```json
{
  "model": {
    "api_key": "${OPENCLAW_API_KEY}"
  }
}
```

---

## 验证配置

配置完成后，使用以下命令验证：

```bash
# 检查配置语法
openclaw config validate

# 测试 AI 连接
openclaw config test-ai

# 测试渠道连接
openclaw config test-channels

# 完整健康检查
openclaw health
```
