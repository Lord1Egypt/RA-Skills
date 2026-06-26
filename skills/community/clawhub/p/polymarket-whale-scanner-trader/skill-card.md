## Description: <br>
Scans public Polymarket leaderboards to identify top-performing whale wallets by SmartScore and trade markets where those wallets have high-conviction positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to run an agent-assisted Polymarket strategy that scans public whale leaderboards, compares whale consensus with conviction signals, and places paper or live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can create real financial loss. <br>
Mitigation: Use paper mode first, require explicit live-trade approval, and keep strict position and drawdown limits. <br>
Risk: The skill requires sensitive trading credentials. <br>
Mitigation: Store SIMMER_API_KEY privately, use the smallest possible API scopes, and avoid withdrawal permissions. <br>
Risk: Market data, slippage, or liquidity conditions can make a whale-aligned signal unsuitable. <br>
Mitigation: Review orders before live execution and keep the configured volume, spread, position, and market-resolution safeguards enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-whale-scanner-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text, runtime configuration, and trading API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading unless live execution is explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
