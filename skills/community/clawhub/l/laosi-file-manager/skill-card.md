## Description: <br>
Windows文件管理器让 an AI agent perform Windows file and folder operations, including creating, copying, moving, deleting, searching, renaming, organizing, and batch processing files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows users can use this skill to automate file organization, batch file handling, search, rename, copy, move, and cleanup workflows on local Windows folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete, move, rename, overwrite, or batch-change local files and folders. <br>
Mitigation: Before any destructive or batch operation, require the agent to list exact affected paths, confirm the intended folder scope, and use backups or a recycle-bin workflow where possible. <br>
Risk: The artifact's safeguards may not reliably prevent broad or unintended file changes. <br>
Mitigation: Limit execution to an explicitly approved workspace or test folder, review proposed commands before execution, and avoid running on system or user-profile directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-file-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python; outputs include file-operation snippets, workflow guidance, and operation reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
