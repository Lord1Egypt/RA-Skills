# 经济学分支工作流（E-0 ~ E-5）

> 配套主 skill: [SKILL.md](../SKILL.md)
> 版本: 2.0.0 新增

## 概述

经济学分支（Econ Branch）是 `nature-paper-workflow` v2.0.0 引入的可选分支，专门处理经济学论文写作。与 STEM 分支的 12 阶段工作流并行存在，采用更聚焦的 6 阶段工作流（E-0 ~ E-5）。

**入口**：Pre-Phase 学科识别命中经济学信号 → 进入 Econ 分支
**前置条件**：用户已安装 econ-* 扩展包（5 个子技能）

## E-0: 输入审计

**主 skill**：`econ-writing-workflow`
**共享 skill**：无
**触发词**：经济学论文 / econ paper / 经济学写作 / 写经济学论文

### 任务
- 检查研究问题（research question）是否明确
- 检查结果包（results package）是否齐全：主回归 / 稳健性 / 异质性 / 机制
- 检查变量说明（variable documentation）完整性
- 标记 TODO 项，生成写作计划

### 升级到 multiagent
当 E-0 发现以下任一情况，自动升级到 `econ-writing-workflow-multiagent`：
- 主表 + 稳健性 + 异质性 + 机制四类表全部要写
- 涉及 3 个以上章节同时起草
- 用户明示"复杂项目"或"多章节协同"

### 输出
- `research_question.md`：研究问题陈述
- `results_package_checklist.md`：结果包清单
- `writing_plan.md`：写作计划（含 TODO）

---

## E-1: 全文起草

**主 skill**：`econ-write`（英文）/ `cn-top-econ-writing`（中文）
**共享 skill**：`paper-bootstrap`（项目初始化）
**触发词**：起草 / 写摘要 / 写引言 / 写方法 / 写实证 / 写讨论 / 写结论 / 投稿包 / cover letter

### 任务
按以下顺序起草（不按 IMRAD 顺序，遵循经济学写作惯例）：
1. **Main Results**（主结果）→ 先写主回归表 + 文字描述
2. **Identification Strategy**（识别策略）→ IV / DiD / RDD / RCT 的识别假设
3. **Data & Variables**（数据与变量）→ 数据来源、变量定义、描述性统计
4. **Introduction**（引言）→ 研究问题 + 贡献 + 主要发现
5. **Literature Review**（文献综述）→ 定位与差异化
6. **Robustness & Heterogeneity**（稳健性与异质性）→ 验证主结果
7. **Mechanism**（机制）→ 中介 / 调节
8. **Conclusion**（结论）→ 政策含义 + 局限

### 英文 vs 中文路由
- **英文顶刊**（AER / QJE / JPE / Econometrica / REStud）→ `econ-write`
- **中文顶刊**（经济研究 / 管理世界 / 中国工业经济 / 经济学季刊）→ `cn-top-econ-writing`

### 输出
- `draft_main_results.md`
- `draft_identification.md`
- `draft_data_variables.md`
- `draft_introduction.md`
- `draft_literature.md`
- `draft_robustness.md`
- `draft_mechanism.md`
- `draft_conclusion.md`

---

## E-2: 表图设计

**主 skill**：`econ-table-figure-design`
**共享 skill**：无
**触发词**：表图设计 / 三线表 / 回归表 / 事件研究图 / 平行趋势图 / 地图 / 经济学图

### 任务
按四类表 + 四类图设计：

#### 四类表
1. **Main Regression Table**（主回归表）：基线结果 + 核心系数 + 标准误
2. **Robustness Table**（稳健性表）：替代样本 / 替代变量 / 替代模型
3. **Heterogeneity Table**（异质性表）：分组分析 + 异质性效应
4. **Mechanism Table**（机制表）：中介 / 调节 / 机制检验

#### 四类图
1. **Event Study Plot**（事件研究图）：动态效应 + 平行趋势检验
2. **Trend Plot**（趋势图）：处理组 vs 对照组时间趋势
3. **Map**（地图）：空间分布 + 中国地图合规（审图号）
4. **Distribution Plot**（分布图）：binscatter / 直方图 / 密度图

### 正文 vs 附录取舍
- **正文**：主表 + 1-2 张核心图
- **附录**：稳健性全表 + 异质性全表 + 机制全表 + 补充图

### 输出
- `tables/main_regression.tex`
- `tables/robustness.tex`
- `tables/heterogeneity.tex`
- `tables/mechanism.tex`
- `figures/event_study.pdf`
- `figures/trend_plot.pdf`
- `figures/map.pdf`
- `figures/distribution.pdf`

---

## E-3: 论证逻辑审计

**主 skill**：`econ-writing-workflow`（使用 argument-logic / regression-results / manuscript-voice references）
**共享 skill**：无
**触发词**：论证审计 / argument audit / 论证逻辑 / claim 检查 / magnitude check

### 任务
按三个维度审计论证逻辑：

#### Dimension 1: Argument Spine（论证脊柱）
- 检查 research question → hypothesis → empirical strategy → results → conclusion 的链条是否完整
- 检查每个 claim 是否有对应的 evidence（表或图）
- 检查是否存在"无证据的 claim"或"无 claim 的证据"

#### Dimension 2: Draft-Time Clarity（草稿期清晰度）
- 检查每段是否有明确的 topic sentence
- 检查段落间是否有逻辑过渡
- 检查术语使用是否一致（如"处理效应"vs"因果效应"）

#### Dimension 3: Regression Magnitude（回归量级）
- 检查系数量级是否在合理范围（避免"显著但经济意义小"）
- 检查标准误与样本量的关系
- 检查 R² / F-stat / Weak IV F-stat 是否达标

### 输出
- `audit_argument_spine.md`：论证脊柱审计报告
- `audit_clarity.md`：清晰度审计报告
- `audit_magnitude.md`：量级审计报告

---

## E-4: 期刊适配

**主 skill**：`cn-top-econ-writing`（中文顶刊）/ `econ-write`（英文顶刊）
**共享 skill**：`submission-audit`（通用投稿预检）
**触发词**：期刊适配 / 投稿体例 / 经济研究体例 / 管理世界体例 / AER 体例 / submission format

### 中文顶刊 4 模式
| 模式 | 期刊 | 体例特征 |
|---|---|---|
| **ER** | 《经济研究》 | 长摘要（500字+）+ 详细数据说明 + 中文参考文献 |
| **MW** | 《管理世界》 | 短摘要（200字）+ 政策启示强 + 图表中文标注 |
| **CIE** | 《中国工业经济》| 中等摘要 + 产业政策聚焦 + 摘要图表 |
| **EQ** | 《经济学季刊》 | 英文摘要 + 实证规范 + 详尽稳健性 |

### 英文顶刊 5 模式
| 期刊 | 体例特征 |
|---|---|
| **AER** | 短摘要 + 主表简洁 + 附录详尽 |
| **QJE** | 长引言 + 故事性强 + 理论+实证并重 |
| **JPE** | 中等篇幅 + 理论框架 + 实证验证 |
| **Econometrica** | 严格计量 + 识别假设 + 估计量推导 |
| **REStud** | 理论模型 + 实证检验 + 政策含义 |

### 4 门槛审计（cn-top-econ-writing 通用）
1. **数据门槛**：数据来源是否可追溯 + 描述性统计是否完整
2. **识别门槛**：识别策略是否清晰 + 内生性处理是否充分
3. **稳健性门槛**：稳健性检验是否覆盖核心假设 + 量级是否合理
4. **贡献门槛**：贡献陈述是否具体 + 与文献差异化是否明确

### 输出
- `journal_adapted_draft.md`：期刊适配后的稿件
- `submission_checklist.md`：投稿清单

---

## E-5: 审稿 + 返修

**主 skill**：`nature-reviewer`（共享，按经济学视角调整）
**共享 skill**：`nature-response`（逐点回复）
**触发词**：审稿模拟 / 预审 / 审稿意见 / 返修 / rebuttal / response / 逐点回复

### 审稿模拟（E-5a）
`nature-reviewer` 按经济学视角调整审稿维度：
- **Identification Quality**：识别策略是否可信 + 内生性处理
- **Data Quality**：数据来源 + 样本选择 + 描述性统计
- **Robustness Coverage**：稳健性检验是否覆盖核心威胁
- **Mechanism Credibility**：机制检验是否说服力
- **Contribution Significance**：贡献陈述 vs 文献定位
- **Policy Implication**：政策含义是否过度推断

输出 3 份 reviewer reports + 综合评审

### 返修回复（E-5b）
`nature-response` 执行：
- 逐点回复（point-by-point response）
- 标红修改（tracked changes）
- cover letter（给 editor 的信）

### 输出
- `reviewer_reports/reviewer_1.md`
- `reviewer_reports/reviewer_2.md`
- `reviewer_reports/reviewer_3.md`
- `cross_review_synthesis.md`
- `response_letter.md`
- `revised_manuscript.md`
- `cover_letter.md`

---

## 跨阶段 handoff 产物

| 起始 → 目标 | 必带产物 | 说明 |
|---|---|---|
| E-0 输入审计 → E-1 起草 | `research_question.md`, `results_package_checklist.md`, `writing_plan.md` | 审计结果作为起草依据 |
| E-1 起草 → E-2 表图 | 草稿中所有提及"表 X"/"图 Y"的位置 | 表图编号需对应 |
| E-2 表图 → E-3 论证审计 | 完整的表图 + 表注 + 图注 | 审计对照表图检查 claim |
| E-3 审计 → E-4 期刊适配 | 审计报告 + 修订草稿 | 适配前先修复审计发现的问题 |
| E-4 适配 → E-5 审稿 | 期刊适配后的稿件 + 投稿清单 | 审稿模拟按目标期刊视角 |

## 关键决策点

### 决策点 1: 何时升级到 multiagent
- 主表 + 稳健性 + 异质性 + 机制四类表全要写
- 3 个以上章节同时起草
- 用户明示"复杂项目"

### 决策点 2: 英文 vs 中文路由
- 期刊是英文顶刊 → `econ-write`
- 期刊是中文顶刊 → `cn-top-econ-writing`
- 用户未明示 → 问 1 个问题确认投稿语言

### 决策点 3: E-3 论证审计的优先级
- 主表 + 主张 → 最高优先级
- 稳健性 + 异质性 → 中优先级
- 机制 → 低优先级（可选）

### 决策点 4: E-4 期刊适配的严格度
- 投稿前必做（strict）
- 返修时按 reviewer 意见调整（moderate）
- 内部传阅可跳过（skip）

## econ-* 子技能速查

| Skill | 阶段 | 核心能力 |
|---|---|---|
| `econ-writing-workflow` | E-0 / E-3 | 任务分类 + argument-logic / regression-results / manuscript-voice references |
| `econ-write` | E-1 / E-4 | 英文经济学论文写作，融合 50+ 经济学家指南 |
| `cn-top-econ-writing` | E-1 / E-4 | 中文顶刊写作，4 模式（ER/MW/CIE/EQ）+ 4 门槛审计 |
| `econ-table-figure-design` | E-2 | 三线表 + 回归图 + 事件研究图 + 地图 |
| `econ-writing-workflow-multiagent` | E-0~E-5 | 多代理协调（复杂项目升级） |

## 许可证声明

econ-* 扩展包采用 **CC BY-NC 4.0** 许可（非商用）。本 router（`nature-paper-workflow`）仅做路由，不复制 econ-* 内容。用户需从原仓库独立安装：
- 仓库：https://github.com/juliaError/econ-TopJournal-writing-Skill
- 上游依赖：`econ-write` 基于 `hanlulong/econ-writing-skill`（MIT）
- 伦理使用约束：见原仓库 `ETHICAL_USE.md`
