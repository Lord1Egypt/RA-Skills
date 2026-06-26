## Description: <br>
Automatically discovers and ranks top Polymarket wallets from public leaderboards, evaluates rolling performance, and builds a dynamic copy roster for Simmer SDK copytrading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to evaluate public Polymarket leaderboard wallets, build a ranked dynamic copy roster, and run simulated or explicitly enabled live copytrading through Simmer SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can execute real Polymarket trades and cause financial loss. <br>
Mitigation: Start in paper mode, keep trade caps low, and use --live only when the operator accepts live-trading risk. <br>
Risk: The skill requires sensitive Simmer trading credentials. <br>
Mitigation: Use a dedicated low-privilege API key where possible and store SIMMER_API_KEY securely. <br>
Risk: Copytrading depends on public leaderboard and market data quality. <br>
Mitigation: Review the generated roster and maintain conservative roster, position, spread, and trade-count limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-copy-dynamic-roster-trader) <br>
- [Predicting.top leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text with Simmer SDK API requests and configurable environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires simmer-sdk and SIMMER_API_KEY; defaults to paper mode unless --live is explicitly used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
