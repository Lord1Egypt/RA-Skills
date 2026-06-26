---
source_url: https://www.mca.gov.cn/article/yw/hjzcbz/2017/201710/20171000006382.shtml
verified_date: 2026-03-30
next_review_date: 2026-06-30
version: 1
breaking_change: false
report_type: finance_final
funder_platform: generic
---

# 项目财务决算报告模板

## 章节结构

### 第1章：项目收支概况
- **必含字段**：project_name（项目名称）、org_name（执行机构）、funder（资助方）、total_grant（资助总额）、total_expenditure（实际支出合计）、unexpended_balance（未支出结余）、report_period（决算报告期）
- **格式要求**：汇总表格，字段名与值两列，金额精确到分（保留2位小数）
- **字数建议**：表格为主，无需段落
- **数据来源**：project_name, org_name, funder, total_grant, total_expenditure, unexpended_balance, report_period

> **注意**：以下所有金额须填写实际数据，禁止由 AI 编造。unexpended_balance = total_grant - total_expenditure，须与实际账目一致。

**格式示例**

| 字段 | 金额（元） |
|------|----------|
| 资助总额 | [total_grant] |
| 实际支出合计 | [total_expenditure] |
| 未支出结余 | [unexpended_balance] |

| 字段 | 内容 |
|------|------|
| 项目名称 | [project_name] |
| 执行机构 | [org_name] |
| 资助方 | [funder] |
| 决算报告期 | [report_period] |

---

### 第2章：支出明细与预算对比
- **必含字段**：budget_lines（预算行列表，每条含：line_no、category、budgeted、actual、variance_amount、variance_rate）。variance_rate 绝对值 > 10% 时，该行必须填写 variance_reason
- **格式要求**：逐行对比表，列：序号 / 支出类别 / 预算金额 / 实际支出 / 差异金额 / 差异率 / 差异说明。差异 > ±10% 的行必须在"差异说明"列填写 variance_reason。合计行加粗
- **字数建议**：表格为主，整体执行情况说明 100–200 字
- **数据来源**：budget_lines[].line_no, budget_lines[].category, budget_lines[].budgeted, budget_lines[].actual, budget_lines[].variance_amount, budget_lines[].variance_rate, budget_lines[].variance_reason（当 |variance_rate| > 10%）

> **注意**：差异率 = (实际支出 - 预算金额) / 预算金额 × 100%。差异金额 = 实际支出 - 预算金额。所有金额须精确到分。

**格式示例**

| 序号 | 支出类别 | 预算金额（元） | 实际支出（元） | 差异金额（元） | 差异率 | 差异说明 |
|-----|---------|-------------|-------------|-------------|------|---------|
| 1 | [类别1] | [预算] | [实际] | [差异] | [variance_rate]% | |
| 2 | [类别2] | [预算] | [实际] | [差异] | [variance_rate]% | [variance_reason（差异>±10%时必填）] |
| **合计** | | **[预算合计]** | **[实际合计]** | **[差异合计]** | | |

[整体财务执行情况说明]

---

### 第3章：结余资金处理说明
- **必含字段**：unexpended_balance（未支出结余）、balance_ratio（结余率 = unexpended_balance / total_grant × 100%）。当 balance_ratio > 1% 时，必须填写 balance_handling（结余资金处置方式：退还资助方 / 按协议转入下期 / 其他）和 balance_handling_desc（详细说明）
- **格式要求**：若无结余或结余 ≤ 1%，本章注明"项目结余金额为 [unexpended_balance] 元，结余率 [balance_ratio]%，无需单独说明"即可。结余 > 1% 时，段落说明处置方式和依据
- **字数建议**：无结余时1行，有结余时 100–200 字
- **数据来源**：unexpended_balance, balance_ratio, balance_handling（当 balance_ratio > 1%）, balance_handling_desc（当 balance_ratio > 1%）

**格式示例（结余 > 1% 时）**

本项目结余资金 [unexpended_balance] 元，结余率 [balance_ratio]%。

处置方式：[balance_handling]

[balance_handling_desc]

**格式示例（结余 ≤ 1% 时）**

本项目结余金额为 [unexpended_balance] 元，结余率 [balance_ratio]%，无需单独说明。

---

### 第4章：发票与凭证说明
- **必含字段**：invoice_count（发票/凭证张数）、invoice_total（发票金额合计）、invoice_notes（特殊凭证说明，如有无票支出须在此说明原因及金额）
- **格式要求**：简短段落 + 凭证汇总表（如有特殊凭证则逐条说明）
- **字数建议**：100–200 字
- **数据来源**：invoice_count, invoice_total, invoice_notes

> **注意**：invoice_total 须与第2章实际支出合计一致（或附差异说明），禁止由 AI 编造。

**格式示例**

本项目共取得发票及凭证 [invoice_count] 张，凭证金额合计 [invoice_total] 元。

[invoice_notes（如有无票支出或特殊凭证，在此说明）]

---

### 附：审计意见栏（留白）
- **必含内容**：审计意见留白区域，供外部审计机构或资助方填写
- **格式要求**：留白方框，标注"（此处留白，供审计机构填写意见）"
- **数据来源**：（无变量，固定留白）

**格式示例**

**审计意见**

（此处留白，供审计机构填写意见）

签名：＿＿＿＿＿＿＿＿　　日期：＿＿＿＿年＿＿月＿＿日

---

### 附录：声明
- **必含内容**：AI 辅助生成声明 + 免责提示
- **格式要求**：固定文本，置于报告末尾，不可删改
- **数据来源**：（固定文本，无变量）

**格式示例**

---

**AI 辅助生成声明**

本报告由 AI 辅助生成，最终内容经人工审核确认。请在正式提交前核实所有财务数据的准确性，并与组织实际账目核对一致。

**免责提示**

AI 生成，仅供参考，请核实数据。本报告内容不构成审计意见，所有金额和凭证须以组织实际财务记录为准。
