---
source_url: https://gongyi.qq.com/
verified_date: 2026-03-30
next_review_date: 2026-06-30
version: 1
breaking_change: false
application_type: tencent99
funder_platform: tencent_gongyi
---

# 腾讯公益 99 公益日项目申报书模板

> **平台版本说明**：本模板格式参照腾讯公益 2026 年项目申报指引（模板版本 v1.0）。如平台要求有更新，请以平台官方最新要求为准。

## 章节结构

### 封面
- **必含字段**：project_name（项目名称）、org_name（申报机构）、tencent_project_category（腾讯公益项目分类标签）、tencent_fundraising_goal（申请筹款金额，用户填写）、application_date（申报日期，系统生成）、ai_label（AI 标识声明，固定文本）
- **格式要求**：居中排版，分类标签以标签样式标注，筹款目标金额精确到元，AI 标识声明置于封面底部
- **字数建议**：封面无正文段落
- **数据来源**：project_name, org_name, tencent_project_category, tencent_fundraising_goal；application_date 系统注入；ai_label 固定文本

> **注意**：`tencent_fundraising_goal` 必须由用户填写，AI 不生成此数字。

**格式示例**

---

**[project_name]**

**腾讯公益 99 公益日项目申报书**

申报机构：[org_name]

项目分类：[tencent_project_category]

申请筹款金额：[tencent_fundraising_goal] 元

申报日期：[application_date]

腾讯公益机构编号：[tencent_org_id 或 [请填写腾讯公益机构编号]]

---

*本申报书由噗滋慈善 AI 助手辅助生成，请相关负责人对所有数据和内容进行核实后方可正式提交。*

---

### 目录
- **必含字段**：（自动生成，无变量输入）
- **格式要求**：列出一至八章及附录标题与对应页码占位符
- **数据来源**：（固定结构，无变量）

**格式示例**

一、机构信息…………………………………[页码]

二、项目简介…………………………………[页码]

三、项目背景与问题…………………………[页码]

四、项目内容…………………………………[页码]

五、执行团队与机构能力……………………[页码]

六、预期成效…………………………………[页码]

七、资金使用计划……………………………[页码]

八、往年执行情况……………………………[页码]

附录：AI 辅助生成声明……………………[页码]

---

### 第一章：机构信息
- **必含字段**：org_name（机构全称）、org_type（机构类型）、org_registration_no（登记证号，若有；否则占位符）、tencent_org_id（腾讯公益机构编号，若有；否则占位符）、org_background（执行能力简介）
- **格式要求**：基本信息以表格呈现，执行能力以段落阐述
- **字数建议**：200–400 字（段落部分）
- **数据来源**：org_name, org_type, org_registration_no, tencent_org_id, org_background

> **注意**：`org_registration_no` 和 `tencent_org_id` 若用户未填写，分别输出 `[请填写登记证书编号]` 和 `[请填写腾讯公益机构编号]` 占位符，禁止 AI 编造。

**格式示例**

| 字段 | 内容 |
|------|------|
| 机构全称 | [org_name] |
| 机构类型 | [org_type] |
| 登记证号 | [org_registration_no 或占位符] |
| 腾讯公益机构编号 | [tencent_org_id 或占位符] |

**机构执行能力**

[org_background]

---

### 第二章：项目简介（公众版，面向捐赠人）
- **必含字段**：target_population（目标受益群体）、target_count（预计受益人次）、project_goal（项目总体目标）
- **格式要求**：面向捐赠人的吸引力叙述，语言温暖、简洁易懂，不超过 150 字（腾讯公益平台显示限制）。禁止编造受益人故事，只基于用户填写的群体特征和项目目标生成描述，禁止出现个体受益人信息
- **字数建议**：严格不超过 150 字（超出自动截断并提示用户）
- **数据来源**：target_population, target_count, project_goal

> **注意**：本章节使用温暖叙事 Prompt 策略，但有以下严格约束：
> 1. 禁止编造受益人个体故事（如"小明今年8岁..."）
> 2. 只允许基于 `target_population` 和 `target_count` 进行群体描述
> 3. 输出超过 150 字时系统自动截断并提示用户人工修改
> 4. 禁止包含任何个体受益人信息（PII 合规红线）

**格式示例**

（AI 基于 target_population、target_count、project_goal 生成，不超过 150 字，温暖叙事风格，描述群体困境与项目价值，不提及具体个人）

---

### 第三章：项目背景与问题
- **必含字段**：problem_statement（社会问题描述，用户填写）、target_population（目标受益群体）、needs_data_source（需求数据来源，如有）
- **格式要求**：段落叙述，先陈述社会问题，再描述目标群体需求。problem_statement 中统计数字不得由 AI 补充
- **字数建议**：400–600 字
- **数据来源**：problem_statement, target_population, needs_data_source

> **注意**：`problem_statement` 中若含统计数字，在生成前提示用户确认数据来源，要求填写 `needs_data_source`。AI 不补充或修改用户未提供的统计数据。

**格式示例**

**社会需求陈述**

[problem_statement]

（如 needs_data_source 非空）数据来源：[needs_data_source]

**目标群体**

[target_population]

---

### 第四章：项目内容
- **必含字段**：project_objectives（具体目标列表，含描述和指标）、activities_design（主要活动列表，含名称、描述、频次）、timeline（项目时间表）、project_duration_months（总月数）、project_start_date（预计起始日期）
- **格式要求**：先列出具体目标和活动设计，再以表格呈现项目时间安排
- **字数建议**：500–800 字
- **数据来源**：project_objectives[].description, project_objectives[].indicator, activities_design[].name, activities_design[].description, activities_design[].frequency, timeline[].phase, timeline[].start_month, timeline[].end_month, timeline[].key_tasks

**格式示例**

**具体目标**

1. [project_objectives[0].description]（考核指标：[project_objectives[0].indicator]）
2. [project_objectives[1].description]（考核指标：[project_objectives[1].indicator]）

**主要活动**

**活动1：[activities_design[0].name]**

[activities_design[0].description]（频次：[activities_design[0].frequency]）

**执行计划**

项目预计自 [project_start_date] 启动，执行周期 [project_duration_months] 个月。

| 阶段 | 执行月份 | 关键任务 |
|------|---------|---------|
| [timeline[0].phase] | 第 [timeline[0].start_month]–[timeline[0].end_month] 月 | [timeline[0].key_tasks] |

---

### 第五章：执行团队与机构能力
- **必含字段**：team_composition（团队成员列表，含角色、背景、投入比例）、partner_orgs（合作机构，如有）、org_past_project（相关历史项目成效，如有）
- **格式要求**：以表格列出团队组成，段落补充合作机构和历史成效。禁止填写真实姓名
- **字数建议**：200–400 字
- **数据来源**：team_composition[].role, team_composition[].background, team_composition[].time_commitment, partner_orgs, org_past_project

> **注意**：`team_composition[].background` 禁止包含真实姓名等 PII。检测到疑似中文姓名时提示用户使用职位描述代替。

**格式示例**

| 角色 | 背景 | 投入比例 |
|------|------|---------|
| [team_composition[0].role] | [team_composition[0].background] | [team_composition[0].time_commitment] |

（如 partner_orgs 非空）**合作机构**：[partner_orgs]

（如 org_past_project 非空）**历史执行能力**：[org_past_project]

---

### 第六章：预期成效
- **必含字段**：expected_outcomes（预期成效指标，含描述和测量方法）、target_count（预计受益人次）、social_impact_narrative（社会影响叙述，如有）
- **格式要求**：以表格列出量化指标和评估方式，段落补充社会影响。AI 可辅助润色叙述，但量化数字须来源于用户填写字段
- **字数建议**：300–500 字
- **数据来源**：expected_outcomes[].outcome, expected_outcomes[].measurement_method, target_count, social_impact_narrative

**格式示例**

| 成效指标 | 评估方式 |
|---------|---------|
| [expected_outcomes[0].outcome] | [expected_outcomes[0].measurement_method] |

（如 social_impact_narrative 非空）**社会影响**

[social_impact_narrative]

---

### 第七章：资金使用计划
- **必含字段**：tencent_fundraising_goal（筹款目标，用户填写）、donation_use_description（捐款用途说明，面向捐赠人）、unit_cost_description（单位成本说明，用户填写，若有）、budget_breakdown（预算分项明细，用户填写）、total_budget（总预算，用户填写）、has_matching_fund（是否有配套资金）
- **格式要求**：先展示面向捐赠人的用途说明，再以表格呈现预算明细。所有金额字段须来自用户填写，AI 不生成金额
- **字数建议**：表格为主，用途说明 100–200 字
- **数据来源**：tencent_fundraising_goal, donation_use_description, unit_cost_description, budget_breakdown[].category, budget_breakdown[].amount, budget_breakdown[].description, budget_breakdown[].percentage（系统计算）, total_budget, matching_fund_amount, matching_fund_source

> **注意**：
> - `tencent_fundraising_goal`、`total_budget`、`budget_breakdown[].amount` 均必须由用户填写，AI 不生成、推算或补充任何金额
> - `unit_cost_description` 中的金额数字若含 AI 无法确认来源的数字，提示用户确认
> - `donation_use_description` 面向公众捐赠人，禁止包含任何受益人个体信息，只允许群体描述

**格式示例**

**捐款用途说明**（面向捐赠人）

[donation_use_description]

（如 unit_cost_description 非空）**单位成本说明**：[unit_cost_description]

**预算明细**

| 费用类别 | 金额（元） | 占比 | 费用说明 |
|---------|----------|------|---------|
| [budget_breakdown[0].category] | [budget_breakdown[0].amount] | [系统计算]% | [budget_breakdown[0].description] |
| **合计** | **[total_budget]** | **100%** | |

99 公益日目标筹款金额：[tencent_fundraising_goal] 元

（如 has_matching_fund = true）配套资金：[matching_fund_amount] 元，来源：[matching_fund_source]

---

### 第八章：往年执行情况
- **必含字段**：has_previous_99_project（是否有往年99公益日经验）、previous_99_outcome（往年核心成效，条件必填）
- **格式要求**：若有往年经验，段落叙述核心成效数据；若无，说明本次为首次申报
- **字数建议**：100–300 字
- **数据来源**：has_previous_99_project, previous_99_outcome

**格式示例**

（has_previous_99_project = true）

本机构曾参与往年腾讯公益 99 公益日项目，核心成效如下：

[previous_99_outcome]

（has_previous_99_project = false）

本次为本机构首次申报腾讯公益 99 公益日项目。[请填写其他可证明机构执行能力的项目经验]

---

### 附录：声明
- **必含内容**：AI 辅助生成声明 + 免责提示 + 生成时间戳 + 版本号 + 数据来源声明
- **格式要求**：固定文本，置于申报书末尾，不可删改
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
