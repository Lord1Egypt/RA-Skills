## Description: <br>
Trades F1 Drivers Championship markets on Kalshi using teammate anti-correlation and requires SIMMER_API_KEY, SOLANA_PRIVATE_KEY, and simmer-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading developers use this skill to scan Kalshi F1 Drivers Championship markets, review teammate anti-correlation signals, and optionally execute small USDC trades when run with --live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-value trading credentials and can place real USDC trades when run with --live. <br>
Mitigation: Start in dry-run mode, review the signals, and use --live only when ready for real trades. <br>
Risk: Live trading exposes wallet funds to strategy, market, and execution risk. <br>
Mitigation: Use a dedicated low-balance Solana wallet, conservative position limits, and a scoped Simmer API key where possible. <br>
Risk: The trading implementation depends on simmer-sdk and uses configurable market safeguards. <br>
Mitigation: Verify the simmer-sdk dependency before providing credentials and review the edge, slippage, liquidity, and trade-count settings before live use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-f1-teammate-anti-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Console text with optional JSON automaton summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run mode; live trading requires --live and configured credentials.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
