## Description: <br>
Office Automation helps agents run local office workflows for Excel merging, Word text replacement, PDF merging, and batch file renaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoheizp](https://clawhub.ai/user/xiaoheizp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, administrators, finance, HR, sales, and operations users can use this skill to automate local document and file handling tasks such as spreadsheet consolidation, contract text replacement, PDF consolidation, and folder cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can batch rename files and overwrite Word documents in place. <br>
Mitigation: Test on copies first, keep backups, and avoid important business, HR, finance, or customer documents until dry-run, confirmation, backup, and collision safeguards are added. <br>
Risk: Bulk office automation can modify many local files quickly if pointed at the wrong folder. <br>
Mitigation: Review input paths before execution and restrict runs to controlled working directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoheizp/ke-office-automation) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoheizp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line output, generated office files, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with python3 and optional packages for Excel, PDF, and Word processing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
