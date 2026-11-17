## Description:

Deploy and manage a Guardian watchdog process for OpenClaw Gateway with automated health monitoring, self-repair via `doctor --fix`, git-based workspace rollback, daily snapshots, and optional Discord alerting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoyeai](https://clawhub.ai/user/leoyeai)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up a watchdog for OpenClaw Gateway instances that need unattended health checks, repair attempts, workspace snapshots, and rollback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent unattended repair can reset Git state and restart processes without enough scoping or warning.

Mitigation: Review the Guardian script before installation, commit or back up important workspace changes, and enable rollback only where unattended reset behavior is acceptable.

Risk: Discord webhook alerts may share operational information with a third-party service.

Mitigation: Use Discord alerts only with an approved webhook and avoid placing sensitive data in alert content.

## Reference(s):

- [Openclaw Guardian on ClawHub](https://clawhub.ai/leoyeai/skills/openclaw-guardian-ultra)
- [Publisher profile](https://clawhub.ai/user/leoyeai)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
