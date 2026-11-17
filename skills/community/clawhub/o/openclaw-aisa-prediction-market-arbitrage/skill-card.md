## Description:

Find and analyze arbitrage opportunities across prediction markets like Polymarket and Kalshi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, developers, and market analysts use this skill to match prediction markets across Polymarket and Kalshi, compare prices, calculate spreads, and check orderbook depth before evaluating a possible arbitrage trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market IDs, search parameters, and optional wallet addresses are sent to AIsa under the user's API key.

Mitigation: Use the skill only for market or wallet data you intend to share with AIsa, and avoid optional wallet, positions, and P&L lookups unless that disclosure is acceptable.

Risk: Arbitrage results may be stale or non-actionable if prices move, fees apply, or orderbook depth is insufficient.

Mitigation: Check current prices and orderbook liquidity immediately before acting, and account for fees and slippage outside the skill output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-prediction-market-arbitrage)
- [OpenClaw](https://openclaw.ai)
- [AIsa](https://aisa.one)
- [AIsa API Reference](https://docs.aisa.one/reference/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python examples, plus optional JSON from bundled CLI scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends prediction-market query parameters to the AIsa API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
