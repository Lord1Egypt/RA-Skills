# house-skills-kit 🏠

[English](README.en.md) | 中文

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776ab.svg)](https://www.python.org/)
[![Skills](https://img.shields.io/badge/skills-25-brightgreen.svg)](skills/)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](#已发布技能)
[![CI](https://github.com/danfeistar/house-skills-kit/actions/workflows/validate.yml/badge.svg)](https://github.com/danfeistar/house-skills-kit/actions/workflows/validate.yml)

**房产 AI 技能仓库 —— 按身份分 Skill，按需取用。**

为房地产行业的七类角色提供开箱即用的 AI 技能（Skill）：房开企业、经纪公司、渠道分销公司、购房者/业主、二手经纪人、一手销售人员、房产自媒体博主。每个身份场景对应一个独立 Skill，`skills/` 目录下各技能均含完整提示词与配套工具，可单独安装、单独发布。

> 🇨🇳 模板通用、零外部依赖（纯 Python 标准库）：不绑定任何平台与数据商，装进 Claude / 其他 Agent 均可。

> 不知道用哪个技能？先看 **[技能地图 docs/SKILL-MAP.md](docs/SKILL-MAP.md)**（按"我正在做什么"和"要交什么"反查）。

> **第一次用？先看 [docs/QUICKSTART.md](docs/QUICKSTART.md)** —— 5 分钟装好（Claude Code / Codex / 临时粘贴三种装法）+ 三个真实场景走一遍（二手经纪人配房、策划竞品报告、购房者选筹）+ 5 条使用纪律与 5 个常见坑。

## 已发布技能

### 🧮 calc-toolkit · 公共计算工具包（全身份通用）

一套覆盖房产交易核心测算场景的命令行工具，**全部身份共用**。

| 编号 | 工具 | 命令 | 说明 |
|---|---|---|---|
| ⑦-1 | 房贷月供 | `mortgage.py` | 商贷/公积金/组合贷 × 等额本息/本金，按城市利率档自动取数 |
| ⑦-2 | 二手房全成本 | `tax.py` | 契税/增值税/个税 + 中介/评估/担保等 6 项费用，买卖双方分账 |
| ⑦-3 | 提前还款 | `prepay.py` | 缩期 vs 减月供双方案对比，违约金/最低额提示，省息一目了然 |
| ⑦-5 | 购房能力 | `capacity.py` | 收入负债 → 可贷上限 → 可买总价，银行双线口径（月供收入比 × 首付成数），瓶颈诊断 |
| ⑦-6 | 一手房成本 | `newhome.py` | 契税/维修基金（按城市×物业类型）/首年物业/登记工本费，按功能分类出单 |
| ⑥ | 首套二套认定 | `status.py` | 商贷/公积金/契税三口径分判（认房不认贷），卖一买一，联动下游工具参数 |
| ⑦-15 | 楼层差价折扣 | `floor.py` | 楼层修正 × 营销折上折，防"先涨后折"真伪校验 |
| ⑦-16 | 公积金额度 | `fund.py` | 四限取最低：上限/房价成数/还贷能力/余额倍数×缴存时间系数，多子女/绿建/人才上浮，组合贷缺口提示 |
| ⑦-17 | 佣金提成试算 | `commission.py` | 二手中介费买卖分账+折扣；渠道阶梯双算法对账（全额跳档vs分段累进）；返佣+团队分佣 |
| ⑦-18 | 得房率换算 | `efficiency.py` | 建面↔套内↔公摊↔使用面积链，单价双向换算，双盘套内口径比价（防"建面便宜"幻觉） |
| ⑦-19 | 租金回报率 | `rent.py` | 租售比/毛净回报率/回收年限+五档坐标（存款/50城均值/回本线/价值线/以租养贷），目标反推 |

**35 城规则库**（北上广深 + 强二线 + 昆明等省会全覆盖）+ **四层规则引擎**：

```
全国默认档 → 城市档（如昆明高层维修基金90元/㎡）→ 区县档 → 我的模板档（使用者自建）
```

- 每个数字可追溯：输出带「参数来源」，规则档标注文号/口径（如"2024年契税16号公告：140㎡线"）
- 政策数据与代码分离：政策变了改 `rules/cities.yaml`，工具不用动
- 万能覆盖：任何参数均可 `--set 键=值` 即时改（如 `--set dti=0.55`）

**快速上手**（零安装，Python 3.8+ 直接跑）：

```bash
git clone https://github.com/danfeistar/house-skills-kit.git
cd house-skills-kit

python3 skills/calc-toolkit/mortgage.py --price 1500000 --downpay 30 --years 30 --city 昆明
python3 skills/calc-toolkit/capacity.py --income 8000,6000 --cash 400000 --debts 2000 --city 昆明
python3 skills/calc-toolkit/tax.py --price 1500000 --area 89 --city 昆明 --first 1 --held 6 --unique 1
python3 skills/calc-toolkit/prepay.py --loan 1000000 --rate 3.1 --years 30 --paid 24 --prepay 200000
```

## 🏠 购房客户线技能（C 端自住购房者）

| 技能 | 内容 | 适合谁 |
|---|---|---|
| [buyer-first-home-advisor 首购购房顾问](skills/buyer-first-home-advisor/) | 需求澄清七问（把"内需不明"问到清楚）+ 场景排除法 → 预算三线法（舒适线/上限线/极限线）→ 资格与首套三口径自查 → 片区五维筛选 + 楼盘百分制打分卡 → 一手五看法 + 二手 15 项验房清单 → 议价筹码与合同十条 → 贷款方案与提前还款 → 收房验房与税费 → 八类常见坑与红线 → 三句话收口（买/不买/再看） | 首次购房的个人与家庭、帮忙出主意的亲友、做 C 端咨询的经纪人 |

> 全流程数字走 [calc-toolkit](skills/calc-toolkit/)：可买总价、月供、首套认定、公积金额度、税费、得房率、提前还款，不口算；政策数字一律"按当地当期口径现查"，技能本身不提供任何城市的具体数字。

## 🏗 开发商顾问线（甲方营销决策）

| 技能 | 内容 | 适合谁 |
|---|---|---|
| [developer-sales-advisor 开发商销售顾问](skills/developer-sales-advisor/) | 12 项必取数据 + 五维体检（量/价/客/竞/队）一页纸诊断 → 三档结论（可接/需改造/劝退）→ 价格与优惠体系（价差表 + **三层优惠结构**：明折定锚 / 暗折转化 / 资源置换保表 + 释放四段节奏 + 破价防控五条）→ 渠道配比与费效（佣金结佣 + 四类风控）→ **去化卡壳五症处方**（来访不足/转化不足/结构错配/价格抗性/竞品挤压，每症带指标阈值、验证周期与止损）→ 预算 5-3-2 与止损 → 甲方周报与经营预警（六指标 + 三档建议 + 预警红线） | 开发商营销负责人、代理公司项目负责人、销售顾问、投前研判岗 |
| [project-feasibility-advisor 开发项目投前决策](skills/project-feasibility-advisor/) | 拿地三指标（净利率 / **双口径 IRR** / 地货比）→ 定位三问（卖给谁 / 总价段能否承接 / 和谁抢）+ 配比三约束 → 成本六块与**最常漏的九项** → 售价三源锚定与去化年限反推 → 敏感性 + **决策阈值表**（建议参与/有条件/不建议）→ 可研八章结构 + **六种注水手法对照** → 城市进入四指标与三类风险。配套 `feasibility.py`（盈亏平衡售价 + 敏感性表） | 投拓/投资发展、项目总、代建与咨询顾问、投前研判岗 |

> 这一线只做决策层的判断与取舍；执行层动作（接待/判客/话术/逼定/开盘）见下方案场销售线，测算一律走 [calc-toolkit](skills/calc-toolkit/)。

## 🔑 二手经纪线技能（经纪公司/二手房门店）

| 技能 | 内容 | 适合谁 |
|---|---|---|
| [broker-listing-sop 二手房源开发与委托 SOP](skills/broker-listing-sop/) | 六渠道房源开发与试水盘三筛 → 业主动因三问 + 价格锚点溯源 + 校准四步（市场/成本/时间/挂高代价）→ 三段式报价建议 → 委托三类对比与**协议七要素**（独家必带对价）→ 实勘十二项核验 + 拍照标准 + 房源卡字段 → 四档分级维护与 30/60/90 天触发 → 跳单信号 + 证据链四件套 + 佣金主张流程 | 二手房经纪人、门店经理、经纪公司运营（真房源合规） |
| [broker-client-deal-sop 二手房客户匹配与成交 SOP](skills/broker-client-deal-sop/) | 需求澄清七问 + 首付四笔漏算 + 资格与贷款预判（只预判不承诺）→ 三维匹配打分（硬约束/软需求/风险扣分，每套必带"代价"）→ 一场三套带看动线与二选一话术 + 不表态四因排查 → 买卖双线议价 + 让步阶梯 + 僵局三破法 → 七步交易流程（定金/居间/网签/资金监管/贷款/过户）与**交房五交接** → **九类风险核验清单** → 佣金口径四件事与跳单应对 | 二手房经纪人、门店经理、交易专员 |
| [broker-lease-sop 租赁经纪作业标准](skills/broker-lease-sop/) | 委托六项核验 + 委托类型三选一 + 委托条款七项 → 三源锚点报价（挂牌-成交价差、空置换算）→ 合法筛选边界（能问什么/不能问什么）+ 收入租金比 + 四种骗局识别 → **十项必备条款** + 押金与首日现金结构（佣金走 `commission.py --scene lease`）→ 交房五件套 → 报修三档/续租/退租四步 → 欠租四步与四类高风险情形 | 二手房门店租赁经纪人、长租公寓运营、兼做租赁的自媒体 |

> 这一线是二手房执业口径（双边议价、产权核验、真房源合规）；面向购房者自己的决策流程见 [buyer-first-home-advisor](skills/buyer-first-home-advisor/)，测算走 [calc-toolkit](skills/calc-toolkit/)。

## 🏠 业主端技能（房产持有人）

| 技能 | 覆盖内容 | 目标读者 |
|---|---|---|
| [owner-sell-home-advisor 卖房业主决策助手](skills/owner-sell-home-advisor/) | 卖前决策（该不该卖/置换顺序/持有成本）→ 定价四步（三源锚点 + **净得价倒算** + 挂高的真实代价 + 降价节奏）→ 可看性工程（清空/低成本维修/拍照红线/带看配合）→ 选中介六维比选与**委托条款七项核验** → 议价接单五问与定金违约测算 → 交易流程与**五类高频纠纷预防** → 继承/共有/离婚析产/抵押查封/学位占用/带租约六类特殊情形 | 二手房业主、置换业主、代家人处置房产的成年子女 |
| [owner-rental-advisor 出租业主决策助手](skills/owner-rental-advisor/) | 该租/该卖/空置三选一（毛净回报 + 空置成本 + **打平涨幅**）→ 租金定价与空置算术 → 房屋准备与合规（隔断群租红线/家具投入回报）→ **合法筛选边界**与十项必备条款 → 履约与纠纷（维修划分/退租四步留痕/欠租处理四步/上门权边界）→ 自管 vs 托管比选 → 合租短租/学位落户/转租等特殊情形 | 出租业主（自管）、考虑托管的业主、代管家人房产者 |

## 🏬 商业地产业务线（商铺/写字楼/公寓）

| 技能 | 内容 | 适合谁 |
|---|---|---|
| [commercial-property-advisor 商业物业投资与租赁决策](skills/commercial-property-advisor/) | 商业与住宅的六个根本差别 → 商铺位置分级 + **五个硬件硬指标**（能否餐饮/面宽进深/层高/独立水电/门前条件）+ 客流三次实地法 → 写字楼三看与公寓四个坑 → **收益法估值**（NOI ÷ cap）与**隐含 cap 反查**（谈判直接用）→ 租约十项条款 + 租户质量四问 → 买入三门槛与退出三变量 → **七类高风险陷阱**（返租包租/产权式商铺/高 cap 诱饵/主力店依赖/规划憧憬/商改住包装/税费陷阱）。配套 `commercial.py`（NOI / 收益法 / 隐含 cap / 持有期 IRR） | 商业地产经纪人、投资客顾问、商铺自用客户、房产自媒体 |

> 商业买的是现金流，住宅买的是预期。测算走 `commercial.py`（NOI/cap 口径），别用住宅的租售比与税费经验。

## 🤝 交易与交付线（成交之后：过户与收房）

| 技能 | 内容 | 适合谁 |
|---|---|---|
| [resale-transaction-sop 二手房交易全流程与风险](skills/resale-transaction-sop/) | 12 节点交易时间轴与三方责任边界 → **查档查六项**（权属/抵押/查封与限制/共有/租赁/限售）→ 三个"金"的区别与定金罚则 → **合同必写 12 条**（含贷款不批三选一）→ 网签与资金监管 → 贷款审批五个不通过原因 → 税费买卖分列与过户顺序 → 抵押注销/赎楼三条路 → 交房六件事与**尾款保留条款** → **七类翻车现场**（查封/共有人缺席/租客不搬/户口不迁/面积误差/卖方毁约/批贷失败）。配套 `tax.py` `deposit.py` `loanterm.py` `status.py` `area_error.py` | 二手经纪人、门店店长、交易管家、自助交易的买卖双方 |
| [handover-inspection-advisor 交房验收](skills/handover-inspection-advisor/) | 验收三条底线（先验后签/书面留痕/整改闭环）→ 到访资料与**200 元工具清单** → 公共部位六处先行 → **室内八大系统实测**（给排水/电气/防水闭水/门窗气密/空鼓/层高开间/烟道通风/附属）→ 面积误差 3% 红线与赠送面积处理 → **问题清单七列模板**与拖延时的三级升级 → 收房后 90 天保修主张三要素。配套 `area_error.py` `efficiency.py` `newhome.py` | 购房者本人、置业顾问与客服、第三方验房师、房产自媒体 |

## 🏢 案场销售线技能（一手销售/案场团队）

| 技能 | 内容 | 适合谁 |
|---|---|---|
| [sales-talk-library 案场话术库](skills/sales-talk-library/) | 地段/配套/户型/竞品/品牌五域 24 个话术块：标准说辞 + 分客群变通 + 翻车警示，合规红线内嵌 | 置业顾问、销售经理、案场培训 |
| [sales-objection-handling 客户异议处理](skills/sales-objection-handling/) | "太贵了/再看看/怕烂尾/会不会降价"四大高频异议：顾虑分支拆解→应对话术→禁语清单，附 6 条二级异议 | 置业顾问、销售经理 |
| [sales-closing-sop 算价与逼定 SOP](skills/sales-closing-sop/) | 算价五要素→让步梯度→购买信号判读→五级逼定→成交收口，含红白脸与审批链团队配合 | 置业顾问、销售主管/经理 |
| [sales-reception-sop 接待与需求挖掘 SOP](skills/sales-reception-sop/) | 首访动线（品牌→区域→项目→户型）+ 七维需求提问树 + 客户画像复述 + 带看匹配与交接 | 置业顾问、销售主管、案场负责人 |
| [sales-lead-grading 判客与跟进 SOP](skills/sales-lead-grading/) | ABC判客分级四维标准 + 分级跟进节奏 + 掉客三层挽回 + 复判升级与归属仲裁 | 置业顾问、销售主管、案场负责人 |
| [sales-mortgage-sop 按揭问题应对 SOP](skills/sales-mortgage-sop/) | 贷款口径统一 + 资质预判分流 + 六类高频问题（流水/征信/首付缺口/首付来源/收入形态/公积金）路径与话术 + 批贷进度跟进 + 合规红线汇总 | 置业顾问、按揭专员、销售主管 |
| [sales-opening-sop 开盘执行 SOP](skills/sales-opening-sop/) | 盘前客户梳理与预登记 + 认筹转认购 + 开盘日七环节选房动线 + 选房规则口径表 + 五类应急预案 + 盘后转化与复盘 | 置业顾问、案场负责人、开盘执行团队 |
| [presale-marketing-sop 蓄客期营销动作清单](skills/presale-marketing-sop/) | 节点倒排四阶段节奏 + 暖场/拓客/圈层/认筹预热动作库 + 自媒体蓄客专节（项目号定位/内容日历/线索承接闭环）+ 四级漏斗与费效复盘 + 合规红线 | 策划、营销负责人、自媒体运营、拓客团队 |
| [competitive-intel-sop 竞品踩盘与市场监控](skills/competitive-intel-sop/) | 竞品A/B/C分级与踩盘频次 + 现场六模块采集清单（价值主张/展示面/销售力/价格/销控/服务）+ 百分制打分表与竞品预判 + 供应成交去化价格四指标周监控（三源交叉）+ 月度竞品报告模板 + 反踩盘纪律与合规红线 | 策划、营销负责人、市调岗、置业顾问 |
| [activity-organization-sop 营销活动组织 SOP](skills/activity-organization-sop/) | 单场活动目标定义 + 活动选型矩阵 + 一页简报模板 + 预算审批 + 执行清单 + 现场分工动线 + 线索承接首触 + 72小时复盘闭环 | 策划、营销负责人、案场负责人 |
| [marketing-materials-sop 营销物料与示范区优化 SOP](skills/marketing-materials-sop/) | 物料任务分类 + 一页设计简报 + 信息与合规审核 + 示范区四层巡检 + 改进台账 + 版本管理 + 客户反馈复盘 | 策划、示范区负责人、置业顾问 |
| [engineering-progress-broadcast-sop 工程进度与品质播报 SOP](skills/engineering-progress-broadcast-sop/) | 工程资料采集 + 节点对照 + 品质工艺表达 + 延期沟通 + 敏感问题升级 + 发布检查 + 复盘归档 | 工程部、策划、品牌、案场客服 |
| [pricing-incentive-release-sop 价格策略与优惠释放 SOP](skills/pricing-incentive-release-sop/) | 价格事实核验 + 房源/客户分层 + 优惠梯度 + 审批变更 + 案场执行 + 台账复盘 + 合规红线 | 营销负责人、案场负责人、置业顾问 |
| [channel-collaboration-sop 渠道协同与分销管理 SOP](skills/channel-collaboration-sop/) | 渠道准入分层 + 政策培训 + 报备查重 + 带访交接 + 判客仲裁 + 佣金对账 + 渠道复盘 | 渠道负责人、项目营销、案场、财务 |
| [channel-management-advisor 渠道管理与分销决策助手](skills/channel-management-advisor/) | **渠道决策层**：来访结构倒推与配比 → 渠道依赖度红线 → 佣金点位四步与**跳点双算法**（全额跳档 vs 分段累进，工具双算）→ 快佣/阶梯现金奖/费效上限 → 准入 A/B/C 分级与**合同八条款** → 三段归属与撞单仲裁 → 六指标产能诊断与四类健康画像 → 飞单信号与处罚梯度 → 月度渠道会与年度框架谈判 | 项目营销负责人、渠道总监/经理、财务对账、区域渠道统筹 |
| [property-media-creator 房产自媒体博主内容助手](skills/property-media-creator/) | **自媒体线的完整内容生产链**：三圈定位法与五类人设 → 四源选题库（客户问答/搜索词/评论区/看台现场）与选题卡 → 黄金 3 秒八种钩子与分型脚本（10 秒速讯/15 秒深度/探盘/政策）→ 机位·字幕硬标准（零错字/关键词置上 1/3/负面词清单）·封面三要素 A/B → 五条红线与限流自查整改 → 评论区三板斧与私信六句转化 → 四指标复盘与止损规则 → 四类变现与三处披露义务 | 经纪人自营号、门店机构号、探盘测评博主、开发商营销号 |
| [customer-advocacy-referral-sop 客户口碑与老带新运营 SOP](skills/customer-advocacy-referral-sop/) | 服务反馈分层 + 口碑内容授权 + 推荐触发 + 线索登记 + 权益兑现 + 客诉隔离 + 复盘 | 客户关系、营销、案场、内容 |
| [launch-integrated-campaign-sop 节点开盘整合营销 SOP](skills/launch-integrated-campaign-sop/) | 开盘战役简报 + 九格协同 + 节点倒排 + 资产包 + 整合承接 + 全员演练 + 开盘衔接 + 盘后复盘 | 营销负责人、策划 |
| `marketing-review` 月度营销复盘与经营看板模块 | `template/modules/marketing-review.md.tmpl` | 策划/营销：口径锁定、漏斗与房源结构、来源费效、异常升级与行动台账 |
| `media-lead-growth` 媒介投放与线索增长模块 | `template/modules/media-lead-growth.md.tmpl` | 策划/营销：付费投放、预算止损、素材测试、线索归因、质量优化与承接交接 |

> 数字类话术（月供/得房率/楼间距等）与 [calc-toolkit](skills/calc-toolkit/) 联动计算，不口算。

## 技能路线图（按身份扩容）

| 身份 | Skill | 状态 |
|---|---|---|
| 全身份通用 | `calc-toolkit` 公共计算工具包 | ✅ 已发布（19 件工具收官） |
| 一手销售/案场 | `sales-talk-library` / `sales-objection-handling` / `sales-closing-sop` / `sales-reception-sop` / `sales-lead-grading` 案场销售线五技能 | ✅ 已发布（L1 主干 7/7 完成） |
| 购房客户 | `buyer-first-home-advisor` 首购购房顾问（需求澄清/预算三线/选筹打分/看房验真/议价签约/收房税费） | ✅ 已发布 |
| 房开案场 | `developer-sales-advisor` 开发商销售顾问（甲方决策线：研判/价格/渠道/处方/预算/汇报） | ✅ 已发布 |
| 一手销售 | 置业顾问跟客助手（含判客/话术） | ✅ 已由 `sales-reception-sop` + `sales-lead-grading` + `sales-talk-library` 覆盖 |
| 二手经纪人 | `broker-listing-sop` + `broker-client-deal-sop` + `broker-lease-sop` 二手房经纪线（房源开发委托 / 客户匹配成交 / 租赁作业） | ✅ 已发布（房源端+客户端+租赁端 3 件） |
| 渠道分销 | `channel-management-advisor` 渠道管理与分销决策助手（决策层）+ `channel-collaboration-sop`（执行层） | ✅ 已发布 |
| 房产自媒体 | `property-media-creator` 内容创作助手 | ✅ 已发布 |
| 业主端 | `owner-sell-home-advisor` 卖房业主决策 + `owner-rental-advisor` 出租业主决策 | ✅ 已发布（卖/租 2 件） |

## 仓库结构

```
skills/            # 25 个独立技能，每个自带 SKILL.md（+ README.md / 正文 / 可选工具）
  calc-toolkit/    #   公共计算工具包 + 35 城规则库（rules/cities.yaml）
  buyer-*/         #   购房客户（C 端）技能
  sales-*/         #   案场销售线技能
  broker-*/        #   二手经纪线技能（房源端/客户端）
template/
  archetypes/      # 4 类角色原型（购房者 / 房开销售 / 经纪经纪人 / 渠道分销）
  modules/         # 31 个业务模块，按需拼装
examples/          # 可直接跑的示例配置（昆明端到端示例、开发商示例）
adapters/mock/     # 模拟数据适配器，接真实房源源时替换
render.py          # 由品牌配置 + 模板渲染出专属技能
mini_yaml.py       # 零依赖 YAML 子集解析器（没装 PyYAML 也能跑 render.py）
tools/             # 仓库自检脚本（结构与文档校验）
```

## 自检与贡献

```bash
python3 tools/validate_skills.py     # 结构与文档自检：技能目录/frontmatter/链接/疑似密钥/编译
python3 tools/validate_skills.py --spec   # 规范覆盖率自检：12 段必备结构（六段新增段）逐技能核对
python3 tools/check_refs.py           # 引用完整性：计算器脚本 / 兄弟技能目录 / Part 编号是否真实存在
python3 tools/check_commands.py           # 文档里的计算器命令逐条实跑
bash tools/install_skills.sh --list        # 一键安装到你的 agent 技能目录（--target 指定位置）

python3 tools/check_links.py              # Markdown 相对链接是否还有效（改名后的死链）
python3 -m unittest discover -s tests -v   # 计算器回归测试（单位口径/公式自洽/越界拦截）
```

当前状态：**30 个技能，六段覆盖 30/30**。新增技能请按 [docs/SKILL-AUTHORING-SPEC.md](docs/SKILL-AUTHORING-SPEC.md) 写，`--spec` 会指出缺哪段。

CI（GitHub Actions）在每次 push 与 PR 上跑：技能自检 → 计算器冒烟 → 每个工具 `--help` → 零依赖渲染 → 渲染可复现性。

欢迎 Issue 与 PR，写之前先看 [CONTRIBUTING.md](CONTRIBUTING.md)；版本变更见 [CHANGELOG.md](CHANGELOG.md)。

## 两条生产线

1. **`skills/` 直发技能**：每个子目录独立 SKILL.md，发布到 ClawHub 各自成技能，可独立安装。
2. **`template/` 品牌生成骨架**：4 类角色原型（购房者/房开销售/经纪经纪人/渠道分销）× 31 业务模块，一份品牌配置即可生成专属顾问技能：

```bash
python3 render.py --config examples/kunming/kunming.buy.yaml --out output/my-brand/
```

## 分发渠道

| 平台 | 链接 |
|---|---|
| GitHub 主库 | [github.com/danfeistar/house-skills-kit](https://github.com/danfeistar/house-skills-kit) |
| Gitee 镜像 | [gitee.com/danfeistar/house-skills-kit](https://gitee.com/danfeistar/house-skills-kit) |
| AtomGit 镜像 | [atomgit.com/danfeistar/house-skills-kit](https://atomgit.com/danfeistar/house-skills-kit) |
| ClawHub 技能市场 | [clawhub.ai/skills/house-skills-kit](https://clawhub.ai/skills/house-skills-kit) |

## 👤 作者

**老何** — 地产行业从业 17 年，历任多家房企云南营销负责人，长期深耕云南及昆明市场，早期 AI 使用者与运用者。现全力建设「房产 AI 平台」（房企端 + 经纪公司端 + 销售人员端 + 买房客户端）。

**为什么做这个仓库**：作者在国内外公开渠道（GitHub / ClawHub / 各大 AI 应用市场）均未找到专注中国房地产的 AI Skill 工具库——市面上的 Skill 生态几乎空白于这个年交易额十万亿级的行业。既然没有，就来做**最早、最专业的中文房产 AI Skill 与工具库**：把一线地产人的业务知识，做成 AI 真正能用的技能。

**本仓库的差异化**：这里的业务模块（判客规则 / 佣金政策 / 案场话术 / 验房清单 / 城市税费档…）全部来自一线业务实践和企业规范化工作场景，不是工程师想象出来的 prompt。AI 懂技术，我们懂房产——两者结合才是行业真正能用的 AI 工作流。

> 💡 **免费开源，长期维护**。如果它对你的工作有帮助，欢迎 Star / Issue / 转发——每一次使用和反馈都是对"房产 AI 开源"路线的支持。
>
> 🤝 **业务合作**：需要为你的房企 / 经纪公司 / 销售团队定制 AI 工具与 AI 工作流？欢迎通过 [GitHub 主页](https://github.com/danfeistar) 联系作者——一线地产 17 年 × AI 工程化落地，帮你把 AI 真正用进业务。

## License

Apache-2.0
