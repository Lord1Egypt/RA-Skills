## Description:

Optimized OpenClaw backup skill for creating full snapshots with workspace archive splitting, change summaries, restore instructions, and Discord notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cccarv82](https://clawhub.ai/user/cccarv82)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to install, configure, run, and schedule full OpenClaw state backups, including split workspace archives, change summaries, restore guidance, and optional Discord notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup workflow can copy and push sensitive OpenClaw state and workspace data.

Mitigation: Use a private dedicated repository, narrow credentials, encryption before pushing, and reviewed exclusions for secrets and workspace data.

Risk: Scheduled backups can repeatedly upload sensitive or unwanted data if cron timing or backup scope is misconfigured.

Mitigation: Require a manually approved cron schedule and confirm the configured OpenClaw home, backup directory, repository, and exclusions before enabling automation.

Risk: Discord notifications can expose changed paths or restore text in a channel.

Mitigation: Disable Discord notifications or send them only to a restricted channel when notification content could reveal sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cccarv82/skills/openclaw-backup-optimized)
- [cccarv82 publisher profile](https://clawhub.ai/user/cccarv82)
- [Backup skill configuration](references/CONFIG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash, PowerShell, and JavaScript references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup setup guidance, cron commands, restore instructions, and a Node.js backup workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
