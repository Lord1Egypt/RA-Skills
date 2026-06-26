## Description: <br>
本地文件整理虾 helps an agent preview, classify, move, rename, and find duplicate files in local folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize local folders such as Downloads, Desktop, photo collections, and project archives by file type, naming convention, or duplicate status. It is intended for agent-assisted local file management with preview-first workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move files and write local reports, which may expose sensitive filenames or paths if reports are shared. <br>
Mitigation: Use the skill on a specific folder, review dry-run output before execution, and avoid sharing generated report files when paths or filenames are sensitive. <br>
Risk: File organization actions can disrupt important local folders if applied too broadly. <br>
Mitigation: Keep backups for important files, preview the planned changes first, and prefer recoverable trash-based cleanup over permanent deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/local-file-organizer) <br>
- [classification-rules.md](references/classification-rules.md) <br>
- [duplicate-detection.md](references/duplicate-detection.md) <br>
- [naming-conventions.md](references/naming-conventions.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The organizer can run in dry-run mode, can use custom JSON classification rules, and can write local organize-report JSON files after execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
