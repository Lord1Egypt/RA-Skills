## Description:

检索快手公开视频、博主作品和视频评论，帮助归纳用户反馈、消费顾虑及内容趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌营销人员和市场分析师可检索快手公开视频及评论，了解用户需求、竞品内容和反馈，以支持选题、产品改进及客服准备。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, Kuaishou links and the API token are sent to a third-party service.

Mitigation: Confirm the service and data-sharing scope before use; keep the token confidential.

Risk: Fetched public comments and creator or search data are retained locally.

Mitigation: Review and clear the logs/ directory when research targets or results are sensitive.

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/why20261/skills/kuaishou-comment-consumer-insights)
- [参数说明](references/options.md)
- [更新日志](references/changelog.md)
- [GUAIKEI API 服务](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON results with optional brief text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, creator-post and comment results include a status; fetched results are also saved locally under logs/.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
