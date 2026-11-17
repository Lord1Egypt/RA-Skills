## Description:

Bidirectional bridge between Pilot Protocol and Discord servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and engineers use this skill to connect Pilot agents with Discord communities for outbound notifications, rich embeds, inbound message streams, and command-response workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent output, telemetry, or trusted channel content could be relayed to Discord beyond the intended audience.

Mitigation: Use a restricted webhook and channel scope, and avoid sending secrets or sensitive operational data through the bridge.

Risk: Inbound Discord commands could trigger unintended Pilot actions if command handling is too broad.

Mitigation: Validate and allowlist inbound commands before acting on them, and limit command responders to the minimum required behavior.

Risk: Discord webhook tokens can be exposed through shell history, logs, or copied command examples.

Mitigation: Provide webhook tokens through protected environment or secret storage and rotate any token that may have appeared in history or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-discord-bridge)
- [Pilot Protocol Homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [shell commands, configuration, code, guidance]

**Output Format:** [Markdown with bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, a Discord webhook URL, and a Discord bot for inbound relay workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
