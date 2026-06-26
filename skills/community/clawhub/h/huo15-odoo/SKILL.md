---
name: huo15-odoo
description: |
  火一五欧度技能（辉火云企业套件 Odoo 19 接口访问指南）。
  支持分布式配置：全局保存系统地址和数据库名，每个 agent 独立保存自己的用户名和密码。
  其他 Odoo 技能可复用本技能保存的配置。
trigger:
  - patterns:
      - "odoo"
      - "辉火云"
      - "欧度"
      - "欧度"
      - "辉火"
    type: fuzzy
---

# 火一五欧度技能（Odoo 19）

> 辉火云企业套件（Odoo 19）接口访问 · 分布式配置版
> **重要**：必须使用 XML-RPC，不兼容 odoorpc 库！

---

## 🏗️ 配置架构

```
全局配置（所有 agent 共享）
  └── ODOO_URL      系统地址
  └── ODOO_DB       数据库名

Agent 本地配置（各 agent 独立）
  └── 用户名         user
  └── 密码           password
```

**查找顺序：**
- 用户名/密码 → 先查本 agent 本地配置，没有则提示用户输入
- 系统地址/数据库名 → 读全局配置
- 其他 Odoo 技能复用同样的逻辑

---

## 🚀 首次使用（自动引导）

首次使用本技能时，按顺序引导：

### 第一步：全局初始化（一次性）

> 由主 agent（main）完成，之后所有 agent 共享

技能检测到没有全局配置，会提示：

```
🔧 Odoo 全局配置
请提供以下信息（前后不能有空格）：

1. 公司系统地址（如 https://huihuoyun.2008qd.com.cn）：
2. 数据库名（如 xinqiantu）：
```

→ 用户输入后，保存到 `~/.openclaw/openclaw.json` 的 `skills.entries.huo15-odoo.env`

> 说「更新 Odoo 全局配置」可重新填写

### 第二步：Agent 凭证初始化

> 每个 agent 会话首次使用时独立进行

技能检测到本 agent 没有凭证配置，会提示：

```
🔑 请提供你的 Odoo 登录信息（仅本 Agent 可访问，不会共享）：

1. 用户名（邮箱）：
2. 密码：
```

→ 用户输入后，保存到 `~/.openclaw/agents/{agentId}/odoo_creds.json`

> 说「更新 Odoo 凭证」可重新填写本 agent 的凭证

---

## 🔧 Python 连接模板

> 在任何 Python 脚本中，先用 helper 读取配置：

```python
import ssl
import json
import os
import xmlrpc.client

# ── 读取配置 ──────────────────────────────────────────────
AGENT_ID = os.environ.get('OC_AGENT_ID', 'main')
AGENTS_DIR = os.path.expanduser('~/.openclaw/agents')

# 1. 全局配置（系统地址 + 数据库名）
import subprocess
r = subprocess.run(
    ['python3', os.path.expanduser('~/.openclaw/workspace/scripts/odoo_config.py'), 'resolve'],
    capture_output=True, text=True,
    env={**os.environ, 'OC_AGENT_ID': AGENT_ID}
)
cfg = json.loads(r.stdout.strip())
# cfg = { 'url': ..., 'db': ..., 'user': ..., 'password': ... }

url = cfg['url']
db = cfg['db']
user = cfg['user']
password = cfg['password']

# 2. SSL 跳过（辉火云证书问题）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 3. 连接
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object', context=ctx)

print(f"✅ 连接成功! UID: {uid}")
```

---

## 📋 Odoo 19 常用模型

### 联系人（res.partner）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'res.partner', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'res.partner', 'create', [values])` |
| 更新 | `execute_kw(db, uid, password, 'res.partner', 'write', [id, values])` |

### 项目（project.project）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'project.project', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'project.project', 'create', [values])` |

### 任务（project.task）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'project.task', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'project.task', 'create', [values])` |

### 商机（crm.lead）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'crm.lead', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'crm.lead', 'create', [values])` |
| 更新 | `execute_kw(db, uid, password, 'crm.lead', 'write', [id, values])` |
| 删除 | `execute_kw(db, uid, password, 'crm.lead', 'unlink', [[id]])` |

### 活动（mail.activity）

| 操作 | 方法 |
|------|------|
| 查询 | `execute_kw(db, uid, password, 'mail.activity', 'search_read', [domain], options)` |
| 创建 | `execute_kw(db, uid, password, 'mail.activity', 'create', [values])` |
| 完成 | `execute_kw(db, uid, password, 'mail.activity', 'action_done', [[id]])` |
| 取消 | `execute_kw(db, uid, password, 'mail.activity', 'action_cancel', [[id]])` |
| 跳过 | `execute_kw(db, uid, password, 'mail.activity', 'action_skip', [[id]])` |

---

## 🔧 常用操作示例

### 查询客户
```python
domain = [('name', 'ilike', '关键词')]
fields = ['id', 'name', 'vat', 'street', 'city', 'phone', 'email']
result = models.execute_kw(db, uid, password, 'res.partner', 'search_read',
    [domain], {'fields': fields, 'limit': 10})
```

### 创建客户公司
```python
values = {
    'name': '公司名称',
    'company_type': 'company',
    'vat': '统一社会信用代码',
}
partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [values])
```

### 创建联系人（关联到公司）
```python
values = {
    'name': '联系人姓名',
    'parent_id': partner_id,
    'type': 'contact',
    'function': '职位',
    'phone': '电话',
    'email': '邮箱',
}
contact_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [values])
```

### 查询项目
```python
domain = [('active', '=', True)]
fields = ['id', 'name', 'partner_id', 'user_id']
result = models.execute_kw(db, uid, password, 'project.project', 'search_read',
    [domain], {'fields': fields, 'limit': 20})
```

### 创建项目
```python
values = {
    'name': '项目名称',
    'partner_id': partner_id,
    'description': '项目描述',
}
project_id = models.execute_kw(db, uid, password, 'project.project', 'create', [values])
```

### 查询任务（⚠️ 必须加 active=True）
```python
domain = [
    ('active', '=', True),
    ('project_id', '=', project_id),
]
fields = ['id', 'name', 'user_ids', 'stage_id', 'priority']
result = models.execute_kw(db, uid, password, 'project.task', 'search_read',
    [domain], {'fields': fields, 'limit': 50})
```

### 创建任务
```python
values = {
    'name': '任务名称',
    'project_id': project_id,
    'user_ids': [(6, 0, [user_id])],
    'description': '任务描述',
    'priority': '0',
}
task_id = models.execute_kw(db, uid, password, 'project.task', 'create', [values])
```

---

## 📊 execute_kw 参数说明

```python
models.execute_kw(db, uid, password, model_name, method, args, kwargs)
```

| 参数 | 说明 |
|------|------|
| db | 数据库名 |
| uid | 登录后的用户ID（authenticate 返回） |
| password | 密码 |
| model_name | 模型名，如 'res.partner' |
| method | 'search_read', 'create', 'write', 'unlink' |
| args | domain 列表（搜索条件） |
| kwargs | {'fields': [...], 'limit': 10, 'order': 'name asc'} |

**Domain 语法示例：**
- `[('name', '=', '张三')]` — 等于
- `[('amount', '>', 1000)]` — 大于
- `[('date', '>=', '2025-01-01')]` — 大于等于
- `[('state', 'in', ['draft', 'sent'])]` — 在多值中
- `[('name', 'ilike', '关键词')]` — 模糊匹配（不区分大小写）
- `[('partner_id', '!=', False)]` — 非空

**组合条件：**
```python
domain = [
    '&',  # AND
    ('state', '=', 'open'),
    ('amount', '>', 1000),
]
```

---

## ⚠️ 常见错误与解决方案

### 1. 权限错误 (AccessError)
**错误信息：** `AccessError: The requested operation cannot be completed due to security restrictions.`

**解决方案：**
- 检查当前用户是否有该模型的读写权限
- 检查字段级权限（某些字段可能只读）
- 联系管理员调整权限组

### 2. 字段不存在 (AttributeError)
**错误信息：** `AttributeError: 'res.partner' object has no attribute 'xxx'`

**解决方案：**
- 使用 `fields_get()` 查看可用字段：
```python
fields = models.execute_kw(db, uid, password, 'res.partner', 'fields_get')
print(fields.keys())
```
- 确认字段名拼写正确（Odoo 使用下划线命名）

### 3. Many2One 字段赋值错误
**错误信息：** `ValueError: Invalid field ...`

**解决方案：**
- Many2One 字段需要传 ID，不是字典：
```python
# ✅ 正确
{'partner_id': partner_id}

# ❌ 错误
{'partner_id': {'id': partner_id, 'name': 'xxx'}}
```

### 4. 创建失败（缺少必填字段）
**错误信息：** `ValidationError: ... field(s) required`

**解决方案：**
- 使用 `fields_get()` 查看必填字段：
```python
fields = models.execute_kw(db, uid, password, 'crm.lead', 'fields_get')
for field, info in fields.items():
    if info.get('required'):
        print(f"必填字段: {field}")
```

### 5. SSL 证书错误
**错误信息：** `ssl.SSLCertVerificationError`

**解决方案：**
确保连接时使用：
```python
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common', context=ctx)
```

---

## ⚠️ 注意事项

1. **必须使用 XML-RPC**，路径 `/xmlrpc/2/common` 和 `/xmlrpc/2/object`
2. **SSL 跳过**：辉火云证书问题，连接时加 `context=ctx`
3. **任务查询**：必须加 `('active', '=', True)` 过滤
4. **用户名/密码** 各 agent 独立存储，不共享
5. **系统地址/数据库名** 全局共享，所有 agent 一致

---

## 📚 知识库 (Knowledge) 操作

### 创建知识库文章
```python
article_id = models.execute_kw(db, uid, password, 'knowledge.article', 'create', [{
    'name': '文章标题',
    'body': '<h1>内容</h1><p>正文</p>',
    'internal_permission': 'write',
}])
```

| 字段 | 类型 | 说明 |
|------|------|------|
| name | Char | 文章标题 |
| body | Html | 内容（HTML格式） |
| internal_permission | Selection | 'write'/'read'/'none' |

---

## 🎯 商机活动管理（提醒/待办）

### 查询商机
```python
domain = [('type', '=', 'opportunity')]  # 只查商机（排除线索）
fields = ['id', 'name', 'partner_id', 'stage_id', 'probability', 'expected_revenue', 'user_id']
result = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
    [domain], {'fields': fields, 'limit': 50})
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| name | Char | 商机名称 |
| partner_id | Many2One (res.partner) | 客户 |
| stage_id | Many2One (crm.stage) | 销售阶段 |
| probability | Float | 成交概率 (%) |
| expected_revenue | Float | 预期收入 |
| user_id | Many2One (res.users) | 负责人 |
| type | Selection | 'lead'（线索）或 'opportunity'（商机） |

### 创建商机
```python
values = {
    'name': '商机名称',
    'type': 'opportunity',
    'partner_id': partner_id,  # 客户ID
    'stage_id': stage_id,      # 阶段ID
    'probability': 30.0,
    'expected_revenue': 10000.0,
    'user_id': user_id,        # 负责人ID（可选）
    'description': '商机描述',
}
lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'create', [values])
```

### 为商机创建提醒/待办活动

在 Odoo 中，**提醒** 和 **待办** 都是 `mail.activity` 类型的活动，通过 `activity_type_id` 区分。

**常用活动类型：**
- 提醒（Reminder）：`email`（邮件）、`phonecall`（电话）
- 待办（To-Do）：`to_do`（待办事项）

```python
activity_id = models.execute_kw(db, uid, password, 'mail.activity', 'create', [{
    'res_model_id': model_id,           # 关联模型ID（商机 = 'crm.lead'）
    'res_id': lead_id,                  # 商机记录ID
    'activity_type_id': activity_type_id, # 活动类型ID
    'summary': '活动标题',
    'note': '<p>详细说明...</p>',        # HTML格式
    'date_deadline': '2025-03-30',      # 截止日期（YYYY-MM-DD）
    'user_id': user_id,                 # 指派给谁（可选）
}])
```

**字段说明：**
| 字段 | 类型 | 说明 |
|------|------|------|
| res_model_id | Many2One (ir.model) | 关联模型（通过 `ir.model` 查询 `crm.lead` 的ID） |
| res_id | Integer | 关联记录ID（商机ID） |
| activity_type_id | Many2One (mail.activity.type) | 活动类型ID |
| summary | Char | 活动标题 |
| note | Html | 详细说明（支持HTML） |
| date_deadline | Date | 截止日期 |
| user_id | Many2One (res.users) | 指派给谁（不填则指给自己） |

**完整示例：**
```python
import xmlrpc.client
import ssl
import json
import os

# 1. 读取配置（略，见前面模板）

# 2. 连接 Odoo（略）

# 3. 查询要添加活动的商机
domain = [('name', '=', '某商机名称')]
leads = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
    [domain], {'fields': ['id', 'name']})
if not leads:
    print('商机不存在')
    exit()
lead_id = leads[0]['id']

# 4. 获取 crm.lead 的 model_id
model_ids = models.execute_kw(db, uid, password, 'ir.model', 'search',
    [[('model', '=', 'crm.lead')]], {'limit': 1})
if not model_ids:
    print('未找到 crm.lead 模型')
    exit()
model_id = model_ids[0]

# 5. 获取活动类型ID（以待办为例）
activity_type_ids = models.execute_kw(db, uid, password, 'mail.activity.type', 'search',
    [[('name', '=', 'To Do')]], {'limit': 1})
if not activity_type_ids:
    # 备选：使用默认的 email 类型
    activity_type_ids = models.execute_kw(db, uid, password, 'mail.activity.type', 'search',
        [[('name', '=', 'Email')]], {'limit': 1})
activity_type_id = activity_type_ids[0] if activity_type_ids else None

# 6. 创建活动
values = {
    'res_model_id': model_id,
    'res_id': lead_id,
    'activity_type_id': activity_type_id,
    'summary': '跟进电话',
    'note': '<p>讨论合同细节</p>',
    'date_deadline': '2025-03-30',
}
activity_id = models.execute_kw(db, uid, password, 'mail.activity', 'create', [values])
print(f'✅ 活动创建成功，ID: {activity_id}')
```

### 查询商机的活动
```python
# 先获取商机的 model_id
model_ids = models.execute_kw(db, uid, password, 'ir.model', 'search',
    [[('model', '=', 'crm.lead')]], {'limit': 1})
model_id = model_ids[0] if model_ids else None

# 查询该商机的所有活动
domain = [
    ('res_model_id', '=', model_id),
    ('res_id', '=', lead_id),
    ('active', '=', True),
]
fields = ['id', 'summary', 'note', 'date_deadline', 'activity_type_id', 'user_id', 'state']
activities = models.execute_kw(db, uid, password, 'mail.activity', 'search_read',
    [domain], {'fields': fields})
```

**活动状态（state）：**
- 'planned' — 计划中
- 'today' — 今日待办
- 'overdue' — 已逾期
- 'done' — 已完成
- 'cancel' — 已取消

### 完成/取消/跳过活动
```python
# 完成
models.execute_kw(db, uid, password, 'mail.activity', 'action_done', [[activity_id]])

# 取消
models.execute_kw(db, uid, password, 'mail.activity', 'action_cancel', [[activity_id]])

# 跳过
models.execute_kw(db, uid, password, 'mail.activity', 'action_skip', [[activity_id]])
```

### 批量查询商机的活动（优化性能）
```python
# 1. 先查询所有商机的 model_id（只需一次）
model_ids = models.execute_kw(db, uid, password, 'ir.model', 'search',
    [[('model', '=', 'crm.lead')]], {'limit': 1})
model_id = model_ids[0] if model_ids else None

# 2. 批量查询多个商机的活动
lead_ids = [1, 2, 3, 4, 5]  # 商机ID列表
domain = [
    ('res_model_id', '=', model_id),
    ('res_id', 'in', lead_ids),
    ('active', '=', True),
]
fields = ['id', 'summary', 'res_id', 'date_deadline', 'state']
activities = models.execute_kw(db, uid, password, 'mail.activity', 'search_read',
    [domain], {'fields': fields})

# 3. 按商机ID分组
from collections import defaultdict
activities_by_lead = defaultdict(list)
for act in activities:
    activities_by_lead[act['res_id']].append(act)

# 4. 输出统计
for lead_id in lead_ids:
    count = len(activities_by_lead[lead_id])
    print(f"商机 {lead_id} 有 {count} 个活动")
```

### 自动为商机创建跟进活动（实用场景）
```python
def create_followup_activities_for_leads(models, db, uid, password, days_ahead=7):
    """为所有未完成商机创建跟进提醒"""

    # 1. 查询活跃商机（排除已won/lost）
    domain = [('type', '=', 'opportunity'), ('active', '=', True)]
    fields = ['id', 'name', 'partner_id', 'user_id']
    leads = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
        [domain], {'fields': fields})

    # 2. 获取必要的 reference 数据
    model_ids = models.execute_kw(db, uid, password, 'ir.model', 'search',
        [[('model', '=', 'crm.lead')]], {'limit': 1})
    model_id = model_ids[0] if model_ids else None

    # 获取活动类型：Email 和 To Do
    activity_types = {}
    for type_name in ['Email', 'To Do', 'Phonecall']:
        type_ids = models.execute_kw(db, uid, password, 'mail.activity.type', 'search',
            [[('name', '=', type_name)]], {'limit': 1})
        activity_types[type_name] = type_ids[0] if type_ids else None

    # 3. 为每个商机创建活动
    from datetime import datetime, timedelta
    deadline = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

    created_count = 0
    for lead in leads:
        user_id = lead.get('user_id') and lead['user_id'][0] or uid

        # 创建 Email 跟进
        if activity_types['Email']:
            models.execute_kw(db, uid, password, 'mail.activity', 'create', [{
                'res_model_id': model_id,
                'res_id': lead['id'],
                'activity_type_id': activity_types['Email'],
                'summary': f'跟进 {lead["name"]} - 发送邮件',
                'note': f'<p>联系客户：{lead["partner_id"][1] if lead.get("partner_id") else "未知客户"}</p>',
                'date_deadline': deadline,
                'user_id': user_id,
            }])
            created_count += 1

        # 创建 To Do
        if activity_types['To Do']:
            models.execute_kw(db, uid, password, 'mail.activity', 'create', [{
                'res_model_id': model_id,
                'res_id': lead['id'],
                'activity_type_id': activity_types['To Do'],
                'summary': f'跟进 {lead["name"]} - 待办事项',
                'note': '<p>确认合同细节</p>',
                'date_deadline': deadline,
                'user_id': user_id,
            }])
            created_count += 1

    print(f'✅ 为 {len(leads)} 个商机创建了 {created_count} 个跟进活动')
    return created_count
```

---

## 🎨 高级用法：销售管道与阶段管理

### 查询销售阶段（crm.stage）
```python
stages = models.execute_kw(db, uid, password, 'crm.stage', 'search_read',
    [], {'fields': ['id', 'name', 'sequence', 'is_won', 'is_lost']})

for stage in stages:
    print(f"{stage['name']} (ID:{stage['id']}) - 序列:{stage['sequence']}")
```

### 按阶段统计商机
```python
# 查询所有商机（包含阶段）
leads = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
    [('type', '=', 'opportunity')],
    {'fields': ['id', 'name', 'stage_id', 'probability', 'expected_revenue']})

# 按阶段分组统计
from collections import defaultdict
by_stage = defaultdict(list)
for lead in leads:
    stage_name = lead['stage_id'][1] if lead.get('stage_id') else '未设置'
    by_stage[stage_name].append(lead)

# 输出统计
for stage_name, leads_list in by_stage.items():
    total_revenue = sum(l.get('expected_revenue', 0) for l in leads_list)
    avg_prob = sum(l.get('probability', 0) for l in leads_list) / len(leads_list) if leads_list else 0
    print(f"{stage_name}: {len(leads_list)} 个商机，总金额 {total_revenue:,.2f}，平均概率 {avg_prob:.1f}%")
```

### 移动商机到下一阶段
```python
def move_lead_to_next_stage(models, db, uid, password, lead_id):
    """将商机推进到下一个销售阶段"""

    # 1. 查询商机当前阶段
    lead = models.execute_kw(db, uid, password, 'crm.lead', 'read',
        [lead_id], {'fields': ['stage_id', 'name']})
    if not lead:
        print('商机不存在')
        return False

    current_stage_id = lead[0].get('stage_id', [False, ''])[0]
    current_stage_name = lead[0].get('stage_id', [False, ''])[1]

    # 2. 查询所有阶段按序列排序
    stages = models.execute_kw(db, uid, password, 'crm.stage', 'search_read',
        [], {'fields': ['id', 'name', 'sequence'], 'order': 'sequence'})

    # 3. 找到下一个阶段
    next_stage = None
    for i, stage in enumerate(stages):
        if stage['id'] == current_stage_id:
            if i + 1 < len(stages):
                next_stage = stages[i + 1]
            break

    if not next_stage:
        print(f'商机 "{lead[0]["name"]}" 已在最后阶段: {current_stage_name}')
        return False

    # 4. 更新商机阶段
    models.execute_kw(db, uid, password, 'crm.lead', 'write',
        [[lead_id], {'stage_id': next_stage['id']}])

    print(f'✅ 商机 "{lead[0]["name"]}" 从 "{current_stage_name}" 移动到 "{next_stage["name"]}"')
    return True
```

---

## 🔄 线索（Leads）转换与活动

### 查询线索
```python
leads = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
    [('type', '=', 'lead')],  # 只查线索，不查商机
    {'fields': ['id', 'name', 'partner_id', 'user_id', 'create_date']})
```

### 将线索转换为商机
```python
lead_id = 123  # 线索ID

# 1. 读取线索信息
lead = models.execute_kw(db, uid, password, 'crm.lead', 'read',
    [lead_id], {'fields': ['name', 'partner_id', 'type', 'description']})[0]

# 2. 更新为商机（修改 type 和 stage）
models.execute_kw(db, uid, password, 'crm.lead', 'write',
    [[lead_id], {
        'type': 'opportunity',
        'stage_id': stage_id,  # 需要先查询一个有效的阶段ID
    }])

print(f'✅ 线索 "{lead["name"]}" 已转换为商机')
```

### 线索自动创建商机（批量转换）
```python
def convert_qualified_leads(models, db, uid, password, criteria=None):
    """将符合条件的高质量线索批量转换为商机"""

    # 默认条件：超过3天且未联系
    domain = [
        ('type', '=', 'lead'),
        ('create_date', '<', (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')),
        ('partner_id', '!=', False),
    ]

    if criteria:
        domain.extend(criteria)

    leads = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
        [domain], {'fields': ['id', 'name', 'partner_id']})

    # 查询默认销售阶段（第一个）
    stages = models.execute_kw(db, uid, password, 'crm.stage', 'search_read',
        [], {'fields': ['id', 'name'], 'limit': 1})
    default_stage_id = stages[0]['id'] if stages else None

    converted = 0
    for lead in leads:
        models.execute_kw(db, uid, password, 'crm.lead', 'write',
            [[lead['id']], {
                'type': 'opportunity',
                'stage_id': default_stage_id,
            }])
        converted += 1

    print(f'✅ 转换了 {converted} 个线索为商机')
    return converted
```

---

## 📈 报表与分析实用函数

### 销售业绩统计（按负责人）
```python
def sales_performance_report(models, db, uid, password, start_date=None, end_date=None):
    """生成销售业绩报表"""

    domain = [('type', '=', 'opportunity'), ('stage_id.is_won', '=', True)]

    if start_date and end_date:
        domain.append(('date_closed', '>=', start_date))
        domain.append(('date_closed', '<=', end_date))

    won_deals = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
        [domain],
        {'fields': ['user_id', 'partner_id', 'expected_revenue', 'date_closed']})

    # 按销售分组
    from collections import defaultdict
    sales_data = defaultdict(lambda: {'count': 0, 'revenue': 0.0, 'customers': set()})

    for deal in won_deals:
        user_name = deal.get('user_id') and deal['user_id'][1] or '未分配'
        sales_data[user_name]['count'] += 1
        sales_data[user_name]['revenue'] += deal.get('expected_revenue', 0)
        if deal.get('partner_id'):
            sales_data[user_name]['customers'].add(deal['partner_id'][1])

    # 打印报表
    print("📊 销售业绩报表")
    print("=" * 60)
    for salesperson, data in sorted(sales_data.items(), key=lambda x: x[1]['revenue'], reverse=True):
        print(f"{salesperson}:")
        print(f"  成交单数: {data['count']}")
        print(f"  总金额: ¥{data['revenue']:,.2f}")
        print(f"  客户数: {len(data['customers'])}")
        print()

    return sales_data
```

### 商机漏斗分析
```python
def funnel_analysis(models, db, uid, password):
    """分析销售漏斗转化率"""

    # 查询所有商机
    leads = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
        [('type', '=', 'opportunity')],
        {'fields': ['stage_id', 'probability', 'expected_revenue']})

    # 查询所有阶段
    stages = models.execute_kw(db, uid, password, 'crm.stage', 'search_read',
        [], {'fields': ['id', 'name', 'sequence'], 'order': 'sequence'})

    stage_data = {stage['id']: {'name': stage['name'], 'count': 0, 'revenue': 0} for stage in stages}

    for lead in leads:
        stage_id = lead.get('stage_id', [False, ''])[0]
        if stage_id in stage_data:
            stage_data[stage_id]['count'] += 1
            stage_data[stage_id]['revenue'] += lead.get('expected_revenue', 0)

    # 输出漏斗
    print("🔍 销售漏斗分析")
    print("=" * 60)
    for stage in stages:
        data = stage_data[stage['id']]
        print(f"{stage['name']}: {data['count']} 个商机，¥{data['revenue']:,.2f}")

    return stage_data
```

---

## 🐳 Odoo Docker 本地开发

| 资源 | 地址/路径 |
|------|-----------|
| Docker 配置仓库 | https://cnb.cool/huo15/tools/odoo19_docker |
| 本地路径 | `~/workspace/study/odoo_study/odoo19_docker` |

启动：
```bash
cd ~/workspace/study/odoo_study/odoo19_docker
docker compose -p <项目名称> up --build
```

---

## 🔗 相关技能

- **huo15-doc-template**：文档生成
- **odoo-reporting**：Odoo 数据报表

---

## 配置命令

| 命令 | 说明 |
|------|------|
| 「更新 Odoo 全局配置」 | 重新设置系统地址和数据库名 |
| 「更新 Odoo 凭证」 | 重新设置本 agent 的用户名和密码 |
| 「查看 Odoo 配置」 | 显示当前配置状态（不显示密码） |
