## Description:

US economic indicators from the Bureau of Labor Statistics — unemployment, CPI, and employment by industry

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and analysts use this skill to query official US economic indicators, including unemployment, CPI, employment by industry, and arbitrary BLS time series, through Pipeworx MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup launches an unpinned npm MCP bridge with mcp-remote@latest.

Mitigation: Pin mcp-remote to a reviewed exact version, preinstall it through a controlled process, and run it under a least-privilege account.

Risk: Economic query arguments are sent to the Pipeworx gateway.

Mitigation: Avoid sending sensitive or confidential query context and review whether outbound requests to the Pipeworx gateway are acceptable for the deployment environment.

Risk: Security evidence marks the release verdict as suspicious.

Mitigation: Install only after reviewing the Pipeworx service, the MCP bridge dependency, and local execution permissions.

## Reference(s):

- [Pipeworx econdata homepage](https://pipeworx.io/packs/econdata)
- [Pipeworx econdata MCP gateway](https://gateway.pipeworx.io/econdata/mcp)
- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-econdata)
- [Publisher profile](https://clawhub.ai/user/b-gutman)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with JSON configuration and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for direct examples and an MCP client configuration that launches mcp-remote for agent tool access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
