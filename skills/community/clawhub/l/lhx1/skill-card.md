## Description:

Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and formula recalculation for .xlsx, .xlsm, .csv, and .tsv workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goulonghui](https://clawhub.ai/user/goulonghui)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, analysts, and spreadsheet-heavy business users use this skill to create, edit, analyze, format, and validate spreadsheet files while preserving formulas and workbook conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled formula recalculation script can make persistent LibreOffice macro changes in the user's normal office profile.

Mitigation: Review before installing and prefer an isolated LibreOffice profile or a patched version that asks before changing local office configuration.

Risk: Formula recalculation can save changes back to the workbook in place.

Mitigation: Run recalculation on copies or backed-up workbooks and review JSON diagnostics before using important spreadsheet outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goulonghui/skills/lhx1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell command snippets, plus generated or modified spreadsheet files and JSON recalculation diagnostics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spreadsheet outputs may include formulas, formatting, charts, workbook edits, and recalculated formula values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
