# Odoo 19「测试验收」API / 字段知识沉淀

> 模块：自定义 `huo15.test.*`（菜单「测试验收」，仅本实例有，非 Odoo 官方）。  
> 本文是 `scripts/testing.py` 的字段坑与状态方法备忘，改脚本前必读。

---

## 1. 模型总览

| 模型 | 中文名 | 说明 |
|---|---|---|
| `huo15.test.bug` | 测试验收 Bug | 主模型，含 mail.thread + mail.activity mixin |
| `huo15.test.sprint` | 测试迭代 / Sprint | 一个项目下分迭代收口 Bug |
| `huo15.test.bug.tag` | 测试验收 Bug 标签 | 标签 / 模块分类（带颜色，可归档） |

---

## 2. `huo15.test.bug` 字段（fields_get 实测）

### 2.1 业务字段（脚本会用到）

| 字段 | 类型 | string | 关键点 |
|---|---|---|---|
| `bug_code` | char | Bug ID | `ir.sequence` 自动生成 `BUG-#####`；**只读**，create 时**不要传** |
| `name` | char | Bug 标题 | 必填 |
| `project_id` | m2o → project.project | 所属项目 | **create 必填**（否则报 `Missing required value for '所属项目'`） |
| `task_id` | m2o → project.task | 关联任务 | 可选；用于把 Bug 挂到具体任务 |
| `sprint_id` | m2o → huo15.test.sprint | 迭代 | 可选 |
| `found_version` | char | 发现版本 | 可选 |
| `tag_ids` | m2m → huo15.test.bug.tag | 标签/模块 | `[(6,0,[ids])]`；标签带 `color` 字段 |
| `severity` | selection | 严重程度 | `serious`/`high`/`medium`/`low` |
| `priority` | selection | 优先级 | `p0`/`p1`/`p2`/`p3`（**不是数字 0-3**，与 project.task 的 0-3 不同！） |
| `state` | selection | 状态 | `new`/`confirmed`/`in_progress`/`resolved`/`closed` |
| `resolution` | selection | 处理结论 | `fixed`/`wontfix`/`duplicate`/`cannotreproduce`/`bydesign` |
| `reporter_id` | m2o → res.users | 呈报人 | 默认当前用户 |
| `report_date` | date | 呈报日期 | 默认今日 |
| `assignee_id` | m2o → res.users | 解决人 | 直接 `write({'assignee_id': uid})`，**没有 action_assign** |
| `verifier_id` | m2o → res.users | 验收人 | 由 `action_verify` 写入**当前用户**，不要手动 write |
| `cc_user_ids` | m2m → res.users | 抄送人 | `[(6,0,[ids])]` |
| `resolve_date` | date | 实际解决日期 | 由 `action_resolve` 写入今日 |
| `verify_date` | date | 验收日期 | 由 `action_verify` 写入今日 |
| `reopen_count` | integer | 打回次数 | 由 `action_reopen` 每次 +1，**只读** |
| `duplicate_of_id` | m2o → self | 重复于 | `action_mark_duplicate` 前必须先 write 设此字段 |
| `related_bug_ids` | m2m → self | 关联 Bug | `[(6,0,[ids])]` |
| `description` | html | Bug 描述 | 纯文本会原样存，建议包 `<p>` |
| `note` | text | 备注 | 纯文本 |
| `effective_hours` | float | 累计工时 | computed，聚合 `timesheet_ids`（account.analytic.line），只读 |
| `timesheet_ids` | one2many → account.analytic.line | 工时单 | 走 timesheet.py 已有能力 |
| `company_id` | m2o → res.company | 公司 | 默认当前公司 |

### 2.2 mail.thread / mail.activity mixin 自带（不用手写）
`message_ids` / `message_follower_ids` / `message_partner_ids` / `activity_ids` / `activity_state` / `activity_date_deadline` / `activity_user_id` / `activity_exception_decoration` / `has_message` / `message_needaction` 等。要给 Bug 加跟进活动走 `activity.py`，`--model huo15.test.bug --id <bug_id>`。

### 2.3 字段坑速查（改脚本前对照）

| 坑 | 正确做法 |
|---|---|
| **必填 project_id** | create 时一定带 `project_id`；测试自测残留 Bug 用项目 54（域品汇）之类 |
| **priority 是字符串 p0-p3** | 不是 project.task 的 0/1/2/3 数字！脚本做 1→p1 映射 |
| **state 不用手动 write** | 全走 action_* 方法，否则 resolve_date/verify_date/verifier_id/reopen_count 不会被写 |
| **action_verify 的 verifier** | 是**当前登录用户**，不能预指派；要让 A 验收就得 A 自己登录 |
| **duplicate 要两步** | 先 `write({'duplicate_of_id': X})` 再 `action_mark_duplicate` |
| **reopen_count 只读** | 只能靠 `action_reopen` +1 |
| **bug_code 不能传** | create 传 `bug_code` 会被忽略/覆盖，交给序列 |
| **unlink 受限** | 普通 `Role/User` 不能删，仅 `测试验收/管理员`（见 §6） |
| **无 active 字段** | Bug **不能归档**（archive），只能推进到 closed |
| **severity≠priority** | severity（serious/high/medium/low）是「严重度」；priority（p0-p3）是「优先级」，两者独立 |

---

## 3. Bug 状态机（来自 form 视图 id=6358 的 header 按钮）

```
 action_confirm   action_start      action_resolve     action_verify
 new ────────▶ confirmed ──────▶ in_progress ──────▶ resolved ──────▶ closed
                                                  │
                                   action_reopen  │ reopen_count++
                                       └──────────┘
```

| 方法 | 前置 state | 后置 state | 写入字段 |
|---|---|---|---|
| `action_confirm` | new | confirmed | — |
| `action_start` | confirmed | in_progress | — |
| `action_resolve` | in_progress | resolved | `resolution='fixed'`, `resolve_date=today` |
| `action_verify` | resolved | closed | `verifier_id=<current user>`, `verify_date=today` |
| `action_reopen` | resolved | in_progress | `reopen_count += 1`（**不改 resolution**，保留 fixed 痕迹） |
| `action_close_wontfix` | ≠ closed | closed | `resolution='wontfix'` |
| `action_mark_duplicate` | ≠ closed 且 `duplicate_of_id` 已设 | closed | `resolution='duplicate'` |
| `action_reset` | closed | new | 清空状态相关字段 |

**实测验证**（2026-07-09，账号赵博 uid=5）：全 8 个方法在 `execute_kw` 远程调用下均成功，无需 context 参数。

调用示例：
```python
odoo.execute_kw("huo15.test.bug", "action_resolve", [[bug_id]], {})
```

> **禁止** `odoo.write("huo15.test.bug", [id], {"state": "resolved"})` —— 这样 `resolve_date` / `resolution` 不会被写。

---

## 4. `huo15.test.sprint` 字段

| 字段 | 类型 | string | 关键点 |
|---|---|---|---|
| `name` | char | 迭代名称 | 必填，如 `2026-07 冲刺` |
| `project_id` | m2o → project.project | 所属项目 | 可选 |
| `date_start` / `date_end` | date | 起止日期 | 可选 |
| `state` | selection | 状态 | `planned` → `active` → `done` |
| `description` | text | 迭代目标 / 说明 | 可选 |
| `bug_ids` | one2many → huo15.test.bug | Bug | 反向，通过 bug.sprint_id |
| `bug_count` | integer | Bug 总数 | computed |
| `bug_closed_count` | integer | 已关闭 | computed |
| `progress` | float | 完成率(%) | computed = closed/count |

### Sprint 状态机（form 视图 id=6366）

| 方法 | 前置 | 后置 |
|---|---|---|
| `action_start` | planned | active |
| `action_done` | active | done |
| `action_reset` | ≠ planned | planned |

把 Bug 挂到 Sprint：`write({'sprint_id': sprint_id})`（无需专用方法）。

---

## 5. `huo15.test.bug.tag` 字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `name` | char | 标签名称 |
| `color` | integer | 颜色索引（0-11，对应 Odoo 颜色选择器） |
| `active` | boolean | 启用（可 archive，默认 True） |

普通用户可创建标签（无 group 限制实测通过）。

---

## 6. 权限（ir.model.access 实测）

| 模型 | 操作 | 允许组 |
|---|---|---|
| `huo15.test.bug` | create / read / write | `Role / User`（全员） |
| `huo15.test.bug` | **unlink（删除）** | **仅 `测试验收 / 管理员`**（group full_name=`测试验收 / 管理员`，id=178） |
| `huo15.test.sprint` | CRUD | 全员 |
| `huo15.test.bug.tag` | CRUD | 全员 |

组结构（`res.groups`）：
- `测试验收 / 用户`（id=177）
- `测试验收 / 管理员`（id=178）

> 删除失败的原始报错：
> ```
> The operation cannot be completed: 不允许删除"测试验收 Bug"（huo15.test.bug）记录。
> 允许对以下组进行此操作：测试验收/管理员
> ```
> 脚本 `bug-delete` 命令应捕获并翻译为友好提示。

---

## 7. 名字 → id 解析约定（沿用 project.py 模式）

| 入参 | 解析 |
|---|---|
| `项目名` / 项目 id | `name_search('project.project', name)` |
| `我` / `me` / `self` | 当前 `uid` |
| 用户名 | `name_search('res.users', name, args=[['share','=',False]])` |
| 迭代名 / id | `name_search('huo15.test.sprint', name)` |
| 标签名 / id | `name_search('huo15.test.bug.tag', name)` |
| 任务名 / id | `name_search('project.task', name)` |
| 重复于 Bug | 可传 `BUG-00001` 或数字 id 或标题模糊匹配 |

---

## 8. 菜单结构（ir.ui.menu）

```
测试验收 (id=1117, seq=55, 顶级)
├── Bug 管理      (id=1118, seq=10, act=1646)  我的 Bug（默认指派给我）
├── 全部 Bug      (id=1123, seq=12, act=1642)  全部
├── 迭代 / Sprint (id=1122, seq=15, act=1645)
├── 统计分析      (id=1119, seq=20, act=1644)  graph+pivot
└── 配置 (id=1120, seq=90)
    └── 标签 / 模块 (id=1121, seq=10, act=1643)
```

---

## 9. 序列

`ir.sequence` id=47：`name='测试验收 Bug 编号'`, `prefix='BUG-'`, `padding=5`, `number_next=6`。  
→ 下一个 Bug 编号会从 `BUG-00006` 起（前 5 个是真实数据 BUG-00001..00005）。

---

## 10. 与其他应用的联动

- **project**：Bug 的 `project_id` / `task_id` 直连项目任务。
- **timesheet**：Bug 的 `timesheet_ids` = `account.analytic.line`，可用 `timesheet.py log --project <项目> --task <task>` 录，但更准的做法是 `write({'timesheet_ids': [(0,0,{...})]})`（后续版本封装）。
- **activity**：`activity.py add --model huo15.test.bug --id <bug_id> --type call --date ...` 给 Bug 加跟进。
- **briefing**（后续）：聚合「我的活跃 Bug（state in new/confirmed/in_progress/resolved 且 assignee=我）」进每日总览。
