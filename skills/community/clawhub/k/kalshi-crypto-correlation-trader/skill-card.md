## Description: <br>
Monitors BTC and ETH Kalshi price-level markets, estimates ETH fair value from a BTC/ETH beta signal, and surfaces or executes trades when configured edge thresholds are met. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to evaluate BTC/ETH correlation signals on Kalshi, run dry-run analyses, and optionally execute live Simmer/DFlow trades with configured limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can use wallet and trading credentials to place real financial trades. <br>
Mitigation: Run dry mode first, use a dedicated low-balance wallet and limited credentials, and invoke --live only after reviewing the strategy and configuration. <br>
Risk: The release security summary flags sensitive credentials and under-scoped position-exit behavior for review. <br>
Mitigation: Review the exit thresholds, max position size, max trades per run, slippage limit, and dependency behavior before scheduling or automating the skill. <br>
Risk: The skill depends on simmer-sdk and optional tradejournal behavior outside the artifact. <br>
Mitigation: Verify simmer-sdk and any tradejournal integration before providing live credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/kalshi-crypto-correlation-trader) <br>
- [Simmer Skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls] <br>
**Output Format:** [Console text with optional JSON automaton summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry run is the default; live trading requires the explicit --live flag and configured Simmer and Solana credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
