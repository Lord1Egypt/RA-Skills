## Description:

通过命令行检索快手公开视频、博主作品和评论数据，并以 JSON 返回。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌营销人员和市场分析师可用它检索快手公开视频、查看博主公开作品和视频评论，辅助选题研究、竞品监测和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and links are sent to the third-party Guaikei service.

Mitigation: Avoid sending confidential or sensitive query terms.

Risk: The security review had medium confidence and only partially analyzed the code.

Mitigation: Review the skill code before installation if the remaining uncertainty is material to your use.

## Reference(s):

- [使用选项](references/options.md)
- [更新日志](references/changelog.md)
- [快手数据智能助手官网与 API Token](https://www.guaikei.com)
- [ClawHub 发布页](https://clawhub.ai/why20261/skills/kuaishou-data-research)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON response envelope containing video, creator, or comment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; results are returned on stdout. Retrieval limits depend on the API token plan.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
