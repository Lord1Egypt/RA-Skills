## Description: <br>
MiniMax spreadsheet production system for tabular data, numeric analysis, and spreadsheet generation with XLSX/XLSM/CSV support, Python workbook construction, LibreOffice formula recalculation, and MiniMaxXlsx validation tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KrisLiu16](https://clawhub.ai/user/KrisLiu16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and spreadsheet producers use this skill to create publication-ready Excel workbooks from tabular data, including formulas, styling, embedded charts, PivotTables, and validation checks before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formula recalculation can make persistent changes to the local LibreOffice macro profile. <br>
Mitigation: Use the recalculation step only when intentionally generating spreadsheets, and isolate or back up the LibreOffice profile before first use. <br>
Risk: The skill invokes local shell commands and workbook tooling, which can modify files in the working directory. <br>
Mitigation: Review generated commands, input paths, and output paths before execution, and keep source data or existing workbooks backed up. <br>
Risk: The MiniMaxXlsx executable is referenced by the skill but was not included in the inspected artifact. <br>
Mitigation: Verify the executable's source and integrity separately before running MiniMaxXlsx commands. <br>
Risk: The broad activation scope may apply spreadsheet workflows to tasks where this local tooling was not intended. <br>
Mitigation: Use the skill only for deliberate spreadsheet-generation, analysis, or validation tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KrisLiu16/minimax-xlsx) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Chart creation guide](artifact/charts.md) <br>
- [Pivot operations manual](artifact/pivot.md) <br>
- [Styling guide](artifact/styling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [XLSX/XLSM/CSV files with Markdown guidance, Python code, and shell command invocations as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workbook outputs are expected to pass formula recalculation, diagnostic checks, chart checks when applicable, and OpenXML validation before delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
