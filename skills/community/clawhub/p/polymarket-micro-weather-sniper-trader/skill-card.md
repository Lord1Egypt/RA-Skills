## Description:

Trades Polymarket weather temperature markets using NOAA and Open-Meteo forecasts as an information edge, using micro-sized positions and paper trading by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run an agent-managed Polymarket weather-market trading strategy that compares forecast temperatures with market bins and proposes or places micro-sized trades. It defaults to paper trading and requires explicit live mode for real USDC execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real USDC trades on Polymarket when enabled.

Mitigation: Use paper mode first, require explicit approval before passing --live, and use a least-privilege SIMMER_API_KEY with server-side trade and balance limits.

Risk: Forecast-source disclosure and live-trading safeguards need review before deployment.

Mitigation: Do not enable live mode until the documented risk controls and the wttr.in fallback behavior are fixed or explicitly accepted.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Pin or vet simmer-sdk before deployment and review dependency updates before using live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-micro-weather-sniper-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure paper or live trading mode, environment variables, tunable risk limits, and Simmer SDK execution.]

## Skill Version(s):

0.0.2 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
