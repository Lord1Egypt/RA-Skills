## Description:

唐诗宋词元曲查询，支持古诗词列表、详情、诗人查询、诗人详情、随机诗词、词牌信息、朝代列表、类别列表和体裁列表，数据由即刻数据开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to query Chinese classical poetry, poet details, poetic forms, dynasties, categories, and genres through the JikeAPI poetry service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API key and poetry query terms are sent to the JikeAPI service, and the security evidence notes that an endpoint override can redirect API-key-bearing requests.

Mitigation: Use a limited, revocable JikeAPI key, keep JIKE_API_BASE_URL unset or pinned to https://api.jikeapi.cn, and avoid running the skill where untrusted users can set environment variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-poetry-query)
- [JikeAPI homepage](https://www.jikeapi.cn/)
- [JikeAPI poetry query endpoint](https://api.jikeapi.cn/v1/poetry/query)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text tables or JSON from command-line API queries, with Markdown usage examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JikeAPI AppKey via JIKE_POETRY_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
