## Description:

查询 IPv6 地址的国家、省份、城市、地区、运营商和 long_ip 数值，数据由即刻数据（jikeapi.cn）接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to validate an IPv6 address, call JikeAPI with an AppKey, and return location and ISP details to a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried IPv6 addresses and the JikeAPI AppKey are sent to the provider during lookups.

Mitigation: Use the skill only when sharing those IPv6 addresses and the AppKey with JikeAPI is acceptable, and scope or rotate the AppKey according to local policy.

Risk: The JIKE_API_BASE_URL environment variable can redirect requests, including the AppKey and queried IP, away from the intended API host.

Mitigation: Keep JIKE_API_BASE_URL unset in normal use, or restrict it to the legitimate HTTPS JikeAPI host before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-ip-query-v6)
- [JikeAPI homepage](https://www.jikeapi.cn/)
- [JikeAPI IPv6 query endpoint](https://api.jikeapi.cn/v1/ip/query/v6)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JikeAPI AppKey via JIKE_IP_QUERY_V6_KEY, JIKE_APPKEY, or the script --key option.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
