## Description:

Pulls recent global gold-related news, connects it to macro drivers such as rates, yields, the dollar, inflation, geopolitics, and ETF flows, and returns a structured bullish, bearish, or wait-and-see sentiment read with confidence and risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyecho-io](https://clawhub.ai/user/cyecho-io)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agents use this skill to gather recent gold-market news, remove weak or repeated signals, and produce a concise sentiment read for short-term and medium-term market context. The skill is analysis support and not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public news requests expose queries to external news providers and may fail or return incomplete results.

Mitigation: Use the retrieval status and item counts before drawing conclusions, and report insufficient data when usable evidence is sparse.

Risk: Fetched headlines, sources, and links are untrusted content and may contain misleading market framing.

Mitigation: Treat fetched items as quoted evidence, prefer original high-credibility sources, and verify important financial conclusions independently.

Risk: Local cached snapshots can become stale while market-sensitive gold drivers change quickly.

Mitigation: Apply the documented freshness window and refresh the snapshot when the cache is stale or the user requests current analysis.

## Reference(s):

- [Automation Template](references/automation-template.md)
- [Scoring Rules](references/scoring-rules.md)
- [Source List](references/source-list.md)
- [Gold News Sentiment on ClawHub](https://clawhub.ai/cyecho-io/skills/gold-news-sentiment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON news snapshots and digest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include explicit timeframe, confidence, core drivers, key news items, uncertainty, and risk notes.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
