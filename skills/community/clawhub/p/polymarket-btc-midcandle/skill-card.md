## Description:

Runs a configurable Polymarket BTC 15-minute mid-candle trading bot that can paper trade or place live trades based on Binance momentum signals and Simmer/Polymarket market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and agent operators use this skill to configure and run a BTC Up/Down market strategy in paper mode or live mode on Polymarket through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run unattended live trades with real funds.

Mitigation: Run paper mode first, use a dedicated low-limit trading key or account, keep conservative position sizing, and avoid cron scheduling until the strategy is understood.

Risk: The skill relies on high-trust credentials and the simmer-sdk dependency.

Mitigation: Pin and review the simmer-sdk dependency, restrict credential permissions where possible, and rotate credentials if they may have been exposed.

Risk: Startup may fail because max_consecutive_losses is referenced but is not defined in the configuration schema.

Mitigation: Fix or add the missing configuration key and validate startup in paper mode before any live deployment.

Risk: A Discord webhook can send trading notifications to a configured external endpoint.

Mitigation: Configure only a trusted HTTPS webhook destination and treat the webhook URL as a secret.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djdyll/skills/polymarket-btc-midcandle)
- [ClawHub publisher profile](https://clawhub.ai/user/djdyll)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Command-line text logs, JSON automaton status, and trading API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and a configured Polymarket agent ID; paper mode is the default and live execution requires --live.]

## Skill Version(s):

1.1.1 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
