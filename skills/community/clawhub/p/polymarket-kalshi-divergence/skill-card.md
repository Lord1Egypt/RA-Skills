## Description:

Cross-platform arbitrage between Kalshi and Polymarket that monitors Kalshi event series, compares prices to equivalent Polymarket markets, and generates BUY or SELL signals when configured divergence thresholds are exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mibayy](https://clawhub.ai/user/mibayy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading automation operators use this skill to monitor Kalshi and Polymarket price divergence, review generated signals, and optionally execute Polymarket trades through SimmerClient when live mode is explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real recurring trades using SIMMER_API_KEY.

Mitigation: Keep the skill in dry-run or paper-trading mode unless market matching has been audited and strict account and trade limits are configured.

Risk: Weak market matching and fail-open safety checks can produce incorrect trade decisions.

Mitigation: Review matched markets and context checks before enabling live execution, and pin dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mibayy/skills/polymarket-kalshi-divergence)
- [Publisher profile](https://clawhub.ai/user/mibayy)
- [Kalshi Trade API endpoint](https://api.elections.kalshi.com/trade-api/v2)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Trading signals]

**Output Format:** [Console logs and summaries with optional API trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs every five minutes as a managed automaton; dry-run is the default, and live trading requires an explicit --live flag.]

## Skill Version(s):

2.0.5 (source: release evidence, artifact metadata, and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
