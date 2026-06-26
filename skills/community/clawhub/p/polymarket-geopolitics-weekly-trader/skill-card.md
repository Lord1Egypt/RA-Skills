## Description: <br>
Trades weekly cyclical patterns in geopolitical prediction markets by combining day-of-week timing with conviction-based sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to find geopolitical Polymarket markets, apply weekly timing and conviction sizing, and submit paper trades by default or live trades when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Simmer trading API key to place real-money Polymarket trades when live mode is explicitly enabled. <br>
Mitigation: Start in the default paper mode, keep position and trade limits conservative, and use --live only when real-money trading is intended. <br>
Risk: Prediction-market signals may be wrong or stale, which can create financial loss in live trading. <br>
Mitigation: Review strategy assumptions and outputs before live use, monitor positions, and enforce configured limits such as max position size, max spread, minimum volume, and max open positions. <br>
Risk: SIMMER_API_KEY is a sensitive credential with trading authority. <br>
Mitigation: Store the key securely, avoid exposing it in logs or prompts, and limit its permissions where the trading provider supports scoped access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-geopolitics-weekly-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Plain text status logs from a Python trader script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
