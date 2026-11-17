## Description:

Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and formula recalculation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goulonghui](https://clawhub.ai/user/goulonghui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and spreadsheet-focused agents use this skill to create, edit, analyze, and validate spreadsheet workbooks while preserving formulas, formatting, and source documentation. It also guides formula recalculation and error checks using LibreOffice and the bundled recalculation script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formula recalculation can automatically create or reuse a persistent LibreOffice macro in the user's profile.

Mitigation: Review the skill before installing and run recalculation in an isolated LibreOffice profile or disposable account.

Risk: Recalculation may save changes back to the workbook being processed.

Mitigation: Use copies of important workbooks and keep backups before running the recalculation script.

## Reference(s):

- [ClawHub skill page: lhx11](https://clawhub.ai/goulonghui/skills/lhx11)
- [Publisher profile: goulonghui](https://clawhub.ai/user/goulonghui)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; recalculation results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify spreadsheet files and may invoke LibreOffice-based formula recalculation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
