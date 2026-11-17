## Description:

查询指定生肖的五行、本命佛、出生年份、幸运数字、幸运花、性格、事业、爱情和运势，数据由即刻数据开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer Chinese zodiac lookup requests by calling Jike's zodiac API and returning readable Chinese text or structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can use JIKE_API_BASE_URL from the environment, so a misconfigured environment could send query terms and the AppKey to an unintended endpoint.

Mitigation: Keep JIKE_API_BASE_URL unset or lock it to https://api.jikeapi.cn before running the skill.

Risk: The AppKey is placed in the request URL when the script calls the API.

Mitigation: Use a scoped or rotatable Jike AppKey and avoid sharing command output, logs, or network traces that may include request URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-chinese-zodiac-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike Chinese zodiac API endpoint](https://api.jikeapi.cn/v1/chinese_zodiac)
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Chinese plain text by default, or JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike AppKey supplied through JIKE_CHINESE_ZODIAC_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
