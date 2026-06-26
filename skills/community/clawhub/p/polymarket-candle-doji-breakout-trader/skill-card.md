## Description: <br>
Detects doji patterns in crypto 5-minute interval markets on Polymarket and trades the post-doji breakout in the direction of the pre-doji trend for BTC, ETH, SOL, and XRP Up or Down markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run or adapt a Polymarket crypto interval trading strategy that detects doji breakout setups, defaults to paper trading, and can place live trades only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and lose funds. <br>
Mitigation: Start in paper mode, enable live trading only deliberately, and confirm trade-size and position-limit tunables before use. <br>
Risk: The skill requires a sensitive SIMMER_API_KEY credential for trading authority. <br>
Mitigation: Keep the API key narrowly scoped where possible and protect it as a high-value credential. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review the simmer-sdk dependency before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-candle-doji-breakout-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trading guidance and executable agent behavior that requires SIMMER_API_KEY and defaults to paper trading unless live mode is explicitly requested.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
