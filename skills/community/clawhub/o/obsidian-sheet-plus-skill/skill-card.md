## Description: <br>
Use when working with Obsidian spreadsheet data, including reading, writing, formatting, filtering, formulas, data validation, conditional formatting, merging cells, and sheet management through the Sheet Plus plugin REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljcoder2015](https://clawhub.ai/user/ljcoder2015) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian users use this skill to let an agent operate spreadsheet workbooks through the Sheet Plus plugin, including bulk data edits, formulas, filters, validation rules, formatting, and worksheet management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet operations can modify, clear, or restructure workbook data. <br>
Mitigation: Verify the target sheet and range before destructive actions and keep backups for important workbooks. <br>
Risk: The local Sheet Plus REST API may expose workbook contents or modification capability if left unauthenticated or reachable beyond localhost. <br>
Mitigation: Enable the plugin API key when appropriate and keep the REST API bound to localhost only. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/ljcoder2015/obsidian-sheet-plus-skill) <br>
- [ClawHub skill page](https://clawhub.ai/ljcoder2015/skills/obsidian-sheet-plus-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local REST API calls to read or modify Obsidian Sheet Plus workbooks.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata); artifact frontmatter version 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
