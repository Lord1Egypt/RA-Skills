## Description:

OpenClaw Session Inspector helps agents register tracked OpenClaw sessions, inspect stuck or inactive work, check the current session UUID, list status, and prepare platform-specific watcher services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netfeel-star](https://clawhub.ai/user/netfeel-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw agent sessions for inactivity or interrupted work, register and unregister tracked sessions, inspect status, and prepare an optional platform watcher service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent watcher can reactivate OpenClaw sessions and prompt host inspection or continued work without a fresh user decision.

Mitigation: Install and enable the watcher only when persistent monitoring is intended, review generated service files before enabling them, and keep start or enable actions tied to explicit user approval.

Risk: The runtime registry stores session and delivery metadata for monitored sessions.

Mitigation: Keep the runtime directory private, register only sessions suitable for monitoring, and disable or remove registrations when monitoring is no longer needed.

## Reference(s):

- [Inspector Runtime Design](artifact/references/config-fields.md)
- [ClawHub Skill Page](https://clawhub.ai/netfeel-star/skills/inspector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may update local runtime registry, state, logs, and optional watcher service files when executed.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
