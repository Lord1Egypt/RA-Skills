## Description:

自动识别发票和票据图片或 PDF，提取金额、日期、商家、税号等关键字段，支持批量汇总、费用分类、税务验真，并生成飞书报销草稿或 Excel/JSON 导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, finance operations teams, and agents use this skill to extract structured data from Chinese invoices and receipts, check key validation rules, classify expense categories, and prepare reimbursement records or summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice images and extracted invoice metadata may be sent to configured OCR, AI vision, tax-verification, or Feishu systems.

Mitigation: Use narrowly scoped API keys, obtain approval before processing sensitive invoices, and add an explicit confirmation step before cloud OCR or external sync.

Risk: OCR or AI vision extraction can misread amounts, dates, seller names, tax numbers, or invoice status.

Mitigation: Require human review for high-value, low-confidence, failed-validation, voided, or red-corrected invoices before reimbursement or accounting use.

Risk: Tax verification may be rate-limited, unavailable, or only advisory for the reimbursement workflow.

Mitigation: Throttle batch verification and direct users to confirm final invoice validity through the official tax verification platform when automated verification fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/invoice-ocr-extractor)
- [Invoice type recognition rules](references/invoice-types.md)
- [Field extraction rules](references/field-extraction.md)
- [Expense category rules](references/expense-categories.md)
- [Tax verification interface notes](references/tax-verification.md)
- [National VAT invoice verification platform](https://inv.chinatax.gov.cn/)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown or plain-text summaries, JSON invoice records, and Excel or JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require configured OCR, tax-verification, or Feishu credentials for cloud recognition, verification, or sync flows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
