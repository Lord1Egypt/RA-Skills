## Description:

查询快手公开作品、用户、评论、搜索、热榜和直播数据，并帮助分析内容趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

快手内容创作者、运营人员和市场分析师可用它查询公开作品与账号数据、跟踪热门内容，并整理内容表现和趋势分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is marked suspicious and partial; it reports unclear compliance-record writes, broad triggers, and an unpinned installer.

Mitigation: Review the complete release, clarify any local file changes, narrow triggers, and pin a reviewed version before installation.

Risk: Requests send the API key and supplied identifiers, keywords, URLs, or optional cookies or tokens to the MaxHub service.

Mitigation: Use only authorized data and credentials, avoid third-party cookies or tokens, and keep secrets out of logs and prompts.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-kuaishou)
- [ClawHub release page](https://clawhub.ai/xiewxx/skills/maxhub-kuaishou-pro)
- [MaxHub API service](https://www.aconfig.cn)
- [Endpoint whitelist](references/endpoints_whitelist.yaml)
- [Query recipes](references/recipes/_index.md)
- [Data usage policy](DATA_USAGE_POLICY.md)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Text, Markdown, JSON]

**Output Format:** [Markdown summaries and structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query results depend on fields returned by the MaxHub API.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
