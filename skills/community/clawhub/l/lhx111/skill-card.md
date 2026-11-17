## Description:

Provides spreadsheet creation, editing, analysis, formatting, visualization, and formula recalculation support for Excel-compatible files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goulonghui](https://clawhub.ai/user/goulonghui)

### License/Terms of Use:

Proprietary

## Use Case:

Developers, analysts, and spreadsheet authors use this skill to create, modify, analyze, and validate Excel-compatible workbooks with formulas, formatting, data analysis, visualization, and LibreOffice-based formula recalculation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formula recalculation can persistently modify and execute LibreOffice application macros in the user's profile.

Mitigation: Review the skill before installation and run recalculation only in an isolated user account or temporary LibreOffice profile.

Risk: The recalculation helper may overwrite an existing LibreOffice Module1.xba macro.

Mitigation: Back up existing workbooks and LibreOffice macro files before using recalculation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goulonghui/skills/lhx111)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline Python and shell command examples; helper script output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spreadsheet outputs may include .xlsx, .xlsm, .csv, or .tsv files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
