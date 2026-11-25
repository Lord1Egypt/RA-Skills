## Description:

帮助内容运营者检索快手公开视频、博主作品和评论，并获取结构化数据用于选题、竞品与舆情分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、品牌运营者和市场分析人员可用它搜索快手公开视频、查看博主公开作品及视频评论，以支持选题调研、竞品分析和舆情观察。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and video or profile links are sent to guaikei.com to retrieve public data.

Mitigation: Avoid sending sensitive keywords or links; use only information appropriate to share with the service.

Risk: The security review is partial with medium confidence; its guidance also flags broad activation wording.

Mitigation: Treat the benign verdict as an incomplete review, inspect the skill before installation, and confirm each invocation matches the user's public-data search or analysis request.

## Reference(s):

- [完整选项说明](references/options.md)
- [更新日志](references/changelog.md)
- [官网与 Token 开通](https://www.guaikei.com)
- [ClawHub 发布页](https://clawhub.ai/why20261/skills/kuaishou-competitor-analysis)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [JSON envelope with video search, creator post, or comment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status and error details; per-month limits are 30 search results, 50 posts, and 60 comments.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
