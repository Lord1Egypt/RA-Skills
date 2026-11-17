## Description:

Manages MaybeAI spreadsheet lifecycle work, including upload and import, workbook profiling, worksheet inspection, read and write operations, formulas, formula lineage tracing, formatting, sharing, SQL result-table workflows, and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no7dw](https://clawhub.ai/user/no7dw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and spreadsheet operators use this skill to work with MaybeAI spreadsheets: importing files, profiling workbook contents, reading and updating worksheets, writing formulas or SQL result sheets, tracing formula dependencies, formatting reports, changing sharing settings, and exporting workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ready-to-run mutation examples can delete or overwrite workbook data.

Mitigation: Use disposable or backed-up workbooks, perform only the explicitly requested operation, and verify the workbook, worksheet, range, and email target before running mutation scripts.

Risk: Sharing examples can expose a sheet publicly or grant editor access.

Mitigation: Confirm the intended visibility and permission level before using sharing operations, and verify resulting permissions after the change.

Risk: Workbook contents and sample rows may be sent to the MaybeAI service.

Mitigation: Avoid using sensitive spreadsheets unless the user has approved the service interaction and the data handling requirements are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/no7dw/skills/maybeai-sheet-skill)
- [MaybeAI Sheet Homepage](https://github.com/OmniMCP-AI/maybeai-uni)
- [File Management Reference](references/file-management.md)
- [Workbook Profile Reference](references/workbook-profile.md)
- [Read and Write Reference](references/read-write.md)
- [Formulas and SQL Reference](references/formulas-sql.md)
- [SQL Formula Showcase](references/sql-formula-showcase.md)
- [Lineage Trace Reference](references/lineage-trace.md)
- [Charts and Formatting Reference](references/charts-formatting.md)
- [Permission Sharing Reference](references/permission-sharing.md)
- [Clickable References Guide](references/clickable-refs.md)
- [Errors and Recovery Reference](references/errors-recovery.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code, shell commands, JSON request examples, and spreadsheet reference tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MaybeAI API call payloads, worksheet operation plans, verification steps, and user-facing workbook summaries.]

## Skill Version(s):

0.13.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
