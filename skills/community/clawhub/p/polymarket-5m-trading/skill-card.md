## Description:

Find a high-volume BTC-related Polymarket priced between 40% and 60%, buy 1 USD of YES, hold for 5 minutes, sell, wait 5 minutes, and repeat until 10 completed buy cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skybinjf](https://clawhub.ai/user/skybinjf)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading automation operators use this skill to run or dry-run a fixed Polymarket BTC market trading cycle. It discovers an eligible market, prepares market-style YES orders, and controls buy, hold, sell, and pause loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket orders and lose money.

Mitigation: Keep the skill in dry-run unless intentionally passing --live, and use a dedicated low-balance wallet for live execution.

Risk: Wallet-derived trading credentials may be sent to an untrusted custom backend if AIONMARKET_BASE_URL is changed.

Mitigation: Do not set AIONMARKET_BASE_URL unless the endpoint is trusted and documented for the deployment.

Risk: Unpinned or unreviewed dependency versions can change behavior before live trading.

Mitigation: Pin and review dependency versions before using the skill with real funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skybinjf/skills/polymarket-5m-trading)
- [Publisher Profile](https://clawhub.ai/user/skybinjf)
- [Polymarket CLOB API Host](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with command-line options and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live execution requires --live and WALLET_PRIVATE_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
