## Description:

Provides guided OpenClaw backup, snapshot, retention, and recovery workflows, with optional email delivery and integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliwang76](https://clawhub.ai/user/liliwang76)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to configure and run local backups, create pre-change snapshots, review backup logs, clean old backups, and follow recovery steps after failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full OpenClaw backups can include credentials and workspace data.

Mitigation: Store backup archives in a private directory with restrictive permissions and review what is included before relying on the workflow.

Risk: Email delivery can transmit sensitive backup archives without enforced encryption.

Mitigation: Keep email delivery disabled unless archives are encrypted first and the email integration is trusted and verified.

Risk: Retention and deletion settings can remove backup material that may be needed for recovery.

Mitigation: Review local and email retention settings carefully and confirm deletion prompts only after checking the listed files or messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liliwang76/skills/openclaw-reliable-backup)
- [Publisher profile](https://clawhub.ai/user/liliwang76)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown-style operational guidance with inline shell commands, user prompts, backup archives, checksum files, and log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local backup archives, snapshots, SHA-256 checksum files, and backup logs; optional email delivery depends on user configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
