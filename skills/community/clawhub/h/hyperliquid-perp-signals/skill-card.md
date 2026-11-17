## Description:

Perpetual futures signal scanner for Hyperliquid L1 DEX that tracks funding rates, open interest shifts, large position changes, liquidation cascades, funding-rate arbitrage setups, crowded trades, and squeeze setups across BTC, ETH, SOL, and altcoin perps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, crypto day traders, DeFi quants, and basis-trade funds use this skill to run CLI checks for Hyperliquid perpetual futures signals, funding basis, liquidation pressure, open-interest divergence, and squeeze setups. Review outputs carefully because the bundled implementation may produce simulated market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present simulated crypto trading data as current market signals, which could mislead users making financial decisions.

Mitigation: Do not rely on outputs for trading unless the skill clearly labels simulation mode or is changed to fetch and verify live exchange data.

## Reference(s):

- [Hyperliquid info endpoint](https://api.hyperliquid.xyz/info)
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/hyperliquid-perp-signals)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON from CLI commands with brief Markdown guidance when used through an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes coin, prices, funding rates, open interest, liquidation summaries, basis calculations, signals, and confidence-style scores where supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
