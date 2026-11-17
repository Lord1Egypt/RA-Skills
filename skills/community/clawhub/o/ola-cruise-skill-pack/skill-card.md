## Description:

A comprehensive skill pack for cruise enthusiasts, offering tools for searching, filtering, and exploring cruise products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[309441738](https://clawhub.ai/user/309441738)

### License/Terms of Use:

MIT

## Use Case:

External users and travel commerce agents use this skill to search cruise products, filter product lists by brand, departure city, destination, duration, cruise line, date, and price range, and retrieve cruise product details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cruise search inputs are sent to an external CruiseSkillBridge MCP gateway.

Mitigation: Confirm the remote gateway, data-sharing expectations, and installation comfort before use; avoid sending sensitive personal or payment data unless approved for this service.

Risk: The documentation is partly boilerplate and mixed-language.

Mitigation: Review the published tool behavior and configuration before deployment so users understand the exact cruise-search capabilities and endpoint behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/309441738/skills/ola-cruise-skill-pack)
- [Publisher Profile](https://clawhub.ai/user/309441738)
- [CruiseSkillBridge](https://cruiseskillbridge.com)
- [MCP Server Schema](https://static.modelcontextprotocol.io/schemas/2025-07-09/server.schema.json)
- [Cruise MCP Gateway](https://cruise-mcp.olavacations.com/api/gw/mcp/2b585d6a-f15c-4526-a204-27ff81ec92fd)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance with structured MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill uses a remote MCP gateway for cruise search and product-detail requests; no local file output is described.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and server.json list 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
