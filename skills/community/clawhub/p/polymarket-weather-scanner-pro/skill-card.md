## Description:

Exploit NOAA/Open-Meteo forecast vs Polymarket temperature market mispricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themsquared](https://clawhub.ai/user/themsquared)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Polymarket temperature markets for forecast-versus-price discrepancies and identify candidate trades. The skill can also produce dry-run or live-buy commands for the highest-ranked opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money Polymarket trades when run with live-buy options.

Mitigation: Use dry-run or scan-only mode unless intentional trading is required, and set external account or wallet limits before enabling live trades.

Risk: The trading path depends on local wallet secrets and a trusted trader.py implementation.

Mitigation: Keep unrelated secrets out of the skill .env file, audit any trader.py before use, and treat wallet or private-key configuration as real financial authority.

Risk: The security verdict is suspicious because the live trading path is under-scoped and handles local secrets broadly.

Mitigation: Review the skill carefully before installation and restrict execution to the minimum permissions needed for scanning or trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/themsquared/skills/polymarket-weather-scanner-pro)
- [Publisher profile](https://clawhub.ai/user/themsquared)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Visual Crossing Timeline API](https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline)
- [Aviation Weather METAR API](https://aviationweather.gov/api/data/metar)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked market candidates, forecast sources, probability estimates, edge estimates, dry-run trade sizing, or live trade execution status.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
