## Description: <br>
Reviews Korean business documents for required fields, formatting, extracted-value accuracy, and cross-document consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ustay-coder](https://clawhub.ai/user/Ustay-coder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, reviewers, and business operations teams use this skill to check Korean invoices, contracts, bank-account copies, estimates, transaction statements, business registrations, subsidy paperwork, inspection reports, transfer confirmations, and result reports. It helps extract key fields, apply document-specific checklists, compare amounts, parties, accounts, dates, and missing-document status, then produce review results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated review reports can contain sensitive business data such as account numbers, registration numbers, addresses, and transaction amounts. <br>
Mitigation: Use the skill in a private workspace, process only documents you are authorized to review, and delete or redact JSON reports when the sensitive details no longer need to be retained. <br>
Risk: OCR output can be inaccurate, especially when extracted values conflict across documents. <br>
Mitigation: Confirm suspicious OCR results against the original document image before treating a discrepancy as final. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ustay-coder/kr-document-reviewer) <br>
- [Bank account checklist](artifact/references/bank-account.md) <br>
- [Business registration checklist](artifact/references/business-registration.md) <br>
- [Contract checklist](artifact/references/contract.md) <br>
- [Estimate checklist](artifact/references/estimate.md) <br>
- [Expense request checklist](artifact/references/expense-request.md) <br>
- [Inspection report checklist](artifact/references/inspection-report.md) <br>
- [Result report checklist](artifact/references/result-report.md) <br>
- [Subsidy application checklist](artifact/references/subsidy-application.md) <br>
- [Tax invoice checklist](artifact/references/tax-invoice.md) <br>
- [Transaction statement checklist](artifact/references/transaction-statement.md) <br>
- [Transfer confirmation checklist](artifact/references/transfer-confirmation.md) <br>
- [Review result JSON schema](artifact/schema/review-result.schema.json) <br>
- [Sample review output](artifact/schema/sample-output.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Structured JSON review report with a concise Markdown or plain-text summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow may save JSON reports to reviews/REV-{YYYYMMDD}-{NNN}.json and may provide PDF-to-image conversion commands for OCR preparation.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
