## Description:

获取小红书博主公开作品及单篇笔记的真实点赞、评论、收藏数据，帮助评估互动质量、筛选 KOL、分析竞品和监控内容趋势。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content creators, brand marketers, market researchers, data analysts, MCN teams, and creator managers use this skill to retrieve public Xiaohongshu note, comment, keyword-search, and creator-post data for marketing and partnership decisions. It is intended for public data workflows and not for private, hidden, login-only, posting, liking, following, or commenting actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, links, and public-content results to guaikei.com using GUAIKEI_API_TOKEN.

Mitigation: Install only when this data flow is acceptable, keep the token secret, and rotate it if command inputs or URLs may have been logged by infrastructure.

Risk: Successful runs automatically save full returned data to a local logs directory.

Mitigation: Delete or protect saved logs when they contain sensitive campaign, creator, or analysis data.

Risk: The skill is limited to public Xiaohongshu data and does not support private, hidden, or login-only data.

Mitigation: Use it only for public-data workflows and avoid using outputs as evidence for data the tool cannot access.

## Reference(s):

- [小红书洞察与竞品分析助手 · 参数与调用说明](references/options.md)
- [技能更新日志](references/changelog.md)
- [Guaikei API service](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-creator-notes-collector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful runs save returned data under the local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
