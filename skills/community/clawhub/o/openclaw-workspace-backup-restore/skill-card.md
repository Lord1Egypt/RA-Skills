## Description:

OpenClaw Backup & Restore helps agents create, validate, list, restore, and Git-sync OpenClaw workspace backups with rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to protect workspace state, recover deleted or corrupted agent configuration files, validate backup integrity, and maintain off-machine backup history when configured intentionally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git sync can upload sensitive OpenClaw configuration when raw config backup is enabled by default in the push workflow.

Mitigation: Use local sanitized backups by default, run Git sync only to private intended repositories, and pass --sanitized-config-only for backup-and-push operations.

Risk: Restore paths and backup names are not tightly controlled, so untrusted backup manifests or names can affect restore behavior.

Mitigation: Run restore with --dry-run first, use trusted backups only, and review backup manifests before applying a restore.

Risk: Scheduled remote backups may propagate sensitive or unintended workspace data without interactive review.

Mitigation: Do not enable cron or unattended remote backups until raw-config defaults and path validation issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/openclaw-workspace-backup-restore)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [RUNBOOK.md](RUNBOOK.md)
- [QUICKSTART.md](QUICKSTART.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, file paths, and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file operations, backup manifests, validation checks, restore previews, and Git sync commands.]

## Skill Version(s):

1.5.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
