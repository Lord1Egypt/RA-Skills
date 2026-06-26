## Description: <br>
Trades session-transition mean-reversion in 5-minute crypto "Up or Down" markets on Polymarket, fading directional bursts that occur during US, Asia, and Europe session opens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and advanced trading users use this skill to discover short-duration crypto Up or Down markets on Polymarket, identify session-transition burst patterns, and generate paper-first or explicitly live trade execution decisions with configurable position limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades with USDC when run with the explicit live flag. <br>
Mitigation: Use paper mode first, review thresholds and position limits, and run --live only when prepared for real trade execution and possible financial loss. <br>
Risk: The skill requires SIMMER_API_KEY, which grants trading access through Simmer and its SDK. <br>
Mitigation: Use a restricted or low-balance key where possible, store it securely, and avoid exposing it in logs, prompts, or shared configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-micro-session-edge-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text with configurable Python execution and Simmer trading API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket execution requires SIMMER_API_KEY and an explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
