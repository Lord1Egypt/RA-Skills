# 辉火套件ERP — 完整命令参考

> SKILL.md 的「命令速查」表覆盖最常用命令；本文件是每个应用的完整 CLI 示例与说明。
> 所有脚本通用：`--json`（程序解析）、`--tools-md <path>`（指定凭据文件）、`-h`（看完整参数）。
> 字段/API 细节见各 `references/odoo-<app>-api.md`。

## 待办（/odoo/to-do）—— todo.py

待办 = `project.task` 且 `project_id` 为空 + 指派给本人。

```bash
# 新建：标题必填，截止/优先级/阶段/标签可选
python3 scripts/todo.py add --title "跟进三和红木分账" --deadline 2026-06-10 --priority 2
python3 scripts/todo.py add --title "写周报" --desc "本周三大进展" --stage Today --tags "管理,周报"

# 列出（默认未完成）
python3 scripts/todo.py list                 # 我的未完成待办
python3 scripts/todo.py list --all           # 含已完成
python3 scripts/todo.py list --stage Today    # 按个人阶段筛
python3 scripts/todo.py stages               # 看我有哪些个人阶段（Inbox/Today/...）

# 改状态
python3 scripts/todo.py done 1234            # 标记完成（可多个 id）
python3 scripts/todo.py reopen 1234          # 重新打开
python3 scripts/todo.py cancel 1234          # 取消

# 修改内容
python3 scripts/todo.py update 1234 --deadline "2026-06-12 18:00" --priority 3
```

关键：截止日期填 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM`（按你本地时间，脚本自动转 UTC）；优先级 0普通/1中/2高/3紧急；完成=state `1_done`。

## 项目（/odoo/project）—— project.py

`project.project` + `project.task`。项目/用户/客户都可用**名字**代替 id。

```bash
# 项目层
python3 scripts/project.py list                      # 所有项目
python3 scripts/project.py list --mine                # 只看我负责的
python3 scripts/project.py show 5                      # 项目详情 + 按阶段统计任务
python3 scripts/project.py add --name "官网改版" --manager 我 --customer "某客户" --deadline 2026-08-31
python3 scripts/project.py edit 5 --manager 张三 --deadline 2026-09-30
python3 scripts/project.py archive 5                   # 归档 / unarchive 恢复

# 任务层
python3 scripts/project.py tasks 5                     # 列项目 5 的未完成任务（--all 全部）
python3 scripts/project.py task-add --project 5 --title "首页设计" --assignee 我 --deadline 2026-06-20 --hours 8
python3 scripts/project.py task-move 88 --stage 进行中  # 移到某看板阶段
python3 scripts/project.py task-assign 88 --users "张三,李四"
python3 scripts/project.py task-done 88                # 标记完成
python3 scripts/project.py task-update 88 --priority 3 --deadline 2026-06-22
```

关键：任务负责人是**多对多**（可多人，逗号分隔）；"我"会自动解析成当前登录用户；分配工时字段是 `allocated_hours`（脚本已处理）。

## 工时单（/odoo/timesheets）—— timesheet.py

工时单 = `account.analytic.line` 且 `project_id` 非空。**默认本月**。

```bash
# 汇总报表
python3 scripts/timesheet.py by-employee                    # 本月每个员工总工时
python3 scripts/timesheet.py by-employee --month 2026-06     # 指定月
python3 scripts/timesheet.py by-employee --department 研发部 --from 2026-06-01 --to 2026-06-30
python3 scripts/timesheet.py by-project --month 2026-06      # 按项目
python3 scripts/timesheet.py by-month --employee 张三 --year 2026   # 某员工逐月趋势

# 明细
python3 scripts/timesheet.py detail --employee 张三 --month 2026-06

# 录入一条工时（可选）
python3 scripts/timesheet.py log --project 5 --hours 3 --task 88 --desc "对接联调"
```

时间范围参数通用：`--month YYYY-MM` / `--from --to` / `--year`，缺省本月。
筛选：`--employee 名字` / `--project 名字或id` / `--department 部门名`。
输出对齐表格 + 合计；加 `--json` 给程序解析。

## CRM（/odoo/crm）—— crm.py

线索/商机同为 `crm.lead`（`type` 区分）。客户/负责人/团队可用**名字**。

```bash
# 商机列表与详情
python3 scripts/crm.py list                  # 我的进行中商机（带预期收入合计）
python3 scripts/crm.py list --all            # 全部进行中；--won 已赢 / --lost 已输
python3 scripts/crm.py list --user 张三 --stage 报价
python3 scripts/crm.py show 88

# 新建 / 修改
python3 scripts/crm.py add --name "某客户-ERP项目" --customer "某客户" --revenue 50000 --user 我 --team 销售一组 --priority 2
python3 scripts/crm.py update 88 --revenue 60000 --probability 70

# 推进 / 赢单 / 输单 / 复活
python3 scripts/crm.py move 88 --stage 谈判          # 推进阶段
python3 scripts/crm.py won 88                        # 标记赢单（自动置赢单阶段 + 100%）
python3 scripts/crm.py lost 88 --reason "价格太高"    # 标记输单（原因不存在自动建）
python3 scripts/crm.py restore 88                    # 复活已输单

# 线索转商机 / 安排跟进活动
python3 scripts/crm.py convert 90 --customer "某客户"
python3 scripts/crm.py activity 88 --type call --date 2026-06-10 --summary "回访报价"

# 销售管道统计（预期收入 + 加权预测）
python3 scripts/crm.py pipeline --by stage           # 按阶段；--by user 负责人 / --by team 团队
```

关键：建商机自动用 `type=opportunity`；负责人 `user_id` 单数；赢单/输单/复活走 Odoo 专用方法（脚本已封装），别手动改 stage/active/probability。

## 活动（My Activities）—— activity.py

活动 = 挂在记录（商机/项目任务/客户…）上的"下一步待办/提醒"。

```bash
python3 scripts/activity.py list                    # 我的逾期+今日活动
python3 scripts/activity.py list --overdue          # 逾期；--today 今日 / --planned 计划 / --all 全部
python3 scripts/activity.py add --model crm.lead --id 88 --type call --summary "3天后回访" --date 2026-06-10
python3 scripts/activity.py done 123 --feedback "已回访"   # 完成（归档，记录仍在，非删除）
python3 scripts/activity.py reschedule 123 --date 2026-06-15
python3 scripts/activity.py cancel 123              # 取消（删除）
```

活动类型 `--type`：todo/call/meeting/email/upload；`--model`+`--id` 指定挂哪条记录（crm.lead/project.task/…）。

## 日历（/odoo/calendar）—— agenda.py

日历事件 + 重复 + 参与人 + 提醒 + 忙闲（calendar.event/alarm/attendee）。脚本名 `agenda`（避开 Python 标准库 calendar）。

```bash
# 看日程
python3 scripts/agenda.py list                       # 本周；--today / --month / --from --to
python3 scripts/agenda.py show 5                      # 详情（重复/参与人响应/关联商机）

# 新建：普通 / 全天 / 重复 / 关联商机
python3 scripts/agenda.py add --name "方案评审" --start "2026-06-10 10:00" --duration 1 --location 会议室A --with "张三,李四" --remind 30m
python3 scripts/agenda.py add --name "团建" --start 2026-06-15 --allday
python3 scripts/agenda.py add --name "周例会" --start "2026-06-29 09:00" --duration 1 --repeat weekly --on mon --count 52
python3 scripts/agenda.py add --name "月度复盘" --start "2026-07-01 14:00" --repeat monthly --day 1 --until 2026-12-31
python3 scripts/agenda.py add --name "客户洽谈" --start "2026-06-12 10:00" --opportunity "某客户-ERP项目"

# 改 / 删（重复事件带范围 self|future|all）
python3 scripts/agenda.py update 5 --start "2026-06-10 14:00" --scope future
python3 scripts/agenda.py cancel 5                    # 删单个；--series future|all 删重复系列
python3 scripts/agenda.py remind 5 --before 1h        # 加提醒（--type notification|email）

# 参与人
python3 scripts/agenda.py invite 5 --add 王五 --remove 李四
python3 scripts/agenda.py attendees 5                 # 看谁接受/拒绝/待定/待回复 + 统计
python3 scripts/agenda.py rsvp 5 --who 张三 --status accept   # 代回复 accept/decline/tentative

# 忙闲（找开会时间）
python3 scripts/agenda.py busy --who 张三 --date 2026-06-25
python3 scripts/agenda.py busy --who 张三 --from "2026-06-25 14:00" --to "2026-06-25 18:00"
```

重复：`--repeat weekly --on mon,wed` / `--repeat monthly --day 1`；次数 `--count N` 或 `--until YYYY-MM-DD`；时区默认 Asia/Shanghai。时间本地输入自动转 UTC；`--with`/`--add` 写名字自动建 attendee；crm 商机用 `--opportunity` 关联。

## 知识库（Knowledge）—— knowledge.py

层级文章 knowledge.article。

```bash
python3 scripts/knowledge.py list                    # 顶级文章；--fav 我收藏 / --mine 我编辑的
python3 scripts/knowledge.py search 退款流程          # 全文搜（标题+正文）
python3 scripts/knowledge.py show 12                  # 读文章正文 + 子文章
python3 scripts/knowledge.py add --title "产品手册" --body "正文..." --icon 📘
python3 scripts/knowledge.py add --title "第一章" --parent 12 --icon 📄   # 子文章
python3 scripts/knowledge.py fav 12                   # 收藏/取消
python3 scripts/knowledge.py tree 12                  # 看子文章层级
python3 scripts/knowledge.py move 15 --parent 12      # 移到某文章下
```

`icon` 是 emoji；建根文章自动获 write 权限；移动走 move_to（脚本已封装）。

## 文档（Documents）—— documents.py

```bash
python3 scripts/documents.py folders                  # 列所有文件夹
python3 scripts/documents.py list --folder 财务        # 列文件夹内文档；--tag 合同
python3 scripts/documents.py search invoice           # 全文搜（名字+内容索引）
python3 scripts/documents.py upload --file ~/report.pdf --folder 财务   # 上传
python3 scripts/documents.py link 123                 # 取下载链接
python3 scripts/documents.py tags                     # 列标签
python3 scripts/documents.py tag 123 --add 合同        # 打标签（建新标签需管理员）
```

Odoo 19 文件夹 = `type='folder'` 的 document；上传直接传 base64（自动建附件）；下载用 access_token。

## 每日总览（辅助提醒 + 待办）—— briefing.py

```bash
python3 scripts/briefing.py                            # 我今天要做什么（待办+活动+会议）
python3 scripts/briefing.py week                       # 本周总览
```

聚合 project.task(待办) + mail.activity(活动) + calendar.event(会议)，逾期标 🔴；是"提醒/待办"的一站式总览。

## 销售（/odoo/sale）—— sales.py

```bash
python3 scripts/sales.py list                        # 我的订单；--draft 报价单 / --confirmed / --customer X / --all
python3 scripts/sales.py show 42
python3 scripts/sales.py add --customer "某客户" --line "办公椅:10" --line "办公桌:5:800"
python3 scripts/sales.py confirm 42                  # 确认报价单→销售订单（建交货单，写操作，先与用户确认）
python3 scripts/sales.py invoice 42                  # 生成发票；cancel 取消
```

订单行 `--line "产品:数量[:单价]"` 可重复；v19 行字段 product_uom_qty/product_uom_id/tax_ids；state 无 done。

## 采购（/odoo/purchase）—— purchase.py

```bash
python3 scripts/purchase.py list --rfq               # 询价单；--confirmed / --vendor X
python3 scripts/purchase.py add --vendor "某供应商" --line "原料A:100:5" --line "原料B:50"
python3 scripts/purchase.py confirm 18               # 确认（建入库单）；待批准用 approve
python3 scripts/purchase.py bill 18                  # 生成供应商账单；cancel 取消
```

⚠️ 采购行数量用 `product_qty`（不是销售的 product_uom_qty）；删除前必须先 cancel。

## 库存（/odoo/inventory）—— stock.py

```bash
python3 scripts/stock.py qty 办公椅                   # 查库存（在手/可用/预测+按库位）；--warehouse W
python3 scripts/stock.py pickings --in               # 待收货；--out 发货 / --internal 调拨 / --done 已完成
python3 scripts/stock.py show 55                      # 出入库单明细（需求/完成）
python3 scripts/stock.py validate 55                  # 验证出入库：预留→设完成量→过账（写操作，先确认）
python3 scripts/stock.py locations                    # 列内部库位；warehouses 列仓库
```

查库存走 product 的 free_qty/qty_available（限仓库走 context）；验证 button_validate 已自动跳欠单向导。
