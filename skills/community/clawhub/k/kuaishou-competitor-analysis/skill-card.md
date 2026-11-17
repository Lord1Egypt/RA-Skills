## Description:

按关键词搜索快手公开视频、获取博主公开作品并查看视频评论，为竞品分析、选题调研和舆情监控提供结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、品牌营销人员、市场分析师和运营团队可用它检索快手公开视频、查看博主公开作品与视频评论，并为选题、竞品观察和舆情分析整理数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and submitted links are sent to www.guaikei.com; ClawScan notes that disclosure clarity is a concern.

Mitigation: Only submit queries and links you are authorized to share, and avoid confidential search terms.

Risk: ClawScan reports that 12 of 32 components were only partially inspected.

Mitigation: Review the skill and its data-handling behavior before installation, especially for components not fully inspected.

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/why20261/skills/kuaishou-competitor-analysis)
- [瓜科易服务与 Token 开通](https://www.guaikei.com)
- [完整选项说明](references/options.md)
- [更新日志](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON response envelopes containing public video, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results and quantity depend on the query and API plan; response fields are documented in the bundled JSON schemas.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
