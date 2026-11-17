## Description:

Autonomous paper trading research agent for Interactive Brokers that helps an agent connect to IBKR, generate technical and news-aware trade decisions, manage positions, log performance, and tune strategy parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[player-1101](https://clawhub.ai/user/player-1101)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-system builders use this skill to run or adapt an IBKR paper trading workflow with strategy signals, brokerage execution, risk checks, news sentiment, and performance logging. It is appropriate only when the operator has reviewed brokerage access, paper/live account separation, and automated trading controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place brokerage orders through IBKR.

Mitigation: Run it only with an isolated paper trading account until brokerage permissions, live-mode gating, and final risk checks have been reviewed and approved.

Risk: The shutdown path can automatically close every visible position.

Mitigation: Require operator confirmation or disable automated shutdown liquidation before connecting the skill to any live or mixed-use brokerage account.

Risk: Strategy and news weights can be tuned from runtime performance history.

Mitigation: Review proposed parameter and weight changes before allowing them to affect live execution, and keep a rollback path through versioned strategy memory.

## Reference(s):

- [IBKR Connection & Authentication Reference](references/ibkr_connection.md)
- [Order Types Reference](references/order_types.md)
- [Self-Improvement Algorithm Reference](references/self_improvement.md)
- [Interactive Brokers](https://www.interactivebrokers.com)
- [Google News RSS Search](https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en)
- [ClawHub Skill Page](https://clawhub.ai/player-1101/skills/ibkr-auto-trade)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code, shell commands, YAML configuration, and JSON memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce brokerage workflow guidance, trade decision records, execution instructions, risk-check explanations, logs, and configuration changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
