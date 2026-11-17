## Description:

Portfolio Optimizer combines virtual-trading MCP price data with news analysis scores to recommend and execute virtual buy, sell, hold, and rebalance decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kackyt](https://clawhub.ai/user/kackyt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a virtual portfolio strategy that reads recent market-news sentiment, checks virtual portfolio state and prices, places virtual trades, and reports the resulting allocation and strategy state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a connected virtual portfolio by placing buy and sell orders.

Mitigation: Require confirmation or dry-run review before order execution, especially when testing a new strategy configuration.

Risk: The skill can overwrite persistent strategy state used by later runs.

Mitigation: Review proposed strategy_state.md changes before writing them and keep recoverable history for prior state.

Risk: The skill fetches mutable external news-analysis content through unpinned git updates.

Mitigation: Use a trusted analysis source and pin or review the exact revision before relying on its scores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kackyt/skills/portfolio-optimizer)
- [News analysis format](references/news-analysis-format.md)
- [Virtual Trading MCP API reference](references/virtual-trading-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, files, guidance]

**Output Format:** [Markdown report with inline commands, virtual-trading MCP tool calls, and strategy state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces virtual trading actions and may update strategy_state.md between runs.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
