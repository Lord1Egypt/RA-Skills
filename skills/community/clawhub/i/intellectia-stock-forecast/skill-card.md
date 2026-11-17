## Description:

Provides Intellectia API workflows for single-symbol stock, ETF, or crypto forecasts and structured "Should I Buy" analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xanxustan](https://clawhub.ai/user/xanxustan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Intellectia for ticker-level forecast data, probability estimates, technical ratings, and structured buy/no-buy rationale. It is intended for informational market analysis rather than personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker symbols and request details are sent to Intellectia's API.

Mitigation: Use only tickers and request details approved for sharing with the third-party API.

Risk: The API output is financial information that may be delayed or unsuitable for time-sensitive trading decisions.

Mitigation: Present results as informational only, avoid personalized investment advice, and verify time-sensitive data against authoritative sources.

Risk: The skill depends on the Python requests package when using Python examples.

Mitigation: Pin or pre-approve the requests dependency before installation in stricter environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xanxustan/skills/intellectia-stock-forecast)
- [xanxustan publisher profile](https://clawhub.ai/user/xanxustan)
- [Intellectia](https://intellectia.ai/?channelId=601&activityId=1)
- [Intellectia forecast endpoint](https://api.intellectia.ai/gateway/v1/stock/screener-public)
- [Intellectia should-i-buy endpoint](https://api.intellectia.ai/gateway/v1/finance/should-i-buy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with cURL and Python examples and summarized API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl or python3 with requests; sends ticker and request details to Intellectia's API.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
