## Description:

Deploys a four-agent disaster response coordination system for sensor aggregation, response coordination, resource allocation, and public communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and emergency-management operators use this skill to configure a coordinated Pilot Protocol deployment across sensor, coordination, resource-allocation, and communications agents. It helps set hostnames, install role-specific skills, establish trust handshakes, and verify connectivity for disaster-response workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports high-impact public-safety communications where incorrect alerts or resource instructions could cause harm.

Mitigation: Use test deployments first and require human approval before public alerts or operational resource decisions.

Risk: Peer trust and dependent skills may be under-scoped for real emergency or public-facing environments.

Mitigation: Verify every peer identity out of band before handshakes, and pin and verify all dependent skills before installation.

Risk: Slack and webhook bridges can send sensitive or incorrect coordination data to unintended destinations.

Mitigation: Restrict allowed Slack and webhook destinations and review channel mappings before enabling live communications.

Risk: The saved setup manifest may expose operational details after deployment.

Mitigation: Protect the manifest at rest and remove it when it is no longer needed.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON manifest examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup instructions for sensor-hub, coordinator, resource-allocator, and comms agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
