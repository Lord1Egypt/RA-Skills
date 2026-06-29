# huo15-furniture-mfg 完整命令参考

> 所有命令在 `scripts/` 目录下执行。查询脚本只读；写操作集中在 `actions.py`（确认制）。
> 凭据未配置时任何命令都会提示先跑 `login.py init`。

## login.py — 凭据管理

```bash
python3 login.py init                 # 交互式：① 地址 ② 数据库 ③ 账号 ④ 密码（默认 test.heysleep.cn / test）
python3 login.py show                 # 显示当前配置（secret 脱敏）
python3 login.py test                 # 验证连接（成功打印 用户名/uid）

# 非交互（AI 推荐用法，secret 走 stdin 不进 shell 历史）：
printf '%s' "$PASSWORD" | python3 login.py set --login <账号> --secret-stdin
printf '%s' "$APIKEY"   | python3 login.py set --login <账号> --auth-type apikey --secret-stdin
# 可选 --url / --db / --transport jsonrpc
```

- 凭据写 `~/.huo15/tools.md` 标记块 `<!-- huo15-furniture-mfg:start/end -->`，与 huo15-huihuo-odoo 的块互不干扰；可用 `FMFG_TOOLS_MD` 改路径。
- 临时覆盖（不落盘）：环境变量 `FMFG_ODOO_URL / FMFG_ODOO_DB / FMFG_ODOO_LOGIN / FMFG_ODOO_SECRET`。

## order.py — 订单跟踪（跟单核心）

```bash
python3 order.py status SO-260531-758      # 按单号（支持模糊，如 260531-758）
python3 order.py status 梁泽光              # 按客户名 → 该客户最近订单展开
python3 order.py list                       # 最近 30 天订单
python3 order.py list --undelivered         # 只看没发完的（pending/started/partial）
python3 order.py list --customer 亿美诺 --days 90 --limit 50
```

`status` 输出五段：**订单头**（状态/发货/开票/金额/交期/销售/跟单/来源单号）→ **明细**（订购/已发）→ **生产**（关联 MO 状态+备料+完工）→ **发货**（出库单状态/计划/完成）→ **质检**（挂在 MO/出库单上的检查及结果）。
多张匹配时第一张全量展开，其余表格摘要。

## mfg.py — 生产

```bash
python3 mfg.py wip [--limit 30]            # 在制（已确认/生产中/待关闭），按截止日期升序
python3 mfg.py late                         # 延期：截止日期已过仍未完工
python3 mfg.py shortage                     # 等料/缺料的在制单列表（components_availability_state）
python3 mfg.py shortage MO-260604-643       # 展开该单组件：需求 vs 可预测供应，缺口行标 ⚠️
```

注意：和栖大部分 MO 不挂 BOM → 展开模式会提示"无组件清单"；列表模式（齐料/等料判断）始终有效。

## inventory.py — 库存

```bash
python3 inventory.py find 山隐              # 名称/内部编号/条码/型号(x_studio_xinghao) 四字段 OR 模糊
python3 inventory.py find C3 --limit 20
```

列：在手 / 可用(free) / 入向 / 出向 / 预测；行首 ❗=负库存，○=零库存；按在手量降序（本地排序）。

## quality.py — 质检

```bash
python3 quality.py todo                     # 待检（quality_state=none）
python3 quality.py recent --days 7          # 最近 N 天质检记录
python3 quality.py fail --days 30           # 不合格清单
python3 quality.py stats --days 30          # 合格率，按检查项目(title)分组
```

## purchase.py — 采购到货

```bash
python3 purchase.py incoming                # 在途（state=purchase 且未收齐），⚠️=超预计到货日
python3 purchase.py overdue                 # 只看逾期的
```

## partner.py — 客户

```bash
python3 partner.py show 亿美诺 [--limit 10]
```

输出：联系方式/地址/业务员/应收余额 + 成交汇总（单数/总额）+ 最近订单表。同名多档案会列出其余候选。

```bash
# 文本一句话建客户档案（huo15_contact_autofill 自动解析姓名/电话/地址，确认制）
python3 partner.py add --text "李梦 13800001234 广东佛山顺德乐从家具城A区12号"
python3 partner.py add --text "..." --yes
python3 partner.py remove 921 --yes        # 删联系人（仅无关联订单的，误建补救）
```

注：res.partner 无 mobile 字段（Odoo 19 并入 phone）；create 须带 name，本命令用文本首段占位、解析后覆盖；name 若仍含手机号数字会自动回退首段姓名保持整洁。

## overview.py — 总览（晨报数据源）

```bash
python3 overview.py today                   # 接单/应交未发/完工/发货/质检 + 风险快照
python3 overview.py yesterday
```

风险快照与日期无关，反映当前态：在制 N 张 | 延期 N 张 | 缺料 N 张 | 采购逾期 N 张 | 待检 N 张。

## actions.py — 写操作（P1，确认制）

**所有命令默认 dry-run 只打印预览；必须显式加 `--yes` 才执行。**
AI 工作流：dry-run → 把预览转述给用户 → 用户明确同意 → 同命令加 `--yes` 重跑。

```bash
# 单据留言（沟通流 comment，@的人收通知）；单号支持 SO-/MO-/PO-/DO-/QC 前缀自动路由
python3 actions.py note SO-260531-758 --text "客户催货，请优先安排" --at 冯广权
python3 actions.py note SO-260531-758 --text "..." --at 冯广权 --at 杨香莲 --yes

# 跟进提醒（待办活动，挂单据上，负责人系统/邮件收到）
python3 actions.py remind SO-260531-758 --to 冯广权 --date 2026-06-16 \
    --summary "回复客户交期" --note "客户问能否提前"

# 调制造单计划开始（只支持 MO；时间可省略默认 08:00）
python3 actions.py reschedule MO-260519-543 --start "2026-06-16 08:00"

# 调销售单承诺交期（只支持 SO；预览会提示先与客户达成一致）
python3 actions.py delay SO-260531-758 --date 2026-06-20

# 撤回误发留言（note 执行成功时会打印对应 undo 命令）
python3 actions.py undo-note 42915 --yes

# 订单工艺要求 → 关联制造单留言 + @车间（SO 自动路由到其关联 MO；无 MO 写在来源单）
python3 actions.py worknote SO-260531-758 --text "床垫围边加厚2cm，海绵密度45D" --at 一组-张三

# 跟进活动 完成 / 改期（活动 id 或单号；单号取其上最近一条待办活动）
python3 actions.py activity-done MO-260604-643 --feedback "已电话回复"
python3 actions.py activity-reschedule 1156 --date 2026-06-25
```

防呆：`--at`/`--to` 只接受内部用户姓名/账号，找不到报错、多匹配列候选（绝不静默猜人）；
单据类型不符（如对 SO 跑 reschedule）直接拒绝。

## report.py — 单据 PDF（合同 / 唛头 / 施工单）

```bash
python3 report.py list [--model sale|mo|picking|qc]   # 列出系统全部 PDF 报表
python3 report.py pdf SO-260531-758 --report contract  # 销售合约·客户版
python3 report.py pdf SO-260531-758 --report quote     # 标准报价单
python3 report.py pdf DO-260604-606 --report label     # 包装唛头 A5（DO 或 MO）
python3 report.py pdf MO-260604-643 --report workorder # 生产施工单
python3 report.py pdf DO-260604-606 --report delivery  # 交货单自定义联次
# 别名外也可直接传完整 report_name；-o 指定输出目录（默认 /tmp/fmfg-reports）
```

输出绝对路径后，AI 必须把 PDF **作为文件消息发给用户**（不要发本地路径/链接）。
实现：web session 认证 + `GET /report/pdf/<report_name>/<id>`（XML-RPC 渲染不了 QWeb）。

## quality.py 写命令 — 拍照质检（P3，确认制）

```bash
# 挂照片：QC 号直挂；传 MO 号自动定位其待检质检单（picture_ids 多图，挂前预览）
python3 quality.py attach MO-260604-643 --image /path/qc1.jpg --image /path/qc2.jpg
python3 quality.py attach QC00618 --image /path/qc1.jpg --yes
python3 quality.py detach <附件id...> --yes        # 误传补救（attach 成功时打印 id）

# 质检判定（do_pass / do_fail，判定后不可随意撤销——必须用户明说结果才执行）
python3 quality.py judge QC00618 --result pass
python3 quality.py judge QC00618 --result fail --yes
```

企微/微信里用户发图 → AI 先把图片落盘（消息媒体目录），拿绝对路径再 attach。

## quote.py — 非标定制报价草稿（P3，确认制）

```bash
# 行格式 产品关键词:数量[:长*宽*高(cm)[:主料]]，--line 可重复；只建 draft 草稿不通知任何人
python3 quote.py draft --customer 李梦 \
    --line "山隐主垫-舒睡版:1:2000*2200*280:进口乳胶" \
    --line "山隐顶垫:2" \
    --note "客户要求加厚围边"
python3 quote.py draft --customer 李梦 --line "山隐顶垫:2" --brand HeySleep --yes   # 带品牌档案
python3 quote.py drop SO-260613-855 --yes          # 删草稿（仅 draft 可删）

# 编辑草稿报价行（仅 draft）：改量/价/折扣、加行、删行；不带操作参数 = 列出当前行
python3 quote.py edit SO-260613-856                              # 列出当前行（带行号）
python3 quote.py edit SO-260613-856 --set 1:3:1200 --add "山隐顶垫:1" --del 2 --yes
```

- 尺寸/主料写入 sale_product_custom 定制字段（custom_length/width/height/material +
  is_custom_product），实测定价逻辑会按非标尺寸自动算价
- `--brand` 带 sale_brand_extension 品牌档案（brand_id：Logo/付款码/地址/条款）；错名会列可用品牌
- `edit --set N:数量[:单价[:折扣]]`，N 是列行命令显示的行号；--add 复用 draft 行格式；--del 传行号
- 产品同名多匹配时预览会列候选，匹配错就换更精确关键词重跑

## order.py channels — 渠道来源统计（P3，只读）

```bash
python3 order.py channels --days 30
```

电商平台单（x_source_order_ref 非空）vs 直营/经销，单数/占比/金额 + 平台单号前缀分布。
实测 60 天：电商 66% 单量 ¥88 万 vs 直营 34% 单量 ¥113 万（直营客单更大）。
注：huo15_xhs_shop / huo15_douyin_ecommerce 连接器在 test 库未安装，装上后可按
`x_xhs_order_id` / `douyin_order_id` 精确分平台。

## digest.py — 晨报 / 风险预警（P2 数据源）

```bash
python3 digest.py morning                  # 晨报：昨日成绩 + 今日应交 + 风险快照 + 延期TOP3
python3 digest.py alerts                   # 风险预警：延期/采购逾期/缺料/待检积压
python3 digest.py alerts --quiet-if-clean  # 无风险时不输出（定时任务用）
python3 digest.py alerts --qc-backlog 80   # 自定义待检积压报警阈值（默认 50）
```

输出为企微友好纯文本（实测晨报约 0.5KB，远低于企微单条 2048 字节限制），可整段直接发送。

### 接 OpenClaw 原生 cron 定时推送（由用户自行执行启用）

```bash
# 每天 8 点晨报 → 发到指定企微会话（把 <目标> 换成接收人/群，如 ZhaoBo 或群 chatid）
openclaw cron add \
  --name "和栖制造晨报" \
  --cron "0 8 * * *" --exact --tz Asia/Shanghai \
  --session isolated --announce --channel wecom --to <目标> \
  --timeout-seconds 120 \
  --message "运行这条命令：cd /Users/jobzhao/workspace/projects/openclaw/furniture_manufacturing/furniture_agents/huo15-furniture-mfg/scripts && python3 digest.py morning ——把 stdout 原样作为最终回复，不要增删改写。报错则回复一行错误摘要。"

# 工作时段每 4 小时风险预警（无风险静默）
openclaw cron add \
  --name "和栖风险预警" \
  --cron "0 9,13,17 * * *" --exact --tz Asia/Shanghai \
  --session isolated --announce --channel wecom --to <目标> \
  --timeout-seconds 120 \
  --message "运行：cd .../huo15-furniture-mfg/scripts && python3 digest.py alerts --quiet-if-clean ——stdout 非空则原样回复；stdout 为空说明无风险，回复 NO_REPLY 结束。"
```

> 设计依据：推送走 OpenClaw 原生 cron（不自造调度器）；预警用 `--quiet-if-clean` 避免无风险时刷屏。

## 典型对话 → 命令映射

| 用户说 | 执行 |
|---|---|
| "梁泽光那张床垫到哪一步了" | `order.py status 梁泽光` |
| "SO-260531-758 发货了吗" | `order.py status SO-260531-758`（看"发货"段） |
| "这个月哪些单还压着没发" | `order.py list --undelivered` |
| "车间现在堆了多少活" | `mfg.py wip` |
| "有没有拖期的" | `mfg.py late` |
| "山隐舒睡版还有现货吗" | `inventory.py find 山隐 舒睡 → find 山隐` |
| "今天质检怎么样/还有多少没检" | `quality.py todo` + `overview.py today` |
| "上个月合格率多少" | `quality.py stats --days 30` |
| "面料什么时候到" | `purchase.py incoming` |
| "亿美诺今年做了多少" | `partner.py show 亿美诺` |
| "给我来个晨报" | `overview.py yesterday` + `overview.py today` 合并口播 |
| "这单留个言让张三跟进" | `actions.py note <单号> --text ... --at 张三`（dry-run→确认→--yes） |
| "提醒冯广权周一回客户" | `actions.py remind <单号> --to 冯广权 --date <周一>`（确认制） |
| "这单生产挪到周三早上" | `actions.py reschedule <MO号> --start "<周三> 08:00"`（确认制） |
| "交期改到20号" | `actions.py delay <SO号> --date <20号>`（确认制，提醒先和客户对齐） |
| "把合同发我" | `report.py pdf <SO号> --report contract` → 文件消息发出 |
| "打个唛头" | `report.py pdf <DO/MO号> --report label` → 文件消息发出 |
