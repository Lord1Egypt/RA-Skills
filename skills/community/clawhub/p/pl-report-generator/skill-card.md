## Description:

Generate automated financial and business reports with PDF output, chart creation, and distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting teams use this skill to turn period-end financial data into P&L, balance sheet, cash flow, KPI, variance, and business reports with charts and PDF deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned reporting and charting dependencies may change behavior or introduce supply-chain exposure.

Mitigation: Install dependencies in a dedicated virtual environment and pin package versions before repeated or production use.

Risk: Generated financial PDFs may contain incorrect, stale, or sensitive information if distributed without review.

Mitigation: Review every generated PDF before sending and require explicit approval before external distribution.

Risk: Financial source files, payroll details, or credentials may be exposed if unrelated secrets or production data are kept in the working directory.

Mitigation: Keep raw client data scoped to the reporting workspace, redact sensitive payroll or PII fields from shared reports, and avoid storing unrelated secrets nearby.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/pl-report-generator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide creation of local report files such as CSV, JSON, chart images, PDFs, and distribution logs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
