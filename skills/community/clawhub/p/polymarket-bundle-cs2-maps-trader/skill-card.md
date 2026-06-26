## Description: <br>
Trades CS2 best-of-three winner markets on Polymarket when individual map winner prices imply a different match outcome. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and trading operators use this skill to monitor CS2 map and match markets, calculate best-of-three pricing differences, and place paper or explicitly enabled live Polymarket trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real funds. <br>
Mitigation: Run in paper mode first and use a dedicated low-balance or least-privilege trading key for live testing. <br>
Risk: Some documented risk limits may not be enforced by the code. <br>
Mitigation: Do not rely on minimum-volume or concurrent-position limits unless the code is fixed or the limits are enforced separately. <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Store the key as a secret, limit its permissions where possible, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-bundle-cs2-maps-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Python trading workflow with runtime logs, tunable configuration, and Simmer SDK trade calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper trading is the default. Live Polymarket trading requires --live and SIMMER_API_KEY, and may spend real funds.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
