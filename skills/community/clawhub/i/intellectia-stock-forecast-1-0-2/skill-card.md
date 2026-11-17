## Description:

Provides Intellectia API forecasts and "Should I Buy?" analysis for single stock, ETF, or crypto tickers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renixaus](https://clawhub.ai/user/renixaus)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to request informational single-symbol market forecasts and structured buy-rationale summaries from the Intellectia API. It supports stock, ETF, and crypto ticker questions where the output should include predictions, probability, target-price context, catalysts, ratings, or a buy/not-buy rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send requested ticker details to the Intellectia API.

Mitigation: Use it only when sharing the requested ticker with Intellectia is acceptable.

Risk: Market forecasts, predictions, and buy-rationale outputs may be delayed, incomplete, or wrong and are not investment advice.

Mitigation: Treat responses as informational research, verify data with authoritative sources, and consult a qualified professional before financial decisions.

Risk: The OpenClaw metadata installs the Python requests dependency without a pinned version.

Mitigation: Install in a controlled environment and review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renixaus/skills/intellectia-stock-forecast-1-0-2)
- [Intellectia API base URL](https://api.intellectia.ai)
- [Forecast endpoint](https://api.intellectia.ai/gateway/v1/stock/screener-public)
- [Should I Buy endpoint](https://api.intellectia.ai/gateway/v1/finance/should-i-buy)
- [Intellectia real-time data page](https://intellectia.ai/?channelId=601&activityId=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API response summaries, ticker-specific forecast values, investment-rationale text, and setup commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
