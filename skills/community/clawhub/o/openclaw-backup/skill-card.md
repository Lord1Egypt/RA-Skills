## Description:

Backup and restore OpenClaw data. Use when user asks to create backups, set up automatic backup schedules, restore from backup, or manage backup rotation. Handles ~/.openclaw directory archiving with proper exclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex3alex](https://clawhub.ai/user/alex3alex)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to create and rotate local backups of ~/.openclaw, configure scheduled backups, and restore OpenClaw state from an archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups include credentials, API keys, tokens, and session data in plaintext archives.

Mitigation: Use only trusted local backup locations, restrict archive access, and consider encrypting backup archives.

Risk: Restore and rollback steps can overwrite or delete the active ~/.openclaw directory.

Mitigation: Verify backup contents first and make a separate safety copy of the current ~/.openclaw directory before running restore or rollback commands.

## Reference(s):

- [Restore OpenClaw from Backup](references/restore.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include backup file paths, cron schedule examples, restore steps, and safety checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
