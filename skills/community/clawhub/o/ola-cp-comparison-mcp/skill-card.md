## Description:

Cruise Product Comparison MCP Server - helps users compare cruise products by price, itinerary, and brand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this remote MCP connector to compare cruise products by price, itinerary, and brand before choosing a cruise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise-comparison requests are sent to a disclosed remote MCP service at olavacations.com.

Mitigation: Review data-sharing expectations and avoid sending sensitive travel or personal data unless approved.

Risk: The artifact is lightly documented for non-Chinese-speaking users.

Mitigation: Have a Chinese-speaking reviewer or publisher documentation confirm expected MCP behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/309441738/skills/ola-cp-comparison-mcp)
- [Publisher profile](https://clawhub.ai/user/309441738)
- [Remote MCP service](https://cruise-mcp.olavacations.com/api/gw/mcp/607dada7-85a0-4d70-b7df-bddcdec3009f)
- [MCP server schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Text returned through a remote MCP service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled local executable code or local persistence was found in the inspected artifact.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
