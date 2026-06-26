---
name: hermes-comm
description: "WorkBuddy 与 Hermes 之间通过共享文件队列直接通信。触发词：发消息给hermes、收hermes消息、查看通信队列、双向通信"
version: 1.0.0
category: autonomous-ai-agents
---

# Hermes-WorkBuddy 通信桥

通过 `~/.hermes/shared/communication/queue.json` 共享文件队列，WorkBuddy 与 Hermes 直接双向通信。

## 核心文件

- 队列：`~/.hermes/shared/communication/queue.json`
- 历史：`~/.hermes/shared/communication/history.json`
- 技能：`~/.workbuddy/skills/hermes-communication-bridge/scripts/communication_queue.py`

## CLI 命令

```bash
# WorkBuddy → Hermes 发消息
python3 ~/.workbuddy/skills/hermes-communication-bridge/scripts/communication_queue.py send workbuddy hermes "内容"

# 收 Hermes → WorkBuddy 的消息
python3 ~/.workbuddy/skills/hermes-communication-bridge/scripts/communication_queue.py receive workbuddy

# 查看队列统计
python3 ~/.workbuddy/skills/hermes-communication-bridge/scripts/communication_queue.py stats

# 标记消息已处理
python3 ~/.workbuddy/skills/hermes-communication-bridge/scripts/communication_queue.py mark <msg_id> completed
```

## 消息格式

```json
{
  "id": "msg_<timestamp>_<sender>",
  "sender": "workbuddy|hermes",
  "receiver": "hermes|workbuddy",
  "type": "message|task|query|response|status|file|command|alert",
  "content": "消息内容",
  "priority": "low|normal|high|urgent",
  "status": "pending|processing|completed|failed"
}
```

## 类型说明

- `message`：普通文本消息
- `task`：任务请求（带元数据）
- `query`：查询请求
- `response`：响应
- `status`：状态更新
- `file`：文件传输
- `command`：系统命令
- `alert`：警报通知

## 工作流

1. **WorkBuddy 发消息**：`send workbuddy hermes "内容"`
2. **Hermes 读取**：通过 cron 或 auto_poller 轮询队列，发现 pending 消息
3. **Hermes 回复**：写 `hermes → workbuddy` 的 pending 消息
4. **WorkBuddy 读取**：`receive workbuddy`，处理消息
5. **标记完成**：`mark <msg_id> completed`
