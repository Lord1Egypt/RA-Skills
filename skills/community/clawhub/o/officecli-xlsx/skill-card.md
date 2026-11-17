## Description:

Helps agents create, inspect, edit, format, validate, and troubleshoot Excel .xlsx workbooks and CSV/TSV imports using OfficeCLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceyliu](https://clawhub.ai/user/iceyliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a task involves Excel workbooks, financial models, dashboards, trackers, formulas, charts, pivot tables, templates, or CSV/TSV import. It guides workbook construction and QA so spreadsheet outputs remain live, readable, and validated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions pipe remote installer scripts directly into a shell.

Mitigation: Inspect the installer first and prefer a pinned OfficeCLI release with published checksums or signatures before execution.

Risk: OfficeCLI commands can modify local spreadsheet files.

Mitigation: Review proposed commands, work on copies when editing existing workbooks, and run the skill's validation and visual QA steps before delivery.

## Reference(s):

- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that create or modify local spreadsheet files; users should inspect commands and validate workbook outputs before delivery.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
