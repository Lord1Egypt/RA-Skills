## Description:

Trades Polymarket "Elon Musk # tweets" markets using XTracker post count data, buying adjacent range buckets when their combined cost is below the configured threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure, dry-run, monitor, and optionally execute automated Polymarket tweet-count trading strategies based on XTracker pace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money trades and on-chain orders cannot be recalled.

Mitigation: Use dry-run mode first, confirm market scope and exit behavior, and enable --live only with conservative position limits.

Risk: The skill may require Simmer API credentials and, for external-wallet trading, a wallet private key.

Mitigation: Prefer managed-wallet mode when available, avoid high-value private keys in the general environment, and use a dedicated low-balance wallet for live trading.

Risk: The default strategy and parameters are not validated as profitable under current market conditions.

Mitigation: Run paper mode for an extended period and keep max position size, sizing percentage, and max trades per run conservative.

Risk: Automated exits may not protect positions in markets that move or resolve faster than the monitoring cycle.

Mitigation: Monitor live positions manually and treat position sizing as the primary risk control for fast-resolving markets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-elon-tweets)
- [Simmer API base](https://api.simmer.markets)
- [Simmer dashboard](https://simmer.markets/dashboard)
- [Simmer V2 migration guide](https://docs.simmer.markets/v2-migration)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run and status modes emit terminal summaries; live mode can submit orders when explicitly enabled.]

## Skill Version(s):

1.3.6 (source: server release metadata, skill frontmatter, and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
