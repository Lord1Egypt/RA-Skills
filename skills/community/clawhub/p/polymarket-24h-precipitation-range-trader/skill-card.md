## Description: <br>
Trades mispricings in precipitation-range markets by reconstructing the implied probability distribution across bins for the same city and period, detecting sum violations and monotonicity breaks on cumulative precipitation markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to scan Polymarket precipitation markets, identify distribution-sum and monotonicity inconsistencies, and produce simulated or live trade actions through Simmer. It is intended for users who can manage trading credentials, tune risk limits, and review financial exposure before enabling live trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can cause real USDC losses when the --live flag is used. <br>
Mitigation: Test in paper mode first, set conservative trade limits, and use --live only when the operator accepts the financial risk. <br>
Risk: SIMMER_API_KEY is a sensitive trading credential. <br>
Mitigation: Protect and scope the key, avoid exposing it in logs or shared environments, and rotate it if disclosure is suspected. <br>
Risk: The skill depends on the third-party simmer-sdk package for market access and order execution. <br>
Mitigation: Review the installed simmer-sdk package and dependency source before running the skill with live trading enabled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diagnostikon/polymarket-24h-precipitation-range-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown instructions, Python code, environment configuration, and console status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to simulated trading and requires --live for real Polymarket orders.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
