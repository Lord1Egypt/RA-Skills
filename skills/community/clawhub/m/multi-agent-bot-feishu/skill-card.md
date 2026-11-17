## Description:

Creates additional OpenClaw agents and binds them to Feishu bots or group chats for multi-bot routing, separate workspaces, and isolated conversation memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardcoder849](https://clawhub.ai/user/richardcoder849)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure additional OpenClaw agents for separate Feishu bots or group chats, with per-agent workspaces, message routing, and access controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app secrets and OpenClaw configuration values are sensitive and may be exposed if copied into shared files or version control.

Mitigation: Keep appSecret values private, avoid committing ~/.openclaw/openclaw.json, and store shared configuration examples with placeholders only.

Risk: Incorrect agent, account, or binding IDs can route Feishu messages to the wrong OpenClaw agent or workspace.

Mitigation: Verify JSON syntax, account IDs, agent IDs, and binding rules before restarting the OpenClaw gateway.

Risk: Overly broad Feishu access settings can allow unintended users or groups to interact with a configured agent.

Mitigation: Use restrictive allowlists for users and groups unless an open policy is explicitly required.

Risk: Configuration mistakes may disrupt an existing OpenClaw gateway setup.

Mitigation: Back up ~/.openclaw/openclaw.json before editing and restart the gateway only after reviewing the updated configuration.

## Reference(s):

- [Configuration template](references/config-template.json)
- [Feishu multi-bot configuration guide](https://docs.openclaw.ai/docs/feishu/multiple-bots)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/richardcoder849/skills/multi-agent-bot-feishu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only setup guidance; no tool calls or executable scripts are bundled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
