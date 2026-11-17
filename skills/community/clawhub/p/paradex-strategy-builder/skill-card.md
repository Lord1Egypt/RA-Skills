## Description:

Designs, backtests, and reasons about Paradex trading strategies from natural language requests, producing structured trading plans with entry and exit rules, risk parameters, and historical validation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sv](https://clawhub.ai/user/sv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert Paradex trading ideas into structured strategy specifications, historical sanity checks, and execution-planning notes. It is intended for strategy design and analysis, not trade execution or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading strategies and example parameters may be inaccurate, incomplete, or unsuitable for current market conditions.

Mitigation: Review every generated strategy independently and treat historical checks as sanity checks rather than guaranteed outcomes.

Risk: Users could mistake strategy analysis for trade execution readiness or financial advice.

Mitigation: Keep execution separate from this skill, and use authenticated order tools only after an intentional review and decision to trade.

Risk: Backtest-style outputs based on kline or trade data may omit fills, slippage, fees, queue priority, and execution timing.

Mitigation: Validate strategies with execution-aware tooling and account for fees, slippage, and liquidity before deployment.

## Reference(s):

- [Expanded Strategy Templates](references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/sv/skills/paradex-strategy-builder)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown strategy specifications with structured rules, historical-check summaries, execution notes, and risk summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute trades; generated strategies require independent review before any trading action.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
