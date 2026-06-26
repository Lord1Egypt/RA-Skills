---
name: multi-agent-deploy
description: 快速部署新的 assistant agent。当用户需要新增 agent 时自动创建，编号递增，沿用现有 workspace 和 agentDir 结构。使用场景：「新增一个 agent」、「创建 assistant2」、「加一个日常助手」等请求。
---

# Multi-Agent Deploy 技能

自动创建新的 assistant agent，编号递增，沿用现有结构。

## 触发条件

当用户表达以下意图时使用：
- 「新增一个 agent」
- 「创建 assistant2」
- 「加一个日常助手」
- 「我需要第 X 个 assistant」
- 「再部署一个 agent」

## 使用方式

### 快速部署（默认）

直接运行部署脚本，自动检测下一个可用编号：

```bash
python3 /home/admin/.openclaw/workspace/skills/multi-agent-deploy/scripts/deploy-agent.py
```

脚本会自动：
1. 检测当前最大的 assistant 编号
2. 创建 `workspace-assistantX` 工作空间（复制 SOUL.md、AGENTS.md、USER.md）
3. 创建 `agents/assistantX/agent` 目录
4. 更新 `~/.openclaw/openclaw.json` 添加新 agent 配置

### 部署后操作

1. **重启 Gateway** 让新配置生效：
   ```bash
   openclaw gateway restart
   ```

2. **可选：配置绑定** - 如需将新 agent 绑定到特定 channel，编辑 `~/.openclaw/openclaw.json` 的 `bindings` 字段

## 目录结构

```
/home/admin/.openclaw/
├── agents/
│   ├── assistant/          # 原始模板
│   │   └── agent/
│   └── assistantX/         # 新创建的 agent
│       └── agent/
├── workspace-assistant/    # 模板工作空间
├── workspace-assistantX/   # 新创建的工作空间
│   ├── SOUL.md
│   ├── AGENTS.md
│   └── USER.md
└── openclaw.json           # 自动更新配置
```

## 配置示例

新增的 agent 配置格式：

```json
{
  "id": "assistant2",
  "name": "日常助手 2",
  "workspace": "/home/admin/.openclaw/workspace-assistant2",
  "agentDir": "/home/admin/.openclaw/agents/assistant2/agent",
  "model": "dashscope/qwen3.5-plus"
}
```

## 自定义

如需自定义新 agent 的配置（名称、模型、绑定等），在运行脚本前说明：
- 「创建一个 research agent，用 qwen3-max 模型」
- 「新增 assistant3，绑定到 telegram」

否则默认沿用现有 assistant 的配置。

## 故障排查

**问题：编号冲突**
- 脚本会自动检测最大编号，不会覆盖现有 agent

**问题：配置未生效**
- 运行 `openclaw gateway restart` 重启 Gateway

**问题：工作空间已存在**
- 脚本会提示警告，不会覆盖现有文件
