## Description: <br>
Trades Polymarket coffee markets using three compounding seasonal edges: Brazil frost window mispricing, harvest cycle awareness, and ENSO phase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a configurable Polymarket coffee-market trading agent that searches for coffee-related markets, applies seasonal conviction sizing, and defaults to paper trading unless live mode is explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using the configured account. <br>
Mitigation: Start in paper mode, enable live mode only intentionally, and use a dedicated low-balance API key or account. <br>
Risk: The trading edge is speculative and may not perform as described. <br>
Mitigation: Review max position and max open position settings before live use and treat seasonal signals as assumptions to validate, not guarantees. <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Store the key as a secret, limit its balance and permissions where possible, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-coffee-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trade decisions, skip reasons, and configuration-driven behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and uses tunable limits for maximum position size, spread, minimum volume, days to resolution, open positions, thresholds, minimum trade size, and ENSO phase.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
