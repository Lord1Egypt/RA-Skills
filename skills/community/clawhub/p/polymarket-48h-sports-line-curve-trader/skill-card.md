## Description: <br>
Trades structural mispricings in sports over/under markets by reconstructing the implied probability curve across multiple O/U line values for the same game and detecting monotonicity violations and set-vs-match inconsistencies in tennis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to analyze Polymarket sports over/under markets, identify implied curve inconsistencies, and execute paper trades by default. Live Polymarket trading is available only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Simmer API key that can authorize trading actions. <br>
Mitigation: Use a dedicated key, keep it out of logs and source control, and rotate it if exposed. <br>
Risk: Live mode can place real Polymarket trades with USDC when explicitly run with --live. <br>
Mitigation: Start in paper mode, keep trade-size and position tunables conservative, and enable live mode only after review. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review or pin the dependency before enabling live trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-48h-sports-line-curve-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance, shell command examples, and terminal log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper mode unless live trading is explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
