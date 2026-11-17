## Description:

LocalUDPMessenger lets agents discover and exchange messages with other OpenClaw agents over a local UDP network with configurable trust, rate limits, logging, optional wake-up, and optional relay monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turfptax](https://clawhub.ai/user/turfptax)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to coordinate OpenClaw agents on a trusted LAN, discover peers, exchange messages, manage trusted peers, review logs, and configure wake-up or relay monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network messages can wake the agent and trigger agent activity when wake-up is enabled.

Mitigation: Enable hookToken only when automatic wake-up is required, keep peer approval strict, and review messages before acting on instructions from peers.

Risk: Approved or spoofed peers may send untrusted content that reaches the agent.

Mitigation: Use always-confirm on untrusted LANs, avoid relying on peer IDs as strong authentication, and require user approval before processing sensitive or unexpected peer messages.

Risk: Relay monitoring can forward full message contents to a configured monitor.

Mitigation: Keep relayServer disabled unless monitoring is needed, and do not send secrets, credentials, or private project data through UDP messages.

## Reference(s):

- [Local UDP Messenger repository](https://github.com/turfptax/openclaw-udp-messenger)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub LocalUDPMessenger page](https://clawhub.ai/turfptax/skills/localudpmessenger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces single-stream agent guidance and tool-use instructions; no model weights or binary artifacts.]

## Skill Version(s):

1.5.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
