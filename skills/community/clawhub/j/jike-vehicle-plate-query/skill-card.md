## Description:

车牌号码归属地。输入车牌号码或至少前两位车牌前缀，查询车牌前缀、省份简称、省份和城市。适用场景：用户说“陕C 是哪里的车牌”“查一下陕C88888 归属地”“这个车牌属于哪个城市”等。数据由即刻数据（jikeapi.cn）开放接口提供。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese vehicle plate origin questions by querying a plate number or at least its first two-character prefix. It returns the plate prefix, province abbreviation, province, and city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can use JIKE_API_BASE_URL to send the API key and queried plate value to an unexpected endpoint.

Mitigation: Keep JIKE_API_BASE_URL unset or restrict it to the official Jike API host before running the skill.

Risk: Passing the Jike API key on the command line can expose it through shell history or process listings.

Mitigation: Use a dedicated API key supplied through JIKE_VEHICLE_PLATE_QUERY_KEY or JIKE_APPKEY instead of the --key argument.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jikeapi-cn/skills/jike-vehicle-plate-query)
- [Jike Data Homepage](https://www.jikeapi.cn/)
- [Jike Vehicle Plate Query API Endpoint](https://api.jikeapi.cn/v1/vehicle/plate/query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, API Calls, Guidance]

**Output Format:** [Plain text or JSON from a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Jike API key through JIKE_VEHICLE_PLATE_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
