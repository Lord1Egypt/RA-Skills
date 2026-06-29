# Odoo 19 待办 / To-Do 模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/`
> 关键文件：`project_todo/models/project_task.py`、`project_todo/views/project_task_views.xml`、`project/models/project_task.py`、`project/models/project_task_stage_personal.py`、`project/models/project_task_type.py`

## 1. 模型与复用机制

**没有专门的 todo 模型。待办就是 `project.task`。**

- `project_todo` 模块只做 `_inherit = 'project.task'`，不新建模型、不加业务字段。它提供：简化视图（kanban/list/form/calendar/activity）、菜单、onboarding 模板、systray 计数。
- `__manifest__.py`：`depends: ['project']`，`auto_install: True`。

**「待办」= 私有 task 的判定**（来自 To-do 主 action 的 domain，这是「什么是待办」的权威定义）：

```python
[('user_ids', 'in', [uid]), ('project_id', '=', False), ('parent_id', '=', False)]
```

即：**指派给我 + 没有归属任何 project（`project_id = False`）+ 不是子任务**。

- `project_id` 的 falsy 标签就是 `🔒 Private`。「私有/个人 project」不是一条真实 project 记录，而是 `project_id = False` 这个状态本身。
- project_todo 的 `create` 覆盖：`name`/`project_id`/`parent_id` 都为空时，从 `description` 第一行自动生成标题；description 也空则填 `'Untitled to-do'`。
- 「转为任务」`action_convert_to_task` 本质就是给私有 task 补上 `project_id`。

**结论：用 XML-RPC 建一条待办 = `project.task.create({...})` 且不传 `project_id`（保持 False），并把当前用户放进 `user_ids`。**

## 2. 新建待办可设置的字段

| 字段名 | 类型 | 含义 / 注意 |
|---|---|---|
| `name` | Char（required, 'Title'） | 标题。project_todo 的 create 会兜底，不传不报错，但建议显式传。 |
| `description` | **Html**（不是 text） | 内容/描述，富文本，传 HTML 字符串。 |
| `date_deadline` | **Datetime**（不是 date！） | 截止时间。格式 `'YYYY-MM-DD HH:MM:SS'`，**按 UTC**。To-do 视图只显示日期部分。 |
| `user_ids` | **Many2many** → res.users | 负责人/指派人。**Odoo 19 是 m2m，不是 m2o**。domain 限 `share=False & active=True`（内部用户）。**建待办必须含当前 uid** 才进「我的待办」。写法 `[(6,0,[uid])]`。 |
| `priority` | Selection | `'0'` 普通(默认) / `'1'` 中 / `'2'` 高 / `'3'` 紧急。 |
| `tag_ids` | Many2many → project.tags | 标签。`[(6,0,[ids])]`；标签不存在可先 `project.tags.create({'name':...})`。 |
| `state` | Selection（required, 默认 `'01_in_progress'`） | 状态，标记完成写这个。见 §3。 |
| `personal_stage_type_id` | Many2one → project.task.type（related, **store=False**） | **个人阶段**（待办真正用的"阶段"）。To-do 表单顶部状态条用它，不是 stage_id。 |
| `stage_id` | Many2one → project.task.type | **项目看板列**。待办场景 `project_id=False` 时被强制 False，**待办不用**。 |
| `project_id` | Many2one → project.project | **待办必须留空（False）**。一旦设值就变成普通任务、退出 To-do 应用。 |
| `active` | Boolean（默认 True） | False=已归档。 |

### state vs stage_id vs personal_stage_type_id（关键三连）

- `stage_id`（→ project.task.type，"Task Stage"）：**项目级看板列**，属于某 project，多任务共享。待办强制 False。
- `personal_stage_type_id`（→ 同样 project.task.type，但 domain `user_id=uid`）：**每个用户私有的个人阶段**。这才是 To-do 里左侧分组/顶部状态条。底层是 `personal_stage_type_ids`（m2m，复用表 `project_task_user_rel` 的 stage_id 列）+ 当前用户视角的单值 related。
- `state`：跨项目的**统一状态机**，与阶段正交。决定开放/完成/取消/等待。To-do 的「打勾完成」操作的就是它。

### 个人阶段（personal stage）机制

- 每个用户首次有 task 指派时，自动创建 7 个默认个人阶段：`Inbox` / `Today` / `This Week` / `This Month` / `Later` / `Done`(fold) / `Cancelled`(fold)。
- create 后 `_populate_missing_personal_stages()` 自动跑，新待办默认落到该用户第一个个人阶段（**Inbox**）。
- 个人阶段记录存在独立模型 `project.task.stage.personal`（`_table='project_task_user_rel'`，字段 `task_id`/`user_id`/`stage_id`，唯一约束 `(task_id,user_id)`）。
- 阶段名用户自定义，**别硬编码 stage_id 数字**。要改个人阶段写 `personal_stage_type_id`（related inverse 会落到 personal stage 记录）。
- **`personal_stage_type_id` 是 store=False 且无自己的 search，不能用 `personal_stage_type_id.name` 点路径做 domain 过滤**。按个人阶段筛任务要查 `project.task.stage.personal`（`user_id=uid, stage_id=sid`）拿 task_id，再 `('id','in',tids)`。

## 3. `state` 字段完整取值（以源码为准）

| state 值（真实字符串） | 标签 | 含义 |
|---|---|---|
| `'01_in_progress'` | In Progress | 进行中（**默认值**） |
| `'02_changes_requested'` | Changes Requested | 要求修改 |
| `'03_approved'` | Approved | 已批准 |
| `'1_done'` | Done | **已完成**（CLOSED） |
| `'1_canceled'` | Cancelled | 已取消（CLOSED） |
| `'04_waiting_normal'` | Waiting | 等待中（被依赖任务阻塞时自动置入） |

易错点：
- 已完成是 **`'1_done'`**（不是 `'1_completed'`、不是 `'done'`）。
- 已取消是 **`'1_canceled'`**（单 l，美式拼写）。
- 等待是 **`'04_waiting_normal'`**（带 `_normal` 后缀）。

**标记「已完成」→ `state = '1_done'`**；取消打勾回退 `'01_in_progress'`；作废 `'1_canceled'`。

`CLOSED_STATES = {'1_done', '1_canceled'}`。判断「未完成/开放」用 `('is_closed','=',False)`（is_closed 是 computed+searchable），等价 `('state','not in',['1_done','1_canceled'])`。

`state` 是 compute+inverse+store 字段（依赖 stage_id 和 depend_on_ids.state）。开启任务依赖且有未完成前置任务时会被自动改成 `'04_waiting_normal'`；**直接 write state 是允许的**（readonly=False），待办无依赖场景不受联动干扰。

## 4. XML-RPC 真实示例

```python
import xmlrpc.client
from datetime import datetime, timedelta

URL, DB, USER, PWD = 'https://www.huo15.com', 'huo15', 'me@huo15.com', 'PWD_OR_APIKEY'
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USER, PWD, {})
models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
def call(model, method, *a, **kw): return models.execute_kw(DB, uid, PWD, model, method, list(a), kw)

# ① 创建待办（不传 project_id = 私有；user_ids 必须含自己）
deadline = (datetime.utcnow() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
todo_id = call('project.task', 'create', [{
    'name': '跟进客户报价单',
    'description': '<p>整理三和红木分账方案，周五前发出</p>',
    'date_deadline': deadline,         # Datetime / UTC
    'user_ids': [(6, 0, [uid])],
    'priority': '2',
}])

# ② 标记完成
call('project.task', 'write', [[todo_id], {'state': '1_done'}])

# ③ 查"我的未完成待办"
my = call('project.task', 'search_read',
    [[('user_ids','in',[uid]), ('project_id','=',False),
      ('parent_id','=',False), ('is_closed','=',False), ('active','=',True)]],
    {'fields': ['id','name','state','priority','date_deadline','personal_stage_type_id'],
     'order': 'priority desc, date_deadline asc, id desc'})
```

**JSON-RPC 等价**：同样 model/method/args，POST `{URL}/jsonrpc`，`params.service='object'`、`params.method='execute_kw'`、`params.args=[DB,uid,PWD,model,method,args,kwargs]`。

## 要点小结

- 模型固定 `project.task`；待办 = `project_id=False` 且 `user_ids` 含本人。
- m2m 写法 `[(6,0,[ids])]`（替换）或 `[(4,id)]`（追加）。
- `date_deadline` 是 **Datetime**，按 UTC。
- 完成=`'1_done'`、取消=`'1_canceled'`、进行中=`'01_in_progress'`、等待=`'04_waiting_normal'`。
- 「未完成」优先 `('is_closed','=',False)`。
- 待办别用 `stage_id`（强制 False）；个人阶段用 `personal_stage_type_id`，筛选走关联表。
