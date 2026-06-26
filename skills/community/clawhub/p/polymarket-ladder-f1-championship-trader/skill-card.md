## Description: <br>
Trades distribution-sum violations in F1 championship winner markets on Polymarket when driver winner probabilities collectively drift above or below approximately 100%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-bot operators use this skill to run a paper-by-default Polymarket strategy that scans F1 championship winner markets for distribution-sum mispricing and can place live trades only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SIMMER_API_KEY, a sensitive trading credential. <br>
Mitigation: Treat SIMMER_API_KEY as a high-value credential and install only if you intend to run a trading bot. <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Start in paper mode and use --live only with funds you are prepared to risk. <br>
Risk: Position sizing and open-position limits affect financial exposure. <br>
Mitigation: Review the max position and max open position tunables before enabling live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-ladder-f1-championship-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and requires --live for live Polymarket trades.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
