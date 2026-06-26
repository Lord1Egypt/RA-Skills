## Description: <br>
Trades temporal inconsistencies across geopolitical markets with different deadlines, identifying later-deadline underpricing and diplomacy-versus-escalation inversions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan Polymarket geopolitical markets for deadline-cascade inconsistencies, generate YES/NO trade signals, and optionally execute trades through Simmer in paper or live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running with --live can place real Polymarket trades using USDC. <br>
Mitigation: Use paper mode first, run live mode only intentionally, and keep conservative position limits. <br>
Risk: SIMMER_API_KEY grants trading authority and should be treated as a high-value credential. <br>
Mitigation: Use a revocable least-privilege SIMMER_API_KEY and rotate or revoke it when live access is no longer needed. <br>
Risk: The skill depends on an unpinned simmer-sdk package for trading access. <br>
Mitigation: Review the simmer-sdk dependency before funding live use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-geopolitics-deadline-cascade-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration values; runtime output is console text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and uses live trading only with the --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
