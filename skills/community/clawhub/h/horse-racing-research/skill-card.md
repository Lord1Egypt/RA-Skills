## Description:

Research horse-race schedules, race cards, runner histories, and results through public FanDuel Racing and DraftKings Racing data. Use for race-day context or past-performance records, not wager picks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External racing researchers and racing fans can use the skill to assemble factual race-day cards and past-performance briefs from public FanDuel Racing and DraftKings Racing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Crawlora API key could be exposed when using the helper.

Mitigation: Keep the key private and do not include it in shared commands, logs, or output.

Risk: Research requests pass through Crawlora and may consume service credits; query parameters could expose private information.

Mitigation: Use a Crawlora API key rather than FanDuel or DraftKings login credentials, keep private information out of queries, and account for service credit use.

Risk: Odds and race records could be mistaken for forecasts or wagering advice.

Mitigation: Present odds as time-stamped observations and results as source records; do not infer a likely winner or recommend a wager.

## Reference(s):

- [Endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/horse-racing-research)
- [Crawlora publisher profile](https://clawhub.ai/user/crawlora-org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown race-card or past-performance brief with tables and source notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes provider and race identifiers, local time context, observation time, and explicit unknowns; informational context, not wagering advice.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
