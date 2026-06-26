## Description: <br>
Trades Polymarket weather temperature markets using NOAA and Open-Meteo forecasts as an information edge, buying YES on matching forecast bins and selling NO on bins the forecast disagrees with using micro-sized positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this agent skill to run a configurable Polymarket weather-market trading strategy in paper mode by default, with optional live execution when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live execution can place real USDC trades on Polymarket when --live is used. <br>
Mitigation: Keep the skill in paper mode unless live trading is intentional, protect SIMMER_API_KEY as a financial credential, and set conservative position limits before enabling live use. <br>
Risk: The security summary says live trades can be justified with misleading weather-source provenance. <br>
Mitigation: Review trade reasoning and provider tracking before relying on audit logs or running unattended live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-micro-weather-sniper-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text and trade requests with structured signal data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires the --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
