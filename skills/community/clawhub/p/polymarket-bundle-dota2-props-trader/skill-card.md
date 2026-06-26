## Description: <br>
Trades bundle inconsistencies across correlated Dota 2 match props on Polymarket by detecting outlier prop prices against an action-score consensus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to monitor Dota 2 Polymarket prop bundles, identify cross-prop price inconsistencies, and generate simulated or live trade actions through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SIMMER_API_KEY is required and represents trading authority. <br>
Mitigation: Store the key only as a secret environment variable and review output before sharing it externally. <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Use the default paper trading mode for review and testing; enable live trading only with the explicit --live flag and conservative tunables for position size, spread, volume, and open-position limits. <br>
Risk: The correlation signal can be wrong when Dota 2 market conditions, team context, or liquidity diverge from the action-score model. <br>
Mitigation: Review proposed opportunities and keep minimum inconsistency, liquidity, spread, and position limits aligned with the user's risk tolerance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-bundle-dota2-props-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Plain text logs with Simmer market queries and trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require SIMMER_API_KEY and the --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
