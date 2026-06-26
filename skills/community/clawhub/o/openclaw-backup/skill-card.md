## Description: <br>
Backup and restore OpenClaw data, including backup creation, automatic backup schedules, restore steps, and backup rotation for the ~/.openclaw directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex3alex](https://clawhub.ai/user/alex3alex) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and administrators use this skill to create local backups of OpenClaw configuration, credentials, workspace data, scheduled tasks, and session data, then restore those backups when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated backup archives may contain credentials, tokens, session data, configuration, and workspace files. <br>
Mitigation: Store backup archives privately, prefer encrypted storage, and avoid sharing or syncing them to untrusted locations. <br>
Risk: Restore commands can replace the current ~/.openclaw directory. <br>
Mitigation: Stop OpenClaw first, keep the current directory as ~/.openclaw-old, and verify the backup path before extraction. <br>
Risk: Scheduled backups can run an unexpected script path if cron configuration is copied without review. <br>
Mitigation: Review the cron payload path before enabling scheduled backups. <br>


## Reference(s): <br>
- [OpenClaw Backup on ClawHub](https://clawhub.ai/alex3alex/openclaw-backup) <br>
- [alex3alex ClawHub profile](https://clawhub.ai/user/alex3alex) <br>
- [Restore OpenClaw from Backup](references/restore.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local compressed backup archives when the backup script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
