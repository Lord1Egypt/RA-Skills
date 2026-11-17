## Description:

Auto-trade BTC, ETH, SOL, XRP on Polymarket price prediction markets at 5-minute and 15-minute intervals using RSI, MACD, and EMA signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyy2099](https://clawhub.ai/user/hyy2099)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to run an agent-controlled Polymarket trading loop for BTC, ETH, SOL, and XRP markets, including dry-run checks before live orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place recurring real-money Polymarket orders using a raw wallet private key.

Mitigation: Start with DRY_RUN=true, use a dedicated wallet with limited funds and approvals, and only enable live orders after reviewing the trading path and position limits.

Risk: The security evidence reports that one trade path appears inconsistent with the documented strategy.

Mitigation: Review the bullish and bearish order logic before relying on automated trades, especially for SELL or NO-token behavior.

Risk: The skill charges the user through SkillPay before each trading cycle.

Mitigation: Confirm billing credentials, expected cycle frequency, and user consent before running it as a scheduler or persistent service.

Risk: The security guidance calls out dependency pinning and consent controls as unresolved concerns.

Mitigation: Pin and review dependencies and add explicit confirmation gates for live orders and billing before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyy2099/skills/polymarket-autotrader-hyy)
- [Publisher profile](https://clawhub.ai/user/hyy2099)
- [Polymarket](https://polymarket.com)
- [Polymarket CLOB](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run recurring trading cycles and can return order, dry-run, billing, market-discovery, and signal status output.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
