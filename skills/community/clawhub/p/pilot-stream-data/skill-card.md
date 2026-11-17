## Description:

Real-time NDJSON data streaming over persistent Pilot Protocol connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to stream structured NDJSON data, such as sensor readings, logs, or metrics, over persistent Pilot Protocol connections with backpressure-aware bidirectional communication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples can stream sensitive structured data to a configured Pilot Protocol destination.

Mitigation: Verify the destination and avoid sending sensitive stream data unless the receiving endpoint is trusted and expected.

Risk: The documented listener writes to a fixed /tmp log path and the producer loop can run indefinitely.

Mitigation: Use a private temporary path or direct processing for logs, and stop background listeners or producer loops when the streaming task is complete.

Risk: The skill depends on an existing pilotctl binary and running daemon.

Mitigation: Install and trust the Pilot Protocol tooling separately, then confirm the daemon state before following the command examples.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command-oriented streaming patterns for agents using pilotctl, jq, bc, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
