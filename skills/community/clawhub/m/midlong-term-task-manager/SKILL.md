# 中长期任务管理技能

## 技能说明

**名称：** midlong-term-task-manager  
**作用：** 管理 AI Agent 的中长期任务（几天到几个月），支持任务分解、进度跟踪、自动提醒

**与三层记忆系统的边界：**
- ✅ 任务数据存储在独立文件：`.tasks/tasks.json`
- ✅ 进度日志记录到：`.tasks/logs/YYYY-MM-DD.md`
- ❌ **不直接编辑 MEMORY.md**（由三层记忆技能自动压缩）

---

## 触发场景

1. **心跳检查时** - 自动 review 所有进行中的任务
2. **用户添加任务** - 登记新任务并分解
3. **任务状态变更** - 更新进度/延期/完成
4. **每日总结** - 生成任务进度报告

---

## 任务数据结构

```json
{
  "tasks": [
    {
      "id": "TSK-20260330-001",
      "name": "学习中长期任务管理",
      "description": "悠悠学习任务管理技能的开发",
      "type": "learning",
      "priority": "high",
      "status": "in_progress",
      "created_at": "2026-03-30T10:30:00+08:00",
      "due_date": "2026-04-06",
      "decomposed": [
        {
          "subtask": "设计数据结构",
          "status": "done",
          "due_date": "2026-03-30"
        },
        {
          "subtask": "编写 SKILL.md",
          "status": "in_progress",
          "due_date": "2026-03-30"
        },
        {
          "subtask": "创建心跳检查脚本",
          "status": "pending",
          "due_date": "2026-03-31"
        }
      ],
      "progress": 33,
      "last_updated": "2026-03-30T10:30:00+08:00",
      "blocked_by": null,
      "depends_on": [],
      "tags": ["skill-development", "self-improvement"]
    }
  ]
}
```

---

## 任务状态

| 状态 | 说明 | 心跳检查动作 |
|------|------|-------------|
| `pending` | 待开始 | 检查是否到达开始日期 |
| `in_progress` | 进行中 | 记录进度，检查是否延期 |
| `blocked` | 阻塞 | 提醒解除阻塞条件 |
| `completed` | 已完成 | 归档，生成总结 |
| `paused` | 暂停 | 记录暂停原因 |
| `cancelled` | 已取消 | 归档 |

---

## 使用方法

### 添加任务

```bash
# 命令格式
task_add <name> --due <YYYY-MM-DD> --priority <low|medium|high> --desc <description>

# 示例
task_add "学习具身智能" --due 2026-04-15 --priority high --desc "帮助智哥了解具身智能基础"
```

### 更新进度

```bash
# 命令格式
task_update <task_id> --progress <0-100> --status <status> --note <note>

# 示例
task_update TSK-20260330-001 --progress 50 --status in_progress --note "完成 SKILL.md"
```

### 查询任务

```bash
# 查看所有任务
task_list

# 查看进行中的任务
task_list --status in_progress

# 查看即将到期的任务（7 天内）
task_list --due-soon 7
```

### 删除任务

```bash
task_cancel <task_id> --reason <reason>
```

---

## 心跳检查集成

在 `HEARTBEAT.md` 中添加：

```markdown
### 【6】任务进度检查
- 运行 `~/.openclaw/skills/midlong-term-task-manager/scripts/task_check.sh`
- 检查所有 `in_progress` 任务
- 记录进度到 `.tasks/logs/YYYY-MM-DD.md`
- 如有延期风险，提醒悠悠
```

---

## Cron 配置

```bash
# 任务检查（心跳时运行，每 30 分钟）
# 在 HEARTBEAT.md 中调用脚本

# 每日总结（每天 20:00）
0 20 * * * ~/.openclaw/skills/midlong-term-task-manager/scripts/daily_summary.sh >> ~/.openclaw/workspace/.tasks/daily.log 2>&1

# 每周 review（每周一 09:00）
0 9 * * 1 ~/.openclaw/skills/midlong-term-task-manager/scripts/weekly_review.sh >> ~/.openclaw/workspace/.tasks/weekly.log 2>&1
```

---

## 与三层记忆系统集成

**正确做法：**
1. ✅ 任务进度日志 → `.tasks/logs/YYYY-MM-DD.md`
2. ✅ 任务完成总结 → `.learnings/LEARNINGS.md`
3. ✅ 由三层记忆技能自动压缩到 MEMORY.md

**错误做法：**
- ❌ 直接编辑 MEMORY.md
- ❌ 直接写入 `memory/YYYY-MM-DD.md`（这是三层记忆技能的 L2 存储）

---

## 文件结构

```
~/.openclaw/skills/midlong-term-task-manager/
├── SKILL.md              # 技能说明
└── scripts/
    ├── task_check.sh     # 心跳检查脚本
    ├── daily_summary.sh  # 每日总结脚本
    └── weekly_review.sh  # 每周 review 脚本

~/.openclaw/workspace/.tasks/
├── tasks.json            # 任务数据库
└── logs/
    └── YYYY-MM-DD.md     # 每日进度日志
```

---

## 最佳实践

1. **及时登记** - 接到任务立即记录，避免遗忘
2. **合理分解** - 长期任务分解为周/日计划
3. **定期 review** - 心跳时自动检查进度
4. **诚实记录** - 延期不隐瞒，及时调整计划
5. **完成总结** - 每个任务完成后记录学习心得

---

## 版本历史

- **v0.1.0** (2026-03-30) - 初始版本，基础功能
