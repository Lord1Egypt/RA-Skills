# Odoo 19 工时单 / Timesheets 模型与 API 速查

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/`
> 文件：`analytic/models/analytic_line.py`（基础字段）、`hr_timesheet/models/hr_timesheet.py`（timesheet 扩展 + create/write）、`timesheet_grid/models/account_analytic_line.py`（企业版 validated/timer）、`hr_timesheet/views/hr_timesheet_views.xml`（action domain 证明判定标准）。

## 1. 模型与「是工时单」判定

**模型名：`account.analytic.line`**（分析行）。不是独立模型——Odoo 把工时单做成"被打了 project 标记的分析行"。

- 基础：`analytic/models/analytic_line.py`（`_order='date desc, id desc'`）
- hr_timesheet 扩展加字段：`task_id`、`parent_task_id`、`project_id`、`employee_id`、`job_title`、`department_id`、`manager_id`、`milestone_id` 等；并**重写** `user_id`（compute 自 employee_id.user_id）。
- 企业版 timesheet_grid 再加：`validated`(Boolean)、`validated_status`(draft/validated)、`user_can_validate`、`display_timer`。

### 如何判定「一条记录是工时单」（关键）

**没有 `is_timesheet` 字段**（全代码库搜不到 `is_timesheet = fields.*`）。判定标准就是：

```
project_id != False
```

证据来自 Odoo 工时单 action：`domain = [('project_id', '!=', False)]`，`context = {'is_timesheet': 1, ...}`。`is_timesheet: 1` 只是 **context 标志**（控制默认值/视图），**不是可查询字段**，domain 里不能用。

> **写工具时**：domain 一律带 `('project_id', '!=', False)`，把普通分析行（费用/采购等）排除掉。

## 2. 工时单关键字段

| 字段 | 类型 | 含义 |
|---|---|---|
| `date` | Date (required, default today) | 工时日期 |
| `name` | Char (required) | 工时描述；空时存为 `'/'` |
| **`unit_amount`** | **Float** | **工时小时数**（基类 label 叫 "Quantity"）。**统计求和用它** |
| `amount` | Monetary | 金额/成本 = `-unit_amount × employee.hourly_cost`（负值），自动算 |
| `employee_id` | Many2one→**hr.employee** | 员工（**按"人"统计/筛选用这个**） |
| `user_id` | Many2one→res.users | compute 自 employee_id.user_id |
| `project_id` | Many2one→project.project (index) | 项目（**非空=工时单判定字段**） |
| `task_id` | Many2one→project.task | 任务（可空，工时可只挂项目） |
| `department_id` | Many2one→hr.department (compute, **store**) | 部门（store，可 groupby/domain） |
| `manager_id` | Many2one→hr.employee (related, store) | 直属经理 = employee_id.parent_id |
| `milestone_id` | Many2one→project.milestone (related, **不 store**) | 里程碑；**不能 groupby/求和**，domain 慎用 |
| `company_id` | Many2one→res.company (required) | 公司 |
| `validated` / `validated_status` | Boolean / Selection | **企业版**审批状态（已审批不可改） |

要点：
- 工时小时数 = **`unit_amount`**（不是 `amount`，amount 是钱）。
- 按"人"统计用 **`employee_id`**（hr.employee），不是 user_id。
- `department_id` store=True，可直接 groupby/domain；`milestone_id` related 非 store，不能进 groupby。
- 员工成本 `hourly_cost` 在 hr.employee（hr_hourly_cost 模块加），不在分析行上。

## 3. 按员工统计（read_group）

核心：对 `account.analytic.line` 调 read_group，domain 加 `('project_id','!=',False)`，对 `unit_amount` 求和。

> ⚠️ `read_group` 仍可 RPC 调，但源码已标 **Deprecated**，推荐 `formatted_read_group`（`aggregates=['unit_amount:sum']`，无 lazy 坑）。
> ⚠️ **`read_group` 默认 lazy=True，多 groupby 只展开第一维**。要"员工×项目/月"逐组明细，必须传 `{'lazy': False}`。

```python
# 3a. 每员工本月总工时
g = models.execute_kw(db, uid, pw, 'account.analytic.line', 'read_group',
    [[('project_id','!=',False),('date','>=','2026-06-01'),('date','<=','2026-06-30')],
     ['unit_amount:sum'], ['employee_id']])
# -> [{'employee_id':[12,'张三'], 'unit_amount':168.0, '__count':21, '__domain':[...]}, ...]

# 3b. 员工 × 项目（必须 lazy=False）
g = models.execute_kw(db, uid, pw, 'account.analytic.line', 'read_group',
    [[('project_id','!=',False),('date','>=','2026-06-01'),('date','<=','2026-06-30')],
     ['unit_amount:sum'], ['employee_id','project_id']], {'lazy': False})

# 3c. 员工 × 月
g = models.execute_kw(db, uid, pw, 'account.analytic.line', 'read_group',
    [[('project_id','!=',False),('date','>=','2026-01-01'),('date','<=','2026-12-31')],
     ['unit_amount:sum'], ['employee_id','date:month']], {'lazy': False})
# date 粒度: date:day / date:week / date:month / date:quarter / date:year；值形如 'June 2026'
```

## 4. 常见筛选维度（domain）

基线先带 `('project_id','!=',False)`，再叠加：

| 维度 | domain |
|---|---|
| 时间段 | `('date','>=','2026-06-01'),('date','<=','2026-06-30')` |
| 项目 | `('project_id','=',pid)` 或 `('project_id','in',[...])` |
| 员工 | `('employee_id','=',eid)` / `('employee_id','in',[...])` |
| 部门（store，直接过滤） | `('department_id','=',did)` 或 `('department_id.name','ilike','研发')` |
| 任务 | `('task_id','=',tid)` |
| 仅已审批（企业版） | `('validated','=',True)` |
| 某经理下属 | `('manager_id','=',mgr_eid)` |

## 5. XML-RPC 完整示例

参数顺序：`execute_kw(db, uid, pw, model, method, [positional], {kwargs})`。
`read_group` positional 三件套 = `[domain, fields, groupby]`，offset/limit/orderby/lazy 进第 7 个 kwargs。

```python
TS_BASE = [('project_id', '!=', False)]

# ① 某员工某月明细
detail = models.execute_kw(db, uid, pw, 'account.analytic.line', 'search_read',
    [TS_BASE + [('employee_id','=',12),('date','>=','2026-06-01'),('date','<=','2026-06-30')]],
    {'fields':['date','name','project_id','task_id','unit_amount','employee_id','department_id'],
     'order':'date asc'})

# ② 每员工本月总工时
by_emp = models.execute_kw(db, uid, pw, 'account.analytic.line', 'read_group',
    [TS_BASE + [('date','>=','2026-06-01'),('date','<=','2026-06-30')],
     ['unit_amount:sum'], ['employee_id']], {'orderby':'unit_amount desc'})
for g in by_emp:
    print(g['employee_id'][1] if g['employee_id'] else '(未指定)', '=>', g['unit_amount'], 'h', f"({g['__count']}条)")

# ③ 按项目统计
by_proj = models.execute_kw(db, uid, pw, 'account.analytic.line', 'read_group',
    [TS_BASE + [('date','>=','2026-06-01'),('date','<=','2026-06-30')],
     ['unit_amount:sum'], ['project_id']])
```

### read_group 返回结构

- groupby 字段值：M2O 为 `[id,'名']`；`date:month` 为 `'June 2026'`。
- 聚合值：键 = 传的 `'unit_amount:sum'`（也可能回 `'unit_amount'`，**取值前 print 一次确认键名**）。
- `__count`：该组记录数；`__domain`：钻取用 domain。

### 现代写法（formatted_read_group）

```python
by_emp = models.execute_kw(db, uid, pw, 'account.analytic.line', 'formatted_read_group',
    [TS_BASE + [('date','>=','2026-06-01'),('date','<=','2026-06-30')]],
    {'groupby':['employee_id'], 'aggregates':['unit_amount:sum'], 'order':'unit_amount:sum desc'})
# 返回 [{'employee_id':[12,'张三'], 'unit_amount:sum':168.0, '__extra_domain':[...]}, ...]
```
签名 `(domain, groupby=(), aggregates=(), having=(), offset=0, limit=None, order=None)`——无 lazy，多 groupby 默认全展开。

## 要点小结（TL;DR）

1. 模型 `account.analytic.line`；"是工时单"= domain 带 `('project_id','!=',False)`，**没有 is_timesheet 字段**。
2. 工时小时数 = **`unit_amount`**（label "Quantity"）；`amount` 是金额（负值），别混。
3. 按"人"用 **`employee_id`**（hr.employee）。`department_id`/`manager_id` store，可 groupby/domain。
4. `read_group` 多 groupby 必传 `{'lazy': False}`；长期工具用 `formatted_read_group`。
5. `read_group` positional = `[domain, fields, groupby]`，其余进 kwargs。
6. `milestone_id` related 非 store，不能 groupby；企业版 `validated` 做"仅已审批"过滤（社区版无此字段）。
