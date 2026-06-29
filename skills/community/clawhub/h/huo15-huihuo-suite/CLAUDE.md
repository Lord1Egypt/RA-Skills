# CLAUDE.md

**项目：huo15-huihuo-suite** — 辉火套件ERP v1.5.0

> **加新应用时的分层原则**：详细 CLI 命令写进 `references/commands.md`，SKILL.md 只更新「四大应用速览」表 + 「命令速查」表 + 「字段坑速查」表，保持 SKILL.md 嵌入体积小（progressive disclosure）。

## 项目定位

用自然语言 + API 操作公司**辉火云企业套件**（www.huo15.com，db=`huo15`，Odoo 19）的待办 / 项目 / 工时单三大应用。纯 Python 标准库（`xmlrpc.client` + `urllib`），零第三方依赖。

## 品牌口径（对外文档必守）

- **对外**（PRD/汇报/客户文档/营销）：辉火云企业套件 / 辉火云。
- **对内调试 / 本技能 SKILL.md / references / 代码注释**：可用 odoo 等真实技术标识符（API 协议文档性质，§11.8 豁免）。
- README.md 主体用业务名，技术实现小节如实写 Odoo 19 API。
- 版权：青岛火一五信息科技有限公司。

## 目录结构

```
huo15-huihuo-suite/
├── SKILL.md            # 技能主文档（触发词 / 工作流 / 命令速查 / 字段坑）
├── README.md           # 对外文档（模板：logo + 标语 + 机构表 + 正文 + 页脚）
├── CLAUDE.md           # 本文件
├── _meta.json          # ClawHub 元数据（slug / version）
├── scripts/
│   ├── odoo_client.py  # 核心：凭据(tools.md 读写) + XML-RPC/JSON-RPC + 通用 ORM 封装
│   ├── odoo_utils.py   # 时区(本地↔UTC) / m2o 格式化 / 中文宽度对齐表格 / state-priority 标签
│   ├── login.py        # 配置并验证凭据（getpass / stdin / 参数三种入口）
│   ├── todo.py         # 待办（add/list/done/reopen/cancel/update/stages）
│   ├── project.py      # 项目+任务（list/show/add/edit/archive + task-*）
│   ├── timesheet.py    # 工时单（by-employee/by-project/by-month/detail/log）
│   ├── crm.py          # CRM 线索/商机（list/show/add/move/won/lost/restore/convert/pipeline/activity）
│   ├── activity.py     # 活动 mail.activity（list/add/done/cancel/reschedule）
│   ├── agenda.py       # 日历/重复/参与人/提醒/忙闲（calendar.*）；名字避开标准库 calendar
│   ├── knowledge.py    # 知识库 knowledge.article（list/tree/search/show/add/fav/move）
│   ├── documents.py    # 文档 documents.document（19版 folder=document/无 share）
│   ├── briefing.py     # 每日/每周总览（聚合 project.task+mail.activity+calendar.event）
│   ├── sales.py        # 销售 sale.order（list/show/add/confirm/cancel/invoice）
│   ├── purchase.py     # 采购 purchase.order（list/show/add/confirm/approve/cancel/bill）
│   └── stock.py        # 库存 stock.quant/picking/move（qty/pickings/show/validate/locations/warehouses）
└── references/         # 命令参考 + Odoo 19 API 知识沉淀（读企业版源码而来）
    ├── commands.md            # 八应用完整 CLI 命令（SKILL.md 瘦身后下沉，progressive disclosure）
    ├── odoo-todo-api.md       # 待办=project.task 私有态 + state 取值 + 个人阶段坑
    ├── odoo-project-api.md    # project.project/task/task.type + allocated_hours/user_ids
    ├── odoo-timesheet-api.md  # account.analytic.line + unit_amount + read_group lazy 坑
    ├── odoo-crm-api.md        # crm.lead(type) + won/lost 专用方法 + team_ids 复数 + 无 mobile
    ├── odoo-activity-calendar-api.md  # mail.activity(Date/完成archive/state无search) + calendar.event(UTC) + alarm
    ├── odoo-calendar-advanced-api.md  # 重复事件(recurrency/rrule结构化字段) + attendee响应 + 忙闲(show_as) + opportunity_id
    ├── odoo-knowledge-documents-api.md  # knowledge.article(层级/收藏/权限/move_to) + documents.document(19版 folder=document/无 share/access_token)
    └── odoo-sales-purchase-stock-api.md  # sale.order/purchase.order(state无done+v19字段product_uom_id/tax_ids) + stock(free_qty/move_ids/button_validate skip_backorder)
```

## 开发规范

1. **所有修改在本地仓库**：`/Users/jobzhao/workspace/projects/openclaw/huo15-skills/huo15-huihuo-suite/`，禁止改 ClawHub 安装副本。
2. **不新增第三方依赖**：保持纯标准库（`_meta.json` 的 dependencies 为空）。
3. **改/写 ORM 调用前必查 `references/`**：Odoo 19 字段坑很多（见下表），别凭记忆。
4. 入口分层：业务脚本（todo/project/timesheet）→ `odoo_client.Odoo` → execute_kw。新功能优先复用 `Odoo` 的便捷方法，别重复写 execute_kw 拼装。
5. 共用逻辑（时区/格式化/表格）放 `odoo_utils.py`，别在各脚本里复制。

## 字段坑速查（改代码前对照，详见 references/）

| 坑 | 正确做法 |
|---|---|
| 待办归属 | `project.task` 且不传 project_id（False）+ user_ids 含本人 |
| 截止日期 | `date_deadline` 是 Datetime/UTC（`odoo_utils.to_utc` 已转） |
| 完成状态 | `state='1_done'` / 取消 `'1_canceled'` / 进行中 `'01_in_progress'` / 等待 `'04_waiting_normal'` |
| 任务负责人 | `user_ids` 是 m2m，`[(6,0,[ids])]` |
| 分配工时 | `allocated_hours`（非 planned_hours） |
| 工时小时数 | `unit_amount`（非 amount） |
| 工时单判定 | `('project_id','!=',False)`（无 is_timesheet 字段） |
| 分组聚合 | read_group 多 groupby 必 `lazy=False`；优先 formatted_read_group |
| 个人阶段筛 | personal_stage_type_id 无 search，走 project.task.stage.personal 关联表 |
| CRM 商机 | 建商机必传 type='opportunity'；user_id 单数；赢/输/复活调 action_set_won/lost/restore 别手动 write |
| CRM 字段 | 手机号写 phone(无 mobile)；crm.stage.team_ids 复数 m2m(空=全团队)；description 是 Html |
| 活动 | date_deadline 是 Date；完成=archive(action_feedback)非删；state computed 无 search(用 date_deadline 比较) |
| 日历 | start/stop 是 Datetime/UTC；partner_ids 自动建 attendee；alarm 仅 notification/email；**脚本名 agenda 不能叫 calendar**(遮蔽标准库) |
| 日历重复/忙闲 | 重复走 calendar.event(recurrency=True),rrule 只读用结构化字段(rrule_type/mon../day);改重复带 recurrence_update(all 不能改时间);代回复用 attendee.do_accept;忙闲区间重叠+show_as=busy;crm 用 opportunity_id |
| 知识库 | 根文章必有 internal_permission(create 自动补 write);收藏 action_toggle_favorite;移动 move_to;权限走 set_internal_permission/invite_members 非直接写 member 表;is_user_favorite/user_has_access 可搜 |
| 文档 | **19版 folder=documents.document(type=folder)**,无 documents.folder/share/workflow.rule;上传直接传 datas(base64)自动建 attachment;下载用 access_token;建标签需 group_documents_manager;child_of 单值 |
| 销售/采购 | state 无 done(用 locked);销售行 product_uom_qty+product_uom_id+tax_ids,采购行 product_qty;确认 action_confirm/button_confirm 建交货/入库单;采购删前先 cancel |
| 库存 | 查库存用 product free_qty/qty_available(限仓库走 context 非 domain);明细 move_ids(无 _without_package);完成量 quantity(非 qty_done);validate 必传 skip_backorder |

## 凭据 / 安全

- 运行期凭据写 `~/.huo15/tools.md`（标记块 + 权限 600），代码里**绝不内嵌任何 secret**。
- secret 入参优先 `--secret-stdin`。
- 测试连接：`python3 scripts/login.py test`。

## 发布流程

> 本技能是独立 skill，无 plugin 引用它，直接发即可（无"先 skill 后 plugin"顺序问题）。

```bash
cd /Users/jobzhao/workspace/projects/openclaw/huo15-skills
git add huo15-huihuo-suite/
git commit -m "feat(huihuo-suite): vX.Y.Z - 说明"
git push origin main      # cnb.cool 主
git push github main      # GitHub 镜像

# ClawHub（绝对路径 + 显式 --version，见 ~/CLAUDE.md §7 六坑）
CLAWHUB_TOKEN=clh_... clawhub publish "$(pwd)/huo15-huihuo-suite" --version 1.0.0

# publish 后手动同步 _meta.json 的 version（CLI 不会自动刷）并单独 chore commit
```

**发布凭据**：见 `~/CLAUDE.md` §2（cnb git / npm / ClawHub token），不写进本仓库。
**发布六坑**：见 `~/CLAUDE.md` §7（绝对路径 / --version 必填 / rate limit / _meta.json 手动同步 / 幽灵占用 +1 patch / SKILL.md 8192 token 上限）。

## 版本号规则

- 新增应用/大改 API 层 → 次版本（1.0→1.1）。
- 新增命令/参数 → 次版本。
- 修 bug/字段坑 → 补丁号（1.0.0→1.0.1）。
- 每次发版同步 bump `package.json`(无)/`_meta.json`/SKILL.md frontmatter `version` 三处一致。
