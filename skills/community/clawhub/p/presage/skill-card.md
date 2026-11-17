## Description:

Connects agents to the Presage prediction market terminal on Solana to analyze live YES/NO markets, identify opportunities, and review portfolio data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seenfinity](https://clawhub.ai/user/seenfinity)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let compatible agents query Presage market data, surface trading-opportunity analysis, and inspect agent portfolio balances and positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market queries, agent IDs, portfolio results, balances, positions, P&L, and trade reasoning may expose sensitive trading or performance information.

Mitigation: Use only agent IDs and portfolio data appropriate to share with Presage and downstream agent context; avoid submitting confidential account identifiers or sensitive portfolio details.

Risk: Market analysis and opportunity recommendations can be incorrect, stale, or misleading for trading decisions.

Mitigation: Treat outputs as decision support rather than trading instructions, and require human review before acting on recommendations.

## Reference(s):

- [Presage API Reference](references/api-docs.md)
- [Presage Market](https://presage.market)
- [Presage API](https://presage.market/api)
- [ClawHub Skill Page](https://clawhub.ai/seenfinity/skills/presage)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown or JSON-style analysis summaries, depending on the calling agent workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market, opportunity, and portfolio analysis based on Presage API responses]

## Skill Version(s):

1.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
