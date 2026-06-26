---
name: goal-task
description: "为目标创建 cron 任务。agent 收到消息后处理目标，完成后主动删除该 cron。适用于延迟处理、定时提醒等场景。"
metadata: {"openclaw":{"emoji":"🎯","requires":{"anyBins":[]}}}
---

# goal-task

为实现特定目标而创建的 cron 任务。agent 收到消息后处理目标，完成后主动删除 job。

## 核心理念

- **以目标为导向**：创建时附带任务说明，agent 收到后明确知道要做什么
- **完成后自删除**：任务完成后 agent 必须主动调用 `delete_goal_task` 删除 job，否则 cron 永久残留
- **区别于 cron 参数**：cron 参数适合定时定点重复执行，goal-task 适合目标驱动的一次性任务

## 使用流程

### 1. 设置环境变量

```bash
export AGENT_SESSION_KEY="agent:<agentId>:feishu:group:<feishu_group_id>"
```

sessionKey 格式：`agent:<agentId>:feishu:group:<groupId>`
- `<agentId>` — 当前 agent 的 ID（如 `main`、`qa`、`producer`）
- `<feishu_group_id>` — 飞书群 ID（从 MEMORY.md 获取）

### 2. 创建 goal task

```bash
source goal-task.sh
goal_task "<delay_minutes>" "<任务目标描述>"
```

**返回值**：jobId（UUID），供后续删除使用。

### 3. 任务执行

agent 收到 cron 注入的 agentTurn 消息，按描述处理目标。

### 4. 完成后删除

```bash
delete_goal_task "<jobId>"
```

**重要**：目标完成后必须删除 job。cron 本身不会自动删除，需要 agent 主动处理。

## 示例

### 持续跟进任务

```bash
# 持续跟进某个目标，定期提醒直到完成，完成后删除 cron
export AGENT_SESSION_KEY="agent:main:feishu:group:oc_xxxxxxxxxxxxxxxx"
source goal-task.sh

# 创建 goal task，agent 会收到“跟进 M2 美工进度”的消息
# agent 处理后（如果完成）调用 delete_goal_task 清理 cron
# 如果未完成，agent 可以创建新的 goal task 继续提醒
job_id=$(goal_task "120" "跟进 M2 美工进度，所有素材完成后删除 cron")
```

### 任务完成后删除

```bash
delete_goal_task "fa5e5455-dd15-49e5-9d67-e63ac0ee6559"
```

## 错误处理

| 场景 | 表现 |
|------|------|
| `AGENT_SESSION_KEY` 未设置 | `ERROR: AGENT_SESSION_KEY not set` |
| 创建失败 | `ERROR: failed to create goal-task` |
| 删除失败（job 不存在） | 返回 `{"ok":true,"removed":false}` |
| 删除成功 | 返回 `{"ok":true,"removed":true}` |

## 注意事项

1. **sessionTarget 格式**：`session:agent:<agentId>:feishu:group:<groupId>`
2. **gateway token**：从 `~/.openclaw/openclaw.json` 读取，脚本运行时自动获取
3. **job 手动删除**：这是设计选择——agent 主动删除确保任务确实完成后才清理，不会误删未完成的任务