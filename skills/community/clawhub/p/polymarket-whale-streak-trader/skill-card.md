## Description: <br>
Tracks rolling win rate per whale wallet and only follows wallets on a verified hot streak, dynamically promoting and demoting wallets based on recent performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading automation users use this skill to evaluate Polymarket whale-wallet performance and place paper or explicitly enabled live copy trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated trading can place real Polymarket orders when the live flag is used. <br>
Mitigation: Run in paper mode first, review market matching and tunables, and use --live only after validating behavior. <br>
Risk: The skill requires sensitive Simmer or Polymarket-linked credentials. <br>
Mitigation: Use a least-privilege credential with limited funds and keep SIMMER_API_KEY out of shared logs and source control. <br>
Risk: Whale streak signals and market matching may select unsuitable or illiquid markets. <br>
Mitigation: Review thresholds, spread, volume, slippage, days-to-resolution gates, and trade logs before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-whale-streak-trader) <br>
- [predicting.top leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text with trade status messages and configurable environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
