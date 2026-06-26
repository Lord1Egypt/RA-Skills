## Description: <br>
Short alias skill for moving files, directories, or data; also for system management like managing services or packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a concise command reference for moving or reorganizing files, managing packages and services, and planning data migration steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce broad local command guidance, including deletion, package changes, service changes, database restores, Docker volume copies, and Git tag operations. <br>
Mitigation: Require explicit review and confirmation before any generated command is executed, especially commands with sudo, deletion, restore, startup, or remote-update effects. <br>
Risk: File moves and migration commands can overwrite, delete, or relocate important data if paths or options are wrong. <br>
Mitigation: Verify source and destination paths, confirm backups, and prefer non-destructive checks or dry-run style workflows before applying changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
