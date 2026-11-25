## Description:

快手高赞视频搜索工具。支持关键词获取快手实时高赞视频数据，助力创作者发现热门趋势、获取创作灵感。支持关键词搜索视频、获取达人公开作品和分析视频评论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use this skill to find popular Kuaishou videos, review public creator posts, and inspect video comments for topic research, competitor analysis, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and video or creator links are sent to Guaikei's service for processing.

Mitigation: Use public Kuaishou content and avoid sending sensitive keywords or links.

Risk: The security scan is incomplete: 20 of 32 components were fully inspected, and tool-misuse analysis was degraded.

Mitigation: If stronger assurance is needed, wait for a more complete scan and review the skill before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/kuaishou-video-search)
- [Guaikei service website](https://www.guaikei.com)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON envelopes containing public video, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited by the selected count and API plan; only public Kuaishou data is supported.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
