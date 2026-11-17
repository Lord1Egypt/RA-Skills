## Description:

OpenClaw Backup helps users configure and run backups of local OpenClaw configuration files across Windows, Linux, and macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hi-jiajun](https://clawhub.ai/user/hi-jiajun)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to set up, run, and maintain backups of OpenClaw configuration data for routine protection, migration, and recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may include credentials and API keys.

Mitigation: Store backups only in private or encrypted locations and avoid shared or synced folders unless that exposure is intentional.

Risk: Archived backup cleanup can permanently delete backup folders.

Mitigation: Review backup destination, old-backup destination, retention count, and size thresholds before running the scripts.

Risk: A broad or valuable old-backup directory could be affected by cleanup behavior.

Mitigation: Do not configure the old-backup directory to a home directory or other broad path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hi-jiajun/skills/openclaw-backup-hiliang)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration steps, and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational backup and restore guidance; setup and backup scripts may create configuration and backup files.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
