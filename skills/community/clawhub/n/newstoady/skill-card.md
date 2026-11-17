## Description:

NewsToday aggregates, deduplicates, and summarizes important news into readable bilingual briefings with optional scheduled push alerts and topic preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use NewsToday to request on-demand daily news, topical tracking, and bilingual morning or evening briefings. Registered users can manage topic preferences and optional scheduled push alerts across supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query public web and RSS sources, so briefings may reflect unavailable, stale, or inconsistent third-party news feeds.

Mitigation: Review source attribution in generated briefings and replace or disable RSS feeds that are unreliable or only available over HTTP.

Risk: When push is explicitly enabled, the skill creates recurring scheduled jobs that message the selected channel.

Mitigation: Enable push only for intended recipients, check status after setup, and use the provided off command when scheduled briefings are no longer wanted.

Risk: Registered users store local topic preferences and delivery settings.

Mitigation: Store only required preferences, use sanitized user identifiers, and remove the local profile when personalization is no longer needed.

## Reference(s):

- [NewsToday ClawHub skill page](https://clawhub.ai/jiajiaoy/skills/newstoady)
- [Publisher profile](https://clawhub.ai/user/jiajiaoy)
- [OpenClaw](https://openclaw.ai)
- [Sina News RSS](https://rss.sina.com.cn/news/china/focus15.xml)
- [The Paper RSS](https://www.thepaper.cn/rss_promotion.jsp)
- [36Kr RSS](https://36kr.com/feed)
- [BBC Chinese RSS](https://feeds.bbci.co.uk/zhongwen/simp/rss.xml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and OpenClaw scheduling directives]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese or English output; optional scheduled jobs can deliver briefings to Telegram, Feishu, Slack, or Discord.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
