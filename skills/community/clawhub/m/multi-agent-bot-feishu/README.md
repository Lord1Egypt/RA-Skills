# Multi-Agent-Bot

在 OpenClaw 中创建新的 Agent 并绑定到飞书机器人，实现多机器人多 Agent 架构。

## 功能

- 为不同飞书群聊配置专属 Agent
- 实现多机器人消息路由
- 分离不同业务线的对话记忆
- 隔离不同群聊的访问权限

## 使用方法

### 1. 安装

```bash
clawhub install multi-agent-bot
```

### 2. 配置

编辑 `~/.openclaw/openclaw.json`，参考 `references/config-template.json` 模板添加：

- `agents.list` - 新增 Agent 定义
- `channels.feishu.accounts` - 新增飞书机器人
- `bindings` - 绑定路由规则

### 3. 创建工作空间

```bash
mkdir ~/.openclaw/workspace-名称
```

### 4. 重启

```bash
openclaw gateway restart
```

## 快速参考

| 配置项 | 说明 |
|--------|------|
| `agents.list[].id` | Agent 唯一标识 |
| `agents.list[].workspace` | 独立工作空间路径 |
| `accounts.*.appId` | 飞书机器人 App ID |
| `accounts.*.appSecret` | 飞书机器人 App Secret |
| `bindings[].agentId` | 目标 Agent ID |
| `bindings[].match.accountId` | 匹配的账户 ID |

## 路由优先级

1. 精确匹配（特定用户/群）
2. 线程继承
3. 账户匹配
4. 渠道匹配
5. 默认 Agent

## 权限策略

- `open` - 允许所有人
- `allowlist` - 仅允许列表内用户
- `denylist` - 禁止列表内用户

## 相关文档

- [飞书多机器人配置指南](https://docs.openclaw.ai/docs/feishu/multiple-bots)
- [OpenClaw 官方文档](https://docs.openclaw.ai)

## 发布日志

### 1.0.0

- 初始版本
- 支持创建新 Agent 并绑定飞书机器人
- 提供完整配置模板
