## Description: <br>
Calculate optimal bet sizes using Kelly Criterion, including single bets, fractional Kelly sizing, multi-bet portfolio sizing, and max-bet enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate bankroll-based wager sizes from odds and estimated true probabilities, including conservative fractional Kelly sizing and multi-bet allocation scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce betting stake recommendations that depend on user-provided probability estimates and bankroll values. <br>
Mitigation: Verify odds, probability estimates, bankroll constraints, and applicable rules before using any output as betting guidance. <br>
Risk: The artifact demonstrates inline Python commands that an agent may run locally. <br>
Mitigation: Inspect generated commands before execution and grant only command or filesystem access needed for the sizing calculation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/kelly-sizer) <br>
- [AgentBets Kelly sizer guide](https://agentbets.ai/guides/openclaw-kelly-sizer-skill/) <br>
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, text] <br>
**Output Format:** [Markdown with inline Python shell commands and calculated text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided bankroll, odds, and estimated true probability; uses python3 for calculations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
