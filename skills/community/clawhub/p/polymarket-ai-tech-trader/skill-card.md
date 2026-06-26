## Description: <br>
Trades Polymarket prediction markets on AI model releases, tech IPOs, product launches, GPU infrastructure milestones, and AI regulation events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as an advanced Polymarket trading template for AI and technology prediction markets. It discovers relevant markets, applies configurable position controls, and defaults to simulated trading unless live execution is explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when live mode is enabled. <br>
Mitigation: Keep the skill in paper mode first, use a least-privileged SIMMER_API_KEY, and enable live mode only after reviewing the strategy logic and portfolio exposure controls. <br>
Risk: Advertised strategy and risk controls may be broader than the code enforces. <br>
Mitigation: Review the dependency version, market-selection behavior, and configured thresholds before enabling live trading, cron, or automaton runs. <br>
Risk: The required SIMMER_API_KEY is a sensitive trading credential. <br>
Mitigation: Store the credential privately and avoid placing a live-capable key in environments where automated code can call live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-ai-tech-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console status text with trade decisions, setup commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and supports tunable trading thresholds, position sizing, spread limits, and position caps.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata; artifact metadata also lists 1.0 in SKILL.md and 0.0.2 in clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
