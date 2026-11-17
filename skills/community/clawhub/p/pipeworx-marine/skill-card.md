## Description:

Marine MCP wraps marine-api.open-meteo.com for free, no-auth marine wave forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can configure an agent to reach the Pipeworx marine MCP connector and request marine wave forecast data without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs an unpinned npm package from the network with local user privileges.

Mitigation: Use a pinned, reviewed version of `mcp-remote` or run the connector in a restricted environment with minimal filesystem and environment-variable access.

Risk: Requests pass through the Pipeworx gateway.

Mitigation: Avoid sending sensitive locations or unrelated private context unless the gateway's handling of request data is trusted.

## Reference(s):

- [Pipeworx marine pack](https://pipeworx.io/packs/marine)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-marine)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON configuration snippets and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exposes MCP tools for wave forecasts and current wave conditions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
