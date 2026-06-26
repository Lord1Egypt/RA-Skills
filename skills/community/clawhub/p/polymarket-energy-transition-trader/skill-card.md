## Description: <br>
Trades Polymarket prediction markets on EV adoption milestones, solar/wind capacity, nuclear energy restarts, oil price thresholds, and energy policy events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to discover energy-transition Polymarket markets, compute conviction-based trade signals, and run those signals in paper mode or explicit live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades through the Simmer SDK when SIMMER_API_KEY is provided and --live is used. <br>
Mitigation: Run paper mode first, review generated behavior, and enable live mode only after accepting the financial risk. <br>
Risk: Some documented risk controls are looser or missing in runnable artifacts. <br>
Mitigation: Set and review actual tunables for minimum days, thresholds, position limits, spread limits, and market volume filtering before live use. <br>
Risk: SIMMER_API_KEY is a sensitive credential with trading authority. <br>
Mitigation: Store the key securely, limit access to trusted runtime environments, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-energy-transition-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Console text, Python execution, environment-variable configuration, and Simmer SDK trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
