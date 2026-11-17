## Description:

输入关键词、快手账号主页链接或视频链接，搜索公开作品、查看博主作品并分析视频评论，返回结构化结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

快手内容创作者、运营人员、品牌营销人员和市场分析师可用此技能搜索公开视频、查看博主作品及分析评论，为选题调研、竞品分析和评论趋势了解提供数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied links are sent to guaikei.com; only 20 of 32 components received a complete security inspection.

Mitigation: Use non-sensitive search terms and public Kuaishou links, and review the skill before installation.

Risk: Returned timestamps use a fixed Beijing-time format.

Mitigation: Interpret timestamps as Beijing time when comparing results with local records.

## Reference(s):

- [完整选项参数说明](references/options.md)
- [快手作品批量下载服务](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results, public creator posts, or video comments with available engagement data and links.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
