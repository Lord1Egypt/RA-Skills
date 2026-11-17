## Description:

Build, test, and deploy custom Linux ISOs with OpenFactory by creating VMs, running compliance tests, and managing recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziegenbalg](https://clawhub.ai/user/ziegenbalg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to create custom Linux ISO recipes, build images, launch VMs, run validation or compliance tests, and retrieve deployable artifacts through OpenFactory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example credentials or privileged administrative settings could be copied into real infrastructure.

Mitigation: Replace example passwords with SSH keys or unique secrets and review recipes before building deployable images.

Risk: VM controls can stop instances, force power off systems, or delete disks.

Mitigation: Require explicit user confirmation before deleting VM disks, force-stopping VMs, or stopping active test environments.

Risk: Images that auto-deploy services can introduce vulnerable or unintended infrastructure.

Mitigation: Use trusted OpenFactory accounts and endpoints, validate recipes, and review auto-deployed services before use.

## Reference(s):

- [OpenFactory homepage](https://openfactory.tech)
- [OpenFactory ClawHub skill page](https://clawhub.ai/ziegenbalg/skills/openfactory)
- [OpenFactory MCP endpoint](https://build.openfactory.tech/api/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with JSON configuration examples and API call plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include build recipes, VM operation steps, test workflows, and deployment guidance for OpenFactory.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
