## Description:

Trades Polymarket prediction markets on weather extremes, climate milestones, natural disasters, and agricultural outcomes using meteorological data signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover climate and weather prediction markets, size candidate positions, and run paper or explicit live trades through Simmer and Polymarket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real trades using SIMMER_API_KEY.

Mitigation: Use paper mode first, avoid unattended live runs, and provide only least-privilege or low-funded live trading credentials.

Risk: Risk-control behavior is not fully reliable because documentation, manifest defaults, and enforcement are inconsistent or incomplete.

Mitigation: Reconcile the documented and configured limits, then fix and review liquidity and portfolio checks before relying on live execution.

## Reference(s):

- [NOAA Climate Data Online](https://www.ncdc.noaa.gov/cdo-web/)
- [Open-Meteo API](https://open-meteo.com/)
- [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
- [ForecastEx](https://forecastex.com/)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console logs, environment configuration, and trade API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading unless live mode is explicitly requested.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
