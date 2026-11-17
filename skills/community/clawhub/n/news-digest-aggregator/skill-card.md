## Description:

Daily automated news digest that fetches configured RSS feeds, creates brief article digests, and delivers formatted updates to Discord, Slack, or Feishu on a schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure RSS sources, generate daily news digests, and send the resulting updates to team messaging channels. It is suited to scheduled content delivery workflows that rely on trusted feed and webhook configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can install unpinned Python packages at runtime.

Mitigation: Preinstall reviewed, pinned dependencies in a controlled environment before running the skill.

Risk: The skill fetches RSS feeds and posts digest content to user-configured network URLs.

Mitigation: Use only trusted RSS feeds and webhook destinations, and avoid running it with access to internal networks or sensitive environment variables.

Risk: Recurring delivery can repeatedly publish incorrect, stale, or unintended digest content.

Mitigation: Review the cron schedule, channel selection, and destination credentials before enabling automated delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/news-digest-aggregator)
- [Publisher profile](https://clawhub.ai/user/cp3d1455926-svg)
- [RSS source configuration](references/sources.json)
- [TechCrunch RSS feed](https://techcrunch.com/feed/)
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml)
- [Reuters Technology RSS feed](https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best)
- [Hacker News RSS feed](https://news.ycombinator.com/rss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest text with shell command and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts digest content to a selected Discord, Slack, or Feishu webhook when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
