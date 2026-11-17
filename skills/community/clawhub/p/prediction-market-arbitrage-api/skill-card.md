## Description:

Find arbitrage opportunities across Polymarket and Kalshi prediction markets via AIsa API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to scan sports prediction markets for cross-platform price discrepancies, compare odds, and check orderbook liquidity before deciding whether an apparent arbitrage is actionable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet, activity, positions, and P&L commands can send wallet identifiers and related analysis requests to AIsa.

Mitigation: Use those commands only when the user intends to disclose the wallet identifier to AIsa; the core arbitrage scanner can be used without wallet identifiers.

Risk: Apparent arbitrage spreads may be misleading or non-executable when orderbook liquidity is insufficient.

Mitigation: Verify orderbook depth before acting and treat computed spreads as analysis, not trading instructions.

Risk: Using the skill requires sharing an AISA_API_KEY with the local scripts and sending market queries to api.aisa.one.

Mitigation: Install and run the skill only when use of the AIsa API is acceptable, and manage the API key as a secret.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/prediction-market-arbitrage-api)
- [AIsa API Reference](https://docs.aisa.one/reference/)
- [AIsa](https://aisa.one)
- [Polymarket](https://polymarket.com)
- [Kalshi](https://kalshi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; commands query api.aisa.one over HTTPS GET and do not execute trades.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
