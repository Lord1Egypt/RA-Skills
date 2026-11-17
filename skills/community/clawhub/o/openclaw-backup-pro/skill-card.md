## Description:

Backup and restore OpenClaw data, including configuration, credentials, workspace data, Telegram sessions, and scheduled tasks, with cache and log exclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardx0319](https://clawhub.ai/user/richardx0319)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to create rotating backups, configure daily backup schedules, and restore OpenClaw state after data loss or migration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain API keys, tokens, session data, workspace files, and scheduled tasks.

Mitigation: Store backup archives in a private encrypted location and avoid shared or synced directories unless encryption is in place.

Risk: Restore operations can overwrite current OpenClaw state and load restored agent configuration or scheduled tasks.

Mitigation: Restore only archives that were created and verified by the operator, and keep a pre-restore copy of the current state for rollback.

## Reference(s):

- [Restore OpenClaw from Backup](references/restore.md)
- [Openclaw Backup on ClawHub](https://clawhub.ai/richardx0319/skills/openclaw-backup-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup and restore commands, cron configuration guidance, and operational status text.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
