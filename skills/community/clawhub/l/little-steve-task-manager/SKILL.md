---
name: little-steve-task-manager
version: 0.1.7
description: Little Steve Task Manager: a lightweight IM-native task system for quick task operations in chat, with daily summaries and auto status updates. / 小史任务管理器：面向 IM 场景的轻量任务系统，可在聊天中快速管理任务，并支持每日汇总与自动状态更新。
---

# Little Steve Task Manager

A lightweight task manager for chat workflows: add, list, update status, reprioritize, and complete tasks quickly.

## Data Files

- `skills/little-steve-task-manager/data/tasks.json`
- `skills/little-steve-task-manager/data/settings.json`

## Agent Command Conventions

1. Add task
```bash
bash {baseDir}/scripts/task.sh add --title "<Title>" --priority P2 --due "2026-03-05" --tags "ops,finance"
```

2. List tasks
```bash
bash {baseDir}/scripts/task.sh list --status open
```

3. Update status
```bash
bash {baseDir}/scripts/task.sh update --id <id> --status doing
```

4. Change priority
```bash
bash {baseDir}/scripts/task.sh update --id <id> --priority P1
```

5. Mark done
```bash
bash {baseDir}/scripts/task.sh done --id <id>
```

## Status Enum

- `open` — todo
- `doing` — in progress
- `blocked` — blocked
- `done` — completed
- `cancelled` — cancelled

## Priority

- `P0` > `P1` > `P2` > `P3`

## IM Output Format

- Sort order: priority → due date → created time
- Per item format: `[status][priority] #ID title (due: date) tags`

---

# 小史任务管理器

面向聊天工作流的轻量任务管理器：快速新增、列表、更新状态、调整优先级与完成任务。

## 数据文件

- `skills/little-steve-task-manager/data/tasks.json`
- `skills/little-steve-task-manager/data/settings.json`

## Agent 执行约定

1. 新增任务
```bash
bash {baseDir}/scripts/task.sh add --title "<标题>" --priority P2 --due "2026-03-05" --tags "ops,finance"
```

2. 查看任务
```bash
bash {baseDir}/scripts/task.sh list --status open
```

3. 更新状态
```bash
bash {baseDir}/scripts/task.sh update --id <id> --status doing
```

4. 调整优先级
```bash
bash {baseDir}/scripts/task.sh update --id <id> --priority P1
```

5. 完成任务
```bash
bash {baseDir}/scripts/task.sh done --id <id>
```

## 状态枚举

- `open` — 待办
- `doing` — 进行中
- `blocked` — 阻塞
- `done` — 已完成
- `cancelled` — 已取消

## 优先级

- `P0` > `P1` > `P2` > `P3`

## IM 输出规范

- 列表排序：优先级 → 截止日 → 创建时间
- 每条显示：`[状态][优先级] #ID 标题 (due: 日期) tags`
