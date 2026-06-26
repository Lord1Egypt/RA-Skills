## Description: <br>
Detects when multiple whale wallets exit positions simultaneously, causing market overshooting. Fades the panic by buying the dip after whale dumps, exploiting retail panic-selling that pushes prices below fair value. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to scan public Polymarket whale activity, identify coordinated exit events, and generate fade-trade decisions with configurable risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and cause financial loss. <br>
Mitigation: Run in paper mode first, review thresholds and position limits, and enable --live only after confirming the configuration. <br>
Risk: The skill requires SIMMER_API_KEY, which is a sensitive credential. <br>
Mitigation: Provide the key only through a secure environment variable and avoid exposing it in prompts, logs, or shared files. <br>
Risk: Signals depend on public leaderboard and activity APIs that may be incomplete, delayed, or unavailable. <br>
Mitigation: Treat generated trades as proposals to review, and keep spread, volume, slippage, and position gates enabled. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-whale-exit-fade-trader) <br>
- [predicting.top Leaderboard API](https://predicting.top/api/leaderboard) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Shell commands, Configuration] <br>
**Output Format:** [Console text with simulated or live trade requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
