---
name: openclaw-config-master
description: Edit and validate OpenClaw Gateway config (openclaw.json / JSON5). Covers all config areas — gateway, agents, channels, models, auth, tools, commands, session, hooks, secrets, acp, messages, plugins, skills, $include. Use when adding/changing config keys or diagnosing openclaw doctor/config validation errors, to avoid schema mismatches that prevent the Gateway from starting or weaken security policies.
---

# OpenClaw Config

## 一句话

用 schema-first 工作流安全编辑 OpenClaw 配置文件，验证先行，避免无效 key 导致 Gateway 无法启动或安全策略被破坏。

---

## 核心要点（5条）

1. **Schema 先行** — 不猜 key，用 `gateway config.schema.lookup path="目标路径"` 获取权威 schema
2. **在线修改** — 优先用 `gateway config.patch` 在线修改（自动验证+重启），备选 `openclaw config set` CLI
3. **验证不可跳** — `config.patch` 自动验证；手动编辑后必须跑 `openclaw doctor`
4. **严格模式** — 大多数对象是 `.strict()`，未知 key 会导致 Gateway 拒绝启动
5. **不轻易用 --fix** — `openclaw doctor --fix/--yes` 会写文件，需用户明确同意
6. **受保护路径** — 部分敏感路径（如 `tools.exec.ask`）`config.patch` 无法修改，会返回 `cannot change protected config paths` 错误。遇此情况需直接编辑 `openclaw.json` 后 `openclaw gateway restart`

---

## 配置覆盖范围（全部顶层 key）

| 顶层 key | 子模块 | 说明 |
|---------|--------|------|
| `gateway` | port, mode, bind, auth, tailscale, nodes, controlUi | 网关核心：端口、模式、认证、Tailscale、节点策略 |
| `agents` | defaults, list | Agent 配置：默认模型/工具/工作区 + agent 列表 |
| `channels` | telegram, feishu, discord, slack, whatsapp, signal, imessage, ... | 渠道配置：每个渠道的连接、策略、审批 |
| `models` | providers, mode, bedrockDiscovery | 模型目录：提供者定义、合并模式、Bedrock 发现 |
| `auth` | profiles | 认证配置：API Key / OAuth 认证档案 |
| `tools` | exec, web, fs, media, links, sessions, loopDetection, message, agentToAgent, elevated, subagents, sandbox, sessions_spawn, profile, allow, alsoAllow, deny, byProvider | 工具策略：执行、网络、文件系统、媒体、沙箱、子代理 |
| `commands` | bash, config, mcp, plugins, debug, restart, text, native, nativeSkills, allowFrom, ownerDisplay, ... | 命令控制：聊天命令开关、权限、提权规则 |
| `session` | scope, dmScope, reset, resetByType, resetByChannel, store, typingMode, identityLinks, threadBindings, maintenance, sendPolicy, agentToAgent, ... | 会话管理：路由、重置策略、存储、线程绑定、维护 |
| `hooks` | internal, external | 钩子：内部钩子（session-memory）+ 外部钩子 |
| `secrets` | providers | 密钥管理：文件/环境变量等密钥提供者 |
| `acp` | enabled, backend, defaultAgent, allowedAgents | ACP 后端：Agent 托管运行时配置 |
| `messages` | ackReactionScope | 消息行为：确认反应范围等 |
| `plugins` | enabled, allow, deny, load, slots, entries, installs | 插件系统：启用/禁用、加载路径、安装记录 |
| `skills` | (skills 配置) | 技能配置 |
| `meta` | lastTouchedVersion, lastTouchAt | 系统元数据（自动管理） |
| `wizard` | lastRunAt, lastRunVersion, lastRunCommand, lastRunMode | 向导元数据（自动管理） |
| `$include` | — | 模块化配置：分割到多个 JSON5 文件 |

---

## 工作流程

> **重要**：在提供任何配置指导之前，必须按以下步骤执行前置检查。

### 第一步：查官方文档（必做）

**每次修改配置前，必须先查阅官方最新文档确认字段和用法。** 技能内的文档可能滞后于官方更新。

#### 在线文档（权威来源）

| 文档 | 链接 | 用途 |
|------|------|------|
| **配置指南** | https://docs.openclaw.ai/gateway/configuration | 所有配置项的完整说明 |
| **配置参考** | https://docs.openclaw.ai/gateway/configuration-reference | 字段类型、默认值、示例 |
| **Config CLI** | https://docs.openclaw.ai/cli/config | `config set/get/unset` 用法 |
| **Update CLI** | https://docs.openclaw.ai/cli/update | 版本更新命令 |
| **Channels CLI** | https://docs.openclaw.ai/cli/channels | 渠道管理命令 |
| **Skills CLI** | https://docs.openclaw.ai/cli/skills | 技能管理命令 |
| **Security CLI** | https://docs.openclaw.ai/cli/security | 安全审计命令 |
| **Models** | https://docs.openclaw.ai/gateway/models | 模型提供者配置 |
| **Agents** | https://docs.openclaw.ai/gateway/agents | Agent 配置 |
| **Tools** | https://docs.openclaw.ai/gateway/tools | 工具配置 |
| **Plugins** | https://docs.openclaw.ai/gateway/plugins | 插件配置 |
| **Cron** | https://docs.openclaw.ai/gateway/cron | 定时任务配置 |
| **Session** | https://docs.openclaw.ai/gateway/session | 会话配置 |

#### 内置文档搜索

```bash
# 搜索特定主题的官方文档
openclaw docs "configuration"
openclaw docs "telegram"
openclaw docs "exec approvals"
openclaw docs "models"
openclaw docs "session"
```

#### 在线 Schema 查询

```
# 通过 gateway 工具查询（推荐）
gateway config.schema.lookup path="目标路径"

# CLI 方式
openclaw config schema
```

#### 何时查什么

| 场景 | 查什么 |
|------|--------|
| 添加/修改模型 | 配置参考 + models 文档 + schema lookup |
| 配置渠道 | 配置参考 + Channels CLI + schema lookup |
| 修改安全策略 | 配置指南 + Security CLI + schema lookup |
| 会话/重置策略 | 配置参考 + session 文档 + schema lookup |
| 工具权限控制 | 配置参考 + tools 文档 + schema lookup |
| 版本升级后配置不兼容 | 配置参考 + Update CLI + `references/version-migration.md` |
| 不确定字段名/类型 | **先查 schema lookup**，再查配置参考 |

### 第二步：版本检查

```bash
# 检查本地版本
openclaw --version

# 检查最新版本
openclaw update status --json
```

**如果本地版本不是最新**：提醒用户先更新：`openclaw update`

### 第三步：执行修改

---

## 两种修改模式

### 模式 A：在线修改（推荐）

通过 `gateway` 工具直接修改，自动验证+重启：

```
# 1. 查询当前值
gateway config.get path="commands.bash"

# 2. 查询 schema 确认字段合法性
gateway config.schema.lookup path="commands"

# 3. 应用修改（用户确认后）
gateway config.patch raw='{"commands":{"bash":true}}' note="启用 bash 命令"
```

- `config.patch`：部分更新，与现有配置合并，适合修改少量字段
- `config.apply`：全量替换，适合大规模重构
- 两者都会自动验证 schema + 写入 + 重启 Gateway
- `note` 参数必填，用于重启后通知用户

### 模式 B：CLI 命令（备选）

无法使用 gateway 工具时，生成命令供用户执行：

```bash
# 设置值
openclaw config set <path> <value> --json

# 验证
openclaw config validate

# 重启
openclaw gateway restart
```

---

## 在线修改配置的标准流程

修改任何配置前，按此流程操作：

1. **查 schema** — `gateway config.schema.lookup path="目标路径"`，确认字段名和类型
2. **读当前值** — `gateway config.get path="目标路径"`，了解现状
3. **向用户说明** — 描述要改什么、为什么改、预期影响
4. **执行修改** — 用户确认后，`gateway config.patch raw='{...}' note="变更说明"`
5. **验证结果** — 重启后自动通知，检查新配置是否生效

**注意**：`config.patch` 会自动写入、验证 schema、重启 Gateway。不需要手动 `openclaw doctor`。

---

## 详细配置参考

### gateway — 网关核心

```json
"gateway": {
  "port": 18789,           // 监听端口
  "mode": "local",         // 运行模式：local
  "bind": "loopback",      // 绑定：loopback | 0.0.0.0
  "auth": {
    "mode": "token",       // 认证模式
    "token": "..."         // 认证 token
  },
  "tailscale": {
    "mode": "off",         // Tailscale 模式
    "resetOnExit": false
  },
  "controlUi": {
    "allowInsecureAuth": false
  },
  "nodes": {
    "denyCommands": [...]  // 节点禁止命令列表
  }
}
```

### agents — Agent 配置

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "provider/model-id",     // 默认模型
      "fallbacks": ["provider/fallback1"] // 回退模型列表
    },
    "models": {                           // 可用模型注册 + 别名
      "provider/model": { "alias": "别名" }
    },
    "workspace": "~/.openclaw/workspace", // 工作目录
    "contextPruning": { "mode": "cache-ttl", "ttl": "1h" },
    "compaction": { "mode": "safeguard" },
    "heartbeat": { "every": "30m" },
    "maxConcurrent": 2,
    "subagents": { "maxConcurrent": 2 }
  },
  "list": [
    {
      "id": "main",
      "tools": { "alsoAllow": [...] },
      "runtime": { "type": "acp", "acp": {...} }
    }
  ]
}
```

### channels — 渠道配置

每个渠道（telegram/feishu/discord/slack/whatsapp/signal/imessage）有独立配置：

```json
"channels": {
  "telegram": {
    "enabled": true,
    "botToken": "...",
    "dmPolicy": "allowlist|open",
    "groupPolicy": "allowlist|open",
    "allowFrom": ["user_id"],
    "streaming": "partial|full|off",
    "execApprovals": {
      "enabled": true,
      "approvers": ["user_id"],
      "target": "dm"
    },
    "groups": { "*": { "requireMention": true } }
  }
}
```

详细字段见 `references/channels-config.md`

### models — 模型目录

```json
"models": {
  "mode": "merge|replace",     // merge=保留内置+叠加自定义, replace=仅用自定义
  "providers": {
    "provider-id": {
      "baseUrl": "https://...",
      "apiKey": "...|secret-ref",
      "api": "openai-completions|anthropic-messages",
      "models": [
        {
          "id": "model-id",
          "name": "显示名",
          "reasoning": true,
          "input": ["text", "image"],
          "contextWindow": 200000,
          "maxTokens": 8192,
          "cost": { "input": 0, "output": 0 }
        }
      ]
    }
  },
  "bedrockDiscovery": { ... }   // AWS Bedrock 自动发现
}
```

### auth — 认证档案

```json
"auth": {
  "profiles": {
    "provider:default": {
      "provider": "provider-name",
      "mode": "api_key|oauth"
    }
  }
}
```

### tools — 工具策略

```json
"tools": {
  "profile": "...",           // 工具策略预设名
  "allow": [...],             // 绝对白名单（替换 profile 默认）
  "alsoAllow": [...],         // 白名单补充（叠加 profile）
  "deny": [...],              // 黑名单（优先级最高）
  "byProvider": { ... },      // 按渠道的工具策略覆盖
  "exec": {
    "security": "allowlist|full",
    "ask": "on-miss",
    "host": "sandbox",
    "safeBins": ["python", "node", "git"],
    "safeBinTrustedDirs": [...],
    "safeBinProfiles": [...],
    "timeoutSec": 120,
    "backgroundMs": 10000,
    "applyPatch": true
  },
  "web": {                    // 搜索/抓取工具策略
    "search": { "enabled": true, "provider": "brave" }
  },
  "fs": { ... },              // 文件系统工具
  "media": { ... },           // 媒体工具
  "links": { ... },           // 链接工具
  "sessions": { ... },        // 会话工具
  "loopDetection": { ... },   // 循环检测
  "message": { ... },         // 消息工具策略
  "agentToAgent": { ... },    // Agent 间工具调用
  "elevated": { ... },        // 提权工具访问
  "subagents": { ... },       // 子代理工具策略
  "sandbox": { ... },         // 沙箱策略
  "sessions_spawn": { ... }   // spawn 会话策略
}
```

### commands — 命令控制

```json
"commands": {
  "native": "auto",            // 原生命令注册（Discord/Slack/Telegram 菜单）
  "nativeSkills": "auto",      // 技能原生命令注册
  "text": true,                // 文本命令解析
  "bash": true,                // ! 和 /bash 命令（布尔值）
  "config": false,             // /config 命令读写配置
  "mcp": false,                // /mcp 命令管理 MCP 服务器
  "plugins": false,            // /plugins 命令管理插件
  "debug": false,              // /debug 运行时调试覆盖
  "restart": true,             // /restart 和 gateway 重启工具
  "useAccessGroups": false,    // 启用访问组策略
  "ownerAllowFrom": [...],     // 显式 owner 白名单
  "ownerDisplay": "raw|hash",  // owner ID 显示方式
  "ownerDisplaySecret": "...", // hash 模式的 HMAC 密钥
  "allowFrom": {               // 提权命令的 channel→用户映射
    "telegram": ["YOUR_TELEGRAM_USER_ID"]
  }
}
```

**关键注意**：
- 所有布尔字段必须用 `true`/`false`，不能是字符串 `"true"`
- `allowFrom` 在 `commands` 下，不在 `tools.exec` 下
- 敏感命令（bash/config/mcp/plugins/debug）默认 false，需显式开启

### session — 会话管理

```json
"session": {
  "scope": "per-sender|global",          // 会话分组策略
  "dmScope": "main|per-peer|per-channel-peer|per-account-channel-peer",
  "dmScopePolicy": "...",                // DM 作用域策略
  "identityLinks": { ... },              // 身份映射（跨渠道同一用户）
  "resetTriggers": [...],                // 会话重置触发词
  "idleMinutes": 0,                      // 空闲重置分钟数（旧版兼容）
  "reset": { ... },                      // 默认重置策略
  "resetByType": {                       // 按聊天类型覆盖
    "direct": { ... },
    "group": { ... },
    "thread": { ... }
  },
  "resetByChannel": { ... },             // 按渠道覆盖
  "store": "path/to/store.db",           // 会话存储路径
  "typingMode": "never|instant|thinking|message",
  "typingIntervalSeconds": 5,
  "parentForkMaxTokens": 0,              // 父会话 fork 上限
  "mainKey": "...",                      // 主会话 key 覆盖
  "sendPolicy": {                        // 跨会话发送权限
    "allow": [...], "deny": [...]
  },
  "agentToAgent": { ... },               // Agent 间会话交换
  "threadBindings": { ... },             // 线程绑定路由
  "maintenance": {                       // 自动维护
    "maxAge": "...", "maxEntries": 1000, "rotateOnStartup": false
  }
}
```

### hooks — 钩子

```json
"hooks": {
  "internal": {
    "enabled": true,
    "entries": {
      "session-memory": { "enabled": true }  // 会话记忆钩子
    }
  },
  "external": { ... }                       // 外部 webhook 钩子
}
```

### secrets — 密钥管理

```json
"secrets": {
  "providers": {
    "lark-secrets": {
      "source": "file",
      "path": "~/.openclaw/credentials/lark.secrets.json"
    }
  }
}
```

### acp — ACP 后端

```json
"acp": {
  "enabled": false,
  "backend": "acpx",
  "defaultAgent": "claude",
  "allowedAgents": ["claude"]
}
```

### messages — 消息行为

```json
"messages": {
  "ackReactionScope": "group-mentions"  // 确认反应范围
}
```

### plugins — 插件系统

```json
"plugins": {
  "enabled": true,
  "allow": ["minimax", "telegram", "feishu"],  // 插件白名单
  "deny": [...],                                // 插件黑名单
  "load": { "paths": [...] },                   // 加载路径
  "slots": { "memory": "..." },                 // 独占槽位
  "entries": {                                  // 插件配置
    "plugin-id": { "enabled": true, "config": {...} }
  },
  "installs": { ... }                           // 安装记录（CLI 管理）
}
```

---

## 版本适配说明（2026.4.x 关键变更）

> **重要**：以下内容记录了从旧版配置格式到当前版本的关键差异。

### 1. `tools.exec` — 不支持 `approvals` 和 `allowFrom`

**错误写法**（会导致 Gateway 崩溃）：
```json
"tools": { "exec": { "approvals": { "enabled": true }, "allowFrom": {...} } }
```

**正确写法**：
```json
"tools": { "exec": { "security": "allowlist", "ask": "on-miss" } }
```

`tools.exec` 支持的字段：`host`, `node`, `security`, `ask`, `pathPrepend`, `safeBins`, `safeBinTrustedDirs`, `safeBinProfiles`, `strictInlineEval`, `backgroundMs`, `timeoutSec`, `cleanupMs`, `notifyOnExit`, `notifyOnExitEmptySuccess`, `applyPatch`。

### 2. exec 审批 → `channels.<channel>.execApprovals`

```json
"channels": {
  "telegram": {
    "execApprovals": { "enabled": true, "approvers": ["YOUR_TELEGRAM_USER_ID"], "target": "dm" }
  }
}
```

### 3. 新旧格式对照速查表

| 功能 | 旧版（错误）位置 | 正确位置 |
|------|-----------------|---------|
| exec 审批 | `tools.exec.approvals` | `channels.telegram.execApprovals` |
| 命令权限白名单 | `tools.exec.allowFrom` | `commands.allowFrom` |
| bash 命令开关 | `commands.bash = "true"` | `commands.bash = true`（布尔值） |
| exec 安全策略 | `tools.exec.security` | `tools.exec.security`（不变） |

---

## $include（模块化配置）

`$include` 在 schema 验证前解析，支持将配置分割到多个 JSON5 文件：

- 支持 `"$include": "./base.json5"` 或数组
- 相对路径相对于当前配置文件目录
- 深度合并规则：对象递归合并，数组拼接，原始值后者覆盖前者
- 限制：最大深度 10；循环 include 被检测并拒绝

---

## Guardrails（避免 Schema 错误）

- **大多数对象是 strict** (`.strict()`)：未知 key 导致 Gateway 拒绝启动
- `channels` 是 `.passthrough()`：扩展 channels 可添加自定义 key
- `env` 是 `.catchall(z.string())`：可直接放字符串环境变量
- **密钥处理**：优先用 `secrets.providers` 或环境变量，避免将 token/API key 写入 `openclaw.json`

---

## 常用配方

**开启 /config 命令**
```
gateway config.patch raw='{"commands":{"config":true}}' note="开启 /config 命令"
```

**配置 exec 安全策略**
```
gateway config.patch raw='{"tools":{"exec":{"security":"allowlist","ask":"on-miss"}}}' note="配置 exec 安全策略"
```

**配置 Telegram（安全模式：仅自己私聊，禁止群聊）**
```
gateway config.patch raw='{"channels":{"telegram":{"enabled":true,"botToken":"YOUR_TELEGRAM_BOT_TOKEN","dmPolicy":"allowlist","allowFrom":["YOUR_TELEGRAM_USER_ID"],"groupPolicy":"disabled"}},"plugins":{"entries":{"telegram":{"enabled":true}}}}' note="配置 Telegram 安全模式"
```

**配置飞书（安全模式：仅自己私聊，群聊开放需 @）**
```
gateway config.patch raw='{"channels":{"feishu":{"enabled":true,"appId":"YOUR_FEISHU_APP_ID","appSecret":"YOUR_FEISHU_APP_SECRET","dmPolicy":"allowlist","allowFrom":["YOUR_FEISHU_USER_ID"],"groupPolicy":"open","groupAllowFrom":["*"],"requireMention":true,"connectionMode":"websocket"}},"plugins":{"allow":["openclaw-lark","minimax"],"entries":{"openclaw-lark":{"enabled":true},"minimax":{"enabled":true}}}}' note="配置飞书安全模式"
```

**获取用户 ID（日志法）**
```bash
# 飞书
tail -500 /tmp/openclaw/openclaw-*.log | grep "message from"
# Telegram
tail -500 /tmp/openclaw/openclaw-*.log | grep "telegram.*message"
```

**验证渠道连接**
```bash
openclaw channels status
openclaw doctor
```

**配置 Telegram exec 审批**
```
gateway config.patch raw='{"channels":{"telegram":{"execApprovals":{"enabled":true,"approvers":["YOUR_TELEGRAM_USER_ID"],"target":"dm"}}}}' note="启用 Telegram exec 审批"
```

**配置命令权限**
```
gateway config.patch raw='{"commands":{"bash":true,"allowFrom":{"telegram":["YOUR_TELEGRAM_USER_ID"]}}}' note="启用 bash 命令并配置权限"
```

**修改会话空闲重置**
```
gateway config.patch raw='{"session":{"idleMinutes":60}}' note="设置会话 60 分钟空闲后重置"
```

**配置会话维护**
```
gateway config.patch raw='{"session":{"maintenance":{"maxEntries":500}}}' note="限制会话存储最多 500 条"
```

**添加模型提供者**
```
gateway config.patch raw='{"models":{"providers":{"new-provider":{"baseUrl":"https://...","api":"openai-completions","models":[...]}}}}' note="添加新模型提供者"
```

**启用插件**
```
gateway config.patch raw='{"plugins":{"allow":["new-plugin"],"entries":{"new-plugin":{"enabled":true}}}}' note="启用新插件"
```

**配置 hooks**
```
gateway config.patch raw='{"hooks":{"internal":{"enabled":true,"entries":{"session-memory":{"enabled":true}}}}}' note="启用 session-memory 钩子"
```

---

## 常见配置错误和修复

| 错误现象 | 常见原因 | 修复方法 |
|---------|---------|---------|
| Gateway 启动崩溃 | `tools.exec` 中有未知字段（如 `approvals`） | 移除不支持的字段 |
| Schema 验证失败 | `commands.bash` 设为字符串 `"true"` | 改为布尔值 `true` |
| exec 审批不生效 | 在 `tools.exec` 中配置审批 | 移至 `channels.telegram.execApprovals` |
| 命令权限不生效 | 在 `tools.exec.allowFrom` 配置白名单 | 移至 `commands.allowFrom` |
| 会话不重置 | `session.reset` 配置不当 | 检查 `resetByType`/`resetByChannel` 是否覆盖 |

---

## 复杂配置操作流程

复杂配置变更（添加新模型提供者、配置新频道等）遵循增强流程：

1. **前置检查** — 确认凭证/参数、验证平台可用性、备份配置
2. **详细配置** — 参考 `references/complex-operations.md`，遵循渐进式修改原则
3. **验证测试** — 逐步测试 + 准备回滚
4. **文档记录** — 记录变更、更新文档

---

## 版本升级流程

1. **升级前准备** — 参阅 `references/version-migration.md`、创建备份、检查兼容性
2. **执行迁移** — 更新字段、处理废弃字段
3. **验证回滚** — 运行测试、准备快速回滚

---

## 快速链接

**Channel 配置** → `references/channels-config.md`
**Telegram + 飞书配置模板** → `references/complex-operations.md`（含安全模式/开放模式模板、AppSecret 安全存储、常见错误）
**复杂配置操作** → `references/complex-operations.md`
**常见错误修复** → `references/common-errors.md`
**版本迁移** → `references/version-migration.md`
**字段索引** → `references/openclaw-config-fields.md`
**Schema 源码** → `references/schema-sources.md`

**工具脚本**
- `scripts/openclaw-config-check.sh` — 配置验证
- `scripts/backup-config.sh` — 配置备份
- `scripts/restore-config.sh` — 配置恢复
- `scripts/validate-config.sh` — 配置验证
- `scripts/validate-migration.sh` — 迁移验证

**官方文档** → 详见上方「第一步：查官方文档」的完整链接表

**故障诊断**
- `openclaw doctor` — 快速诊断
- `~/.openclaw/logs/openclaw.log` — 日志分析
