## Description: <br>
Detects smart money divergence in Polymarket by finding top-performing whale wallets that take positions opposite retail consensus at probability extremes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External prediction-market operators and agents use this skill to monitor Polymarket whale-versus-retail divergence and produce paper or explicitly live trading actions with configurable limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-money prediction-market trading can place live Polymarket orders when --live is enabled. <br>
Mitigation: Run in paper mode first, require clear human approval before enabling --live, and keep SIMMER_MAX_POSITION and SIMMER_MAX_POSITIONS low. <br>
Risk: The skill requires SIMMER_API_KEY, which is sensitive and could authorize trading activity. <br>
Mitigation: Store SIMMER_API_KEY only in a protected secret or environment variable and rotate it if exposure is suspected. <br>
Risk: Whale leaderboard and market activity signals may be incomplete, stale, or wrong. <br>
Mitigation: Review generated trade logs, retain spread, volume, days-to-resolution, slippage, and minimum-whale safeguards, and validate signals before live use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-whale-contrarian-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [Polymarket data API](https://data-api.polymarket.com) <br>
- [Polymarket leaderboard API](https://predicting.top/api/leaderboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Configuration] <br>
**Output Format:** [Console log text with Simmer SDK trade requests and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
