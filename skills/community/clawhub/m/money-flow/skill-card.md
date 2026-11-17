## Description:

Chinese-language stock money-flow analysis skill that tracks major, super, and large-order net inflows and outflows, then compares them with price action to infer institutional intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danpian1](https://clawhub.ai/user/danpian1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to interpret Chinese stock money-flow concepts such as DDX, DDI, major-fund movement, large-order net flow, and price-volume confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides stock-analysis heuristics that may influence trading decisions.

Mitigation: Verify market data independently and do not treat generated buy, sell, or institutional-intent signals as professional financial advice.

Risk: Money-flow indicators can be delayed or misleading, including false inflow patterns and T+1 data latency described by the artifact.

Mitigation: Cross-check signals against current price action, volume, sector rotation, and other market evidence before acting.

## Reference(s):

- [Money-flow indicators reference](references/money-flow-indicators.md)
- [ClawHub skill page](https://clawhub.ai/danpian1/skills/money-flow)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or conversational text with structured analysis steps and indicator interpretations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language stock-analysis heuristics; no code execution, credentials, persistence, or external tool use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
