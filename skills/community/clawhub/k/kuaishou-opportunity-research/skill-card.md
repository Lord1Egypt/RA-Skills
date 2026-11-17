## Description:

检索快手公开搜索结果、博主作品和视频评论，支持内容选题、增长研究与用户反馈分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、运营人员和市场研究者可用它查询快手公开视频、博主作品及评论，以发现选题方向、分析用户反馈并评估内容机会。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Kuaishou links are sent to Guaikei; its retention practices have not been verified.

Mitigation: Avoid confidential queries unless sharing them with the service is approved.

Risk: Optional local logs can retain queries and results.

Mitigation: Enable logging only when needed and remove temporary logs when finished.

## Reference(s):

- [快手机会研究服务](https://www.guaikei.com)
- [快手选项说明](references/options.md)
- [版本更新日志](references/changelog.md)
- [ClawHub 发布页](https://clawhub.ai/why20261/skills/kuaishou-opportunity-research)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON response envelopes containing public video, comment, creator, and engagement data for agent analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Kuaishou data only; results are not logged by default.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
