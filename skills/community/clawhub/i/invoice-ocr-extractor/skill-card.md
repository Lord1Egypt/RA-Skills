## Description: <br>
发票票据识别虾 automatically identifies invoice and receipt images, extracts key fields such as amounts, dates, merchants, and tax IDs, supports batch processing, expense categorization, tax verification, and can prepare Feishu table data or export Excel files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance staff, operations teams, and agents use this skill to process Chinese invoice and receipt images or PDFs, extract reimbursable fields, flag validation issues, classify expenses, verify VAT invoices when configured, and prepare spreadsheet or Feishu expense outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice images, tax data, API keys, and exported files are sensitive. <br>
Mitigation: Use scoped credentials in environment variables, process invoices only with approved OCR, model, tax-verification, and Feishu providers, and store exported JSON or Excel files in protected locations. <br>
Risk: OCR or AI-vision extraction may produce incorrect invoice fields, especially when images are unclear or API fallback is used. <br>
Mitigation: Review extracted results before uploads or reimbursement workflows, and manually confirm high-value invoices and validation warnings. <br>
Risk: Batch processing can read unintended input folders or write outputs to unintended paths. <br>
Mitigation: Confirm exact input directories and output paths before running batch extraction or expense-form generation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/invoice-ocr-extractor) <br>
- [Invoice Type Recognition Rules](references/invoice-types.md) <br>
- [Field Extraction Rules](references/field-extraction.md) <br>
- [Expense Category Rules](references/expense-categories.md) <br>
- [Tax Verification Interface Notes](references/tax-verification.md) <br>
- [National VAT Invoice Verification Platform](https://inv.chinatax.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, Excel files] <br>
**Output Format:** [Markdown guidance with bash commands, plus JSON or Excel invoice extraction outputs and draft expense-form JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require scoped OCR, tax-verification, or Feishu credentials; extracted amounts and tax results should be reviewed before upload or reimbursement use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
