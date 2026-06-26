## Description: <br>
Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, visualization, and formula recalculation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goulonghui](https://clawhub.ai/user/goulonghui) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and analysts use this skill to create, edit, analyze, format, and validate spreadsheet files while preserving formulas and template conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify spreadsheet files. <br>
Mitigation: Keep backups of important workbooks and review generated changes before relying on the output. <br>
Risk: The recalculation helper may leave or overwrite a LibreOffice macro in the user's profile. <br>
Mitigation: Use the helper only in an environment where persistent LibreOffice profile changes are acceptable, and inspect the profile if macro state matters. <br>
Risk: Untrusted spreadsheets may carry unsafe content or misleading formulas. <br>
Mitigation: Avoid running the workflow on untrusted spreadsheets and verify formulas, links, and outputs before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goulonghui/lhx11) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify spreadsheet files and may return JSON formula-recalculation results from recalc.py.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
