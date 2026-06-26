## Description: <br>
Trades CPI/inflation markets on Kalshi using documented seasonal patterns in CPI data, with dry-run mode by default and live trading only when explicitly enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan Kalshi CPI and inflation markets, compare prices against a static seasonal adjustment model, review candidate trades, and optionally execute live USDC trades through Simmer when they enable live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires high-value trading credentials and wallet access. <br>
Mitigation: Use a dedicated low-balance wallet, keep SIMMER_API_KEY and SOLANA_PRIVATE_KEY scoped to this workflow, and avoid using primary wallets or accounts. <br>
Risk: Live mode can place or exit real USDC trades automatically. <br>
Mitigation: Start in dry-run mode, keep position limits low, and enable --live only after reviewing the strategy, dependency, and current configuration. <br>
Risk: Trading decisions depend on a static seasonal CPI model that may not reflect current market conditions. <br>
Mitigation: Review proposed trades before live execution and calibrate or supplement the signal with current CPI, energy, housing, and market data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-econ-seasonal-trader) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [CLI text output with optional JSON automaton status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run output reports detected signals and proposed trades; live mode can place and exit real-money trades.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
