## Description:

Manage local and cloud backups with listing, creating, restoring, scheduling, and monitoring using Time Machine, rsync, cron, and rclone integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT

## Use Case:

Developers and end users use this skill to inspect backup status, create rsync-based backups, restore files, schedule recurring backups, and sync selected backups to configured cloud remotes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore commands can overwrite or otherwise modify files at the selected destination.

Mitigation: Restore into a staging folder when possible and confirm the destination path is safe before running the command.

Risk: Cloud sync can upload selected backup files to a configured rclone remote.

Mitigation: Review the rclone remote, provider access controls, and file contents before syncing.

Risk: Backups may fail or become incomplete if the destination has insufficient space or required tools are missing.

Mitigation: Check backup status, disk space, and required tools before relying on a backup schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ppopen/skills/openclaw-skill-backup-manager)
- [Publisher profile](https://clawhub.ai/user/ppopen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command snippets and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backup, restore, scheduling, and cloud-sync commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
