## Description: <br>
Automates analysis of Polymarket crypto Up or Down markets to detect 5-minute versus hourly candle consensus mismatches and place convergence trades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to run a configurable paper or live Polymarket crypto trading workflow that compares 5-minute interval consensus with hourly market pricing before placing convergence trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades and requires SIMMER_API_KEY, which should be treated like financial account access. <br>
Mitigation: Start in paper mode, use --live only intentionally, keep position and spread limits conservative, and protect the API key. <br>
Risk: The strategy documentation makes strong convergence and certainty claims that may overstate trading reliability. <br>
Mitigation: Treat signals as hypotheses, paper trade or backtest before live use, and do not rely on strategy language as a guarantee of returns or loss avoidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-candle-timeframe-mismatch-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands] <br>
**Output Format:** [Console logs and trading API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
