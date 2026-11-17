## Description:

Perform Google web and image searches -- retrieve ranked web results with titles, snippets, and URLs, or search for images with country and language targeting, result count control, and page-based pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to collect Google web and image search results through KeyAPI and synthesize search intelligence reports for content research, competitive analysis, SERP monitoring, and visual asset discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner requires a KeyAPI token and can persist credentials locally if entered interactively.

Mitigation: Set KEYAPI_TOKEN only in the current shell session, avoid interactive token entry, and remove any generated .env file after use.

Risk: Search requests and responses may be cached locally under .keyapi-cache/.

Mitigation: Treat cached search data as potentially sensitive and review or clear .keyapi-cache/ after use.

Risk: KEYAPI_SERVER_URL can redirect requests to a different MCP endpoint.

Mitigation: Do not set KEYAPI_SERVER_URL unless the endpoint is trusted.

Risk: The shipped runner can call broader KeyAPI MCP tools beyond the Google search framing.

Mitigation: Inspect available tools and schemas before use, and limit calls to the intended Google search tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lycici/skills/keyapi-google-search)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Google MCP Server](https://mcp.keyapi.ai/google/mcp)
- [KeyAPI MCP Base](https://mcp.keyapi.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses KEYAPI_TOKEN, Node.js, and locally cached KeyAPI MCP responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
