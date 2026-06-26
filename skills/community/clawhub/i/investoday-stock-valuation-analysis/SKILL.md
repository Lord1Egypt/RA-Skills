---
name: investoday-stock-valuation-analysis
title: "股票估值分析"
version: 1.3.0
description: 面向A股个股估值分析，聚焦PE、PB、PS、PEG、历史分位、行业比较与估值匹配度判断。基于今日投资金融数据接口，自动识别股票代码并输出结构化估值分析报告。触发词：估值分析、贵不贵、便宜不便宜、历史分位、PEG、PE、PB。
tags:
  - valuation-analysis
  - pe-valuation
  - pb-valuation
  - peg-analysis
  - historical-percentile
  - industry-comparison
  - valuation-position
  - margin-of-safety
metadata:
  clawdbot:
    emoji: "💰"
    category: "finance"
    requires:
      skills: ["investoday-finance-data"]
---

# 💰 股票估值分析

面向 A 股个股估值分析，聚焦 PE、PB、PS、PEG、历史分位、行业比较与估值匹配度判断。基于今日投资金融数据接口，自动识别股票代码并输出结构化估值分析报告。

## 触发场景

- 用户询问某只股票当前估值高不高、贵不贵、有没有安全边际
- 用户希望判断历史分位、行业相对位置、成长与估值是否匹配
- 用户想知道“现在值不值得继续看”“估值有没有修复空间”
- 关键词：估值分析、PE、PB、PS、PEG、历史分位、贵不贵、便宜不便宜、估值位置、安全边际

## 输入示例

**示例 1：估值高低**
```
浪潮信息现在估值贵不贵？
```

**示例 2：历史分位**
```
宁德时代目前大概处在什么估值分位？
```

**示例 3：成长匹配度**
```
中际旭创的 PEG 合不合理，估值有没有透支？
```

> 💡 支持输入股票名称或 6 位股票代码。若用户只提供名称，先通过 `search` 识别标的，再进入估值分析流程。若用户更关心“财务质量”，优先使用 `股票财务分析`；若更关心“当前走势与支撑压力”，优先使用 `股票技术分析`。

## 前置依赖

本 Skill 依赖 `investoday-finance-data`（今日投资金融数据）Skill 获取实时金融数据。

基础 API 调用与底层执行方式统一以该 Skill 为准，业务 Skill 不重复展开底层接入细节。

## 工具说明

以下为本 Skill 通过 `investoday-finance-data` 使用的数据接口。在 System Prompt 中以 `工具ID` 标识调用。

### 基础工具

| 工具名称 | 工具ID | 方法 | 说明 |
|---------|--------|------|------|
| 综合标的搜索 | `search` | GET | 通过关键字搜索股票代码 |
| 股票基本信息 | `stock/basic-info` | GET | 获取股票名称、行业、主营业务等基础信息 |

### 估值核心工具

| 工具名称 | 工具ID | 方法 | 说明 |
|---------|--------|------|------|
| 当前估值指标 | `stock/finance/valuation` | GET | 获取 PE、PB、PS、PEG 等核心估值指标 |
| 历史估值序列 | `stock/finance/valuation-hist` | GET | 获取历史估值指标及分位参考 |
| 行情估值指标 | `stock/val-indicators` | GET | 获取总市值、流通市值、动态估值快照 |

### 基本面辅助工具

| 工具名称 | 工具ID | 方法 | 说明 |
|---------|--------|------|------|
| 盈利能力指标 | `stock/finance/profit-ability` | GET | 获取 ROE、ROA、毛利率等盈利指标 |
| 成长能力指标 | `stock/finance/growth-ability` | GET | 获取营收增速、净利润增速等成长指标 |
| 研报评级 | `report/stock-forecast-ratings` | GET | 获取机构目标价、评级与预期变化 |

## 数据获取流程

用户提供股票名称或代码后，Agent 按以下流程获取数据：

- **Step 0：标的识别（如用户输入名称而非代码）**：工具ID `search`，参数 `key=<股票名称> type=11`
- **Step 1：股票基本信息**：工具ID `stock/basic-info`，参数 `stockCode=<code>`
- **Step 2：当前估值指标**：工具ID `stock/finance/valuation`，参数 `stockCode=<code>`
- **Step 3：历史估值序列**：工具ID `stock/finance/valuation-hist`，参数 `stockCode=<code> type=2`
- **Step 4：行情估值指标**：工具ID `stock/val-indicators`，参数 `stockCode=<code>`
- **Step 5：盈利能力指标**：工具ID `stock/finance/profit-ability`，参数 `stockCode=<code>`
- **Step 6：成长能力指标**：工具ID `stock/finance/growth-ability`，参数 `stockCode=<code>`
- **Step 7：研报评级（近180天）**：工具ID `report/stock-forecast-ratings`，参数 `stockCode=<code> beginDate=<180天前> endDate=<今天> pageNum=1 pageSize=20`

> **并行优化**：完成 Step 0 的代码识别后，Step 1-7 可并行调用；分析时以 Step 2-4 的估值结果为主，以 Step 5-7 的基本面与一致预期作交叉验证。

## 分析框架（5步）

Agent 获取数据后，按以下 5 步框架进行结构化分析：

### Step 1：确认估值口径与公司类型

**目标**：明确该公司更适合看 PE、PB、PS 还是 PEG，避免估值方法错配。

**数据来源**：`stock/basic-info` + `stock/finance/profit-ability` + `stock/finance/growth-ability`

分析要点：
- 所处行业、商业模式、盈利稳定性
- 是否属于高成长、稳健成长、周期、金融或重资产公司
- 由此确定主要估值口径与辅助口径

**输出**：估值口径选择与适用理由。

### Step 2：评估当前估值水平

**目标**：判断当前 PE、PB、PS、PEG 所反映的定价状态。

**数据来源**：`stock/finance/valuation` + `stock/val-indicators`

分析要点：
- 当前 PE(TTM)、PB、PS、PEG 是否处于偏高、合理或偏低区间
- 动态估值与市值口径是否一致
- 若多个指标分化，需明确“贵在哪里、便宜在哪里”

**输出**：当前估值快照与初步判断。

### Step 3：评估历史位置与安全边际

**目标**：判断当前估值在历史区间中所处的位置。

**数据来源**：`stock/finance/valuation-hist`

分析要点：
- 当前 PE/PB/PS 所处历史分位
- 是否位于低估区、合理区或高估区
- 若历史分位较低但基本面未恶化，可提示安全边际改善

**输出**：历史分位结论与安全边际判断。

### Step 4：验证估值是否与基本面匹配

**目标**：判断当前估值是否被盈利能力和成长性支撑。

**数据来源**：`stock/finance/profit-ability` + `stock/finance/growth-ability` + `report/stock-forecast-ratings`

分析要点：
- ROE、毛利率、净利润增速能否支撑当前估值中枢
- PEG 是否反映合理的成长性价比
- 机构目标价与当前估值之间是否存在明显偏差

**输出**：估值与基本面匹配度结论。

### Step 5：形成综合估值结论

**目标**：综合当前估值、历史位置与基本面匹配度，输出最终判断。

**数据来源**：前 4 步分析结果汇总

分析要点：
- 当前更偏低估、合理还是高估
- 风险来自估值透支、成长不达预期还是市场过度悲观
- 后续需重点跟踪哪些验证指标（业绩兑现、估值修复、目标价变化）

**输出**：综合估值判断、主要依据与跟踪重点。

## 策略逻辑汇总

| 信号组合 | 含义 | 判断 |
|---------|------|------|
| PEG < 1 且净利润增速 > 20% | 成长性价比较高 | ✅ 积极 |
| PEG 介于 1-1.5 | 成长与估值大体匹配 | 📊 中性 |
| PEG > 2 | 市场预期要求偏高 | ⚠️ 警惕 |
| PE/PB 历史分位 < 30% | 处于相对低位区间 | ✅ 积极 |
| PE/PB 历史分位 30%-70% | 估值处于合理区间 | 📊 中性 |
| PE/PB 历史分位 > 70% | 估值处于偏高区间 | ⚠️ 警惕 |
| ROE > 15% 且 PB < 3 | 盈利能力对估值支撑较强 | ✅ 积极 |
| ROE < 10% 且 PB > 3 | 容易出现估值透支 | 🔴 高风险 |
| 机构目标价均值较现价上行空间 > 20% | 卖方预期偏乐观 | 🟡 关注 |
| 机构目标价明显下修且估值仍高分位 | 估值与预期双重承压 | 🔴 高风险 |

## 输出格式

```markdown
# 💰 [股票名称] 估值分析报告

> 分析日期：YYYY-MM-DD | 数据来源：今日投资

## 一、估值口径与公司类型

（说明公司更适合看 PE / PB / PS / PEG 的原因）

## 二、当前估值水平

（PE、PB、PS、PEG 与市值口径解读）

## 三、历史位置与安全边际

（历史分位、低估/合理/高估区间判断）

## 四、估值与基本面匹配度

（ROE、增速、机构目标价与当前估值的匹配关系）

## 五、综合结论

- 3-5 条核心发现
- 明确估值偏高/合理/偏低的主要依据
- 给出后续需要验证的关键指标
```

## 证据约束（必须遵守）

1. 每个估值判断至少引用 2 个数值证据；没有数据则写“该维度数据不足，暂无法判断”
2. 不允许只写“贵/便宜”，必须说明对应估值口径与数值
3. 历史分位、机构目标价、增长率等数据必须标明对应时间范围
4. 百分比统一保留 2 位小数，倍数统一保留 2 位小数
5. 不得引用输入数据之外的传闻、题材情绪或主观估值假设
6. 不给目标买卖价、仓位建议或交易时点，只做估值状态判断
7. 若公司属于强周期或盈利波动很大的行业，必须说明单纯使用 PE 可能失真

## 执行示例

用户说：“中际旭创现在贵不贵？”

1. 通过 `search` 获取股票代码
2. 并行调用 `stock/basic-info`、`stock/finance/valuation`、`stock/finance/valuation-hist`、`stock/val-indicators`、`stock/finance/profit-ability`、`stock/finance/growth-ability` 与 `report/stock-forecast-ratings`
3. 先确认估值口径，再判断当前估值、历史位置和匹配度
4. 输出 Markdown 格式估值分析报告
5. 在结尾写出估值结论与后续验证点

## 安全与隐私

- 仅通过今日投资 API 查询公开市场数据
- 不记录、不存储用户的查询记录
- 分析结论仅供参考，不构成投资建议
