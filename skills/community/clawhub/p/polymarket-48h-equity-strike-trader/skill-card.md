## Description: <br>
Trades structural mispricings in equity/stock price-threshold markets by reconstructing the implied probability curve across strike levels for the same company and period, detecting monotonicity breaks and range-sum inconsistencies in strike ladders for PLTR, MSFT, NVDA, TSLA, SpaceX, Nasdaq-100, and other equity markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and prediction-market operators use this skill to scan Polymarket equity strike ladders for monotonicity, range-sum, and bin-sum inconsistencies, then place paper or explicitly enabled live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when intentionally run in live mode. <br>
Mitigation: Test in paper mode first, use live mode only deliberately, and keep conservative position, spread, volume, threshold, and maximum-open-position limits. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Provide the key only in the runtime environment, keep it out of source control and logs, restrict access to it, and rotate it if exposed. <br>
Risk: The external simmer-sdk dependency mediates market access and trade execution. <br>
Mitigation: Review or pin the dependency before real-money use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-48h-equity-strike-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Console text logs and Simmer trade API calls; documentation is Markdown with environment-variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the --live flag and SIMMER_API_KEY. Position size, spread, volume, threshold, and maximum-open-position limits are tunable.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release metadata); artifact frontmatter declares 1.0.0 and clawhub.json declares 0.0.2 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
