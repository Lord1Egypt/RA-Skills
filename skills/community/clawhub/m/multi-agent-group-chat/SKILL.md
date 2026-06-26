---
name: multi-agent-chat
description: |
  多 Agent 群聊协作插件。子 Agent 完成 sessions_send 任务后，自动将回复发送到来源群聊。
  支持 Telegram 和飞书，无需配置群 ID，自动检测消息来源。
  适用于：多 Bot 协作、团队分工、群聊表演等场景。
version: 2.0.0
homepage: https://clawhub.com
metadata:
  openclaw:
    emoji: "🤝"
    keywords:
      - multi-agent
      - group-chat
      - collaboration
      - telegram
      - feishu
      - sessions_send
      - plugin
---

# Multi-Agent Group Chat Plugin

多 Agent 群聊协作插件，让 AI 团队在群里"讨论"起来。

## 功能

- ✅ 子 Agent 完成任务后，自动发到群里
- ✅ 自动检测来源群，无需配置群 ID
- ✅ 支持 Telegram 和飞书
- ✅ 仅处理 sessions_send 内部任务，不影响正常对话

## 架构

```
用户 @Boss → Boss 分配任务 → 子 Agent 执行
                              ↓
                    【插件自动转发到群】
                              ↓
                    用户在群里看到讨论过程
```

## 安装

### 方式 1：从 ClawHub 安装
```bash
clawhub install multi-agent-chat
```

### 方式 2：手动安装
复制 `index.ts` 和 `openclaw.plugin.json` 到：
```
~/.openclaw/extensions/multi-agent-chat/
```

## 配置

在 `openclaw.json` 中启用插件：

```json
{
  "plugins": {
    "allow": ["multi-agent-chat"],
    "entries": {
      "multi-agent-chat": {
        "enabled": true
      }
    }
  }
}
```

## 配套 Agent 配置

需要配置多个 Agent：

```json
{
  "agents": {
    "entries": {
      "boss": { "workspace": "~/.openclaw/agents/boss" },
      "coder": { "workspace": "~/.openclaw/agents/coder" },
      "writer": { "workspace": "~/.openclaw/agents/writer" }
    }
  },
  "channels": {
    "telegram": {
      "accounts": {
        "boss": { "token": "BOT_TOKEN_1", "agent": "boss" },
        "coder": { "token": "BOT_TOKEN_2", "agent": "coder" },
        "writer": { "token": "BOT_TOKEN_3", "agent": "writer" }
      },
      "groupPolicy": "open"
    }
  }
}
```

## 使用方式

1. 创建 Telegram 群
2. 拉入多个 Bot
3. @BossBot 发任务
4. 观察各 Agent 在群里讨论

## 工作原理

1. Boss Agent 用 `sessions_send` 给子 Agent 发任务
2. 子 Agent 完成任务后回复
3. 插件监听 `agent_end` 事件
4. 检测到是 `sessions_send` 来的任务
5. 自动将回复发到来源群

## 注意事项

- 需要 OpenClaw 内置的 announce 机制配合
- 子 Agent 的结果会同时：返回给 Boss + 发到群里
- 插件不会影响正常的用户对话

## 作者

OpenClaw 社区
