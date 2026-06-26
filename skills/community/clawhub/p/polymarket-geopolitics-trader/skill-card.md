## Description: <br>
Trades Polymarket prediction markets on geopolitical events, including wars, ceasefires, sanctions, diplomatic breakthroughs, and regime changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and advanced trading operators use this skill to discover geopolitical Polymarket markets, score threshold-based YES or NO opportunities, and place paper or explicitly enabled live trades with configurable risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags less clear and less conservative live-trading safeguards than the documentation suggests. <br>
Mitigation: Review the code and manifest defaults before installation, run in paper mode first, and enable live trading only after confirming position, spread, and market-selection settings. <br>
Risk: The skill requires a sensitive trading credential. <br>
Mitigation: Use only a scoped or revocable SIMMER_API_KEY, monitor its activity, and rotate or revoke it if behavior is unexpected. <br>
Risk: Live Polymarket execution can create real financial exposure. <br>
Mitigation: Set strict maximum position, open-position, spread, and trade-size limits before any live run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-geopolitics-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text and trading API actions driven by Python execution and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; default execution is paper trading unless the live flag is explicitly provided.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
