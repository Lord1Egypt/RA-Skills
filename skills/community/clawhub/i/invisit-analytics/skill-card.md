## Description:

Read and act on a site’s invisit analytics (visitors, sources, AI referrals, funnels, revenue, web vitals) through the invisit MCP server or REST API. Use when asked about traffic, conversions or revenue of a site measured with invisit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berkinory](https://clawhub.ai/user/berkinory)

### License/Terms of Use:

MIT-0

## Use Case:

External site owners, analysts, and developers can use an assistant to inspect traffic, conversions, revenue, funnels, AI referrals, and site health for an invisit-measured site. The skill guides site selection, date ranges, authentication, permissions, and querying through MCP or REST.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the external MCP or REST API involves granting access and may require sending a personal token or site API key as a bearer credential.

Mitigation: Review the consent screen and grant only the access needed; keep bearer credentials private and follow the documented scopes.

## Reference(s):

- [Invisit MCP endpoint](https://app.invisit.dev/mcp)
- [Invisit MCP API documentation](https://invisit.dev/docs/api/mcp.md)
- [Invisit REST OpenAPI document](https://api.invisit.dev/openapi/json)
- [Invisit REST API documentation](https://invisit.dev/docs/api/rest.md)
- [ClawHub release page](https://clawhub.ai/berkinory/skills/invisit-analytics)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Text or Markdown analytics summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected site, time window, permissions, and available analytics data.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
