## Description: <br>
Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goulonghui](https://clawhub.ai/user/goulonghui) <br>

### License/Terms of Use: <br>
Proprietary. LICENSE.txt has complete terms <br>


## Use Case: <br>
Developers, analysts, and spreadsheet-heavy users use this skill to create, edit, analyze, format, and recalculate Excel-compatible workbooks while preserving formulas and template conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify and save local spreadsheet workbooks while recalculating formulas. <br>
Mitigation: Work on copies of important files, keep backups, and review generated or modified workbooks before relying on them. <br>
Risk: The security review notes that the recalculation helper silently adds a persistent LibreOffice macro to the user's profile. <br>
Mitigation: Install only in an environment where that profile change is acceptable, or use a sandboxed or dedicated LibreOffice profile and inspect or remove the macro after use. <br>
Risk: Running LibreOffice on untrusted or sensitive workbooks may expose local documents to tool behavior outside the agent transcript. <br>
Mitigation: Avoid untrusted or sensitive workbooks unless LibreOffice is sandboxed and the workbook contents are appropriate for local processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goulonghui/lhx111) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Spreadsheet files, Markdown guidance, Python code, shell commands, and JSON recalculation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require LibreOffice for formula recalculation and workbook error checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
