## Description:

Aggregates recent results from Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and web search into research briefs with AISA planning, clustering, reranking, and JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to research recent people, companies, products, competitors, releases, market topics, and trends across social, community, market, GitHub, and web sources. It is best suited for time-sensitive briefs and structured summaries, not static encyclopedia questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and selected result text may leave the local machine for AISA and other source APIs.

Mitigation: Use the skill only for topics appropriate for those services, configure credentials deliberately, and review provider terms before submitting sensitive queries.

Risk: Webhook delivery can send findings to an external destination when configured.

Mitigation: Configure delivery only for trusted webhook URLs and review destination access before enabling watchlist notifications.

Risk: The Xiaohongshu source depends on a local logged-in service path.

Mitigation: Avoid enabling the Xiaohongshu source unless that local service is intended and trusted.

Risk: Developer evaluation scripts may run against git revisions while API keys are present.

Mitigation: Do not run evaluation utilities against untrusted revisions, and clear API key environment variables before testing unknown code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/last30days-aisa-zh)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)
- [Skill repository](https://github.com/AIsa-team/agent-skills)
- [AISA API service](https://api.aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown briefs, structured JSON, and concise shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit compact Markdown, full Markdown, context text, or JSON; may save outputs or persist findings to a local SQLite store when requested.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, ClawHub release metadata, and target metadata; pyproject.toml lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
