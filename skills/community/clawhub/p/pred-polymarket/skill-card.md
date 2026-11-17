## Description:

Prediction markets data - Polymarket, Kalshi markets, prices, positions, and trades

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search prediction markets, retrieve Polymarket and Kalshi prices, inspect historical market data, compare sports markets across platforms, and review wallet positions or P&L when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prediction-market searches, market IDs, wallet addresses, and the AISA API key are sent to AIsa.

Mitigation: Use the skill only when that data sharing is acceptable, keep the API key in environment variables, and avoid exposing secrets in prompts or logs.

Risk: Wallet lookups can reveal privacy-sensitive portfolio, activity, and P&L information.

Mitigation: Query third-party wallets only with a legitimate, authorized reason and limit sharing of returned wallet data.

Risk: The API documentation states a per-query cost.

Mitigation: Monitor usage cost and remaining credits, and apply limits or filters before running broad searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/pred-polymarket)
- [Publisher profile](https://clawhub.ai/user/aisadocs)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa signup](https://aisa.one)
- [OpenClaw homepage](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python command examples, JSON response examples, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AISA_API_KEY and read-only API requests for market, price, trade, orderbook, candlestick, sports matching, and wallet lookup data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
