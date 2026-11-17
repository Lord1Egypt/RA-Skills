## Description:

Automatically merges U9C system export spreadsheets into a standardized Excel report for overdue or stalled documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingchazhushui](https://clawhub.ai/user/qingchazhushui)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, finance, and administrative users use this skill to combine U9C export spreadsheets for purchase requests, receipts, sales orders, shipments, and payment requests into a consistent stalled-document review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local U9C export spreadsheets and creates a business-facing Excel report that may be used for administrative action.

Mitigation: Run it only on intended input files or a chosen folder, set an explicit output path, and review the generated workbook before relying on it for business decisions.

Risk: Unexpected files in a scanned folder could be included if their names match the supported U9C prefixes.

Mitigation: Prefer an explicit file list or a curated folder containing only the spreadsheets intended for the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingchazhushui/skills/merge-u9c-reports)
- [Publisher profile](https://clawhub.ai/user/qingchazhushui)
- [Artifact skill instructions](artifact/SKILL.md)
- [U9C report merger script](artifact/merge_u9c_reports.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, command-line usage, and generated Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local .xlsx report with fixed sections, Chinese report labels, standardized columns, formatting, and a date-based sheet name.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
