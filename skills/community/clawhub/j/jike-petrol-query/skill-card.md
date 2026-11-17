## Description:

国内油价实时查询。按省份查询 92号汽油、95号汽油、98号汽油和0号柴油价格，也支持不传省份返回全部地区油价。适用场景：用户说“四川今天油价多少”“查一下广东95号汽油价格”“全国油价列表”等。数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current petrol and diesel prices for Chinese provinces or all available regions from the Jike API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can redirect API-key-bearing requests when JIKE_API_BASE_URL is set.

Mitigation: Do not set JIKE_API_BASE_URL for normal use; if testing requires an override, restrict it to an approved HTTPS endpoint.

Risk: The skill sends a Jike AppKey with external API requests.

Mitigation: Use a low-privilege AppKey, keep it in environment configuration, and avoid exposing it in prompts, logs, or shared command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-petrol-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Petrol query API endpoint](https://api.jikeapi.cn/v1/petrol/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash command examples; runtime output is a terminal text table or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike AppKey supplied through JIKE_PETROL_QUERY_KEY, JIKE_APPKEY, --key, or a local .env file.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
