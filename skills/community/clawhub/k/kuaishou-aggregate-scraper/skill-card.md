## Description:

快手全场景数据查询助手，支持 App 和 Web 双端 API，覆盖视频详情、用户数据、搜索、热榜、直播、评论等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, and analysts use this skill to query Kuaishou video, user, search, trend, live, and comment data through MaxHub APIs and produce concise browse, analysis, or comparison reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou links, IDs, search terms, and account-linked API activity are sent to MaxHub at www.aconfig.cn.

Mitigation: Install and use the skill only when this data sharing is acceptable, and avoid sending unrelated secrets or sensitive private identifiers.

Risk: The artifact includes cross-platform fallback paths that may route some fallback behavior through Douyin endpoints.

Mitigation: Review or remove the Douyin fallback mappings before authorizing Kuaishou-only use.

Risk: Broad activation behavior could lead the agent to call APIs for loosely matched video or social-data requests.

Mitigation: Confirm the request is a Kuaishou or MaxHub data task and review planned API calls before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/kuaishou-aggregate-scraper)
- [Publisher profile](https://clawhub.ai/user/new-ironman)
- [MaxHub API website](https://www.aconfig.cn)
- [User Data API](references/api-user.md)
- [Video & Content API](references/api-video.md)
- [Parameter Mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown responses with tables, summaries, and optional curl commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MAXHUB_API_KEY for authenticated read-only MaxHub API requests and returns data-driven summaries in Chinese or English to match the user.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
