## Description:

Secure outbound-only relay for remote OpenClaw control without exposed ports, SSH, or Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-czar](https://clawhub.ai/user/jason-czar)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use PrivaClaw to connect headless or server-deployed OpenClaw nodes to a trusted relay for remote prompts, workflow triggers, health checks, and restarts without exposing inbound infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote relay commands can control prompts, workflows, status checks, and restarts on the OpenClaw node.

Mitigation: Use only a relay operator you trust and deploy only with clear command-level authorization controls.

Risk: The AUTH_TOKEN is a secret that authenticates the node to the relay and could expose node control if leaked.

Mitigation: Keep the token secret, rotate it regularly, and avoid logging or sharing configuration that contains it.

Risk: The security evidence warns that command dispatch lacks an authenticated-state gate.

Mitigation: Avoid production use until the maintainer adds an authenticated-state gate before dispatching commands.

Risk: Non-TLS relay URLs weaken the intended secure transport posture.

Mitigation: Require wss:// relay URLs for deployed use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jason-czar/skills/privaclaw)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Configuration]

**Output Format:** [WebSocket JSON messages with streamed text responses and status or completion payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RELAY_URL, NODE_ID, and AUTH_TOKEN; sends node identity, heartbeat data, command status, and prompt response tokens through the configured relay.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
