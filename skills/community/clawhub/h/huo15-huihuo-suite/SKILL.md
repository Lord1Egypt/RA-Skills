---
name: huo15-huihuo-suite
displayName: 辉火套件ERP
description: >-
  Use this skill whenever the user wants to manage their work in the 火一五/辉火云
  company Odoo system (www.huo15.com, db=huo15) — to-dos / tasks ("记个待办"
  "加任务" "我的待办"), projects, timesheets ("记工时"), CRM leads & opportunities
  ("新建商机" "跟进客户" "销售管道"), follow-up activities & reminders ("提醒我"
  "3天后回访"), calendar events & meetings ("安排会议" "我这周日程" "提前30分钟提醒"),
  knowledge-base articles ("查/写知识库" "产品手册"), or document files ("找文档"
  "上传文件"). Also a one-stop "我今天/本周要做什么" briefing. Triggers on odoo,
  辉火云企业套件, 公司系统, /odoo/to-do /project /timesheets /crm /calendar
  /knowledge /documents /sale /purchase /inventory, or "登录公司系统/保存 odoo 账号". Treat bare work-context
  mentions of 待办/任务/项目/工时/客户/商机/会议/日程/提醒/知识库/文档/销售/采购/库存/订单/发货/收货 as this skill.
  First run: login.py init (地址/数据库/账号/密码 → ~/.huo15/tools.md). Pure
  standard library, zero dependencies.
version: 1.5.0
aliases:
  - 火一五odoo技能
  - 火一五Odoo技能
  - 辉火云odoo
  - odoo待办
  - odoo项目
  - odoo工时单
  - 公司系统待办
  - 公司系统项目
  - 公司系统工时单
  - 公司系统CRM
  - odoo商机
  - odoo-crm
  - 销售管道
  - 客户管理
  - 商机管理
  - 活动管理
  - odoo日历
  - 日程安排
  - 会议提醒
  - 公司系统日历
  - 待办事项
  - 记待办
  - 加任务
  - 跟进客户
  - 提醒我
  - 安排会议
  - 记工时
  - 知识库
  - odoo文档
  - 产品手册
  - 我今天要做什么
  - 本周安排
  - huo15-odoo
  - huo15-suite
  - 辉火套件ERP
  - 辉火套件
  - 辉火ERP
  - odoo销售
  - odoo采购
  - 库存查询
  - 销售订单
  - 采购订单
dependencies:
  python-packages: []   # 纯标准库，无第三方依赖
---

# 辉火套件ERP v1.5

通过 XML-RPC / JSON-RPC 操作公司 Odoo 系统（**辉火云企业套件**，www.huo15.com，db=`huo15`）。
十一大能力：**待办**、**项目**、**工时单**、**CRM**、**活动**、**日历**、**知识库**、**文档**、**销售**（/odoo/sale）、**采购**（/odoo/purchase）、**库存**（/odoo/inventory），外加 `briefing.py` 每日/每周总览。

> **完整命令** → [references/commands.md](references/commands.md)
> **API/字段细节** → [todo](references/odoo-todo-api.md) · [project](references/odoo-project-api.md) · [timesheet](references/odoo-timesheet-api.md) · [crm](references/odoo-crm-api.md) · [activity+calendar](references/odoo-activity-calendar-api.md) · [calendar-advanced](references/odoo-calendar-advanced-api.md) · [knowledge+documents](references/odoo-knowledge-documents-api.md) · [sales+purchase+stock](references/odoo-sales-purchase-stock-api.md)

## 触发场景

- "帮我登录公司系统" / "连一下 odoo" / "保存我的 odoo 账号"
- "新建一个待办：xxx，截止周五" / "把待办 123 标记完成" / "看我的待办"
- "看一下 X 项目" / "给 X 项目加个任务" / "把任务移到进行中" / "改任务负责人"
- "统计这个月每个员工的工时" / "看 X 项目的工时" / "研发部本月工时报表"
- "看我的商机/销售管道" / "新建商机" / "把商机标记赢单/输单" / "线索转商机" / "按阶段统计 pipeline"
- "看我的活动/待跟进" / "给这个商机加个3天后回访" / "我这周有什么日程/会议" / "建个会议提醒我" / "提前30分钟提醒"
- "查/写知识库" / "产品手册放哪" / "找个文档/上传文件" / "**我今天要做什么**" / "本周安排"
- "建个报价单/销售订单" / "确认这个订单" / "建采购单/询价单" / "查 X 产品库存还有多少" / "看待收货/待发货" / "验证出入库"

---

## ⚠️ 第一步：凭据初始化（首次必做）

所有脚本都依赖已保存的凭据。**没配过就先初始化这 4 项，别直接跑 todo/project/timesheet。**

| # | 输入项 | 示例 | 说明 |
|---|---|---|---|
| ① | 公司系统地址 | `www.huo15.com` | 只输域名即可，脚本自动补 `https://` |
| ② | 数据库 | `huo15` | 数据库名 |
| ③ | 账号 | 邮箱 / 用户名 | 登录账号 |
| ④ | 密码 | 密码或 API Key | 推荐 API Key（偏好设置→账户安全→新建，可随时吊销） |

保存到 `~/.huo15/tools.md`（权限 600）。

### 方式 A：Claude 代配（默认，在对话里完成）

1. 在对话里**依次问用户这 4 项**（地址 / 数据库 / 账号 / 密码），不要自己编。
2. 用 stdin 传密码（避免明文进 shell 历史 / ps）：

```bash
printf '%s' "<用户输入的密码>" | python3 scripts/login.py set \
    --url www.huo15.com --db huo15 --login "<账号>" --auth-type password
# 密码填的是 API Key 就把 --auth-type 换成 apikey
```

### 方式 B：用户自助初始化（密码不回显）

```bash
python3 scripts/login.py init     # 交互式依次提示输入 ①地址 ②数据库 ③账号 ④密码（无参等效）
```

login.py 会**先验证连接成功才落盘**，写入 `~/.huo15/tools.md`（权限 600）；失败报中文原因（账号错 / db 错 / 网络）。验证：`python3 scripts/login.py test`。

> 凭据文件默认 `~/.huo15/tools.md`，可用环境变量 `HUO15_TOOLS_MD` 改路径。
> 临时/CI 可用环境变量免落盘：`HUO15_ODOO_LOGIN` / `HUO15_ODOO_SECRET` / `HUO15_ODOO_DB` / `HUO15_ODOO_URL`。
> **此文件含明文凭据，务必不要提交 git。**

---

## 四大应用速览

每个应用一个脚本，风格统一（`add`/`list`/… 子命令，名字可代 id，`--json` 输出，`-h` 看完整参数）。
**完整命令示例 → [references/commands.md](references/commands.md)；字段/API 细节 → 各 `references/odoo-<app>-api.md`。**

| 应用 | 脚本 | 核心模型 | 主要子命令 |
|---|---|---|---|
| 📝 待办 `/odoo/to-do` | `todo.py` | project.task（私有态） | `add` `list` `done` `reopen` `cancel` `update` `stages` |
| 📁 项目 `/odoo/project` | `project.py` | project.project + task | `list` `show` `add` `edit` `archive` `tasks` `task-add` `task-move` `task-assign` `task-done` |
| ⏱️ 工时单 `/odoo/timesheets` | `timesheet.py` | account.analytic.line | `by-employee` `by-project` `by-month` `detail` `log` |
| 💼 CRM `/odoo/crm` | `crm.py` | crm.lead（线索/商机） | `list` `show` `add` `move` `won` `lost` `restore` `convert` `pipeline` `activity` |
| 🔔 活动 My Activities | `activity.py` | mail.activity | `list` `add` `done` `cancel` `reschedule` |
| 📅 日历 `/odoo/calendar` | `agenda.py` | calendar.event + alarm + attendee | `list` `show` `add` `update` `cancel` `remind` `invite` `attendees` `rsvp` `busy`（含重复事件/忙闲查询） |
| 📚 知识库 `/odoo/knowledge` | `knowledge.py` | knowledge.article | `list` `search` `show` `add` `fav` `tree` `move` |
| 📁 文档 `/odoo/documents` | `documents.py` | documents.document | `folders` `list` `search` `upload` `link` `tags` `tag` |
| 🛒 销售 `/odoo/sale` | `sales.py` | sale.order | `list` `show` `add` `confirm` `cancel` `invoice` |
| 🛍️ 采购 `/odoo/purchase` | `purchase.py` | purchase.order | `list` `show` `add` `confirm` `approve` `cancel` `bill` |
| 📦 库存 `/odoo/inventory` | `stock.py` | stock.quant/picking/move | `qty` `pickings` `show` `validate` `locations` `warehouses` |
| 🗓️ 每日总览 | `briefing.py` | 聚合待办+活动+会议 | `briefing.py [today\|week]` —— 一站式「我今天/本周要做什么」 |

下方「命令速查」给最常用命令的具体写法，够日常用；要完整参数/示例读 [references/commands.md](references/commands.md)。

---

## 命令速查

| 想做 | 命令 |
|---|---|
| 初始化(交互) | `python3 scripts/login.py init` —— 提示输入 地址/数据库/账号/密码 |
| 配登录(代配) | `printf '%s' "$PWD" \| python3 scripts/login.py set --url www.huo15.com --db huo15 --login X` |
| 测连接 | `python3 scripts/login.py test` |
| 新建待办 | `todo.py add --title ... [--deadline --priority --stage --tags]` |
| 我的待办 | `todo.py list` |
| 完成待办 | `todo.py done <id>` |
| 项目列表/详情 | `project.py list` / `project.py show <id>` |
| 建项目/任务 | `project.py add --name ...` / `project.py task-add --project <id> --title ...` |
| 移阶段/改负责人 | `project.py task-move <id> --stage X` / `task-assign <id> --users a,b` |
| 工时汇总 | `timesheet.py by-employee\|by-project\|by-month [--month/--from/--to]` |
| 工时明细 | `timesheet.py detail --employee X --month YYYY-MM` |
| CRM 商机 | `crm.py list` / `crm.py add --name ... --customer ... --revenue N --user 我` |
| 赢/输/管道 | `crm.py won\|lost <id>` / `crm.py pipeline --by stage\|user\|team` |
| 活动/提醒 | `activity.py list` / `activity.py add --model crm.lead --id N --type call --date ...` |
| 日历/会议 | `agenda.py list` / `agenda.py add --name ... --start "... HH:MM" --with X --remind 30m` |
| 重复/忙闲 | `agenda.py add ... --repeat weekly --on mon --count 52` / `agenda.py busy --who X --date Y` / `agenda.py attendees <id>` |
| 知识库 | `knowledge.py search <kw>` / `knowledge.py add --title ... --icon 📘` / `knowledge.py show <id>` |
| 文档 | `documents.py folders` / `documents.py upload --file <path> --folder X` / `documents.py link <id>` |
| 每日总览 | `briefing.py` / `briefing.py week` —— 聚合待办+活动+会议「我今天要做什么」 |
| 销售/采购 | `sales.py add --customer X --line "产品:数量"` / `purchase.py add --vendor X --line ...` / `confirm <id>` |
| 库存 | `stock.py qty <产品>` / `stock.py pickings --in\|--out` / `stock.py validate <id>` |

所有脚本支持 `--json` 输出、`--tools-md <path>` 指定凭据文件。

---

## 字段坑速查（最容易错，改脚本前必看）

| 坑 | 正确做法 |
|---|---|
| 待办放哪 | `project.task` 且 **不传 project_id**（保持 False）+ `user_ids` 含本人 |
| 截止日期 | `date_deadline` 是 **Datetime / UTC**，不是 date（脚本已自动本地→UTC） |
| 完成状态 | `state='1_done'`；取消 `'1_canceled'`；进行中 `'01_in_progress'`；等待 `'04_waiting_normal'` |
| 任务负责人 | `user_ids` 是 **Many2many**，写 `[(6,0,[ids])]`；不是 user_id |
| 分配工时 | 任务用 `allocated_hours`，**不是 planned_hours**（19 已删） |
| 工时小时数 | 工时单求和用 `unit_amount`（不是 amount，amount 是钱） |
| 是不是工时单 | 没有 is_timesheet 字段，判定 `('project_id','!=',False)` |
| 分组统计 | `read_group` 多 groupby 必须 `lazy=False`；优先 `formatted_read_group`（脚本已封装） |
| 个人阶段筛选 | `personal_stage_type_id` 无 search，按阶段筛走 `project.task.stage.personal` 关联表（脚本已处理） |
| CRM 赢/输单 | 建商机必传 `type='opportunity'`；负责人 `user_id` 单数；赢/输/复活调 `action_set_won/lost/restore`，别手动 write |
| CRM 字段 | 手机号写 `phone`（无 mobile）；`crm.stage.team_ids` 复数 m2m（空=全团队）；`description` 是 Html |
| 活动 | `date_deadline` 是 **Date**；完成=archive(`action_feedback`)不是删；`state` computed 无 search，查逾期用 `date_deadline` 比较 |
| 日历 | `start/stop` 是 **Datetime/UTC**（脚本自动转）；写 `partner_ids` 自动建参与人；alarm 只有 notification/email |
| 日历重复/忙闲 | 重复走 calendar.event(`recurrency=True`)，rrule 只读用结构化字段；改重复带 `recurrence_update`(all 不能改时间)；忙闲用区间重叠+`show_as=busy`；crm 用 `opportunity_id` 关联 |
| 知识库 | 根文章必有 internal_permission(create 自动补 write)；收藏 `action_toggle_favorite`；移动 `move_to`；权限走方法非直接写 member |
| 文档 | **19 版文件夹=document(type=folder)**，无 documents.folder/share；上传直接传 datas(base64)；下载用 access_token；建标签需管理员 |
| 销售/采购 | state 无 done(用 locked)；销售行 `product_uom_qty`+`product_uom_id`+`tax_ids`，采购行 `product_qty`；确认是写操作建交货/入库单；采购删除前先 cancel |
| 库存 | 查库存用 product `free_qty`/`qty_available`(限仓库走 context)；明细 `move_ids`(无 \_without_package)；完成量 `quantity`(非 qty_done)；validate 必传 `skip_backorder` |

> 这些都已在脚本里处理对。手工写新调用 / 改脚本时对照本表和 references/。

---

## 品牌口径

- **对外**（PRD/汇报/客户文档）：辉火云企业套件 / 辉火云。
- **对内调试 / 本技能文档 / 代码注释**：可用 odoo 等真实技术标识符。
- 版权：青岛火一五信息科技有限公司。

## 安全红线

1. 凭据只写 `~/.huo15/tools.md`（权限 600），**永不进 git / commit / 日志**。
2. secret 传参优先 `--secret-stdin`，避免明文进 shell 历史。
3. 推荐 API Key 而非主密码（可吊销）。
4. 删除/归档/批量改状态前向用户确认。
