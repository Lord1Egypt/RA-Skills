## Description:

Bridge A2A (Agent-to-Agent) protocol messages over Pilot tunnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect A2A agents across different networks by routing messages through Pilot's overlay network. It is intended for multi-agent systems that need reliable messaging when agents are not on the same local network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote A2A messages may trigger task processing from untrusted senders.

Mitigation: Use trusted Pilot peers only, apply sender allowlists, and validate message schemas before processing tasks.

Risk: Unbounded payloads or long-running task processing can affect listener reliability.

Mitigation: Constrain payload size, processing time, and listener behavior under explicit user control.

Risk: Unsafe JSON serialization in outbound responses can produce malformed or misleading messages.

Mitigation: Serialize outbound JSON with safe tooling instead of manual string interpolation.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl on PATH, a running pilotctl daemon, and A2A-compatible agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
