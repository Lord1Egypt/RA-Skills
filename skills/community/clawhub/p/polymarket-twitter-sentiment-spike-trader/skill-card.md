## Description: <br>
Detects crisis and news spikes across other Polymarket markets and adjusts expected posting rates upward for post-count bins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to analyze crisis-adjacent Polymarket signals and produce paper-by-default trading actions for post-count prediction markets. Live Polymarket execution is available only when the operator supplies a Simmer API key and explicitly passes the live flag. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live execution can place real Polymarket trades when a live-capable Simmer key is present and --live is passed. <br>
Mitigation: Start in paper mode, keep --live as a manual operator action, and use restricted or test credentials where possible. <br>
Risk: SIMMER_API_KEY is a sensitive credential with trading authority. <br>
Mitigation: Store the key outside source files, limit where live-capable keys are available, and rotate the key if it may have been exposed. <br>
Risk: Trade sizing and open-position limits affect financial exposure. <br>
Mitigation: Tune max position size, minimum trade size, thresholds, and max open positions conservatively before any live run. <br>
Risk: The documented minimum-volume filter is not enforced by the current trading script. <br>
Mitigation: Do not rely on minimum-volume protection until the implementation is updated and verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-twitter-sentiment-spike-trader) <br>
- [Simmer skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python execution commands and runtime trade-status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless --live is passed.] <br>

## Skill Version(s): <br>
0.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
