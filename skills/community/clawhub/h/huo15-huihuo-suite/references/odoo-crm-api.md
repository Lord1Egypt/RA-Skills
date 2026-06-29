# Odoo 19 CRM 模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/crm/`
> 文件：`models/crm_lead.py`、`crm_stage.py`、`crm_team.py`、`crm_lost_reason.py`；团队基模型在 `sales_team/models/crm_team.py`。

## ⚠️ 最易错的 8 条（改代码前必看）

1. **`crm.lead` 没有 `mobile` 字段** —— 手机号写 `phone`。
2. **`crm.stage` 的团队关联是 `team_ids`（复数 m2m），不是 `team_id`**；空 team_ids = 全团队共享。
3. **`crm.lead.user_id` 是单数 Many2one**（负责人/销售员）；`crm.team.user_id` 是团队 Leader。
4. **`description` 是 Html** 不是 Text（传 `<p>...</p>` 或纯字符串）。
5. **赢单/输单/复活务必调专用方法**（`action_set_won`/`action_set_lost`/`action_restore`），别手动 write stage/active/probability，否则破坏 PLS 概率模型、概率约束、lost_reason 清理等不变式。
6. **建商机务必显式传 `type='opportunity'`** —— 默认值依赖配置（启用线索功能时默认 `'lead'`）。
7. **`probability` 一旦手写就与 `automated_probability` 脱钩**，自动重算不再覆盖。
8. **`read_group` 默认只统计 `active=True`**（输单 active=False 自动排除）；要含输单须 `context={'active_test': False}`。`priority` 是字符串 `'0'/'1'/'2'/'3'`。

## 1. crm.lead（线索与商机同一模型）

`type` selection：`('lead','Lead')` / `('opportunity','Opportunity')`。线索=待资格化原始请求；商机=进入 pipeline、参与概率/收入预测。

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char, required | 商机/线索标题 |
| `type` | Selection | `'lead'` / `'opportunity'`（建商机显式传 opportunity） |
| `partner_id` | Many2one→res.partner | 客户/联系人 |
| `contact_name` | Char | 联系人姓名 |
| `email_from` | Char | 邮箱 |
| `phone` | Char | 电话（**手机号也写这里，无 mobile 字段**） |
| `partner_name` | Char | 公司名（转商机时创建的公司） |
| `expected_revenue` | Monetary | 预期收入 |
| `prorated_revenue` | Monetary（compute store）| = expected_revenue × probability/100（加权预测） |
| `probability` | Float（store, **可写** 0–100）| 成交概率，可手写 |
| `automated_probability` | Float（**只读**）| 机器学习（朴素贝叶斯 PLS）算的概率 |
| `stage_id` | Many2one→crm.stage | 阶段，domain `['|',('team_ids','=',False),('team_ids','in',team_id)]` |
| `user_id` | **Many2one**→res.users | 负责人/销售员（**单数**），默认当前用户，domain `[('share','=',False)]` |
| `team_id` | Many2one→crm.team | 销售团队 |
| `priority` | Selection | `'0'`低/`'1'`中/`'2'`高/`'3'`很高 |
| `date_deadline` | Date | 预计成交日 |
| `description` | **Html** | 备注 |
| `tag_ids` | Many2many→crm.tag | 标签 |
| `lost_reason_id` | Many2one→crm.lost.reason | 输单原因 |
| `active` | Boolean | 归档标记（输单=False） |
| `won_status` | Selection（store compute, 只读）| `'won'`/`'lost'`/`'pending'`，**判断赢/输/进行中的权威字段** |
| `date_closed` | Datetime（只读）| 关单日期 |
| `campaign_id`/`source_id`/`medium_id` | Many2one | UTM 营销活动/来源/媒介 |

**won_status 派生**：`probability==100 and stage_id.is_won` → won；`not active and probability==0` → lost；其余 → pending。

## 2. crm.stage

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char, required | 阶段名 |
| `sequence` | Integer | 排序（小在前） |
| `is_won` | Boolean | 赢单阶段标记 |
| `team_ids` | **Many2many→crm.team** | 绑定团队（**复数**），空=全团队共享 |
| `fold` | Boolean | 看板折叠 |
| `rotting_threshold_days` | Integer | 多少天不更新算"腐烂"，0=禁用 |

> 把 stage 改成 is_won=True 时，Odoo 会把该阶段下所有 lead 强制 probability=100。

## 3. crm.team（销售团队）

`name`（团队名）、`user_id`（团队 Leader）、`member_ids`（成员 m2m）、`crm_team_member_ids`（成员明细 o2m，含配额）。crm 扩展：`use_leads`/`use_opportunities`/`assignment_*`。

## 4. 赢单 / 输单 / 复活（真实方法名）

### 赢单 `action_set_won`（crm_lead.py:1127）
语义：移到 is_won=True 阶段 + probability=100。实现：先 unarchive → `_stage_find(domain=[('is_won','=',True)])` 选赢单阶段 → `write({'stage_id': won, 'probability': 100})`。
- RPC：`execute_kw('crm.lead', 'action_set_won', [[ids]])`
- `action_set_won_rainbowman` = 同上 + UI 彩虹特效（RPC 用前者即可）。

### 输单 `action_set_lost(self, **additional_values)`（crm_lead.py:1121）
```python
res = self.action_archive()                       # active=False
self.write({**additional_values, 'probability': 0, 'automated_probability': 0})
```
- 传输单原因：kwargs `lost_reason_id`。
- RPC：`execute_kw('crm.lead', 'action_set_lost', [[ids]], {'lost_reason_id': reason_id})`
- 结果：active=False、probability=0、automated_probability=0、lost_reason_id=该 id。
- **无需走 crm.lead.lost 向导**，直接调方法。

### 复活 `action_restore`（crm_lead.py:1112）
= unarchive（清空 lost_reason_id）+ probability=automated_probability（回自动概率轨道）。
- RPC：`execute_kw('crm.lead', 'action_restore', [[ids]])`

### crm.lost.reason
字段：`name`（required，输单原因描述）、`active`。

## 5. 线索 → 商机

`convert_opportunity(self, partner, user_ids=False, team_id=False)`（crm_lead.py:1850）。
- RPC：`execute_kw('crm.lead', 'convert_opportunity', [[lead_id], partner_id_or_False])`（partner 传 **id 整数** 或 False）。
- 内部置 `type='opportunity'` + `date_conversion` + 无 stage 时补默认阶段 + 可选分配。
- 简单场景也可 `write({'type':'opportunity'})`，但不补 date_conversion / 默认 stage / 分配。

## 6. Pipeline 统计（read_group）

domain 注意：`('type','=','opportunity')` + `('active','=',True)`（默认已排除输单）；只看进行中加 `('won_status','=','pending')`。

```python
# 按阶段统计预期收入 + 加权预测
stats = call('crm.lead', 'read_group', [
    [('type','=','opportunity'), ('active','=',True)],
    ['expected_revenue:sum', 'prorated_revenue:sum'],   # fields
    ['stage_id'],                                        # groupby
], {'lazy': False})
# groupby 换 ['user_id'] / ['team_id']；formatted_read_group 同理（aggregates=[...]）
```

## 7. 安排跟进活动（activity_schedule）

crm.lead 继承 `mail.activity.mixin`，**用 `activity_schedule` 而非手建 mail.activity**：
```python
call('crm.lead', 'activity_schedule',
     [[lead_id], 'mail.mail_activity_data_call'],         # ids + 活动类型 xmlid
     {'date_deadline': '2026-06-10', 'summary': '回访客户', 'user_id': uid})
```
活动类型 xmlid：`mail.mail_activity_data_call`（电话）/ `_meeting`（会议）/ `_todo`（待办）/ `_email`（邮件）。

## 8. XML-RPC 实战示例

```python
def call(model, method, args, kw=None): return models.execute_kw(db, uid, pw, model, method, args, kw or {})

# ① 新建商机（type 必显式传；user_id 单数）
opp = call('crm.lead', 'create', [{
    'name': '某客户-ERP项目', 'type': 'opportunity', 'partner_id': 42,
    'expected_revenue': 50000, 'user_id': uid, 'team_id': 1,
    'priority': '2', 'date_deadline': '2026-07-01'}])

# ② 推进阶段（按名字找 stage）
sid = call('crm.stage', 'name_search', [], {'name': '报价', 'limit': 1})[0][0]
call('crm.lead', 'write', [[opp], {'stage_id': sid}])

# ③ 赢单
call('crm.lead', 'action_set_won', [[opp]])

# ④ 输单（带原因）
rid = call('crm.lost.reason', 'search', [[('name','ilike','价格太高')]], {'limit':1})
rid = rid[0] if rid else call('crm.lost.reason', 'create', [{'name':'价格太高'}])
call('crm.lead', 'action_set_lost', [[opp]], {'lost_reason_id': rid})

# ⑤ pipeline 按阶段
call('crm.lead', 'read_group',
     [[('type','=','opportunity'),('active','=',True)], ['expected_revenue:sum'], ['stage_id']],
     {'lazy': False})

# ⑥ 我的进行中商机
call('crm.lead', 'search_read',
     [[('type','=','opportunity'),('user_id','=',uid),('won_status','=','pending')]],
     {'fields': ['name','partner_id','stage_id','expected_revenue','probability','date_deadline'],
      'order': 'priority desc, date_deadline asc'})
```
