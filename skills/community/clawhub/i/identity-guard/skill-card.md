## Description:

Identity Guard blocks sensitive OpenClaw requests unless the sender is authorized by sender_id rather than display name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhongxuyang](https://clawhub.ai/user/zhongxuyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to gate sensitive owner, memory, configuration, and host-operation requests on trusted sender_id metadata. It is intended for multi-user or group-chat environments where display names and self-claims are not reliable authorization signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorization controls are broad enough to affect sensitive owner information and broader agent actions.

Mitigation: Review and narrow the trigger scope before deployment so the guard applies only to clearly sensitive requests and security-critical actions.

Risk: Shell, awk, and sed parsing can make authorization checks fragile.

Mitigation: Replace text parsing with structured JSON parsing and exact equality checks for sender_id, channel, master_id, and allowlist values.

Risk: Session logs are not strong proof of the current caller identity.

Mitigation: Use trusted current-message metadata for sender_id and channel, and treat missing or untrusted metadata as unauthorized.

Risk: Allowlist or master_id changes can expand access to protected information and actions.

Mitigation: Restrict identity configuration changes to an explicit trusted administrator process and review identities.json after updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhongxuyang/skills/identity-guard)
- [Publisher profile](https://clawhub.ai/user/zhongxuyang)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authorization decisions are represented by shell exit codes; helper scripts can create or update identities.json.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
