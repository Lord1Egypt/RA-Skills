## Description:

Cross-platform prediction market data via AIsa API. Query Polymarket and Kalshi markets, prices, orderbooks, candlesticks, positions, and trades. Use when user asks about: prediction market odds, election betting, event probabilities, market sentiment, Polymarket prices, Kalshi prices, sports betting odds, wallet PnL, or cross-platform market comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query prediction market odds, market details, prices, orderbooks, candlesticks, trades, wallet positions, and cross-platform sports market matches from Polymarket and Kalshi through AIsa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prediction-market queries, market IDs, wallet addresses, and the AIsa API key are sent to api.aisa.one.

Mitigation: Use the skill only when that disclosure is acceptable, keep the API key in the AISA_API_KEY environment variable, and avoid submitting sensitive wallet addresses.

Risk: Wallet lookup commands can reveal financial activity to the API provider.

Mitigation: Limit wallet, position, and PnL lookups to addresses the user is authorized to analyze.

## Reference(s):

- [Prediction Market Data on ClawHub](https://clawhub.ai/bibaofeng/skills/prediction-market-data)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa](https://aisa.one)
- [Polymarket](https://polymarket.com)
- [Kalshi](https://kalshi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an AISA_API_KEY environment variable; API responses include usage cost and remaining credits when returned by the provider.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
