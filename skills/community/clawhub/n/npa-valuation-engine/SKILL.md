---
name: npa-valuation-engine
display_name: 法拍不良资产估值引擎·折价真伪拆解+三情景IRR+全栈处置库
display_name_en: Foreclosure & NPL Valuation Engine - Discount, IRR Playbook
description: "法拍与不良资产全栈估值定价引擎：折价口径对齐、折价可修复性打分、三情景 IRR/MOIC、投标上限反推，并生成可审计的 xlsx 估值模型。触发词：法拍、不良资产、NPL、资产包、投标上限、折价率、IRR、MOIC、处置、尽调、债权转让、AMC、回收率、抵押物、个贷不良、对公不良。"
description_zh: "法拍最坑的不是买贵，是以为捡漏、其实在接盘。法院评估价不等于市场价，折价率还有两种口径，同一句话能差近 3 倍；折扣里只有能靠自己的动作主动修复的那部分，才是真收益。这套引擎把纸面折扣还原成真实安全边际：折价真伪拆解 + 三情景 IRR/MOIC + 投标上限反推，一步出可审计的 xlsx 估值模型。"
description_en: "A valuation and pricing engine for court auctions and non-performing loan portfolios. The costly mistake in distressed buying is not bidding too high — it is believing you found a bargain while quietly absorbing someone else's problem. Three questions get forced before any money moves: which discount convention you are quoting, whether each slice of the discount can actually be repaired by your own action or is simply the market pricing in illiquidity, and whether the deal still clears your hurdle rate on a conservative exit. The engine generates an auditable Excel model with three cash-flow scenarios, IRR and MOIC side by side, sensitivity tables and a reverse-solved bid ceiling, verifies every formula independently before delivery, and ranks an entire deal pipeline by risk-adjusted return. It ships with a due-diligence checklist, thirty disposal techniques, regional pricing benchmarks and a four-cycle market history."
category: investment-finance
version: 3.0.1
author: 九品锦锂e
license: MIT
---

# 法拍 / NPA 估值定价引擎（全栈版）

把「纸面折扣」翻译成真金白银的 IRR。

任何法拍标的、不良资产包、困境资产，填一组假设即出：三情景 IRR + MOIC 双指标、敏感性矩阵、折价可修复性打分、投标上限反推；另外配一套从形成机制到处置退出的全栈知识库兜底——不靠感觉出价。

**输入**：标的基本信息、债务人与抵押物情况、所在区域
**输出**：估值区间与建议出价上限、处置路径建议、尽调重点清单、可审计的 xlsx 估值模型

---

## 一、什么时候用

- 法拍房 / 法拍股权 / 不良债权包摆在面前，要回答「要不要买、出多少」
- 需要把折价率换算成 IRR / MOIC，给决策层一个能看懂的数
- 客户或合投方问不良资产投资逻辑、投标上限、处置回报
- 手上有一批标的要排序，按风险调整后回报挑出该先做的那几个
- 要出一份尽调清单，查权利瑕疵、抵押物可控性、债务人可执行财产
- 需要系统搞清对公不良与个贷不良的不同打法

---

## 二、三条铁律（做之前先背下来）

### 铁律一：先对口径，否则全错

| 口径 | 定义 | 谁在用 |
|---|---|---|
| **折扣率**（本引擎采用） | 成交价 ÷ 评估价 | 千际投行、中指研究院 |
| 折价幅度 | 1 − 成交价 ÷ 评估价 | 克而瑞 |

两者互为 1 的补数。同一句「折价率 74.1%」，两种口径下含义相差近 3 倍。

**第二层陷阱（更致命）**：评估价 ≠ 市场价。法院评估价普遍滞后且偏高。「相对评估价折 26%」不等于「相对市场价便宜 26%」。

**必须另算【真实折价率 = 成交价 ÷ 对标市场价】**，这才是真安全边际。模型里单独做了这一列。

### 铁律二：只有可主动修复的折价才是真收益

| 要素 | 可修复性 | 修复抓手 |
|---|---|---|
| 信息折价 | 高 ★★★★★ | 尽调补齐产权 / 占用 / 欠费 / 税费 |
| 时间折价 | 中 ★★★☆☆ | 垫资提速、预清场、缩短过户 |
| 流动性折价 | 低 ★☆☆☆☆ | 只能选城市、选地段——**低分即风险** |
| 风险折价 | 中高 ★★★★☆ | 交易结构与条款对冲 |

用打分卡算「可修复折价占比」：**> 50% 才值得做，< 30% 直接放弃**。

流动性折价几乎不可修复 —— 所以远郊房、老破小、低能级城市的商业资产，折得再深也不该碰：那不是便宜，那是市场在给「卖不掉」定价。

### 铁律三：三情景 + IRR/MOIC 双指标，决策看保守情景

- 三层结构：情景（保守 / 基准 / 乐观）→ 现金流（回款节奏 + 税费 / 诉讼 / 运营）→ 门槛（叠加资金成本与机会成本）
- **决策看保守情景，乐观情景只用来估上行空间**
- IRR 看效率、MOIC 看倍数；**两者背离时（倍数高但 IRR 低）＝ 钱压得久**，这是法拍最常见的死法
- 反推**投标上限**：给定门槛 IRR，反解最高可出价。现价低于上限才有安全垫

---

## 三、环境依赖

```bash
pip install openpyxl numpy_financial
# 国内网络加镜像：
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple openpyxl numpy_financial
```

| 依赖 | 用途 | 是否必需 |
|---|---|---|
| `openpyxl` | 生成 xlsx 估值模型 | 必需 |
| `numpy_financial` | IRR / NPV 独立自算比对 | 必需 |
| LibreOffice（`soffice`） | `verify_model.py` 换引擎重算比对 | 可选，未安装则该脚本进入降级模式（退出码 2），其余功能不受影响 |

`bid-quick-calc.py`、`disposal-decision-model.py`、`regional-valuation.py` 只用标准库，无需安装任何包。

---

## 四、工具链怎么跑

六个脚本，全部只用命令行参数，不依赖交互输入（`bid-quick-calc.py` 不传参数时才进入交互模式）。

### 1. 生成估值模型 — `scripts/build_model.py`

```bash
# 先用内置示例试跑，确认环境没问题
python scripts/build_model.py --demo --out model.xlsx

# 正式标的：拷模板填数后跑
python scripts/build_model.py --config deal.json --out model.xlsx

# 回显合并默认值之后的完整配置，用于检查假设有没有填错
python scripts/build_model.py --config deal.json --print-config
```

产出 5 张表：**使用说明 / 输入假设 / 三情景现金流 / 敏感性分析 / 折价打分卡**。

- 输入模板：`templates/deal_template.json`，只填已知字段，缺的走默认值
- `asset_type` 支持 **住宅 / 商办 / 工业 / 股权**，自动切换四要素折价的默认权重
- 金额单位＝元，比率用小数（`0.15` = 15%）

### 2. 独立验证 — `scripts/verify_model.py`

```bash
python scripts/verify_model.py --model model.xlsx          # 人类可读
python scripts/verify_model.py --model model.xlsx --json   # 机器可读
python scripts/verify_model.py --model model.xlsx --allow-degraded   # 缺 LibreOffice 时也返回 0
```

做五件事：LibreOffice 重算 → Python（`numpy_financial`）独立自算比对，偏差应 < 1e-12；反推投标上限；全表错误单元格扫描；公式存在性检查。

**退出码**：`0` = 完整双验通过；`1` = 验证不通过（模型有偏差或结构缺失）；`2` = 降级通过——本机没装 LibreOffice，重算与缓存值比对无法执行，但 Python 独立自算与公式存在性检查已过，脚本会明确打印「降级模式」并给出 Python 侧 IRR/MOIC/NPV 供核对。**这不是模型不合格，是环境缺件**；装上 LibreOffice 重跑即得完整结论。

**未通过验证（退出码 1）的模型不得对外交付。**

### 3. 批量筛选 — `scripts/screen_deals.py`

```bash
# 直接用样例跑通
python scripts/screen_deals.py --deals templates/deals_sample.json

# 只看保守情景 IRR ≥ 15% 的标的，并导出结果
python scripts/screen_deals.py --deals deals.json --min-conservative-irr 0.15 --out-xlsx result.xlsx

# 机器可读输出，便于接进别的流程
python scripts/screen_deals.py --deals deals.json --json
```

按保守情景 IRR 降序排名，输出三情景 IRR / MOIC、投标上限、价差空间、可修复占比、判定结论。多标的输入格式见 `templates/deals_sample.json`。

### 4. 投标速算 — `scripts/bid-quick-calc.py`

```bash
python scripts/bid-quick-calc.py                                     # 交互模式
python scripts/bid-quick-calc.py --amount 120000000 --recovery 0.15 --discount 0.12 --term 2 --cost 0.05
python scripts/bid-quick-calc.py --preset 个贷包 --amount 120000000
```

预设类型（`--preset`）：`个贷包` / `对公抵押` / `一线住宅抵押`（还有更多内置类型，不传 `--preset` 时脚本会列出）。竞价前 30 秒出一档可出价区间，用于银登中心、司法拍卖平台的现场报价。

### 5. 处置决策 — `scripts/disposal-decision-model.py`

```bash
python scripts/disposal-decision-model.py
```

五维评分（资产质量 / 法律状态 / 处置效率 / 回收确定性 / 成本效益）→ 加权总分与评级 → 推荐处置策略 TOP 3 → 方案对比（回收率 × 周期 × 成本 → 毛利与 IRR）→ 敏感性分析。

脚本内的资产字典就是输入模板，改字段即可换成自己的案子。

### 6. 区域估值 — `scripts/regional-valuation.py`

```bash
# 单点：某城市能级下，1 亿公允价值 / 8000 万不良本金的估值
python scripts/regional-valuation.py --fair-value 100000000 --bad-debt 80000000 --tier 一线

# 横向对比五个城市能级，看同一笔资产放在不同城市的估值差
python scripts/regional-valuation.py --fair-value 100000000 --bad-debt 80000000 --compare

# 指定资产类型（住宅/商办/工业用地/产业园/商业综合/酒店/制造业贷款/个贷/城投债/股权）
python scripts/regional-valuation.py --fair-value 50000000 --bad-debt 30000000 --tier 二线 --asset-type 住宅

# 无参数运行 = 演示模式
python scripts/regional-valuation.py
```

`--tier` 只接受 **一线 / 新一线 / 二线 / 三线 / 四线**。`--batch` 目前仍走演示模式。

---

## 五、标准流程

1. 拿到标的信息 → 拷 `templates/deal_template.json` 填数（评估价、起拍价、预估成交价、**对标市场价**）
2. 跑 `build_model.py` 生成模型 → 看「真实折价率」是否与城市锚偏离过大
3. 对标城市折价率锚（见 `@references/market-anchors.md`）校核退出售价系数与处置周期
4. 跑 `verify_model.py` 双验 → 未通过不交付
5. 读结论：保守情景 IRR 达标吗？可修复折价占比 > 50% 吗？投标上限与现价之间还有多少空间？
6. 一批标的用 `screen_deals.py` 排序，先做风险调整后回报最高的那个

---

## 六、核心公式（可审计）

- 资产处置价值 ＝ 可实现市场价值 − 交易与交付成本 − 风险损失 − 资金时间成本
- 年化 IRR ＝ (1 + 季度IRR) ^ 4 − 1（现金流按季度排布）
- MOIC ＝ 总回收 ÷ 总投入
- 投标上限：令保守情景 IRR ＝ 门槛 IRR，反解买入价
- 可修复折价占比 ＝ Σ(可修复性评分 × 折价权重) ÷ Σ(评分满值 × 折价权重)

---

## 七、知识库模块索引

按主题分组，用到哪块读哪块。

### 估值定价核心（先读这组）

| 文件 | 什么时候读 |
|---|---|
| `@references/valuation-methods.md` | 选估值方法：交易案例比较法 / 专家判断法 / 现金流折现分别适用什么场景 |
| `@references/asset-valuation.md` | 三重折价模型的完整推导，折价拆解的底层逻辑 |
| `@references/valuation-case-studies.md` | 要有可比案例支撑估值结论时 |
| `@references/valuation-params-sensitivity.md` | 参数取值区间怎么定、敏感性怎么设 |
| `@references/market-anchors.md` | 每次建模都要：用城市折价率锚校核假设是否离谱 |
| `@references/recovery-modeling.md` | 回收率怎么量化建模、不同资产类型的回收分布 |

### 投标与谈判

| 文件 | 什么时候读 |
|---|---|
| `@references/bidding-valuation-strategy.md` | 竞价博弈下的报价策略、动态报价节奏 |
| `@references/valuation-negotiation.md` | 价格谈判阶段的话术与让步结构 |

### 处置路径

| 文件 | 什么时候读 |
|---|---|
| `@references/disposal-strategies.md` | 处置策略总览与选择逻辑 |
| `@references/disposal-techniques-30.md` | 30 种处置技术的适用场景、周期、回收差异 |
| `@references/classification-disposal-mapping.md` | 已知资产分类，反查该走哪条处置路径 |
| `@references/npl-lifecycle-framework.md` | 从收购到退出的全生命周期视角，做长周期规划时读 |

### 尽调

| 文件 | 什么时候读 |
|---|---|
| `@references/due-diligence.md` | 尽调要点与红线 |
| `@references/due-diligence-workflow.md` | 尽调实操七步法，按步骤执行 |
| `@references/legal-framework-l1.md` | 查法律监管框架与权利顺位问题时 |
| `templates/valuation-due-diligence-checklist.md` | 直接当尽调作业清单用，打勾交付 |

### 基础与分类

| 文件 | 什么时候读 |
|---|---|
| `@references/fundamentals-classification.md` | 基础概念、按来源 / 按形态分类的口径 |
| `@references/formation-mechanism.md` | 不良是怎么形成的，判断资产包成因时读 |
| `@references/knowledge-cards-l1.md` | 快速过一遍核心概念，适合给新手 / 客户做科普底稿 |
| `@references/knowledge-cards-l5.md` | 个贷不良批转市场的前沿速查 |

### 市场与主体

| 文件 | 什么时候读 |
|---|---|
| `@references/trading-market-pricing.md` | 交易市场结构与定价机制，含区域差异 |
| `@references/market-participants.md` | 六类参与主体（AMC / 银行 / 服务商 / 投资人等）的诉求差异 |
| `@references/npl-ecosystem-2026-map.md` | 2026 年生态图谱，看自己在链条里的位置 |
| `@references/transaction-workflow.md` | 从出表到交割的交易实务全流程 |

### 周期史与案例复盘

| 文件 | 什么时候读 |
|---|---|
| `@references/npl-four-cycles-history.md` | 1999 年至今四轮周期的历史沿革，判断当前处在哪一阶段 |
| `@references/four-cycle-case-studies.md` | 四轮周期的标杆案例速查，给结论找历史参照 |

### 科技与个贷批量

| 文件 | 什么时候读 |
|---|---|
| `@references/ai-retail-npl-tech.md` | 个贷不良批量处置的科技手段与成本结构 |
| `@references/tech-reshaping-market.md` | 科技怎么改变市场底层逻辑，判断趋势时读 |

---

## 八、尽调清单（只查三件事）

尽调千头万绪，但这三件没查清，其他都是细节：

1. **权利是否干净** —— 抵押登记是否有效、顺位、是否存在优先权冲突（担保债权 / 职工债权 / 税款债权 / 共益债务）、有无未决诉讼与查封轮候
2. **抵押物是否真实可控** —— 权属完整、实际占用状态、腾退难度、户口滞留、欠费（物业 / 水电 / 税费）、有无租约绑定与用途限制
3. **债务人有无可执行财产** —— 除抵押物外的可执行财产线索、对外投资与关联交易、隐性负债

完整清单直接打开 `templates/valuation-due-diligence-checklist.md` 逐项打勾；估值方案成稿模板见 `templates/valuation-template.md`。

**税费是最大暗坑**：原产权人为公司可能触发土地增值税、企业所得税；「所有税费由买受人承担」这一条可以让实际成本远超成交价——建模时务必单独列项。

---

## 九、踩过的坑（写脚本时已经处理，改脚本前先看）

- **公式行号必须动态捕获**：openpyxl 生成多表模型时硬编码行号，插一行就全表静默错位（openpyxl 不求值、不报错）
- **文本以 `=` 开头**会被 Excel / LibreOffice 当公式解析 → `Err:501`；说明性文字用全角 `＝`
- **LibreOffice 对 OOXML 默认不重算**（`OOXMLRecalcMode=never`），转换后公式缓存值恒为 0，会误判成「模型算不出数」；解法：先给工作簿打 `fullCalcOnLoad` 标志再转
- **`soffice` 转换时源文件与输出目录不能同名同目录**，否则静默失败
- Excel `IRR()` 返回的是**季度** IRR，年化须 `(1+q)^4-1`
- 打印 / 转 PDF 要设 `landscape + fitToWidth=1`，否则长文本列断页

---

## 十、边界与风险

- **模型不产生数据**：三情景假设的质量取决于尽调深度，垃圾进垃圾出
- **税费与腾退是回款归零级风险**：腾退失败、户口滞留属于把回收打到接近零的情形，模型用情景系数覆盖，实际操作里必须单独设红线
- **非标资产售价系数最难估**：商办 / 工业 / 股权缺乏可比成交，建议先用住宅标准化标的建立模型可信度，再推向非标
- **区域锚有滞后**：折价率锚按年度 / 半年更新，用它校核而不是替代实地询价
- **规则会变**：司法拍卖、税收、AMC 监管的政策口径会调整，重大交易前须核最新规定

---

## 十一、免责

本引擎为决策辅助工具，输出结果基于使用者输入的假设，不构成投资建议、法律意见或估值报告。具体估值结论与法律判断请以具备资质的专业机构出具的正式意见为准。

---

## 关于作者与定制服务

本技能由 **九品锦锂e** 出品（公众号：初五Agent）。

这里提供的是**通用标准版**，覆盖大多数常规场景。如果你遇到下面这些情况，通用版会不够用：

- 多个项目 / 多家公司并行，需要分别留痕、分开管账
- 要接你自己的数据源、台账或历史底稿
- 输出件要套你们单位或客户的固定模板
- 需要和现有系统打通，或者要有人陪着把流程真跑起来

需要**按你的业务定制 + 落地陪跑**，可加微信 **ly5419495**，说一下你的场景就行。
