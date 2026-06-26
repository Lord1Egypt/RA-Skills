## Description: <br>
Trades crypto "Up or Down" 5-minute Polymarket interval markets by detecting Three White Soldiers and Three Black Crows continuation patterns, defaulting to paper trading unless live mode is explicitly enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run or adapt a Simmer/Polymarket trading workflow for short-interval crypto prediction markets. It is intended for users who understand automated trading, credential handling, and the risk of real financial loss when live mode is enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and create financial loss. <br>
Mitigation: Start in paper mode and use --live only after accepting the financial risk and checking configured trade limits. <br>
Risk: SIMMER_API_KEY is a high-value trading credential. <br>
Mitigation: Store the credential securely, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: The workflow depends on the third-party simmer-sdk package. <br>
Mitigation: Verify the simmer-sdk package source before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-candle-three-soldiers-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text with configurable environment variables and Simmer trade API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
