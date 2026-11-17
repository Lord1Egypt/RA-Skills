## Description:

Scans Polymarket markets for AMM/CLOB price divergence and can buy the underpriced side, then exit via take-profit or time-stop rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prysm96](https://clawhub.ai/user/prysm96)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and automation operators use this skill to scan Polymarket markets for price-dislocation signals, execute simulated or live trades, monitor open positions, and summarize P&L.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged trading settings can allow spending far above the documented limits.

Mitigation: Review and lower max_position_usd, max_trades_per_run, and daily_max_spend before installing or running live mode.

Risk: Helper scripts read a shared .env file, which may expose unrelated secrets to the runtime.

Mitigation: Use an isolated runtime environment, avoid shared .env files, and provide only a narrowly scoped SIMMER_API_KEY.

Risk: Live mode can place trades or redeem positions using the configured Simmer account.

Mitigation: Run in dry-run mode first and pin/review simmer-sdk before granting live trading authority.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/prysm96/skills/polymarket-spread-sniper)
- [Simmer API](https://api.simmer.markets)
- [Simmer Positions API](https://api.simmer.markets/api/sdk/positions)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code, Files]

**Output Format:** [Console text, JSON status reports, and local JSON/log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; dry run is the default unless live execution is requested.]

## Skill Version(s):

1.3.2 (source: server release evidence; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
