## Description: <br>
Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and formula recalculation for spreadsheet files such as .xlsx, .xlsm, .csv, and .tsv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goulonghui](https://clawhub.ai/user/goulonghui) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to create, edit, analyze, format, and validate spreadsheet workbooks while preserving formulas and existing template conventions. It is especially oriented toward formula-driven spreadsheet generation and financial-model style formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formula recalculation installs a persistent LibreOffice macro in the user's profile and can overwrite an existing macro file. <br>
Mitigation: Review before installing, use copies of important spreadsheets, and prefer running recalculation in an isolated temporary LibreOffice profile or with explicit user approval before changing application-level macro files. <br>
Risk: Running spreadsheet recalculation on untrusted macro-enabled workbooks can expose users to workbook-level macro risk. <br>
Mitigation: Avoid running this workflow on untrusted macro-enabled workbooks and inspect files before recalculation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goulonghui/lhx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; agents may also create or modify spreadsheet files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formula recalculation returns JSON status, error counts, formula counts, and error locations when the included recalculation script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
