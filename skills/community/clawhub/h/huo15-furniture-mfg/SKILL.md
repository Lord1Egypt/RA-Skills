---
name: huo15-furniture-mfg
displayName: 家具制造业智能体（和栖家居）
description: >-
  Use this skill whenever the user asks about furniture manufacturing
  operations on the HeySleep/和栖家居 system — order tracking ("这个订单到哪一步了"
  "SO-260531-758 什么情况" "梁泽光的单发了吗" "哪些订单还没发货"), production
  ("在制有多少" "生产进度" "哪些制造单延期了" "MO-xxx 缺什么料" "欠料/缺料"),
  inventory ("山隐主垫还有几张" "库存查询" "型号 C3 有货吗"), quality ("待检"
  "质检合格率" "最近有没有不合格"), purchasing ("采购到货了吗" "哪些采购单逾期"),
  customers ("亿美诺的档案" "这个客户成交多少"), daily overview ("今日总览"
  "晨报" "今天接了几单/发了几单"), write actions ("给这个单留言" "@张三跟进"
  "提醒冯广权周一回复客户" "交期改到20号" "生产提前到周三" "改这单报价"
  "把这个客户存一下" "工艺要求发给车间" "这个跟进做完了"), or documents
  ("打印合同" "发我唛头标签" "要个施工单 PDF"). Backed by the 和栖家居
  manufacturing system (test.heysleep.cn, db=test, 辉火云企业套件 v19) over
  XML-RPC. Also handles photo QC ("把这几张照片挂到质检单" "质检判合格"),
  custom-size quotations ("客户要 2 米乳胶床垫报个价" "建个报价草稿"), and
  channel analysis ("电商单占多少" "渠道分布"). Also triggers on: 和栖,
  heysleep, 床垫订单, 跟单, 交期, 制造单, 生产单, 发货状态, 山隐, 山宿,
  销售合约, 唛头, 拍照质检, 非标报价. First run: python3 scripts/login.py init
  (地址/数据库/账号/密码 → ~/.huo15/tools.md, chmod 600). Pure standard
  library, zero dependencies. Write actions are two-step confirm-gated
  (dry-run preview → user approves → --yes).
version: 1.4.0
aliases:
  - 家具制造智能体
  - 和栖家居
  - heysleep
  - 床垫工厂
  - 订单跟踪
  - 跟单助手
  - 订单到哪了
  - 生产进度
  - 在制清单
  - 欠料检查
  - 缺料
  - 延期订单
  - 库存查询
  - 质检合格率
  - 待检清单
  - 采购到货
  - 客户档案
  - 今日总览
  - 生产晨报
  - 订单留言
  - 跟进提醒
  - 调整交期
  - 打印合同
  - 唛头标签
  - 报价编辑
  - 改报价
  - 文本建档
  - 客户建档
  - 车间工艺要求
  - 跟进完成
dependencies:
  python-packages: []   # 纯标准库，零第三方依赖
---

# 家具制造业智能体 v1.4（和栖家居 · 查询 + 确认制操作 + 行业深化）

通过 XML-RPC 操作和栖家居制造系统（**辉火云企业套件 v19**，test.heysleep.cn，db=`test`）。
**查询**：订单穿透 / 在制 / 欠料 / 库存 / 质检 / 采购 / 客户 / 总览 / 渠道分布 / 晨报预警（只读）。
**操作**（确认制）：留言@人 / 跟进提醒 / 跟进完成·改期 / 调生产计划 / 调承诺交期 /
报价起草·编辑·带品牌 / 文本一句话建客户档案 / 工艺要求→车间看板 / 拍照质检（挂图+判定）/
合同·唛头 PDF。

**收到图片要挂质检单时**：先把图片落盘拿到本地路径，再 `quality.py attach <单号> --image <路径>`
走确认制；判定（judge）不可随意撤销，必须用户明确说"判合格/不合格"才执行。

> **完整命令与输出示例** → [references/commands.md](references/commands.md)
> **API/字段坑（改代码前必读）** → [references/heysleep-mfg-api.md](references/heysleep-mfg-api.md)

## 首次使用

```bash
cd <skill目录>/scripts
python3 login.py init        # ① 地址 ② 数据库 ③ 账号 ④ 密码（默认 test.heysleep.cn / test）
python3 login.py test        # 验证连接
```

凭据存 `~/.huo15/tools.md`（标记块独立，与 huo15-huihuo-odoo 共存，权限 600）。
AI 非交互配置用：`printf '%s' "$PASSWORD" | python3 login.py set --login <账号> --secret-stdin`。

## 命令速查（均在 scripts/ 下执行）

| 用户在问 | 命令 |
|---|---|
| 这个订单到哪了 / 什么时候能发货 | `python3 order.py status <订单号或客户名>` |
| 哪些订单没发完 / 最近订单 | `python3 order.py list --undelivered` / `--days N --customer X` |
| 在制有多少 / 生产排到哪了 | `python3 mfg.py wip` |
| 哪些生产延期了 | `python3 mfg.py late` |
| 缺料吗 / MO-xxx 欠什么料 | `python3 mfg.py shortage [制造单号]` |
| xx 还有几张库存 / 型号 C3 有货吗 | `python3 inventory.py find <关键词>` |
| 有多少待检 / 最近质检 / 不合格 | `python3 quality.py todo` / `recent` / `fail` |
| 质检合格率 | `python3 quality.py stats [--days N]` |
| 采购到货了吗 / 哪些逾期 | `python3 purchase.py incoming` / `overdue` |
| 客户档案 / 成交历史 | `python3 partner.py show <客户名>` |
| 今日总览 / 晨报 | `python3 overview.py today` / `yesterday` |
| 给单据留言 / @同事 | `python3 actions.py note <单号> --text "..." [--at 姓名]` |
| 提醒某人跟进 | `python3 actions.py remind <单号> --to 姓名 --date YYYY-MM-DD` |
| 调生产计划开始 | `python3 actions.py reschedule <MO号> --start "日期 时间"` |
| 调承诺交期 | `python3 actions.py delay <SO号> --date YYYY-MM-DD` |
| 打印合同 / 唛头 / 施工单 | `python3 report.py pdf <单号> --report contract\|label\|workorder` |
| 晨报 / 风险预警（一条消息体量） | `python3 digest.py morning` / `alerts [--quiet-if-clean]` |
| 拍照挂质检单 / 质检判定 | `python3 quality.py attach <QC或MO号> --image 路径` / `judge <QC号> --result pass\|fail` |
| 非标报价草稿（尺寸+主料+品牌） | `python3 quote.py draft --customer X --line "产品:数量[:长*宽*高[:主料]]" [--brand 品牌名]` |
| 改报价草稿（改量/价/折扣、加删行） | `python3 quote.py edit <SO> --set N:数量[:单价[:折扣]] / --add 产品:数量 / --del N` |
| 文本一句话建客户档案 | `python3 partner.py add --text "姓名 电话 地址"` |
| 工艺要求→车间(关联制造单) | `python3 actions.py worknote <SO> --text "..." [--at 姓名]` |
| 跟进活动 完成 / 改期 | `python3 actions.py activity-done <活动id或单号>` / `activity-reschedule <id> --date` |
| 电商 vs 直营渠道分布 | `python3 order.py channels [--days 30]` |

## 写操作确认制（铁律，违反 = 事故）

`actions.py` 所有命令默认 **dry-run**（只打印预览，不写系统）：

1. 用户提出写操作 → 先**不带 --yes** 跑一次，把「将要执行」预览**原样转述给用户**
2. 用户明确回复同意（"确认" "可以" "执行"）→ 同一命令**加 --yes** 重跑
3. 用户没确认、含糊、或改了主意 → 绝不执行；绝不第一次就带 --yes
4. `--at`/`--to` 只接受内部用户姓名，解析不到会报错列候选——**不要**自己猜着换人
5. 留言误发可撤：`actions.py undo-note <message_id> --yes`

## PDF 直发规则

`report.py pdf` 输出本地文件路径后，**把 PDF 作为文件消息发送给用户**（走当前
聊天通道的发文件能力）；绝不发 `/tmp/...` 本地路径或 localhost 链接当作交付。

## 回答用户时的规则

1. **先跑命令再回答**，把脚本输出转成口语化中文摘要；表格可直接展示。
2. 用户给的单号/客户名**原样透传**做模糊匹配，不要自行改写或猜补全。
3. 订单类问题优先 `order.py status`——一条命令含 明细/生产/发货/质检 全链路，不用分四次查。
4. 风险词（延期/缺料/逾期/不合格）回答时**给出下一步建议**（如"延期 23 张，要看明细吗"；
   用户说"催一下"→ 走 `actions.py note/remind` 确认制流程）。
5. 写操作只有上面五种；用户要求其他写动作（确认订单/录质检结果/开票等）时说明暂不支持、
   属后续版本。
6. **绝不**把 `~/.huo15/tools.md` 内容、密码、API Key 输出到对话。

## 业务底色（和栖家居，2026-06 实测）

- 床垫制造，按单生产（MTO）：SO → MO（`origin`=SO 单号，覆盖率 92%）→ 出库 → 质检
- 产品线：山隐/山宿系列主垫+顶垫，大量非标尺寸（产品名内嵌规格如 `1800*2000*280`）
- 制造单基本不挂 BOM（全库组件行个位数）→ 欠料逐项分析仅对挂了 BOM 的单有效
- 质检 94% 不挂产品（挂在作业类型），统计按检查项目（成品入库质检/销售出库质检）分组
- 定制字段在用：跟单人 `x_follower_user_id`、销售人 `x_salesperson_user_id`、来源单号 `x_source_order_ref`、实际发货 `x_actual_shipment_time`、型号 `x_studio_xinghao`

## 字段坑速查（Odoo 19 / 本库实测，改代码前对照）

| 坑 | 正确做法 |
|---|---|
| 质检状态字段 | `quality_state`（none/pass/fail），**没有** `state` 字段 |
| name_search 参数 | Odoo 19 是 `domain=`，传 `args=` 直接 TypeError |
| 库存数量排序 | `qty_available` 等非存储计算字段不能进 `order`，取回后本地排 |
| 组件实收数量 | Odoo 19 是 `quantity`（不是 17 以前的 `quantity_done`） |
| SO→MO 链路 | `mrp.production.origin = sale.order.name`（92% 覆盖） |
| SO→出库链路 | 优先 `stock.picking.sale_id`，回退 `origin` |
| Datetime 时区 | 全部 UTC 存储，显示用 `odoo_utils.from_utc`，当天范围用 `day_range_utc` |
| 分组聚合 | `read_group` 多 groupby 必 `lazy=False` |
| message_post 返回 | XML-RPC 序列化成 `[id]` 列表，取标量再用 |
| 活动 mail.activity | `date_deadline` 是 Date；需 `res_model_id`(ir.model id)；To-Do 类型 id=4 |
| QWeb PDF 渲染 | XML-RPC 渲染不了，走 `/web/session/authenticate` + GET `/report/pdf/<name>/<id>`（report.py 已封装） |

## 安全

- 查询脚本零写入；写操作集中在 `actions.py` 且确认制（默认 dry-run + --yes 两段式）。
- 凭据文件权限 600；secret 永不进命令行参数（用 stdin）。
- 当前仅允许连 test 库（test.heysleep.cn / db=test）；生产环境上线须经发布流程审批。
