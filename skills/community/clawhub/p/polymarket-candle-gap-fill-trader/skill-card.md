## Description: <br>
Trades gap-fill reversions on Polymarket 5-minute crypto interval markets using conviction-based position sizing scaled by gap magnitude. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to evaluate and run a Polymarket strategy that looks for gap-fill reversions in BTC, ETH, SOL, and XRP 5-minute interval markets. It defaults to paper trading and requires explicit live mode before placing real Polymarket trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades. <br>
Mitigation: Keep the skill in paper mode first and use --live only with position limits the user is willing to risk. <br>
Risk: The skill requires SIMMER_API_KEY, a high-value trading credential. <br>
Mitigation: Protect and scope the credential, and review access before deploying the skill. <br>
Risk: Trading behavior depends on the simmer-sdk dependency and market data returned at runtime. <br>
Mitigation: Review simmer-sdk and monitor paper-mode results before enabling live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-candle-gap-fill-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with Python execution commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and uses tunable risk parameters for position size, spread, volume, thresholds, and maximum open positions.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
