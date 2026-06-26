## Description: <br>
Trades Polymarket prediction markets on space launches, SpaceX milestones, satellite deployments, Mars missions, and commercial spaceflight outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as an automated prediction-market trading helper for space and launch-related Polymarket markets. It discovers relevant markets, sizes paper or live trades from configurable risk parameters, and defaults to paper trading until live mode is explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades using USDC. <br>
Mitigation: Keep the skill in paper mode first, review the strategy and position limits, and provide a live-capable SIMMER_API_KEY only when prepared to risk real USDC. <br>
Risk: The skill requires a sensitive SIMMER_API_KEY credential. <br>
Mitigation: Keep the credential private and avoid placing a live-capable key in environments where automated code could call live mode unexpectedly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diagnostikon/polymarket-space-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [Console status text and configured trading actions through the Simmer SDK] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; paper trading is the default, and live Polymarket trading requires an explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
