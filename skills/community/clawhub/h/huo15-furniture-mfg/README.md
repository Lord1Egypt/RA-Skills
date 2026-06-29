# 家具制造业智能体技能（huo15-furniture-mfg）

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

为家具制造企业（首个落地客户：**和栖家居 HeySleep**，床垫制造）打造的 AI 智能体技能包。让工厂的每个角色在聊天里用一句话完成日常查询——不打开管理系统也能跑业务：

- **跟单/销售**：「梁泽光那张床垫到哪一步了」→ 订单 → 生产 → 发货 → 质检 全链路一屏
- **厂长/老板**：「今日总览」→ 接单 / 应交 / 完工 / 发货 / 质检 + 延期缺料风险快照
- **计划**：「在制有多少」「哪些拖期了」「MO 缺什么料」
- **质检**：「还有多少待检」「上个月合格率」
- **采购**：「哪些采购逾期没到货」
- **仓库**：「山隐主垫还有几张现货」

后端为客户部署的**辉火云企业套件 v19**（销售 / 制造 / 库存 / 质检 / 采购全模块）。查询全部只读；写操作（v1.1 起）采用**两段式确认制**——先预览"将要执行什么"，用户明确同意后才落笔，且每一步可撤回。

## 快速开始

```bash
cd huo15-furniture-mfg/scripts
python3 login.py init      # ① 系统地址 ② 数据库 ③ 账号 ④ 密码
python3 login.py test      # 验证连接
python3 overview.py today  # 今日总览
```

- 零第三方依赖（纯 Python 标准库），macOS / Linux 自带 python3 直接跑
- 凭据保存在 `~/.huo15/tools.md`（权限 600），永不进代码与 git

## 能力清单（v1.4.0 = 查询 + 操作 + 协同起草）

| 能力 | 命令 |
|---|---|
| 订单全链路穿透 | `order.py status <单号/客户名>` |
| 订单列表（未发完/按客户/按时间） | `order.py list` |
| 在制清单 / 延期清单 | `mfg.py wip` / `mfg.py late` |
| 欠料检查 | `mfg.py shortage [制造单号]` |
| 库存模糊查询（名称/编号/条码/型号） | `inventory.py find <关键词>` |
| 质检：待检/最近/不合格/合格率 | `quality.py todo / recent / fail / stats` |
| 采购在途 / 逾期 | `purchase.py incoming / overdue` |
| 客户档案 + 成交汇总 | `partner.py show <客户名>` |
| 今日/昨日总览（晨报数据源） | `overview.py today / yesterday` |
| 单据留言@同事（确认制） | `actions.py note <单号> --text ... [--at 姓名]` |
| 跟进提醒（确认制） | `actions.py remind <单号> --to 姓名 --date 日期` |
| 调生产计划 / 调承诺交期（确认制） | `actions.py reschedule / delay` |
| 合同·唛头·施工单 PDF 直发 | `report.py pdf <单号> --report contract\|label\|workorder` |
| 报价编辑（改量/价/折扣、加删行） | `quote.py edit <SO> --set / --add / --del` |
| 报价带品牌档案 | `quote.py draft … --brand 品牌名` |
| 文本一句话建客户档案 | `partner.py add --text "姓名 电话 地址"` |
| 工艺要求→车间（关联制造单） | `actions.py worknote <SO> --text … [--at 姓名]` |
| 跟进活动 完成 / 改期 | `actions.py activity-done / activity-reschedule` |

完整命令与对话映射见 [references/commands.md](references/commands.md)。

## 路线图

**已交付（v1.4.0）**

- **P0** ✅：十项查询（订单穿透 / 在制 / 欠料 / 库存 / 质检 / 采购 / 客户 / 总览 / 渠道 / 晨报）
- **P1** ✅：写操作闭环（留言@人、跟进提醒、调计划/交期，全部确认制）+ 合同/唛头/施工单 PDF 直发
- **P2** ✅：晨报/预警生成器（定时推送一条命令启用）
- **P3** ✅：拍照质检（挂图+判定）、非标报价草稿对话流、渠道来源统计
- **P4** ✅：协同起草增强——工艺要求→车间看板、报价编辑·带品牌、文本一句话建档、跟进闭环（营销数据同步待客户聚光授权后接入）

**操作能力规划（演进中）**

- **P5 流程推进**：报价转订单、生产/采购单据推进、缺料一键补货 + 企微审批、报价直发客户（全程人工确认）
- **P6 现场执行闭环**：确认发货、车间报工完工、收货确认（全程人工确认 + 向导校验）

> **安全边界**：所有写操作两段式确认（先预览、人点头才落笔）；开票、收款等涉及财务的敏感动作坚持人工操作，智能体只起草与提醒。详见操作规划。

---

<div align="center">

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** postmaster@huo15.com | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**

<img src="https://tools.huo15.com/uploads/images/system/qrcode_yxzk.jpg" alt="逸寻智库公众号二维码" style="width: 200px; height: auto; margin: 10px 0;" />

</div>

---
