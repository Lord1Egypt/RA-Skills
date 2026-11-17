## Description:

Real-time financial market data MCP server for stocks, crypto, forex quotes, klines, sector analysis, and fundamentals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infoway-api](https://clawhub.ai/user/infoway-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external MCP users use this skill to connect AI assistants to Infoway market data for real-time quotes, K-line charts, market overview, sector analysis, and company fundamentals. It is intended for market-data retrieval and analysis workflows that require an Infoway API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data queries and the Infoway API key are sent to a third-party service.

Mitigation: Use the skill only when Infoway's data-handling terms meet the deployment's needs, and avoid sending confidential trading strategies or non-public financial information.

Risk: Installing the MCP server connects an MCP client to a third-party Python package and SDK.

Mitigation: Pin a reviewed package version or use a locked environment before connecting it to production MCP clients.

## Reference(s):

- [Infoway API](https://infoway.io)
- [ClawHub Skill Page](https://clawhub.ai/infoway-api/skills/infoway-financial-data)
- [Package Repository](https://github.com/infoway-api/infoway-mcp-server)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [JSON-formatted text returned through MCP tool responses, with configuration snippets for MCP clients.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INFOWAY_API_KEY and sends market-data queries to the Infoway service.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
