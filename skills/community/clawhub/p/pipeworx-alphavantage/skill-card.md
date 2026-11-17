## Description:

Access real-time stock prices, historical data, company fundamentals, financial statements, and earnings for stock symbols through an Alpha Vantage MCP connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve market data, company fundamentals, financial statements, and earnings information for stock symbols through a configured MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols and MCP request metadata may be sent to the disclosed remote gateway.

Mitigation: Review data-sharing expectations before installation and avoid sending symbols or request context that should not leave the environment.

Risk: Financial data is provided through a remote service and may be unsuitable as the sole basis for important financial decisions.

Mitigation: Verify important financial decisions against trusted sources before acting on the output.

## Reference(s):

- [Pipeworx alphavantage on ClawHub](https://clawhub.ai/brucegutman/skills/pipeworx-alphavantage)
- [Publisher profile](https://clawhub.ai/user/brucegutman)
- [Alpha Vantage MCP Gateway](https://gateway.pipeworx.io/alphavantage/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration]

**Output Format:** [Markdown or text responses from MCP market-data calls, plus JSON MCP server configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial data is retrieved through the disclosed remote Pipeworx Alpha Vantage MCP gateway.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
