## Description:

将 OpenClaw 连接到 Clawhome 聊天平台，实现 AI 自动回复。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengguo](https://clawhub.ai/user/shengguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw Gateway to the Clawhome messaging platform for bidirectional channel messaging and AI auto-replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs mutable remote packages and loads an unpinned OpenClaw plugin.

Mitigation: Review before installing, use only if the Clawhome package publisher and OpenClaw plugin source are trusted, prefer a pinned reviewed version, and verify package and plugin provenance.

Risk: The configured `channelSecret` is sensitive and the installed plugin persists while processing messaging traffic.

Mitigation: Treat `channelSecret` like a password and run the OpenClaw Gateway with least privilege.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shengguo/skills/openclaw-clawhome-cli)
- [OpenClaw install documentation](https://docs.openclaw.ai/install)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw plugin installation, Gateway restart, MQTT topic, heartbeat, message, and channel credential configuration guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
