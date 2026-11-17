## Description:

Trades Polymarket weather markets using NOAA and Open-Meteo forecasts through the Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect, configure, paper-trade, or explicitly live-trade weather prediction markets based on forecast data and market prices. It also supports position checks and replay/backtest workflows for validating the trading path before adding capital.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money trades when live mode is enabled, and automated trading can produce irreversible losses.

Mitigation: Start in dry-run or TRADING_VENUE=sim, keep tight platform and per-trade caps, and use --live only after accepting the trading risk.

Risk: Some safeguards can be bypassed or fail open when context data is unavailable or when --no-safeguards is used.

Mitigation: Keep safeguards enabled, review preflight/status output before live use, and avoid --no-safeguards unless the operator has independently verified the market context.

Risk: Weather bucket markets can resolve by gapping directly to near zero, so stop-loss monitoring may not cap downside.

Mitigation: Size positions assuming the full position can be lost, keep max position and max buys per market conservative, and rely on position sizing rather than stop-losses alone.

Risk: External-wallet self-custody mode may require WALLET_PRIVATE_KEY, which increases credential exposure if handled casually.

Mitigation: Avoid providing WALLET_PRIVATE_KEY unless external-wallet live trading is required, prefer paper or managed-wallet flows first, and keep credentials scoped to the runtime environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-weather-trader)
- [Simmer wallet setup](https://docs.simmer.markets/wallets)
- [Simmer V2 migration](https://docs.simmer.markets/v2-migration)
- [Open-Meteo Previous Runs API](https://previous-runs-api.open-meteo.com/v1/forecast)
- [NOAA Weather API](https://api.weather.gov)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python entrypoints, JSON configuration, and console summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place simulated or live trading orders only when invoked with the required runtime configuration and explicit live mode.]

## Skill Version(s):

1.23.22 (source: server evidence, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
