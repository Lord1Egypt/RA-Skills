## Description: <br>
Trades mispricings in precipitation-range markets by reconstructing implied probability distributions across bins for the same city and period, then detecting sum violations and monotonicity breaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and trading operators use this skill to scan Polymarket precipitation-range markets, identify probability-distribution inconsistencies, and place paper or explicitly enabled live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades. <br>
Mitigation: Keep the skill in paper mode first and use --live only after setting position and order limits you are comfortable risking. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Protect SIMMER_API_KEY like a financial credential and restrict it to the intended runtime environment. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review the simmer-sdk dependency before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-48h-precipitation-range-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console logs, Simmer trade requests, and environment-based configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
