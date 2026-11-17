## Description:

Verify any Hyperliquid wallet's track record from the public ledger before copying it. Win rate, expectancy, profit factor, drawdown, equity curve, positions and anomaly flags for $0.05 per address via x402, no API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pulsenetwork](https://clawhub.ai/user/pulsenetwork)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill to inspect a Hyperliquid wallet's public trading record before considering it for further review. It summarizes performance, drawdown, current positions, and activity flags without identifying the wallet owner or recommending that users copy trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each lookup costs $0.05 and discloses the queried wallet address to the provider; the remote service behavior was not independently verified.

Mitigation: State the price and address disclosure, obtain approval before the first paid lookup, and use a dedicated low-balance payment wallet.

Risk: Limited fill coverage, stale activity, and anomaly flags can be mistaken for a complete record or a verdict about a trader.

Mitigation: Lead with coverage and last-fill age, treat anomaly flags as prompts to inspect, and present historical performance as neither a forecast nor advice to copy.

## Reference(s):

- [CryptoPulse Trader Record API](https://cryptopulse.theaslangroupllc.com/api/trader-record)
- [ClawHub Skill Release](https://clawhub.ai/pulsenetwork/skills/hyperliquid-trader-record)
- [Publisher Profile](https://clawhub.ai/user/pulsenetwork)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured trading statistics with concise natural-language interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-wallet record; fill statistics cover up to the venue's 2,000 most recent fills, with coverage and equity-window details included.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
