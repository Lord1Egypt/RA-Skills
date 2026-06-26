## Description: <br>
Trades monotonicity violations in NHL hockey O/U market ladders and spread-vs-total consistency on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and trading operators use this skill to monitor NHL Polymarket over/under ladders, identify pricing inconsistencies, and run paper-first or explicitly live trading workflows with configurable risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using the configured account. <br>
Mitigation: Start in paper mode, require an explicit --live run for real trades, and keep conservative position size and open-position limits before risking funds. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Store the key only in trusted runtime secrets, limit access to authorized operators, and rotate it if exposure is suspected. <br>
Risk: Market signals may be wrong or become stale before execution. <br>
Mitigation: Use the configured volume, spread, threshold, minimum-violation, and open-position controls to reduce exposure from weak or illiquid signals. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/diagnostikon/polymarket-ladder-nhl-hockey-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance and Python runtime output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and uses live Polymarket trading only when explicitly run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
