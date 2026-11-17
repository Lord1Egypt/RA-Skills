## Description:

Match agents with complementary capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators use this skill to discover, rank, and select peer agents by capability requirements, trust status, latency, pricing, and service expectations for delegation or team formation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example trust scoring can misclassify an untrusted peer as trusted if a peer ID is crafted maliciously.

Mitigation: Compare node IDs as exact literals and preserve JSON values safely before using trust ranking for real delegation.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline bash commands and workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl, a running daemon, jq, and bc.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
