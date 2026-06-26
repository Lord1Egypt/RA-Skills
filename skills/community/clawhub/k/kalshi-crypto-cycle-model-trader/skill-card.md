## Description: <br>
Trades Bitcoin year-end price markets on Kalshi using the 4-year halving cycle pattern to compute fair price probabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to analyze Kalshi Bitcoin year-end price markets, identify model-versus-market pricing gaps, and optionally execute constrained live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money trades and requires wallet credentials. <br>
Mitigation: Keep the skill in dry-run until reviewed, pass --live only intentionally, and use a dedicated low-balance wallet or API setup for live trading. <br>
Risk: The skill depends on a third-party SDK and high-value credentials. <br>
Mitigation: Review simmer-sdk before providing SOLANA_PRIVATE_KEY or SIMMER_API_KEY, and avoid exposing a primary wallet private key. <br>
Risk: Trading decisions can be wrong because the halving-cycle model and market data may not predict actual Bitcoin outcomes. <br>
Mitigation: Use the declared tunables for max position, max trades, entry edge, slippage, and minimum liquidity to limit exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/kalshi-crypto-cycle-model-trader) <br>
- [Publisher Profile](https://clawhub.ai/user/diagnostikon) <br>
- [Simmer Skills](https://simmer.markets/skills) <br>
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk PyPI Package](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration] <br>
**Output Format:** [Console text with optional automaton JSON status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live mode can execute trades when explicitly started with --live.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
