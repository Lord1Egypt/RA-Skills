## Description: <br>
Trades Polymarket prediction markets by chaining commodity pressure through inflation and rate expectations to identify equity-market divergences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trading agents and operators use this skill to monitor macro-linked Polymarket markets, size positions, and run paper or explicitly enabled live trades under configured risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real USDC trades on Polymarket. <br>
Mitigation: Use paper mode first and pass --live only after reviewing market selection, thresholds, and position limits. <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Keep the credential private and provide it only in trusted runtime environments. <br>
Risk: The skill depends on simmer-sdk for market access and execution. <br>
Mitigation: Review the dependency before providing live credentials when dependency-level assurance is required. <br>
Risk: Aggressive tunables can increase trading exposure. <br>
Mitigation: Set conservative max position, max open positions, spread, liquidity, and threshold values before running live. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-macro-inflation-chain-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance and command-line trading logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
