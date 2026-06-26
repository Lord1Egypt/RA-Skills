## Description: <br>
Trades altcoin (ETH/SOL/XRP) Up/Down markets based on BTC weekend price threshold momentum drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run or adapt a Polymarket trading agent that compares BTC weekend threshold-market drift against ETH, SOL, and XRP Up/Down markets. It defaults to paper trading and requires an explicit live mode for real trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SIMMER_API_KEY is a sensitive trading credential. <br>
Mitigation: Store it only in the runtime secret manager or environment and rotate it if exposed. <br>
Risk: Running with --live can place real Polymarket trades and put USDC at risk. <br>
Mitigation: Run in the default paper mode first, set account and position limits, and use live mode only with funds the operator is willing to risk. <br>
Risk: The strategy depends on third-party market data and the simmer-sdk dependency. <br>
Mitigation: Review the dependency and current market behavior before deployment, especially after SDK or venue changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-macro-weekend-momentum-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and trade execution requests through simmer-sdk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
