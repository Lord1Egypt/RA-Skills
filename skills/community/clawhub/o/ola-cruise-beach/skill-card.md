## Description:

Explore cruise products specifically tailored for beach vacation enthusiasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External travelers and travel-planning agents use this skill to find cruise products for beach vacations and filter options by brand, departure city, price, destination, trip duration, cruise line, and date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote MCP endpoint can receive trip preferences and may receive unnecessary sensitive personal data if users over-share.

Mitigation: Send only the destination, dates, budget, and trip preferences needed for cruise search; do not send passwords, payment details, passport numbers, or other sensitive personal data.

Risk: The documentation is incomplete and still contains scaffold text, which can make behavior and data handling unclear.

Mitigation: Review the remote MCP endpoint before use and ask the publisher for a clear privacy and data-handling notice before relying on it for sensitive workflows.

## Reference(s):

- [MCP Server Access](references/mcp.md)
- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/ola-cruise-beach)
- [Model Context Protocol Server Schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and MCP configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a remote streamable HTTP MCP endpoint for cruise product lookup.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and server.json list package version 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
