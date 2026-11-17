## Description:

Backs up and restores an OpenClaw workspace with incremental archives, integrity checks, health diagnostics, optional configuration encryption, and optional WebDAV upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifox2046](https://clawhub.ai/user/ifox2046)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create local or WebDAV-backed OpenClaw backups, restore a workspace after migration or failure, verify backup integrity, and set up lightweight scheduled backup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive OpenClaw backups and WebDAV credentials.

Mitigation: Review and harden the shell scripts before installation; use encrypted configuration backups for any remote upload and keep backup passwords in a password manager.

Risk: Restore and delete operations can overwrite workspace files or remove backup data.

Mitigation: Use dry-run or verification modes first, confirm paths and selected backup versions, and keep a current rollback backup before destructive operations.

Risk: Portable exports or uploaded backup sets may expose configuration data if redaction or encryption is incomplete.

Mitigation: Do not share exported packages until configuration redaction is verified, and avoid uploading unencrypted OpenClaw configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ifox2046/skills/openclaw-webdav-backup)
- [Backup notes](references/backup.md)
- [Restore notes](references/restore.md)
- [Scheduled backups](references/scheduling.md)
- [OpenClaw + WebDAV backup and migration plan](references/migration-plan.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose remote upload, restore, delete, encryption, and scheduling steps that require review before execution.]

## Skill Version(s):

1.3.0 (source: server release evidence and version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
