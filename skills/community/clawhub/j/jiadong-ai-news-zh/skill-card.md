## Description:

中文AI科技日报自动采集与推送。从The Verge、Wired、TechCrunch等英文源抓取最新AI资讯，自动翻译整理为中文，按分类推送到飞书/Telegram/Discord等渠道。适合关注AI行业动态的中文用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiadong0723](https://clawhub.ai/user/jiadong0723)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking AI news readers and operators use this skill to collect public English-language AI news, translate and classify it into a concise Chinese daily briefing, and optionally send it to configured Feishu, Telegram, or Discord channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled delivery could send briefings to an unintended Feishu, Telegram, or Discord destination if channel settings are wrong.

Mitigation: Review the configured channel and cron settings before enabling scheduled delivery.

Risk: Briefings depend on public external news sources and automated translation, so summaries may omit context or reflect source inaccuracies.

Mitigation: Review the generated briefing and source links before using it for business decisions or broad distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiadong0723/skills/jiadong-ai-news-zh)
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence)
- [Wired AI RSS](https://www.wired.com/feed/tag/ai/latest/rss)
- [TechCrunch RSS](https://techcrunch.com/feed/)
- [Anthropic News](https://www.anthropic.com/news)
- [MIT Technology Review RSS](https://www.technologyreview.com/feed/)
- [Google AI Blog](https://blog.google/technology/ai/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown daily briefing with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [8-12 ranked news items with Chinese summaries, category tags, source URLs, and one daily insight.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
