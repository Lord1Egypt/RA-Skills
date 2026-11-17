## Description:

Network health monitoring with latency and reachability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose Pilot Protocol connectivity, latency, throughput, routing, daemon health, active connections, and known peers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose Pilot Protocol connection and known-peer metadata during diagnostics.

Mitigation: Use it only where that metadata is not sensitive or where the operator is authorized to inspect it.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-health)
- [Publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented diagnostic examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pilotctl --json commands and assumes jq-style inspection in examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
