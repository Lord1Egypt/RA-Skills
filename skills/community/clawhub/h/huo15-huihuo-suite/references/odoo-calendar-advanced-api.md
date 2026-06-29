# Odoo 19 日历高级操作 API 速查（重复 / 参与人 / 忙闲 / 关联）

> 源码核对：`~/workspace/study/odoo/odoo-19.0+e.20260501/odoo/addons/calendar/`
> 文件：`models/calendar_event.py`、`calendar_recurrence.py`、`calendar_attendee.py`、`calendar_event_type.py`；CRM 关联在 `crm/models/calendar.py`。
> 基础字段见 [odoo-activity-calendar-api.md](odoo-activity-calendar-api.md)。

## ⚠️ 最易错的 9 条

1. 重复参数走 **`calendar.event` 的 create/write**，别直接 CRUD `calendar.recurrence`（伪 related 自动建/改）。
2. `rrule` 串是 **只读 compute**，传结构化字段（rrule_type/mon../interval/...）。
3. **`recurrency=True` 是开关**，缺了不生成系列。
4. 改重复参数必须配 **`recurrence_update`**（future_events/all_events），否则 UserError；**`all_events` 不能改时间**（改时间用 future_events）。
5. `show_as` 默认 **busy**；找空闲 domain 带 `('show_as','=','busy')`，区间重叠用 `stop>=winStart AND start<=winEnd`，时间用 **naive UTC**。
6. 加/减参与人用 `partner_ids` 的 `(4,id)`/`(3,id)`/`(6,0,[...])`，attendee 自动联动，**不支持 0/1 command**。
7. crm.lead 用 **`opportunity_id`** 关联；其它模型用 **`res_model_id`**+`res_id`（写 res_model_id，不是只读的 res_model）。
8. weekly 用**小写布尔** `mon/tue/...`；monthly「第几个周几」用**大写** `weekday`(MON) + `byday`(1/2/3/4/-1)。别混。
9. 代他人接受/拒绝优先**直接对 `calendar.attendee` 调 `do_accept`/`do_decline`/`do_tentative`**（public、跨 partner）；`change_attendee_status` 只动当前登录用户自己的。

## 1. 重复事件（recurrency / rrule）

calendar.event 上的伪 related 重复字段（真正存储在 `calendar.recurrence`）：

| 字段 | 值 |
|---|---|
| `recurrency` | Boolean，**开关，必须 True** |
| `rrule_type` | `daily`/`weekly`(默认)/`monthly`/`yearly` |
| `interval` | 正整数，每隔几 |
| `end_type` | `count`(默认)/`end_date`/`forever` |
| `count` | 次数（end_type=count） |
| `until` | Date（end_type=end_date） |
| `mon`..`sun` | 7 个小写布尔（weekly 选周几） |
| `month_by` | `date`(按几号)/`day`(按第几个周几) |
| `day` | 第几号（month_by=date，1-31） |
| `weekday` | `MON`..`SUN` 大写（month_by=day） |
| `byday` | `1`/`2`/`3`/`4`/`-1`(Last)（month_by=day） |
| `event_tz` | 时区，**强烈建议传** `Asia/Shanghai`（决定周起算/DST） |

> `forever` 实际按 `calendar.max_recurrence_years`(默认15年) + `MAX_RECURRENT_EVENT=720` 封顶。

**创建 vals 示例**（时间 naive UTC）：
```python
# 每周一9点：rrule_type='weekly', interval=1, mon=True
# 每日站会：rrule_type='daily', interval=1, end_type='forever'
# 每月1号：rrule_type='monthly', month_by='date', day=1
# 每月第二个周一：rrule_type='monthly', month_by='day', weekday='MON', byday='2'
{'name':'周例会','start':'2026-06-29 01:00:00','stop':'2026-06-29 02:00:00',
 'recurrency':True,'rrule_type':'weekly','interval':1,'mon':True,
 'event_tz':'Asia/Shanghai','end_type':'count','count':52,'partner_ids':[(4,p1)]}
```

**修改重复事件** `recurrence_update`（store=False，write 时随 vals 传）：`self_only`(默认,只改这个) / `future_events`(这个及将来) / `all_events`(全部)。
- 对**单个 occurrence 的 id** write，带 `'recurrence_update':'future_events'`。
- 改重复参数用 self_only → UserError；改时间用 all_events → 被禁（用 future_events）。

**删除**：删单个 `unlink([occ_id])`；删系列调 `action_mass_deletion(setting)`（`[[id], 'future_events'|'all_events']`）；归档 `action_mass_archive(setting)`。

## 2. 参与人响应（attendee）

`calendar.attendee.state`：`accepted`(Yes) / `declined`(No) / `tentative`(Maybe) / `needsAction`(默认,待回复)。

**回复方法**（public，对 attendee 记录调，可跨任意 partner）：`do_accept()` / `do_decline()` / `do_tentative()`。
```python
att = call(ATTENDEE,'search',[[('event_id','=',eid),('partner_id','=',pid)]])
call(ATTENDEE,'do_accept',[att])   # 代该 partner 接受
```
> event 上的 `change_attendee_status(status, setting)` 只动**当前登录用户**自己的 attendee。代别人必须走上面的 attendee.do_xxx。

**查响应**：读 event 的 `attendee_ids` → 读 attendee 的 `partner_id`/`common_name`/`state`。统计字段（非存储 compute）：`accepted_count`/`declined_count`/`tentative_count`/`awaiting_count`(=needsAction)。

## 3. 更新事件 + 加减参与人

- 改 start/stop/location：直接 write（改时间触发重排 alarm + 给将来事件参与人发改期通知；别人改时间会把组织者 attendee 重置 needsAction）。
- 加减参与人：write `partner_ids` 用 `(4,id)` 加 / `(3,id)` 减 / `(6,0,[...])` 替换，attendee 自动联动；加人会给新参与人发邀请（仅未来事件）。**不支持 (0,..)/(1,..)**。

## 4. 忙闲 / 找空闲

`show_as`：`free`(Available,查忙闲时忽略) / `busy`(Busy,默认)。
```python
# 查 partner 在 [lo,hi) 是否有占用（区间重叠 + busy）
n = call('calendar.event','search_count',[[
    ('partner_ids','in',[pid]), ('stop','>=',lo), ('start','<=',hi), ('show_as','=','busy')]])
# n==0 → 空闲。时间用 naive UTC。背靠背不算冲突就用 stop>lo AND start<hi
```
辅助：event 上 `unavailable_partner_ids`（compute）= 该事件参与人里同时段还有别的 busy 事件的人（撞期提示）。

## 5. 关联业务记录

- **crm.lead → 用 `opportunity_id`**（Many2one crm.lead，自动同步 res_model/res_id + 在 lead 上 log_meeting；lead 有反向 `calendar_event_ids`）。
  ```python
  call(EVENT,'create',[{'name':'洽谈','start':..,'stop':..,'opportunity_id':88}])
  call(EVENT,'search',[[('opportunity_id','=',88)]])   # 反查商机的会议
  ```
- **其它模型 → 用 `res_model_id`(写它,不是只读 res_model) + `res_id`**。
  ```python
  mid = call('ir.model','search',[[('model','=','project.task')]])[0]
  call(EVENT,'create',[{'name':'任务评审','start':..,'stop':..,'res_model_id':mid,'res_id':tid}])
  call(EVENT,'search',[[('res_model','=','project.task'),('res_id','=',tid)]])
  ```

## 6. 事件标签（calendar.event.type）

`name`(required,全局唯一) + `color`。event 用 `categ_ids`(m2m)。
```python
tid = call('calendar.event.type','create',[{'name':'客户拜访'}])
call(EVENT,'write',[[eid],{'categ_ids':[(4,tid)]}])   # 不存在可 (0,0,{'name':..})
```

## 7. XML-RPC 示例

```python
def call(m,meth,a,kw=None): return models.execute_kw(db,uid,pw,m,meth,a,kw or {})

# ① 每周一9点周会
call('calendar.event','create',[{'name':'周例会',
  'start':'2026-06-29 01:00:00','stop':'2026-06-29 02:00:00','recurrency':True,
  'rrule_type':'weekly','interval':1,'mon':True,'event_tz':'Asia/Shanghai',
  'end_type':'count','count':52,'partner_ids':[(4,p1),(4,p2)]}])

# ② 查参与人响应
ev = call('calendar.event','read',[[eid]],{'fields':['attendee_ids','accepted_count','awaiting_count']})[0]
call('calendar.attendee','read',[ev['attendee_ids']],{'fields':['common_name','state']})

# ③ 代某参与人接受
att = call('calendar.attendee','search',[[('event_id','=',eid),('partner_id','=',pid)]])
call('calendar.attendee','do_accept',[att])

# ④ 改重复事件"将来所有"的地点
call('calendar.event','write',[[occ_id],{'location':'3楼A','recurrence_update':'future_events'}])

# ⑤ 查某人明天下午忙闲（14-18点 Asia/Shanghai = 06-10 UTC）
busy = call('calendar.event','search_count',[[('partner_ids','in',[pid]),
  ('stop','>=','2026-06-25 06:00:00'),('start','<=','2026-06-25 10:00:00'),('show_as','=','busy')]])

# ⑥ 会议关联 crm.lead#88
call('calendar.event','create',[{'name':'商机洽谈','start':..,'stop':..,'opportunity_id':88}])
```
