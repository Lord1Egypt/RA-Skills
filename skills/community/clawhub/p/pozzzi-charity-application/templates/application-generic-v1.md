---
source_url: ""
verified_date: 2026-03-30
next_review_date: 2026-06-30
version: 1
breaking_change: false
application_type: generic
funder_platform: generic
---

# 通用公益项目申请书模板

## 章节结构

### 封面
- **必含字段**：project_name（项目名称）、org_name（申报机构）、application_date（申报日期，系统自动生成）、total_budget（申请金额，用户填写）、ai_label（AI 标识声明，固定文本）
- **格式要求**：居中排版，申请金额金额精确到元，AI 标识声明置于封面底部
- **字数建议**：封面无正文段落
- **数据来源**：project_name, org_name, total_budget；application_date 由系统注入；ai_label 固定文本

> **注意**：`total_budget` 必须由用户填写，AI 不生成此数字。

**格式示例**

---

**[project_name]**

**项目申请书**

申报机构：[org_name]

申报日期：[application_date]

申请金额：[total_budget] 元

---

*本申报书由噗滋慈善 AI 助手辅助生成，请相关负责人对所有数据和内容进行核实后方可正式提交。*

---

### 目录
- **必含字段**：（自动生成，无变量输入）
- **格式要求**：列出一至八章及附录的标题与对应页码占位符
- **字数建议**：目录条目即可，无正文
- **数据来源**：（固定结构，无变量）

**格式示例**

一、机构基本信息…………………………………[页码]

二、项目背景与需求分析…………………………[页码]

三、项目设计方案…………………………………[页码]

四、项目时间表……………………………………[页码]

五、项目团队………………………………………[页码]

六、预期成效与评估方案…………………………[页码]

七、项目预算………………………………………[页码]

八、项目可持续性…………………………………[页码]

附录：AI 辅助生成声明…………………………[页码]

---

### 第一章：机构基本信息
- **必含字段**：org_name（机构全称）、org_type（机构类型）、org_registration_no（登记证号，若有；否则输出占位符）、org_background（执行能力简介）、org_past_project（相关历史项目成效，如有）
- **格式要求**：登记信息以表格呈现，执行能力以段落阐述，历史项目以简短条目列举
- **字数建议**：300–500 字（段落部分）
- **数据来源**：org_name, org_type, org_registration_no, org_background, org_past_project

> **注意**：`org_registration_no` 若用户未填写，输出 `[请填写登记证书编号]` 占位符，禁止 AI 编造。

**格式示例**

| 字段 | 内容 |
|------|------|
| 机构全称 | [org_name] |
| 机构类型 | [org_type] |
| 登记证号 | [org_registration_no 或占位符] |

**执行能力简介**

[org_background]

**相关历史项目成效**

[org_past_project（如有，列举1-3条；无则省略本节）]

---

### 第二章：项目背景与需求分析
- **必含字段**：problem_statement（社会问题描述，用户填写）、target_population（目标受益群体描述）、target_count（预计直接受益人次）、needs_data_source（需求数据来源，如有）
- **格式要求**：段落叙述，先陈述社会问题，再描述目标群体，最后说明需求证据。problem_statement 中的统计数字不得由 AI 补充，须来自用户填写
- **字数建议**：400–700 字
- **数据来源**：problem_statement, target_population, target_count, needs_data_source

> **注意**：`problem_statement` 中若含统计数字（如"XX万人""XX%"），在生成前提示用户确认数据来源，并要求填写 `needs_data_source`。AI 不补充或修改用户未提供的统计数据。

**格式示例**

**一、社会问题陈述**

[problem_statement]

（如 needs_data_source 非空）数据来源：[needs_data_source]

**二、目标受益群体**

本项目面向 [target_population]，预计直接受益人数为 [target_count] 人次。

**三、需求分析**

（基于用户填写的 problem_statement 和 target_population，AI 辅助组织逻辑，不补充新的数字或统计数据）

---

### 第三章：项目设计方案
- **必含字段**：project_goal（项目总体目标）、project_objectives（具体目标列表，含描述和可量化指标）、activities_design（主要活动列表，含名称、描述、频次、预计参与人数）
- **格式要求**：先陈述总体目标（段落），再以编号列出具体目标及对应指标（列表），最后逐一描述主要活动（子小节）
- **字数建议**：500–900 字
- **数据来源**：project_goal, project_objectives[].description, project_objectives[].indicator, activities_design[].name, activities_design[].description, activities_design[].frequency, activities_design[].expected_participants

**格式示例**

**一、项目总体目标**

[project_goal]

**二、具体目标**

1. [project_objectives[0].description]
   - 考核指标：[project_objectives[0].indicator]
2. [project_objectives[1].description]
   - 考核指标：[project_objectives[1].indicator]

**三、主要活动设计**

**活动1：[activities_design[0].name]**

[activities_design[0].description]

执行频次：[activities_design[0].frequency]（预计每次参与人数：[activities_design[0].expected_participants] 人）

---

### 第四章：项目时间表
- **必含字段**：timeline（分阶段计划，含阶段名称、起止月份、关键任务）、project_duration_months（项目总月数）、project_start_date（预计起始日期）
- **格式要求**：甘特图样式文字版，以表格列出各阶段起止时间和关键任务；阶段划分须连贯，不得有空缺月份
- **字数建议**：表格为主，文字说明 100–200 字
- **数据来源**：timeline[].phase, timeline[].start_month, timeline[].end_month, timeline[].key_tasks, project_duration_months, project_start_date

**格式示例**

项目预计自 [project_start_date] 启动，执行周期共 [project_duration_months] 个月。

| 阶段 | 执行月份 | 关键任务 |
|------|---------|---------|
| [timeline[0].phase] | 第 [timeline[0].start_month]–[timeline[0].end_month] 月 | [timeline[0].key_tasks] |
| [timeline[1].phase] | 第 [timeline[1].start_month]–[timeline[1].end_month] 月 | [timeline[1].key_tasks] |

---

### 第五章：项目团队
- **必含字段**：team_composition（团队成员列表，含角色、背景、投入比例）、partner_orgs（合作机构，如有）、volunteer_plan（志愿者计划，如有）
- **格式要求**：以表格列出团队成员角色和背景，合作机构和志愿者计划以段落补充说明。禁止填写真实姓名
- **字数建议**：200–400 字
- **数据来源**：team_composition[].role, team_composition[].background, team_composition[].time_commitment, partner_orgs, volunteer_plan

> **注意**：`team_composition[].background` 禁止包含真实姓名、身份证号、联系方式等个人信息。若检测到疑似中文姓名，提示用户使用职位描述代替。

**格式示例**

| 角色 | 背景 | 投入比例 |
|------|------|---------|
| [team_composition[0].role] | [team_composition[0].background] | [team_composition[0].time_commitment] |
| [team_composition[1].role] | [team_composition[1].background] | [team_composition[1].time_commitment] |

（如 partner_orgs 非空）**合作机构**：[partner_orgs]

（如 volunteer_plan 非空）**志愿者计划**：[volunteer_plan]

---

### 第六章：预期成效与评估方案
- **必含字段**：expected_outcomes（预期成效指标列表，含成效描述和测量方法）、social_impact_narrative（社会影响叙述，如有）
- **格式要求**：以表格列出量化指标和评估方法，再以段落补充社会影响叙述。AI 可辅助润色叙述，但量化数字须来源于用户填写的字段
- **字数建议**：300–500 字
- **数据来源**：expected_outcomes[].outcome, expected_outcomes[].measurement_method, social_impact_narrative

**格式示例**

| 成效指标 | 目标值 | 评估方式 |
|---------|-------|---------|
| [expected_outcomes[0].outcome] | （含于指标描述中） | [expected_outcomes[0].measurement_method] |
| [expected_outcomes[1].outcome] | （含于指标描述中） | [expected_outcomes[1].measurement_method] |

（如 social_impact_narrative 非空）**社会影响**

[social_impact_narrative（AI 可辅助润色，但不补充新数字）]

---

### 第七章：项目预算
- **必含字段**：total_budget（申请资金总额，用户填写）、budget_breakdown（预算分项明细，含费用类别、金额、说明，用户填写）、has_matching_fund（是否有配套资金）、matching_fund_amount（配套金额，条件必填）、matching_fund_source（配套来源，条件必填）
- **格式要求**：预算汇总表（表格）+ 说明段落。金额精确到元，百分比保留一位小数。所有金额字段须来自用户填写，禁止 AI 生成或推算
- **字数建议**：表格为主，文字说明 100–200 字
- **数据来源**：total_budget, budget_breakdown[].category, budget_breakdown[].amount, budget_breakdown[].description, budget_breakdown[].percentage（系统计算）, has_matching_fund, matching_fund_amount, matching_fund_source

> **注意**：`total_budget` 和 `budget_breakdown[].amount` 必须由用户填写，AI 不生成、推算或补充任何预算金额。若预算分项合计与总额不符（差异 > 1 元），系统阻断并提示用户确认。

**格式示例**

**预算汇总**

| 费用类别 | 金额（元） | 占比 | 费用说明 |
|---------|----------|------|---------|
| [budget_breakdown[0].category] | [budget_breakdown[0].amount] | [系统计算百分比]% | [budget_breakdown[0].description] |
| [budget_breakdown[1].category] | [budget_breakdown[1].amount] | [系统计算百分比]% | [budget_breakdown[1].description] |
| **合计** | **[total_budget]** | **100%** | |

（如 has_matching_fund = true）**配套资金**：[matching_fund_amount] 元，来源：[matching_fund_source]

---

### 第八章：项目可持续性
- **必含字段**：sustainability_plan（项目可持续性说明，如有）
- **格式要求**：段落叙述，说明项目结束后的影响持续方案（如成果移交、社区自主运营、后续资金来源等）。若用户未填写，输出提示占位符
- **字数建议**：150–300 字
- **数据来源**：sustainability_plan

> **注意**：若 `sustainability_plan` 为空，输出 `[请填写项目可持续性说明]` 占位符，禁止 AI 自行编写。

**格式示例**

[sustainability_plan（如有）]

（若 sustainability_plan 为空）[请填写项目可持续性说明]

---

### 附录：声明
- **必含内容**：AI 辅助生成声明 + 免责提示 + 生成时间戳 + 版本号 + 数据来源声明
- **格式要求**：固定文本，置于申请书末尾，不可删改
- **数据来源**：（固定文本，生成时间戳和版本号由系统注入）

**格式示例**

---

**AI 辅助生成声明**

本申报书由噗滋慈善 AI 助手辅助生成，请相关负责人对所有数据和内容进行核实后方可正式提交。

**免责提示**

AI 生成，仅供参考，请核实数据。本申报书内容不构成法律或财务意见，所有数字和事实须以组织实际记录为准。

**数据来源声明**

以下申报内容来源于机构填报信息，噗滋不对数据真实性负责。

**版本信息**

草稿 [版本号]（生成于 [生成时间戳 UTC+8]）
