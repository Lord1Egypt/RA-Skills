---
source_url: https://www.mca.gov.cn/article/yw/hjzcbz/2017/201710/20171000006382.shtml
verified_date: 2026-03-30
next_review_date: 2026-06-30
version: 1
breaking_change: false
report_type: project_final
funder_platform: generic
---

# 通用项目结项报告模板

## 章节结构

### 第1章：项目基本信息
- **必含字段**：project_name（项目名称）、org_name（执行机构）、funder（资助方）、total_grant（资助总额）、project_period（项目周期，开始日期–结束日期）、project_area（项目地区）、target_group（目标群体）、project_objective（项目目标）
- **格式要求**：项目概况表格，字段名与值两列
- **字数建议**：表格为主，项目目标可补充1–2句说明
- **数据来源**：project_name, org_name, funder, total_grant, project_period, project_area, target_group, project_objective

> **注意**：total_grant 须填写实际数据，禁止由 AI 编造。

**格式示例**

| 字段 | 内容 |
|------|------|
| 项目名称 | [project_name] |
| 执行机构 | [org_name] |
| 资助方 | [funder] |
| 资助总额 | [total_grant] 元 |
| 项目周期 | [project_period] |
| 项目地区 | [project_area] |
| 目标群体 | [target_group] |
| 项目目标 | [project_objective] |

---

### 第2章：项目目标与完成情况
- **必含字段**：indicators（指标列表，每条含：indicator_name、planned、actual、completion_rate）。completion_rate 低于 80% 时，同一行或下方必须填写 deviation_reason
- **格式要求**：指标对照表（计划值 vs 实际值 vs 完成率）
- **字数建议**：表格为主，整体评价段落 100–200 字
- **数据来源**：indicators[].indicator_name, indicators[].planned, indicators[].actual, indicators[].completion_rate, indicators[].deviation_reason（当 completion_rate < 80%）

**格式示例**

| 指标名称 | 计划值 | 实际值 | 完成率 | 备注 |
|---------|-------|-------|-------|------|
| [指标1] | [计划] | [实际] | [completion_rate]% | |
| [指标2] | [计划] | [实际] | [completion_rate]% | [deviation_reason（如完成率<80%）] |

[整体完成情况评价段落]

---

### 第3章：主要活动记录
- **必含字段**：activities（活动列表，每条含：activity_date、activity_name、activity_location、participant_count、activity_description）
- **格式要求**：时间线或列表格式，按活动时间排序
- **字数建议**：每条活动 50–150 字
- **数据来源**：activities[].activity_date, activities[].activity_name, activities[].activity_location, activities[].participant_count, activities[].activity_description

**格式示例**

**[activity_date] — [activity_name]**

地点：[activity_location]  参与人数：[participant_count] 人

[activity_description]

---

**[activity_date] — [activity_name]**

地点：[activity_location]  参与人数：[participant_count] 人

[activity_description]

---

### 第4章：财务执行情况
- **必含字段**：budget_lines（预算行列表，每条含：category、budgeted、actual、variance_rate）。variance_rate 绝对值 > 10% 时，该行必须填写 variance_reason。finance_summary（财务执行整体说明）
- **格式要求**：预算 vs 实际对比表，差异列标注百分比。差异 > ±10% 的行用备注说明原因
- **字数建议**：表格为主，文字说明 100–200 字
- **数据来源**：budget_lines[].category, budget_lines[].budgeted, budget_lines[].actual, budget_lines[].variance_rate, budget_lines[].variance_reason（当 |variance_rate| > 10%）, finance_summary

> **注意**：以下所有金额须填写实际数据，禁止由 AI 编造。

**格式示例**

| 支出类别 | 预算金额（元） | 实际支出（元） | 差异率 | 差异说明 |
|---------|-------------|-------------|------|---------|
| [类别1] | [预算] | [实际] | [variance_rate]% | |
| [类别2] | [预算] | [实际] | [variance_rate]% | [variance_reason（差异>±10%时必填）] |
| **合计** | **[预算合计]** | **[实际合计]** | | |

[finance_summary]

---

### 第5章：项目成效与故事
- **必含字段**：quantitative_outcomes（量化成效，列表）、story_case（典型案例，至少1个，含 case_title 和 case_description）
- **格式要求**：量化成效以列表呈现，典型案例以段落叙述。案例中禁止出现可识别个体的真实姓名和身份证号等 PII
- **字数建议**：量化成效列表 + 每个典型案例 150–300 字
- **数据来源**：quantitative_outcomes, story_case[].case_title, story_case[].case_description

> **注意**：案例描述须已经过 PII 处理（匿名化），禁止在模板或提示词中要求填写个体真实姓名。

**格式示例**

**量化成效**

- [成效1]
- [成效2]

**典型案例：[case_title]**

[case_description]（案例中个人信息已匿名处理）

---

### 第6章：执行挑战与应对
- **必含字段**：challenges（执行中遇到的主要挑战，列表）、responses（应对措施，与挑战逐一对应）
- **格式要求**：逐条列举，挑战与应对配对呈现
- **字数建议**：200–400 字
- **数据来源**：challenges, responses

**格式示例**

**挑战1**：[challenge_1]

**应对**：[response_1]

---

### 第7章：经验总结与改进建议
- **必含字段**：lessons_learned（经验总结，列表）、improvement_suggestions（改进建议，列表）
- **格式要求**：列表格式，经验与建议分别列举
- **字数建议**：200–400 字
- **数据来源**：lessons_learned, improvement_suggestions

**格式示例**

**主要经验**

- [经验1]
- [经验2]

**改进建议**

- [建议1]
- [建议2]

---

### 第8章：社会影响与媒体传播（如有）
- **必含字段**：media_coverage（媒体报道，列表，含 media_name、coverage_date、coverage_url）、social_impact_desc（社会影响描述）
- **格式要求**：媒体报道以表格列举（如有），社会影响以段落描述。若本章无内容，注明"本项目报告期内无媒体传播记录"
- **字数建议**：100–300 字
- **数据来源**：media_coverage（可为空），social_impact_desc

**格式示例**

**媒体报道**

| 媒体名称 | 报道日期 | 链接 |
|---------|---------|------|
| [media_name] | [coverage_date] | [coverage_url] |

[social_impact_desc]

---

### 附件清单
- **必含内容**：列出本报告应附上的支撑材料清单（实际附件由 NGO 自行整理，此处为提示清单）
- **格式要求**：编号列表
- **数据来源**：（固定提示文本，无变量）

**格式示例**

本报告建议附上以下材料：

1. 活动照片（至少 [activity_count] 场活动照片）
2. 财务凭证（发票、收据汇总）
3. 受益对象签到表或服务记录
4. 媒体报道截图（如有）
5. 其他支撑材料

---

### 附录：声明
- **必含内容**：AI 辅助生成声明 + 免责提示
- **格式要求**：固定文本，置于报告末尾，不可删改
- **数据来源**：（固定文本，无变量）

**格式示例**

---

**AI 辅助生成声明**

本报告由 AI 辅助生成，最终内容经人工审核确认。请在正式提交前核实所有数据的准确性。

**免责提示**

AI 生成，仅供参考，请核实数据。本报告内容不构成法律或财务意见，所有数字和事实须以组织实际记录为准。
