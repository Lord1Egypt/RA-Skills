# Odoo 19 项目 / Project 模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/project/`
> 文件：`models/project_project.py`、`models/project_task.py`（CLOSED_STATES 在文件头部）、`models/project_task_type.py`、`models/project_project_stage.py`、`models/project_milestone.py`；工时字段来自 `hr_timesheet/`，Gantt 字段来自 `project_enterprise/`。

## ⚠️ 与旧版关键差异（务必注意）

1. 任务"分配工时"字段是 **`allocated_hours`**，**不是** 旧版 `planned_hours`。
2. 任务 `state` 用编号前缀 selection（`01_in_progress`/`1_done`…），不是 `draft/done`。
3. 任务负责人是 **`user_ids`（Many2many，多负责人）**，不是单选 `user_id`。
4. `read_group` 已标注 **Deprecated**，推荐 `formatted_read_group`（两者都能 RPC 调）。
5. `project.project.stage`（项目级阶段）受组 `project.group_project_stages` 控制，需开启"项目阶段"特性才可见。

## 1. project.project

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char, **required** | 项目名 |
| `user_id` | Many2one→res.users | 项目负责人（界面 "Project Manager"，默认当前用户） |
| `partner_id` | Many2one→res.partner | 客户 |
| `company_id` | Many2one→res.company | 公司（compute+store，可写） |
| `date_start` | Date | 开始日期 |
| `date` | Date | **到期/结束日期**（约束 `date >= date_start`） |
| `stage_id` | Many2one→**project.project.stage** | 项目阶段（受 `project.group_project_stages` 限制） |
| `privacy_visibility` | Selection, required, default=`portal` | 见下 |
| `description` | Html | 项目描述 |
| `label_tasks` | Char, default="Tasks" | 任务别名（translate） |
| `active` | Boolean, default=True | 归档标志（False=归档） |
| `task_count` / `open_task_count` / `closed_task_count` | Integer (compute) | 任务计数 |
| `task_ids` / `tasks` | One2many→project.task | 该项目任务 |
| `type_ids` | Many2many→project.task.type | 该项目启用的**任务看板阶段**集合 |
| `allow_timesheets` | Boolean | "Timesheets"（来自 hr_timesheet，需配 analytic account） |
| `tag_ids` | Many2many→project.tags | 标签 |

**`privacy_visibility` 真实值**（用 value 不用 label）：
```
('followers',     'Invited internal users')
('invited_users', 'Invited internal and portal users')
('employees',     'All internal users')
('portal',        'All internal users and invited portal users')   # 默认
```

**编辑项目常改**：`name`/`user_id`/`partner_id`/`date_start`/`date`/`stage_id`/`privacy_visibility`/`description`/`tag_ids`/`active`/`allow_timesheets`。

## 2. project.task

`_order = "priority desc, sequence, date_deadline asc, id desc"`

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char, **required** | 任务标题 |
| `project_id` | Many2one→project.project | 所属项目（为空=私有任务/待办） |
| `stage_id` | Many2one→**project.task.type** | 看板阶段（`domain=[('project_ids','=',project_id)]`） |
| `user_ids` | **Many2many**→res.users | **负责人/Assignees（多人）**，`domain=[('share','=',False),('active','=',True)]` |
| `date_deadline` | **Datetime** | 截止时间（不是 Date） |
| `state` | Selection, required, default=`01_in_progress` | 状态（store+inverse，**可直接写**） |
| `priority` | Selection, default=`0` | `'0'`普通/`'1'`中/`'2'`高/`'3'`紧急 |
| `parent_id` / `child_ids` | Many2one / One2many→project.task | 父/子任务 |
| `tag_ids` | Many2many→project.tags | 标签 |
| `description` | Html | 描述 |
| `partner_id` | Many2one→res.partner | 客户（compute+store，可写） |
| `milestone_id` | Many2one→project.milestone | 里程碑（`domain=[('project_id','=',project_id)]`） |
| `allocated_hours` | **Float** | **分配工时**（"Allocated Time"，取代 planned_hours） |
| `active` | Boolean | 归档标志 |
| `depend_on_ids` / `dependent_ids` | Many2many→project.task | 任务依赖 |

**`state` 真实值**：`01_in_progress`(默认) / `02_changes_requested` / `03_approved` / `1_done` / `1_canceled` / `04_waiting_normal`。`is_closed` 为真 ⇔ state ∈ {`1_done`,`1_canceled`}。

**工时类字段（hr_timesheet，compute 只读）**：`effective_hours`/`remaining_hours`/`total_hours_spent`/`progress`/`timesheet_ids`。
**Gantt 字段（project_enterprise）**：`planned_date_begin`、`planned_date_start`。

> 写任务注意：`stage_id` 必须属于该任务的 `project_id`（域约束）；`user_ids` 是 m2m，用 `[(6,0,[ids])]`。

## 3. project.task.type（任务看板阶段）

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char, required, translate | 阶段名 |
| `sequence` | Integer | 看板列顺序 |
| `project_ids` | Many2many→project.project | **该阶段所属项目集合**（一个阶段可被多项目共享） |
| `fold` | Boolean | 看板折叠（通常=完成列） |
| `user_id` | Many2one→res.users | 阶段属主（设了 project_ids 会清空，二者互斥；个人阶段才有 user_id） |

**关联机制**：m2m `project_ids` ↔ 项目 `type_ids`。一个 task.type 出现在某项目看板 ⇔ 项目 id ∈ task.type.project_ids。
**移动任务到某阶段** = `task.write({'stage_id': type_id})`，前提目标 type 的 project_ids 含该任务的 project_id。

> 区分两个"阶段"模型：`project.task.type` = **任务**看板阶段；`project.project.stage` = **项目**自身阶段（§1 的 stage_id）。

## 4. XML-RPC 真实示例

```python
def call(model, method, *args, **kw): return models.execute_kw(db, uid, pw, model, method, list(args), kw)

# ① 新建项目
pid = call('project.project', 'create', [{
    'name': '辉火云官网改版', 'user_id': uid, 'partner_id': 12,
    'date_start': '2026-06-10', 'date': '2026-08-31',
    'privacy_visibility': 'employees', 'description': '<p>官网二期</p>',
}])

# ② 在项目下建任务（user_ids 是 m2m！allocated_hours 不是 planned_hours！）
tid = call('project.task', 'create', [{
    'name': '完成首页设计稿', 'project_id': pid,
    'user_ids': [(6, 0, [uid])], 'priority': '2',
    'date_deadline': '2026-06-20 18:00:00', 'allocated_hours': 8.0,
}])

# ③ 列项目任务并按 stage 分组
groups = call('project.task', 'formatted_read_group',
    [['project_id','=',pid]], ['stage_id'], ['__count','allocated_hours:sum'])
# 兼容旧版：call('project.task','read_group',[['project_id','=',pid]],['allocated_hours:sum'],['stage_id'])

# ④ 编辑项目 / 移动任务到 Done + 完成
call('project.project', 'write', [pid], {'user_id': 7})
done = call('project.task.type', 'search', [['name','=','Done'],['project_ids','=',pid]], {'limit':1})
if done: call('project.task','write',[tid],{'stage_id':done[0],'state':'1_done'})

# 归档项目
call('project.project', 'write', [pid], {'active': False})
```

## 避坑清单

1. 任务负责人 = `user_ids`(m2m)，写 `[(6,0,[ids])]`；不存在单数 `user_id`（项目才有 user_id=负责人）。
2. 分配工时 = `allocated_hours`(Float)，**绝不写 `planned_hours`**。
3. `state` 用编号前缀字符串，`priority` 用 `'0'..'3'` 字符串。
4. `date_deadline` 是 **Datetime**（UTC）。
5. `stage_id`(任务) 受 `domain=[('project_ids','=',project_id)]`：目标 type 必须属该任务项目。
6. 项目 `stage_id` 指 project.project.stage，带 `groups="project.group_project_stages"`，账号无该组读写受限，需先启用"项目阶段"特性。
7. 归档 `active=False`；查归档记录带 `context={'active_test': False}`。
8. `read_group` 已 Deprecated，新代码用 `formatted_read_group(domain, groupby, aggregates, ...)`，计数聚合名 `__count`，聚合写 `'field:agg'`。
9. `allow_timesheets` 及工时统计字段来自 `hr_timesheet`，需项目配 analytic account。
10. `privacy_visibility` 默认 `portal`，用 value 字符串别用 label。
