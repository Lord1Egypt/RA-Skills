## Description:

Analyze Polymarket football/soccer match URLs and estimate match win/draw probabilities using API-Football/API-SPORTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[remixmm](https://clawhub.ai/user/remixmm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to turn a Polymarket soccer URL into fixture lookup, API-Football prediction percentages, and a comparison with market-implied prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad date range can exhaust API-Football quota.

Mitigation: Keep --days small and prefer --fixture-id when the fixture ID is known.

Risk: Outputs combine third-party model predictions and market prices and can be mistaken for betting advice.

Mitigation: Present the results as API-Football prediction output and Polymarket prices, not as an independent betting recommendation.

Risk: Fixture matching can be ambiguous when team names, dates, or markets are unclear.

Mitigation: Ask for confirmation or rerun with --fixture-id when confidence is low or multiple candidates are reported.

## Reference(s):

- [API Reference](references/api-football-polymarket.md)
- [API-Football v3 documentation](https://www.api-football.com/documentation-v3)
- [Polymarket market data docs](https://docs.polymarket.com/market-data/fetching-markets)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable summary or structured JSON from the bundled TypeScript analysis script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an API-Football/API-SPORTS key and a Polymarket event or market URL, market slug, or fixture ID.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
