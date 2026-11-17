## Description:

Lark Multi Agent Factory helps configure multiple OpenClaw agents for the official @larksuite/openclaw-lark plugin, including Lark-specific threadSession, replyMode, and blockStreaming settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cchenwei](https://clawhub.ai/user/cchenwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to preview, create, list, remove, and adjust multiple OpenClaw agents backed by the official Lark plugin. It is intended for batch setup of Lark app credentials, channel settings, bindings, and local agent workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Lark app secrets and writes persistent agent configuration.

Mitigation: Use a protected config file instead of inline --config for real secrets, check permissions on ~/.openclaw/openclaw.json, and review saved configuration before use.

Risk: The skill can expand inter-agent communication by updating agentToAgent.allow.

Mitigation: Confirm automatic allow-list changes match the intended trust boundary before enabling the new agents.

Risk: Generated IDENTITY.md and SOUL.md files influence the behavior of newly created agents.

Mitigation: Inspect generated IDENTITY.md and SOUL.md files before using the new agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cchenwei/skills/lark-multi-agent-factory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local OpenClaw configuration and agent workspace files when the bundled setup script is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
