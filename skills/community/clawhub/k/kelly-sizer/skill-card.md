## Description:

Calculate Kelly Criterion bet sizes from bankroll, odds, and an estimated true probability, with advertised fractional, portfolio, and maximum-bet safeguards requiring review because the security evidence says they are not enforced.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate Kelly Criterion bet sizing for wagers when bankroll, odds, and the user's true probability estimate are available. Outputs should be treated as informational betting guidance, not as enforced risk controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an unsafe shell-command pattern when raw user-provided values are substituted into the command.

Mitigation: Use a validated script or an argument-array invocation instead of interpolating raw user input into a shell command.

Risk: The skill advertises fractional Kelly, portfolio sizing, and maximum-bet safeguards that the security evidence says are not enforced.

Mitigation: Treat these safeguards as unverified and independently validate stake limits, fractional multipliers, and portfolio allocation before acting on the output.

Risk: The output may be used for betting or bankroll decisions where incorrect inputs or calculations can cause financial loss.

Mitigation: Review the inputs, odds conversion, true probability estimate, and final stake recommendation before using the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/skills/kelly-sizer)
- [AgentBets](https://agentbets.ai)
- [OpenClaw Kelly Sizer tutorial](https://agentbets.ai/guides/openclaw-kelly-sizer-skill/)
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline Python shell command snippets and explanatory calculation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; output is informational and should be reviewed before use for financial or betting decisions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
