## Description:

Multi-Agent Trading Debate coordinates role-based market analysis, bull and bear arguments, judge verdicts, and position-sizing guidance for trading decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w491623834-oss](https://clawhub.ai/user/w491623834-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading teams use this skill to coordinate multi-agent market analysis, compare bull and bear cases, and produce a judge verdict with position sizing and follow-up logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may influence real trade execution decisions despite weak safeguards for that impact.

Mitigation: Use it only as analysis support unless explicit human approval is required before any order is placed.

Risk: Simulation-mode helper output or stale market assumptions could be mistaken for validated live market data.

Mitigation: Require validated live market data and label simulation output as non-actionable before using results in a trade decision.

Risk: Prediction and transaction-cost logs may contain sensitive trading activity or strategy details.

Mitigation: Document what is logged, who can access it, and how long records are retained.

## Reference(s):

- [Feishu Trading Debate Formats](references/feishu_format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown debate prompts and verdict templates, plus JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trading signal, confidence, position size, risk level, stop loss, next review, and prediction log fields.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
