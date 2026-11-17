## Description:

行业情报官 - 定时采集 GitHub Trending、X(Twitter)、知乎、36kr、掘金等平台热点，AI 摘要后推送到指定渠道。集成 fxtwitter API 和 RSSHub。

This skill is ready for commercial/non-commercial use.

## Publisher:

[muisenice](https://clawhub.ai/user/muisenice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure recurring industry-intelligence collection, summarization, deduplication, history retention, and delivery to collaboration or messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses webhook, bot, API, SMTP, and scheduled-delivery configuration that can expose credentials or send information to unintended destinations if misconfigured.

Mitigation: Configure only intended delivery destinations, use least-privilege webhook or bot credentials, avoid committing secrets to files, and test with dry-run mode before enabling cron delivery.

Risk: Scheduled collection and local history retention can accumulate source data, summaries, logs, and cache entries over time.

Mitigation: Review the configured sources, retention locations, and generated history files before production use, and keep only the sources and records needed for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muisenice/skills/openclaw-intelligence-officer)
- [RSSHub](https://github.com/DIYgod/RSSHub)
- [Huginn](https://github.com/huginn/huginn)
- [TrendRadar](https://github.com/sansan0/TrendRadar)
- [GitHub Trending weekly](https://github.com/trending?since=weekly)
- [Zhihu hot list](https://www.zhihu.com/hot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local history, cache, log, and summary files under memory/intelligence when implemented by the agent.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
