## Description: <br>
输入中文姓氏后查询姓氏起源、名人、迁徙分布等信息，数据由即刻数据开放接口提供。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to answer Chinese surname questions with origin, notable-person, and migration/distribution details from Jike Data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Surname queries and the Jike AppKey are sent to Jike's external API. <br>
Mitigation: Use a dedicated API key and avoid exposing the key in logs, screenshots, or shared command output. <br>
Risk: Changing JIKE_API_BASE_URL can redirect requests to an alternate API endpoint. <br>
Mitigation: Leave JIKE_API_BASE_URL unset unless the alternate endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-surname-query) <br>
- [Jike Data homepage](https://www.jikeapi.cn/) <br>
- [Jike surname query API endpoint](https://api.jikeapi.cn/v1/surname/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain Chinese text by default, or JSON when the --json flag is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a Jike AppKey configured with JIKE_SURNAME_QUERY_KEY, JIKE_APPKEY, or the --key option.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
