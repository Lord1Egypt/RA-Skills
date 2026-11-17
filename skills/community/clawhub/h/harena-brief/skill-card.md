## Description:

Harena Brief generates Chinese structured investment briefs from financial symbols or news-event keywords by retrieving market and news data through a remote MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allenzhang79](https://clawhub.ai/user/allenzhang79)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request concise Chinese investment analysis briefs for cryptocurrency symbols, U.S. stock symbols, or market-moving event keywords. The skill is suited for personal research workflows and should not be treated as verified financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried symbols, event keywords, and related request metadata are sent to an externally hosted MCP service.

Mitigation: Avoid confidential portfolio details or sensitive strategy information when using the skill.

Risk: The remote implementation can change outside the reviewed artifact, and generated financial analysis is unverified.

Mitigation: Review outputs against independent market and news sources before acting on them.

Risk: The documented privacy claims are not fully supported by the reviewed data flow evidence.

Mitigation: Treat privacy assurances as publisher claims unless independently validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allenzhang79/skills/harena-brief)
- [Harena Brief homepage](https://github.com/allenzhang79/harena-brief)
- [Remote MCP server](https://web-production-cf0c41.up.railway.app/mcp)
- [CoinGecko](https://www.coingecko.com)
- [CoinDesk](https://www.coindesk.com)
- [Alpha Vantage](https://www.alphavantage.co)
- [Google News](https://news.google.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured investment brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language brief for up to six financial symbols or event keywords per request.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
