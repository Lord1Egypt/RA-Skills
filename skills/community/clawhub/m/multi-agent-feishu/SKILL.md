---
name: multi-agent-feishu
description: |
  在 OpenClaw Gateway 中创建多个 Agent 并绑定多个飞书账号。
  适用于：(1) 需要多个独立 AI 助手 (2) 不同用户使用不同 Agent (3) 需要隔离的记忆/身份场景。
---

# Multi-Agent Feishu Setup

在同一个 OpenClaw Gateway 下创建多个 Agent，每个绑定不同飞书机器人。

## 快速开始

### 1. 创建 Agent

```bash
openclaw agents add <agent_id> \
  --workspace ~/.openclaw/workspace<N> \
  --bind feishu:<account_id> \
  --non-interactive
```

### 2. 添加飞书账号

编辑 `~/.openclaw/openclaw.json`，在 `channels.feishu.accounts` 中添加：

```json
"<account_id>": {
  "appId": "cli_xxx",
  "appSecret": "xxx"
}
```

### 3. 重启 Gateway

```bash
openclaw gateway restart
```

### 4. 配对飞书

```bash
openclaw pairing approve feishu <配对码>
```

## 验证配置

```bash
openclaw agents list --bindings
```

## 详细文档

- [配置字段说明](references/config-fields.md) - agents.list、bindings、channels 字段详解
- [飞书机器人创建指南](references/feishu-app.md) - 如何在飞书开放平台创建机器人
- [多 Agent 架构图](references/architecture.md) - 架构说明和流程图
- [常见问题](references/faq.md) - 配对失败、收不到消息等问题排查
- [备份与恢复](references/backup.md) - 配置备份和恢复方法
