---
name: investment-research-os
version: 1.2
description: |
  投资研究操作系统 v1.2 — 来源可追溯 + 自动数据填入 + 行业量化模型 + 多标的并行。
  
  触发条件：用户输入投资研究对象，要求"投资研究"、"深度研究"、
  "投资决策分析"、"研究XXX"、"投资分析"、"对比XXX和YYY"等关键词时使用本 skill。
  
  不写研报，只做判断。核心五问：
  市场定价什么？→ 市场错在哪里？→ 预期差在哪里？→ 赔率风险比如何？→ 如何下注？
  
  v1.2新功能（来源可追溯）：
  - 每个数据点必须标注来源URL、覆盖时段、验证方式
  - 报告末尾强制附加「来源与注释」区块 + 「输出检查清单」
  - 支持审计轨迹、数据验证、透明度及未来更新
  
  v1.1功能：
  - 自动解析 Macrotrends/StockAnalysis 数据并填入模板
  - 行业生命周期量化判定（基于营收增速+利润率趋势）
  - 多标的并行比较研究（--targets模式）
  
  架构：6个专业Agent + 1个CIO裁决引擎，10层研究深度，形成研究→假设→建仓→跟踪→调整→退出的完整闭环。
  
  数据源：NeoData（行情/财报）、OpenAlex（学术趋势）、World Bank（宏观）、web搜索（行业/竞争）
---

# Investment Research OS v1.1

## 核心理念

```
多数人研究：发生了什么
优秀投资者研究：为什么发生
顶级投资者研究：市场接下来会重新定价什么
```

**研究终点不是"写完报告"，而是：**
```
研究 → 形成假设 → 建仓 → 跟踪验证 → 调整仓位 → 退出
```

## 系统架构

```
市场 → 行业 → 公司 → 估值 → 预期差 → 风险 → 投资决策
          ↑
     6个专业Agent
     (并行/串行协作)
          ↓
      CIO裁决引擎
```

## 工作流程（10层强制执行）

### Layer 0 — 投资问题重构
**禁止直接研究公司。先定义投资问题。**

用户输入后，先将其转化为具体的投资问题：
- 市场是否低估/高估XXX未来Y年的Z？
- 而不是：XXX怎么样？

### Layer 1 — 行业状态机
行业分析师（Agent1）输出：
- 行业生命周期阶段（导入/成长/成熟/衰退）
- 当前阶段核心驱动因素
- 行业核心矛盾（A vs B）
- 未来催化剂

### Layer 2 — 公司研究框架
公司分析师（Agent2）输出：
- 商业模式 → 竞争优势 → 盈利能力 → 增长能力 → 管理层 → 资本配置
- 6个维度结构化分析

### Layer 3 — 护城河分析
使用 Moat Framework 评估：
- 品牌 / 网络效应 / 成本优势 / 转换成本 / 规模优势 / 数据优势
- 综合护城河评分 0-100

### Layer 4 — 市场预期差分析
**这是投资研究的核心。**

预期差分析师（Agent5）输出：
- 市场当前共识（3点）
- 反共识判断（3点）+ 原因
- 预期差 = 反共识 − 共识 的空间

### Layer 5 — 估值系统
估值分析师（Agent4）输出：
- 当前估值 + 历史分位
- 行业比较
- 三情景估值：Bull / Base / Bear
- 隐含增长率

### Layer 6 — 催化剂系统
市场不会因价值出现而上涨，必须有催化剂：
- 未来12个月3个核心催化剂
- 每个催化剂的概率 + 影响程度

### Layer 7 — 红队系统
红队分析师（Agent6）强制反向分析：
- 做空这家公司最强的3个理由
- 投资逻辑失效的条件
- 最危险的数据点

### Layer 8 — 投资决策引擎
CIO综合所有Agent输出，给出最终判断：
- 评级：强烈买入 / 买入 / 观察 / 减持 / 卖出
- 置信度 0-100
- 核心逻辑（3点）
- 关键催化剂（3点）
- 关键风险（3点）

### Layer 9 — 仓位系统
财务分析师（Agent3）结合赔率给出：
- 赔率（Bull vs Bear 收益比）
- 成功概率
- 预期收益 / 最大回撤
- 建议仓位
- 观察指标

## Agent定义

### Agent1：行业分析师（industry-analyst）
**职责**：判断行业周期位置，找到核心矛盾
**输入**：公司主营业务 → 输出行业状态机

### Agent2：公司分析师（company-analyst）
**职责**：拆解公司竞争要素，找到增长来源
**输入**：公司 → 输出6维度框架

### Agent3：财务分析师（financial-analyst）
**职责**：验证或推翻投资故事，找到最危险的数据
**输入**：财务数据 → 输出盈利质量 + 仓位建议

### Agent4：估值分析师（valuation-analyst）
**职责**：理解市场当前定价，找到三情景赔率
**输入**：估值数据 → 输出三情景估值

### Agent5：预期差分析师（expectation-gap-analyst）
**职责**：识别市场共识 vs 真相，找到反向押注的理由
**输入**：所有信息 → 输出共识/反共识/预期差

### Agent6：红队分析师（red-team-analyst）
**职责**：强制反向思考，找到投资逻辑的致命漏洞
**输入**：投资逻辑 → 输出做空理由 + 逻辑失效条件

### CIO：首席投资官（cio-decision）
**职责**：综合所有信息，做出最终投资决策
**输入**：所有Agent输出 → 输出投资结论 + 仓位

## 数据源调用

### 优先级排序（按稳定性）
1. **Macrotrends**（最稳定，无需API Key）→ PE/营收/净利润/毛利率历史
2. **StockAnalysis**（稳定）→ 卖方一致预期/目标价
3. **OpenAlex**（稳定，HTTP直连）→ 学术趋势
4. **NeoData**（间歇性不可用）→ 行情/财务
5. **World Bank**（需代理）→ 宏观经济

### 具体调用
```
# 单标的自动数据填入（v1.1）
python scripts/investment_research_v11.py --target "腾讯" --question "市场是否低估腾讯未来3年盈利增长？" --fetch-data

# 多标的并行比较（v1.1新增）
python scripts/investment_research_v11.py --targets "腾讯,英伟达,苹果" --question "三者中谁最被低估？"

# NeoData（先确认服务可用）
python scripts/neodata_health_check.py

# OpenAlex
python scripts/openalex_api.py --query "行业关键词" --type institutions

# World Bank
python scripts/worldbank_api.py --query "国家+指标"

# 卖方一致预期
web_fetch https://stockanalysis.com/stocks/{ADR_TICKER}/forecast/
```

## 执行模式

### 快速研究（单标的，5分钟）
Layer0 → Layer4 → Layer8 → Layer9，跳过红队
```bash
python scripts/investment_research_v11.py --target "腾讯" --question "是否低估？" --fetch-data
```

### 完整研究（单标的，15-20分钟）
执行全部10层，6个Agent串/并行
```bash
python scripts/investment_research_v11.py --target "腾讯" --question "核心问题" --fetch-data
```

### 比较研究（多标的，20-30分钟）[v1.1新增]
1. Layer0 定义比较问题
2. 对每个标的并行执行 Layer1-7（subagent并行）
3. Layer8 CIO比较排序（使用 cio.md 中的多标的模板）
4. 输出组合配置建议
5. 输出文件：`research/portfolio_{date}.md`
```bash
python scripts/investment_research_v11.py --targets "腾讯,英伟达,苹果" --question "谁最被低估？" --fetch-data
```

## 输出格式

最终输出包含：
1. 投资问题定义
2. 行业状态机
3. 公司分析（6维度）
4. 护城河评分
5. 市场预期差
6. 三情景估值
7. 催化剂系统
8. 红队报告
9. 投资结论（CIO裁决）
10. 仓位建议

每个标的的研究结果存入：`research/{标的}_{日期}.md`
组合研究存入：`research/portfolio_{日期}.md`

## 来源可追溯规范（v1.2 新增）

### 核心原则
每个数据点必须回答三个问题：**它来自哪里？它覆盖哪个时期？它是如何被核实的？**

### 引用规范
- **数据来源**：必须附超链接（URL格式，非纯文本描述）
  - Macrotrends → `https://www.macrotrends.net/stocks/charts/{TICKER}/{slug}/{metric}`
  - StockAnalysis → `https://stockanalysis.com/stocks/{TICKER}/forecast/`
  - NeoData → `neodata://{symbol}`（内部数据源）
  - OpenAlex → `https://api.openalex.org/works?filter=...`
  - World Bank → `https://api.worldbank.org/v2/country/{code}/indicator/{id}`
  - 研报/新闻 → 原文URL
- **覆盖时期**：`YYYY-MM-DD ~ YYYY-MM-DD` 或 `FY2021-FY2025`
- **验证方式**：交叉核对（至少2个独立来源）或单来源标注 `⚠ 单来源`
- **截至日期**：所有数据必须标注 `截至 YYYY-MM-DD`

### 优先级来源
| 数据类型 | 优先来源 | 备选来源 |
|----------|----------|----------|
| 财务历史 | Macrotrends | NeoData |
| 卖方预期 | StockAnalysis | Reuters |
| 学术趋势 | OpenAlex | arXiv |
| 实时行情 | NeoData | Yahoo Finance |
| 宏观经济 | World Bank | IMF |
| 行业竞争 | web搜索 | 公司IR页面 |

### 报告模板中的引用格式
```markdown
| 指标 | 数值 | 来源 | 覆盖时期 | 验证 |
|------|------|------|----------|------|
| PE Ratio | 18.65x | [Macrotrends](url) | 2022-2026 | 交叉: [StockAnalysis](url) |
| 营收增速 | 13.86% | [Macrotrends](url) | FY2024-FY2025 | 单来源 |
```

## 输出检查清单（v1.2 新增）

**报告生成后，必须逐一确认：**

- [ ] 每个数据点标注了来源URL
- [ ] 数据覆盖时期明确
- [ ] 关键数据经过交叉核对（或标注 ⚠ 单来源）
- [ ] 数据来自一致的时间段（无混用FY/CY导致的时间错位）
- [ ] 相关处已添加超链接（文件、页面、研究报告）
- [ ] 注释部分记录了来源和方法论
- [ ] 日期戳为当前（"截至 YYYY-MM-DD"）
- [ ] [MANUAL] 标注处已人工填写
- [ ] 三情景估值完整
- [ ] 红队分析已执行
- [ ] 仓位建议具体数字

## 约束

- **禁止写公司介绍**：只写市场关心的投资信息
- **禁止单点估值**：必须三情景
- **禁止模糊判断**：每个结论必须有数据支撑
- **禁止不做空思考**：红队必须强制执行
- **禁止无来源数据**：v1.2起每个数据点必须标注来源（v1.1的[AUTO-FILL]数据由脚本自动标注URL）
- **仓位必须明确**：给具体数字，不给"适量""适度"

## 已知问题与 v1.1 改进方向

### 数据源稳定性（已知）
- NeoData Gateway 行情数据间歇性返回空 → 备选：Macrotrends
- Yahoo Finance 持续限流 → 备选：mcporter yahoo-finance MCP
- World Bank 需代理 → 已集成但偶发超时

### 脚本模板待完善
- `--fetch-data` 获取的数据未自动填入模板 → v1.1 计划
- Macrotrends 数据解析需 HTML scraping → 当前返回原始 HTML

### 评估记录
- v1.0 Round 1：98/115 = B级
- v1.0 Round 2：102.5/115 = B+级
- v1.0 Round 3：106/115 = A-级
- v1.1 目标：≥110/115 = A级
- v1.2 目标：≥112/115 = A+级（来源可追溯加分）

### v1.2 改进项
1. ✅ 来源可追溯：每个数据点标注来源URL、覆盖时期、验证方式
2. ✅ 输出检查清单：报告生成后强制确认数据完整性
3. ✅ 引用格式标准化：超链接+交叉核对+截至日期
4. ✅ 优先级来源表：按数据类型指定首选/备选来源
5. ✅ 禁止无来源数据：新增约束

### v1.1 改进项（已完成）
1. ✅ 自动数据填入模板（Macrotrends/StockAnalysis解析）
2. ✅ 行业生命周期量化判定（classify_industry_lifecycle函数）
3. ✅ 多标的并行比较（--targets模式+CIO排序模板）
4. ✅ 数据缓存（JSON文件复用）
5. ✅ 网络请求retry+指数退避

## 使用方法

用户输入：
```
/research 研究腾讯，市场是否低估腾讯未来3年的盈利增长？
```

或中文：
```
研究腾讯，市场是否低估腾讯未来3年的盈利增长？
```

系统自动执行完整10层研究流程，最终给出投资结论和仓位建议。
