## Description:

Fetch token market snapshots with price, liquidity, and volume data and return stable JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicholasoxford](https://clawhub.ai/user/nicholasoxford)

### License/Terms of Use:


## Use Case:

External developers and ClawHub/OpenClaw bot builders use this skill to fetch parseable token market snapshots for symbols, names, or mint addresses without wallet operations, swaps, or trade recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token queries are sent to a disclosed external market-data endpoint.

Mitigation: Use the skill only when external market-data lookup is appropriate for the user request.

Risk: Ambiguous prompts may trigger market-data lookup more often than intended.

Mitigation: Apply stricter market-data intent checks before invoking the skill.

Risk: Market snapshots can be mistaken for trading advice.

Mitigation: Return factual JSON data only and avoid wallet actions, swaps, or trade recommendations.

## Reference(s):

- [ClawHub Market Snapshot skill page](https://clawhub.ai/nicholasoxford/skills/market-snapshot)
- [Vecstack application](https://app.vecstack.com)
- [Market snapshot endpoint example](https://app.vecstack.com/api/skills/market-snapshot?q=SOL&source=openclaw)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stable parseable snapshot with null fields plus warnings or errors when market data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
