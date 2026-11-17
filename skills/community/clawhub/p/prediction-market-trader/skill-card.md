## Description:

Prediction Market Trader is a Kalshi trading toolkit for API authentication, market scanning, Sofascore de-vigging, true probability calculation, Kelly sizing, and order execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merjua14](https://clawhub.ai/user/merjua14)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prediction market analysts use this skill to evaluate Kalshi markets, compare prices with de-vigged external odds, size candidate trades, and prepare or execute orders with explicit safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support live financial actions on Kalshi, including placing or canceling orders.

Mitigation: Use read-only or test credentials where possible and require explicit human confirmation, dry-run defaults, order-size limits, and exposure checks before any live order action.

Risk: Private Kalshi credentials or RSA keys could be exposed if pasted into shell history or shared agent context.

Mitigation: Use a secrets manager or protected key file, avoid pasting private keys into shell history, and rotate credentials after testing or accidental exposure.

Risk: Fragile market-participant matching can produce incorrect trades or misleading edge calculations.

Mitigation: Require reliable participant matching by stable identifiers or full names, deduplicate equivalent positions, and manually review matched markets before execution.

Risk: Fast-moving odds and stale market data can make calculated edges obsolete before execution.

Mitigation: Re-check source odds, Kalshi price, fees, and liquidity immediately before trading, and avoid execution when the edge has closed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/merjua14/skills/prediction-market-trader)
- [Market Categories](artifact/references/market-categories.md)
- [Risk Rules](artifact/references/risk-rules.md)
- [Lessons Learned](artifact/references/lessons-learned.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and JavaScript examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests, market-edge calculations, position sizing guidance, and trade/order recommendations that require review before live execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
