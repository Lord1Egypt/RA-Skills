## Description: <br>
Trades Bitcoin price bin markets on Kalshi by comparing market-implied volatility to BTC historical ~60% annualized volatility using a lognormal model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-system operators use this skill to evaluate Kalshi BTC price-bin markets and optionally execute trades when a lognormal volatility model diverges from market prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live use can involve a Solana private key and real-money automated trades. <br>
Mitigation: Start in dry-run mode, review trader.py and simmer-sdk, use a dedicated low-balance Solana wallet and scoped API key, keep trade limits low, and enable --live or scheduling only after accepting the financial risk. <br>
Risk: Credential exposure could compromise SIMMER_API_KEY or SOLANA_PRIVATE_KEY. <br>
Mitigation: Provide credentials only through protected environment variables or a secrets manager, scope access where possible, and rotate credentials if exposure is suspected. <br>
Risk: The volatility model and market assumptions may produce losing trades. <br>
Mitigation: Tune max position size, max trades per run, slippage, liquidity, entry edge, and exit threshold before live use, and monitor positions after execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/diagnostikon/kalshi-crypto-volatility-skew-trader) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text with optional JSON automaton status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires --live and configured SIMMER_API_KEY and SOLANA_PRIVATE_KEY.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
