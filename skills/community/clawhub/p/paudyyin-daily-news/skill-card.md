## Description:

每日新闻自动采集与报告生成。使用 web_search (freshness=oneDay) 替代旧版 Bing/Tavily 方案，确保新闻均为24小时内真实最新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and automation operators use this skill to generate a Chinese daily news digest from recent web search results across global and China politics, finance, AI, technology, and consumer electronics categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run on the disclosed weekday schedule and perform web searches without a manual trigger.

Mitigation: Confirm the OpenClaw cron schedule before enabling the skill, and disable or adjust it if unattended weekday execution is not desired.

Risk: News digests generated from web search can include outdated, incomplete, or misleading items despite the one-day freshness filter.

Mitigation: Review important items against their original sources before using the report for decisions or redistribution.

Risk: Dated Markdown report archives may retain generated news content in memory.

Mitigation: Review retention expectations for memory/daily_news_{YYYY-MM-DD}.md archives and remove stored reports when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/paudyyin-daily-news)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown daily news report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated report archive path: memory/daily_news_{YYYY-MM-DD}.md when supported by the agent environment.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
