## Description: <br>
Creates timestamped full backups of the local OpenClaw configuration directory, including hidden files, credentials, logs, and workspace data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijiangtai](https://clawhub.ai/user/lijiangtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create local snapshots of their OpenClaw state before changes, migration, or recovery work. It provides backup and restore guidance around the ~/.openclaw directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup directories can contain credentials, logs, workspace files, and other sensitive OpenClaw state. <br>
Mitigation: Protect each timestamped backup like the original ~/.openclaw directory and avoid sharing or syncing it unintentionally. <br>
Risk: Restore commands can replace or move the active OpenClaw configuration directory. <br>
Mitigation: Verify source and destination paths before running restore commands, and keep a separate copy of the current configuration until recovery is confirmed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lijiangtai/openclaw-all-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a timestamped local backup directory under the user's home directory when the backup script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
