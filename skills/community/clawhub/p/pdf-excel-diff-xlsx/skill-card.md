## Description: <br>
Provides spreadsheet creation, editing, analysis, formatting, visualization, and formula recalculation workflows for XLSX, XLSM, CSV, and TSV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, analysts, and spreadsheet modelers use this skill to create, inspect, modify, format, and verify spreadsheet workbooks while preserving formulas and workbook conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formula recalculation can write a persistent LibreOffice Basic macro into the user's normal LibreOffice profile. <br>
Mitigation: Run recalculation in a disposable environment or back up the LibreOffice macro folder and important spreadsheets before use. <br>
Risk: Spreadsheet changes can create or modify workbook files and affect business-critical models. <br>
Mitigation: Review generated workbook changes, preserve backups, and verify reported formula errors before relying on outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/pdf-excel-diff-xlsx) <br>
- [Publisher profile](https://clawhub.ai/user/lnj22) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and spreadsheet file instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or modification of workbook files and formula recalculation checks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
