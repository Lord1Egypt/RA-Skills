## Description:

Reviews Korean business documents for format compliance, required fields, value accuracy, and cross-document consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ustay-coder](https://clawhub.ai/user/ustay-coder)

### License/Terms of Use:


## Use Case:

Employees, finance teams, operations teams, and reviewers use this skill to review Korean invoices, contracts, bank account copies, estimates, transaction statements, business registrations, subsidy documents, inspection reports, transfer confirmations, and result reports. It extracts key fields, checks each document against type-specific rules, and compares amounts, parties, account details, dates, and missing documents across a submission set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive business, financial, tax, and account identifiers through spawned model sessions and workspace files.

Mitigation: Use it only for documents approved for that processing path, prefer redacted outputs, and get explicit approval before saving reports.

Risk: Review outputs may retain unredacted financial and business identifiers in the workspace.

Mitigation: Delete the reviews directory and sensitive intermediate files when the review is complete, or store only redacted report versions.

Risk: OCR or cross-document comparisons can misread Korean names, company names, account numbers, addresses, or amounts.

Mitigation: Verify suspicious or high-impact findings against the original source document before acting on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ustay-coder/skills/kr-document-reviewer)
- [Tax invoice checklist](references/tax-invoice.md)
- [Contract checklist](references/contract.md)
- [Bank account copy checklist](references/bank-account.md)
- [Estimate checklist](references/estimate.md)
- [Transaction statement checklist](references/transaction-statement.md)
- [Business registration checklist](references/business-registration.md)
- [Expense request checklist](references/expense-request.md)
- [Subsidy application checklist](references/subsidy-application.md)
- [Inspection report checklist](references/inspection-report.md)
- [Transfer confirmation checklist](references/transfer-confirmation.md)
- [Result report checklist](references/result-report.md)
- [Review result JSON schema](schema/review-result.schema.json)
- [Sample review output](schema/sample-output.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured JSON review results and Markdown chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save JSON reports under reviews/REV-{YYYYMMDD}-{NNN}.json when approved; summaries are derived from the JSON summary section.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
