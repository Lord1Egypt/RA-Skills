## Description:

Query real-time and historical financial data for equities, including prices, news, statements, metrics, estimates, ownership activity, SEC filings, earnings releases, screening, and macro interest rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve equity market data from AIsa for investment research, alerts, screening, and reporting workflows. It supports both curl examples and a Python CLI for querying prices, company news, financial statements, filings, estimates, ownership data, and macro interest rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires runtime access to AISA_API_KEY and sends ticker symbols, filters, dates, and usage metadata to AIsa.

Mitigation: Use a scoped or replaceable API key, avoid confidential trading strategies or sensitive watchlists unless the provider relationship is acceptable, and rotate the key if exposure is suspected.

Risk: Pay-as-you-go API calls can incur usage costs.

Mitigation: Monitor response usage fields and account credits, and set operational limits around automated or repeated queries.

Risk: The earnings press releases endpoint has narrower ticker coverage and returns an invalid ticker error for unsupported symbols.

Mitigation: Check the supported ticker list before using that endpoint, and fall back to analyst estimates or income statements when coverage is unavailable.

## Reference(s):

- [AIsa homepage](https://aisa.one)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [Earnings Press Releases Supported Tickers](earnings-press-releases-tickers.md)
- [Financial Datasets earnings press releases tickers](https://api.financialdatasets.ai/earnings/press-releases/tickers)
- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/openclaw-aisa-finance-equity-price-market-data-news)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include API request examples, JSON response guidance, endpoint parameters, and cost or credential notes.]

## Skill Version(s):

2.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
