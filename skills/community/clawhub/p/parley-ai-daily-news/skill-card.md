## Description:

每天定时获取AI行业最新资讯，整理为早报并发送给用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

Users and teams who follow the AI industry use this skill to generate a concise Chinese-language morning briefing with major news, technical progress, trend analysis, almanac notes, and a selected Mao anthology quotation. It can run manually or as a scheduled 08:30 Asia/Shanghai announcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled announcements may be sent to the wrong WeCom destination or at an undesired time.

Mitigation: Confirm the destination channel and the 08:30 Asia/Shanghai schedule before enabling the job.

Risk: Generated public-news summaries may be sent automatically without human review.

Mitigation: Use human review or monitoring when publishing to broad audiences, especially for time-sensitive or reputationally sensitive news.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zrxparley/skills/parley-ai-daily-news)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown briefing delivered as an announcement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for a roughly three-minute daily read; scheduled delivery targets WeCom by default.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
