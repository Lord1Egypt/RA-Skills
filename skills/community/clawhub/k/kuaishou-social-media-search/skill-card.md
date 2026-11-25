## Description:

实时搜索快手公开视频、达人作品和评论数据，提供内容、互动与趋势信息，支持品牌、话题和内容表现分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

快手内容创作者、品牌营销人员和市场分析师可用它搜索公开视频、查看博主作品与评论，并分析互动表现和内容趋势。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and video or profile links are sent to the third-party Guaikei service.

Mitigation: Use non-sensitive search terms and public links; avoid sending confidential or personal information.

Risk: Some executable files received only partial inspection in the security scan.

Mitigation: Review the skill files before running them in environments with sensitive data or elevated access.

## Reference(s):

- [Options reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei service and support](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [JSON data for public video search, creator posts, and comments, with concise natural-language analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on public content availability, configured API access, and account plan limits.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
