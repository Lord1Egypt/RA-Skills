## Description: <br>
Trades Fed rate markets on Kalshi based on macro data releases (CPI, jobs). Scans CPI bin markets for implied CPI, adjusts rate cut probabilities using data sensitivity model. Requires SIMMER_API_KEY and simmer-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to identify and optionally trade Kalshi Fed rate markets after CPI or jobs data changes expected rate-cut probabilities. It defaults to dry-run mode and requires explicit live execution plus trading credentials before placing real USDC trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated trading can cause real financial loss when live mode is enabled. <br>
Mitigation: Keep the skill in dry-run mode first, use the disclosed risk tunables, and pass --live only after reviewing the strategy and credentials. <br>
Risk: The skill requires sensitive trading and wallet credentials. <br>
Mitigation: Use dedicated low-balance trading credentials and review simmer-sdk before supplying live credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-fed-data-reaction-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration] <br>
**Output Format:** [Console text with optional JSON automaton status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires --live and configured credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
