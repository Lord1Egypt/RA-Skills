## Description: <br>
Backup and restore an OpenClaw workspace with incremental backups, integrity verification, health checks, optional config encryption and optional WebDAV upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ifox2046](https://clawhub.ai/user/ifox2046) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create local or WebDAV-backed backups, restore a workspace, migrate a single-machine OpenClaw setup, verify backup integrity, and manage backup retention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads OpenClaw workspace, extension, and configuration data that may include credentials or other sensitive content. <br>
Mitigation: Review what will be backed up, keep generated archives private, and use --encrypt-config before any WebDAV upload. <br>
Risk: Local backup and migration environment files are treated as trusted shell inputs. <br>
Mitigation: Use only config files from trusted locations, review .env.backup, .env.backup.secret, .env.backup.notify, and generated migrate .env files before running scripts, and do not commit or share files containing credentials. <br>
Risk: Restore and deletion workflows can overwrite workspace data or remove backup versions. <br>
Mitigation: Run dry-run or verification modes first, confirm the backup path and target workspace, and keep a current fallback backup before restore or deletion. <br>
Risk: A restore check may contact Telegram unexpectedly when notification settings are present. <br>
Mitigation: Review or disable notification configuration before restore checks if outbound messages are not intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ifox2046/openclaw-webdav-backup) <br>
- [Backup Notes](references/backup.md) <br>
- [Restore Notes](references/restore.md) <br>
- [Scheduled Backups](references/scheduling.md) <br>
- [Migration Plan](references/migration-plan.md) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify backup archives, encrypted configuration copies, logs, manifests, checksums, portable export packages, and WebDAV uploads when the user runs the provided shell scripts.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and version.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
