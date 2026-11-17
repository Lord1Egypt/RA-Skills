## Description:

Use when repeated large fills suggest directional participation or informed flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to evaluate prediction-market trade flow where repeated large fills may indicate directional pressure. It helps shape custom Nautilus strategy code from exact market slugs and TradeTick backtests without presenting the archetype as a proven edge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large-fill clusters can be mistaken for reliable directional conviction or investment advice.

Mitigation: Frame outputs as research and backtesting guidance only, and require user review before any trading implementation.

Risk: Filled TradeTick replay cannot reveal maker intent, hidden liquidity, queue position, or live execution quality.

Mitigation: State these data limits in generated analyses and validate strategy ideas against market-specific fill quality before use.

## Reference(s):

- [Large Fill Pressure on ClawHub](https://clawhub.ai/superior-ai/skills/large-fill-pressure)
- [superior-ai publisher profile](https://clawhub.ai/user/superior-ai)

## Skill Output:

**Output Type(s):** [analysis, code, configuration, guidance]

**Output Format:** [Markdown with JSON configuration examples and strategy guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports strategy archetype generation for filled TradeTick backtests; outputs should not be treated as investment advice or automated trading authority.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
