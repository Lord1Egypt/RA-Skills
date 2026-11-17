## Description:

分析快手各垂类行业视频和达人趋势，输出市场机会与风险。当用户询问快手市场规模、类目增长或达人结构时使用。支持三大能力：(1) 关键词搜索视频，可按点赞数、发布时间、视频时长筛选排序；(2) 博主作品抓取，按主页链接获取公开作品列表；(3) 视频评论分析，按视频链接获取评论内容与互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

外部内容创作者、品牌营销人员和市场分析师可用它搜索快手公开视频、查看公开博主作品和分析视频评论，为选题、竞品研究、达人筛选及舆情判断收集数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or creator links are sent to the third-party guaikei.com service.

Mitigation: Submit only queries and links that are appropriate to share with that provider.

Risk: Large result requests may incur plan costs or exceed plan-specific limits.

Mitigation: Check plan limits and costs before requesting large result sets; lower the requested limit or ask the user before upgrading.

Risk: When optional logging is enabled, queries and results are retained in local temporary-directory logs until removed.

Mitigation: Keep optional logging disabled unless needed and remove retained logs when they are no longer required.

## Reference(s):

- [完整选项说明](references/options.md)
- [版本更新日志](references/changelog.md)
- [快手数据服务与令牌开通](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON query results with concise Chinese trend and market guidance when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves public Kuaishou video, creator, and comment data; result counts are subject to token plan limits.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog released 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
