## Description: <br>
Scans Polymarket markets for tight bid-ask spreads combined with extreme probabilities, then can place small conviction-sized trades on matching outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to evaluate a Polymarket micro-spread trading strategy in paper mode and, when explicitly enabled, execute small live USDC orders through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real USDC trades on Polymarket. <br>
Mitigation: Use paper mode first and enable --live only with a restricted Simmer/Polymarket key and funds the user is prepared to lose. <br>
Risk: The security summary says the documentation overstates coverage and safeguards. <br>
Mitigation: Verify the real discovery scope, thresholds, and safeguards before relying on the strategy or increasing position limits. <br>
Risk: The skill requires SIMMER_API_KEY, which grants trading authority. <br>
Mitigation: Store the key as a secret, scope it narrowly, rotate it when needed, and avoid sharing it with unrelated tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-micro-spread-sniper-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Console text and Simmer trade requests configured by environment variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require an explicit --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
