## Description:

查询中超、英超、意甲、德甲、法甲、西乙、苏超等足球联赛的赛程、比赛结果和积分榜，并通过聚合数据 API 返回实时信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer football league schedule, result, and standings questions after configuring a Juhe football API key. Agents can present the returned schedule or ranking data as readable text, Markdown, or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Juhe API key to API endpoints over plaintext HTTP.

Mitigation: Change Juhe API calls to HTTPS before deployment and rotate any key already used with the plaintext HTTP endpoints.

Risk: Documented key-handling options include passing the API key on the command line or storing it in a .env file under the skill directory.

Mitigation: Prefer a runtime environment variable or secret manager, avoid command-line secrets, and keep local .env files out of shared artifacts.

## Reference(s):

- [Juhe Football API Documentation](https://www.juhe.cn/docs/api/id/90)
- [Juhe Data Platform](https://www.juhe.cn)
- [ClawHub Skill Page](https://clawhub.ai/juhemcp/skills/juhe-football-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or terminal text with optional JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_FOOTBALL_KEY credential; results depend on the Juhe football API response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
