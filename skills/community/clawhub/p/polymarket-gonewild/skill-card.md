## Description:

Query Polymarket prediction markets - check odds, trending markets, search events, track prices and momentum. Includes watchlist alerts, resolution calendar, momentum scanner, and paper trading (simulated, no real money).

This skill is ready for commercial/non-commercial use.

## Publisher:

[shrimpdaddie](https://clawhub.ai/user/shrimpdaddie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect public Polymarket prediction-market data, monitor market movement, configure local watchlist alerts, and track simulated paper-trading positions without real-money trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes unauthenticated public API requests to Polymarket and may be unsuitable where prediction-market access is restricted by policy or jurisdiction.

Mitigation: Review organizational and regional requirements before use, and install only where public Polymarket market-data access is permitted.

Risk: Watchlist alerts and simulated portfolio data are stored locally in ~/.polymarket.

Mitigation: Treat local watchlist and portfolio files as user data, and remove or protect them according to the user's workstation data-handling practices.

Risk: Suggested cron entries can run periodic market checks after installation.

Mitigation: Add scheduled jobs only when the user wants ongoing checks, and review the exact cron commands before enabling them.

Risk: Prediction-market information and paper-trading output could be mistaken for real trading or financial advice.

Mitigation: Keep user-facing guidance clear that the artifact does not handle wallets, API keys, credentials, real-money trades, or financial transactions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shrimpdaddie/skills/polymarket-gonewild)
- [Polymarket](https://polymarket.com)
- [Polymarket Documentation](https://docs.polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON files under ~/.polymarket for watchlists and simulated paper-trading portfolios.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
