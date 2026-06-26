# 模型切换通知 Skill v3.0

## 功能

当 agent 使用的模型发生变化时，第一时间通知当前会话用户。

**核心特性：**
- 心跳检测：每次会话回复时自动检查
- 中断处理：消息中断时下次会话第一时间通知
- SQLite 存储：统一数据库管理

## 存储

只使用 SQLite 数据库：
- 路径：`~/.openclaw/data/model-switch.db`
- 支持心跳时间戳
- 支持 pending_notify 待发送通知

## 快速使用

### 心跳检测（推荐）

```bash
python3 ~/.openclaw/skills/model-switch-notify/scripts/check_model.py check \
  --agent "coder" \
  --current-model "ollama/qwen3.5-code" \
  --channel "qqbot" \
  --session "qqbot:c2c:xxx"
```

### 设置中断通知

```bash
# 当通知发送失败/中断时调用
python3 check_model.py interrupt \
  --agent "coder" \
  --model "ollama/qwen3.5-code" \
  --message "老板，模型已切换，当前使用：ollama/qwen3.5-code"
```

### 其他命令

```bash
# 更新心跳
python3 check_model.py heartbeat --agent "coder" --current-model "ollama/qwen3.5-code"

# 获取当前状态
python3 check_model.py get --agent "coder"

# 列出所有 agent
python3 check_model.py list

# 重置状态
python3 check_model.py reset --agent "coder"
```

## 返回示例

### 首次使用
```json
{
  "changed": true,
  "previousModel": null,
  "currentModel": "ollama/qwen3.5-code",
  "shouldNotify": true,
  "notifyMessage": "当前使用模型：ollama/qwen3.5-code",
  "firstTime": true,
  "pendingNotify": false,
  "pendingMessage": null
}
```

### 模型切换
```json
{
  "changed": true,
  "previousModel": "ollama/qwen3.5-code",
  "currentModel": "ollama/glm-5:cloud",
  "shouldNotify": true,
  "notifyMessage": "老板，模型已切换，当前使用：ollama/glm-5:cloud",
  "firstTime": false,
  "pendingNotify": false,
  "pendingMessage": null
}
```

### 有待发送通知（中断恢复）
```json
{
  "changed": false,
  "previousModel": "ollama/qwen3.5-code",
  "currentModel": "ollama/qwen3.5-code",
  "shouldNotify": true,
  "notifyMessage": "老板，模型已切换，当前使用：ollama/qwen3.5-code",
  "firstTime": false,
  "pendingNotify": true,
  "pendingMessage": "老板，模型已切换，当前使用：ollama/qwen3.5-code"
}
```

### 无变化
```json
{
  "changed": false,
  "previousModel": "ollama/qwen3.5-code",
  "currentModel": "ollama/qwen3.5-code",
  "shouldNotify": false,
  "notifyMessage": "",
  "firstTime": false,
  "pendingNotify": false,
  "pendingMessage": null
}
```

## 执行时机

### 正常流程
```
用户消息到达
    ↓
解析 Runtime 获取 currentModel
    ↓
调用 check 命令
    ↓
检查 pending_notify（上次中断？）
    ↓
检查模型是否变化
    ↓
如果 shouldNotify=true → 在回复中附加通知
    ↓
正常回复用户
```

### 中断处理
```
发送通知失败/中断
    ↓
调用 interrupt 命令
    ↓
保存 pending_notify=1
    ↓
下次会话 check 检测到
    ↓
返回 pending_message
    ↓
发送后自动清除
```

## 参数来源

| 参数 | 来源 | 示例值 |
|------|------|--------|
| agent | Runtime `agent=` | `coder` |
| currentModel | Runtime `model=` | `ollama/qwen3.5-code` |
| channel | Inbound Context | `qqbot` |
| session | Inbound Context `chat_id` | `qqbot:c2c:xxx` |

## 数据库表结构

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

## 目录结构

```
~/.openclaw/skills/model-switch-notify/
├── SKILL.md              # 技能定义文档
├── README.md             # 本文档
└── scripts/
    └── check_model.py    # 检查脚本（SQLite）

~/.openclaw/data/
└── model-switch.db       # SQLite 数据库
```

---

版本: 3.0.0
更新: 2026-03-16