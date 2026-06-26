---
name: openclaw-overview
description: OpenClaw 全局概览 — 帮助 Agent 快速理解架构、核心概念、工具体系、配置结构、目录布局和常用操作。当 Agent 需要了解 OpenClaw 是什么、怎么工作、有哪些能力时使用。
user-invocable: true
version: 1.0.0
---

# OpenClaw 全局概览

> 你的第二个大脑——只不过这个真的记得东西放哪儿了。

OpenClaw 是一个**本地优先的 AI Agent 运行时**。它通过一个长期运行的 Gateway 进程，把大模型、消息渠道、工具执行、会话管理和自动化调度串在一起，让 Agent 能在你选择的任何平台上（Telegram、WhatsApp、Discord、Signal、WebChat……）持续工作。

---

## 一、架构总览

```
┌─────────────────────────────────────────────────┐
│                  Gateway (守护进程)                │
│                                                   │
│  ┌──────────┐  ┌──────────┐  ┌───────────────┐   │
│  │ 消息渠道  │  │ Agent 运行 │  │  工具执行层   │   │
│  │ 连接管理  │  │ 时 (会话)  │  │ exec/browser  │   │
│  │ WhatsApp  │  │           │  │ canvas/nodes  │   │
│  │ Telegram  │  │ 模型调用   │  │ cron/memory   │   │
│  │ Discord   │  │ 上下文管理  │  │ message/web   │   │
│  │ Signal    │  │ 压缩/截断  │  │               │   │
│  │ WebChat   │  │           │  │               │   │
│  └──────────┘  └──────────┘  └───────────────┘   │
│                                                   │
│  WebSocket API (ws://host:18789)                  │
└──────────┬──────────────────────┬─────────────────┘
           │                      │
    ┌──────▼──────┐       ┌──────▼──────┐
    │  客户端      │       │  节点设备    │
    │ macOS App   │       │ iOS/Android │
    │ CLI         │       │ headless    │
    │ Web UI      │       │ (配对后连接) │
    └─────────────┘       └─────────────┘
```

**核心原则：Gateway 是唯一的真相来源。** 所有会话状态、token 计数、消息路由都由 Gateway 掌控。客户端只做展示。

---

## 二、核心概念

### Agent（智能体）

一个 Agent 拥有独立的：
- **工作区**（`~/.openclaw/workspace`）— 文件、AGENTS.md、SOUL.md、USER.md
- **状态目录**（`~/.openclaw/agents/<agentId>/agent`）— 认证、模型注册
- **会话存储**（`~/.openclaw/agents/<agentId>/sessions/`）— 聊天历史

默认是单 Agent 模式（`agentId = main`）。支持多 Agent 隔离路由。

### Session（会话）

- 私聊合并到主会话 `agent:main:main`
- 群聊/频道独立隔离
- 存储为 JSONL 文件：`~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
- `session.dmScope` 控制私聊隔离策略：`main` / `per-peer` / `per-channel-peer`

### Model（模型）

选择优先级：
1. `agents.defaults.model.primary` — 主模型
2. `agents.defaults.model.fallbacks` — 降级链
3. Provider 内认证故障转移

支持多 Provider 配置：OpenAI、Anthropic、小米 MiMo、Ollama、OpenRouter 等。

### Compaction（上下文压缩）

当会话接近模型 context window 上限时，自动触发压缩：
- **模式**：`safeguard`（默认，保守压缩）/ `auto` / `off`
- **原理**：摘要旧消息，保留近期消息
- 可配置专用压缩模型：`agents.defaults.compaction.model`

### Skills（技能）

Agent 的能力扩展机制。三个加载位置（优先级从高到低）：
1. `<workspace>/skills/` — 工作区专属
2. `~/.openclaw/skills/` — 全局共享
3. 内置技能（随安装包分发）

每个 Skill 是一个包含 `SKILL.md` 的目录。通过 YAML frontmatter 声明元数据。

### Nodes（节点设备）

iOS/Android/树莓派等设备配对后连接到 Gateway，提供：
- 相机拍照/录像
- 屏幕录制
- 位置获取
- 语音唤醒
- 通知读取

---

## 三、工具体系

OpenClaw 为 Agent 提供**一等公民工具**（非 shell 调用）：

| 工具 | 用途 |
|------|------|
| `read` / `write` / `edit` | 文件读写编辑 |
| `exec` / `process` | Shell 命令执行与进程管理 |
| `browser` | 浏览器自动化（Playwright） |
| `canvas` | Canvas 画布（A2UI） |
| `nodes` | 节点设备控制 |
| `cron` | 定时任务管理 |
| `message` | 消息发送与渠道操作 |
| `gateway` | Gateway 配置与重启 |
| `sessions_*` | 会话管理（列表/历史/发送/生成） |
| `memory_search` / `memory_get` | 语义记忆检索 |
| `web_fetch` / `mimo_web_search` | 网页抓取与搜索 |
| `subagents` | 子 Agent 编排 |

**工具策略**：通过 `tools.profile`（`minimal` / `coding` / `messaging` / `full`）和 `tools.allow` / `tools.deny` 控制可用范围。

---

## 四、目录布局

```
~/.openclaw/
├── openclaw.json              # 主配置文件
├── agents/
│   └── main/
│       ├── agent/
│       │   └── auth-profiles.json   # 认证配置
│       └── sessions/
│           ├── sessions.json        # 会话索引
│           └── *.jsonl              # 会话记录
├── skills/                    # 全局 Skill
├── cron/
│   └── jobs.json              # 定时任务
├── memory/                    # 记忆存储
├── workspace/                 # Agent 工作区
│   ├── AGENTS.md              # 操作指令
│   ├── SOUL.md                # 人格与边界
│   ├── USER.md                # 用户档案
│   ├── TOOLS.md               # 工具备注
│   ├── IDENTITY.md            # Agent 身份
│   ├── HEARTBEAT.md           # 心跳任务
│   └── BOOTSTRAP.md           # 首次引导（用完删除）
├── logs/                      # 日志
├── browser/                   # 浏览器数据
└── extensions/                # 扩展插件
```

---

## 五、消息渠道

支持的渠道（每个 Gateway 可同时连接多个）：

| 渠道 | 协议 | 说明 |
|------|------|------|
| WhatsApp | Baileys (Web) | 无需官方 API |
| Telegram | grammY | Bot 模式 |
| Discord | discord.js | Bot 模式 |
| Signal | signal-cli | 本地连接 |
| iMessage | imsg CLI | 仅 macOS |
| Slack | Bolt | Bot 模式 |
| WebChat | 内置 | Gateway 自带 |
| 飞书/钉钉/MS Teams | 插件/桥接 | 需额外配置 |

**路由规则**：
- 私聊 → 按 `dmScope` 策略路由到对应会话
- 群聊 → 需 @mention 或关键词触发（可配置）
- `channel-routing.md` 控制细粒度路由

---

## 六、自动化

### Heartbeat（心跳）

Gateway 定期唤醒 Agent 执行 `HEARTBEAT.md` 中的任务。适合批量检查（邮件、日历、天气等）。
- 默认间隔：30 分钟
- 配置：`gateway.heartbeat`

### Cron Jobs（定时任务）

精确时间调度，支持两种负载：
- `systemEvent` — 注入到主会话
- `agentTurn` — 创建隔离会话执行
- 管理命令：`openclaw cron list/add/remove/run`

### Hooks（钩子）

事件驱动执行：消息到达、会话创建、Agent 完成回复等时机触发自定义脚本。

---

## 七、CLI 命令速查

```bash
# 状态与诊断
openclaw status              # 系统状态概览
openclaw doctor              # 健康检查
openclaw logs                # 查看日志

# 配置
openclaw configure           # 交互式配置向导
openclaw config get/set      # 读写配置

# Agent 管理
openclaw agents list         # 列出 Agent
openclaw agents add <id>     # 添加新 Agent

# 会话
openclaw sessions list       # 列出会话

# 模型
openclaw models list         # 可用模型
openclaw models set          # 设置主模型

# 渠道
openclaw channels list       # 已连接渠道
openclaw channels add        # 添加渠道

# Cron
openclaw cron list           # 定时任务列表
openclaw cron add            # 添加任务
openclaw cron run <id>       # 立即执行

# Skills
openclaw skills list         # 已加载技能

# Gateway 服务
openclaw gateway start/stop/restart
openclaw gateway status

# 更新
openclaw update              # 检查并更新

# 备份
openclaw backup create       # 创建备份
```

---

## 八、配置速查

主配置文件：`~/.openclaw/openclaw.json`（JSON5 格式）

```json5
{
  // 模型
  models: {
    providers: {
      xiaomi: { baseUrl: "...", apiKey: "...", models: [...] },
      openai: { apiKey: "...", models: [...] },
    }
  },
  // Agent 默认值
  agents: {
    defaults: {
      model: { primary: "xiaomi/mimo-v2-pro", fallbacks: [...] },
      workspace: "~/.openclaw/workspace",
      compaction: { mode: "safeguard" },
    }
  },
  // Gateway
  gateway: {
    port: 18789,
    mode: "local",        // local | remote
    bind: "lan",          // lan | tailscale
    heartbeat: { enabled: true, intervalMs: 1800000 },
  },
  // 会话
  session: {
    dmScope: "per-channel-peer",  // main | per-peer | per-channel-peer
  },
  // 工具策略
  tools: {
    profile: "full",              // minimal | coding | messaging | full
    deny: ["tts"],
    exec: { security: "allowlist" },
  },
}
```

---

## 九、安全模型

- **Exec 安全**：`tools.exec.security` 控制命令执行策略（`allowlist` / `full`）
- **沙箱**：`agents.defaults.sandbox` 隔离非主会话的工作区
- **设备配对**：所有节点设备需人工审批配对
- **Token 认证**：Gateway 默认要求 WS 连接携带 auth token
- **Skill 隔离**：第三方 Skill 视为不受信任代码，读取前审阅

---

## 十、文档位置

本地文档根目录：`/usr/lib/node_modules/openclaw/docs/`

| 目录 | 内容 |
|------|------|
| `concepts/` | 架构、Agent、会话、模型、压缩、多 Agent |
| `cli/` | 所有 CLI 命令文档 |
| `channels/` | 各消息渠道配置 |
| `tools/` | 工具、Skill、浏览器、exec |
| `gateway/` | Gateway 配置、认证、网络 |
| `automation/` | Cron、Heartbeat、Hooks、Webhook |
| `install/` | 安装指南（Docker、Pi、云平台） |
| `providers/` | 模型 Provider 配置 |
| `zh-CN/` | 中文文档（覆盖大部分内容） |

在线文档：https://docs.openclaw.ai
