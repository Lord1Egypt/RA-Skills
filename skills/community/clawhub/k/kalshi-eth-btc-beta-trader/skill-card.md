## Description: <br>
Trades ETH price markets on Kalshi by using the beta relationship between ETH and BTC to identify lagging ETH market prices, with dry-run mode as the default and live trading enabled only by an explicit flag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to evaluate or run an automated ETH/BTC beta-lag strategy for Kalshi price markets. It discovers BTC and ETH markets, estimates fair ETH probabilities from BTC shifts, and can propose or execute trades subject to configured risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live execution can place real-money trades and create financial loss. <br>
Mitigation: Keep the skill in dry-run mode while evaluating behavior, and enable --live only after accepting the trading risk. <br>
Risk: The skill requires high-value credentials, including SIMMER_API_KEY and SOLANA_PRIVATE_KEY. <br>
Mitigation: Use a dedicated low-balance Solana wallet, protect environment variables, and rotate credentials if exposure is suspected. <br>
Risk: Trading behavior depends on simmer-sdk and market data from external services. <br>
Mitigation: Review or pin simmer-sdk before live use and monitor executions for unexpected market, slippage, or API behavior. <br>
Risk: Automated scheduling could repeatedly run the strategy if enabled. <br>
Mitigation: Leave cron disabled until the strategy has been reviewed, then set conservative trade limits and position sizes before scheduling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-eth-btc-beta-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and optional automaton JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable risk parameters for edge threshold, exit threshold, position size, trade count, slippage, liquidity, beta factor, and lag window.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
