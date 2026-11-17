## Description:

Connect AI smart glasses to OpenClaw via Companion App with linkCode pairing, a chat API, and SSE streaming for voice-controlled AI conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orideclaw](https://clawhub.ai/user/orideclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw gateway operators use this skill to connect Nimo AI smart glasses through a companion app, pair sessions, and route chat requests to an AI agent with JSON or streaming responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pairing and deployment defaults may expose sensitive gateway access too broadly.

Mitigation: Use a strong unique gateway token and keep the gateway on localhost or behind TLS, VPN, or firewall rules before deployment.

Risk: The health endpoint exposes the current linkCode during initial pairing.

Mitigation: Remove linkCode from unauthenticated health output or restrict that endpoint before enabling the plugin on a reachable gateway.

Risk: The deployment script includes broad cleanup behavior and unpinned OpenClaw installation or update commands.

Mitigation: Review the script before running it, avoid the cleanup option unless intentional, and pin the OpenClaw package version used for deployment.

## Reference(s):

- [Nimo AI Glasses on ClawHub](https://clawhub.ai/orideclaw/skills/nimo-glasses)
- [Artifact README](artifact/README.md)
- [OpenClaw plugin manifest](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and SSE text chunks, with Markdown installation and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to be concise and are controlled by the plugin's maxResponseLength setting.]

## Skill Version(s):

0.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
