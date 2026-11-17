## Description:

Scans the spot-vs-perpetual futures basis across Binance, Bybit, OKX, and Deribit using public REST market-data endpoints, then reports spot price, perpetual mark price, basis percentage, rough annualized basis, and 8-hour funding rate for requested symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent operators, and crypto researchers use this skill to compare spot-vs-perpetual basis, funding rates, and rough annualized spread estimates before independently evaluating cash-and-carry or funding-rate arbitrage opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried symbols and normal request metadata are sent to Binance, Bybit, OKX, and Deribit public APIs.

Mitigation: Use the skill only when that data sharing is acceptable for the user or organization.

Risk: Market-data output and rough annualized basis estimates can be incomplete, stale, rate-limited, or insufficient for trading decisions.

Mitigation: Independently verify exchange data, order-book depth, liquidity, fees, funding mechanics, and position risk before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/perp-basis-scanner)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Shell commands, Guidance]

**Output Format:** [Markdown prose with inline shell commands, plus table or JSON scanner output when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market-data scan; watch mode can repeat output on a configured interval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
