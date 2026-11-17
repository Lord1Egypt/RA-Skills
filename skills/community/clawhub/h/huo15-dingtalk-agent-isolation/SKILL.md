---
name: huo15-dingtalk-agent-isolation
displayName: 火一五钉钉智能体隔离
description: 火一五钉钉智能体隔离 - 为每个钉钉用户创建独立 Agent 工作空间、记忆和会话历史。支持手动绑定和动态创建两种模式。触发词：钉钉Agent隔离、钉钉用户隔离、动态Agent创建、dingtalk agent isolation。
version: 1.0.0
dependencies:
  required: ["@dingtalk-real-ai/dingtalk-connector >=0.8.24"]
  optional: ["huo15-openclaw-multi-agent"]
aliases:
  - 火一五钉钉智能体隔离
  - 火一五钉钉Agent隔离
  - 火一五钉钉用户隔离
  - 火一五动态Agent创建
  - 火一五钉钉工作空间隔离
  - 钉钉Agent隔离
  - 钉钉用户隔离
  - dingtalk agent isolation
  - dynamic agent creation
---

# 🔒 火一五钉钉智能体隔离 (huo15-dingtalk-agent-isolation)

> **作者**: 火一五信息科技有限公司
> **版本**: v1.0.0
> **适用**: `@dingtalk-real-ai/dingtalk-connector` >= 0.8.24
> **参考**: OpenClaw Feishu `dynamic-agent.ts` 实现

---

## 一、概述

为每个钉钉用户创建**独立的 Agent 工作空间**，实现：

| 隔离维度 | 说明 |
|---------|------|
| **工作空间** | 每个用户有独立的 `workspace` 目录，文件互不干扰 |
| **Agent 目录** | 独立的 `agentDir`，存放 Agent 配置和记忆 |
| **会话历史** | 对话上下文按用户隔离，互不可见 |
| **技能/插件** | 可为不同用户配置不同的技能和工具 |
| **公共资源** | 公共技能和插件仍然共享，无需重复安装 |

### 架构示意

```
钉钉用户 A 发消息
    ↓ bindings 匹配
Agent: dingtalk-userA (workspace: ~/.openclaw/workspace-dingtalk-userA)
    ↓ 独立会话
    ↓ 独立记忆
    ↓ 独立工作空间文件

钉钉用户 B 发消息
    ↓ bindings 匹配
Agent: dingtalk-userB (workspace: ~/.openclaw/workspace-dingtalk-userB)
    ↓ 独立会话
    ↓ 独立记忆
    ↓ 独立工作空间文件

公共技能/插件 → 所有 Agent 共享（无需重复安装）
```

---

## 二、两种模式

### Mode A: 手动绑定（推荐，开箱即用）

**适用场景**: 用户数量已知且固定（如团队内部使用）

**原理**: 在 `openclaw.json` 中手动为每个用户配置 agent + binding。钉钉连接器 v0.8.24+ 已内置 `bindings` 匹配逻辑，**无需修改任何代码**。

**优点**:
- 零代码改动，纯配置
- 完全可控，精确指定哪些用户使用哪个 Agent
- 支持群聊和单聊两种场景

**限制**:
- 需要提前知道用户的 `senderStaffId`
- 新用户需要手动添加配置

### Mode B: 动态创建（高级，自动扩展）

**适用场景**: 用户数量未知或持续增长（如对外服务）

**原理**: 用户首次私聊机器人时，自动创建独立的 Agent + binding，写入 `openclaw.json`。参考飞书 `dynamic-agent.ts` 的实现。

**优点**:
- 全自动，新用户首次对话即自动隔离
- 支持上限控制 (`maxAgents`)
- 原子化配置写入，并发安全

**限制**:
- 需要修改钉钉连接器源码（打 patch）
- 仅支持单聊（DM）场景的自动创建
- 群聊仍需手动配置 binding

---

## 三、Mode A — 手动绑定配置指南

### 3.1 获取用户 ID

让目标用户给机器人发一条消息，在 OpenClaw 日志中找到 `senderStaffId`：

```
[DingTalk] 处理消息: accountId=default, sender=张三, senderStaffId=xxxx123
```

### 3.2 配置 openclaw.json

在 `~/.openclaw/openclaw.json` 中添加 agents 和 bindings：

```jsonc
{
  // ... 其他配置 ...

  "agents": {
    "default": "main",
    "list": [
      {
        "id": "main",
        "workspace": "~/.openclaw",
        "agentDir": "~/.openclaw/agents/main/agent"
      },
      // ===== 钉钉用户 A 的独立 Agent =====
      {
        "id": "dingtalk-userA",
        "workspace": "~/.openclaw/workspace-dingtalk-userA",
        "agentDir": "~/.openclaw/agents/dingtalk-userA/agent"
      },
      // ===== 钉钉用户 B 的独立 Agent =====
      {
        "id": "dingtalk-userB",
        "workspace": "~/.openclaw/workspace-dingtalk-userB",
        "agentDir": "~/.openclaw/agents/dingtalk-userB/agent"
      }
    ]
  },

  "bindings": [
    // 用户 A 的单聊消息 → dingtalk-userA Agent
    {
      "agentId": "dingtalk-userA",
      "match": {
        "channel": "dingtalk-connector",
        "peer": { "kind": "direct", "id": "用户A的senderStaffId" }
      }
    },
    // 用户 B 的单聊消息 → dingtalk-userB Agent
    {
      "agentId": "dingtalk-userB",
      "match": {
        "channel": "dingtalk-connector",
        "peer": { "kind": "direct", "id": "用户B的senderStaffId" }
      }
    },
    // 特定群聊 → 特定 Agent（可选）
    {
      "agentId": "dingtalk-team-alpha",
      "match": {
        "channel": "dingtalk-connector",
        "peer": { "kind": "group", "id": "cidXXXXXXXXXXXX" }
      }
    }
  ]
}
```

### 3.3 创建工作空间目录

```bash
# 为每个用户创建工作空间和 Agent 目录
mkdir -p ~/.openclaw/workspace-dingtalk-userA
mkdir -p ~/.openclaw/agents/dingtalk-userA/agent
mkdir -p ~/.openclaw/workspace-dingtalk-userB
mkdir -p ~/.openclaw/agents/dingtalk-userB/agent
```

### 3.4 重启 OpenClaw

```bash
openclaw restart
```

### 3.5 binding 匹配规则

钉钉连接器按以下优先级匹配：

| match 字段 | 说明 | 示例 |
|-----------|------|------|
| `channel` | 渠道 ID，固定为 `dingtalk-connector` | `"dingtalk-connector"` |
| `accountId` | 账号 ID（多账号场景） | `"default"` 或自定义 |
| `peer.kind` | 会话类型 | `"direct"` (单聊) / `"group"` (群聊) |
| `peer.id` | 用户 ID 或群会话 ID | `"senderStaffId"` 或 `"cidXXXX"` |
| `peer.id: "*"` | 通配符，匹配该 kind 下所有会话 | `"*"` |

> 匹配顺序：从上到下，第一个匹配的 binding 生效。未匹配到任何 binding 时，使用 `agents.default` 指定的 Agent。

---

## 四、Mode B — 动态 Agent 创建指南

### 4.1 前置条件

- 钉钉连接器已通过 `openclaw install @dingtalk-real-ai/dingtalk-connector` 安装
- 连接器源码位于 `~/.openclaw/extensions/dingtalk/` 或通过 npm 安装

### 4.2 执行 Patch

```bash
# 方式一：使用本 Skill 提供的 patch 脚本
bash ~/.catpaw/skills/huo15-dingtalk-agent-isolation/scripts/apply-dynamic-agent-patch.sh

# 方式二：手动应用（见 references/dynamic-agent-patch.ts）
```

Patch 做了以下修改：

1. **`src/config/schema.ts`**: 在 `DingtalkSharedConfigShape` 中添加 `dynamicAgentCreation` 配置项
2. **`src/types/index.ts`**: 添加 `DynamicAgentCreationConfig` 类型
3. **`src/dynamic-agent.ts`** (新文件): 移植飞书的 `maybeCreateDynamicAgent` 逻辑
4. **`src/core/message-handler.ts`**: 在 binding 匹配为 default 时调用动态创建

### 4.3 配置 openclaw.json

在 `channels.dingtalk-connector` 中添加 `dynamicAgentCreation` 配置：

```jsonc
{
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "clientId": "your-client-id",
      "clientSecret": "your-client-secret",

      // ===== 动态 Agent 创建配置 =====
      "dynamicAgentCreation": {
        "enabled": true,
        "workspaceTemplate": "~/.openclaw/workspace-dingtalk-{agentId}",
        "agentDirTemplate": "~/.openclaw/agents/{agentId}/agent",
        "maxAgents": 100
      }
    }
  }
}
```

### 4.4 配置参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | `false` | 是否启用动态创建 |
| `workspaceTemplate` | string | `~/.openclaw/workspace-dingtalk-{agentId}` | 工作空间路径模板 |
| `agentDirTemplate` | string | `~/.openclaw/agents/{agentId}/agent` | Agent 目录路径模板 |
| `maxAgents` | number | 无限制 | 动态创建的 Agent 最大数量 |

**模板变量**:

| 变量 | 说明 | 示例 |
|------|------|------|
| `{userId}` | 钉钉用户 senderStaffId | `abc123def456` |
| `{agentId}` | 自动生成的 Agent ID | `dingtalk-abc123de-a1b2c3d4...` |

### 4.5 动态 Agent ID 生成规则

```
默认账号:  dingtalk-{senderStaffId}
命名账号:  dingtalk-{accountId前12位}-{sha256(accountId+senderStaffId)前32位}
```

### 4.6 重启并验证

```bash
openclaw restart
```

---

## 五、混合模式（推荐最佳实践）

同时使用 Mode A + Mode B：

- **已知核心用户**: 手动配置 binding（Mode A），使用定制化的 Agent 配置
- **未知新用户**: 动态创建（Mode B），使用默认配置
- **公共群聊**: 手动配置 binding 到共享 Agent

```jsonc
{
  "agents": {
    "default": "main",
    "list": [
      { "id": "main", "workspace": "~/.openclaw", "agentDir": "~/.openclaw/agents/main/agent" },
      // 核心用户的手动 Agent
      { "id": "dingtalk-admin", "workspace": "~/.openclaw/workspace-admin", "agentDir": "~/.openclaw/agents/dingtalk-admin/agent" }
      // 动态创建的 Agent 会自动追加到此列表
    ]
  },
  "bindings": [
    // 管理员 → 专用 Agent
    {
      "agentId": "dingtalk-admin",
      "match": { "channel": "dingtalk-connector", "peer": { "kind": "direct", "id": "admin的staffId" } }
    }
    // 动态创建的 binding 会自动追加
  ],
  "channels": {
    "dingtalk-connector": {
      "enabled": true,
      "clientId": "...",
      "clientSecret": "...",
      "dynamicAgentCreation": {
        "enabled": true,
        "maxAgents": 50
      }
    }
  }
}
```

> **匹配优先级**: 手动 binding > 动态 binding > default Agent。手动配置的 binding 会先匹配到，不会被动态创建覆盖。

---

## 六、验证

### 6.1 手动验证

```bash
# 1. 检查配置是否正确
cat ~/.openclaw/openclaw.json | jq '.agents.list | length'
# 应输出: N（原有 + 新增的用户 Agent 数量）

# 2. 检查工作空间目录是否创建
ls -la ~/.openclaw/workspace-dingtalk-*/
# 应看到每个用户的独立目录

# 3. 检查 Agent 目录
ls -la ~/.openclaw/agents/dingtalk-*/
# 应看到每个用户的 agent 目录

# 4. 发送测试消息
# 用户 A 给机器人发消息 → 检查日志中 agentId=dingtalk-userA
# 用户 B 给机器人发消息 → 检查日志中 agentId=dingtalk-userB
```

### 6.2 日志验证

在 OpenClaw 日志中搜索以下关键字：

```
# 手动模式
grep "agentId=dingtalk-" ~/.openclaw/logs/openclaw.log

# 动态模式
grep "creating dynamic agent" ~/.openclaw/logs/openclaw.log
grep "Agent 工作空间路径" ~/.openclaw/logs/openclaw.log
```

### 6.3 自动验证脚本

```bash
bash ~/.catpaw/skills/huo15-dingtalk-agent-isolation/scripts/verify-isolation.sh
```

---

## 七、常见问题

### Q1: 新用户发消息后没有创建 Agent？

**检查清单**:
1. `dynamicAgentCreation.enabled` 是否为 `true`
2. 用户是否通过**单聊**（非群聊）发消息 — 动态创建仅在单聊时触发
3. `maxAgents` 是否已达上限
4. 连接器 patch 是否正确应用 — 检查 `src/dynamic-agent.ts` 是否存在
5. OpenClaw 是否已重启

### Q2: 群聊消息没有按用户隔离？

群聊默认使用 `groupSessionScope: "group"`（一个群一个会话）。如需群聊中按用户隔离：
- 设置 `groupSessionScope: "group_sender"`（群内按发送者隔离会话）
- 或为群聊手动配置 binding 到特定 Agent

### Q3: 如何为不同用户配置不同的模型/工具？

在 `agents.list` 中为每个 Agent 指定独立的配置：

```jsonc
{
  "id": "dingtalk-userA",
  "workspace": "~/.openclaw/workspace-dingtalk-userA",
  "agentDir": "~/.openclaw/agents/dingtalk-userA/agent",
  "model": "gpt-4o",           // 指定模型
  "tools": {
    "profile": "full",          // 指定工具档
    "alsoAllow": ["web_search"] // 追加工具
  },
  "systemPrompt": "你是用户A的专属助手..."
}
```

> 动态创建的 Agent 默认继承 `agents.defaults` 的配置。如需为动态创建的 Agent 自定义配置，在 `workspaceTemplate` 指向的目录中放置 `agent.json`。

### Q4: 如何删除某个用户的 Agent？

1. 从 `openclaw.json` 的 `agents.list` 中移除对应条目
2. 从 `bindings` 中移除对应的 binding
3. 删除工作空间目录: `rm -rf ~/.openclaw/workspace-dingtalk-userA`
4. 删除 Agent 目录: `rm -rf ~/.openclaw/agents/dingtalk-userA`
5. 重启 OpenClaw

### Q5: 动态创建的 Agent 会共享公共技能吗？

**是的**。所有 Agent（无论手动还是动态创建）都共享 OpenClaw 全局安装的技能和插件。Agent 的 `workspace` 和 `agentDir` 仅隔离工作文件、记忆和会话历史，不影响技能的可用性。

---

## 八、版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0.0 | 2026-08-01 | 初始版本：支持手动绑定（Mode A）和动态创建（Mode B）两种模式 |
