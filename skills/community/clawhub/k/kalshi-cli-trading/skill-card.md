## Description:

Trade prediction markets on Kalshi with kalshi-cli for market discovery, order placement, portfolio management, streaming prices, and ASCII candlestick charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lacymorrow](https://clawhub.ai/user/lacymorrow)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate kalshi-cli for Kalshi market research, order workflows, portfolio review, streaming data, and bot-oriented JSON command flows while keeping live trading behind explicit confirmation.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill installs and relies on an unpinned third-party trading CLI that handles credentials and can place or cancel real-money orders.

Mitigation: Review the exact kalshi-cli version and source before installing, prefer a pinned verified release, and use demo mode before production trading.

Risk: Non-interactive order flows and the --yes flag can bypass command confirmations for live orders.

Mitigation: Keep production trading behind explicit human approval and avoid --yes for live orders unless the full bot workflow has been reviewed.

Risk: Kalshi API credentials are required for authenticated trading and account operations.

Mitigation: Use narrowly scoped credentials that can be revoked quickly, and avoid hardcoding private keys in scripts or configuration.

## Reference(s):

- [kalshi-cli](https://github.com/6missedcalls/kalshi-cli)
- [OpenClaw Kalshi Trading Skill Repository](https://github.com/lacymorrow/openclaw-kalshi-trading-skill)
- [Kalshi API Docs](https://docs.kalshi.com/welcome)
- [Kalshi Fee Schedule](https://kalshi.com/fee-schedule)
- [Kalshi Liquidity Incentive Program](https://help.kalshi.com/incentive-programs/liquidity-incentive-program)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code, JSON]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include demo or production Kalshi CLI commands; live trading should require explicit human confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
