## Description: <br>
Trades structural mispricings in sports over/under markets by reconstructing the implied probability curve across multiple O/U line values for the same game and detecting monotonicity violations and set-vs-match inconsistencies in tennis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to analyze Polymarket sports over/under markets for structural pricing inconsistencies and run a paper-first trading workflow. Live trading is available only when explicitly enabled with the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades using USDC when run with the live flag. <br>
Mitigation: Use paper mode first and enable --live only with a dedicated low-balance or least-privilege SIMMER_API_KEY. <br>
Risk: SIMMER_API_KEY is a high-value credential used for trading authority. <br>
Mitigation: Store the credential securely, restrict its scope where possible, and avoid sharing it with unrelated workflows. <br>
Risk: The trading integration depends on simmer-sdk. <br>
Mitigation: Review or pin simmer-sdk before live use because it handles market access and trade execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/diagnostikon/polymarket-24h-sports-line-curve-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, api calls] <br>
**Output Format:** [Console logs, command-line execution, configuration values, and Simmer trading API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper trading is the default; live Polymarket trading requires the explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
