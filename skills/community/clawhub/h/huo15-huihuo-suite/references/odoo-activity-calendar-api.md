# Odoo 19 活动 / 日历 / 提醒 模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/`
> 文件：`mail/models/mail_activity.py`、`mail_activity_type.py`、`mail_activity_mixin.py`、`calendar/models/calendar_event.py`、`calendar_alarm.py`、`calendar_attendee.py`。

## ⚠️ 最易错的 7 条

1. `mail.activity.date_deadline` 是 **Date**（不是 datetime）。
2. 活动**完成 = archive**（`active=False`），不是删除；用 `action_feedback`，记录仍在（`state='done'`、填 `date_done`）。
3. `mail.activity.state` 是 **computed 无 search** —— 查逾期/今日用 `date_deadline` 比较 + `active=True`，别在 domain 写 `state`。
4. `calendar.event.start/stop` 是 **Datetime / UTC**；allday 用 `start_date/stop_date`（Date）但 start/stop 仍存。
5. 写 `calendar.event.partner_ids` 会**自动建参与人**（calendar.attendee），不用手动建。
6. `calendar.alarm.alarm_type` 只有 **`notification` / `email`**（基础模块无 sms）。
7. 活动有行级权限：非超管只看分配给自己或对关联文档有读权的活动。

## 1. mail.activity（活动 = 挂在任意记录上的下一步待办/提醒）

`_order='date_deadline ASC, id ASC'`。

| 字段 | 类型 | 含义 |
|---|---|---|
| `res_model` | Char（related, store） | 关联模型技术名（如 `crm.lead`），**可直接写** |
| `res_model_id` | M2o→ir.model | 关联模型 |
| `res_id` | Many2oneReference | 关联记录 id |
| `res_name` | Char（compute store） | 关联记录显示名 |
| `activity_type_id` | M2o→mail.activity.type | 活动类型 |
| `summary` | Char | 摘要/标题 |
| `note` | Html | 备注 |
| `date_deadline` | **Date**（required） | 截止日 |
| `date_done` | Date（compute store） | 完成日（archive 时填） |
| `user_id` | M2o→res.users | 负责人（不传**不会**自动给当前用户） |
| `state` | Selection（**computed 无 search**） | `overdue`/`today`/`planned`/`done` |
| `active` | Boolean | 完成=False |
| `calendar_event_id` | M2o→calendar.event | 关联会议 |

**state 算法**：`not active`→done；否则按 `date_deadline - 今天`：=0→today，<0→overdue，>0→planned。

**活动类型 xmlid**（`mail.activity.type`）：`mail.mail_activity_data_todo`（待办）/`_call`（电话）/`_meeting`（会议）/`_email`（邮件）/`_upload_document`（上传文档）。

**创建（正道）**：mixin 方法 `activity_schedule(act_type_xmlid='', date_deadline=None, summary='', note='', **act_values)`（`mail_activity_mixin.py:357`）。在目标记录上调，自动解析 xmlid、置 `automated=True`。`date_deadline` 传 date 字符串。也可直接 `create mail.activity`（要自己填 res_model_id/res_id/activity_type_id）。

**完成**：`action_feedback(feedback=False, attachment_ids=None)`（`mail_activity.py:482`）——发 chatter + archive。`action_done()` 是无反馈包装；`action_feedback_schedule_next(...)` 完成并排下一个。

**取消**：`unlink`（或 `action_cancel`）。**改期**：write `date_deadline`。

**我的活动 domain**：
```python
[('user_id','=',uid), ('active','=',True), ('date_deadline','<=', today)]  # 逾期+今日
# 逾期 date_deadline<today；今日 ==today；计划 >today。别用 state（无 search）
```

## 2. calendar.event（日历事件/会议）

继承 mail.activity.mixin / mail.thread / resource.mixin。

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char（required） | 主题 |
| `start` | **Datetime/UTC**（required） | 开始 |
| `stop` | Datetime（compute store, 可写） | 结束 |
| `duration` | Float（小时，compute store, 可写） | 时长（写 start+duration 自动算 stop） |
| `allday` | Boolean | 全天 |
| `start_date`/`stop_date` | Date | 仅 allday 用（非 allday 为 False） |
| `location` | Char | 地点 |
| `description` | Html | 描述 |
| `user_id` | M2o→res.users | 组织者（默认当前用户） |
| `partner_ids` | **M2m→res.partner** | 参与人（写它自动建 attendee） |
| `attendee_ids` | O2m→calendar.attendee | 参与人状态 |
| `alarm_ids` | **M2m→calendar.alarm** | 提醒 |
| `privacy` | Selection | `public`/`private`/`confidential` |
| `show_as` | Selection（required, 默认 busy） | `free`/`busy` |
| `recurrency`/`rrule` | Boolean/Char | 重复（rrule_type daily/weekly/monthly/yearly） |

**allday vs 带时间**：带时间用 `start`/`stop`（UTC）+ `duration` 联动；allday 给 `allday=True` + `start`/`stop`（compute 自动填 start_date/stop_date 最稳）。

**我的日程 domain**（组织者或参与人 + start 范围）：
```python
['&', '|', ('user_id','=',uid), ('partner_ids','in',[my_partner_id]),
      '&', ('start','>=',utc_lo), ('start','<',utc_hi)]
# my_partner_id = res.users.read([uid],['partner_id']); start 边界先本地→UTC
```

## 3. calendar.alarm（提醒）

| 字段 | 类型 | 含义 |
|---|---|---|
| `name` | Char | 名称 |
| `alarm_type` | Selection（required） | **`notification` / `email`**（无 sms） |
| `duration` | Integer（required） | 提前量数值 |
| `interval` | Selection（required） | `minutes`/`hours`/`days` |
| `duration_minutes` | Integer（compute store） | 折算分钟（可 search） |

**给事件加提醒**（m2m 命令）：
```python
event.write({'alarm_ids': [(0,0,{'name':'提前15分钟','alarm_type':'notification','duration':15,'interval':'minutes'})]})  # 内联建
event.write({'alarm_ids': [(4, alarm_id)]})   # 复用已有
```
预置 alarm 外部 id：`calendar.alarm_notif_1`(15min)/`_2`(30min)/`_3`(1h)/`_4`(2h)/`_5`(1day)；`calendar.alarm_mail_1`(email 3h)/`_2`(6h)。

## 4. XML-RPC 实战示例

```python
def call(m, meth, args, kw=None): return models.execute_kw(db, uid, pw, m, meth, args, kw or {})
from datetime import date, timedelta
today = date.today().isoformat()

# ① 给 crm.lead#88 加"3天后回访"活动（走 mixin）
call('crm.lead', 'activity_schedule', [[88]], {
    'act_type_xmlid': 'mail.mail_activity_data_call', 'summary': '3天后回访',
    'note': '<p>电话回访</p>', 'date_deadline': (date.today()+timedelta(days=3)).isoformat(), 'user_id': uid})

# ② 我的逾期+今日活动
call('mail.activity', 'search_read',
    [[('user_id','=',uid),('active','=',True),('date_deadline','<=',today)]],
    {'fields':['summary','res_name','date_deadline','activity_type_id'], 'order':'date_deadline asc'})

# ③ 标记活动完成（archive）
call('mail.activity', 'action_feedback', [[act_id]], {'feedback': '已回访'})

# ④ 新建日历事件（明天10-11点+地点+2参与人，start/stop 是 UTC）
call('calendar.event', 'create', [{
    'name': '方案评审', 'start': '2026-06-10 02:00:00', 'stop': '2026-06-10 03:00:00',  # UTC(本地10点=UTC2点)
    'location': '会议室A', 'user_id': uid, 'partner_ids': [(6,0,[11,22])]}])

# ⑤ 给事件加"提前30分钟通知"
call('calendar.event', 'write', [[event_id, {}][0]], {'alarm_ids':[(0,0,{
    'name':'提前30分钟','alarm_type':'notification','duration':30,'interval':'minutes'})]})

# ⑥ 我本周日历事件
my_partner = call('res.users','read',[[uid],['partner_id']])[0]['partner_id'][0]
call('calendar.event','search_read',
    [['&','|',('user_id','=',uid),('partner_ids','in',[my_partner]),
      '&',('start','>=','2026-06-01 00:00:00'),('start','<','2026-06-08 00:00:00')]],
    {'fields':['name','start','stop','allday','location','alarm_ids'],'order':'start asc'})
```
