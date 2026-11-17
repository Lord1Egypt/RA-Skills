## Description:

Discover craft breweries across the US by name, city, or ID via Open Brewery DB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to search US brewery data by name, city, or ID for trip planning, craft beer finder features, contact lookup, or brewery-type analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client configuration runs an automatically downloaded unpinned npm package with local user privileges.

Mitigation: Prefer a pinned mcp-remote version or a controlled preinstall before enabling the MCP server.

Risk: Brewery search fields may send user-provided text to a remote service.

Mitigation: Avoid sending personal or confidential text in brewery lookup queries.

## Reference(s):

- [Pipeworx Breweries Pack](https://pipeworx.io/packs/breweries)
- [Pipeworx Breweries MCP Gateway](https://gateway.pipeworx.io/breweries/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks; MCP tool calls return structured brewery records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include brewery name, type, address, city, state, postal code, phone, website URL, and coordinates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
