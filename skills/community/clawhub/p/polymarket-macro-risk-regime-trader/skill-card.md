## Description: <br>
Detects macro risk regimes by scanning Polymarket categories for risk-on or risk-off signals and trading lagging markets that have not repriced yet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a configurable Polymarket macro regime strategy that scans market categories, computes cross-category sentiment, and proposes or places paper trades by default. Live trading requires an explicit live flag and acceptance of real USDC trading risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Start in paper mode and use --live only after reviewing position limits, spread limits, and market-selection behavior. <br>
Risk: The skill requires SIMMER_API_KEY, a credential with trading authority. <br>
Mitigation: Use a scoped, rotateable key and rotate it if exposed or no longer needed. <br>
Risk: Macro regime signals and cross-category assumptions can be wrong or stale. <br>
Mitigation: Review the configured thresholds and monitor generated trade reasoning before relying on live execution. <br>


## Reference(s): <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Python script, JSON configuration, and console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and tunable risk parameters; defaults to paper trading unless --live is used.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
