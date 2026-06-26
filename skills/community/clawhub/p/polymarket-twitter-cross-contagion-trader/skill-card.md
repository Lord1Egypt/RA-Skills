## Description: <br>
Trades post-count bin markets by detecting cross-person contagion where one public figure posting heavily causes correlated figures to increase their rate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced trading agents use this skill to evaluate and optionally trade Polymarket post-count bin markets through Simmer based on cross-person posting correlation signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated trading can place real Polymarket orders when live mode is explicitly enabled with live-capable credentials. <br>
Mitigation: Test in paper mode first, keep cron and autostart disabled unless automation is intended, and provide live-capable credentials only after reviewing the skill and simmer-sdk. <br>
Risk: The SIMMER_API_KEY grants trading authority and is required by the skill. <br>
Mitigation: Keep the key private, scope it to the intended environment, and avoid storing live-capable credentials where unattended automation can invoke --live. <br>
Risk: The advertised minimum-volume filter is not enforced by the included code. <br>
Mitigation: Do not rely on SIMMER_MIN_VOLUME for liquidity protection until the implementation enforces it; review candidate markets before live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-twitter-cross-contagion-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [Console text and Simmer trade API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading unless run with --live; requires SIMMER_API_KEY and simmer-sdk.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
