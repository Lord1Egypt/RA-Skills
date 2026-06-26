## Description: <br>
Detects harami candlestick patterns on Polymarket crypto 5-minute interval markets and can place conviction-sized BTC, ETH, SOL, and XRP Up or Down trades through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to run a Simmer-managed Polymarket strategy that detects harami reversal patterns in crypto interval markets. It defaults to paper trading and only places real USDC trades when explicitly run in live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when live mode is explicitly enabled. <br>
Mitigation: Test in paper mode first and use --live only when the operator accepts the configured USDC limits and financial risk. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Keep SIMMER_API_KEY protected and provide it only through the runtime environment or approved secret storage. <br>
Risk: Trading behavior depends on the external simmer-sdk dependency and live market data. <br>
Mitigation: Review the simmer-sdk dependency and the configured tunables before deployment. <br>


## Reference(s): <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Console text from a Python trading script plus Simmer trade API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; live trading requires the explicit --live flag and uses configured USDC risk limits.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
