---
name: multi-agent-bot
description: 在 OpenClaw 中创建新的 Agent 并绑定到新的飞书机器人/群聊。用于：(1) 添加新 Agent 管理不同飞书群聊 (2) 实现多机器人路由 (3) 为不同业务线创建独立 Agent。需修改 ~/.openclaw/openclaw.json 配置文件。
---

# Multi-Agent-Bot 创建技能

此技能用于在 OpenClaw 中快速创建新 Agent 并配置飞书机器人绑定，实现多机器人多 Agent 架构。

## 使用场景

- 为不同飞书群聊配置专属 Agent
- 实现多机器人消息路由
- 分离不同业务线的对话记忆
- 隔离不同群聊的访问权限

## 工作原理

OpenClaw 支持多账户配置，通过 `bindings` 将不同的飞书机器人绑定到不同的 Agent，每个 Agent 有独立的工作空间和记忆。

## 创建步骤

### 步骤 1：准备信息

收集以下内容：
| 内容 | 说明 | 示例 |
|------|------|------|
| Agent ID | 唯一标识符 | `support`, `sales` |
| Agent 名称 | 显示名称 | "客服助手" |
| 工作空间 | 独立目录路径 | `~/.openclaw/workspace-support` |
| 飞书 App ID | 机器人凭证 | `cli_xxx` |
| 飞书 App Secret | 机器人密钥 | `xxx` |

### 步骤 2：修改配置文件

编辑 `~/.openclaw/openclaw.json`，添加三部分配置：

**1. 在 `agents.list` 添加新 Agent：**

```json
{
  "id": "新agent-id",
  "name": "显示名称",
  "workspace": "~/.openclaw/workspace-名称",
  "model": { "primary": "ark/doubao" }
}
```

**2. 在 `channels.feishu.accounts` 添加机器人：**

```json
{
  "account-id": {
    "appId": "飞书appId",
    "appSecret": "飞书appSecret",
    "botName": "机器人名称",
    "dmPolicy": "allowlist",
    "allowFrom": ["允许的用户ID"]
  }
}
```

**3. 在 `bindings` 添加路由：**

```json
{
  "agentId": "新agent-id",
  "match": {
    "channel": "feishu",
    "accountId": "account-id"
  }
}
```

完整配置模板见 `references/config-template.json`。

### 步骤 3：创建工作空间

```bash
mkdir ~/.openclaw/workspace-名称
```

### 步骤 4：重启生效

```bash
openclaw gateway restart
```

## 路由优先级

当收到飞书消息时，按以下顺序匹配：

1. **精确匹配**：`peer.kind` + `peer.id`（特定用户/群）
2. **线程继承**：群聊中线程消息
3. **账户匹配**：`accountId`
4. **渠道匹配**：`channel` + `accountId: "*"`
5. **默认 Agent**：设为 `default: true` 的 Agent

## 权限策略

| 策略 | 说明 |
|------|------|
| `open` | 允许所有人 |
| `allowlist` | 仅允许列表内用户 |
| `denylist` | 禁止列表内用户 |

## 注意事项

1. 每个 Agent 必须有独立工作空间，避免记忆混淆
2. 飞书机器人需先在飞书开放平台创建
3. 修改配置后必须重启 OpenClaw
4. 建议使用有意义的 Agent ID，便于识别

## 相关文档

- [飞书多机器人配置指南](https://docs.openclaw.ai/docs/feishu/multiple-bots)
- [OpenClaw 官方文档](https://docs.openclaw.ai)
