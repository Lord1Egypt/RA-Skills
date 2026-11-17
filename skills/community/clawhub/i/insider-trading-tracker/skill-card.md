## Description:

Track insider trading from SEC Form 4 filings: insider buying and selling by ticker, market-wide insider activity, cluster buy signals where 3 or more insiders buy the same stock, and 10b5-1 plan detection for officer, director, and 10% owner trades. Read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and financial researchers use this skill to review public insider transaction disclosures by ticker or across the market, identify cluster buying, and distinguish planned sales from other reported activity. It provides informational context and does not offer personalized investment advice or place trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries sent to the SentiSense API reveal the requested tickers or insider-activity questions to that service.

Mitigation: Use a dedicated SentiSense API key and avoid including sensitive information in requests.

Risk: Free-tier preview results may omit filings, so a partial result can be mistaken for a complete view of insider activity.

Mitigation: Clearly label preview results and do not make whole-window claims from a truncated slice.

Risk: Readers could mistake public filing summaries for personalized investment recommendations.

Mitigation: Present the results as informational context only, distinguish transaction types, and do not infer motives or recommend trades.

## Reference(s):

- [SentiSense API documentation](https://sentisense.ai/docs/api/#full-sample-responses-with-a-free-key)
- [Get a SentiSense API key](https://app.sentisense.ai/get-api-key)
- [SentiSense](https://sentisense.ai)
- [ClawHub skill release](https://clawhub.ai/thesentitrader/skills/insider-trading-tracker)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown]

**Output Format:** [Markdown summaries of SEC Form 4 data returned by the SentiSense API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational and educational; read-only. Free-tier market-wide endpoints may return only a preview slice.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
