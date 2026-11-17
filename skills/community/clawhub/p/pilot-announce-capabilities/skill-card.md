## Description:

Broadcast structured capability manifests to the network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to advertise services, resources, APIs, pricing, and SLAs through Pilot Protocol capability manifests so other peers can discover available agent capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Capability manifests can expose infrastructure or business details such as hostnames, node IDs, endpoints, regions, GPU inventory, pricing, or SLA commitments to Pilot Protocol peers or registries.

Mitigation: Review each manifest before publishing, remove details that should not be visible externally, and treat registry targets as external recipients.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-announce-capabilities)
- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl on PATH, a running daemon, and a registry or target that accepts capability announcements.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
