## Description:

MiniMax XLSX Pro helps agents create, recalculate, validate, style, chart, and pivot Excel workbooks from tabular data using Python, LibreOffice, and MiniMaxXlsx tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luaqnyin](https://clawhub.ai/user/luaqnyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to turn tabular data and analysis requirements into publication-ready XLSX/XLSM/CSV spreadsheet deliverables with formulas, charts, PivotTables, styling, and validation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recalculation helper modifies the user's LibreOffice macro profile and can trust or overwrite application-level macro code.

Mitigation: Review or sandbox scripts/recalc.py before use, preferably with a temporary LibreOffice profile and away from enterprise macro controls or existing macro libraries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luaqnyin/skills/minimax-xlsx-pro)
- [charts.md](artifact/charts.md)
- [pivot.md](artifact/pivot.md)
- [styling.md](artifact/styling.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets for spreadsheet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or validates spreadsheet deliverables, typically XLSX/XLSM/CSV files, through agent-authored code and local command execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
