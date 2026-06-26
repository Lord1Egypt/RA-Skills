## Description: <br>
OpenClaw automated file-management assistant for batch file operations, intelligent classification, duplicate cleanup, file renaming, directory synchronization, and related file workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and end users use this skill to organize local folders, batch rename files, detect and handle duplicates, and synchronize directories. It is suited to file workflow automation where users can preview actions and confirm changes before modifying local data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive file operations can rename, move, copy, overwrite, or delete files at scale. <br>
Mitigation: Use scan-only or preview modes first, test on non-critical folders, keep backups, prefer quarantine or move over permanent deletion, and verify every source and target path. <br>
Risk: Cron, watch, or no-confirm automation can amplify unintended file changes. <br>
Mitigation: Avoid unattended automation until the exact command and recovery plan have been reviewed. <br>


## Reference(s): <br>
- [File management best practices](references/best_practices.md) <br>
- [ClawHub release page](https://clawhub.ai/muguozi1/muguozi1-openclaw-file-manager-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, configuration notes, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file-operation plans, dry-run previews, logs, and reports before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
