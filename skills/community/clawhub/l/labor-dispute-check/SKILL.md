---
name: labor-dispute-check
description: Check common China labor dispute issues and estimate employee rights
version: 1.2.0
tags: legal, labor-law, china, rights, dispute, employment, evidence, arbitration
---

# Labor Dispute Check

Check common China labor dispute issues and estimate employee rights. Use for 劳动纠纷, 被辞退赔偿, 违法解除, N+1, 2N, 加班费计算, 试用期规定, 未签劳动合同, 劳动仲裁, 经济补偿, severance, overtime pay, probation rules, and evidence preparation.

## Usage Scenarios

### Scenario 1: Termination Severance Calculation
**User input:** "工作3年被辞退，公司说我不符合要求，能赔多少钱？"
**Expected output:** The skill identifies the issue type (termination & severance), gathers facts (city, start date, end date, monthly wage, termination reason, notice status), checks applicable labor law rules, and calculates: economic compensation estimate (years × monthly wage base), distinguishes N+1 vs 2N scenarios based on whether termination was lawful, explains the difference, and provides evidence checklist and arbitration timeline.

### Scenario 2: Overtime Pay Calculation
**User input:** "平时加班和周末加班没有加班费，我能要回来吗？怎么算？"
**Expected output:** The skill identifies the issue type (overtime pay), asks for missing facts (overtime dates, hours, whether rest was arranged, monthly wage base), applies labor law rates (standard overtime 150%, rest day 200%, holiday 300%), computes estimate, explains the monthly cap of 36 hours, provides evidence requirements (attendance records, chat records, payslips), and notes the 1-year arbitration deadline.

### Scenario 3: Probation Period Legality Check
**User input:** "试用期6个月合法吗？签了3年合同"
**Expected output:** The skill checks contract length (3 years) against maximum probation rules: 3-year contract permits max 6 months probation. Confirms the probation period is legal. Notes that wages during probation must be at least 80% of agreed wage or minimum wage, whichever is higher. Also checks: only one probation period allowed for the same position, and probation must be included in the contract term. Suggests next steps if any violation is found.

## Overview

This skill helps employees and employers check common labor law issues, calculate rights and obligations, and understand dispute resolution options. It provides quick assessments of labor situations based on Chinese labor law provisions.

**⚠️ Important Disclaimer**: This tool provides informational assistance only. It does not constitute legal advice, nor does it guarantee any particular outcome. Always consult a qualified labor attorney or the local labor bureau for specific disputes.

## High-Intent Questions

Use this skill when the user asks:

- 公司辞退我应该赔多少钱
- N+1 和 2N 怎么算
- 试用期被辞退有没有赔偿
- 加班费、周末加班、法定节假日加班怎么算
- 没签劳动合同怎么办
- 劳动仲裁需要准备哪些证据
- 被迫离职、调岗降薪、拖欠工资怎么处理
- Is my termination legal under China labor law?

## When to Use This Skill

- Checking if termination was lawful
- Calculating severance/economic compensation
- Understanding overtime pay entitlements
- Verifying probation period rules
- Reviewing labor contract terms
- Assessing labor dispute options

## Limitations

- Based on general Chinese labor law principles
- May not reflect local regulations or specific circumstances
- Cannot assess case merits or predict outcomes
- Not a substitute for professional legal advice
- Calculations are estimates only

## Workflow

1. **Identify issue type** — Determine the labor concern
2. **Gather facts** — Collect relevant dates, amounts, terms
3. **Check rules** — Apply labor law provisions
4. **Calculate rights** — Compute entitlements if applicable
5. **Build evidence pack** — Turn available materials into a usable proof list
6. **Suggest options** — Recommend next steps

Read `references/evidence-pack.md` when the user asks "我要准备什么证据", "怎么仲裁", or "材料够不够".

## Fact Checklist

Ask only for missing facts that affect the estimate:

- City or province, because local implementation may vary
- Start date, end date, and contract term
- Monthly wage base and whether bonuses/allowances are included
- Termination reason and whether there was written notice
- Probation status and contract length
- Overtime dates, hours, and whether rest was arranged
- Evidence available: contract, payslips, attendance records, chat records, termination notice

## Evidence Pack Output

When facts are enough, provide:

1. `Claim type`: termination, overtime, unpaid wage, probation, contract, social insurance, or mixed.
2. `Core facts to prove`: employment relationship, wage base, dates, employer action, employee response.
3. `Evidence already mentioned`: classify as strong, medium, weak, or missing.
4. `Evidence to preserve now`: screenshots, exports, paper copies, originals, witness notes.
5. `Calculation table`: formula, assumptions, and missing variables.
6. `Arbitration package outline`: claims, facts, evidence list, timeline, and risk notes.

Do not tell the user to fabricate, alter, or secretly obtain unlawful evidence.

## Common Labor Issues

### 1. Termination & Severance
- **Lawful termination**: Employee fault, mutual agreement, operational reasons
- **Unlawful termination**: No valid reason, improper procedure
- **Economic compensation**: N+1 or 2N depending on circumstances
- **Notice period**: 30 days or payment in lieu

### 2. Overtime Pay
- **Standard overtime**: 150% of hourly rate
- **Rest day overtime**: 200% (or time off)
- **Holiday overtime**: 300%
- **Monthly cap**: 36 hours maximum

### 3. Probation Period
- **3-month contract**: Max 1 month probation
- **1-year contract**: Max 2 months probation
- **3-year+ contract**: Max 6 months probation
- **Same position**: Only one probation period allowed

### 4. Labor Contract
- **Required elements**: Parties, position, compensation, term
- **Written contract**: Required within 1 month of start
- **Fixed term**: Can renew but watch for indefinite term rules
- **Indefinite term**: After 2 consecutive fixed terms or 10 years

## Usage

### Basic Check
```
"被辞退怎么赔偿"
"加班费怎么算"
"试用期规定"
"劳动纠纷咨询"
```

### With Context
```
"工作3年被辞退，赔偿多少"
"试用期6个月合法吗"
"加班没有加班费怎么办"
```

## Output Format

For each inquiry:
- **Issue summary**: What law applies
- **Rights calculation**: Estimated entitlements
- **Key deadlines**: Statute of limitations
- **Suggested actions**: Next steps
- **Disclaimer**: Consult professional advice

Use this structure for Chinese user questions:

1. 初步判断
2. 需要补充的关键事实
3. 赔偿/加班费估算公式
4. 证据清单
5. 劳动仲裁时限和下一步
6. 风险与免责声明

## Calculation Helpers

If enough facts are available:

- Economic compensation estimate: working years x monthly wage base
- Payment in lieu of notice: usually one additional monthly wage when applicable
- Unlawful termination risk: explain why 2N may be discussed, but do not promise outcome
- Overtime estimate: distinguish workday, rest day, and statutory holiday rates
- Probation check: compare contract length against maximum probation period

## References

For detailed labor law guidance:
- [references/api_reference.md](references/api_reference.md) — Local helper function reference
- [references/evidence-pack.md](references/evidence-pack.md) — Evidence package and arbitration outline
- [scripts/labor-checker.js](scripts/labor-checker.js) — Severance, overtime, and probation calculation helpers

## Privacy Note

Employment information is processed for assessment only. No data is stored or transmitted to third parties.

## Important Reminders

- **Time limits**: Labor arbitration must be filed within 1 year
- **Evidence**: Keep contracts, pay slips, termination notices
- **Arbitration**: Required before court for labor disputes
- **Local rules**: Some cities have additional protections
