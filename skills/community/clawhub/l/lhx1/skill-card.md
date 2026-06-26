## Description: <br>
lhx1 helps agents create, edit, analyze, and validate spreadsheets with formulas, formatting, data analysis, visualization, and LibreOffice-based recalculation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goulonghui](https://clawhub.ai/user/goulonghui) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and other spreadsheet users can use this skill to guide agents through spreadsheet creation, editing, analysis, formula construction, formatting, visualization, and recalculation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formula recalculation writes a persistent LibreOffice macro into the user's application profile. <br>
Mitigation: Review the skill before installing, use it only with trusted spreadsheet files, and understand that recalculation configures LibreOffice locally. <br>
Risk: Spreadsheet edits can overwrite existing files or preserve incorrect formulas if changes are not reviewed. <br>
Mitigation: Save modified workbooks as copies, keep backups, and require formula error checks before treating outputs as final. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goulonghui/lhx1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON recalculation summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or modification of .xlsx, .xlsm, .csv, and .tsv files; formula recalculation reports spreadsheet error locations and counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
