## Description:

Deploy an MCP and A2A bridge fleet with three agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a three-agent Pilot fleet that bridges MCP tool servers and Google A2A agents through a shared tool registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures trusted networked agents and cross-protocol routing, so confidential tool inputs or outputs may pass through Pilot tunnels and peer links.

Mitigation: Verify each peer's identity during mutual handshakes, and route confidential data only after the Pilot transport, trust model, logging, and local manifest permissions meet requirements.

Risk: The setup installs multiple add-on skills without pinned versions in the artifact commands.

Mitigation: Pin or verify installed skills where possible before deployment, especially in sensitive environments.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-mcp-bridge-fleet-setup)
- [ClawHub publisher profile](https://clawhub.ai/user/teoslayer)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, JSON manifests, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific setup instructions for a three-agent Pilot bridge fleet; requires pilotctl, clawhub, and a running Pilot daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
