## Description:

Openclaw Backup helps agents create manual, scheduled, and encrypted backups of OpenClaw data and list backup archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halaoluan](https://clawhub.ai/user/halaoluan)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to back up local OpenClaw state, create encrypted archives, configure scheduled backups, and inspect existing backup files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive OpenClaw data and server security evidence says it should be reviewed before installation.

Mitigation: Review and harden the scripts before use, especially temporary storage, cleanup behavior, cron changes, and password handling.

Risk: Plaintext archives or predictable temporary directories could expose backup contents during execution.

Mitigation: Use private random temporary directories, protected temporary storage, and cleanup traps before deploying the backup scripts.

Risk: Backup passwords may be exposed through command-line arguments or long-lived environment variables.

Mitigation: Avoid passing passwords on command lines or storing them in persistent environment variables; use an appropriate secret handling flow.

Risk: Scheduled backup setup can modify user crontabs.

Mitigation: Validate and display cron entries before installing or replacing scheduled backup jobs.

Risk: Documented broad permission or live-directory deletion examples can weaken file security or damage data.

Mitigation: Do not follow documented chmod -R 755 or live-directory deletion examples; operate on staged copies with narrow permissions.

## Reference(s):

- [Openclaw Backup on ClawHub](https://clawhub.ai/halaoluan/skills/halaoluan-openclaw-backup)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenSSL Documentation](https://www.openssl.org/docs/)
- [cron Manual](https://man.openbsd.org/cron.8)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run backup, encryption, checksum, listing, and cron setup commands depending on the user's request.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
