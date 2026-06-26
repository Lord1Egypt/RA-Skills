## Description: <br>
Detects engulfing reversal patterns in crypto 5-minute interval markets on Polymarket and targets BTC, ETH, SOL, and XRP Up or Down bundles with conviction-based position sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to run a configurable Polymarket trading strategy that detects engulfing reversal patterns in crypto 5-minute interval markets. It defaults to paper trading and can place live Polymarket trades only when explicitly run with the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated live trading can create real USDC exposure on Polymarket. <br>
Mitigation: Start in paper mode, use the live flag only intentionally, keep position limits small, and actively monitor trading behavior. <br>
Risk: The skill requires SIMMER_API_KEY, which grants trading authority. <br>
Mitigation: Protect the key as a high-value credential and scope or rotate it where the provider supports that. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review the dependency before deployment and keep it pinned or monitored according to the deployment environment's dependency policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-candle-engulfing-reversal-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance, Python execution, and console logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires an explicit live flag and a SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
