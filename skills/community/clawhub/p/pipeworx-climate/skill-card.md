## Description:

Long-range climate projections from Open-Meteo - temperature trends from 1950 to 2050 with multi-model comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and climate-risk analysts use this skill to retrieve long-range temperature projections for locations worldwide and compare climate model outputs for planning, research, real estate, or agriculture assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to run a mutable npm package automatically through mcp-remote@latest.

Mitigation: Review the MCP setup before installing, prefer pinning mcp-remote to a reviewed exact version or locked dependency, and run the MCP server with only the files and credentials needed for climate queries.

## Reference(s):

- [Pipeworx Climate Pack](https://pipeworx.io/packs/climate)

## Skill Output:

**Output Type(s):** [Text, Configuration, API calls]

**Output Format:** [Markdown with JSON and bash examples; MCP tool responses return climate projection data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented example and an MCP setup that uses mcp-remote.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
