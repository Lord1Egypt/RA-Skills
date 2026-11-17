## Description:

Trade Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via Simmer API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to configure an agent that discovers Polymarket fast crypto markets, evaluates short-window CEX momentum signals, and proposes or executes trades through Simmer. It is intended for users who understand automated trading risk and can review strategy parameters before live execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket orders and the security review flags stale GTC cleanup behavior that may cancel orders not definitively tied to this skill.

Mitigation: Review or disable stale GTC cleanup before live use, and run in dry-run or an isolated account with small limits until behavior is verified.

Risk: The release depends on an unpinned simmer-sdk range for trading execution.

Mitigation: Pin the exact reviewed simmer-sdk version before deployment and re-review behavior before upgrading.

Risk: Fast markets may resolve before scheduled stop-loss or take-profit monitors can act.

Mitigation: Use conservative position sizing, daily budgets, and dry-run observation rather than relying on automated stop-losses for 5-minute or 15-minute markets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-fast-loop)
- [Simmer dashboard](https://simmer.markets/dashboard?ref=sdk-skill&utm_campaign=sdk-skill)
- [Simmer Polymarket V2 migration guide](https://docs.simmer.markets/v2-migration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration values, and trading run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live trading requires explicit --live use and Simmer credentials.]

## Skill Version(s):

1.7.4 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
