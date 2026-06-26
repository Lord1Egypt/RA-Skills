## Description: <br>
Trades Polymarket prediction markets on weather extremes, climate milestones, natural disasters, and agricultural outcomes. Use when you want to capture alpha on temperature records, hurricane seasons, flood events, and CO2 threshold markets using meteorological data signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to discover climate and weather prediction markets, size positions from seasonal signals, and submit paper or explicitly enabled live trades through Simmer. It is intended for Polymarket market analysis and execution workflows that require configurable position, spread, volume, and open-position limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says this is a trading skill whose artifacts under-disclose real-money automated trading risk. <br>
Mitigation: Review carefully before installing, begin with paper trading credentials, and confirm whether live order placement can occur before providing any live-capable key. <br>
Risk: The skill requires a trading credential and can place live Polymarket orders when live execution is explicitly enabled. <br>
Mitigation: Use least-privilege API keys, keep SIMMER_API_KEY private, set conservative order limits, and verify stop controls and managed-execution disablement before live use. <br>
Risk: Climate and weather market signals may be incomplete, stale, or misaligned with market resolution rules. <br>
Mitigation: Validate the data source, market terms, spread limits, and resolution timing before accepting proposed trades. <br>


## Reference(s): <br>
- [Polymarket Climate Trader on ClawHub](https://clawhub.ai/diagnostikon/polymarket-climate-trader) <br>
- [NOAA Climate Data Online](https://www.ncdc.noaa.gov/cdo-web/) <br>
- [Open-Meteo API](https://open-meteo.com/) <br>
- [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/) <br>
- [ForecastEx](https://forecastex.com/) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, API calls] <br>
**Output Format:** [Markdown guidance with Python code and configuration-driven trading actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; OPENMETEO_API_KEY is optional. Defaults to paper trading unless live execution is explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
