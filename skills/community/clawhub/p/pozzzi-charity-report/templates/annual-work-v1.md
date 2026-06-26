---
source_url: https://www.mca.gov.cn/article/yw/hjzcbz/2017/201710/20171000006382.shtml
verified_date: 2026-03-30
next_review_date: 2026-06-30
version: 1
breaking_change: false
report_type: annual_work
funder_platform: generic
---

# 社会组织年度工作报告模板

## 章节结构

### 第1章：组织基本信息
- **必含字段**：org_name（组织名称）、registration_number（登记证号）、registration_authority（登记机关）、legal_representative（法定代表人）、address（地址）、mission（使命）、vision（愿景）、governance_structure（治理结构说明）
- **格式要求**：表格 + 段落。登记信息以表格呈现，使命愿景以段落阐述，治理结构说明治理架构（理事会/监事会/秘书处）
- **字数建议**：200–400 字（段落部分）
- **数据来源**：org_name, registration_number, registration_authority, legal_representative, address, mission, vision, governance_structure

**格式示例**

| 字段 | 内容 |
|------|------|
| 组织名称 | [org_name] |
| 登记证号 | [registration_number] |
| 登记机关 | [registration_authority] |
| 法定代表人 | [legal_representative] |
| 办公地址 | [address] |

**使命与愿景**

[mission]

[vision]

**治理结构**

[governance_structure]

---

### 第2章：年度工作概述
- **必含字段**：year（报告年份）、projects_summary（项目总览，列表）、total_beneficiaries（受益人次）、key_achievements（总体成果摘要）
- **格式要求**：段落 + 项目概况表格。先以2–3段概述全年工作，再以表格列出所有项目名称、执行状态、受益人次
- **字数建议**：300–500 字（段落部分）
- **数据来源**：year, projects_summary, total_beneficiaries, key_achievements

**格式示例**

[year] 年，[org_name] 共执行项目 [项目数量] 个，累计受益人次 [total_beneficiaries]。[key_achievements]

| 项目名称 | 执行状态 | 受益人次 |
|---------|---------|---------|
| [项目1] | 已结项 | [数量] |
| [项目2] | 执行中 | [数量] |

---

### 第3章：项目执行情况
- **必含字段**：projects_list（项目列表，每个项目含：project_name、project_period、funder、planned_indicators、actual_indicators、completion_rate、project_summary）
- **格式要求**：逐项目展开，每个项目独立小节，包含指标完成情况对照表（计划值 vs 实际值 vs 完成率）。completion_rate 低于 80% 时必须包含 deviation_reason
- **字数建议**：每个项目 200–400 字
- **数据来源**：projects_list[].project_name, projects_list[].project_period, projects_list[].funder, projects_list[].planned_indicators, projects_list[].actual_indicators, projects_list[].completion_rate, projects_list[].project_summary

**格式示例**

#### 3.1 [project_name]

**项目概况**：[project_summary]

**执行周期**：[project_period]  **资助方**：[funder]

| 指标名称 | 计划值 | 实际值 | 完成率 |
|---------|-------|-------|-------|
| [指标1] | [计划] | [实际] | [completion_rate]% |
| [指标2] | [计划] | [实际] | [completion_rate]% |

> 如完成率 < 80%，须在此说明原因：[deviation_reason]

---

### 第4章：财务概况
- **必含字段**：total_income（收入合计）、total_expenditure（支出合计）、year_end_balance（年末结余）、income_breakdown（收入结构分析，含各类型金额及占比）
- **格式要求**：收支总表（表格）+ 收入结构分析（表格 + 简短文字说明）。金额精确到元，百分比保留一位小数
- **字数建议**：表格为主，文字说明 100–200 字
- **数据来源**：total_income, total_expenditure, year_end_balance, income_breakdown

> **注意**：以下金额字段须填写实际数据，禁止由 AI 编造。

**格式示例**

**收支总表**

| 项目 | 金额（元） |
|------|----------|
| 收入合计 | [total_income] |
| 支出合计 | [total_expenditure] |
| 年末结余 | [year_end_balance] |

**收入结构**

| 收入类型 | 金额（元） | 占比 |
|---------|----------|------|
| [类型1] | [金额] | [占比]% |
| [类型2] | [金额] | [占比]% |

[income_breakdown 文字说明]

---

### 第5章：人员与志愿者
- **必含字段**：staff_fulltime（全职人数）、staff_parttime（兼职人数）、volunteer_count（志愿者人次）、volunteer_hours（志愿者服务时长，如有）
- **格式要求**：汇总表格 + 简短说明
- **字数建议**：100–200 字
- **数据来源**：staff_fulltime, staff_parttime, volunteer_count, volunteer_hours

**格式示例**

| 类别 | 数量 |
|------|------|
| 全职员工 | [staff_fulltime] 人 |
| 兼职员工 | [staff_parttime] 人 |
| 志愿者人次 | [volunteer_count] 人次 |
| 志愿服务时长 | [volunteer_hours] 小时 |

---

### 第6章：治理与内部管理
- **必含字段**：board_meetings（理事会会议次数）、supervisor_meetings（监事会会议次数，如有）、key_policies_implemented（年内执行的重要制度，列表）
- **格式要求**：列表 + 段落说明
- **字数建议**：150–300 字
- **数据来源**：board_meetings, supervisor_meetings, key_policies_implemented

**格式示例**

本年度，理事会共召开会议 [board_meetings] 次，监事会共召开会议 [supervisor_meetings] 次。

年内执行的重要制度：
- [制度1]
- [制度2]

[key_policies_implemented 说明]

---

### 第7章：面临的挑战与应对
- **必含字段**：challenges（面临的主要挑战，列表）、responses（应对措施，与挑战逐一对应）
- **格式要求**：逐条列举，每条挑战后跟对应的应对措施
- **字数建议**：200–400 字
- **数据来源**：challenges, responses

**格式示例**

**挑战1**：[challenge_1]

**应对**：[response_1]

**挑战2**：[challenge_2]

**应对**：[response_2]

---

### 第8章：下一年度工作计划
- **必含字段**：next_year_plans（下年度计划，含计划事项和预期目标，列表）
- **格式要求**：列表 + 简短说明，不得出现具体金额和尚未确认的数字
- **字数建议**：200–400 字
- **数据来源**：next_year_plans

> **注意**：未确认的资金来源、项目资助金额等不确定数据须使用占位符 `[请填写实际数据]`，禁止由 AI 编造。

**格式示例**

[next_year] 年，[org_name] 计划重点推进以下工作：

1. [计划事项1]：[预期目标1]
2. [计划事项2]：[预期目标2]

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
