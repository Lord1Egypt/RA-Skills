## Description:

针对任意关键词获取快手作品、互动和评论数据，并据此分析舆情健康、情感占比、负面信息、事件时间、热度排行与竞品口碑，形成舆情报告；支持按点赞数、发布时间和视频时长筛选关键词搜索结果、按主页链接获取公开作品列表，以及按视频链接获取评论与互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、品牌营销人员和市场分析师可用此技能检索快手公开视频、博主作品及评论，辅助选题调研、竞品观察和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 查询会将搜索关键词或账号、视频链接发送至 guaikei.com。

Mitigation: 使用前告知相关人员数据去向，并避免提交机密的监测目标。

## Reference(s):

- [完整选项说明](references/options.md)
- [更新日志](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [结构化 JSON 数据及基于结果生成的自然语言分析或舆情报告]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [仅查询公开数据；结果数量受 Token 套餐限制。]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
