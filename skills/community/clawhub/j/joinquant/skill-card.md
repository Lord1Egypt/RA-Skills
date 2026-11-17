## Description:

JoinQuant helps agents use the JoinQuant quantitative trading platform for A-share, futures, fund, and index data queries, event-driven strategy backtests, and simulated trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and quantitative researchers use this skill to generate JoinQuant/JQData setup guidance, API examples, and Python strategy snippets for market data research, backtesting, and simulated trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated trading examples can place or liquidate orders if adapted into live strategy contexts.

Mitigation: Run examples in backtest or simulation first and require explicit approval before any live order or liquidation action.

Risk: JoinQuant credentials are required for data access and could be exposed in source code or logs.

Mitigation: Keep credentials out of source code and logs by using environment variables or a secret manager.

Risk: The release uses broad dependency requirements and may run in environments connected to account state.

Mitigation: Use a virtual environment with pinned, reviewed dependency versions before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderwpf/skills/joinquant)
- [JoinQuant official website](https://www.joinquant.com)
- [JoinQuant API documentation](https://www.joinquant.com/help/api/help)
- [JoinQuant community](https://www.joinquant.com/community)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JoinQuant/JQData API examples, credential setup guidance, and trading strategy snippets.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact files also mention 1.1.0 and 1.2.0, so verify before publication)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
