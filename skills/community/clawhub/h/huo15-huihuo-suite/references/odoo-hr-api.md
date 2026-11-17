# Odoo 19 人力资源模块模型与 XML-RPC API 速查

> 源码核对：`~/workspace/study/odoo-19.0+e.20260501/odoo/addons/`（hr / hr_attendance / hr_holidays / hr_expense）

## ⚠️ v19 字段坑（最易错）

1. **hr.employee.name 是 related**：通过 `resource_id.name` 关联(store=True)，改 name 等于改 resource.name。
2. **部门用 complete_name**：`hr.department` 的 `name` 只是本层名字，`complete_name` 是层级全名（"总部/研发部"），**搜部门名用 complete_name**。
3. **考勤 check_in/check_out 是 Datetime/UTC**：和日历事件一样，脚本用 `from_utc` 转本地时间显示。
4. **签到/签退不走 hr.attendance.create**：走 `hr.employee._attendance_action_change`，它自动判断该签到还是签退（有未签退记录就签退，否则签到）。
5. **hr.leave 用 request_date_from/to（Date）**：不是 `date_from/date_to`（那俩是 Datetime/UTC，由 request_date_from/to + 员工时区 compute 出来）。
6. **hr.leave.number_of_days 是 compute**：由 `request_date_from`/`request_date_to` + `resource_calendar`（工作日历）算出来，**不可直接 write**。
7. **hr.leave.state**：`confirm`(待审批) → `validate1`(待二审) → `validate`(已批准) / `refuse`(已拒绝) / `cancel`(已取消)。
8. **请假审批走 action_approve**：单审 confirm→validate；双审 confirm→validate1→validate。拒绝用 `action_refuse`。
9. **v19 报销无 sheet**：`hr.expense.sheet` 已废弃（v19 直接在 `hr.expense` 上操作），有 `former_sheet_id` 字段保留旧分组数据。
10. **报销 state 7 值**：`draft`→`submitted`→`approved`→`posted`→`in_payment`→`paid`；`refused` 旁路。
11. **报销 payment_mode**：`own_account`(员工先垫后报销) / `company_account`(公司直接付)。
12. **报销 action_post 有副作用**：approved→posted 时自动建 `account.move` 凭证，不可逆。

---

## 一、hr.employee（员工）

`_order='name'`。继承 `resource.mixin`（有 `resource_id`）和 `mail.activity.mixin`。

### 核心字段

| 字段 | 含义 |
|---|---|
| name(姓名, related=resource_id.name, store) · active(在职, related=resource_id.active, store) · company_id(required) | 基础 |
| user_id(关联系统用户, m2o res.users, related=resource_id.user_id, store) · resource_id(resource.resource, required) · resource_calendar_id(工作日历) | 用户/资源 |
| department_id(部门 m2o hr.department) · job_id(岗位 m2o hr.job) · parent_id(直属上级 m2o hr.employee) · coach_id(导师 m2o hr.employee) · child_ids(下属 o2m) | 组织 |
| work_phone(工作电话) · mobile_phone(手机) · work_email(工作邮箱) · work_contact_id(工作联系人 m2o res.partner) | 联系 |
| private_phone(私人电话) · private_email(私人邮箱) · birthday(生日) · lang · place_of_birth · country_of_birth | 个人信息 |
| work_location_type(home/office/other) · work_location_name | 工作地点 |
| permit_no(工作许可号) · visa_no · visa_expire · has_work_permit · work_permit_expiration_date | 签证/许可 |
| bank_account_ids(银行账户 m2m res.partner.bank) · primary_bank_account_id(主账户) | 银行 |
| date_start(入职日期, related=version_id.date_start) · contract_date_start · contract_date_end · contract_wage · structure_type_id · contract_type_id | 合同(version 继承) |
| hr_presence_state(present/absent/archive/out_of_working_hour, compute) · last_activity · last_activity_time · newly_hired | 考勤/状态 |
| category_ids(标签 m2m hr.employee.category) · color · note | 标签 |
| version_id(版本 m2o hr.version) · version_ids(版本列表 o2m) · current_version_id · versions_count | 版本(历史) |

### 方法

| 方法 | 说明 |
|---|---|
| `_attendance_action_change` | 签到/签退（自动判断，有未签退就签退，否则签到） |

### 查询

- 在职员工：`('active','=',True)`
- 按部门(含子部门)：`('department_id','child_of',dept_id)`
- 按名字搜：`('name','ilike','张')`
- 当前用户关联的员工：`('user_id','=',uid)`

---

## 二、hr.department（部门）

`_order='name'`。`_rec_name='complete_name'`。`_parent_store=True`（层级树）。

### 核心字段

| 字段 | 含义 |
|---|---|
| name(本层名称) · complete_name(全名 "总部/研发部", compute recursive) · active · company_id · parent_id(上级部门 m2o self) · child_ids(子部门 o2m) · parent_path(层级路径) | 组织 |
| manager_id(负责人 m2o hr.employee) · member_ids(成员 o2m hr.employee, readonly, by department_id) · total_employee(人数, compute) · jobs_ids(岗位 o2m hr.job) · note · color | 人员 |

### 查询

- 全部活跃部门：`('active','=',True)`
- 搜层级名：`('complete_name','ilike','研发')`（注意 complete_name 是 compute，name_search 可用）

---

## 三、hr.attendance（考勤）

`_order='check_in desc'`。

### 核心字段

| 字段 | 含义 |
|---|---|
| employee_id(员工 m2o, required, ondelete=cascade) · department_id(部门, related from employee, readonly) · manager_id(上级, related, readonly) | 关联 |
| check_in(签到时间, Datetime/UTC, required) · check_out(签退时间, Datetime/UTC) · date(日期, Date, compute from check_in + tz, store) | 时间 |
| worked_hours(工时, Float, compute from check_out-check_in, store) · expected_hours(理论工时, compute) · overtime_hours(加班, compute) · overtime_status(to_approve/approved/refused, compute) | 工时 |
| in_latitude/in_longitude/in_location/in_ip_address/in_browser/in_mode(kiosk/systray/manual/technical) · out_* (签退对应) | 签到信息 |

### 方法

- 签到/签退不直接操作 `hr.attendance`，而是调 `hr.employee._attendance_action_change([emp_id])`

### 查询

- 某员工某天：`('employee_id','=',emp_id), ('date','=',today)`
- 未签退：`('employee_id','=',emp_id), ('check_out','=',False)`
- 某部门某月：`('employee_id.department_id','child_of',dept_id), ('date','>=','2026-08-01'), ('date','<=','2026-08-31')`

---

## 四、hr.leave（请假/休假）

`_order='date_from desc'`。

### 核心字段

| 字段 | 含义 |
|---|---|
| name(描述, compute from leave_type+dates, copy=False) · private_name(私密描述, hr_holidays_responsible group) · state(confirm/refuse/validate1/validate/cancel) | 标识/状态 |
| employee_id(员工 m2o, required) · user_id(用户, related from employee, store) · department_id(部门, compute, store) · company_id(compute, store) | 人员 |
| holiday_status_id(假期类型 m2o hr.leave.type, required) · validation_type(审批类型, related from leave_type) | 类型 |
| **request_date_from**(请求开始日, **Date**, 用户输入) · **request_date_to**(请求结束日, **Date**, 用户输入) | 请求日期 |
| date_from(开始 Datetime/UTC, **compute from request_date_from + tz**, store) · date_to(结束 Datetime/UTC, **compute**, store) | 实际日期 |
| number_of_days(天数, **compute** from request_dates + resource_calendar, store) · number_of_hours(小时, compute) · duration_display(显示文本, compute) | 时长 |
| request_unit_half(半天假, compute) · request_unit_hours(特定时间假, compute) · request_date_from_period(am/pm) | 特殊 |
| notes(原因, Text) · first_approver_id(一审 m2o hr.employee) · second_approver_id(二审 m2o hr.employee) · meeting_id(日历事件 m2o) | 其他 |

### 方法

| 方法 | 说明 |
|---|---|
| `action_approve` | 批准（单审 confirm→validate；双审 confirm→validate1，再调一次 validate1→validate） |
| `action_refuse` | 拒绝 |
| `action_draft` | 回草稿 |

### 创建请假

```python
call('hr.leave', 'create', [{
    'employee_id': 5,
    'holiday_status_id': 1,       # 假期类型 id（如年假/病假/事假）
    'request_date_from': '2026-08-10',   # Date，不是 Datetime
    'request_date_to': '2026-08-12',
    'notes': '家里有事',
}])
# 创建后默认 state='confirm'（待审批）
```

> 注意：不传 `date_from`/`date_to`，只传 `request_date_from`/`request_date_to`。
> `number_of_days` 由系统根据工作日历自动算（不含周末/节假日）。

### 查询

- 我的请假：`('employee_id.user_id','=',uid)`
- 待审批：`('state','in',('confirm','validate1'))`
- 已批准：`('state','=','validate')`
- 按员工：`('employee_id','=',emp_id)`
- 按部门(含子)：`('employee_id.department_id','child_of',dept_id)`

---

## 五、hr.leave.type（假期类型）

`_order='sequence'`。

| 字段 | 含义 |
|---|---|
| name(类型名) · sequence(排序) · active · color · icon_id · create_calendar_meeting(日历显示) | 基础 |
| leave_validation_type(no_validation/hr/manager/both) · requires_allocation(是否需要额度) · employee_requests(员工可申请额度) · allocation_validation_type | 审批/额度 |
| max_leaves(最大额度, compute) · leaves_taken(已休, compute) · virtual_remaining_leaves(剩余, compute, **searchable**) | 额度 |
| request_unit(day/hour/half_day) · responsible_ids(通知人 m2m res.users) · company_id · country_id | 配置 |

### 查询

- 需要额度的类型：`('requires_allocation','=',True)`
- 可用的类型（有额度或不需要额度）：`('|',('requires_allocation','=',False),('has_valid_allocation','=',True))`

---

## 六、hr.expense（报销）

`_order='date desc, id desc'`。

### 核心字段

| 字段 | 含义 |
|---|---|
| name(描述, compute from product, store) · date(日期, Date) · state(draft/submitted/approved/posted/in_payment/paid/refused, compute) · approval_state(approved/refused, copy=False) · approval_date | 标识/状态 |
| employee_id(员工 m2o, required) · department_id(部门, compute from employee, store) · manager_id(主管 m2o res.users, compute) · company_id | 人员 |
| product_id(产品 m2o product.product) · product_uom_id(单位, related) · name(描述, compute from product, store) · description(内部备注, Text) · quantity(数量, required, default=1) | 产品 |
| total_amount(总额, Monetary, company_currency) · total_amount_currency(原币总额, Monetary) · untaxed_amount_currency(未税原币) · tax_amount(税额公司币) · tax_amount_currency(税额原币) · currency_id · company_currency_id | 金额 |
| payment_mode(own_account=个人/company_account=公司, required) · vendor_id(供应商 m2o res.partner) · account_id(科目 m2o account.account) · tax_ids(税 m2m account.tax, domain purchase) · payment_method_line_id(付款方式 m2o) · journal_id(账簿, related) | 付款/税 |
| receipt_attachment_ids(收据附件 o2m ir.attachment) · duplicate_expense_ids(重复检测) · same_receipt_expense_ids · split_expense_origin_id(拆分来源) | 附件 |
| former_sheet_id(旧报告 id, Integer, 保留旧 sheet 数据) | 历史 |

### 方法

| 方法 | 说明 |
|---|---|
| `action_submit` | 提交 draft→submitted |
| `action_approve` | 批准 submitted→approved |
| `action_refuse` | 拒绝 →refused |
| `action_post` | 过账 approved→posted（**自动建 account.move 凭证**，不可逆） |
| `action_draft` | 回草稿 |
| `action_approve_duplicates` | 批量批准重复报销 |

### 创建报销

```python
call('hr.expense', 'create', [{
    'employee_id': 5,
    'product_id': 12,              # 可选，不传也能建
    'name': '差旅费',
    'quantity': 1,
    'total_amount': 200.0,
    'date': '2026-08-01',
    'payment_mode': 'own_account', # 个人先垫后报销
}])
```

### 查询

- 我的报销：`('employee_id.user_id','=',uid)`
- 草稿：`('state','=','draft')`
- 待批准：`('state','=','submitted')`
- 已批准：`('state','=','approved')`
- 按员工：`('employee_id','=',emp_id)`

---

## 脚本对应关系

| 脚本命令 | 模型方法 |
|---|---|
| `hr.py employees` | search_read hr.employee |
| `hr.py emp-show` | read hr.employee |
| `hr.py departments` | search_read hr.department |
| `hr.py attendance` | search_read hr.attendance |
| `hr.py check-in` | hr.employee._attendance_action_change |
| `hr.py check-out` | hr.employee._attendance_action_change |
| `hr.py leaves` | search_read hr.leave |
| `hr.py leave-add` | create hr.leave (request_date_from/to) |
| `hr.py leave-approve` | hr.leave.action_approve |
| `hr.py leave-refuse` | hr.leave.action_refuse |
| `hr.py expenses` | search_read hr.expense |
| `hr.py expense-add` | create hr.expense |
| `hr.py expense-submit` | hr.expense.action_submit |
| `hr.py expense-approve` | hr.expense.action_approve |
| `hr.py expense-refuse` | hr.expense.action_refuse |
| `hr.py expense-post` | hr.expense.action_post |
