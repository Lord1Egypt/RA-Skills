## Description: <br>
Trades CPI range bin markets on Kalshi by normalizing mutually exclusive bin prices to identify and trade the most mispriced bin when deviation exceeds tolerance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a dry-run-by-default Kalshi CPI bin trading strategy, inspect signals, positions, and configuration, and optionally execute live trades when credentials and the live flag are supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can execute real-money automated trades. <br>
Mitigation: Run in dry-run mode first and pass --live only when intentionally authorizing live execution. <br>
Risk: The skill requires high-value trading and wallet credentials. <br>
Mitigation: Use limited Simmer/Kalshi authority and a dedicated low-balance Solana wallet for live mode. <br>
Risk: Third-party dependency behavior may affect trading and credential handling. <br>
Mitigation: Review or pin simmer-sdk before providing secrets. <br>
Risk: Strategy language could be mistaken for a guarantee of profit or safety. <br>
Mitigation: Treat the bin-sum strategy as a trading heuristic and review outputs before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-econ-bin-sum-trader) <br>
- [Simmer Markets skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Console text with optional JSON automaton reports and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry run is the default; live execution requires explicit --live mode and Simmer/Kalshi credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact metadata version is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
