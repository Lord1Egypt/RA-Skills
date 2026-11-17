## Description:

Trade Kalshi weather markets using NOAA forecasts via the Simmer SDK and DFlow on Solana.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to configure, dry-run, and optionally execute automated Kalshi temperature-market trades driven by NOAA forecast signals. It also helps inspect account balances, open weather positions, and trading thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says live-trading safeguards can fail open.

Mitigation: Keep dry-run mode enabled until behavior is verified, and do not rely on advertised safeguards unless the fail-open behavior is fixed or acceptable for the user's risk tolerance.

Risk: The skill handles wallet-signing credentials and can place real on-chain orders.

Mitigation: Use a dedicated low-balance wallet, keep the Solana private key only in secured environment storage, and avoid connecting funds beyond the amount intended for this strategy.

Risk: The security guidance notes an unpinned Simmer SDK dependency.

Mitigation: Pin or review the simmer-sdk version before live use, especially before installing updates or enabling scheduled runs.

Risk: Automated weather-market trades can lose value quickly near resolution and may not be recoverable.

Mitigation: Use conservative position sizing, start with paper or simulated runs, and review market resolution timing before enabling live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/kalshi-weather-trader)
- [Simmer API](https://api.simmer.markets)
- [Simmer dashboard](https://simmer.markets/dashboard)
- [NOAA Weather API](https://api.weather.gov)
- [DFlow Proof KYC](https://dflow.net/proof)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live trading requires explicit --live execution and configured credentials.]

## Skill Version(s):

1.0.12 (source: server evidence, frontmatter, changelog released 2026-09-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
