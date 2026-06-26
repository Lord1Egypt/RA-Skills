# Personal Assistant 数据模型

数据库文件：`~/.hermes/data/personal_assistant/tasks.db`（SQLite）

---

## 表概览

| 表名 | 用途 | 记录类型 |
|------|------|----------|
| `tasks` | 核心任务表 | 用户任务 |
| `milestones` | 任务里程碑 | 任务子项 |
| `progress_logs` | 进展日志 | 操作记录 |
| `recurring_tasks` | 周期任务模板 | 配置模板 |
| `okr_items` | OKR 本地缓存 | 目标数据 |
| `reminder_log` | 提醒推送记录 | 系统日志 |

---

## 1. tasks — 核心任务表

存储所有工作任务，是整个系统的核心。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 自增主键 |
| `title` | TEXT NOT NULL | 任务标题 |
| `description` | TEXT | 详细描述（Markdown） |
| `category` | TEXT | 分类标签（如 "开发"、"会议"） |
| `status` | TEXT | 状态：`todo` / `in_progress` / `blocked` / `done` / `cancelled` |
| `priority` | INTEGER | 优先级：1=最高, 5=最低 |
| `deadline` | TEXT | 截止时间，ISO 8601 格式 |
| `start_time` | TEXT | 计划开始时间 |
| `estimated_hours` | REAL | 预估耗时（小时） |
| `actual_hours` | REAL | 实际耗时（小时） |
| `progress` | INTEGER | 完成百分比 (0-100) |
| `progress_note` | TEXT | 最新进展简述 |
| `parent_task_id` | INTEGER FK | 父任务 ID（子任务拆分） |
| `okr_id` | INTEGER FK | 关联 OKR ID（→ `okr_items.id`） |
| `source_type` | TEXT | 来源：`manual` / `recurring` / `okr` / `import` |
| `recurring_id` | INTEGER FK | 关联周期任务 ID（→ `recurring_tasks.id`） |
| `extra` | TEXT | JSON 扩展字段 |
| `created_at` | TEXT | 创建时间（本地时间） |
| `updated_at` | TEXT | 更新时间（本地时间） |

**索引：** `status`, `deadline`, `priority`, `category`, `parent_task_id`, `okr_id`

---

## 2. milestones — 里程碑表

关联到任务的关键子目标。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 自增主键 |
| `task_id` | INTEGER FK | 关联任务 ID（CASCADE 删除） |
| `title` | TEXT NOT NULL | 里程碑名称 |
| `status` | TEXT | 状态：`pending` / `completed` |
| `due_date` | TEXT | 预期完成时间 |
| `completed_at` | TEXT | 实际完成时间 |
| `sort_order` | INTEGER | 排序权重 |
| `created_at` | TEXT | 创建时间 |

**索引：** `task_id`

---

## 3. progress_logs — 进展日志表

记录每次进展更新的完整历史。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 自增主键 |
| `task_id` | INTEGER FK | 关联任务 ID（CASCADE 删除） |
| `content` | TEXT NOT NULL | 进展内容（Markdown） |
| `progress_before` | INTEGER | 更新前进度 % |
| `progress_after` | INTEGER | 更新后进度 % |
| `hours_spent` | REAL | 本次投入小时数 |
| `logged_at` | TEXT | 记录时间（本地时间） |

**索引：** `task_id`, `logged_at`

---

## 4. recurring_tasks — 周期任务模板表

定义自动生成任务实例的规则。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 自增主键 |
| `template_title` | TEXT NOT NULL | 任务标题模板 |
| `template_desc` | TEXT | 描述模板 |
| `category` | TEXT | 分类标签 |
| `priority` | INTEGER | 优先级（默认 3） |
| `estimated_hours` | REAL | 预估工时 |
| `recurrence_type` | TEXT | 周期类型：`daily` / `weekly` / `biweekly` / `monthly` / `custom` |
| `recurrence_rule` | TEXT | 自定义规则（类 iCal RRULE） |
| `enabled` | INTEGER | 启用状态：0=暂停, 1=启用 |
| `next_run_date` | TEXT NOT NULL | 下次生成实例的日期 |
| `last_run_date` | TEXT | 上次生成日期 |
| `advance_days` | INTEGER | 提前生成天数 |
| `extra` | TEXT | JSON 扩展字段 |
| `created_at` | TEXT | 创建时间 |
| `updated_at` | TEXT | 更新时间 |

---

## 5. okr_items — OKR 本地缓存表

从飞书文档同步或手动创建的 OKR 数据，采用 **Objective → Key Result → Initiative** 三层树形结构（通过 `parent_id` 自引用实现）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 自增主键 |
| `title` | TEXT NOT NULL | OKR 项标题 |
| `description` | TEXT | 详细描述（Markdown） |
| `parent_id` | INTEGER FK | 父级 OKR ID（自引用，实现 O→KR→Initiative 层级） |
| `obj_type` | TEXT NOT NULL | 类型：`objective` / `key_result` / `initiative` |
| `progress` | INTEGER | 进度百分比 (0-100) |
| `status` | TEXT NOT NULL | 状态：`active` / `completed` / `cancelled` |
| `start_date` | TEXT | 开始日期 |
| `end_date` | TEXT | 结束日期 |
| `weight` | REAL | 权重（默认 1.0） |
| `extra` | TEXT | JSON 扩展字段 |
| `source_doc_token` | TEXT | 飞书文档 token（同步来源标识） |
| `synced_at` | TEXT | 最后同步时间 |
| `created_at` | TEXT | 创建时间（本地时间） |
| `updated_at` | TEXT | 更新时间（本地时间） |

**索引：** `idx_okr_status`, `idx_okr_parent`, `idx_okr_source`

---

## 6. reminder_log — 提醒推送记录表

记录每次提醒推送，用于去重和审计。同一任务同一天同一类型只记录一次（UNIQUE 约束）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER PK | 自增主键 |
| `task_id` | INTEGER FK | 关联任务 ID（CASCADE 删除） |
| `reminder_type` | TEXT NOT NULL | 类型：`morning` / `afternoon` / `evening` / `deadline_alert` / `manual` |
| `reminder_date` | TEXT NOT NULL | 提醒日期（如 "2026-05-26"） |
| `sent_at` | TEXT NOT NULL | 发送时间（本地时间） |
| `message` | TEXT | 提醒消息内容 |

**约束：** `UNIQUE(task_id, reminder_type, reminder_date)`

---

## 关系概览

```
tasks ──1:N── milestones        (CASCADE 删除)
tasks ──1:N── progress_logs     (CASCADE 删除)
tasks ──N:1── okr_items         (SET NULL 删除)
tasks ──N:1── recurring_tasks   (SET NULL 删除)
tasks ──N:1── tasks             (自引用: parent_task_id, SET NULL)
tasks ──1:N── reminder_log      (CASCADE 删除)
```
