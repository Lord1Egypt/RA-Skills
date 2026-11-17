## Description:

实时搜索快手公开视频、作品互动数据与视频评论，支持关键词搜索、博主作品查询和评论分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌运营人员和分析师可通过关键词搜索、博主公开作品查询及视频评论，了解快手公开内容的表现与讨论情况。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and Kuaishou links may be sent to www.guaikei.com.

Mitigation: Before querying, confirm the keyword or link is appropriate to share with that service, and use the skill only for public Kuaishou content.

Risk: The skill requires an API token and reports timestamps in Beijing time.

Mitigation: Keep GUAIKEI_API_TOKEN private and account for the displayed timezone when interpreting results.

## Reference(s):

- [使用选项说明](artifact/references/options.md)
- [更新日志](artifact/references/changelog.md)
- [服务与令牌开通](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/kuaishou-social-media-search)
- [Publisher profile](https://clawhub.ai/user/why20261)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [JSON result envelope with video, creator, engagement, and comment data, summarized in natural language by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monthly-token limits are 30 search results, 50 creator works, and 60 comments; pay-as-you-go supports up to 10,000 where allowed.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog released 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
