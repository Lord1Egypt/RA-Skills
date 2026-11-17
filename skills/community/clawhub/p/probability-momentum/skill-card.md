## Description:

Use when a Polymarket outcome price and filled volume are accelerating in the same direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to reason about Polymarket probability-momentum setups, backtest fit, strategy configuration, and failure modes for markets with accelerating price and filled volume.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated strategy or order examples could be mistaken for live trading instructions.

Mitigation: Treat outputs as financial-risk analysis and require explicit user confirmation before any live trading action.

Risk: Filled-trade backtests can overstate live execution quality because they do not prove maker queue position, maker rebates, or order-book depth.

Mitigation: Use outputs with a concrete market and backtest context, and review liquidity, expiry, and execution assumptions before relying on the strategy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/superior-ai/skills/probability-momentum)
- [Publisher Profile](https://clawhub.ai/user/superior-ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; generated strategy examples should be reviewed before trading.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
