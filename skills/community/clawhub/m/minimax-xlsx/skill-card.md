## Description:

MiniMax spreadsheet production system. Engage for any task that involves tabular data, numeric analysis, or spreadsheet generation. Supports XLSX/XLSM/CSV through Python 3 (openpyxl + pandas) for workbook construction, formula recalculation via recalc.py (LibreOffice headless), and the MiniMaxXlsx CLI (C#/.NET) for structural validation, formula auditing, and pivot table synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krisliu16](https://clawhub.ai/user/krisliu16)

### License/Terms of Use:


## Use Case:

Developers, analysts, and spreadsheet-focused agents use this skill to build publication-ready Excel deliverables from tabular data, including validated formulas, charts, PivotTables, styling, and recalculation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recalculation helper persistently changes the user's LibreOffice macro profile and may overwrite existing macros.

Mitigation: Run the skill in a contained workspace or with an isolated LibreOffice profile before using it on important workbooks.

Risk: The skill runs local shell commands for workbook recalculation and validation.

Mitigation: Review commands and generated artifacts before execution, especially when handling sensitive or untrusted spreadsheets.

Risk: Server evidence notes missing CLI provenance for the MiniMaxXlsx binary.

Mitigation: Verify the CLI source or binary provenance before relying on its results for high-risk or sensitive workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krisliu16/skills/minimax-xlsx)
- [Pivot Operations Manual](artifact/pivot.md)
- [Chart Creation and Verification Guide](artifact/charts.md)
- [Visual Styling Reference](artifact/styling.md)
- [LibreOffice Recalculation Script](artifact/scripts/recalc.py)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Excel workbooks, CSV files, Markdown guidance, Python code, shell commands, and JSON diagnostics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or validate XLSX/XLSM/CSV files and emit recalculation or audit summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
