## Description: <br>
Trades F1 Drivers Championship markets on Kalshi using recent race results weighted by recency. Hot streaks boost championship probability, cold streaks reduce it. Requires SIMMER_API_KEY and simmer-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to identify and optionally execute Kalshi F1 Drivers Championship trades based on a recency-weighted race momentum model. It supports dry-run review by default and live execution only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place automated trades when live mode is enabled, which can create real financial exposure. <br>
Mitigation: Test dry-run mode first, review position limits, and enable --live only after confirming the trading setup. <br>
Risk: The skill requires wallet and trading credentials that authorize the Simmer/DFlow/Solana execution path. <br>
Mitigation: Use a dedicated low-balance trading wallet and protect SIMMER_API_KEY and SOLANA_PRIVATE_KEY as high-value credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-f1-race-momentum-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON] <br>
**Output Format:** [Console text with optional JSON automaton reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run mode; live trading requires explicit --live execution and configured credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
