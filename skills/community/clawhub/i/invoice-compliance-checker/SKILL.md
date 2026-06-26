---
slug: invoice-compliance-checker
version: "1.1.0"
tags: invoice-compliance, regulatory-check, accounts-payable, tax-validation, financial-controls
type: descriptive
language: en
---

# Invoice Compliance Checker

## Overview

Checks invoices for compliance with regulatory requirements and internal policies. This is a descriptive skill that provides templates, frameworks, and heuristic analysis without executing real code, accessing external APIs, or performing actual financial transactions.

## Trigger

Use this skill when the user wants to:
- get structured guidance on invoice compliance checker
- apply best-practice frameworks to their financial situation
- generate templates and checklists for financial planning

### Example prompts
- "Help me create a personal budget"
- "Analyze my cash flow forecast"
- "Check my expense categorization"
- "Assess my financial health"
- "Review my receivables aging"
- "Check invoice compliance"
- "Develop a pricing strategy"
- "Find cost reduction opportunities"
- "Optimize my tax deductions"
- "Interpret my financial reports"

## Workflow

1. User provides context and goals.
2. Skill applies built-in templates and frameworks.
3. Skill generates structured output with recommendations.
4. User receives actionable insights and next steps.

## Inputs
- User context (financial situation, goals, constraints)
- Optional data inputs (amounts, categories, timeframes)
- Analysis preferences

## Outputs
- Structured analysis report
- Templates and frameworks
- Actionable recommendations
- Next steps checklist

## Usage Scenarios

### Scenario 1

**User input:** "Check if our invoice template meets EU e-invoicing requirements for B2B transactions."

**Expected output:** Compliance checklist mapping each field to EU Directive 2014/55/EU requirements — mandatory fields (VAT ID, PO reference, unit price), format (UBL 2.1), digital signature, and archiving rules — with gap identification and remediation steps.

### Scenario 2

**User input:** "Audit these 20 vendor invoices for compliance with our purchase order policy."

**Expected output:** Exception report flagging PO mismatches, missing approvals, pricing deviations >5%, duplicate invoice detection, and non-compliant tax treatments — with severity ratings and resolution instructions.

### Scenario 3

**User input:** "Set up a self-check system so our team can validate invoices before submission."

**Expected output:** Pre-submission checklist organized by region (EU vs. US vs. APAC requirements), with automated validation rules (VAT number format, amount matching, required attachments by country) and approval workflow template.
### Scenario 4: 收到一张发票不知道是真的假的
**User input:** "我在闲鱼上找人代购了一台iPad，对方给我开了一张电子发票，我怀疑是假的，怎么查验？"
**Expected output:** 提供发票真伪查验流程：1）登录国家税务总局全国增值税发票查验平台（https://inv-veri.chinatax.gov.cn）输入发票代码、号码、开票日期、校验码后6位；2）核对票面信息——看开票方名称和实际销售方是否一致；3）检查电子发票印章——真发票有税务机关监制章和开票方电子签章；4）如果是不合规发票，可以在12366纳税服务热线举报。建议购买大件商品优先选择京东自营/天猫旗舰店等能开具正规发票的渠道。

## Safety
- No real financial transactions or API calls
- No access to real bank accounts or financial systems
- Recommendations are informational only
- Users should consult financial professionals for actual decisions

## Acceptance Criteria
- Must return structured markdown/JSON output
- Must include actionable recommendations
- Must clearly state the descriptive/non-executable nature
- Must provide templates or frameworks for user adaptation
