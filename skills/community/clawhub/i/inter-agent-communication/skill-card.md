## Description:

Guides agents through creating, reusing, and protecting labeled subagent sessions for agent-to-agent communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panmenglin](https://clawhub.ai/user/panmenglin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to establish persistent, reusable communication channels between agents while avoiding reuse of human-agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and reuses long-lived subagent communication sessions.

Mitigation: Use it only when persistent agent-to-agent channels are intended, and require explicit approval before making sessions long-lived.

Risk: The session protection flow includes a local command path that can be unsafe with untrusted session keys.

Mitigation: Validate session keys, avoid passing untrusted values to shell commands, and prefer a scoped non-shell API with a clear undo path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panmenglin/skills/inter-agent-communication)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes session label and sessionKey handling guidance for OpenClaw subagent sessions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
