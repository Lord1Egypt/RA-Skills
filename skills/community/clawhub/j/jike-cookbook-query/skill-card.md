## Description:

菜谱查询。支持食材列表查询、菜谱搜索、菜谱详情和随机菜谱，返回菜名、分类、耗时、口味、烹饪方式、主料辅料和做法步骤。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up ingredients, search recipes, retrieve full recipe steps by ID, or request random recipe suggestions from Jike cookbook APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookbook search terms, recipe IDs, and the Jike AppKey are sent to the configured API provider.

Mitigation: Install only if this data sharing is acceptable, and keep the AppKey in environment variables rather than embedding it in prompts or shared files.

Risk: The JIKE_API_BASE_URL override can redirect requests and the AppKey to a different server.

Mitigation: Do not set JIKE_API_BASE_URL unless the destination is controlled and validated; prefer the default https://api.jikeapi.cn endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-cookbook-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike cookbook search endpoint](https://api.jikeapi.cn/v1/cookbook/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text tables or JSON from a Python command-line script, with agent-facing Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JIKE_COOKBOOK_QUERY_KEY or JIKE_APPKEY credential.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
