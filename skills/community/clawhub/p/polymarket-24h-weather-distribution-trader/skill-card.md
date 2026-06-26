## Description: <br>
Trades mispricings in weather temperature-bin markets by reconstructing the implied probability distribution across bins for the same city and date, detecting sum violations and monotonicity breaks on cumulative markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to identify distribution-sum and cumulative-monotonicity inconsistencies across Polymarket weather temperature-bin markets, then paper trade by default or place live trades only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated prediction-market trading can create real financial loss when live mode is enabled. <br>
Mitigation: Start in dry-run mode, keep small trade limits until tested, and enable live trading only after reviewing local configuration and logs. <br>
Risk: The skill requires a sensitive SIMMER_API_KEY with trading authority. <br>
Mitigation: Use a restricted API key if supported and store it as a secret rather than in source files. <br>


## Reference(s): <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-24h-weather-distribution-trader) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, shell commands, configuration, API calls] <br>
**Output Format:** [Text logs, configuration values, and trading API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to simulated trading; live trading requires an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
