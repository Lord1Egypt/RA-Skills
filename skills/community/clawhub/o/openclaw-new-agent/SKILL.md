---
name: openclaw-new-agent
description: 在 OpenClaw 上创建新的独立飞书机器人（多账号模式）。当用户要求创建新的飞书机器人、新增 Agent、部署第二个机器人时使用。流程包括：收集配置信息 → 备份 → 创建工作区 → 修改配置 → 验证。
keywords:
  - openclaw
  - feishu
  - lark
  - multi-agent
  - chatbot
  - robot
version: 1.2.1
author: Zhou Quan
homepage: https://clawhub.com
repository: https://github.com/itzhouq/openclaw-new-agent
license: MIT
---

# openclaw-new-agent

> 在 OpenClaw 上丝滑创建多个独立的飞书机器人 Agent

本 Skill 用于在已运行的 OpenClaw 实例上，新增一个独立的飞书机器人 Agent。

---

## 前提条件

用户需要提前准备好：
1. 飞书开放平台上的新应用（App ID + App Secret）
2. 新机器人在飞书中的名称
3. 工作区文件夹名称（与现有 workspace 平级，不是子文件夹）

### 快速创建飞书机器人

如果用户还没有飞书机器人，可通过以下方式快速创建：

👉 **推荐：一键创建模板应用**
https://open.feishu.cn/page/openclaw?form=multiAgent

使用此链接可直接生成包含 WebSocket 事件订阅配置的多账号模式模板应用，无需手动配置权限和事件订阅。

---

## Step 0：确认使用场景

在开始之前，向用户确认以下信息：

| 问题 | 说明 |
|------|------|
| 新 Agent 的用途是什么？ | 用于记录到 SOUL.md，定义 Agent 角色 |
| 工作区文件夹名称？ | 建议：`workspace-{功能名}`，如 `workspace-codewriter` |
| App ID & App Secret？ | 新的飞书机器人凭证（格式：`cli_xxx`） |
| Obsidian 相关（可选） | 如涉及信息收集，记录 vault 路径和笔记结构 |

> **账号获取说明**：配置初期 allowFrom 可先留空，等用户向新机器人发送测试消息后，从日志中自动获取发送者 open_id 并补充到 allowFrom。

---

## Step 1：备份现有配置

**必须操作**，所有配置变更前必须备份：

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.{日期标签}.bak
```

常用备份标签：
- `.beforemultiagentbak` — 多机器人配置前
- `.before-{agentId}bak` — 新增特定 Agent 前

---

## Step 2：创建独立工作区

工作区必须与主 `workspace` **平级**，不是子文件夹：

```
.openclaw/
├── workspace/                  ← 主工作区
└── workspace-{name}/           ← 新工作区（平级）
    ├── SOUL.md                 # Agent 角色定义
    ├── USER.md                 # 用户信息
    ├── AGENTS.md               # 工作区说明
    ├── MEMORY.md               # 长期记忆（可选）
    ├── HEARTBEAT.md            # 心跳任务（默认空）
    └── memory/                 # 每日工作日志
        └── YYYY-MM-DD.md
```

### SOUL.md 模板

```markdown
# SOUL.md - {Agent名称}

_我是 {Agent名称}，..._

## 角色定位

- **核心能力**：
- **风格**：
- **原则**：

## 工作方式

1.
2.
3.

## 边界

-
```

### USER.md 模板

```markdown
# USER.md - 用户信息

- **Name:** {用户名}
- **What to call them:** {称呼}
- **Timezone:** Asia/Shanghai (GMT+8)

## 相关信息（如适用）

-
```

---

## Step 3：确认飞书机器人配置

向用户收集以下信息：

| 信息 | 必填 | 说明 |
|------|------|------|
| App ID | ✅ | 格式：`cli_xxx`，来自飞书开放平台 |
| App Secret | ✅ | 对应 App ID 的 Secret |
| Bot Name | ✅ | 机器人在飞书显示的名称 |
| 允许的用户 | ⚠️ | 用户的 open_id（可能有多个账号）|

> 💡 **没有飞书机器人？** 使用 [一键创建链接](https://open.feishu.cn/page/openclaw?form=multiAgent)，自动生成已配置好权限和事件订阅的模板应用。

### ⚠️ 重要：allowFrom 自动获取

**allowFrom 不需要用户提前确认**。配置时 allowFrom 可先留空，等用户向新机器人发送测试消息后，从日志中自动获取发送者 open_id：

```bash
grep "{agentId}" ~/.openclaw/logs/gateway.log | grep "received message from"
```

获取到 open_id 后，用 `gateway config.patch` 补充到 `allowFrom` 即可。

---

## Step 4：修改 openclaw.json

使用 `gateway config.patch` **局部更新**，不要覆盖整个文件。

### 配置结构

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": { ... },                    // 现有账号，保持不变
        "{agentId}": {                         // 新账号
          "enabled": true,
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "domain": "feishu",
          "connectionMode": "websocket",
          "requireMention": true,
          "dmPolicy": "allowlist",
          "allowFrom": [
            "ou_将使用此机器人的账号open_id"  // ⚠️ 只加实际会发消息的账号
          ],
          "groupAllowFrom": [
            "ou_将使用此机器人的账号open_id"
          ],
          "groupPolicy": "allowlist",
          "groups": {
            "*": { "enabled": true }
          }
        }
      }
    }
  },
  "agents": {
    "list": [
      { "id": "main" },
      { "id": "{agentId}", "workspace": "/path/to/workspace-{name}" }
    ]
  }
}
```

> ⚠️ **allowFrom 配置原则**：只添加**实际会发送消息**的账号。不要添加主账号（它使用 default 机器人）。如果用户有多个账号，确保所有会向此机器人发送消息的账号都在 allowFrom 中。

---

## Step 5：验证创建结果

### 5.1 检查配置

```bash
openclaw doctor --non-interactive
```

确认输出中包含新 agent：

```
Agents: main (default), {agentId}
```

### 5.2 检查日志

```bash
grep "{agentId}" ~/.openclaw/logs/gateway.log
```

确认无错误，特别是：
- WebSocket 连接成功
- 消息接收正常

### 5.3 功能测试

让用户通过飞书向新机器人发送消息，验证：
- 消息是否到达（查看日志）
- 是否在白名单中
- 是否正确路由到对应 workspace

---

## 常见问题 Checklist

开始前逐项确认，避免创建失败：

- [ ] **备份已完成**：`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.beforemultiagentbak`
- [ ] **工作区目录已创建**：与 `workspace` 平级，不是子文件夹
- [ ] **App ID 和 App Secret 正确**：格式为 `cli_xxx` 和对应的 Secret
- [ ] **allowFrom 已正确配置**：只添加**实际会向此机器人发送消息**的账号（通常不是主账号）
- [ ] **Gateway 已重启**：配置更新后等待 2-3 秒
- [ ] **飞书开放平台已配置**：机器人已启用、权限已开通、事件订阅已配置（可使用 [一键创建链接](https://open.feishu.cn/page/openclaw?form=multiAgent) 快速完成）

---

## 回滚方案

如果创建失败，执行以下回滚：

```bash
# 恢复配置
cp ~/.openclaw/openclaw.json.beforemultiagentbak ~/.openclaw/openclaw.json

# 重启 Gateway
openclaw gateway restart
```

---

## 相关文档

- OpenClaw 官方文档：`~/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/docs/`
- 飞书插件文档：`~/.openclaw/extensions/openclaw-lark/`
