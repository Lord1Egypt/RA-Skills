## Description:

Use when the user asks about U.S. equity perpetuals on Hyperliquid: trend, trading volume, open interest, funding rates or related news. Calls the Maneki AI agent through Finch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask for analysis of U.S. equity perpetuals on Hyperliquid, including trends, trading volume, open interest, funding rates, and related news, through Maneki AI on Finch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker and question details are sent to Finch and Maneki AI for analysis.

Mitigation: Do not include private account details or confidential trading information.

Risk: A paid run costs 0.01 USDC per run.

Mitigation: Use free runs unless the user explicitly approves a paid run.

Risk: The external MCP connection guide was unavailable during this review.

Mitigation: Review the connection instructions before adding the Finch MCP server.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/a0971025732-netizen/skills/hyperliquid-us-stock-perps)
- [Finch Maneki AI market analysis](https://www.finchtech.ai/market/chips/agent-eee98da7-f7b3-471b-b0e4-fdd2a617e436/run?utm_source=skill&utm_medium=agent&utm_campaign=toa_skills&utm_content=hyperliquid-us-stock-perps)
- [Finch MCP connection instructions](https://github.com/a0971025732-netizen/finch-agents/blob/main/CONNECT.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Plain-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ticker-specific market analysis; results are not guaranteed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
