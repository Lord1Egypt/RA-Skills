---
name: investoday-fund-comprehensive-diagnosis
title: "基金综合诊断"
version: 1.3.0
description: 面向公募基金综合诊断，聚焦收益表现、风险收益匹配、持仓结构、基金经理与费用分红特征。基于今日投资金融数据接口，自动识别基金代码并输出结构化基金综合诊断报告。触发词：基金诊断、基金分析、收益风险、持仓怎么看、长期持有、基金体检。
tags:
  - fund-diagnosis
  - fund-analysis
  - risk-return
  - holdings-structure
  - fund-manager
  - fee-analysis
  - dividend-profile
  - fund-checkup
metadata:
  clawdbot:
    emoji: "🩺"
    category: "finance"
    requires:
      skills: ["investoday-finance-data"]
---

# 🩺 基金综合诊断

面向公募基金综合诊断，聚焦收益表现、风险收益匹配、持仓结构、基金经理与费用分红特征。基于今日投资金融数据接口，自动识别基金代码并输出结构化基金综合诊断报告。

## 触发场景

- 用户询问某只基金值不值得长期持有，想看综合诊断报告
- 用户希望同时了解收益、风险、持仓、经理与费率分红等多维情况
- 用户想知道“这只基金整体质地怎么样”“适不适合继续拿”“主要问题出在哪”
- 关键词：基金诊断、基金分析、收益风险、持仓怎么看、长期持有、基金体检、综合诊断

## 输入示例

**示例 1：综合分析**
```
帮我分析一下易方达蓝筹精选这只基金。
```

**示例 2：继续持有判断**
```
华夏成长混合适不适合继续长期拿着？
```

**示例 3：多维诊断**
```
这只基金收益、风险、持仓和基金经理分别怎么样？
```

> 💡 支持输入基金名称或 6 位基金代码。若用户只提供名称，优先使用 `entity-recognition` 识别基金实体；若无法稳定唯一识别，再提示补充完整名称或代码。若用户只关心回撤、波动与风险承受特征，优先使用 `基金风险分析`；若只想拆解超额收益来自选股、择时还是 Beta 暴露，优先使用 `基金业绩归因分析`。

## 前置依赖

本 Skill 依赖 `investoday-finance-data`（今日投资金融数据）Skill 获取实时金融数据。

基础 API 调用与底层执行方式统一以该 Skill 为准，业务 Skill 不重复展开底层接入细节。

## 工具说明

以下为本 Skill 通过 `investoday-finance-data` 使用的数据接口。在 System Prompt 中以 `工具ID` 标识调用。

### 标的识别工具

| 工具名称 | 工具ID | 方法 | 说明 |
|---------|--------|------|------|
| 实体识别 | `entity-recognition` | POST | 从自然语言中识别基金实体 |
| 基金基本信息 | `fund/basic-info` | POST | 获取基金名称、类型、管理人、投资目标等 |

### 业绩与风险工具

| 工具名称 | 工具ID | 方法 | 说明 |
|---------|--------|------|------|
| 归因分析 | `fund/performance-attribution` | POST | 获取收益、回撤、波动率、Alpha、夏普等综合指标 |
| 基金评价同类平均指标 | `fund/eval-peer-avg-ind` | POST | 获取同类平均、排名与同类对比指标 |

### 组合与管理工具

| 工具名称 | 工具ID | 方法 | 说明 |
|---------|--------|------|------|
| 现任基金经理及回报 | `fund/current-manager-returns` | POST | 获取基金经理任职时间、任期回报与从业信息 |
| 基金资产分布 | `fund/portfolio-asset-holdings` | POST | 获取股票、债券、现金等资产配置 |
| 基金持仓股票 | `fund/portfolio-stock-holdings` | POST | 获取基金重仓股信息 |
| 基金持仓股票及行业涨幅 | `fund/holdings-stocks-industries` | POST | 获取重仓股及所属行业表现 |

### 费用与分红工具

| 工具名称 | 工具ID | 方法 | 说明 |
|---------|--------|------|------|
| 基金费率结构 | `fund/fee-structures` | POST | 获取申购费、赎回费、管理费、托管费等费率信息 |
| 基金分红 | `fund/dividend` | POST | 获取基金分红记录与分红特征 |

## 数据获取流程

用户提供基金名称或代码后，Agent 按以下流程获取数据：

- **Step 0：基金实体识别（如用户输入名称而非代码）**：工具ID `entity-recognition` (POST)，参数 `input=<用户原始问题>`
- **Step 1：基金基本信息**：工具ID `fund/basic-info` (POST)，参数 `fundCode=<code>`
- **Step 2：归因分析**：工具ID `fund/performance-attribution` (POST)，参数 `fundCode=<code>`
- **Step 3：同类平均指标**：工具ID `fund/eval-peer-avg-ind` (POST)，参数 `fundCode=<code>`
- **Step 4：现任基金经理及回报**：工具ID `fund/current-manager-returns` (POST)，参数 `fundCode=<code>`
- **Step 5：基金资产分布**：工具ID `fund/portfolio-asset-holdings` (POST)，参数 `fundCode=<code>`
- **Step 6：基金持仓股票**：工具ID `fund/portfolio-stock-holdings` (POST)，参数 `fundCode=<code>`
- **Step 7：基金持仓股票及行业涨幅**：工具ID `fund/holdings-stocks-industries` (POST)，参数 `fundCode=<code>`
- **Step 8：基金费率结构**：工具ID `fund/fee-structures` (POST)，参数 `fundCode=<code>`
- **Step 9：基金分红**：工具ID `fund/dividend` (POST)，参数 `fundCode=<code>`

> **并行优化**：完成 Step 0 的基金识别后，Step 1-9 可并行调用；分析时优先以 Step 2-4 形成收益风险与管理能力判断，再用 Step 5-9 补充持仓与回报特征。

## 分析框架（6步）

Agent 获取数据后，按以下 6 步框架进行结构化分析：

### Step 1：建立基金画像

**目标**：确认基金类型、投资目标、管理人与风险收益特征。

**数据来源**：`fund/basic-info`

分析要点：
- 基金类型、风格、是否偏主动管理或被动跟踪
- 管理人、投资目标、风险收益特征是否清晰
- 为后续收益与风险分析建立对照框架

**输出**：基金画像与产品定位。

### Step 2：评估收益表现与同类竞争力

**目标**：判断基金过去一段时间的收益能力及相对同类表现。

**数据来源**：`fund/performance-attribution` + `fund/eval-peer-avg-ind`

分析要点：
- 近 1 月、6 月、1 年、3 年收益表现
- 相对同类平均是否有超额收益
- 若短期好、长期一般或相反，必须明确指出期限分化

**输出**：收益表现结论与同类竞争力判断。

### Step 3：评估风险收益匹配度

**目标**：判断基金承担的风险是否换来了合理回报。

**数据来源**：`fund/performance-attribution` + `fund/eval-peer-avg-ind`

分析要点：
- 最大回撤、波动率、夏普、卡玛、Alpha 等指标
- 风险控制能力与收益质量是否匹配
- 若收益高但回撤明显偏大，应提示持有体验压力

**输出**：风险收益匹配度与主要短板。

### Step 4：分析持仓结构与风格支撑

**目标**：判断当前持仓配置是否支持基金既有业绩特征。

**数据来源**：`fund/portfolio-asset-holdings` + `fund/portfolio-stock-holdings` + `fund/holdings-stocks-industries`

分析要点：
- 股票、债券、现金等资产配置比例
- 前十大重仓股、行业暴露与持仓集中度
- 当前配置是否支撑收益来源，是否存在风格依赖或集中度风险

**输出**：持仓结构结论与配置支撑判断。

### Step 5：评估基金经理与管理人能力

**目标**：判断基金经理任期表现是否与产品定位匹配。

**数据来源**：`fund/current-manager-returns` + `fund/basic-info`

分析要点：
- 任职时间、任期回报、从业年限、平均年化表现
- 管理人平台实力与基金经理任内兑现程度
- 若产品偏被动或指数跟踪型，应弱化对基金经理主观管理能力的扩展解读，更关注产品定位是否稳定兑现
- 若经理任期较短，应提示样本期有限

**输出**：基金经理与管理能力评价。

### Step 6：分析费用与分红特征并形成综合结论

**目标**：补充产品持有成本与分红特征，形成完整综合判断。

**数据来源**：`fund/basic-info` + `fund/fee-structures` + `fund/dividend` + 前 5 步结果汇总

分析要点：
- 费率结构、分红记录与分红稳定性
- 产品回报特征更偏净值增长导向还是现金分红导向
- 综合收益、风险、持仓、经理、费用后形成总判断

**输出**：综合诊断结论与后续跟踪重点。

## 策略逻辑汇总

> **口径提示**：以下信号更适合作为同类型基金内部的粗略参考；股票型、债券型、指数型、FOF 等产品不可直接按同一阈值横向套用。

| 信号组合 | 含义 | 判断 |
|---------|------|------|
| 近1年收益显著高于同类平均且回撤控制良好 | 业绩与风险匹配较优 | ✅ 积极 |
| 近1年收益较高但最大回撤也显著偏高 | 收益来自较高风险承担 | 🟡 关注 |
| 夏普比率 > 1 且卡玛比率较高 | 风险调整后收益较好 | ✅ 积极 |
| Alpha 为正且同类排名靠前 | 主动管理有一定价值 | ✅ 积极 |
| 股票仓位高且重仓股集中度高 | 风格与集中度暴露较明显 | 🟡 关注 |
| 经理任期回报稳定、从业年限较长 | 管理延续性较强 | ✅ 积极 |
| 经理任期较短或任期回报缺乏代表性 | 管理能力仍需观察 | 📊 中性 |
| 分红记录稳定且产品定位偏稳健 | 现金回报特征较清晰 | 🟡 关注 |
| 收益落后同类且风险控制也不占优 | 综合性价比较弱 | 🔴 高风险 |
| 产品定位与实际持仓风格明显不一致 | 风格漂移风险存在 | ⚠️ 警惕 |

## 输出格式

```markdown
# 🩺 [基金名称]（[基金代码]）基金综合诊断报告

> 分析日期：YYYY-MM-DD | 数据来源：今日投资

## 一、综合诊断结论

（用一段话概括基金整体质地、主要优势和主要问题）

## 二、基金概况

（基金类型、定位、管理人、风险收益特征）

## 三、收益能力诊断

（多期限收益、同类比较、超额收益情况）

## 四、风险收益特征

（回撤、波动率、夏普、卡玛、Alpha 等）

## 五、持仓结构诊断

（资产配置、前十大持仓、行业暴露、集中度）

## 六、经理与管理人诊断

（经理任期回报、从业年限、平台实力）

## 七、费用与分红特征

（费率、分红、回报特征）

## 综合结论

- 3-5 条核心发现
- 明确基金主要强项、短板与更匹配的持有诉求
- 给出后续需要跟踪的关键变量
```

## 执行示例

用户说：“帮我分析一下华夏成长混合适不适合继续长期拿着。”

1. 通过 `entity-recognition` 识别基金实体与基金代码
2. 并行调用 `fund/basic-info`、`fund/performance-attribution`、`fund/eval-peer-avg-ind`、`fund/current-manager-returns`、`fund/portfolio-asset-holdings`、`fund/portfolio-stock-holdings`、`fund/holdings-stocks-industries`、`fund/fee-structures` 与 `fund/dividend`
3. 从收益、风险、持仓、经理、费用分红 5 个维度做综合诊断
4. 输出 Markdown 格式基金综合诊断报告
5. 在结尾写出综合结论与后续跟踪重点

## 安全与隐私

- 仅通过今日投资 API 查询公开市场数据
- 不记录、不存储用户的查询记录
- 分析结论仅供参考，不构成投资建议
