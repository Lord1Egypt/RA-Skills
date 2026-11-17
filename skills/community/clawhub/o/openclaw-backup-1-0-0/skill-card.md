## Description:

Backup and restore OpenClaw data by creating backups, setting up automatic backup schedules, restoring from backup, managing backup rotation, and archiving the ~/.openclaw directory with exclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, rotate, schedule, and restore backups of OpenClaw configuration, credentials, sessions, scheduled tasks, and workspace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may include API keys, tokens, session data, workspace memory, user files, and scheduled tasks.

Mitigation: Store backup archives only in an owner-controlled trusted directory and consider encrypting them before retention or transfer.

Risk: Restore commands can overwrite or delete the current OpenClaw state.

Mitigation: Review restore commands before running them and keep a current-state copy until the restored OpenClaw environment is verified.

## Reference(s):

- [Restore OpenClaw from Backup](references/restore.md)
- [Openclaw Backup 1.0.0 on ClawHub](https://clawhub.ai/kenswj/skills/openclaw-backup-1-0-0)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of compressed OpenClaw backup archives and scheduled backup configuration.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
