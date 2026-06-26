## Description: <br>
Trades BTC weekend price threshold markets on Polymarket by comparing first-passage and terminal probability signals, then scaling conviction by entry timing and BTC halving-cycle volatility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agents use this skill to discover BTC weekend threshold markets, calculate conviction from market probabilities and strategy constraints, and run the trader in paper mode or explicitly enabled live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can operate on real funds when live trading is enabled. <br>
Mitigation: Use paper mode first, provide exchange credentials with minimum permissions, disable withdrawals, and enable live mode only after verifying confirmation, risk limits, and logging. <br>
Risk: The security review found live-trading safeguards were not documented consistently enough for automatic approval. <br>
Mitigation: Review the skill before installation and keep position size, spread, volume, and maximum-open-position settings conservative until behavior is validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-btc-weekend-volatility-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python trading script behavior, configuration values, and console logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless live mode is explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
