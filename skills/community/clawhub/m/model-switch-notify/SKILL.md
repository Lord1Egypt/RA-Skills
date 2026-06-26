---
name: model-switch-notify
description: 模型切换通知。当agent使用的模型发生变化时，第一时间通知当前会话用户。支持心跳检测机制，消息中断时下次会话自动通知。使用 SQLite 存储。
version: 3.0.0
author: OpenClaw
triggers:
  - on_session_start
  - on_heartbeat
  - on_model_change
  - on_user_query
---

# 模型切换通知 Skill v3.0

## 功能概述

自动检测模型切换并通知用户：
- 记录每个 agent 上次使用的模型（SQLite 存储）
- 心跳检测：每次会话回复时自动检查
- 消息中断处理：下次会话第一时间通知
- 模型变化时推送通知到当前会话

## 核心特性

### 1. 心跳检测机制

每次会话回复时执行心跳检测：
1. 检查是否有待发送通知（上次中断时）
2. 检查模型是否变化
3. 更新心跳时间戳

### 2. 消息中断处理

如果通知发送失败/中断：
1. 保存待发送通知到数据库
2. 下次会话第一时间发送
3. 发送后自动清除

### 3. SQLite 存储

只使用 SQLite 数据库存储：
- 路径：`~/.openclaw/data/model-switch.db`
- 支持 pending_notify 字段记录中断通知

## 使用方法

### 命令行工具

```bash
# 心跳检测（每次会话回复时调用）
python3 check_model.py check \
  --agent "coder" \
  --current-model "ollama/qwen3.5-code" \
  --channel "qqbot" \
  --session "qqbot:c2c:xxx"

# 更新心跳
python3 check_model.py heartbeat \
  --agent "coder" \
  --current-model "ollama/qwen3.5-code"

# 设置中断通知
python3 check_model.py interrupt \
  --agent "coder" \
  --model "ollama/qwen3.5-code" \
  --message "老板，模型已切换，当前使用：ollama/qwen3.5-code"

# 获取当前状态
python3 check_model.py get --agent "coder"

# 列出所有 agent
python3 check_model.py list

# 重置状态
python3 check_model.py reset --agent "coder"
```

### 心跳检测返回值

```json
{
  "changed": true,
  "previousModel": "ollama/glm-5:cloud",
  "currentModel": "ollama/qwen3.5-code",
  "shouldNotify": true,
  "notifyMessage": "老板，模型已切换，当前使用：ollama/qwen3.5-code",
  "firstTime": false,
  "pendingNotify": false,
  "pendingMessage": null
}
```

### 参数获取方式

| 参数 | 来源 | 示例 |
|------|------|------|
| agentId | Runtime `agent=` | `coder` |
| currentModel | Runtime `model=` | `ollama/qwen3.5-code` |
| channel | Inbound Context | `qqbot` |
| sessionId | Inbound Context `chat_id` | `qqbot:c2c:xxx` |

## 数据库结构

```sql
CREATE TABLE model_states (
  agent_id TEXT PRIMARY KEY,
  last_model TEXT NOT NULL,
  last_notify TIMESTAMP,
  last_heartbeat TIMESTAMP,
  channel TEXT,
  session TEXT,
  pending_notify INTEGER DEFAULT 0,
  pending_message TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 执行流程

### 正常流程

```
用户消息到达
    ↓
解析 Runtime 获取 currentModel
    ↓
调用 check_model.py check
    ↓
检查 pending_notify（上次中断？）
    ↓
检查模型是否变化
    ↓
如果 shouldNotify=true → 返回通知消息
    ↓
Agent 在回复中附加通知
    ↓
正常回复用户
```

### 中断处理流程

```
发送通知失败/中断
    ↓
调用 check_model.py interrupt
    ↓
保存 pending_notify=1, pending_message
    ↓
下次会话开始
    ↓
check 检测到 pending_notify
    ↓
返回 pending_message 作为通知
    ↓
发送后清除 pending_notify
```

## 通知模板

### 首次使用
```
当前使用模型：{currentModel}
```

### 模型切换
```
老板，模型已切换，当前使用：{currentModel}
```

### 中断通知恢复
```
[上次未发送] 老板，模型已切换，当前使用：{currentModel}
```

## 集成指南

### 在 Agent 中集成

每次会话回复前执行：

```python
import subprocess
import json

def check_model_switch(agent_id, current_model, channel, session):
    result = subprocess.run([
        "python3", 
        "~/.openclaw/skills/model-switch-notify/scripts/check_model.py",
        "check",
        "--agent", agent_id,
        "--current-model", current_model,
        "--channel", channel,
        "--session", session
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)

# 在回复前检查
result = check_model_switch("coder", "ollama/qwen3.5-code", "qqbot", "qqbot:c2c:xxx")

if result["shouldNotify"]:
    notify_msg = result["notifyMessage"]
    # 在回复中附加通知
```

## 目录结构

```
~/.openclaw/skills/model-switch-notify/
├── SKILL.md              # 本文档
├── README.md             # 使用说明
└── scripts/
    └── check_model.py    # 检查脚本（SQLite 存储）

~/.openclaw/data/
└── model-switch.db       # SQLite 数据库
```

## 注意事项

1. **心跳检测**：每次会话回复时调用 `check` 命令
2. **中断处理**：消息发送失败时调用 `interrupt` 命令
3. **存储方式**：只使用 SQLite，不再支持 JSON 文件
4. **跨会话**：模型状态和中断通知跨会话持久化

## 更新日志

- **v3.0.0** (2026-03-16): 移除 JSON 存储，只使用 SQLite；添加心跳检测和中断通知机制
- **v2.0.0** (2026-03-16): 添加 SQLite 支持、详细集成指南
- **v1.0.0** (2026-03-13): 初始版本