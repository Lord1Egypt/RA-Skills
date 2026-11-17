## Description:

Lemon8 内容数据查询助手，覆盖搜索、发现页、帖子详情、用户信息、评论、话题和热搜数据查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to query Lemon8 content, user, topic, comment, trending, and discovery data through MaxHub APIs. It supports lifestyle trend research, content analysis, user lookup, and share-link ID extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Under-disclosed fallback behavior may route failed Lemon8 requests to unrelated Douyin endpoints.

Mitigation: Before deployment, remove the Douyin fallback paths or explicitly document them and restrict automatic fallback to reviewed endpoints.

Risk: Lemon8 search terms, share links, content IDs, user IDs, profile requests, and follower-list requests are sent to MaxHub/aconfig.cn with the user's API key.

Mitigation: Use only with data users are permitted to submit to MaxHub, keep MAXHUB_API_KEY secret, and avoid pasting sensitive personal or proprietary inputs.

Risk: The skill relies on a third-party API service and may return unavailable, incomplete, or changed endpoint behavior.

Mitigation: Handle API errors explicitly, avoid blind retries, and verify endpoint paths and parameters against the bundled reference files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/lemon8-aggregate-scraper)
- [Publisher profile](https://clawhub.ai/user/new-ironman)
- [MaxHub API website](https://www.aconfig.cn)
- [Search & Discover API](references/api-search-discover.md)
- [Post & User API](references/api-post-user.md)
- [Parameter Mappings](references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries, tables, setup guidance, and shell command snippets for API usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output should match the user's language, avoid exposing API keys, and base conclusions on returned API data.]

## Skill Version(s):

3.6.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
