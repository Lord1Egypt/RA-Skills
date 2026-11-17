## Description:

Install and manage Paw, a standalone web chat frontend for OpenClaw Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oriliz](https://clawhub.ai/user/oriliz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, update, or configure Paw as a browser-based chat interface for an OpenClaw Gateway. It supports local static hosting or deployment into the Gateway control UI directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway tokens can grant broad access to chats, agent settings, and scheduled-task controls if exposed.

Mitigation: Use Paw only from a trusted local or HTTPS-served page, prefer wss:// for non-local Gateways, never paste the token into an untrusted Paw page, and rotate any token that may have been exposed.

Risk: The Paw UI can modify agent behavior and manage scheduled tasks.

Mitigation: Treat the UI as an administrative surface and restrict access to users who are authorized to read chats, change agent behavior, and manage scheduled tasks.

## Reference(s):

- [Paw Chat on ClawHub](https://clawhub.ai/oriliz/skills/paw-chat)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Project Repository](https://github.com/openclaw/openclaw)
- [Paw Package Repository](https://github.com/openclaw/paw.git)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local server URLs, Gateway WebSocket URL guidance, token setup steps, and install or update commands.]

## Skill Version(s):

1.0.6 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
