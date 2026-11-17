## Description:

Industry News Agent fetches technology, finance, and science articles from configurable RSS feeds from the last 24 hours, filters them by keywords, and formats a concise news digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop)

### License/Terms of Use:

MIT-0

## Use Case:

People tracking technology and industry developments use this skill to fetch recent articles from configured RSS feeds, filter by keywords, and produce a digest for manual review or scheduled delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented cron command can create a persistent daily job.

Mitigation: Use manual execution unless scheduled delivery is intended, and inspect or remove the crontab entry when the skill is no longer needed.

Risk: Configurable RSS sources allow broad outbound fetching.

Mitigation: Keep RSS sources limited to trusted public feed URLs and review feed changes before running the skill.

Risk: When keyword filtering finds no matches, the script may return recent articles that did not match the configured keywords.

Mitigation: Review generated digests before sharing or acting on them, and tune include and exclude keywords for the intended topic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongrebeccahhh-boop/skills/industry-news-agent)
- [36Kr RSS feed](https://36kr.com/feed)
- [Huxiu RSS feed](https://www.huxiu.com/rss/0.xml)
- [Leiphone RSS feed](https://www.leiphone.com/feed)
- [SSPai RSS feed](https://sspai.com/feed)
- [ifanr RSS feed](https://www.ifanr.com/feed)
- [FT Chinese RSS feed](https://www.ftchinese.com/rss/news)
- [ScienceDaily RSS feed](https://www.sciencedaily.com/rss/all.xml)
- [Nature RSS feed](https://www.nature.com/nature.rss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown-style news digest with article titles, dates, sources, summaries, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable RSS sources, include and exclude keywords, per-source limits, and total result limit.]

## Skill Version(s):

3.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
