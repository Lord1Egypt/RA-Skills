## Description: <br>
Trades marubozu continuation signals on Polymarket 5-minute crypto interval markets, targeting BTC, ETH, SOL, and XRP Up or Down bundles with conviction-based position sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to detect marubozu-style continuation signals in Polymarket five-minute crypto interval markets and submit simulated or explicitly live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Simmer trading API key. <br>
Mitigation: Treat the key as a high-value credential and install the skill only if you are comfortable granting that access. <br>
Risk: Using the --live flag can place real Polymarket trades with financial exposure. <br>
Mitigation: Start in paper mode, review the configured position limits, and use --live only when live trading is intentional. <br>


## Reference(s): <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-candle-marubozu-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text with Simmer trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require an explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
