# OpenClaw 复杂配置操作指南

本指南提供 OpenClaw 配置文件 `~/.openclaw/openclaw.json` 的复杂操作步骤，包括前置条件、详细步骤、验证方法和常见错误处理。

## 📋 目录

1. [添加新的模型提供者](#1-添加新的模型提供者)
2. [配置新的频道](#2-配置新的频道)
3. [修改 Agent 工具配置](#3-修改-agent-工具配置)
4. [调整诊断和日志设置](#4-调整诊断和日志设置)
5. [配置 ACP 运行时](#5-配置-acp-运行时)
6. [配置 MCP 服务器](#6-配置-mcp-服务器)
7. [配置审批策略](#7-配置审批策略)

---

## 1. 添加新的模型提供者

### 一句话

在 `models.providers` 中注册新提供者，在 `agents.defaults.model` 中启用。

### 核心要点

- API Key 优先使用环境变量引用（`env:VAR_NAME`）
- `api` 字段必须与提供者兼容（`openai-completions` / `anthropic-messages` 等）
- 模型 `id` 必须与提供者 API 中的实际模型 ID 完全一致
- 建议设置 `fallbacks` 链确保高可用

### 详细内容

#### 前置条件检查

- [ ] 已获取模型提供者的 API Key 或 OAuth 凭证
- [ ] 已确认提供者的 API 端点 URL
- [ ] 已确认 API 兼容类型（OpenAI Completions / Anthropic Messages 等）
- [ ] 已了解模型的参数限制（上下文窗口、最大 Token 数等）
- [ ] OpenClaw Gateway 已停止运行

#### 操作步骤

**步骤 1: 添加认证配置**

在 `auth.profiles` 部分添加新的认证配置：

```json
{
  "auth": {
    "profiles": {
      "yourprovider:default": {
        "provider": "yourprovider",
        "mode": "api_key"
      }
    }
  }
}
```

**可选认证模式**：
- `api_key`: 使用 API 密钥认证
- `oauth`: 使用 OAuth 认证

**步骤 2: 配置环境变量（如需要）**

如果使用 API Key，在 `env.vars` 部分添加：

```json
{
  "env": {
    "vars": {
      "YOURPROVIDER_API_KEY": "your-api-key-here"
    }
  }
}
```

**步骤 3: 添加模型提供者配置**

在 `models.providers` 部分添加新提供者：

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "yourprovider": {
        "baseUrl": "https://api.yourprovider.com/v1",
        "apiKey": "env:YOURPROVIDER_API_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "model-name",
            "name": "Display Name",
            "reasoning": true,
            "input": ["text"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            },
            "contextWindow": 128000,
            "maxTokens": 4096
          }
        ]
      }
    }
  }
}
```

**关键字段说明**：
- `baseUrl`: API 端点 URL
- `apiKey`: 认证密钥，支持 `env:VAR_NAME` 引用环境变量，也支持 `{ source: "env"|"file"|"exec", provider, id }` 高级格式
- `api`: API 类型（`openai-completions` / `anthropic-messages` 等）
- `models`: 模型列表数组

**步骤 4: 在 Agent 默认配置中注册模型**

在 `agents.defaults.models` 部分添加新模型：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "yourprovider/model-name",
        "fallbacks": ["zai/glm-5"]
      },
      "models": {
        "yourprovider/model-name": {}
      }
    }
  }
}
```

**步骤 5: 启动 Gateway 并验证**

```bash
# 启动 Gateway
openclaw gateway

# 在另一个终端验证配置
openclaw doctor

# 测试模型调用
openclaw gateway call chat --params '{"message":"测试"}'
```

#### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```
   检查输出中是否包含新提供者信息

2. **模型可用性**：
   ```bash
   openclaw gateway call models.list --params '{}'
   ```
   确认新模型出现在列表中

3. **实际调用测试**：
   发送测试消息，验证模型响应

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Unknown provider` | 提供者 ID 拼写错误 | 检查 `auth.profiles` 和 `models.providers` 中的 ID 一致性 |
| `Invalid API key` | API Key 未设置或错误 | 确认 `env.vars` 中的变量名正确，且 `apiKey` 引用格式正确 |
| `Connection refused` | baseUrl 错误或服务不可用 | 验证 API 端点 URL 可访问性 |
| `Model not found` | 模型 ID 错误 | 检查提供者文档中的正确模型 ID |

---

## 2. 配置新的频道

### 一句话

在 `channels` 中添加频道配置，同时在 `plugins.entries` 中启用对应插件。

### 核心要点

- 频道配置（`channels`）和插件启用（`plugins.entries`）需同时配置
- Feishu 频道尤其需要注意两边一致性，否则会报 warning
- `dmPolicy` / `groupPolicy` 等策略控制频道的访问权限
- 建议先在测试环境验证 Webhook 或 WebSocket 连接

### 详细内容

#### 前置条件检查

- [ ] 已获取频道的 Bot Token 或 OAuth 凭证
- [ ] 已在频道平台创建 Bot 应用
- [ ] 已配置 Bot 的权限和范围
- [ ] OpenClaw Gateway 已停止运行

#### 操作步骤

**Telegram 配置**

1. **创建 Telegram Bot**：
   - 与 [@BotFather](https://t.me/BotFather) 对话
   - 使用 `/newbot` 命令创建新 Bot
   - 保存生成的 Bot Token

2. **添加配置**：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "your-telegram-bot-token",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "streaming": "partial"
    }
  },
  "plugins": {
    "entries": {
      "telegram": {
        "enabled": true
      }
    }
  }
}
```

**策略选项**：
- `dmPolicy`: `"open"` / `"pairing"` / `"closed"`
- `groupPolicy`: `"allowlist"` / `"blocklist"` / `"closed"`

#### Telegram 独立配置

**1. 创建 Telegram Bot**
- 与 [@BotFather](https://t.me/BotFather) 对话
- 使用 `/newbot` 命令创建新 Bot
- 保存生成的 Bot Token

**2. 获取你的 Telegram 用户 ID**
- 向 [@userinfobot](https://t.me/userinfobot) 或你的 Bot 发送消息
- 从回复中获取数字 ID

**3. 配置模板**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_TELEGRAM_USER_ID"],
      "groupPolicy": "disabled"
    }
  },
  "plugins": {
    "allow": ["openclaw-lark", "minimax", "feishu", "telegram"],
    "entries": {
      "minimax": { "enabled": true },
      "openclaw-lark": { "enabled": true },
      "feishu": { "enabled": true },
      "telegram": { "enabled": true }
    }
  }
}
```

**Telegram 策略说明**：

| 字段 | 选项 | 说明 |
|------|------|------|
| `dmPolicy` | `allowlist` | 仅白名单用户可私聊（推荐） |
| `dmPolicy` | `pairing` | 需要配对码 |
| `dmPolicy` | `open` | 所有人可私聊（不推荐） |
| `groupPolicy` | `disabled` | 禁止所有群聊 |
| `groupPolicy` | `open` | 所有群聊开放 |
| `groupPolicy` | `allowlist` | 仅白名单群聊可用 |
| `groupAllowFrom` | `["*"]` | 群里任何人都能 @ 机器人 |

#### 飞书（Feishu）独立配置

**1. 创建飞书应用**
- 登录 [飞书开放平台](https://open.feishu.cn/)
- 创建企业自建应用
- 获取 `App ID` (`cli_xxxxx`) 和 `App Secret`

**2. 配置应用权限**
- 开通以下权限：
  - `im:message`（读取消息）
  - `im:message:send_as_bot`（发送消息）
  - `im:chat`（群组管理）

**3. 获取你的飞书用户 ID**
- 在飞书给机器人发一条消息
- 查看 Gateway 日志：`tail -500 /tmp/openclaw/openclaw-*.log | grep "message from"`
- 日志输出格式：`received message from ou_xxxxxxxxx`

**4. 配置模板**

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "YOUR_FEISHU_APP_ID",
      "appSecret": { "source": "file", "provider": "lark-secrets", "id": "/lark/appSecret" },
      "domain": "feishu",
      "connectionMode": "websocket",
      "requireMention": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_FEISHU_USER_ID"],
      "groupPolicy": "open",
      "groupAllowFrom": ["*"],
      "groups": {
        "YOUR_FEISHU_GROUP_ID": { "enabled": true }
      }
    }
  },
  "plugins": {
    "allow": ["openclaw-lark", "minimax"],
    "entries": {
      "minimax": { "enabled": true },
      "openclaw-lark": { "enabled": true }
    }
  }
}
```

**飞书策略说明**：

| 字段 | 选项 | 说明 |
|------|------|------|
| `dmPolicy` | `allowlist` | 仅白名单用户可私聊（推荐） |
| `groupPolicy` | `open` | 所有群聊开放 |
| `groupAllowFrom` | `["*"]` | 群里任何人都能 @ 机器人 |
| `requireMention` | `true` | 必须 @ 机器人才会回复（推荐） |
| `connectionMode` | `websocket` | 使用 WebSocket 连接（推荐） |

#### Telegram + 飞书联合配置模板

**推荐配置（安全模式）：仅自己可用，禁止群聊**

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_TELEGRAM_USER_ID"],
      "groupPolicy": "disabled"
    },
    "feishu": {
      "enabled": true,
      "appId": "YOUR_FEISHU_APP_ID",
      "appSecret": { "source": "file", "provider": "lark-secrets", "id": "/lark/appSecret" },
      "domain": "feishu",
      "connectionMode": "websocket",
      "requireMention": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_FEISHU_USER_ID"],
      "groupPolicy": "open",
      "groupAllowFrom": ["*"],
      "groups": {
        "YOUR_FEISHU_GROUP_ID": { "enabled": true }
      }
    }
  },
  "plugins": {
    "allow": ["openclaw-lark", "minimax", "feishu", "telegram"],
    "entries": {
      "minimax": { "enabled": true },
      "openclaw-lark": { "enabled": true },
      "feishu": { "enabled": true },
      "telegram": { "enabled": true }
    }
  }
}
```

**开放配置（群聊可用，需 @）**：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TELEGRAM_BOT_TOKEN",
      "dmPolicy": "open",
      "groupPolicy": "open",
      "groupAllowFrom": ["*"],
      "requireMention": true
    },
    "feishu": {
      "enabled": true,
      "appId": "YOUR_FEISHU_APP_ID",
      "appSecret": { "source": "file", "provider": "lark-secrets", "id": "/lark/appSecret" },
      "domain": "feishu",
      "connectionMode": "websocket",
      "requireMention": true,
      "dmPolicy": "open",
      "groupPolicy": "open",
      "groupAllowFrom": ["*"]
    }
  },
  "plugins": {
    "allow": ["openclaw-lark", "minimax"],
    "entries": {
      "minimax": { "enabled": true },
      "openclaw-lark": { "enabled": true }
    }
  }
}
```

#### 飞书 AppSecret 安全存储

推荐将 AppSecret 存放在环境变量或 secrets 文件中，避免明文写入配置：

```json
{
  "appSecret": { "source": "file", "provider": "lark-secrets", "id": "/lark/appSecret" }
}
```

或直接使用环境变量：

```bash
# 在 ~/.openclaw/.env 中添加
export LARK_APP_SECRET="your-app-secret-here"

# 配置中引用
{
  "appSecret": "env:LARK_APP_SECRET"
}
```

#### 验证与排错

**1. 配置验证**
```bash
openclaw doctor
```

**2. 查看渠道连接状态**
```bash
openclaw channels status
openclaw config get channels.telegram
openclaw config get channels.feishu
```

**3. 获取用户 ID（日志法）**
```bash
# 飞书
tail -500 /tmp/openclaw/openclaw-*.log | grep "message from"
# 输出: received message from ou_xxxxxxxxx

# Telegram
tail -500 /tmp/openclaw/openclaw-*.log | grep "telegram.*message"
```

**4. 重启 Gateway**
```bash
openclaw gateway restart
```

**5. 查看日志**
```bash
openclaw logs --limit 200
tail -500 /tmp/openclaw/openclaw-*.log | grep feishu
tail -500 /tmp/openclaw/openclaw-*.log | grep telegram
```

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `plugins.entries.X: plugin disabled (disabled in config) but config is present` | 频道和插件配置不一致 | 同时检查并启用 `channels.X` 和 `plugins.entries.X.enabled` |
| `飞书无法连接` | 飞书插件名称错误 | 使用 `openclaw-lark` 而不是 `feishu` 作为 plugins.entries 的 key |
| `私聊不回复` | 用户ID未加入白名单 | 将用户 ID 加入 `channels.xxx.allowFrom`，参考日志获取 ID |
| `群聊不回复` | `requireMention: true` 时必须 @ 机器人 | 设置 `requireMention: false` 或群里 @ 机器人 |
| `Gateway 启动失败` | 配置了不存在的字段或值 | 检查 `groupPolicy: "deny"` 应为 `disabled`，运行 `openclaw doctor` |

---

**Discord 配置**

1. **创建 Discord 应用**：
   - 访问 [Discord Developer Portal](https://discord.com/developers/applications)
   - 创建应用并启用 Bot
   - 保存 Bot Token
   - 配置 OAuth2 权限

2. **添加配置**：

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "botToken": "your-discord-bot-token",
      "dmPolicy": "pairing",
      "guildPolicy": "allowlist",
      "streaming": "partial"
    }
  },
  "plugins": {
    "entries": {
      "discord": {
        "enabled": true
      }
    }
  }
}
```

**Slack 配置**

1. **创建 Slack 应用**：
   - 访问 [Slack API](https://api.slack.com/apps)
   - 创建应用并配置 Bot 权限
   - 安装应用到工作区
   - 保存 Bot Token 和 Signing Secret

2. **添加配置**：

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-your-bot-token",
      "signingSecret": "your-signing-secret",
      "dmPolicy": "pairing",
      "teamPolicy": "allowlist",
      "streaming": "partial"
    }
  },
  "plugins": {
    "entries": {
      "slack": {
        "enabled": true
      }
    }
  }
}
```

#### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **频道连接测试**：
   - Telegram: 向 Bot 发送 `/start` 命令
   - Discord: 在服务器中邀请 Bot 并发送消息
   - Slack: 在频道中提及 Bot

3. **日志检查**：
   ```bash
   journalctl -u openclaw -f
   ```

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Invalid bot token` | Token 格式错误或已失效 | 重新生成 Token 并更新配置 |
| `Bot not authorized` | Bot 权限不足 | 检查 Bot 在频道平台的权限配置 |
| `Connection timeout` | 网络连接问题 | 检查防火墙设置和网络连接 |
| `Webhook failed` | Webhook URL 配置错误 | 确认外部访问配置正确 |
| `plugins.entries.X: plugin disabled (disabled in config) but config is present` | 频道和插件配置不一致 | 同时检查并启用 `channels.X` 和 `plugins.entries.X.enabled` |

---

## 3. 修改 Agent 工具配置

### 一句话

通过 `tools` 部分配置全局工具策略，通过 `agents.list` 为特定 Agent 定制工具集。

### 核心要点

- `tools.profile` 有四个预设：`minimal` / `coding` / `messaging` / `full`
- `tools.web` 结构已在 2026.3.x 重构，使用 provider-specific 配置
- `tools.exec.host` 控制 exec 工具运行位置（`sandbox` / `gateway` / `node`）
- Agent 级工具配置可覆盖全局配置

### 详细内容

#### 前置条件检查

- [ ] 已了解工具配置的基本结构
- [ ] 已确定需要修改的工具配置项
- [ ] 已备份当前配置文件
- [ ] OpenClaw Gateway 已停止运行

#### 操作步骤

**步骤 1: 查看当前工具配置**

```bash
# 查看当前工具配置
openclaw gateway call tools.list --params '{}'

# 查看特定工具详情
openclaw gateway call tools.get --params '{"toolId":"tool-name"}'
```

**步骤 2: 修改全局工具配置**

修改 `tools` 部分。注意：`tools.exec` 不包含 `approvals` 和 `allowFrom`。

若需审批配置，请使用 `channels.<channel>.execApprovals`； 若需命令权限控制，请使用 `commands.allowFrom`。

```json
{
  "tools": {
    "profile": "coding",
    "elevated": {
      "enabled": true
    },
    "exec": {
      "host": "sandbox",
      "security": "allowlist",
      "ask": "on-miss",
      "safeBins": ["python", "node", "git", "ls", "cat", "grep"]
    },
    "web": {
      "search": {
        "enabled": true,
        "provider": "brave",
        "maxResults": 10,
        "timeoutSeconds": 30,
        "cacheTtlMinutes": 60,
        "brave": {
          "apiKey": "env:BRAVE_API_KEY",
          "baseUrl": "https://api.search.brave.com",
          "model": "brave-search"
        },
        "firecrawl": {
          "apiKey": "env:FIRECRAWL_API_KEY",
          "baseUrl": "https://api.firecrawl.dev"
        },
        "perplexity": {
          "apiKey": "env:PERPLEXITY_API_KEY",
          "baseUrl": "https://api.perplexity.ai",
          "model": "sonar"
        }
      },
      "fetch": {
        "enabled": true,
        "maxChars": 50000,
        "maxCharsCap": 100000,
        "maxResponseBytes": 1048576,
        "timeoutSeconds": 30
      },
      "x_search": {
        "enabled": true,
        "timeoutSeconds": 30,
        "cacheTtlMinutes": 60
      }
    },
    "media": {
      "enabled": true,
      "images": {
        "enabled": true
      }
    }
  }
}
```

> **注意**：`tools.exec` 的完整字段列表请参考 `openclaw-config-fields.md#toolsexec` 章节。
审批配置请使用 `channels.<channel>.execApprovals`，命令权限请使用 `commands.allowFrom`。**工具配置选项**：
- `profile`: 预设配置（`"minimal"` / `"coding"` / `"messaging"` / `"full"`）
- `elevated`: 提升权限模式
- `exec`: 命令执行配置（见 tools.exec 详细字段）
- `web`: Web 访问配置（search/fetch/x_search）
- `media`: 媒体处理配置

**步骤 3: 配置特定 Agent 的工具**

修改 `agents.list` 中特定 Agent 的工具配置：

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "profile": "full",
          "allow": ["bash", "edit", "read"],
          "deny": ["camera.snap", "screen.record"]
        }
      }
    ]
  }
}
```

**步骤 4: 启动并验证**

```bash
# 启动 Gateway
openclaw gateway

# 验证工具配置
openclaw gateway call agent.inspect --params '{"agentId":"main"}'
```

#### tools.web.search Provider 详解

| Provider | 主要字段 | 说明 |
|----------|---------|------|
| `brave` | apiKey, baseUrl, model, mode | Brave Search API |
| `firecrawl` | apiKey, baseUrl, model | Firecrawl 网页抓取 |
| `gemini` | apiKey, baseUrl, model | Google Gemini 搜索 |
| `grok` | apiKey, baseUrl, model, inlineCitations | x.ai Grok |
| `kimi` | apiKey, baseUrl, model | Moonshot Kimi |
| `perplexity` | apiKey, baseUrl, model | Perplexity Sonar |

每个 Provider 的 `apiKey` 也支持高级格式：`{ source: "env"|"file"|"exec", provider, id }`

#### tools.exec 关键字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `host` | string | 执行位置：`"sandbox"` / `"gateway"` / `"node"` |
| `security` | string | 安全模式：`"deny"` / `"allowlist"` / `"full"` |
| `safeBins` | array | 允许的可执行文件列表 |
| `safeBinTrustedDirs` | array | 可信的可执行文件目录 |
| `backgroundMs` | integer | 后台执行最大毫秒数 |
| `timeoutSec` | integer | 默认超时秒数 |
| `notifyOnExit` | boolean | 进程退出时通知 |
| `applyPatch` | object | 补丁应用配置 |

#### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **工具可用性测试**：
   ```bash
   openclaw gateway call tools.list --params '{}'
   ```

3. **实际功能测试**：
   使用 Agent 执行需要特定工具的任务

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Tool not found` | 工具 ID 不存在 | 检查工具名称拼写 |
| `Permission denied` | 权限配置错误 | 调整 `allow` / `deny` 列表 |
| `Profile not found` | 配置预设不存在 | 使用有效的 profile 名称 |
| `Tool execution failed` | 工具依赖未满足 | 安装必要的依赖或启用相关插件 |
| `web.search provider not found` | provider 名称错误 | 使用有效的 provider：`brave`, `firecrawl`, `gemini`, `grok`, `kimi`, `perplexity` |

---

## 4. 调整诊断和日志设置

### 一句话

通过 `diagnostics`、`logging`、`gateway.http`、`gateway.push` 细粒度控制可观测性。

### 核心要点

- `diagnostics` 控制 OpenTelemetry 和缓存追踪
- `logging` 控制日志级别、输出、敏感信息脱敏
- `gateway.http` 控制 HTTP 端点（chat completions、responses API）
- `gateway.push` 控制 APNS 推送通知中继

### 详细内容

#### 前置条件检查

- [ ] 已了解当前诊断配置
- [ ] 已确定需要调整的诊断级别
- [ ] 已确认日志存储空间充足
- [ ] OpenClaw Gateway 已停止运行

#### 操作步骤

**步骤 1: 配置基本诊断设置**

```json
{
  "diagnostics": {
    "enabled": true,
    "otel": {
      "enabled": true,
      "traces": true,
      "metrics": true,
      "logs": true
    },
    "cacheTrace": {
      "enabled": true,
      "includeMessages": true,
      "includePrompt": true,
      "includeSystem": true
    }
  }
}
```

**选项说明**：
- `enabled`: 启用/禁用诊断功能
- `otel`: OpenTelemetry 配置
  - `traces`: 追踪请求链路
  - `metrics`: 性能指标
  - `logs`: 日志收集
- `cacheTrace`: 缓存追踪配置
  - `includeMessages`: 包含消息内容
  - `includePrompt`: 包含提示内容
  - `includeSystem`: 包含系统信息

**步骤 2: 配置日志级别和输出**

```json
{
  "logging": {
    "level": "debug",
    "console": {
      "enabled": true,
      "level": "info"
    },
    "file": {
      "enabled": true,
      "path": "~/.openclaw/logs/openclaw.log",
      "level": "debug",
      "maxSize": "100mb",
      "maxFiles": 10
    },
    "redaction": {
      "enabled": true,
      "keys": ["api_key", "token", "password"]
    }
  }
}
```

**日志级别**：`trace` > `debug` > `info` > `warn` > `error` > `fatal`

**步骤 3: 配置 HTTP 端点（gateway.http）**

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": {
          "enabled": true
        },
        "responses": {
          "enabled": true,
          "maxBodyBytes": 10485760,
          "maxUrlParts": 10,
          "files": {
            "allowedMimes": ["image/*", "text/*"],
            "maxBytes": 52428800,
            "maxRedirects": 5,
            "timeoutMs": 30000
          },
          "images": {
            "maxImageParts": 10,
            "maxTotalImageBytes": 104857600
          }
        }
      },
      "securityHeaders": {
        "strictTransportSecurity": "max-age=31536000; includeSubDomains"
      }
    }
  }
}
```

**HTTP 端点选项**：
- `endpoints.chatCompletions.enabled`: 启用 `/v1/chat/completions` 端点
- `endpoints.responses.enabled`: 启用 Responses API 端点
- `endpoints.responses.maxBodyBytes`: 最大请求体大小
- `endpoints.responses.maxUrlParts`: 文件 URL 最大部分数
- `securityHeaders.strictTransportSecurity`: HSTS 头

**步骤 4: 配置推送通知（gateway.push）**

```json
{
  "gateway": {
    "push": {
      "apns": {
        "relay": {
          "baseUrl": "https://push.example.com",
          "timeoutMs": 5000
        }
      }
    }
  }
}
```

**步骤 5: 配置会话维护**

```json
{
  "session": {
    "maintenance": {
      "mode": "enforce",
      "pruneAfter": "30d",
      "maxEntries": 500,
      "rotateBytes": "10mb"
    }
  }
}
```

**步骤 6: 验证配置并启动**

```bash
# 验证配置
openclaw doctor

# 启动 Gateway
openclaw gateway

# 查看日志
tail -f ~/.openclaw/logs/openclaw.log
```

#### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **日志输出检查**：
   ```bash
   tail -f ~/.openclaw/logs/openclaw.log
   ```

3. **诊断数据查看**：
   ```bash
   openclaw gateway call diagnostics.status --params '{}'
   ```

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Log file not writable` | 日志目录权限不足 | 检查并修正日志目录权限 |
| `Disk space low` | 磁盘空间不足 | 清理旧日志文件或增加存储空间 |
| `Invalid log level` | 日志级别名称错误 | 使用有效的级别名称 |
| `Otel connection failed` | OpenTelemetry 服务不可用 | 检查 OTel 服务配置或禁用 |

---

## 5. 配置 ACP 运行时

### 一句话

ACP（Agent Communication Protocol）运行时配置，控制 Agent 间的消息分发、流式输出和会话管理。

### 核心要点

- `acp.enabled` 全局开关控制 ACP 功能
- `acp.dispatch` 控制消息分发
- `acp.stream` 控制流式输出的行为和模式
- `acp.defaultAgent` 指定处理 ACP 请求的默认 Agent

### 详细内容

#### 前置条件检查

- [ ] 已了解 ACP 协议基本概念
- [ ] 已确定需要配置的 ACP 功能范围
- [ ] OpenClaw Gateway 已停止运行

#### 操作步骤

**基础 ACP 配置**

```json
{
  "acp": {
    "enabled": true,
    "dispatch": {
      "enabled": true
    },
    "backend": "built-in",
    "defaultAgent": "main",
    "allowedAgents": ["main", "secondary"],
    "maxConcurrentSessions": 10
  }
}
```

**完整 ACP 配置（含 Stream 细粒度控制）**

```json
{
  "acp": {
    "enabled": true,
    "dispatch": {
      "enabled": true
    },
    "backend": "built-in",
    "defaultAgent": "main",
    "allowedAgents": ["main", "agent-2"],
    "maxConcurrentSessions": 10,
    "stream": {
      "coalesceIdleMs": 100,
      "maxChunkChars": 1000,
      "repeatSuppression": true,
      "deliveryMode": "live",
      "hiddenBoundarySeparator": "newline",
      "maxOutputChars": 100000,
      "maxSessionUpdateChars": 4000,
      "tagVisibility": {
        "prefixed": true
      }
    },
    "runtime": {
      "ttlMinutes": 60,
      "installCommand": "npm install -g @openclaw/acp-runtime"
    }
  }
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `enabled` | boolean | 全局启用 ACP |
| `dispatch.enabled` | boolean | 启用消息分发 |
| `backend` | string | ACP 后端类型（`built-in`） |
| `defaultAgent` | string | 默认处理 ACP 请求的 Agent ID |
| `allowedAgents` | array | 允许接收 ACP 消息的 Agent 列表 |
| `maxConcurrentSessions` | integer | 最大并发 ACP 会话数 |
| `stream.coalesceIdleMs` | integer | 空闲流块合并毫秒数 |
| `stream.maxChunkChars` | integer | 每个流块最大字符数 |
| `stream.repeatSuppression` | boolean | 启用重复内容抑制 |
| `stream.deliveryMode` | string | `live`（实时）或 `final_only`（仅最终） |
| `stream.hiddenBoundarySeparator` | string | 隐藏边界分隔符：`none` / `space` / `newline` / `paragraph` |
| `stream.maxOutputChars` | integer | 总输出最大字符数 |
| `stream.maxSessionUpdateChars` | integer | 会话更新最大字符数 |
| `runtime.ttlMinutes` | integer | ACP 运行时实例 TTL |
| `runtime.installCommand` | string | ACP 运行时安装命令 |

#### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **ACP 状态检查**：
   ```bash
   openclaw gateway call acp.status --params '{}'
   ```

3. **测试 ACP 消息**：
   向配置的 Agent 发送 ACP 协议消息验证响应

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `ACP not enabled` | ACP 未启用 | 设置 `acp.enabled: true` |
| `Agent not found` | 指定的 defaultAgent 不存在 | 确认 `agents.list` 中存在对应 ID |
| `Max concurrent sessions exceeded` | 并发会话数超限 | 增大 `maxConcurrentSessions` 或等待空闲会话 |
| `ACP runtime install failed` | 运行时安装失败 | 检查 `installCommand` 和网络连接 |

---

## 6. 配置 MCP 服务器

### 一句话

MCP（Model Context Protocol）服务器配置，让 Agent 可以调用外部 MCP 工具。

### 核心要点

- MCP 服务器通过 `command` + `args` 启动
- `env` 支持字符串、数字、布尔类型的环境变量
- `cwd` / `workingDirectory` 设置工作目录
- 服务器名称（`servers` 下的 key）用于在 Agent 工具中引用

### 详细内容

#### 前置条件检查

- [ ] 已了解 MCP 协议和可用 MCP 服务器
- [ ] 已确定需要集成的 MCP 服务器及其启动命令
- [ ] OpenClaw Gateway 已停止运行

#### 操作步骤

**基础 MCP 配置**

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/node/.openclaw/workspace"],
        "cwd": "/home/node/.openclaw/workspace"
      }
    }
  }
}
```

**多服务器配置示例**

```json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/node/.openclaw/workspace"],
        "env": {
          "DEBUG": false,
          "MAX_FILES": 100
        },
        "cwd": "/home/node/.openclaw/workspace",
        "workingDirectory": "/home/node/.openclaw/workspace"
      },
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {
          "GITHUB_PERSONAL_ACCESS_TOKEN": "env:GITHUB_TOKEN"
        }
      },
      "brave-search": {
        "command": "uvx",
        "args": ["mcp-server-brave-search", "--api-key", "env:BRAVE_API_KEY"],
        "env": {},
        "cwd": "/tmp"
      },
      "sequential-thinking": {
        "command": "uvx",
        "args": ["mcp-server-sequential-thinking"],
        "env": {
          "THOUGHT_TIMEOUT_MS": 30000
        },
        "cwd": "/home/node"
      }
    }
  }
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `servers.<name>.command` | string | 启动 MCP 服务器的可执行命令 |
| `servers.<name>.args` | array | 命令行参数数组 |
| `servers.<name>.env` | object | 环境变量 `{ key: value }`，值支持 string/number/boolean |
| `servers.<name>.cwd` | string | 服务器进程工作目录 |
| `servers.<name>.workingDirectory` | string | `cwd` 的别名 |

**常用 MCP 服务器启动命令参考**：

| 服务器 | 命令 | 参数示例 |
|--------|------|---------|
| filesystem | `npx` | `["-y", "@modelcontextprotocol/server-filesystem", "/path"]` |
| github | `npx` | `["-y", "@modelcontextprotocol/server-github"]` |
| brave-search | `uvx` | `["mcp-server-brave-search", "--api-key", "env:BRAVE_API_KEY"]` |
| sequential-thinking | `uvx` | `["mcp-server-sequential-thinking"]` |

#### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **MCP 服务器状态**：
   ```bash
   openclaw gateway call mcp.list --params '{}'
   ```

3. **测试 MCP 工具调用**：
   通过 Agent 执行 MCP 工具验证功能

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `MCP server command not found` | 可执行命令不存在 | 确认 command 路径正确或已安装 |
| `MCP server startup failed` | 服务器启动失败 | 检查 args、env、工作目录是否正确 |
| `Invalid env type` | env 值类型不支持 | 仅使用 string/number/boolean |
| `Server timeout` | MCP 服务器响应超时 | 检查网络或增加超时配置 |

---

## 7. 配置审批策略

### 一句话

通过 `approvals` 控制 exec 和 plugin 工具的审批流程，支持基于 Agent、会话、目标渠道的细粒度规则。

### 核心要点

- `approvals.exec` 和 `approvals.plugin` 分别控制两类工具的审批
- `mode` 可选 `session` / `targets` / `both`
- `targets` 支持按 `channel` / `accountId` / `threadId` 精确匹配
- `agentFilter` 和 `sessionFilter` 用于进一步缩小审批范围

### 详细内容

#### 前置条件检查

- [ ] 已了解审批策略的使用场景
- [ ] 已确定需要审批的工具类型和触发条件
- [ ] OpenClaw Gateway 已停止运行

#### 操作步骤

**基础审批配置**

```json
{
  "approvals": {
    "exec": {
      "enabled": true,
      "mode": "session"
    },
    "plugin": {
      "enabled": true,
      "mode": "session"
    }
  }
}
```

**基于目标的审批配置（targets）**

```json
{
  "approvals": {
    "exec": {
      "enabled": true,
      "mode": "targets",
      "agentFilter": ["main", "admin"],
      "sessionFilter": ["telegram:*", "discord:guild:*"],
      "targets": [
        {
          "channel": "telegram",
          "accountId": "123456789",
          "threadId": null
        },
        {
          "channel": "discord",
          "accountId": null,
          "threadId": "987654321"
        }
      ]
    },
    "plugin": {
      "enabled": true,
      "mode": "targets",
      "agentFilter": ["main"],
      "targets": [
        {
          "channel": "telegram",
          "accountId": "123456789"
        }
      ]
    }
  }
}
```

**审批模式详解**：

| 模式 | 说明 |
|------|------|
| `session` | 每个新会话首次执行时触发审批 |
| `targets` | 仅对匹配 `targets` 规则的操作触发审批 |
| `both` | 同时满足 session 规则和 target 规则时触发 |

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `exec.enabled` | boolean | 启用 exec 审批 |
| `exec.mode` | string | 审批触发模式 |
| `exec.agentFilter` | array | 仅对这些 Agent 触发审批（空=所有） |
| `exec.sessionFilter` | array | 仅对这些会话模式触发审批（支持通配符） |
| `exec.targets` | array | 目标规则数组 |
| `plugin.*` | — | plugin 执行审批，同 exec 结构 |

**target 规则字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `channel` | string | 渠道名称（如 `telegram`、`discord`） |
| `accountId` | string/null | 账户 ID（null 表示任意） |
| `threadId` | string/null | 线程/群组 ID（null 表示任意） |
| `to` | string/null | 消息目标（可选） |

#### 验证方法

1. **配置验证**：
   ```bash
   openclaw doctor
   ```

2. **审批状态检查**：
   ```bash
   openclaw gateway call approvals.status --params '{}'
   ```

3. **测试审批流程**：
   执行需要审批的操作，观察是否正确触发审批提示

#### 常见错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Approval timeout` | 审批请求超时 | 增加审批超时配置或确认审批通道畅通 |
| `No matching target` | 没有匹配的目标规则 | 检查 `targets` 配置或使用 `mode: "session"` |
| `Agent not in filter` | Agent 不在审批白名单 | 将 Agent ID 添加到 `agentFilter` |
| `Session blocked` | 会话被过滤规则阻止 | 检查 `sessionFilter` 配置 |

---

## 🔧 通用故障排除

### 配置重载失败

**症状**：修改配置后无法生效

**解决步骤**：

1. **验证 JSON 语法**：
   ```bash
   jq < ~/.openclaw/openclaw.json
   ```

2. **检查配置有效性**：
   ```bash
   openclaw doctor
   ```

3. **完全重启 Gateway**：
   ```bash
   openclaw gateway stop
   openclaw gateway
   ```

### 版本兼容性问题

**症状**：配置字段在当前版本中不支持

**解决步骤**：

1. **检查 OpenClaw 版本**：
   ```bash
   openclaw --version
   ```

2. **获取当前版本的 Schema**：
   ```bash
   openclaw gateway call config.schema --params '{}' > schema.json
   ```

3. **对比配置与 Schema**：
   ```bash
   grep -r "fieldName" schema.json
   ```

### 权限问题

**症状**：配置文件无法读写

**解决步骤**：

1. **检查文件权限**：
   ```bash
   ls -la ~/.openclaw/openclaw.json
   ```

2. **修正权限**：
   ```bash
   chmod 600 ~/.openclaw/openclaw.json
   ```

3. **检查文件所有者**：
   ```bash
   chown $USER:$USER ~/.openclaw/openclaw.json
   ```

---

## 📚 相关资源

- **配置字段索引**：`openclaw-config-fields.md`
- **Schema 源码指南**：`schema-sources.md`
- **OpenClaw 官方文档**：https://github.com/openclaw/openclaw
- **配置示例仓库**：https://github.com/openclaw/config-examples

---

## ⚠️ 重要提示

1. **备份配置**：在进行任何复杂配置修改前，务必备份当前配置文件
2. **渐进式修改**：一次只修改一个部分，便于定位问题
3. **验证优先**：每次修改后都运行 `openclaw doctor` 验证配置
4. **日志监控**：修改后密切关注日志输出，及时发现潜在问题
5. **版本匹配**：确保配置与当前 OpenClaw 版本兼容（本文档基于 2026.3.28）

---

**文档版本**：1.1.0
**最后更新**：2026-03-31
**参考配置版本**：OpenClaw 2026.3.28
