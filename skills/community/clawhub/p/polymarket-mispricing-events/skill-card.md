## Description: <br>
Detects mispricings on Polymarket by cross-referencing Kalshi and Manifold consensus probability, then trades the gap using Kelly criterion sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading automaton operators use this skill to scan prediction markets for cross-platform pricing gaps and execute configured Polymarket trades through Simmer. It is intended for users who can manage API credentials, paper-trading tests, position limits, and live-money trading controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run on a schedule and place live-money prediction-market trades without a clear per-trade approval step. <br>
Mitigation: Keep TRADING_VENUE set to sim until fully tested, confirm how to pause or uninstall the scheduled job, and enable live trading only after reviewing the behavior. <br>
Risk: Trading credentials can authorize automated actions if exposed or over-permissioned. <br>
Mitigation: Use restricted API credentials and rotate or revoke them if the deployment environment is no longer trusted. <br>
Risk: Automated trade sizing and market matching can create financial loss if configured too aggressively or matched incorrectly. <br>
Mitigation: Set conservative trade size and position limits, start with paper trading, and review live results before increasing exposure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Mibayy/polymarket-mispricing-events) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Kalshi Trade API](https://api.elections.kalshi.com/trade-api/v2) <br>
- [Manifold Markets API](https://api.manifold.markets/v0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [Console log text and configured trading API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on a 15-minute schedule when installed as a managed automaton; requires SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
