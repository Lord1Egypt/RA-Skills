---
name: openclaw-multiagent
description: Configure multi-agent TG group system with shared Workspace + MemOS memory. Use when user wants to set up multiple AI agents in a Telegram group, with specialized roles and collaborative workspace.
triggers:
  - "多 Agent"
  - "多 agent"
  - "multi-agent"
  - "multi agent"
  - "TG 群组"
  - "telegram group"
  - "配置 Agent"
  - "添加子 Agent"
  - "协作 Agent"
version: 1.0.0
---

# OpenClaw 多 Agent TG 群组系统配置指南

## 架构说明

### Workspace：共享模式

所有 Agent 共享同一个 workspace（`.openclaw/workspace`）。

- 主 Agent 的文件在 workspace 根目录（SOUL.md, AGENTS.md 等）
- 每个子 Agent 的专属文件在 `workspace/agents/{agent_id}/` 子目录
- 共享上下文在 `workspace/shared-context/` — 所有 Agent 都可读取
- 协作通过文件完成：一个 Agent 写文件，另一个 Agent 读文件

### 记忆：MemOS Cloud

- MemOS Cloud 插件已安装并启用，挂载在 OpenClaw 实例级别
- **所有 Agent 自动共享同一个记忆池**
- 不需要创建 memory/ 目录或 YYYY-MM-DD.md 日志文件

### 目录结构

```
workspace/
├── SOUL.md                    # 主 Agent 的灵魂
├── IDENTITY.md                # 主 Agent 身份卡
├── AGENTS.md                  # 主 Agent 行为规则
├── USER.md                    # 用户信息（所有 Agent 共享读取）
├── HEARTBEAT.md               # 主 Agent 心跳任务
├── shared-context/            # 跨 Agent 共享层
│   ├── FEEDBACK-LOG.md        # 通用反馈/修正记录
│   └── SIGNALS.md             # 当前关注的趋势/信号
└── agents/
    ├── {agent_id}/            # 子 Agent 专属目录
    │   ├── SOUL.md            # 子 Agent 灵魂
    │   ├── IDENTITY.md        # 子 Agent 身份卡
    │   └── AGENTS.md          # 子 Agent 行为规则
    └── {另一个agent_id}/
        └── ...
```

## 配置前准备

需要用户提供：

1. **TG 群组 ID**（负数，如 -1002345678901）
2. **用户的 TG 用户 ID**（如 5701780765）
3. **主 Bot Token**（已配置或新提供）
4. **子 Agent 列表**（YAML 格式）

## ⚠️ 手动前置操作（必须）

### 1. BotFather 设置
每个子 Bot → `/setprivacy` → **Disable**（否则 Bot 无法读取群消息）

### 2. 拉 Bot 进群
所有 Bot（主 + 子）必须先被添加到目标 TG 群组

### 3. 获取 Bot Token
每个子 Bot 需要从 @BotFather 获取独立的 Bot Token

### 4. 获取群组 ID
- 转发群消息给 [@raw_data_bot](https://t.me/raw_data_bot)
- 或查看群组消息的 `chat.id` 字段

## 执行步骤

### Step 1：备份
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d%H%M%S)
```

### Step 2：创建目录结构
```bash
# 共享上下文目录
mkdir -p ~/.openclaw/workspace/shared-context

# 每个子 Agent 的专属目录
mkdir -p ~/.openclaw/workspace/agents/{agent_id}

# 每个子 Agent 的 OpenClaw 内部目录
mkdir -p ~/.openclaw/agents/{agent_id}/agent
```

### Step 3：创建共享上下文文件
写入 `shared-context/FEEDBACK-LOG.md` 和 `shared-context/SIGNALS.md`

### Step 4-6：为每个子 Agent 创建
- SOUL.md
- IDENTITY.md
- AGENTS.md

### Step 7：修改 openclaw.json
关键修改：
1. **channels.telegram** → 改为 accounts 多账号模式
2. **agents** → 添加子 Agent 配置
3. **bindings** → 添加 agent 与 channel 的绑定
4. **tools** → 确保 agentToAgent 和 sessions.visibility 配置

### Step 8-11：验证、重启、验证上线、汇报

## 配置示例

### Telegram Accounts 配置
```json
"telegram": {
  "enabled": true,
  "dmPolicy": "pairing",
  "groupPolicy": "allowlist",
  "streaming": "partial",
  "accounts": {
    "default": {
      "botToken": "主BotToken",
      "dmPolicy": "pairing",
      "groupPolicy": "allowlist",
      "streaming": "partial",
      "groups": {
        "-100xxxx": { "requireMention": false }
      },
      "groupAllowFrom": ["用户ID"]
    },
    "agent_id": {
      "name": "Agent名称",
      "enabled": true,
      "botToken": "子BotToken",
      "dmPolicy": "allowlist",
      "allowFrom": ["用户ID"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["用户ID"],
      "streaming": "off",
      "commands": {
        "native": false,
        "nativeSkills": false
      },
      "groups": {
        "-100xxxx": { "requireMention": true }
      }
    }
  }
}
```

### Agents 配置
```json
"agents": {
  "defaults": {
    "workspace": "~/.openclaw/workspace",
    "model": { "primary": "..." }
  },
  "list": [
    { "id": "main" },
    {
      "id": "agent_id",
      "name": "agent_id",
      "workspace": "~/.openclaw/workspace",
      "model": "..."
    }
  ]
}
```

### Bindings 配置
```json
"bindings": [
  {
    "agentId": "agent_id",
    "match": {
      "channel": "telegram",
      "accountId": "agent_id"
    }
  }
]
```

## 踩坑防护清单

- [ ] 子 Bot 的 `/setprivacy` 必须设为 Disable
- [ ] 子 Bot 的 commands.native 和 nativeSkills 必须为 false
- [ ] 原顶层 botToken 必须删除，移入 accounts.default
- [ ] JSON 修改后必须验证语法
- [ ] 所有 Agent 的 workspace 指向同一个路径
- [ ] 区分 workspace/agents/（工作文件）和 .openclaw/agents/（内部数据）
- [ ] shared-context/ 文件遵循一写多读原则
- [ ] MemOS 记忆已全局生效，不要创建 memory/ 目录

## 参考

- 完整指南: https://github.com/bozhouDev/openclaw_agent_create_prompt
