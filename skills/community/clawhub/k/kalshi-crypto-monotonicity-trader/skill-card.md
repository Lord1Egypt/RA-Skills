## Description: <br>
Enforces monotonicity constraints on crypto price-level markets on Kalshi and trades violations by buying underpriced lower-threshold contracts and selling overpriced higher-threshold ones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent operators use this skill to scan Kalshi crypto price-level markets for BTC or ETH monotonicity violations, review dry-run opportunities, and optionally execute bounded live trades with configured risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute automated financial trades when run with live mode and valid trading credentials. <br>
Mitigation: Run in dry-run mode first, enable --live only deliberately, and keep max position size, max trades per run, slippage, and liquidity limits conservative. <br>
Risk: The skill requires high-value SIMMER_API_KEY and SOLANA_PRIVATE_KEY credentials for live trading. <br>
Mitigation: Use a dedicated low-balance Solana key, avoid primary wallets, and keep credentials scoped and isolated from unrelated environments. <br>
Risk: The security scan verdict is suspicious because the skill handles trading and wallet credentials with incomplete top-level scoping. <br>
Mitigation: Review or pin the simmer-sdk dependency and inspect behavior before installing or scheduling live execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/kalshi-crypto-monotonicity-trader) <br>
- [Simmer Skills](https://simmer.markets/skills) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [CLI text output and JSON automaton reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run mode; live trading requires an explicit --live flag and configured credentials.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
