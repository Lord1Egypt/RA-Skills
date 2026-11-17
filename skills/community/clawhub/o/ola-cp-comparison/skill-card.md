## Description:

Helps agents compare cruise products by price, itinerary, brand, departure city, destination, duration, cruise line, and date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and travel-focused agents use this skill to search and compare cruise products across multiple criteria so they can make more informed cruise selection decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise search criteria are sent to the disclosed CruiseSkillBridge/olavacations remote MCP endpoint.

Mitigation: Install only when users are comfortable sharing those criteria with the remote service, and review the disclosed endpoint before use.

Risk: Some documentation remains Chinese-only or template-like, which can make review harder for non-Chinese-speaking users.

Mitigation: Review the included MCP reference and publisher information before deployment, and request clearer localization from the publisher when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/ola-cp-comparison)
- [MCP Server Access](references/mcp.md)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [MCP Server Schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Markdown or plain text with MCP tool call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill exposes a remote product_list MCP tool for multi-criteria cruise product filtering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
