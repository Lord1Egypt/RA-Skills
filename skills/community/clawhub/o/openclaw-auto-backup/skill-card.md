## Description:

OpenClaw Auto Backup helps agents manage local OpenClaw configuration backups with scheduled backup, version listing, restore, and cleanup workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwg2025](https://clawhub.ai/user/williamwg2025)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to protect local OpenClaw configuration state, keep versioned backups, inspect available backup versions, restore a prior backup, and remove older backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy sensitive OpenClaw state into plaintext backup archives.

Mitigation: Constrain backupDir and watchFiles to intended OpenClaw paths, exclude secrets, restrict backup directory permissions, and encrypt backups with an external tool when sensitive state may be present.

Risk: Restore and cleanup operations can overwrite or delete local files.

Mitigation: Treat restore and cleanup as destructive operations, use dry-run or confirmation flows first, and create a fresh backup before restoring or deleting old backups.

Risk: Path expansion and restore layout issues can make backup or restore behavior differ from user expectations.

Mitigation: Pin the reviewed skill version and verify configured paths and restore targets in a non-critical environment before relying on the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwg2025/skills/openclaw-auto-backup)
- [README_EN.md](README_EN.md)
- [README.md](README.md)
- [backup-config.json](config/backup-config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local backup, restore, list, and cleanup guidance for OpenClaw configuration files.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
