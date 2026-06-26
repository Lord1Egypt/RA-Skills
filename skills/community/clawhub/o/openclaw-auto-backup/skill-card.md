## Description: <br>
Openclaw Auto Backup helps OpenClaw users back up selected local configuration and workspace files, list backup versions, restore a selected backup, and clean up old backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwg2025](https://clawhub.ai/user/williamwg2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and administrators use this skill to protect local agent configuration and workspace state with manual or scheduled backups, backup version listing, restore, and retention cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may copy sensitive OpenClaw profile, memory, or configuration data into ~/.openclaw/backups in unencrypted form. <br>
Mitigation: Use restrictive permissions on the backup directory, review configured watchFiles before use, and apply external encryption when sensitive data may be included. <br>
Risk: Restore and cleanup operations can overwrite or remove local OpenClaw state. <br>
Mitigation: List available backups first, use dry-run behavior where available, and review cleanup or restore targets before allowing changes. <br>
Risk: Scheduled execution can repeatedly change local state without direct user action. <br>
Mitigation: Review any OpenClaw cron or system cron entry and disable or adjust it when automatic local backups are not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/williamwg2025/openclaw-auto-backup) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of bundled local Python scripts that create, list, restore, and delete backup files.] <br>

## Skill Version(s): <br>
0.1.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
