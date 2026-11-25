## Description:

搜索快手公开视频、博主作品和视频评论，并按关键词、热度、发布时间与时长筛选。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

创作者、品牌运营人员和分析人员可用它发现快手公开内容趋势、查看博主作品，并汇总视频评论。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and Kuaishou links are sent to www.guaikei.com to perform queries.

Mitigation: Avoid sending confidential or sensitive terms and links unless you are comfortable sharing them with the provider.

## Reference(s):

- [完整选项说明](references/options.md)
- [更新日志](references/changelog.md)
- [Token 开通与服务支持](https://www.guaikei.com)
- [ClawHub 技能页面](https://clawhub.ai/why20261/skills/kuaishou-videos-search)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON result envelope containing video search results, creator profile and posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include status and request metadata; the selected command determines the result fields.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
