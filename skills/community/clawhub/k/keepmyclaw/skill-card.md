## Description:

Backup, restore, and manage encrypted OpenClaw agent snapshots using the Keep My Claw API for configuration, workspace files, credentials, cron jobs, and multi-agent configs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryce](https://clawhub.ai/user/ryce)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure off-site encrypted backups, restore agent state on a new machine, schedule backup runs, list snapshots, and prune old backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate signup, payment, API-key creation, and uploads to a paid off-site backup service.

Mitigation: Require explicit human approval before registration, payment, account changes, API-key creation, or uploading backups.

Risk: Backups may include sensitive OpenClaw workspace files, credentials, cron jobs, and agent configuration.

Mitigation: Review backup scope before upload, prefer an agent-scoped API key, and keep recovery credentials outside chat logs.

Risk: Restoring a backup can overwrite existing OpenClaw files and should not be trusted blindly.

Mitigation: Avoid restoring untrusted backups; verify the selected snapshot and require human approval before restore on machines with existing data.

Risk: Losing the local encryption passphrase makes encrypted backups unrecoverable.

Mitigation: Store the passphrase in a password manager or other durable location outside the backed-up machine.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ryce/skills/keepmyclaw)
- [Keep My Claw documentation](https://keepmyclaw.com/docs.html)
- [Keep My Claw website](https://keepmyclaw.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup, restore, list, prune, setup, scheduling, and recovery guidance.]

## Skill Version(s):

1.4.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
