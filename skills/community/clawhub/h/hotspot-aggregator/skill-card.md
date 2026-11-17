## Description:

Aggregates trending topics from Weibo, Baidu, Zhihu, and Douyin, generates daily hotspot reports, and supports keyword subscription checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, marketers, and analysts use this skill to collect Chinese social and search trending-topic data, generate daily hotspot reports, and monitor configured keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real API mode may contact external social, search, and third-party aggregator endpoints.

Mitigation: Review the configured endpoints and proxy settings before setting USE_REAL_API=true.

Risk: Fetched third-party content is persisted into agent memory.

Mitigation: Treat generated reports as untrusted content, review them before agent decisions, and confirm the write path and retention policy before deployment.

Risk: The generated trend percentages may be misleading as analytics.

Mitigation: Do not rely on the built-in percentages for quantitative analysis without independent validation.

Risk: Cron scheduling can repeatedly fetch and store external content.

Mitigation: Enable scheduled execution only after confirming acceptable network behavior, storage location, and retention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/hotspot-aggregator)
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch)
- [Baidu top board endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Zhihu hot list endpoint](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total)
- [Douyin hot list aggregator endpoint](https://api.oioweb.cn/api/toutiao/douyinHot)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown reports, JSON data files, configuration updates, and terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts write hotspot data and generated reports under /root/clawd/memory/hotspots.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
