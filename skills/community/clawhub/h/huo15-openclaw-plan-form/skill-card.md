## Description:

Huo15 Openclaw Plan Form helps an agent classify varied planning Excel workbooks into three standard templates, normalize their contents, generate unified XLSX outputs, and annotate differences against prior versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and planning teams use this skill to turn customer demand, production planning, tracking, and DIP scheduling spreadsheets into consistent company templates. Developers and agents can also use it to inspect workbook structure, review classification confidence, apply column mappings, and produce normalized JSON, filled XLSX files, or annotated diff reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer-provided spreadsheets may contain formulas that are carried into generated Excel files.

Mitigation: Process trusted spreadsheets only, or add formula sanitization before writing XLSX outputs.

Risk: Unpinned dependencies can make installs less reproducible across environments.

Mitigation: Pin pandas, openpyxl, and xlrd versions before production use.

Risk: Generated outputs can overwrite or mix with existing work if written into shared directories.

Mitigation: Write normalized JSON, generated workbooks, and diff reports to a dedicated work or output directory.

Risk: Automatic sheet, header, date, and column mapping can be wrong for complex or low-confidence workbooks.

Mitigation: Review inspect and extraction reports, then use explicit sheet, header-row, data-start, year, or mapping overrides when confidence is low.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-plan-form)
- [Workflow guide](reference/workflow.md)
- [Classification guide](reference/classification.md)
- [Template schema](reference/templates_schema.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON, Excel files]

**Output Format:** [Markdown guidance with inline shell commands, normalized JSON, generated XLSX workbooks, and diff JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include filled template workbooks, clean blank template workbooks, annotated diff workbooks, and classification or extraction reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
