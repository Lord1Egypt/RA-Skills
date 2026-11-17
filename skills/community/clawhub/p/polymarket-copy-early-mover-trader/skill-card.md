## Description:

Identifies which whale wallet consistently enters markets first before others follow, then copies the lead indicator wallet's fresh positions before other traders push prices away.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-agent developers use this skill to scan Polymarket-related whale activity, identify confirmed early movers, and generate paper or explicitly live copy-trading actions through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real trades.

Mitigation: Keep the skill in paper mode unless automated trading is intentional, and require explicit review before using the --live flag.

Risk: The Simmer API key can authorize trading actions.

Mitigation: Use a minimally scoped SIMMER_API_KEY and rotate it if it is exposed.

Risk: Safety and dependency controls are under-scoped.

Mitigation: Pin and review the simmer-sdk dependency before enabling live mode.

Risk: Position sizing and portfolio limits affect financial exposure.

Mitigation: Set conservative values for max position, max open positions, spread, volume, and market-resolution tunables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-copy-early-mover-trader)
- [Publisher Profile](https://clawhub.ai/user/diagnostikon)
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard)
- [Polymarket Data API](https://data-api.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, API calls]

**Output Format:** [Console text with trading signal summaries and Simmer trade API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit --live flag and a SIMMER_API_KEY.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
