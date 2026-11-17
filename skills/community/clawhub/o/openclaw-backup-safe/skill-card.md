## Description:

Backup and restore OpenClaw data, including backup creation, automatic backup scheduling, restore steps, and backup rotation for the ~/.openclaw directory with documented exclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alessandropcostabr](https://clawhub.ai/user/alessandropcostabr)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to back up OpenClaw configuration, credentials, sessions, workspace files, and scheduled tasks, then restore them when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain credentials, sessions, memory, scheduled tasks, and user files in portable plaintext form.

Mitigation: Store backups only in a private encrypted location, restrict file permissions, and avoid shared or synchronized folders unless they provide appropriate encryption and access controls.

Risk: An exposed backup may compromise OpenClaw credentials or active sessions.

Mitigation: Treat exposed backups as credential or session compromise and rotate or revoke affected secrets and sessions.

Risk: Restore operations replace the active ~/.openclaw directory.

Mitigation: Stop OpenClaw before restore, keep a timestamped safety copy of the existing directory, and verify service status after restart.

## Reference(s):

- [OpenClaw Backup Safe on ClawHub](https://clawhub.ai/alessandropcostabr/skills/openclaw-backup-safe)
- [Restore OpenClaw from Backup](references/restore.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup and restore instructions; the backup script creates compressed tar archives and keeps the last 7 backups.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
