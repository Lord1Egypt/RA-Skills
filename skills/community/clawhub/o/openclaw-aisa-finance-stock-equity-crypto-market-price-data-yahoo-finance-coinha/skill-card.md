## Description:

Query real-time and historical financial data across equities and crypto-prices, market moves, metrics, and trends for analysis, alerts, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve stock and crypto prices, market news, financial statements, metrics, filings, ownership data, analyst estimates, screeners, and interest-rate data through the AIsa/OpenClaw market-data service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ticker and filter requests to the AIsa/OpenClaw market-data service using the user's AISA_API_KEY.

Mitigation: Use an API key scoped to this service, store it as an environment variable, and monitor API credit usage.

Risk: Prompts or screener filters could include unrelated personal, brokerage, or account data.

Mitigation: Limit prompts and filters to market-data queries and avoid sending personal, brokerage, or account information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-finance-stock-equity-crypto-market-price-data-yahoo-finance-coinhacko)
- [OpenClaw](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, Python client commands, and JSON API responses from the market-data service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, curl, and an AISA_API_KEY; API responses include usage cost and remaining credits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
