## Description:

OpenClaw Deck launches a local multi-column web UI for managing and chatting with OpenClaw agents side by side.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to start a local chat deck, connect to an OpenClaw Gateway, and manage side-by-side conversations with one or more agent columns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway tokens and connection targets may be exposed through URLs or shared deck links.

Mitigation: Use environment configuration for tokens, avoid shared links with gateway or token parameters, and keep the gateway bound to localhost unless a broader binding is intentional.

Risk: The deck connects to a configurable gateway and can interact with local agent sessions.

Mitigation: Install only from a trusted publisher, run it in a controlled local environment, and verify any custom VITE_GATEWAY_URL before use.

Risk: The release depends on local Vite and build dependencies.

Mitigation: Review and update the Vite/build dependencies before broader deployment.

## Reference(s):

- [OpenClaw Deck on ClawHub](https://clawhub.ai/kellyclaudeai/skills/openclaw-deck)
- [kellyclaudeai Publisher Profile](https://clawhub.ai/user/kellyclaudeai)
- [OpenClaw Architecture Documentation](https://docs.openclaw.ai/concepts/architecture)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands, local URL, and shortcut guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, npm, and a running OpenClaw Gateway at ws://127.0.0.1:18789 or a configured VITE_GATEWAY_URL.]

## Skill Version(s):

0.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
