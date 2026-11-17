## Description:

Query real-time and historical financial data across equities and crypto, including prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to query AIsa market-data APIs for stock and cryptocurrency prices, financial statements, analyst estimates, filings, screening, and related market analysis. It is intended for workflows that need API-key-backed market data in shell, Python, or agent-generated reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-data queries and ticker lists are sent to the AIsa API using the user's API key.

Mitigation: Use the skill only when you trust AIsa/OpenClaw with those queries and avoid submitting private watchlists, strategies, or filters.

Risk: API calls may consume paid credits or quota.

Mitigation: Review planned requests before execution and monitor usage.cost and credits_remaining values returned by the service.

Risk: Financial data can be incomplete, delayed, or unsuitable as the sole basis for trading decisions.

Mitigation: Validate important outputs against authoritative market-data sources and apply human review before investment or compliance decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-market-pulse)
- [OpenClaw](https://openclaw.ai)
- [AIsa API Reference](https://docs.aisa.one/reference/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python commands; the bundled client prints JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY for authenticated AIsa API calls; uses curl or python3 depending on the workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
