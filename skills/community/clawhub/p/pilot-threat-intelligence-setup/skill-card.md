## Description:

Deploys a four-agent threat intelligence setup for IOC collection, enrichment, analysis, and distribution to security infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to configure collector, enricher, analyzer, and distributor agents for a threat intelligence pipeline. It helps coordinate IOC aggregation, contextual enrichment, severity analysis, peer handshakes, and downstream STIX/TAXII, SIEM, firewall, or IDS/IPS distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable dependencies installed through ClawHub may change behavior if versions and publishers are not verified.

Mitigation: Confirm exact dependency versions and publishers before installation, especially for role-specific skills installed by the collector, enricher, analyzer, and distributor.

Risk: Incorrect peer handshakes can establish trust with unintended agents in the threat intelligence pipeline.

Mitigation: Verify peer hostnames and identities before initiating handshakes, then inspect trust state with pilotctl before sending IOC data.

Risk: Distributor output can affect production SIEM, firewall, IDS/IPS, or STIX/TAXII destinations.

Mitigation: Test distributor behavior in a non-production environment and ensure each external destination is approved and reversible before enabling live publication.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-threat-intelligence-setup)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup steps, peer handshake guidance, and manifest templates; no credentials are embedded in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
