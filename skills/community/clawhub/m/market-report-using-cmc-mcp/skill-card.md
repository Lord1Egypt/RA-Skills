## Description:

Generates a comprehensive crypto market report using CoinMarketCap MCP data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryan-cmc](https://clawhub.ai/user/bryan-cmc)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate concise or full crypto market reports covering market health, BTC and ETH anchors, technicals, leverage, trending narratives, and upcoming catalysts from CoinMarketCap MCP data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends relevant market-summary prompts to the configured CoinMarketCap MCP service.

Mitigation: Install and invoke the skill only when that data flow is acceptable, preferably through an explicit request such as /market-report.

Risk: A report may be incomplete if one or more CoinMarketCap MCP tools fail.

Mitigation: Use the skill's partial-report behavior and clearly note unavailable sections before relying on the report.

## Reference(s):

- [CoinMarketCap MCP endpoint](https://mcp.coinmarketcap.com/mcp)
- [CoinMarketCap API key login](https://pro.coinmarketcap.com/login)
- [ClawHub skill page](https://clawhub.ai/bryan-cmc/skills/market-report-using-cmc-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown market report with structured sections and concise bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May provide a partial report when one or more CoinMarketCap MCP tools are unavailable.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
