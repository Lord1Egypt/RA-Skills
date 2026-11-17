## Description:

聚合 47 个平台热榜数据的 API 服务。

This skill is for research and development only.

## Publisher:

[rpeng666](https://clawhub.ai/user/rpeng666)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers use this skill to fetch and summarize current trending-list data from social, news, technology, finance, video, and entertainment platforms through a standardized HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts airouter.tech to retrieve public trending-list data.

Mitigation: Use it only where external network access to airouter.tech is acceptable, and avoid placing sensitive text in source IDs or custom API requests.

Risk: Ambiguous news or trend requests could cause an agent to fetch external data when the user did not intend it.

Mitigation: Configure the agent to confirm whether HotRank Hub should be used for broad or ambiguous news-summary requests.

Risk: Trending data comes from third-party platforms and may be incomplete, unavailable, or inaccurate.

Mitigation: Present source names and retrieval context to users, handle failed sources gracefully, and avoid treating trend entries as verified facts.

Risk: Documentation claims 47 supported platforms, while sources.json contains 45 source entries in the artifact evidence.

Mitigation: Verify the active source list before relying on complete platform coverage or advertising an exact source count.

Risk: Repeated polling can waste requests because the service caches data for about 5 minutes and recommends no more than 60 requests per minute.

Mitigation: Cache repeated source requests for about 5 minutes and use batching, backoff, and request deduplication for multi-platform workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rpeng666/skills/hotrankhub)
- [Publisher profile](https://clawhub.ai/user/rpeng666)
- [HotRank Hub API](https://airouter.tech/api)
- [HotRank Hub website](https://airouter.tech)
- [API reference](https://airouter.tech/docs/api)
- [Usage examples](https://airouter.tech/docs/examples)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses and optional code or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill retrieves public trending-list data from airouter.tech and returns current-source results; API data is server-cached for about 5 minutes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
