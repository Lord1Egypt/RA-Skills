## Description:

Explore excursion options available for cruise travelers at various ports, enhancing your travel experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to explore cruise excursion options and query cruise product listings through a remote MCP integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to send analysis requests to an unrelated httpbin.org endpoint, which could expose travel plans, booking details, contact information, credentials, or other sensitive data.

Mitigation: Avoid entering booking references, contact details, credentials, or other sensitive information unless the publisher removes or clearly scopes that submission path and documents what data is sent where.

Risk: The skill depends on a remote cruise-search MCP integration, so user requests may be sent to an external gateway.

Mitigation: Install only if the remote integration and publisher are acceptable for the intended data and use case.

## Reference(s):

- [MCP Server Access](references/mcp.md)
- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/ola-cruise-excursion)
- [MCP Server Schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and MCP remote configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a remote streamable HTTP MCP endpoint for cruise excursion and product-list queries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
