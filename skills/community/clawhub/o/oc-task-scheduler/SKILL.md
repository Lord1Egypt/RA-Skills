---
name: task-scheduler
description: Task queue management with WebSocket real-time updates. Schedule, monitor, and control background tasks. Supports immediate, scheduled, and recurring tasks with priority levels.
tools:
  - read
  - write
  - exec
  - cron
---

# Task Scheduler - 任务调度器

基于 Bytebot Task System 实现的任务队列管理，支持 WebSocket 实时推送。

**Version**: 1.0.0  
**Features**: 任务队列、定时调度、优先级管理、WebSocket 推送、状态追踪

## Purpose

让 OpenClaw 能够:
- 管理后台任务队列
- 定时执行任务
- 实时推送任务状态更新
- 追踪任务执行历史
- 优先级调度

## Quick Start

### 1. 创建任务

```bash
# 立即执行任务
python3 scripts/main.py create --description "Analyze codebase" --priority high

# 定时任务
python3 scripts/main.py create --description "Daily backup" --schedule "0 2 * * *"

# 带参数的任务
python3 scripts/main.py create --description "Process file" --params '{"path": "/tmp/data.csv"}'
```

### 2. 管理任务

```bash
# 列出所有任务
python3 scripts/main.py list

# 查看任务详情
python3 scripts/main.py get --id task_123

# 取消任务
python3 scripts/main.py cancel --id task_123

# 重新运行失败任务
python3 scripts/main.py retry --id task_123
```

### 3. 监控任务

```bash
# 启动调度器
python3 scripts/main.py daemon --ws-port 8080

# WebSocket 连接接收实时更新
wscat -c ws://localhost:8080/ws
```

## Python API

```python
from task_scheduler import TaskScheduler, TaskPriority

# 初始化调度器
scheduler = TaskScheduler()

# 创建任务
task = scheduler.create_task(
    description="Generate report",
    priority=TaskPriority.HIGH,
    handler=generate_report
)

# 定时任务
scheduler.schedule_task(
    description="Daily sync",
    cron="0 2 * * *",
    handler=daily_sync
)

# 监听状态变化
@scheduler.on_status_change
def on_status(task_id, old_status, new_status):
    print(f"Task {task_id}: {old_status} -> {new_status}")

# 启动调度
scheduler.start()
```

## Task Lifecycle

```
CREATED -> PENDING -> RUNNING -> COMPLETED
                    -> FAILED -> RETRYING
                    -> CANCELLED
```

## Task Priority

| Priority | Value | Description |
|----------|-------|-------------|
| LOW      | 1     | 后台任务    |
| MEDIUM   | 2     | 普通任务    |
| HIGH     | 3     | 优先处理    |
| URGENT   | 4     | 立即执行    |

## CLI Reference

### Task Management

```bash
# 创建任务
python3 scripts/main.py create \
  --description "Task description" \
  --type immediate \
  --priority high \
  --params '{"key": "value"}'

# 创建定时任务
python3 scripts/main.py schedule \
  --description "Daily task" \
  --cron "0 9 * * *" \
  --timezone Asia/Shanghai

# 列出任务
python3 scripts/main.py list \
  --status running \
  --limit 10

# 获取详情
python3 scripts/main.py get --id <task_id>

# 更新任务
python3 scripts/main.py update --id <task_id> --priority urgent

# 取消任务
python3 scripts/main.py cancel --id <task_id>

# 删除任务
python3 scripts/main.py delete --id <task_id>
```

### Scheduler Daemon

```bash
# 启动调度器
python3 scripts/main.py daemon \
  --concurrency 4 \
  --ws-port 8080 \
  --persist-tasks

# 状态
python3 scripts/main.py status

# 停止
python3 scripts/main.py stop
```

## WebSocket Protocol

连接: `ws://host:port/ws`

### 消息格式

```json
// 任务创建
{
  "event": "task.created",
  "data": {
    "id": "task_123",
    "description": "...",
    "status": "pending",
    "priority": "high"
  }
}

// 状态更新
{
  "event": "task.status_changed",
  "data": {
    "id": "task_123",
    "old_status": "pending",
    "new_status": "running",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}

// 任务完成
{
  "event": "task.completed",
  "data": {
    "id": "task_123",
    "result": {...},
    "duration_ms": 5000
  }
}
```

## Configuration

```yaml
# config.yaml
scheduler:
  concurrency: 4
  retry_attempts: 3
  retry_delay: 5
  
websocket:
  host: 0.0.0.0
  port: 8080
  
persistence:
  enabled: true
  path: ./tasks.db
  
logging:
  level: INFO
  file: ./scheduler.log
```

## Architecture

```
task-scheduler/
├── SKILL.md
├── requirements.txt
├── lib/
│   ├── __init__.py
│   ├── scheduler.py         # TaskScheduler 核心
│   ├── task.py              # Task 类定义
│   ├── queue.py             # 任务队列
│   ├── worker.py            # 工作进程
│   ├── websocket.py         # WebSocket 服务
│   └── persistence.py       # 持久化存储
├── scripts/
│   └── main.py              # CLI 入口
└── examples/
    ├── basic_usage.py
    └── websocket_client.py
```

## Integration with OpenClaw

```python
from task_scheduler import TaskScheduler

class MySkill:
    def __init__(self):
        self.scheduler = TaskScheduler()
        
    def run_long_task(self, description):
        task = self.scheduler.create_task(
            description=description,
            handler=self._process
        )
        return task.id
    
    def get_task_status(self, task_id):
        return self.scheduler.get_task(task_id).status
```

## Use Cases

1. **后台任务** - 代码分析、文档生成
2. **定时任务** - 每日报告、定期备份
3. **工作流** - 多步骤任务链
4. **监控** - 实时查看任务进度

## License

MIT License - 基于 Bytebot Task System 实现
