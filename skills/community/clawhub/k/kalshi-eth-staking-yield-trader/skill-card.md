## Description: <br>
Trades ETH price markets on Kalshi using the 4% staking yield as a fundamental price floor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to analyze ETH Kalshi markets, review staking-yield floor signals, and optionally automate position entries or exits through Simmer with configured risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can use real trading credentials and place financial trades. <br>
Mitigation: Test dry-run mode first, use a dedicated low-balance Solana wallet and limited Simmer credentials, and only pass --live after reviewing the configured limits. <br>
Risk: Trade sizing, slippage, and frequency settings can materially change financial exposure. <br>
Mitigation: Double-check max position, max trades per run, slippage, and related tunables before enabling live trading. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review simmer-sdk before trusting it with live credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-eth-staking-yield-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with optional JSON automaton summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode is the default; live trading requires an explicit --live flag and configured credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
