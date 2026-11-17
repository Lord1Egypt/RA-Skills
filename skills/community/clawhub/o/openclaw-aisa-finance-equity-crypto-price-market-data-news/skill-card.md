## Description:

Query real-time and historical financial data across equities and crypto prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to retrieve equity and cryptocurrency prices, market news, financial statements, analyst estimates, filings, ownership data, screening results, and related market metrics for analysis, alerts, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market research requests, ticker lists, dates, screening filters, and the AISA bearer token are sent to the third-party AISA API.

Mitigation: Install only where api.aisa.one is approved, and avoid sending confidential trading strategies or sensitive internal watchlists unless that service is approved for the environment.

Risk: The skill is designed for financial-data lookup and may return market data that users could over-rely on for investment decisions.

Mitigation: Use the returned data as an input to analysis and reporting workflows, with independent review before trading, portfolio, or compliance decisions.

Risk: Command outputs and logs may contain ticker lists, dates, filters, account usage data, or other market research context.

Mitigation: Treat generated commands, API responses, and captured logs as potentially sensitive and apply normal token and data-handling controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-finance-equity-crypto-price-market-data-news)
- [OpenClaw](https://openclaw.ai)
- [AISA API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AISA](https://aisa.one)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python command examples; API and client calls return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to api.aisa.one.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
