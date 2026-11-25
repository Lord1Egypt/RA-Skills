---
name: house-skills-kit
description: 房产AI技能仓库总览：按身份分技能（房开企业/经纪公司/渠道分销/购房者业主/二手经纪人/一手销售/房产自媒体）。共30个独立技能：calc-toolkit公共计算工具包、购房客户线首购购房顾问、开发商销售顾问、二手经纪线（房源开发与委托/客户匹配与成交/租赁作业）、交易与交付线（二手房交易全流程与风险/交房验收）、案场销售线与策划线十六技能（19件收官：房贷月供/二手房全成本/一手房成本/购房能力/提前还款/首套二套认定/楼层折扣/公积金额度/佣金提成/得房率换算/租金回报/LPR变动影响/持有成本/买房vs理财/面积误差补退/违约金定金/房龄贷款年限/楼面价货值/日照楼间距，35城规则库四层引擎，每个数字可追溯）；template/为品牌顾问技能生成骨架（4类角色原型×31业务模块）。Use when 需要房产相关AI技能的安装、使用、生成或按身份选型。
license: Apache-2.0
---

# house-skills-kit · 房产 AI 技能仓库

按身份分 Skill，按需取用。本文件是仓库总览；各技能在 `skills/` 子目录下，均为独立完整技能（自带 SKILL.md，可单独发布安装）。

## 技能索引

| 技能 | 路径 | 适合谁 |
|---|---|---|
| **calc-toolkit 公共计算工具包** | `skills/calc-toolkit/` | 全身份：19 件工具——房贷月供、二手房交易全成本、一手房交易成本、购房能力、提前还款、首套二套认定、楼层折扣、公积金额度、佣金提成、得房率换算、租金回报、LPR变动影响。35 城规则库四层引擎，每个数字可追溯，全参数 `--set` 可覆盖 |
| **buyer-first-home-advisor 首购购房顾问** | `skills/buyer-first-home-advisor/` | 购房客户（C 端自住）：需求澄清七问、预算三线法、资格与首套三口径、片区五维+楼盘百分制打分卡、一手五看法+二手15项验房、议价与合同十条、贷款与提前还款、收房税费、八类坑与红线、三句话收口 |
| **broker-listing-sop 二手房源开发与委托 SOP** | `skills/broker-listing-sop/` | 二手房经纪人/门店经理：六渠道房源开发与三筛、业主动因与价格校准四步、委托协议七要素与独家对价、实勘十二项与真房源档案、四档维护节奏、跳单证据链 |
| **broker-client-deal-sop 二手房客户匹配与成交 SOP** | `skills/broker-client-deal-sop/` | 二手房经纪人/交易专员：需求七问与资格预判、三维匹配打分、一场三套带看与二选一、买卖双线议价、七步交易流程与交房五交接、九类风险核验、佣金与跳单争议 |
| **broker-lease-sop 租赁经纪作业标准** | `skills/broker-lease-sop/` | 租赁经纪人/长租运营：委托六项核验与条款七项、三源锚点报价与空置换算、合法筛选边界与收入租金比、十项必备条款与佣金分摊（`commission.py --scene lease`）、交房五件套、退租四步、欠租四步与四类高风险情形 |
| **sales-talk-library 案场话术库** | `skills/sales-talk-library/` | 置业顾问/销售经理：地段/配套/户型/竞品/品牌五域标准说辞、分客群变通与合规红线 |
| **sales-objection-handling 客户异议处理** | `skills/sales-objection-handling/` | 置业顾问/销售经理：高频异议三段式应对、禁语清单与演练 |
| **sales-closing-sop 算价与逼定 SOP** | `skills/sales-closing-sop/` | 置业顾问/销售主管：算价动作链、议价博弈、逼定信号与团队配合逼定 |
| **sales-reception-sop 接待与需求挖掘 SOP** | `skills/sales-reception-sop/` | 置业顾问/销售主管：首访接待动线、七维需求挖掘、匹配带看与交接 |
| **sales-lead-grading 判客与跟进 SOP** | `skills/sales-lead-grading/` | 置业顾问/销售主管：ABC判客分级、跟进节奏、掉客挽回与归属仲裁 |
| **sales-mortgage-sop 按揭问题应对 SOP** | `skills/sales-mortgage-sop/` | 置业顾问/按揭专员：资质预判分流、六类高频按揭问题路径与话术、合规红线 |
| **sales-opening-sop 开盘执行 SOP** | `skills/sales-opening-sop/` | 置业顾问/案场负责人/开盘执行团队：盘前梳理预登记、认筹转认购、开盘日七环节选房动线、规则口径、五类应急预案、盘后转化 |
| **presale-marketing-sop 蓄客期营销动作清单** | `skills/presale-marketing-sop/` | 策划/营销负责人/自媒体运营：节点倒排节奏、暖场/拓客/圈层/认筹预热动作库、自媒体蓄客专节（定位/日历/线索闭环）、四级漏斗复盘、合规红线 |
| **competitive-intel-sop 竞品踩盘与市场监控** | `skills/competitive-intel-sop/` | 策划/营销负责人/市调岗：竞品A/B/C分级、六模块现场采集、百分制打分与竞品预判、四指标周监控三源交叉、月度竞品报告、反踩盘纪律与合规红线 |
| **activity-organization-sop 营销活动组织 SOP** | `skills/activity-organization-sop/` | 策划/营销负责人/案场负责人：活动目标定义、活动选型矩阵、一页简报、预算审批、执行清单、线索承接与复盘闭环、合规红线 |
| **marketing-materials-sop 营销物料与示范区优化 SOP** | `skills/marketing-materials-sop/` | 策划/示范区负责人/置业顾问：物料任务分类、设计简报、信息与合规审核、示范区四层巡检、改进台账、版本管理与反馈复盘 |
| **engineering-progress-broadcast-sop 工程进度与品质播报 SOP** | `skills/engineering-progress-broadcast-sop/` | 工程部/策划/品牌/案场客服：工程资料采集、节点对照、品质工艺表达、延期沟通、敏感问题升级、发布检查与复盘归档 |
| **pricing-incentive-release-sop 价格策略与优惠释放 SOP** | `skills/pricing-incentive-release-sop/` | 营销负责人/案场负责人/置业顾问：价格事实核验、房源与客户分层、优惠梯度、审批变更、案场执行、台账复盘与合规红线 |
| **channel-collaboration-sop 渠道协同与分销管理 SOP** | `skills/channel-collaboration-sop/` | 渠道负责人/项目营销/案场/财务：渠道准入分层、政策培训、报备查重、带访交接、判客仲裁、佣金对账与渠道复盘 |
| **owner-sell-home-advisor 卖房业主决策助手** | `skills/owner-sell-home-advisor/` | 二手房业主/置换业主：卖前决策与置换顺序、三源锚点定价四步与净得价倒算、可看性工程、选中介六维比选与委托条款七项、接单五问与定金违约、交易流程与五类纠纷预防、继承共有抵押查封等特殊情形 |
| **owner-rental-advisor 出租业主决策助手** | `skills/owner-rental-advisor/` | 出租业主/托管委托业主：该租该卖三选一与打平涨幅、租金定价与空置算术、房屋准备与合规红线、合法筛选边界与十项必备条款、履约纠纷四步留痕、自管与托管比选、合租短租学位等特殊情形 |
| **channel-management-advisor 渠道管理与分销决策助手** | `skills/channel-management-advisor/` | 项目营销负责人/渠道总监/财务：结构配比倒推、跳点双算法与费效上限、准入分级与合同八条款、归属仲裁、六指标诊断与汰换、飞单治理、年度框架谈判 |
| **property-media-creator 房产自媒体博主内容助手** | `skills/property-media-creator/` | 经纪人自营号/机构号/探盘博主：三圈定位、四源选题库、黄金 3 秒钩子与分型脚本、字幕与封面规范、平台红线与限流整改、私信六句转化、四指标复盘、变现与披露 |
| **customer-advocacy-referral-sop 客户口碑与老带新运营 SOP** | `skills/customer-advocacy-referral-sop/` | 客户关系/营销/案场/内容：服务反馈分层、口碑内容授权、推荐触发、线索登记、权益兑现、客诉隔离与复盘 |
| **launch-integrated-campaign-sop 节点开盘整合营销 SOP** | `skills/launch-integrated-campaign-sop/` | 营销负责人/策划：开盘战役简报、九格协同、节点倒排、资产包、整合承接、全员演练、开盘衔接与盘后复盘 |
| **marketing-review 模块（月度营销复盘与经营看板）** | `template/modules/marketing-review.md.tmpl` | 策划/营销：口径锁定、漏斗与房源结构、来源费效、异常升级与行动台账 |
| 案场销售顾问（排期） | `skills/`（待建） | 房开案场 |
| **二手经纪线（broker-listing-sop / broker-client-deal-sop / broker-lease-sop）** | `skills/broker-*/` | 二手经纪人/经纪公司（含租赁业务） |
| 渠道管理助手（排期） | `skills/`（待建） | 渠道分销 |
| **开发项目投前决策** | `skills/project-feasibility-advisor/` | 开发商投拓/项目总/代建咨询：拿地三指标、定位三问、成本六块、敏感性、决策阈值、可研八章 |
| **商业物业投资决策** | `skills/commercial-property-advisor/` | 商铺/写字楼/公寓：收益法估值、隐含 cap 反查、租约条款、持有期 IRR、七类陷阱 |
| **二手房交易全流程与风险** | `skills/resale-transaction-sop/` | 12 节点时间轴、查档六项、定金罚则、合同必写 12 条、资金监管、赎楼三条路、七类翻车现场 |
| **交房验收** | `skills/handover-inspection-advisor/` | 先验后签、公共部位先行、室内八大系统实测、面积误差 3%、问题清单七列、收房后 90 天保修 |
| **房产自媒体内容助手** | `skills/property-media-creator/` | 房产自媒体博主 |
| **业主端（卖房/出租决策）** | `skills/owner-*` | 房产持有人（业主） |

## 两条生产线

1. **`skills/` 直发技能**：独立 SKILL.md，发布 ClawHub 各自成技能（现有 30 个：calc-toolkit、buyer-first-home-advisor、developer-sales-advisor、project-feasibility-advisor、commercial-property-advisor、resale-transaction-sop、handover-inspection-advisor、broker 二手经纪线 3 个、业主端 2 个，与案场/策划线十六个）。
2. **`template/` 品牌生成骨架**：4 类角色原型（consumer-buy / developer-sales / brokerage-agent / channel-distributor）× 30 业务模块，`python3 render.py --config brand.yaml --out output/my-brand/` 一份配置生成品牌专属顾问技能，`install.sh` 装进任意 Agent。

## 使用顺序建议

测算场景按咨询流串用：**购房能力**（能买多少）→ **月供**（月供多少）→ **楼层折扣**（这套房折后价）→ **新房/二手成本**（交易税费）→ **提前还款**（买后规划）。

## 规则与数据

- 政策档位全部外置 `skills/calc-toolkit/rules/cities.yaml`（35 城，标注文号/口径/as_of），政策更新改配置不动代码
- 使用者可用 `--city` 选城市档、`--template` 挂自己的模板、`--set 键=值` 临时覆盖任意参数
- 所有档位默认为演示口径，正式经营使用前请按所在城市官方公告核对
