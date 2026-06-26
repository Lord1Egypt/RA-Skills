# 火一五·辉火云企业套件插件

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

## 简介

**火一五·辉火云企业套件插件** 是 [OpenClaw](https://github.com/nicepkg/openclaw) 的辉火云企业套件适配插件，让你用自然语言全面操作辉火云企业套件。尤其适合**实施经理、项目经理、销售经理**的日常工作场景。

连接后，龙虾 AI Agent 即可帮你管理待办、跟进商机、查看工单、核对账款、记录工时、查库存、看员工——一句话搞定。

### 核心特性

- **Per-Agent 凭据隔离** — 搭配 WeCom 动态 agent，每个企微用户拥有独立的辉火云凭据，互不干扰
- **智能连接引导** — 首次使用自动引导输入系统地址、用户名、密码；数据库自动检测
- **实施经理每日概况** — 一句"今天有什么工作？"汇总任务、活动、工单、逾期账款、商机、未读消息
- **待办 & 任务** — 创建、列表、更新状态/优先级/截止日期
- **CRM 商机管道** — 查看/创建/推进/赢单/输单
- **项目 & 里程碑** — 项目进度总览、里程碑完成率、工时记录
- **客服工单** — 查看/创建 Helpdesk 工单
- **销售 & 采购** — 查看销售订单、采购订单
- **财务发票** — 发票查询、逾期应收账款筛选
- **联系人/客户** — 查询/创建联系人、客户、供应商
- **库存管理** — 库存水平查询、调拨单/出入库单
- **HR 人事** — 员工查询、考勤打卡记录、请假记录
- **审批流** — 查看审批请求
- **活动提醒** — 创建活动、查看今日到期/逾期活动
- **日历会议** — 创建日历事件
- **消息 & 邮件** — 未读消息查看、Chatter 消息发送
- **通用搜索** — 搜索任意辉火云数据模型（客户、产品、员工、库存...）
- **后台通知同步** — 自动轮询推送新任务/活动/消息/邮件/日历变更

---

## 一键安装

```bash
openclaw plugins install @huo15/huo15-huihuoyun-odoo
```

重启 OpenClaw 生效：

```bash
openclaw restart
```

---

## 首次配置

### 方式一：通过对话连接（推荐）

用户只需说一句话，插件会自动引导：

> 帮我连接公司系统

龙虾会依次询问：系统地址、用户名、密码。数据库自动检测（单库自动连接，多库让你选择）。

连接信息按 agent 隔离保存，下次使用自动恢复，无需重新输入。

### 方式二：通过 openclaw.plugin.json 预配置

```json
{
  "odoo": {
    "url": "https://www.huo15.com",
    "db": "huo15",
    "username": "admin@huo15.com",
    "password": "your-password"
  },
  "sync": {
    "enabled": true,
    "intervalSeconds": 30,
    "channels": ["todo", "activity", "message", "email", "calendar"]
  }
}
```

---

## 工具列表（32 个）

### 基础
| 工具 | 说明 |
|------|------|
| `odoo_connect` | 连接辉火云企业套件（db 可选，自动检测） |
| `odoo_status` | 检查连接状态和轮询状态 |
| `odoo_disconnect` | 断开连接并清除已保存凭据 |

### 任务 & 活动
| 工具 | 说明 |
|------|------|
| `odoo_create_task` | 创建待办任务 |
| `odoo_list_tasks` | 查看待办列表（支持 today_only/state 筛选） |
| `odoo_update_task` | 更新任务（状态/阶段/截止日期/优先级） |
| `odoo_create_activity` | 创建活动提醒（关联到记录） |
| `odoo_list_activities` | 查看今日及逾期活动 |
| `odoo_activity_types` | 查询活动类型列表 |
| `odoo_create_event` | 创建日历事件/会议 |

### 消息
| 工具 | 说明 |
|------|------|
| `odoo_get_messages` | 查看未读消息/邮件通知 |
| `odoo_send_message` | 向记录发送 Chatter 消息 |

### CRM
| 工具 | 说明 |
|------|------|
| `odoo_crm_pipeline` | 查看商机管道 |
| `odoo_crm_create` | 创建商机/线索 |
| `odoo_crm_update` | 更新商机信息 |
| `odoo_crm_won` | 标记赢单 |
| `odoo_crm_lost` | 标记输单 |

### 项目 & 工时
| 工具 | 说明 |
|------|------|
| `odoo_project_overview` | 项目列表 + 里程碑进度 |
| `odoo_timesheet_log` | 记录工时 |

### 销售 & 采购 & 财务
| 工具 | 说明 |
|------|------|
| `odoo_sale_orders` | 查看销售订单 |
| `odoo_purchase_orders` | 查看采购订单 |
| `odoo_invoices` | 查看发票/账单（支持逾期筛选） |

### 客服
| 工具 | 说明 |
|------|------|
| `odoo_tickets` | 查看客服工单 |
| `odoo_ticket_create` | 创建客服工单 |

### 联系人（v1.2 新增）
| 工具 | 说明 |
|------|------|
| `odoo_contacts` | 查询联系人/客户/供应商 |
| `odoo_contact_create` | 创建联系人/客户/供应商 |

### 库存（v1.2 新增）
| 工具 | 说明 |
|------|------|
| `odoo_stock_levels` | 查看库存水平 |
| `odoo_stock_pickings` | 查看调拨单/出入库单 |

### HR 人事（v1.2 新增）
| 工具 | 说明 |
|------|------|
| `odoo_employees` | 查询员工列表 |
| `odoo_leaves` | 查看请假记录 |
| `odoo_attendances` | 查看考勤打卡记录 |

### 审批（v1.2 新增）
| 工具 | 说明 |
|------|------|
| `odoo_approvals` | 查看审批请求 |

### 助手
| 工具 | 说明 |
|------|------|
| `odoo_search` | 通用搜索（任意模型任意条件） |
| `odoo_daily_briefing` | 实施经理每日工作概况 |

---

## WeCom 动态 Agent 多用户隔离

搭配 `@huo15/wecom` 插件的动态 agent 能力，每个企微用户/群组拥有独立的辉火云连接：

1. **凭据隔离** — 用户 A 的辉火云账号密码，用户 B 看不到也用不了
2. **Session 隔离** — 每个用户各自的辉火云 session，互不干扰
3. **数据隔离** — 每个用户看到的是自己辉火云账号的数据
4. **自动恢复** — 每个用户的凭据独立持久化，重启后自动恢复

**实现原理**：
- 工具通过 `ctx.agentId` 获取当前用户的动态 agent ID（如 `wecom-acct-ws-dm-zhangsan`）
- 配置持久化到 `~/.openclaw/plugin-configs/odoo/{agentId}.json`
- OdooClient 和 NotificationPoller 均按 agentId 隔离存储

---

## 使用示例

```
👤 帮我连接公司系统
🦞 好的，请提供：1) 系统地址 2) 用户名 3) 密码

👤 地址 https://erp.huo15.com，用户名 zhang@huo15.com，密码 xxx
🦞 已成功连接到 erp.huo15.com（数据库: huo15），欢迎使用辉火云企业套件！

👤 今天有什么工作？
🦞 汇总：3个待办任务、2个到期活动、1个紧急工单、华为商机需跟进...

👤 帮我创建任务：明天发报价单给华为
🦞 已创建任务 #456，截止日期 2026-04-13

👤 查看我的商机
🦞 你有 5 个活跃商机：华为ERP项目（报价阶段，50万）...

👤 商机 #88 赢了
🦞 已标记商机 #88 为赢单

👤 有哪些客户还没付款
🦞 3张未付发票：华为 ¥12,000（逾期15天）...

👤 查下产品A还有多少库存
🦞 产品A 库存：上海仓 120 件、北京仓 45 件

👤 研发部有哪些员工
🦞 研发部共 8 人：张三（前端）、李四（后端）...
```

---

## 通知同步

插件连接后自动轮询（默认 30 秒），推送以下变更：

| 通道 | 触发条件 |
|------|---------|
| todo | 我的任务有新增或更新 |
| activity | 今日到期活动 |
| message | 新 Chatter 消息 |
| email（可选）| 新邮件通知 |
| calendar（可选）| 今明两天内的新日历事件 |

---

## 技术架构

- **JSON-RPC 对接** — 通过 `/web/session/authenticate` 和 `/web/dataset/call_kw` 与辉火云后端通信
- **Per-Agent 隔离** — 按 `ctx.agentId` 隔离 OdooClient / Poller / Config，兼容 WeCom 动态 agent
- **数据库自动检测** — `/web/database/list` 查询可用数据库，单库自动选择
- **Session 自动重连** — `ensureAuthenticated()` 在轮询前自动检查并恢复 session
- **高水位线去重** — 消息/邮件用 `id > highWaterMark` 去重，避免时钟偏差问题
- **基线初始化** — 首次启动静默建立水位线，不推送历史数据
- **OpenClaw 插件规范** — `definePluginEntry` + `api.registerTool()` + `api.on("before_prompt_build")`

---

## 常见问题

**Q: 连接失败怎么办？**
A: 检查 URL（末尾不带斜杠）、账号密码。用 `odoo_status` 查看当前状态。数据库名一般不用手动填，插件会自动检测。

**Q: WeCom 多用户场景下，每个用户都要单独连接吗？**
A: 是的。每个企微用户首次使用辉火云企业套件功能时会被引导输入自己的系统地址和账号密码，之后自动保存，无需重复输入。

**Q: 每日概况失败提示没有 helpdesk 模块？**
A: 系统中未安装 Helpdesk 模块时，工单部分会自动跳过，其他项正常返回。

**Q: 商机阶段 ID 怎么获取？**
A: 通过 `odoo_search(model="crm.stage")` 查询所有 CRM 阶段及其 ID。

**Q: 如何断开连接并清除保存的密码？**
A: 告诉龙虾"断开辉火云连接"，会调用 `odoo_disconnect` 清除当前用户的凭据。

---

## Changelog

- **v1.2.0** — Per-agent 凭据隔离（WeCom 多用户）、智能连接引导、数据库自动检测、联系人/客户管理、库存查询（stock.quant/stock.picking）、HR 员工/考勤/请假、审批流查询、odoo_disconnect 工具。共 32 个工具
- **v1.1.0** — CRM 商机管道、项目里程碑、工时记录、销售/采购订单、Helpdesk 工单、发票/逾期账款查询、任务状态更新、活动类型查询、实施经理每日概况
- **v1.0.0** — 基础版：待办/任务、活动提醒、日历事件、消息/邮件、通用搜索、后台轮询

---

## License

MIT

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
