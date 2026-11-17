## Description:

Converts MT940, Excel, and PDF bank statements into standard Excel import templates for BIPV5, Kingdee EAS_YXH, Fingard ATS, NSTC, and Yonyou NCC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jreadstone](https://clawhub.ai/user/jreadstone)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operations teams, treasury system implementers, and developers use this skill to convert bank statement files into import-ready templates for supported treasury and ERP systems, including single-file and batch conversion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically download and cache spreadsheet templates when local templates are missing, and those templates affect generated financial import files.

Mitigation: Review the template-download behavior before installation and prefer pre-provisioned, verified local templates.

Risk: Bank statements may contain sensitive financial data, and optional OCR integrations could expose that data if routed through an unapproved service.

Mitigation: Use an isolated non-privileged Python environment with pinned dependencies and avoid enabling cloud OCR for sensitive statements unless approved.

Risk: Incorrectly parsed or mapped spreadsheet output could introduce errors before import into treasury or ERP systems.

Mitigation: Review generated spreadsheets before importing them into financial systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jreadstone/skills/imp-trm-accstmt)
- [Currency List](references/currency.md)
- [Tesseract OCR installation reference](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Excel workbook files with concise command and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces target-system import templates from supported bank statement inputs; generated spreadsheets should be reviewed before financial-system import.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
