## Description:

Send messages to a local OpenClaw/Rook gateway and receive responses directly from Claude Code, enabling bidirectional agent-to-agent communication through the openclaw agent CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to send messages to a local OpenClaw/Rook gateway, request second opinions, delegate tasks, and hand off context between agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages and file excerpts sent through the bridge may expose secrets or private context to the local gateway and downstream agents.

Mitigation: Review the exact payload before sending, avoid credentials and private notes, and share file paths or minimal excerpts only when necessary.

Risk: The documented shell examples interpolate user text into commands, which can be unsafe with untrusted text.

Mitigation: Use safer argument handling or careful quoting, and do not paste untrusted text directly into shell command templates.

Risk: The local gateway must be trusted and available for the skill to behave as expected.

Mitigation: Run a gateway health check before use and stop if the gateway is unreachable.

## Reference(s):

- [Openclaw Bridge on ClawHub](https://clawhub.ai/nerua1/skills/openclaw-bridge)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and parsed agent response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return one or more payload texts from the local OpenClaw gateway; no streaming is documented.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
