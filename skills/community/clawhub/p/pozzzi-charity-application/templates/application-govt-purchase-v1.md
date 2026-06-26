---
source_url: ""
verified_date: 2026-03-30
next_review_date: 2026-06-30
version: 1
breaking_change: false
application_type: govt_purchase
funder_platform: government
---

# 政府购买服务申报书（服务方案）模板

> **使用说明**：本模板适用于民政局、妇联、教育局等政府部门的购买服务招标申报。正式公文体，语言风格比通用申报书更强调"符合政府采购要求"。
>
> **占位符说明**：所有资质证书编号、政府文件编号、银行账号等字段，本模板一律输出强制占位符（如 `[请填写登记证书编号]`），AI 不生成具体编号，提交前须由机构负责人手动填写。

## 章节结构

### 封面
- **必含字段**：org_name（投标机构名称）、tender_project_name（招标项目名称，与采购公告一致）、tender_code（招标公告编号，用户填写或占位符）、price_quote（报价，用户填写）、application_date（申报日期，系统生成）、ai_label（AI 标识声明，固定文本）
- **格式要求**：正式公文封面样式，居中排版，招标编号若用户未填写则输出占位符，报价金额精确到元，AI 标识声明置于封面底部
- **字数建议**：封面无正文段落
- **数据来源**：org_name, tender_project_name, tender_code, price_quote；application_date 系统注入；ai_label 固定文本

> **注意**：`tender_code` 若用户未填写，输出 `[请填写招标公告编号]` 占位符，禁止 AI 编造。`price_quote` 必须由用户填写，AI 不生成此数字。

**格式示例**

---

**[tender_project_name]**

**服务方案（投标/申报材料）**

投标机构：[org_name]

招标项目名称：[tender_project_name]

招标公告编号：[tender_code 或 [请填写招标公告编号]]

报价总额：[price_quote] 元（人民币）

申报日期：[application_date]

---

*本申报书由噗滋慈善 AI 助手辅助生成，请相关负责人对所有数据和内容进行核实后方可正式提交。*

---

### 目录
- **必含字段**：（自动生成，无变量输入）
- **格式要求**：列出一至八章及附录标题与对应页码占位符
- **数据来源**：（固定结构，无变量）

**格式示例**

一、机构基本情况…………………………[页码]

二、对采购需求的理解……………………[页码]

三、服务方案………………………………[页码]

四、工作计划与时间安排…………………[页码]

五、团队配置方案…………………………[页码]

六、绩效目标与考核方案…………………[页码]

七、报价明细………………………………[页码]

八、风险防控方案…………………………[页码]

附录：AI 辅助生成声明…………………[页码]

---

### 第一章：机构基本情况
- **必含字段**：org_name（机构全称）、org_type（机构类型）、org_registration_no（登记证号，用户填写或占位符）、govt_qualification_desc（参与政府购买服务资质说明）、org_background（执行能力简介）、org_past_project（相关历史项目主要业绩，如有）
- **格式要求**：登记注册情况以表格呈现，资质和业绩以段落阐述。所有证书编号使用占位符，章节末尾添加资质材料提交提醒
- **字数建议**：300–500 字（段落部分）
- **数据来源**：org_name, org_type, org_registration_no, govt_qualification_desc, org_background, org_past_project

> **注意**：以下字段若用户未填写具体编号，一律输出对应占位符，禁止 AI 编造：
> - 登记证号 → `[请填写登记证书编号]`
> - 其他资质证书编号 → `[请填写资质证书编号]`

**格式示例**

**一、登记注册情况**

| 字段 | 内容 |
|------|------|
| 机构全称 | [org_name] |
| 机构类型 | [org_type] |
| 登记证号 | [org_registration_no 或 [请填写登记证书编号]] |
| 登记机关 | [请填写登记机关名称] |
| 成立时间 | [请填写机构成立时间] |

**二、资质证明**

[govt_qualification_desc]

*以上资质信息请附原件扫描件作为附件，本方案中的编号占位符需在提交前替换为真实编号。*

**三、主要业绩**

[org_background]

（如 org_past_project 非空）[org_past_project]

---

### 第二章：对采购需求的理解
- **必含字段**：govt_dept_name（采购方政府部门全称）、tender_project_name（招标项目名称）、problem_statement（服务目标和问题分析，用户填写）、target_population（服务对象描述）、service_area（服务覆盖行政区划）
- **格式要求**：正式公文体，先阐述对采购需求的理解，再分析服务对象需求。语言风格须强调"符合政府采购要求"和"满足采购方目标"
- **字数建议**：400–600 字
- **数据来源**：govt_dept_name, tender_project_name, problem_statement, target_population, service_area

> **注意**：`problem_statement` 若含统计数字，提示用户确认来源，AI 不补充统计数据。

**格式示例**

本机构仔细研究了 [govt_dept_name] 发布的"[tender_project_name]"采购需求，对本次采购的服务目标和服务背景理解如下：

**服务目标理解**

[AI 基于 problem_statement 和 tender_project_name 组织，正式公文体，不补充用户未提供的数字]

**服务对象需求分析**

服务覆盖范围：[service_area]

服务对象：[target_population]

[AI 基于 problem_statement 分析服务对象需求，不编造统计数据]

---

### 第三章：服务方案
- **必含字段**：project_objectives（具体目标列表）、activities_design（主要活动列表，含名称、描述、频次）、project_goal（项目总体目标）
- **格式要求**：先陈述服务总体思路，再逐项描述服务内容、服务方式、服务流程。正式公文体
- **字数建议**：600–1000 字
- **数据来源**：project_goal, project_objectives[].description, project_objectives[].indicator, activities_design[].name, activities_design[].description, activities_design[].frequency, activities_design[].expected_participants

**格式示例**

**一、服务总体思路**

[AI 基于 project_goal 生成总体思路，正式公文体]

**二、服务内容**

1. [project_objectives[0].description]

**三、服务方式**

[AI 基于 activities_design 描述服务方式，不编造数据]

**四、服务流程**

**服务项目一：[activities_design[0].name]**

[activities_design[0].description]

执行频次：[activities_design[0].frequency]（预计每次服务人数：[activities_design[0].expected_participants] 人）

---

### 第四章：工作计划与时间安排
- **必含字段**：timeline（分阶段计划）、project_duration_months（项目总月数）、project_start_date（预计起始日期）
- **格式要求**：甘特图样式文字版，以表格列出各阶段起止时间和关键任务，正式公文体
- **字数建议**：表格为主，文字说明 100–200 字
- **数据来源**：timeline[].phase, timeline[].start_month, timeline[].end_month, timeline[].key_tasks, project_duration_months, project_start_date

**格式示例**

本机构计划自 [project_start_date] 正式开展服务，执行周期共 [project_duration_months] 个月，具体工作计划如下：

| 阶段 | 执行月份 | 关键工作内容 |
|------|---------|------------|
| [timeline[0].phase] | 第 [timeline[0].start_month]–[timeline[0].end_month] 月 | [timeline[0].key_tasks] |
| [timeline[1].phase] | 第 [timeline[1].start_month]–[timeline[1].end_month] 月 | [timeline[1].key_tasks] |

---

### 第五章：团队配置方案
- **必含字段**：team_composition（团队成员列表，含角色、背景、投入比例）、partner_orgs（合作机构，如有）、volunteer_plan（志愿者使用计划，如有）
- **格式要求**：以表格列出人员组成和职责分工，合作机构和志愿者计划以段落补充。禁止填写真实姓名。正式公文体
- **字数建议**：200–400 字
- **数据来源**：team_composition[].role, team_composition[].background, team_composition[].time_commitment, partner_orgs, volunteer_plan

> **注意**：`team_composition[].background` 禁止包含真实姓名、身份证号等 PII。检测到疑似中文姓名时提示用户使用职位描述代替（如"社会工作专业硕士，8年相关经验"）。

**格式示例**

**人员配置**

| 岗位 | 资质与背景 | 投入比例 |
|------|----------|---------|
| [team_composition[0].role] | [team_composition[0].background] | [team_composition[0].time_commitment] |
| [team_composition[1].role] | [team_composition[1].background] | [team_composition[1].time_commitment] |

（如 partner_orgs 非空）**合作机构**：[partner_orgs]

（如 volunteer_plan 非空）**志愿者配置**：[volunteer_plan]

---

### 第六章：绩效目标与考核方案
- **必含字段**：performance_indicators（绩效指标列表，与采购方要求对应，含指标名称、目标值、考核方式）、expected_outcomes（预期成效指标）
- **格式要求**：以表格列出绩效指标，严格对应用户填写的 `performance_indicators`，不自行添加指标。正式公文体
- **字数建议**：表格为主，文字说明 100–200 字
- **数据来源**：performance_indicators[].indicator, performance_indicators[].target, performance_indicators[].measurement, expected_outcomes[].outcome, expected_outcomes[].measurement_method

> **注意**：绩效目标章节严格对应用户填写的 `performance_indicators`，禁止 AI 自行添加或修改指标值。

**格式示例**

**一、绩效指标**

| 绩效指标 | 目标值 | 考核方式 |
|---------|-------|---------|
| [performance_indicators[0].indicator] | [performance_indicators[0].target] | [performance_indicators[0].measurement] |
| [performance_indicators[1].indicator] | [performance_indicators[1].target] | [performance_indicators[1].measurement] |

**二、预期成效**

| 成效指标 | 评估方式 |
|---------|---------|
| [expected_outcomes[0].outcome] | [expected_outcomes[0].measurement_method] |

---

### 第七章：报价明细
- **必含字段**：price_quote（报价总额，用户填写）、price_breakdown（报价明细说明，用户填写）、budget_breakdown（预算分项，用户填写）
- **格式要求**：汇总表格为主，正式公文体。所有金额须来自用户填写，AI 不生成金额
- **字数建议**：表格为主，说明 100–200 字
- **数据来源**：price_quote, price_breakdown, budget_breakdown[].category, budget_breakdown[].amount, budget_breakdown[].description, budget_breakdown[].percentage（系统计算）

> **注意**：`price_quote`、`price_breakdown`、`budget_breakdown[].amount` 均必须由用户填写，AI 不生成、推算或补充任何金额。若预算分项合计与总额不符（差异 > 1 元），系统阻断并提示用户确认。
>
> **银行账号等支付信息**：一律输出 `[请填写银行账号]`、`[请填写开户行名称]` 占位符，禁止 AI 编造。

**格式示例**

**报价汇总**

| 费用类别 | 金额（元） | 占比 | 费用说明 |
|---------|----------|------|---------|
| [budget_breakdown[0].category] | [budget_breakdown[0].amount] | [系统计算]% | [budget_breakdown[0].description] |
| [budget_breakdown[1].category] | [budget_breakdown[1].amount] | [系统计算]% | [budget_breakdown[1].description] |
| **报价合计** | **[price_quote]** | **100%** | |

**报价明细说明**

[price_breakdown]

**支付信息**（如采购方需要）

账户名称：[org_name]

银行账号：[请填写银行账号]

开户行：[请填写开户行名称]

---

### 第八章：风险防控方案
- **必含字段**：project_objectives（项目目标，用于推断潜在风险）、activities_design（活动设计，用于推断执行风险）
- **格式要求**：正式公文体，列出主要风险类别（执行风险、资金风险、政策风险等）及对应防控措施。AI 可基于项目类型生成常见风险框架，但具体数字（如风险发生概率）须由用户补充，禁止 AI 编造
- **字数建议**：300–500 字
- **数据来源**：project_objectives（参考用于推断风险），activities_design（参考用于推断风险）；AI 可基于 project_domain 生成通用风险框架

> **注意**：AI 可生成风险框架，但以下内容禁止由 AI 编造：
> - 具体事故发生概率或损失金额
> - 具体政策法规编号（输出 `[建议核查最新有效法规版本]` 标注）

**格式示例**

**一、执行风险与防控**

| 风险类型 | 风险描述 | 防控措施 |
|---------|---------|---------|
| 执行进度风险 | [AI 基于 activities_design 描述可能的进度风险] | [AI 生成常规防控措施] |
| 参与人数不足风险 | [AI 基于 target_count 和 activities_design 描述] | [AI 生成措施] |

**二、财务风险与防控**

| 风险类型 | 风险描述 | 防控措施 |
|---------|---------|---------|
| 预算超支风险 | [AI 生成常规描述] | [AI 生成措施] |

**三、政策与合规风险**

[AI 基于 project_domain 生成合规风险提示，政策法规引用标注"建议核查最新有效法规版本"]

---

### 附录：声明
- **必含内容**：AI 辅助生成声明 + 免责提示 + 生成时间戳 + 版本号 + 数据来源声明 + 占位符填写提醒
- **格式要求**：固定文本，置于服务方案末尾，不可删改。占位符提醒为本模板专属附加项
- **数据来源**：（固定文本，生成时间戳和版本号由系统注入）

**格式示例**

---

**AI 辅助生成声明**

本申报书由噗滋慈善 AI 助手辅助生成，请相关负责人对所有数据和内容进行核实后方可正式提交。

**免责提示**

AI 生成，仅供参考，请核实数据。本申报书内容不构成法律或财务意见，所有数字和事实须以组织实际记录为准。

**数据来源声明**

以下申报内容来源于机构填报信息，噗滋不对数据真实性负责。

**占位符填写提醒**

提交前请务必将以下占位符替换为真实信息：
- `[请填写登记证书编号]` → 替换为实际登记证书编号
- `[请填写招标公告编号]` → 替换为采购公告上的编号
- `[请填写资质证书编号]` → 替换为实际资质证书编号
- `[请填写银行账号]` → 替换为机构对公账户账号
- `[请填写开户行名称]` → 替换为实际开户行名称
- `[请填写登记机关名称]` → 替换为民政局等登记机关全称
- 其他 `[请填写...]` 格式的占位符

*提交前请将资质证明文件扫描件作为附件随本方案一并提交。*

**版本信息**

草稿 [版本号]（生成于 [生成时间戳 UTC+8]）
