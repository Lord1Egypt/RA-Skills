# 技能地图（SKILL-MAP）

> 用途：**从"我手上这件事"出发找技能**，而不是从技能名字猜。
> 每个技能自己那一页（`skills/<名>/README.md`）都有「什么时候不要用我」，两页配合看不会走错。
> 28 个技能。新增技能必须在本页登记，`tools/validate_skills.py` 会核。

---

## 一、三秒定位：我正在做什么

| 我正在做的事 | 打开这个技能 |
|---|---|
| 接待一个刚进门的客户，问清他要什么 | `sales-reception-sop` |
| 判断这个客户是 A/B/C，后面怎么跟 | `sales-lead-grading` |
| 客户说"太贵了/再看看/怕烂尾" | `sales-objection-handling` |
| 客户谈到价格，要算价、要逼定 | `sales-closing-sop` |
| 客户问首付、流水、征信、公积金、批贷 | `sales-mortgage-sop` |
| 明天开盘，谁站哪、怎么选房、出事了怎么办 | `sales-opening-sop` |
| 客户问"你们这个户型好在哪"，要一段可直接说的话 | `sales-talk-library` |
| 甲方问我"这个盘还能不能接、去化卡在哪" | `developer-sales-advisor` |
| 要排蓄客节奏、定阶段性营销动作 | `presale-marketing-sop` |
| 要做本月竞品报告 | `competitive-intel-sop` |
| 要做物料、要看示范区哪里不对 | `marketing-materials-sop` |
| 要办一场暖场/圈层/认筹活动 | `activity-organization-sop` |
| 要定价格体系、优惠怎么放、放到第几步 | `pricing-incentive-release-sop` |
| 要定渠道配比、佣金点位、判渠道健不健康 | `channel-management-advisor` |
| 要落渠道报备、带访交接、佣金对账（执行） | `channel-collaboration-sop` |
| 要打通"蓄客→开盘"整场战役的协同 | `launch-integrated-campaign-sop` |
| 要做工程进度与品质播报 | `engineering-progress-broadcast-sop` |
| 要做老带新、口碑、客诉隔离 | `customer-advocacy-referral-sop` |
| 要拿房源委托、签独家、防跳单 | `broker-listing-sop` |
| 要给二手客户配房、带看、议价、过户 | `broker-client-deal-sop` |
| 要接租赁委托、带看、签租约、处理欠租退租 | `broker-lease-sop` |
| 要看一块地能不能拿、要不要做可研 | `project-feasibility-advisor` |
| 客户要买商铺/写字楼/公寓，判断值不值 | `commercial-property-advisor` |
| 单子签了，卡在贷款/赎楼/过户/交房 | `resale-transaction-sop` |
| 明天去交房，要拿一张清单逐项查 | `handover-inspection-advisor` |
| **我是业主，要卖房**（挂多少、找谁、什么时候点头） | `owner-sell-home-advisor` |
| **我是业主，要出租**（租多少、配什么、租客怎么筛） | `owner-rental-advisor` |
| **我是买家，判断这套该不该买** | `buyer-first-home-advisor` |
| 我自己的账号要出内容（短视频/图文） | `property-media-creator` |
| 任何价格/税费/月供/佣金/回报/得房率的数字 | `calc-toolkit`（禁止口算） |

---

## 二、六条主线（按一周的真实工作流排序）

**① 案场销售线（置业顾问）**
`sales-reception-sop`（接待问需求）→ `sales-lead-grading`（判级定跟进）→ `sales-objection-handling`（应对异议）→ `sales-closing-sop`（算价逼定，数字走 `calc-toolkit`）→ `sales-opening-sop`（开盘选房）
穿插：`sales-talk-library`（要话术时查）、`sales-mortgage-sop`（客户问贷款时）

**② 策划线**
`presale-marketing-sop`（定节奏与动作）→ `competitive-intel-sop`（盯竞品）→ `marketing-materials-sop`（出物料/看示范区）→ `activity-organization-sop`（办活动）→ `pricing-incentive-release-sop`（定优惠释放）→ `engineering-progress-broadcast-sop`（播报进度）
战役级协同：`launch-integrated-campaign-sop`（把上面几条串成一场开盘）

**③ 甲方/营销负责人**
`developer-sales-advisor`（五维体检出结论）→ `pricing-incentive-release-sop`（价格与优惠）→ `channel-management-advisor`（渠道配比与佣金）→ `launch-integrated-campaign-sop`（战役协同）→ 周报与预警回到 `developer-sales-advisor`

**④ 二手经纪线**
`broker-listing-sop`（拿售房委托）→ `broker-client-deal-sop`（配房成交）→ `calc-toolkit`（佣金/税费/解押）
租赁业务另走一条：`broker-lease-sop`（委托核验 → 报价带看 → 筛租客 → 签租约 → 交房 → 退租与欠租）→ `calc-toolkit/commission.py --scene lease`
交叉：业主自己来问卖房 → 转 `owner-sell-home-advisor`（你只做经纪端，别替业主定价）

**④-b 交易与交付线（成交之后）**
`broker-client-deal-sop` 谈成之后进入 `resale-transaction-sop`（查档 → 定金与合同 → 网签与资金监管 → 贷款审批 → 缴税过户 → 放款交房），数字走 `calc-toolkit`（`tax.py` / `deposit.py` / `loanterm.py` / `status.py` / `area_error.py`）
交房当天：二手交房走 `resale-transaction-sop` Part 6；新房/专业验收清单走 `handover-inspection-advisor`（面积误差用 `area_error.py`，费用核对用 `newhome.py`）
红线：过户前必复检查档（签约前查过不等于过户那天还干净）；没钱进监管就不付大额首付

**⑤ 业主线**
卖房 `owner-sell-home-advisor`（净得测算 → 定价 → 选中介 → 议价 → 过户）
出租 `owner-rental-advisor`（回报测算 → 定价 → 合规准备 → 筛租客 → 合同 → 履约）
决策分叉：先算 `calc-toolkit/rent.py --net` 与 `buy_vs_invest.py`，再决定"留还是卖"

**⑥ 购房者线**
`buyer-first-home-advisor`（需求七问 → 预算三线 → 选筹打分 → 看房验真 → 议价签约 → 收房）
数字：`calc-toolkit`（capacity / status / fund / tax / newhome / mortgage / prepay）

---

## 三、按交付物反查（"明天要交什么"）

| 交付物 | 主技能 | 必须一起跑的工具 |
|---|---|---|
| 客户算价单 | `sales-closing-sop` | `tax.py` `mortgage.py` `commission.py` |
| 一页纸客户画像与跟进计划 | `sales-lead-grading` | — |
| 开盘执行手册 | `sales-opening-sop` | — |
| 单盘经营体检与三档结论 | `developer-sales-advisor` | `commission.py --scene channel` |
| 竞品月度报告 | `competitive-intel-sop` | — |
| 价格与优惠释放方案 | `pricing-incentive-release-sop` | `tax.py` `newhome.py` |
| 渠道政策与费效测算 | `channel-management-advisor` | `commission.py --scene channel --tiers` |
| 渠道月度对账表 | `channel-collaboration-sop` | `commission.py --scene channel` |
| 房源委托方案（含独家对价） | `broker-listing-sop` | — |
| 二手客户配房与议价方案 | `broker-client-deal-sop` | `tax.py` `commission.py --scene resale` |
| 租赁委托一页纸 / 带看记录卡 / 房屋交接单 | `broker-lease-sop` | `commission.py --scene lease` `rent.py --net` |
| 一页纸投前测算 / 敏感性表 / 可研报告 | `project-feasibility-advisor` | `feasibility.py`（盈亏平衡 + 敏感性） |
| 商业一页纸估值卡 / 隐含 cap 反查 / 租约核对表 | `commercial-property-advisor` | `commercial.py`（NOI / cap / 持有 IRR） |
| 交易时间轴 / 风险排查表 / 税费买卖分列清单 | `resale-transaction-sop` | `tax.py` `deposit.py` `loanterm.py` `status.py` |
| 交房验收清单 / 问题清单 / 面积补退核对 | `handover-inspection-advisor` | `area_error.py` `efficiency.py` `newhome.py` |
| **卖房决策一页纸** | `owner-sell-home-advisor` | `tax.py` `commission.py` `prepay.py` `deposit.py` |
| **出租决策一页纸** | `owner-rental-advisor` | `rent.py --net` `holding.py` `buy_vs_invest.py` |
| 购房预算三线表 | `buyer-first-home-advisor` | `capacity.py` `status.py` `fund.py` |
| 看房检查清单与结论（买/不买/再看） | `buyer-first-home-advisor` | `tax.py` `newhome.py` |
| 短视频脚本与选题卡 | `property-media-creator` | — |

---

## 四、四条最容易走错的岔路

1. **业主 vs 经纪人**：业主来问"我这房挂多少"，用 `broker-listing-sop` 会得到"怎么说服业主降价"的视角，方向反了 → 用 `owner-sell-home-advisor`。
2. **执行层 vs 决策层**：要"跟渠道对账"，用 `channel-management-advisor` 会得到一套配比与佣金设计，答案不对题 → 用 `channel-collaboration-sop`。
3. **卖 vs 租**：明明是出租，翻 `owner-sell-home-advisor` 的净得测算，会漏掉回报率与空置成本 → 用 `owner-rental-advisor`（Part 1 就能给出"留还是卖"的结论）。
4. **成交前 vs 成交后**：合同已经签了、卡在贷款/赎楼/过户，翻 `broker-client-deal-sop` 会得到配房与议价方法，答不对题 → 用 `resale-transaction-sop`；交房当天的专业验收 → `handover-inspection-advisor`（别用交易流程技能替代验收清单）。

---

## 五、维护规则（改本页之前先读）

1. 新增技能：本页第一节加一行、第二节归入某条主线、第三节若对应交付物就补一行。
2. 改技能名或拆分技能：全仓 `grep` 旧名，连边界段、QUICKSTART、README 一起改；`tools/check_refs.py` 只查脚本与 Part，技能名引用靠人查。
3. 每次发版跑：`python3 tools/validate_skills.py`（含本页登记校验）、`--spec-strict`、`python3 tools/check_refs.py`、`python3 tools/check_commands.py`。
