## Description:

Fetches Nasdaq-100 futures quote data from the Yahoo Finance chart API and returns price, change, percent change, timestamp, and a human-readable summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbl581581](https://clawhub.ai/user/lbl581581)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to retrieve Nasdaq-100 futures quote metrics, or another Yahoo Finance symbol, for market-aware responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested ticker symbol is sent to Yahoo Finance.

Mitigation: Use only symbols that are acceptable to disclose to the external data provider, or restrict allowed symbols before deployment.

Risk: Responses are formatted in Chinese, which may not match all user locales.

Mitigation: Review or modify the message formatting before use in English-only or localized deployments.

Risk: Quote results depend on Yahoo Finance data availability, market hours, and network access.

Mitigation: Treat returned prices as external market data and verify critical financial decisions against an authoritative market data source.

## Reference(s):

- [OpenClaw runtime details](references/openclaw.md)
- [Yahoo Finance chart API endpoint](https://query1.finance.yahoo.com/v8/finance/chart/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON object with string-formatted quote fields and a human-readable message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Chinese-formatted success and failure messages; results depend on Yahoo Finance availability, market hours, and network access.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
