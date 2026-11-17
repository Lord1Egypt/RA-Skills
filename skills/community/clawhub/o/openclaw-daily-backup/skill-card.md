## Description:

OpenClaw Daily Backup helps create, list, validate, and restore backups for OpenClaw workspace identity and configuration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to make scheduled or named backups, verify backup integrity, preview restores, and recover workspace identity and configuration files after deletion or bad changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore operations can overwrite active OpenClaw identity and instruction files, including from bundled third-party backup files.

Mitigation: Remove bundled backups before installation, explicitly select the intended backup source, run restore in dry-run mode first, and inspect diffs before applying changes.

Risk: Generated backups can contain user profiles, agent instructions, service configuration, and possibly credentials.

Mitigation: Store backups with workspace-equivalent access controls and avoid committing or sharing backup directories.

Risk: The skill backs up more local OpenClaw data than the short description conveys.

Mitigation: Review the backup script and manifest contents so users know exactly which workspace, agent, and configuration files are collected.

Risk: Scheduled backups can preserve sensitive or unintended data over time.

Mitigation: Enable cron only after confirming retained data, retention behavior, and cleanup commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/openclaw-daily-backup)
- [Project homepage](https://github.com/X-RayLuan/soul-backup-skill)
- [README](README.md)
- [Runbook](RUNBOOK.md)
- [Examples](EXAMPLES.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js scripts and local filesystem backups; restore operations can modify workspace files.]

## Skill Version(s):

1.3.1 (source: package.json and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
