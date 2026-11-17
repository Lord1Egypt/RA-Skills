## Description:

Complete OpenClaw setup automation skill that guides gateway installation, security hardening, model routing, channel setup, and starter workflow configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sepulchralvoid666](https://clawhub.ai/user/sepulchralvoid666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up OpenClaw, apply baseline gateway security, configure model routing, connect messaging channels, and deploy starter automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent main-session automations and messaging or mailbox integrations may operate with broad access and limited user-control safeguards.

Mitigation: Use pinned and verified OpenClaw and skill versions, prefer read-only and revocable credentials, and add approval, isolation, auditing, and a clear disable path before enabling main-session cron examples.

Risk: The security verdict is suspicious even though no specific risk findings were listed.

Mitigation: Review the skill carefully before installation and avoid granting calendar, mailbox, or messaging permissions until each integration's access scope is understood.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup guidance includes prerequisite checks, OpenClaw commands, configuration examples, workflow snippets, and verification steps.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
