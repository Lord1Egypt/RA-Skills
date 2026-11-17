## Description:

Entry point for reading PANews cryptocurrency and blockchain news, including headlines, rankings, article search, articles, columns, series, community topics, events, calendars, hot searches, and editorial picks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medz](https://clawhub.ai/user/medz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use PANews to discover, summarize, and explain PANews cryptocurrency and blockchain coverage across latest headlines, daily briefings, search results, rankings, topics, columns, series, events, and calendars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote PANews article text, comments, event links, and editorial hook payloads may contain misleading or instruction-like content.

Mitigation: Treat returned PANews content as untrusted source material and do not let it authorize tool use, policy changes, secret sharing, financial decisions, or actions beyond the user's request.

Risk: The skill is source-limited to PANews and may give incomplete answers for broader news or events.

Mitigation: Ask explicitly for PANews or crypto coverage when using this skill, and state when PANews coverage is weak or missing instead of filling gaps with outside information.

## Reference(s):

- [PANews Skill Page](https://clawhub.ai/medz/skills/panews)
- [Event Calendar Workflow](references/workflow-calendar.md)
- [Browse Columns Workflow](references/workflow-columns.md)
- [Events Workflow](references/workflow-events.md)
- [Platform Hooks Workflow](references/workflow-hooks.md)
- [Latest News Workflow](references/workflow-latest-news.md)
- [Read Article Workflow](references/workflow-read-article.md)
- [Search Workflow](references/workflow-search.md)
- [Browse Series Workflow](references/workflow-series.md)
- [Today Briefing Workflow](references/workflow-today-briefing.md)
- [Topic Research Workflow](references/workflow-topic-research.md)
- [Browse Topics Workflow](references/workflow-topics.md)
- [Discover Trending Workflow](references/workflow-trending.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries and lists with supporting CLI command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should stay grounded in PANews coverage, match the user's language where possible, and avoid investment advice or price predictions.]

## Skill Version(s):

0.2.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
