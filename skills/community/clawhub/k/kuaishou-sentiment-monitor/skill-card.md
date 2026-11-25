## Description:

快手舆情监测助手，可按关键词获取快手作品数据、详情、互动数据和评论数据，并据此分析舆情与输出报告；支持视频搜索、博主作品抓取和视频评论分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

适用于品牌营销人员、内容运营者和市场分析师，通过关键词、公开视频或主页链接收集快手公开作品与评论数据，用于舆情观察、竞品研究和选题分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and target links are sent to the third-party service to retrieve Kuaishou data.

Mitigation: Avoid confidential queries and submit only keywords or links you are authorized to share.

Risk: The security scan did not fully inspect all components, so it cannot rule out issues in scripts that were only partially reviewed.

Mitigation: Review the uninspected scripts before installation if their behavior is material to your use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/kuaishou-sentiment-monitor)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [Service website and token setup](https://www.guaikei.com)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured JSON records with agent-written analysis or a sentiment report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results, creator data, and comments are returned for public Kuaishou content; report conclusions should be grounded in the returned data.]

## Skill Version(s):

1.1.2 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
