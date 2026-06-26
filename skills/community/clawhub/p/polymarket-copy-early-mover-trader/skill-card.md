## Description: <br>
Identifies which whale wallet consistently enters markets first before others follow, then copies that lead indicator wallet's fresh positions before the herd pushes prices away. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and advanced prediction-market operators use this skill to monitor Polymarket whale activity, identify wallets that tend to enter markets before followers, and copy fresh aligned positions through Simmer. It is intended for users who understand wallet credentials, prediction-market trading, and the risk of financial loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and lose funds. <br>
Mitigation: Use paper mode first and enable live trading only deliberately after reviewing strategy behavior and market risk. <br>
Risk: The skill requires sensitive credentials through SIMMER_API_KEY. <br>
Mitigation: Protect the API key as a secret, scope access where possible, and avoid exposing it in logs or shared environments. <br>
Risk: Copy-trading signals can be wrong, delayed, crowded, or affected by slippage. <br>
Mitigation: Keep trade-size and max-position tunables conservative, and use the built-in volume, spread, freshness, and portfolio gates. <br>
Risk: The skill depends on simmer-sdk and external prediction-market data APIs. <br>
Mitigation: Review the simmer-sdk dependency and monitor API availability before relying on automated runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-copy-early-mover-trader) <br>
- [Predicting.top leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trade decisions and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk dependency; defaults to paper mode unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
