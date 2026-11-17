## Description:

HTTP status code cat images - get a cat photo for any status code plus a reference of all common codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation authors, and operations teams use this skill to look up HTTP status-code meanings and retrieve matching http.cat image URLs for docs, alerts, teaching material, or dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented MCP configuration runs mcp-remote@latest through npx, which can change over time and executes locally with process privileges.

Mitigation: Pin and audit the mcp-remote package version, or use a client-native remote MCP configuration when available.

Risk: The bridge process may receive more local file or environment access than this status-code lookup use case needs.

Mitigation: Run the MCP bridge with minimal file-system and environment permissions.

Risk: The skill depends on a remote Pipeworx HTTP endpoint for status-code lookup behavior.

Mitigation: Review the endpoint before deployment and monitor availability or changes in returned status-code data.

## Reference(s):

- [Pipeworx httpcat homepage](https://pipeworx.io/packs/httpcat)
- [Pipeworx httpcat MCP endpoint](https://gateway.pipeworx.io/httpcat/mcp)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [JSON tool responses with status-code descriptions and image URLs, plus Markdown examples for shell commands and MCP configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for the documented example call; MCP setup uses a remote Pipeworx HTTP endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
