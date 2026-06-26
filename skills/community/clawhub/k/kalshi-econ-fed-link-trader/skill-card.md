## Description: <br>
Cross-market strategy that uses CPI bin prices to estimate CPI level, then adjusts Fed rate market positions via a sensitivity model. High CPI means Fed less likely to cut. Requires SIMMER_API_KEY and simmer-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to inspect CPI-linked Kalshi markets, compare CPI-implied Fed probabilities against Fed rate market prices, and identify or execute bounded trading opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place and close real USDC positions automatically. <br>
Mitigation: Test in dry-run first and pass --live only when intentional. <br>
Risk: The skill requires trading credentials and a Solana private key for live execution. <br>
Mitigation: Use a dedicated low-balance wallet and API key. <br>
Risk: Recurring automation can repeatedly execute the trading strategy if enabled. <br>
Mitigation: Keep cron disabled unless recurring execution is intended. <br>
Risk: The simmer-sdk dependency receives live trading authority when credentials are provided. <br>
Mitigation: Review or pin simmer-sdk before supplying live credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/kalshi-econ-fed-link-trader) <br>
- [Simmer Skills](https://simmer.markets/skills) <br>
- [simmer-sdk PyPI Package](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text with dry-run opportunity reports, position/config views, and optional live trading actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run; --live can place and close real USDC positions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
