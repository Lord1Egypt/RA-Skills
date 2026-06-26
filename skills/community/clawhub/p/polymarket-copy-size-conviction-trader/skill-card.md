## Description: <br>
Weights Polymarket copy trading by portfolio concentration, using high-concentration whale positions to boost trade sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to analyze Polymarket trader portfolios, identify high-concentration whale positions, and paper-trade or explicitly live-trade aligned signals with configurable risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can place real Polymarket trades when run with --live and a valid Simmer API key. <br>
Mitigation: Start in paper mode, keep position limits low, review logs and signals before using --live, and revoke or restrict the API key when the skill is no longer in use. <br>
Risk: The workflow depends on external leaderboard and market data APIs, so stale data or weak market-title matches can produce incorrect trade candidates. <br>
Mitigation: Review matched markets, volume, spread, days-to-resolution gates, and trade logs before enabling live execution. <br>
Risk: Copy-trading concentrated whale positions can still follow losing, crowded, or manipulated markets. <br>
Mitigation: Tune concentration thresholds and YES/NO conviction bands, keep per-position exposure capped, and monitor aggregate open positions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-copy-size-conviction-trader) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, trade orders, configuration] <br>
**Output Format:** [Plain text run logs plus Simmer trade requests and signal metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
