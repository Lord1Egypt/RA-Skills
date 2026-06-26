## Description: <br>
Jiji5188 File Manager helps agents organize files, batch rename files, find duplicates, and synchronize directories using local Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiji5188](https://clawhub.ai/user/jiji5188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to preview and run local file organization, duplicate cleanup, batch rename, and one-way sync workflows for personal or project folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File operations can move, rename, synchronize, or delete local data. <br>
Mitigation: Use preview or scan-only modes first, review the operation list, keep backups, and require explicit execution before modifying files. <br>
Risk: Duplicate deletion and sync deletion can remove files that still matter. <br>
Mitigation: Prefer quarantine or move actions for duplicates, avoid sync deletion until differences are reviewed, and keep a backup of important folders. <br>


## Reference(s): <br>
- [File management best practices](references/best_practices.md) <br>
- [ClawHub skill page](https://clawhub.ai/jiji5188/jiji5188-file-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Code] <br>
**Output Format:** [Markdown with inline shell commands and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file operations default to previews or scan-only modes; execute modes require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
