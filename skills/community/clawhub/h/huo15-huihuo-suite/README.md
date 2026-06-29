# 辉火套件ERP（huo15-huihuo-suite）

---

<div align="center">

<img src="https://tools.huo15.com/uploads/images/system/logo-colours.png" alt="火一五Logo" style="width: 120px; height: auto; display: inline; margin: 0;" />

</div>

<div align="center">

<h3>打破信息孤岛，用一套系统驱动企业增长</h3>
<h3>加速企业用户向全场景人工智能机器人转变</h3>

</div>
<div align="center">

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式         | 💬 QQ群      | 📺 配套视频                         |
|:-----------:|:--------:|:------------------:|:-----------:|:-----------------------------------:|
| 逸寻智库 | Job | support@huo15.com | 1093992108  | [📺 B站视频](https://space.bilibili.com/400418085) |

</div>

---

## 这是什么

用自然语言操作公司**辉火云企业套件**（www.huo15.com，数据库 `huo15`）的十一大应用，全程走系统 API，零第三方依赖：

- 📝 **待办**（/odoo/to-do）：新建/列出/完成个人待办，支持标题、内容、截止日期、个人阶段、优先级、标签。
- 📁 **项目**（/odoo/project）：管理项目与任务——编辑项目、加任务、移看板阶段、改负责人、统计任务。
- ⏱️ **工时单**（/odoo/timesheets）：按员工 / 项目 / 月份统计工时，输出筛选好的报表与明细。
- 💼 **CRM**（/odoo/crm）：管理线索与商机——新建、推进阶段、赢单/输单（带原因）、线索转商机、安排跟进活动，按阶段/负责人/团队统计销售管道。
- 🔔 **活动**（My Activities）：给任意记录（商机/任务/客户）加"下一步"跟进活动/提醒，看我的逾期+今日活动，标记完成。
- 📅 **日历**（/odoo/calendar）：新建会议/事件（参与人、地点、时长），**重复周会/例会**，看本周日程，**查参与人接受/拒绝、查某人忙闲找开会时间**，关联商机，加提前提醒。
- 📚 **知识库**（/odoo/knowledge）：层级文章管理——建/搜/读知识库文章、子文章、收藏、移动，emoji 图标。
- 📁 **文档**（/odoo/documents）：文件管理——列文件夹、上传/下载文件、全文搜、打标签、按文件夹筛。
- 🛒 **销售**（/odoo/sale）：管理报价单与销售订单——建单、确认（自动建交货单）、生成发票，按客户/状态筛。
- 🛍️ **采购**（/odoo/purchase）：管理询价单与采购订单——建单、确认（自动建入库单）、批准、生成供应商账单。
- 📦 **库存**（/odoo/inventory）：查产品实时库存（在手/可用/预测）、列待收发货出入库单、验证出入库、看库位/仓库。
- 🗓️ **每日总览**（`briefing.py`）：把待办+活动+会议聚合成「我今天/本周要做什么」，辅助提醒和待办。

底层基于 Odoo 19 的 XML-RPC / JSON-RPC 接口，仅用 Python 标准库实现。

## 安装

```bash
# ClawHub
clawhub install huo15-huihuo-suite

# 或源码（OpenClaw 插件方式拉取）
# 仓库：https://cnb.cool/huo15/ai/huo15-skills  /  https://github.com/zhaobod1/huo15-skills
```

## 快速开始

### ① 第一次：初始化连接（4 项）

初始化收集 4 项存入 `~/.huo15/tools.md`：**①公司系统地址**（如 www.huo15.com，只输域名即可，自动补 https://）、**②数据库**（如 huo15）、**③账号**、**④密码**（推荐 API Key）。

```bash
# 交互式初始化：依次提示输入这 4 项（密码不回显）
python3 scripts/login.py init
python3 scripts/login.py test     # 验证连接

# 或非交互（密码走 stdin，不进 shell 历史）
printf '%s' "你的密码或APIKey" | python3 scripts/login.py set \
    --url www.huo15.com --db huo15 --login 你的账号 --auth-type apikey
```

凭据保存在个人文件 `~/.huo15/tools.md`（自动 `chmod 600`），可用环境变量 `HUO15_TOOLS_MD` 改路径。**该文件含明文凭据，请勿提交 git。**

### ② 待办

```bash
python3 scripts/todo.py add --title "跟进三和红木分账" --deadline 2026-06-10 --priority 2
python3 scripts/todo.py list                 # 我的未完成待办
python3 scripts/todo.py done 1234            # 标记完成
```

### ③ 项目

```bash
python3 scripts/project.py list
python3 scripts/project.py show 5            # 详情 + 按阶段统计任务
python3 scripts/project.py task-add --project 5 --title "首页设计" --assignee 我 --deadline 2026-06-20
python3 scripts/project.py task-move 88 --stage 进行中
```

### ④ 工时单

```bash
python3 scripts/timesheet.py by-employee --month 2026-06           # 每员工本月工时
python3 scripts/timesheet.py by-employee --department 研发部        # 按部门筛
python3 scripts/timesheet.py by-project --month 2026-06            # 按项目
python3 scripts/timesheet.py detail --employee 张三 --month 2026-06 # 明细
```

### ⑤ CRM

```bash
python3 scripts/crm.py list                                       # 我的进行中商机
python3 scripts/crm.py add --name "某客户-ERP项目" --customer "某客户" --revenue 50000 --user 我
python3 scripts/crm.py move 88 --stage 谈判                        # 推进阶段
python3 scripts/crm.py won 88                                     # 赢单 / lost 88 --reason "价格太高" 输单
python3 scripts/crm.py pipeline --by stage                        # 销售管道统计
```

### ⑥ 活动

```bash
python3 scripts/activity.py list                                          # 我的逾期+今日活动
python3 scripts/activity.py add --model crm.lead --id 88 --type call --summary "3天后回访" --date 2026-06-10
python3 scripts/activity.py done 123 --feedback "已回访"                   # 完成（归档）
```

### ⑦ 日历

```bash
python3 scripts/agenda.py list                                            # 本周日程（--today/--month）
python3 scripts/agenda.py add --name "方案评审" --start "2026-06-10 10:00" --duration 1 --with "张三,李四" --remind 30m
python3 scripts/agenda.py remind 5 --before 1h                            # 给事件加提醒
```

### ⑧ 知识库 / 文档 / 每日总览

```bash
python3 scripts/knowledge.py search 退款流程                              # 搜知识库
python3 scripts/knowledge.py add --title "产品手册" --body "正文..." --icon 📘
python3 scripts/documents.py folders                                      # 列文件夹
python3 scripts/documents.py upload --file ~/report.pdf --folder 财务      # 上传文档
python3 scripts/briefing.py                                               # 我今天要做什么（待办+活动+会议）
python3 scripts/briefing.py week                                          # 本周总览
```

### ⑨ 销售 / 采购 / 库存

```bash
python3 scripts/sales.py add --customer "某客户" --line "办公椅:10" --line "办公桌:5:800"   # 建报价单
python3 scripts/sales.py confirm 42                                       # 确认订单（建交货单）
python3 scripts/purchase.py add --vendor "某供应商" --line "原料A:100:5"                    # 建询价单
python3 scripts/stock.py qty 办公椅                                        # 查产品库存
python3 scripts/stock.py pickings --in                                    # 待收货出入库单
```

## 命令总览

| 脚本 | 命令 |
|---|---|
| `login.py` | `init`（交互初始化）/ `set` / `show` / `test` |
| `todo.py` | `add` / `list` / `done` / `reopen` / `cancel` / `update` / `stages` |
| `project.py` | `list` / `show` / `add` / `edit` / `archive` / `tasks` / `task-add` / `task-move` / `task-assign` / `task-done` / `task-update` |
| `timesheet.py` | `by-employee` / `by-project` / `by-month` / `detail` / `log` |
| `crm.py` | `list` / `show` / `add` / `update` / `move` / `won` / `lost` / `restore` / `convert` / `pipeline` / `activity` |
| `activity.py` | `list` / `add` / `done` / `cancel` / `reschedule` |
| `agenda.py` | `list` / `show` / `add` / `update` / `cancel` / `remind` / `invite` / `attendees` / `rsvp` / `busy` |
| `knowledge.py` | `list` / `tree` / `search` / `show` / `add` / `fav` / `move` |
| `documents.py` | `folders` / `list` / `search` / `upload` / `link` / `tags` / `tag` |
| `briefing.py` | `today` / `week`（聚合待办+活动+会议总览） |
| `sales.py` | `list` / `show` / `add` / `confirm` / `cancel` / `invoice` |
| `purchase.py` | `list` / `show` / `add` / `confirm` / `approve` / `cancel` / `bill` |
| `stock.py` | `qty` / `pickings` / `show` / `validate` / `locations` / `warehouses` |

所有脚本支持 `--json`（程序解析）和 `--tools-md <path>`（指定凭据文件）。各脚本 `-h` 看完整参数。

## 目录结构

```
huo15-huihuo-suite/
├── SKILL.md            # 技能主文档（触发词、工作流、命令速查、字段坑）
├── README.md           # 本文件
├── CLAUDE.md           # 开发指引
├── _meta.json          # ClawHub 元数据
├── scripts/
│   ├── odoo_client.py  # 核心库：凭据 + XML-RPC/JSON-RPC 双通道 + 通用 ORM
│   ├── odoo_utils.py   # 时区换算 / 字段格式化 / 中文对齐表格
│   ├── login.py        # 配置并验证凭据，写入 tools.md
│   ├── todo.py         # 待办管理
│   ├── project.py      # 项目与任务管理
│   ├── timesheet.py    # 工时单统计报表
│   ├── crm.py          # CRM 线索/商机管理
│   ├── activity.py     # 活动（mail.activity）
│   ├── agenda.py       # 日历/重复/参与人/提醒/忙闲（calendar.*，避开标准库 calendar）
│   ├── knowledge.py    # 知识库（knowledge.article）
│   ├── documents.py    # 文档（documents.document）
│   ├── briefing.py     # 每日/每周总览（聚合待办+活动+会议）
│   ├── sales.py        # 销售 sale.order
│   ├── purchase.py     # 采购 purchase.order
│   └── stock.py        # 库存 stock.quant/picking/move
└── references/         # 命令参考 + Odoo 19 API 知识沉淀（读源码而来，遇坑先查）
    ├── commands.md            # 十一应用完整 CLI 命令
    ├── odoo-todo-api.md
    ├── odoo-project-api.md
    ├── odoo-timesheet-api.md
    ├── odoo-crm-api.md
    ├── odoo-activity-calendar-api.md
    ├── odoo-calendar-advanced-api.md
    ├── odoo-knowledge-documents-api.md
    └── odoo-sales-purchase-stock-api.md
```

## 安全

- 凭据只写 `~/.huo15/tools.md`（权限 600），永不进 git / 日志。
- secret 优先用 `--secret-stdin` 管道传入，避免明文进 shell 历史 / 进程列表。
- 推荐 API Key 而非主密码（泄漏可吊销）。
- 删除 / 归档 / 批量改状态前会向你确认。

## 技术说明

- 纯 Python 标准库（`xmlrpc.client` + `urllib`），无第三方依赖。
- 同时支持 XML-RPC（默认，最稳）和 JSON-RPC 两种通道，`login.py set --transport jsonrpc` 切换。
- 适配 Odoo 19 字段变化（`user_ids` 多对多、`allocated_hours`、`state` 编号 selection、`read_group` 弃用等），细节见 `references/`。

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
