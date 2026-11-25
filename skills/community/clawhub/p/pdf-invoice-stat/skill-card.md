## Description:

Extracts invoice fields from PDF, XML, OFD, ZIP, and RAR files and writes them to a 15-column Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seairteng](https://clawhub.ai/user/seairteng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance teams can use the skill to extract key fields from supported electronic invoices and prepare a spreadsheet for review and reimbursement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports a spreadsheet formula risk when processing invoices.

Mitigation: Review generated workbooks before opening them in software that evaluates formulas, especially when inputs are untrusted.

Risk: The security assessment notes extraction reliability mismatches and partial coverage.

Mitigation: Check important extracted fields against the source invoice before relying on the workbook.

## Reference(s):

- [pdf-invoice-stat on ClawHub](https://clawhub.ai/seairteng/skills/pdf-invoice-stat)

## Skill Output:

**Output Type(s):** [Files, Structured data]

**Output Format:** [Excel workbook (.xlsx) with 15 columns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A spreadsheet of extracted invoice fields, with reimbursement fields available for manual entry.]

## Skill Version(s):

2.4.7 (source: server-resolved release metadata, version.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
