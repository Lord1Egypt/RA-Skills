## Description:

通过关键词搜索、创作者主页和视频链接获取快手公开作品与评论数据，支持内容选题、竞品研究和舆情分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

快手品牌方、内容创作者、营销人员和分析师可用此技能搜索公开视频、查看创作者作品与评论互动数据，支持选题研究、竞品分析和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and account or video links are sent to a third-party service and could reveal sensitive interests.

Mitigation: Use non-sensitive keywords and public account or video links; avoid requests that disclose confidential interests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-insight)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [Guaikei service](https://www.guaikei.com)
- [Command options](references/options.md)
- [Release changelog](references/changelog.md)
- [Output envelope schema](assets/output_envelope.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retrieves public Kuaishou search, creator, and comment data; requires Node.js and a GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
