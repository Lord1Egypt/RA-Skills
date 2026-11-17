## Description:

Configures multiple OpenClaw Gateway agents so each agent can be bound to a separate Feishu bot account with isolated identity and workspace state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kolikoliko](https://clawhub.ai/user/kolikoliko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up multiple independent OpenClaw agents behind one Gateway and route different Feishu bot accounts to different agents. It is useful when teams need separate assistant identities, memories, workspaces, or models for different Feishu users or workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secret values may be exposed through shared configuration files or backups.

Mitigation: Keep ~/.openclaw/openclaw.json private, restrict file permissions, avoid committing it, and encrypt backups that include OpenClaw configuration or agent workspaces.

Risk: Restore commands can overwrite active OpenClaw configuration and Gateway restarts can interrupt service.

Mitigation: Create a current backup before restoring configuration, verify the target backup file, and plan Gateway restarts during an acceptable maintenance window.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kolikoliko/skills/multi-agent-feishu)
- [Configuration fields](references/config-fields.md)
- [Feishu bot creation guide](references/feishu-app.md)
- [Architecture](references/architecture.md)
- [FAQ](references/faq.md)
- [Backup and restore](references/backup.md)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only setup guidance; no tool or API calls are executed by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
