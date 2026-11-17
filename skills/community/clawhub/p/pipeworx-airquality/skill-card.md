## Description:

Air Quality MCP wraps air-quality-api.open-meteo.com through the Pipeworx open MCP gateway with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query air quality information through a JSON-RPC 2.0 MCP endpoint, including listing tools and calling the Pipeworx airquality gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP client setup uses npx -y mcp-remote@latest, which auto-downloads an unpinned npm package.

Mitigation: Pin mcp-remote to a reviewed version before use, or run it only in a restricted environment with limited file, environment-variable, and credential access.

## Reference(s):

- [Pipeworx Airquality Homepage](https://pipeworx.io/packs/airquality)
- [Pipeworx Open MCP Gateway](https://pipeworx.io)
- [Pipeworx Airquality MCP Endpoint](https://gateway.pipeworx.io/airquality/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON-RPC 2.0 responses from the remote MCP gateway]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
