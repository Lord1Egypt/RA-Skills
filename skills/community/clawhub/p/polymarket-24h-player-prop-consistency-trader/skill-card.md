## Description: <br>
Trades NBA player prop mispricings on Polymarket by detecting cross-stat consistency or divergence for the same player (Points, Rebounds, Assists O/U) and identifying outlier stats that disagree with the consensus direction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to analyze NBA player prop markets on Polymarket for cross-stat consistency or divergence and, when explicitly enabled, place Simmer-managed trades within configured risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can place real Polymarket orders and expose funds to loss. <br>
Mitigation: Use the default simulation mode first; enable live trading only deliberately and set max-position, max-open-position, spread, volume, and trade-size tunables to match loss limits. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Use a dedicated limited-scope API key where possible and keep funds limited before live use. <br>
Risk: Cross-stat market signals can be stale, incomplete, or wrong under changing game conditions. <br>
Mitigation: Review the generated reasoning and monitor thresholds, liquidity filters, and open positions before relying on live execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diagnostikon/polymarket-24h-player-prop-consistency-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration, API calls, Text logs] <br>
**Output Format:** [Plain text logs, Python command execution, environment configuration, and Simmer trading API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to simulation mode; live Polymarket trading requires an explicit live flag and a SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
