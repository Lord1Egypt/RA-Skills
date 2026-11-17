## Description:

OpenClaw Backup backs up OpenClaw workspace, config, and state with the built-in `openclaw backup create` command, and supports cleanup of old backups plus backup health verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyiptk](https://clawhub.ai/user/joeyiptk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create, verify, schedule, and clean up local OpenClaw backups that may include workspace files, configuration, encrypted credentials, session history, skills, and settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain sensitive workspace, configuration, credential, and session data.

Mitigation: Use a private backup directory such as mode 700, protect archives as sensitive secrets, and avoid shared or synced locations unless the archives are encrypted.

Risk: Recurring automation may run at an unexpected time or in an unexpected timezone.

Mitigation: Confirm the cron schedule and timezone before relying on the recurring backup job.

Risk: Cleanup can permanently delete backup archives when run with `--execute`.

Mitigation: Review the selected archives before running cleanup with `--execute`.

## Reference(s):

- [OpenClaw Backup Setup Guide](references/SETUP_GUIDE.md)
- [OpenClaw Backup on ClawHub](https://clawhub.ai/joeyiptk/skills/openclawbackup)
- [joeyiptk ClawHub profile](https://clawhub.ai/user/joeyiptk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup, verification, cleanup, and cron setup guidance for an OpenClaw environment.]

## Skill Version(s):

1.0.0 (source: frontmatter, CHANGELOG, version.txt, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
