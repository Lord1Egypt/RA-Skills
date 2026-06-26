## Description: <br>
Trades F1 Drivers Championship winner markets on Kalshi using current points standings and Monte Carlo simulation to compute win probabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify and optionally execute Kalshi F1 Drivers Championship trades when a points-based Monte Carlo model diverges from market prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute real-money automated trades when live mode is enabled. <br>
Mitigation: Start in dry-run mode, enable --live only intentionally, keep max position and trade-count tunables small, and review all trading behavior before deployment. <br>
Risk: Live trading requires sensitive API and wallet credentials. <br>
Mitigation: Use a dedicated low-balance Solana wallet and limited trading credentials; do not provide a main wallet private key. <br>
Risk: The strategy depends on static F1 standings, driver ratings, and third-party market data. <br>
Mitigation: Review and update the model inputs and simmer-sdk behavior before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-f1-points-model-trader) <br>
- [Simmer skills](https://simmer.markets/skills) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, JSON automaton reports, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires explicit --live and configured credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
