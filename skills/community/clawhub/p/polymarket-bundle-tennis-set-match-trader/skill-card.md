## Description: <br>
Trades Polymarket tennis prop-market constraint violations across Set 1 games, match games, total sets, set handicap, and set/match winner bundles, defaulting to paper trading unless live mode is explicitly enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and advanced trading operators use this skill to scan Polymarket tennis prop bundles for structural price inconsistencies and submit simulated or explicitly enabled live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real USDC trades on Polymarket when SIMMER_API_KEY is configured and --live is passed. <br>
Mitigation: Keep the default paper trading mode until the strategy assumptions, market selection, and position-size tunables have been reviewed. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Store the key only in the intended runtime secret store, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: Constraint signals may be wrong or stale if markets are parsed incorrectly or liquidity conditions change. <br>
Mitigation: Use the configured minimum volume, spread, position, and violation thresholds, and review trade logs before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-bundle-tennis-set-match-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console log text with Simmer SDK trade API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires --live and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
