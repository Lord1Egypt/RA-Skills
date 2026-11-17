## Description:

Provides Altos Research real estate market intelligence through MCP tools for market snapshots, inventory trends, listings, pending sales, new listings, and downloadable data files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting real estate workflows use this skill to query Altos market statistics, inventory trends, active listings, pending sales, new listings, and downloadable data catalogs for a requested region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a hosted Altos MCP endpoint, so live server behavior and returned data are controlled remotely.

Mitigation: Before installing or using it in production, confirm that the publisher and hosted endpoint are trusted for the intended real estate workflow.

## Reference(s):

- [Pipeworx altos ClawHub listing](https://clawhub.ai/brucegutman/skills/pipeworx-altos)
- [Altos MCP endpoint](https://gateway.pipeworx.io/altos/mcp)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown with JSON MCP server configuration and natural-language tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries a hosted Altos MCP endpoint for region-specific real estate market data.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
